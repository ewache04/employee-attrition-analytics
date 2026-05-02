import pandas as pd
import numpy as np

from src.utils.logger import get_logger
from src.utils.config import AppConfig

logger = get_logger(__name__)


class GoldAggregator:
    """Builds all business-ready aggregation tables for Power BI and reporting."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.gold_path = config.paths.gold
        self.exports_path = config.paths.exports

    def build(self, df: pd.DataFrame) -> dict:
        self.gold_path.mkdir(parents=True, exist_ok=True)
        self.exports_path.mkdir(parents=True, exist_ok=True)

        tables = {
            "attrition_by_department":    self._attrition_by_department(df),
            "attrition_by_role":          self._attrition_by_role(df),
            "attrition_by_demographics":  self._attrition_by_demographics(df),
            "satisfaction_analysis":      self._satisfaction_analysis(df),
            "salary_analysis":            self._salary_analysis(df),
            "tenure_analysis":            self._tenure_analysis(df),
            "overtime_impact":            self._overtime_impact(df),
            "risk_scores":                self._compute_risk_scores(df),
            "executive_summary":          self._executive_summary(df),
        }

        for name, table in tables.items():
            table.to_parquet(self.gold_path / f"{name}.parquet", index=False, engine="pyarrow")
            table.to_csv(self.exports_path / f"{name}.csv", index=False)

        logger.info(f"Gold layer complete: {len(tables)} tables built and exported")
        return tables

    # ── Attrition Aggregations ─────────────────────────────────────────────────

    def _attrition_by_department(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby("Department", observed=True)
            .agg(
                TotalEmployees=("Attrition", "count"),
                AttritionCount=("Attrition", "sum"),
                AttritionRate=("Attrition", "mean"),
                AvgMonthlyIncome=("MonthlyIncome", "mean"),
                AvgJobSatisfaction=("JobSatisfaction", "mean"),
                AvgYearsAtCompany=("YearsAtCompany", "mean"),
                OvertimeRate=("OverTime", "mean"),
            )
            .round(4)
            .reset_index()
        )

    def _attrition_by_role(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby(["Department", "JobRole"], observed=True)
            .agg(
                TotalEmployees=("Attrition", "count"),
                AttritionCount=("Attrition", "sum"),
                AttritionRate=("Attrition", "mean"),
                AvgMonthlyIncome=("MonthlyIncome", "mean"),
                AvgJobLevel=("JobLevel", "mean"),
                AvgSatisfactionComposite=("SatisfactionComposite", "mean"),
            )
            .round(4)
            .reset_index()
        )

    def _attrition_by_demographics(self, df: pd.DataFrame) -> pd.DataFrame:
        frames = []
        for dim in ["AgeBand", "MaritalStatus", "EducationField", "DistanceTier"]:
            agg = (
                df.groupby(dim, observed=True)
                .agg(
                    TotalEmployees=("Attrition", "count"),
                    AttritionCount=("Attrition", "sum"),
                    AttritionRate=("Attrition", "mean"),
                )
                .round(4)
                .reset_index()
                .rename(columns={dim: "DimensionValue"})
            )
            agg["Dimension"] = dim
            agg["DimensionValue"] = agg["DimensionValue"].astype(str)
            frames.append(agg)
        return pd.concat(frames, ignore_index=True)

    # ── Satisfaction & Salary ──────────────────────────────────────────────────

    def _satisfaction_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        sat_cols = [
            "EnvironmentSatisfaction", "JobSatisfaction",
            "RelationshipSatisfaction", "WorkLifeBalance",
        ]
        records = []
        for col in sat_cols:
            agg = (
                df.groupby(col)
                .agg(TotalEmployees=("Attrition", "count"), AttritionRate=("Attrition", "mean"))
                .reset_index()
            )
            agg.columns = ["Score", "TotalEmployees", "AttritionRate"]
            agg["SatisfactionDimension"] = col
            records.append(agg)
        return pd.concat(records, ignore_index=True).round(4)

    def _salary_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby(["JobLevel", "JobRole"], observed=True)
            .agg(
                TotalEmployees=("MonthlyIncome", "count"),
                MinIncome=("MonthlyIncome", "min"),
                MedianIncome=("MonthlyIncome", "median"),
                MeanIncome=("MonthlyIncome", "mean"),
                MaxIncome=("MonthlyIncome", "max"),
                AttritionRate=("Attrition", "mean"),
                AvgIncomeVsLevelMedian=("IncomeVsLevelMedian", "mean"),
            )
            .round(2)
            .reset_index()
        )

    # ── Tenure & Overtime ─────────────────────────────────────────────────────

    def _tenure_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby("YearsAtCompany")
            .agg(
                TotalEmployees=("Attrition", "count"),
                AttritionCount=("Attrition", "sum"),
                AttritionRate=("Attrition", "mean"),
                AvgYearsSincePromotion=("YearsSinceLastPromotion", "mean"),
                AvgManagerTenureRatio=("ManagerTenureRatio", "mean"),
            )
            .round(4)
            .reset_index()
        )

    def _overtime_impact(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby(["OverTime", "JobSatisfaction"])
            .agg(
                TotalEmployees=("Attrition", "count"),
                AttritionRate=("Attrition", "mean"),
                AvgMonthlyIncome=("MonthlyIncome", "mean"),
            )
            .round(4)
            .reset_index()
        )

    # ── Risk Scoring ──────────────────────────────────────────────────────────

    def _compute_risk_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Composite flight-risk score (0–1) weighted across statistically
        significant attrition predictors. Higher = higher departure risk.

        Weights derived from feature importance analysis (see notebook 05).
        """
        risk = df[[
            "EmployeeNumber", "JobRole", "Department",
            "MonthlyIncome", "YearsAtCompany", "Attrition",
        ]].copy()

        def norm(s: pd.Series) -> pd.Series:
            mn, mx = s.min(), s.max()
            return (s - mn) / (mx - mn) if mx > mn else pd.Series(0.0, index=s.index)

        risk["r_overtime"]       = df["OverTime"].astype(float)
        risk["r_satisfaction"]   = 1 - norm(df["SatisfactionComposite"])
        risk["r_promo_lag"]      = norm(df["PromotionLag"])
        risk["r_distance"]       = norm(df["DistanceFromHome"])
        risk["r_income"]         = 1 - norm((df["IncomeVsLevelMedian"].clip(-1, 1) + 1) / 2)
        risk["r_single"]         = (df["MaritalStatus"] == "Single").astype(float)
        risk["r_tenure_risk"]    = df["YearsAtCompany"].apply(
            lambda y: 1.0 if 1 <= y <= 3 else (0.6 if 4 <= y <= 6 else 0.2)
        )

        weights = {
            "r_overtime": 0.25, "r_satisfaction": 0.25, "r_promo_lag": 0.15,
            "r_distance": 0.08, "r_income": 0.12, "r_single": 0.05, "r_tenure_risk": 0.10,
        }

        risk["FlightRiskScore"] = sum(risk[col] * w for col, w in weights.items()).round(4)
        risk["RiskBand"] = pd.cut(
            risk["FlightRiskScore"],
            bins=[0, 0.30, 0.50, 0.70, 1.01],
            labels=["Low", "Moderate", "High", "Critical"],
            right=False,
        )

        return risk[[
            "EmployeeNumber", "JobRole", "Department", "MonthlyIncome",
            "YearsAtCompany", "FlightRiskScore", "RiskBand", "Attrition",
        ]]

    # ── Executive Summary ─────────────────────────────────────────────────────

    def _executive_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        total = len(df)
        attritors = int(df["Attrition"].sum())
        high_risk = int(
            ((df["SatisfactionComposite"] < 2.0) & (df["OverTime"] == 1)).sum()
        )
        rows = [
            {"Metric": "Total Employees",            "Value": total},
            {"Metric": "Total Attrition Count",      "Value": attritors},
            {"Metric": "Overall Attrition Rate",     "Value": round(attritors / total, 4)},
            {"Metric": "Avg Monthly Income (USD)",   "Value": round(df["MonthlyIncome"].mean(), 2)},
            {"Metric": "Avg Age",                    "Value": round(df["Age"].mean(), 1)},
            {"Metric": "Avg Years at Company",       "Value": round(df["YearsAtCompany"].mean(), 1)},
            {"Metric": "Overtime Rate",              "Value": round(df["OverTime"].mean(), 4)},
            {"Metric": "Avg Satisfaction Composite", "Value": round(df["SatisfactionComposite"].mean(), 2)},
            {"Metric": "High-Risk Employees (OT + Low Satisfaction)", "Value": high_risk},
        ]
        return pd.DataFrame(rows)
