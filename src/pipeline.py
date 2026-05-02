from pathlib import Path

from src.utils.config import load_config, AppConfig
from src.utils.logger import get_logger
from src.bronze.ingest import BronzeIngester
from src.silver.transform import SilverTransformer
from src.gold.aggregate import GoldAggregator

logger = get_logger(__name__)


def run_pipeline(source_path: Path = None, config: AppConfig = None) -> dict:
    """
    Execute the full Bronze → Silver → Gold Medallion pipeline.

    Args:
        source_path: Path to the raw CSV. Defaults to config bronze dir / source_filename.
        config:      AppConfig instance. Loads from settings.yaml if not provided.

    Returns:
        dict with keys 'bronze', 'silver', 'gold' containing the resulting DataFrames/tables.
    """
    cfg = config or load_config()

    if source_path is None:
        source_path = cfg.paths.bronze / cfg.data.source_filename

    logger.info("=" * 60)
    logger.info("MEDALLION PIPELINE  —  Employee Attrition")
    logger.info("=" * 60)

    # ── Bronze ────────────────────────────────────────────────────────────────
    logger.info("[1/3] BRONZE — Raw ingestion")
    bronze_df = BronzeIngester(cfg).ingest(source_path)

    # ── Silver ────────────────────────────────────────────────────────────────
    logger.info("[2/3] SILVER — Clean & transform")
    silver_df = SilverTransformer(cfg).transform(bronze_df)

    # ── Gold ──────────────────────────────────────────────────────────────────
    logger.info("[3/3] GOLD — Aggregate & export")
    gold_tables = GoldAggregator(cfg).build(silver_df)

    logger.info("Pipeline complete. All layers written to data/")
    return {"bronze": bronze_df, "silver": silver_df, "gold": gold_tables}
