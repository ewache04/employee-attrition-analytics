# Architecture — Medallion Framework

## Overview

This project implements the **Medallion Architecture** (Bronze → Silver → Gold) for the
IBM HR Analytics Employee Attrition dataset. Each layer has a distinct contract: what it
accepts, what it guarantees, and what it produces.

```
Raw CSV
   │
   ▼
┌─────────────────────────────────────────────────────┐
│  BRONZE  (data/bronze/)                              │
│  • Exact copy of source CSV                          │
│  • No transformations, no filtering                  │
│  • metadata.json captures ingestion audit trail      │
│  • Schema: 1,470 rows × 35 columns (raw types)      │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  SILVER  (data/silver/)                              │
│  • 3 constant columns removed                        │
│  • Binary columns encoded to int (0/1)              │
│  • Categoricals cast to pandas category dtype       │
│  • 7 ordinal label columns added                    │
│  • 7 derived features engineered                    │
│  • Validated before write                            │
│  • Format: Parquet (pyarrow engine)                  │
│  • Schema: 1,470 rows × ~47 columns                 │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  GOLD  (data/gold/ + data/exports/)                  │
│  • 9 purpose-built aggregation tables               │
│  • Flight risk scoring model                        │
│  • Executive summary KPIs                           │
│  • Parquet for Python consumers                     │
│  • CSV for Power BI import                          │
└─────────────────────────────────────────────────────┘
```

## Data Flow

```
main.py
  └── src/pipeline.py::run_pipeline()
        ├── BronzeIngester.ingest()       → data/bronze/*.csv + metadata.json
        ├── SilverTransformer.transform() → data/silver/*.parquet
        └── GoldAggregator.build()        → data/gold/*.parquet
                                            data/exports/*.csv
```

## Source Code Structure

```
src/
├── bronze/ingest.py       BronzeIngester class
├── silver/transform.py    SilverTransformer class
├── gold/aggregate.py      GoldAggregator class
├── utils/
│   ├── config.py          AppConfig dataclass + load_config()
│   ├── logger.py          Structured logger factory
│   └── validators.py      validate_bronze() / validate_silver()
└── pipeline.py            run_pipeline() orchestrator
```

## Design Decisions

### Why Parquet for Silver/Gold?
Parquet preserves dtypes (including pandas `category`), supports predicate pushdown,
and is 5–10x smaller than CSV for this dataset. Power BI connects via CSV exports
in `data/exports/` — the extra copy is justified by the format mismatch.

### Why not a database?
This is a single-user analytical project, not a production data platform.
File-based storage keeps the setup dependency-free and portable.

### Why separate validation functions?
`validate_bronze` and `validate_silver` are pure functions that accept DataFrames
and return `ValidationResult` — easy to unit-test and easy to extend.

### Flight Risk Score
The composite risk score is an interpretable weighted sum, not an ML black box.
Weights were calibrated against statistically significant predictors identified
in notebook 04. It is intentionally explainable for HR stakeholders.
