import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

from src.utils.logger import get_logger
from src.utils.validators import validate_bronze
from src.utils.config import AppConfig

logger = get_logger(__name__)


class BronzeIngester:
    """Loads raw CSV into the bronze layer with metadata capture."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.bronze_path = config.paths.bronze

    def ingest(self, source_path: Path) -> pd.DataFrame:
        logger.info(f"Ingesting raw data from: {source_path}")

        if not source_path.exists():
            logger.info("Source file not found — attempting Kaggle auto-download...")
            try:
                from src.utils.downloader import download_dataset
                source_path = download_dataset(self.bronze_path)
            except (ImportError, ValueError, RuntimeError) as e:
                raise FileNotFoundError(
                    f"Source file not found at {source_path} and auto-download failed:\n\n"
                    f"  {e}\n\n"
                    "Manual fallback:\n"
                    "  1. Visit https://www.kaggle.com/datasets/patelprashant/employee-attrition\n"
                    "  2. Download and place 'WA_Fn-UseC_-HR-Employee-Attrition.csv' in data/bronze/"
                ) from e

        df = pd.read_csv(source_path)
        logger.info(f"Loaded {len(df):,} rows x {df.shape[1]} columns")

        result = validate_bronze(df)
        if result.passed:
            logger.info("Bronze validation passed")
        else:
            for failure in result.failures:
                logger.warning(f"Validation warning: {failure}")

        self._write_bronze(df, source_path)
        self._write_metadata(df, source_path)

        return df

    def _write_bronze(self, df: pd.DataFrame, source_path: Path) -> None:
        self.bronze_path.mkdir(parents=True, exist_ok=True)
        dest = self.bronze_path / source_path.name
        df.to_csv(dest, index=False)
        logger.info(f"Bronze layer written: {dest}")

    def _write_metadata(self, df: pd.DataFrame, source_path: Path) -> None:
        meta = {
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
            "source_file": str(source_path),
            "row_count": len(df),
            "column_count": df.shape[1],
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "attrition_distribution": df["Attrition"].value_counts().to_dict()
            if "Attrition" in df.columns
            else {},
        }
        meta_path = self.bronze_path / "metadata.json"
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        logger.info(f"Ingestion metadata written: {meta_path}")
