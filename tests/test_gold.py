import pytest
import pandas as pd
from unittest.mock import MagicMock


@pytest.fixture
def mock_config(tmp_path):
    cfg = MagicMock()
    cfg.paths.gold = tmp_path / "gold"
    cfg.paths.exports = tmp_path / "exports"
    return cfg


@pytest.fixture
def silver_df():
    return pd.DataFrame({
        "EmployeeNumber": range(1, 11),
        "Age": [25, 32, 40, 28, 50, 35, 45, 29, 38, 55],
        "Attrition": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        "Department": ["Sales"] * 5 + ["R&D"] * 5,
        "JobRole": ["Sales Executive"] * 5 + ["Research Scientist"] * 5,
        "JobLevel": [1, 2, 3, 1, 4, 2, 3, 1, 2, 5],
        "MonthlyIncome": [3000, 5000, 8000, 3500, 12000, 4500, 7000, 3200, 6000, 18000],
        "OverTime": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        "MaritalStatus": ["Single", "Married", "Married", "Single", "Divorced",
                          "Single", "Married", "Single", "Married", "Divorced"],
        "DistanceFromHome": [2, 15, 8, 25, 3, 1, 20, 12, 5, 30],
        "JobSatisfaction": [2, 4, 3, 1, 4, 2, 3, 1, 3, 4],
        "EnvironmentSatisfaction": [3, 4, 2, 1, 4, 2, 3, 2, 4, 3],
        "RelationshipSatisfaction": [2, 3, 4, 1, 3, 2, 4, 1, 3, 4],
        "WorkLifeBalance": [1, 3, 2, 1, 4, 2, 3, 1, 3, 4],
        "SatisfactionComposite": [2.0, 3.5, 2.75, 1.0, 3.75, 2.0, 3.25, 1.25, 3.25, 3.75],
        "IncomeVsLevelMedian": [-0.1, 0.0, 0.05, -0.2, 0.1, 0.0, -0.05, -0.15, 0.02, 0.2],
        "PromotionLag": [0.2, 0.1, 0.3, 0.8, 0.05, 0.4, 0.2, 0.9, 0.1, 0.0],
        "ManagerTenureRatio": [0.8, 0.5, 0.6, 0.3, 0.9, 0.4, 0.7, 0.2, 0.6, 0.8],
        "YearsAtCompany": [2, 5, 10, 1, 20, 3, 8, 1, 6, 15],
        "YearsSinceLastPromotion": [0, 1, 3, 1, 1, 1, 2, 1, 1, 0],
        "NumCompaniesWorked": [2, 1, 3, 4, 1, 2, 1, 5, 2, 1],
        "TotalWorkingYears": [3, 8, 15, 3, 25, 6, 12, 3, 9, 20],
        "AgeBand": pd.Categorical(["18-25", "26-35", "36-45", "26-35", "46-55",
                                   "26-35", "36-45", "26-35", "36-45", "55+"],
                                  categories=["18-25", "26-35", "36-45", "46-55", "55+"]),
        "DistanceTier": pd.Categorical(["Near", "Far", "Moderate", "Very Far", "Near",
                                        "Near", "Far", "Moderate", "Near", "Very Far"],
                                       categories=["Near", "Moderate", "Far", "Very Far"]),
        "EducationField": pd.Categorical(["Life Sciences"] * 5 + ["Medical"] * 5),
    })


def test_gold_build_returns_all_tables(mock_config, silver_df):
    from src.gold.aggregate import GoldAggregator
    aggregator = GoldAggregator(mock_config)
    tables = aggregator.build(silver_df)

    expected = [
        "attrition_by_department", "attrition_by_role", "attrition_by_demographics",
        "satisfaction_analysis", "salary_analysis", "tenure_analysis",
        "overtime_impact", "risk_scores", "executive_summary",
    ]
    for name in expected:
        assert name in tables, f"Missing gold table: {name}"


def test_risk_scores_bounded(mock_config, silver_df):
    from src.gold.aggregate import GoldAggregator
    tables = GoldAggregator(mock_config).build(silver_df)
    scores = tables["risk_scores"]["FlightRiskScore"]
    assert (scores >= 0).all() and (scores <= 1).all()


def test_executive_summary_has_attrition_rate(mock_config, silver_df):
    from src.gold.aggregate import GoldAggregator
    tables = GoldAggregator(mock_config).build(silver_df)
    summary = tables["executive_summary"]
    rate_row = summary[summary["Metric"] == "Overall Attrition Rate"]
    assert len(rate_row) == 1
    assert 0 <= float(rate_row["Value"].iloc[0]) <= 1
