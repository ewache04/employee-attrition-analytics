"""
Kaggle dataset auto-downloader (kaggle >= 2.x).

Credentials — save your token to the standard location once:
  Windows:   C:\\Users\\<you>\\.kaggle\\access_token
  Mac/Linux: ~/.kaggle/access_token

Or set the environment variable:
  KAGGLE_API_TOKEN=KGAT_...   (add to your .env file)

The kaggle package reads both locations automatically.
"""

from pathlib import Path

from src.utils.logger import get_logger

logger = get_logger(__name__)

DATASET_SLUG = "patelprashant/employee-attrition"
EXPECTED_FILENAME = "WA_Fn-UseC_-HR-Employee-Attrition.csv"


def download_dataset(dest_dir: Path) -> Path:
    """
    Download and unzip the IBM HR Attrition dataset from Kaggle into dest_dir.
    Returns the path to the extracted CSV.

    Raises:
        ImportError:  kaggle package not installed.
        ValueError:   Kaggle credentials not configured.
        RuntimeError: Download or extraction failed.
    """
    try:
        from kaggle import KaggleApi
    except ImportError:
        raise ImportError(
            "kaggle package is not installed. Run: pip install kaggle"
        )

    dest_dir.mkdir(parents=True, exist_ok=True)
    csv_path = dest_dir / EXPECTED_FILENAME

    if csv_path.exists():
        logger.info(f"Dataset already present at {csv_path} — skipping download")
        return csv_path

    api = KaggleApi()

    try:
        api.authenticate()
    except Exception as e:
        raise ValueError(
            "Kaggle credentials not found.\n\n"
            "Save your API token to:  C:\\Users\\<you>\\.kaggle\\access_token\n"
            "Or set env var:          KAGGLE_API_TOKEN=KGAT_...  (in your .env)\n\n"
            "Get a token at: https://www.kaggle.com/settings → API → Create New Token"
        ) from e

    logger.info(f"Downloading '{DATASET_SLUG}' from Kaggle into {dest_dir} ...")

    try:
        api.dataset_download_files(
            DATASET_SLUG,
            path=str(dest_dir),
            unzip=True,
            quiet=False,
        )
    except Exception as e:
        raise RuntimeError(f"Kaggle download failed: {e}") from e

    if not csv_path.exists():
        # The zip may have extracted with a different name — find and rename it
        csvs = list(dest_dir.glob("*.csv"))
        if not csvs:
            raise RuntimeError(
                f"Download completed but '{EXPECTED_FILENAME}' was not found in {dest_dir}.\n"
                f"Files present: {[f.name for f in dest_dir.iterdir()]}"
            )
        csvs[0].rename(csv_path)
        logger.info(f"Renamed '{csvs[0].name}' → '{EXPECTED_FILENAME}'")

    logger.info(f"Dataset ready: {csv_path}")
    return csv_path
