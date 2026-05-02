import pandas as pd
from typing import NamedTuple


class ValidationResult(NamedTuple):
    passed: bool
    failures: list


EXPECTED_COLUMNS = {
    "Age", "Attrition", "BusinessTravel", "DailyRate", "Department",
    "DistanceFromHome", "Education", "EducationField", "EmployeeCount",
    "EmployeeNumber", "EnvironmentSatisfaction", "Gender", "HourlyRate",
    "JobInvolvement", "JobLevel", "JobRole", "JobSatisfaction", "MaritalStatus",
    "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked", "Over18", "OverTime",
    "PercentSalaryHike", "PerformanceRating", "RelationshipSatisfaction",
    "StandardHours", "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear",
    "WorkLifeBalance", "YearsAtCompany", "YearsInCurrentRole",
    "YearsSinceLastPromotion", "YearsWithCurrManager",
}


def validate_bronze(df: pd.DataFrame) -> ValidationResult:
    failures = []

    missing = EXPECTED_COLUMNS - set(df.columns)
    if missing:
        failures.append(f"Missing expected columns: {sorted(missing)}")

    if df.empty:
        failures.append("DataFrame is empty")

    if "EmployeeNumber" in df.columns and df.duplicated(subset=["EmployeeNumber"]).any():
        n = df.duplicated(subset=["EmployeeNumber"]).sum()
        failures.append(f"{n} duplicate EmployeeNumber records found")

    nulls = df.isnull().sum()
    if nulls.any():
        failures.append(f"Null values detected: {nulls[nulls > 0].to_dict()}")

    return ValidationResult(passed=len(failures) == 0, failures=failures)


def validate_silver(df: pd.DataFrame) -> ValidationResult:
    failures = []

    if "Attrition" in df.columns:
        if df["Attrition"].isnull().any():
            failures.append("Target column 'Attrition' contains nulls after encoding")
        if not df["Attrition"].isin([0, 1]).all():
            failures.append("Attrition must be binary 0/1 after encoding")

    for col in ["MonthlyIncome", "Age", "TotalWorkingYears"]:
        if col in df.columns and (df[col] < 0).any():
            failures.append(f"Negative values detected in '{col}'")

    # Allow metadata columns to have nulls, check only core columns
    core_nulls = df.drop(columns=["_silver_ts"], errors="ignore").isnull().sum()
    if core_nulls.any():
        null_cols = core_nulls[core_nulls > 0].index.tolist()
        failures.append(f"Null values in silver core columns: {null_cols}")

    return ValidationResult(passed=len(failures) == 0, failures=failures)
