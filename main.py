"""
Employee Attrition — Medallion Pipeline Entry Point
====================================================
Run this script to execute the full Bronze → Silver → Gold pipeline.

Usage:
    python main.py
    python main.py --source path/to/WA_Fn-UseC_-HR-Employee-Attrition.csv
"""
import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Employee Attrition Medallion Pipeline")
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Path to raw CSV. Defaults to data/bronze/WA_Fn-UseC_-HR-Employee-Attrition.csv",
    )
    args = parser.parse_args()

    from src.pipeline import run_pipeline

    try:
        results = run_pipeline(source_path=args.source)
        silver = results["silver"]
        gold = results["gold"]
        summary = gold["executive_summary"]

        print("\n" + "=" * 60)
        print("PIPELINE SUMMARY")
        print("=" * 60)
        print(f"Silver layer : {len(silver):,} rows x {silver.shape[1]} columns")
        print(f"Gold tables  : {len(gold)}")
        print("\nExecutive KPIs:")
        for _, row in summary.iterrows():
            print(f"  {row['Metric']:<45} {row['Value']}")
        print("=" * 60)
        print("Exports ready in: data/exports/  (connect to Power BI)")

    except FileNotFoundError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
