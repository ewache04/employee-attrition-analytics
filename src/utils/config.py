from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import yaml


@dataclass
class PathsConfig:
    bronze: Path
    silver: Path
    gold: Path
    exports: Path


@dataclass
class DataConfig:
    source_filename: str
    target_column: str
    constant_columns: list
    ordinal_mappings: dict


@dataclass
class AppConfig:
    paths: PathsConfig
    data: DataConfig
    random_seed: int = 42


def load_config(config_path: Optional[Path] = None) -> AppConfig:
    if config_path is None:
        config_path = Path(__file__).parents[2] / "config" / "settings.yaml"

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    root = Path(__file__).parents[2]

    paths = PathsConfig(
        bronze=root / raw["paths"]["bronze"],
        silver=root / raw["paths"]["silver"],
        gold=root / raw["paths"]["gold"],
        exports=root / raw["paths"]["exports"],
    )

    data = DataConfig(**raw["data"])

    return AppConfig(paths=paths, data=data, random_seed=raw.get("random_seed", 42))
