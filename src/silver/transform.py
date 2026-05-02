import pandas as pd
import numpy as np
from datetime import datetime, timezone

from src.utils.logger import get_logger
from src.utils.validators import validate_silver
from src.utils.config import AppConfig

logger = get_logger(__name__)

CONSTANT_COLUMNS = ["EmployeeCount", "Over18", "StandardHours"]

ORDINAL_MAPPINGS = {
    "Education": {1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor"},
    "EnvironmentSatisfaction": {1: "Low", 2: "Medium", 3: "High", 4: "Very High"},
    "JobInvolvement": {1: "Low", 2: "Medium", 3: "High", 4: "Very High"},
    "JobSatisfaction": {1: "Low", 2: "Medium", 3: "High", 4: "Very High"},
    "PerformanceRating": {1: "Low", 2: "Good", 3: "Excellent", 4: "Outstanding"},
    "RelationshipSatisfaction": {1: "Low", 2: "Medium", 3: "High", 4: "Very High"},
    "WorkLifeBalance": {1: "Bad", 2: "Good", 3: "Better", 4: "Best"},
}


class SilverTransformer:
    """Cleans, validates, and enriches bronze data into the silver layer."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.silver_path = config.paths.silver

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Starting silver transformation")
        df = df.copy()

        df = self._remove_constants(df)
        df = self._encode_binary(df)
        df = self._cast_categoricals(df)
        df = self._add_ordinal_labels(df)
        df = self._engineer_features(df)
        df = self._add_metadata(df)

        result = validate_silver(df)
        if not result.passed:
            for f in result.failures:
                logger.error(f"Silver validation failure: {f}")
            raise ValueError(f"Silver layer failed validation: {result.failures}")

        logger.info("Silver validation passed")
        self._write_silver(df)
        logger.info(f"Silver complete: {len(df):,} rows x {df.shape[1]} columns")
        return df

    def _remove_constants(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = [c for c in CONSTANT_COLUMNS if c in df.columns]
        logger.info(f"Dropping constant columns: {cols}")
        return df.drop(columns=cols)

    def _encode_binary(self, df: pd.DataFrame) -> pd.DataFrame:
        # Encode to int so downstream numeric operations work cleanly
        df["Attrition"] = (df["Attrition"] == "Yes").astype(int)
        df["OverTime"] = (df["OverTime"] == "Yes").astype(int)
        df["Gender"] = (df["Gender"] == "Male").astype(int)  # 1 = Male, 0 = Female
        return df

    def _cast_categoricals(self, df: pd.DataFrame) -> pd.DataFrame:
        cats = ["BusinessTravel", "Department", "EducationField", "JobRole", "MaritalStatus"]
        for col in cats:
            if col in df.columns:
                df[col] = df[col].astype("category")
        return df

    def _add_ordinal_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        for col, mapping in ORDINAL_MAPPINGS.items():
            if col in df.columns:
                df[f"{col}_Label"] = df[col].map(mapping)
        return df

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        sat_cols = ["EnvironmentSatisfaction", "JobSatisfaction",
                    "RelationshipSatisfaction", "WorkLifeBalance"]
        df["SatisfactionComposite"] = df[sat_cols].mean(axis=1).round(2)

        # Average tenure per employer — high values indicate loyalty or stagnation
        df["YearsPerCompany"] = np.where(
            df["NumCompaniesWorked"] > 0,
            (df["TotalWorkingYears"] / df["NumCompaniesWorked"]).round(2),
            df["TotalWorkingYears"],
        )

        # How much an employee earns vs the median for their job level
        level_median = df.groupby("JobLevel")["MonthlyIncome"].transform("median")
        df["IncomeVsLevelMedian"] = (
            (df["MonthlyIncome"] - level_median) / level_median
        ).round(4)

        # Ratio of years since promotion to total tenure — captures stagnation
        df["PromotionLag"] = (
            df["YearsSinceLastPromotion"] / df["YearsAtCompany"].clip(lower=1)
        ).round(4)

        # Stability of current manager relationship
        df["ManagerTenureRatio"] = (
            df["YearsWithCurrManager"] / df["YearsAtCompany"].clip(lower=1)
        ).round(4)

        df["DistanceTier"] = pd.cut(
            df["DistanceFromHome"],
            bins=[0, 5, 10, 20, 100],
            labels=["Near", "Moderate", "Far", "Very Far"],
        )

        df["AgeBand"] = pd.cut(
            df["Age"],
            bins=[17, 25, 35, 45, 55, 100],
            labels=["18-25", "26-35", "36-45", "46-55", "55+"],
        )

        return df

    def _add_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        df["_silver_ts"] = datetime.now(timezone.utc).isoformat()
        return df

    def _write_silver(self, df: pd.DataFrame) -> None:
        self.silver_path.mkdir(parents=True, exist_ok=True)
        path = self.silver_path / "employee_attrition_silver.parquet"
        df.to_parquet(path, index=False, engine="pyarrow")
        logger.info(f"Silver parquet written: {path}")
