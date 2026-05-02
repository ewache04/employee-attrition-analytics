import pytest
import pandas as pd
from src.utils.validators import validate_bronze, EXPECTED_COLUMNS


@pytest.fixture
def valid_df():
    data = {col: [1] for col in EXPECTED_COLUMNS}
    data["Attrition"] = ["Yes"]
    data["EmployeeNumber"] = [1]
    return pd.DataFrame(data)


def test_validate_bronze_passes_on_valid_data(valid_df):
    result = validate_bronze(valid_df)
    assert result.passed


def test_validate_bronze_fails_on_missing_column(valid_df):
    df = valid_df.drop(columns=["Age"])
    result = validate_bronze(df)
    assert not result.passed
    assert any("Age" in f for f in result.failures)


def test_validate_bronze_fails_on_duplicates(valid_df):
    df = pd.concat([valid_df, valid_df], ignore_index=True)
    result = validate_bronze(df)
    assert not result.passed
    assert any("duplicate" in f.lower() for f in result.failures)


def test_validate_bronze_fails_on_empty():
    result = validate_bronze(pd.DataFrame())
    assert not result.passed
