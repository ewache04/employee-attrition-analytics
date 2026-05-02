import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from pathlib import Path

from src.silver.transform import SilverTransformer, CONSTANT_COLUMNS


@pytest.fixture
def mock_config(tmp_path):
    cfg = MagicMock()
    cfg.paths.silver = tmp_path / "silver"
    return cfg


@pytest.fixture
def bronze_df():
    return pd.DataFrame({
        "Age": [30, 45, 28],
        "Attrition": ["Yes", "No", "Yes"],
        "BusinessTravel": ["Travel_Rarely", "Non-Travel", "Travel_Frequently"],
        "DailyRate": [800, 1200, 500],
        "Department": ["Sales", "R&D", "HR"],
        "DistanceFromHome": [5, 20, 1],
        "Education": [3, 4, 2],
        "EducationField": ["Life Sciences", "Medical", "Other"],
        "EmployeeCount": [1, 1, 1],
        "EmployeeNumber": [1, 2, 3],
        "EnvironmentSatisfaction": [3, 4, 1],
        "Gender": ["Male", "Female", "Male"],
        "HourlyRate": [65, 90, 48],
        "JobInvolvement": [3, 4, 2],
        "JobLevel": [2, 3, 1],
        "JobRole": ["Sales Executive", "Research Scientist", "HR"],
        "JobSatisfaction": [4, 3, 1],
        "MaritalStatus": ["Single", "Married", "Divorced"],
        "MonthlyIncome": [5000, 9000, 3000],
        "MonthlyRate": [15000, 22000, 11000],
        "NumCompaniesWorked": [3, 1, 5],
        "Over18": ["Y", "Y", "Y"],
        "OverTime": ["Yes", "No", "Yes"],
        "PercentSalaryHike": [14, 11, 20],
        "PerformanceRating": [3, 3, 4],
        "RelationshipSatisfaction": [4, 2, 3],
        "StandardHours": [80, 80, 80],
        "StockOptionLevel": [1, 0, 2],
        "TotalWorkingYears": [10, 20, 5],
        "TrainingTimesLastYear": [2, 3, 1],
        "WorkLifeBalance": [3, 2, 1],
        "YearsAtCompany": [5, 15, 2],
        "YearsInCurrentRole": [3, 8, 1],
        "YearsSinceLastPromotion": [1, 5, 0],
        "YearsWithCurrManager": [4, 10, 1],
    })


def test_constants_removed(mock_config, bronze_df):
    t = SilverTransformer(mock_config)
    result = t.transform(bronze_df)
    for col in CONSTANT_COLUMNS:
        assert col not in result.columns


def test_attrition_encoded(mock_config, bronze_df):
    t = SilverTransformer(mock_config)
    result = t.transform(bronze_df)
    assert set(result["Attrition"].unique()).issubset({0, 1})


def test_overtime_encoded(mock_config, bronze_df):
    t = SilverTransformer(mock_config)
    result = t.transform(bronze_df)
    assert set(result["OverTime"].unique()).issubset({0, 1})


def test_derived_features_exist(mock_config, bronze_df):
    t = SilverTransformer(mock_config)
    result = t.transform(bronze_df)
    for col in ["SatisfactionComposite", "PromotionLag", "IncomeVsLevelMedian",
                "AgeBand", "DistanceTier", "ManagerTenureRatio"]:
        assert col in result.columns, f"Missing derived feature: {col}"
