# Employee Attrition Analytics

**A production-grade analytics codebase for the IBM HR Attrition dataset,
built on the Medallion Architecture (Bronze → Silver → Gold).**

---

## What This Project Does

This project ingests IBM's HR Attrition dataset, cleans and enriches it through
a structured data pipeline, computes 9 analytical tables, scores every employee
with a composite flight-risk model, and exports everything for Power BI reporting.

It surfaces **10 hidden patterns** in the data that standard dashboards miss —
from the Overtime Trap to the Satisfaction Trinity — each backed by statistical evidence
and translated into actionable HR recommendations.

---

## Quick Start

### 1. Prerequisites

```bash
# Python 3.11+ required
python --version

# Install dependencies into the existing virtual environment
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 2. Configure Kaggle Credentials (for auto-download)

The pipeline downloads the dataset automatically on first run if credentials are set up.

**Method A — kaggle.json (recommended, one-time setup):**
1. Go to https://www.kaggle.com/settings → API → **Create New Token**
2. Save the downloaded `kaggle.json` to `C:\Users\<you>\.kaggle\kaggle.json`
3. Done — the pipeline will auto-download on next run.

**Method B — environment variables:**
```
# Copy .env.example to .env, then fill in:
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

**Method C — manual fallback** (no Kaggle account needed):
Download from https://www.kaggle.com/datasets/patelprashant/employee-attrition
and place `WA_Fn-UseC_-HR-Employee-Attrition.csv` at `data/bronze/`.

### 3. Run the Pipeline

```bash
python main.py
```

Expected output:
```
============================================================
PIPELINE SUMMARY
============================================================
Silver layer : 1,470 rows x 47 columns
Gold tables  : 9
...
Exports ready in: data/exports/  (connect to Power BI)
```

### 4. Open Notebooks (optional — for full analysis)

```bash
jupyter notebook notebooks/
```

Run in order: `01` → `02` → `03` → `04` → `05`

### 5. Connect Power BI

Open `employee_attrition_report.pbix` → **Get Data** → point to `data/exports/`

See `docs/powerbi_integration.md` for the full page-by-page setup guide.

---

## Project Structure

```
Employee Attrition/
│
├── main.py                          # Pipeline entry point
├── requirements.txt
│
├── data/
│   ├── bronze/                      # Raw CSV + ingestion metadata
│   ├── silver/                      # Cleaned parquet (employee_attrition_silver.parquet)
│   ├── gold/                        # Aggregated parquet tables (9 files)
│   └── exports/                     # CSV exports for Power BI (9 files)
│
├── notebooks/
│   ├── 01_bronze_data_ingestion.ipynb      # Raw data profiling
│   ├── 02_silver_data_cleaning.ipynb       # Cleaning & feature engineering
│   ├── 03_gold_feature_engineering.ipynb   # Aggregations & risk scoring
│   ├── 04_exploratory_data_analysis.ipynb  # Statistics & correlations
│   └── 05_insights_and_presentation.ipynb  # 10 hidden patterns + exec dashboard
│
├── src/
│   ├── bronze/ingest.py             # BronzeIngester
│   ├── silver/transform.py          # SilverTransformer
│   ├── gold/aggregate.py            # GoldAggregator
│   ├── pipeline.py                  # Orchestrator
│   └── utils/
│       ├── config.py                # AppConfig + load_config()
│       ├── logger.py                # Structured logger
│       └── validators.py            # validate_bronze() / validate_silver()
│
├── config/settings.yaml             # All configurable parameters
│
├── docs/
│   ├── architecture.md              # Medallion design decisions
│   ├── data_dictionary.md           # All 35 source + 14 derived columns
│   ├── insights_playbook.md         # The 10 hidden patterns, fully documented
│   └── powerbi_integration.md       # Page-by-page Power BI setup + DAX
│
└── tests/
    ├── test_bronze.py
    ├── test_silver.py
    └── test_gold.py
```

---

## The 10 Hidden Insights

These patterns are invisible in standard HR dashboards. Each is documented in full
in `docs/insights_playbook.md` and visualised in notebook 05.

| # | Insight | Key Finding |
|---|---|---|
| 1 | **The Overtime Trap** | OT employees leave at 3.1× the rate; OT + low satisfaction = ~53% attrition |
| 2 | **Salary Compression Cliff** | Below-median earners (within their level) leave at 2× the rate |
| 3 | **Promotion Stagnation Effect** | 4+ years without promotion = 1.8× higher attrition |
| 4 | **The 3-Year Crisis** | Dual-peak departure curve: onboarding failure (yr 1–3) + plateau (yr 5–8) |
| 5 | **The Satisfaction Trinity** | All 3 satisfaction scores simultaneously low = ~50% attrition |
| 6 | **Manager Loyalty Anchor** | Long-term manager = 40% lower attrition — most underrated retention factor |
| 7 | **Stock Option Paradox** | Level 1 retains best; Level 3 (max) underperforms Level 2 |
| 8 | **The Distance Gradient** | Non-linear spike beyond 10 miles; quadratic relationship |
| 9 | **Single Employee Vulnerability** | Single + OT = ~40% departure rate |
| 10 | **Business Travel Burnout** | Frequent travel + poor WLB = ~50% attrition |

---

## Gold Layer Tables

| Table | Rows | Description |
|---|---|---|
| `attrition_by_department` | 3 | Attrition KPIs per department |
| `attrition_by_role` | 9 | Attrition by dept × role |
| `attrition_by_demographics` | ~20 | Age / marital / education / distance |
| `satisfaction_analysis` | 16 | All 4 satisfaction dimensions vs. attrition |
| `salary_analysis` | ~14 | Income distribution by level + role |
| `tenure_analysis` | ~40 | Attrition by years at company |
| `overtime_impact` | 8 | OT × satisfaction interaction |
| `risk_scores` | 1,470 | Per-employee composite flight risk score |
| `executive_summary` | 9 | Top-level KPI table |

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Key Design Decisions

**Medallion Architecture** separates raw truth (Bronze), clean data (Silver),
and analytical products (Gold). Each layer has a validation contract and a clear
single responsibility. See `docs/architecture.md`.

**Parquet** is used for Silver/Gold because it preserves pandas dtypes
(including `category`) and is 5–10× smaller than CSV. Power BI gets CSV exports
because it cannot natively read Parquet from a local path without a connector.

**Flight Risk Score** is an interpretable weighted sum, not an ML model.
This was intentional: HR stakeholders need to trust and explain the score,
not treat it as a black box.

---

## Documentation

| Document | Contents |
|---|---|
| `docs/architecture.md` | Data flow, module design, design decisions |
| `docs/data_dictionary.md` | All columns: source, type, range, description |
| `docs/insights_playbook.md` | 10 hidden patterns with statistical evidence and actions |
| `docs/powerbi_integration.md` | Report page specs, DAX measures, refresh guide |

---

## Dataset Citation

> IBM HR Analytics Employee Attrition & Performance
> Originally published by IBM Watson Analytics
> Available at: https://www.kaggle.com/datasets/patelprashant/employee-attrition
