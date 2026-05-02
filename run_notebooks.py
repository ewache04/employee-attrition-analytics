"""
run_notebooks.py -- Execute all analysis notebooks in order.

Runs notebooks 01 -> 05 sequentially, saves outputs back into each .ipynb,
and exports an HTML report for every notebook so charts are viewable in
any browser without Jupyter.

Usage:
    python run_notebooks.py                  # run all 5 notebooks
    python run_notebooks.py --only 4 5       # run notebooks 04 and 05 only
    python run_notebooks.py --no-html        # skip HTML export
"""

import argparse
import asyncio
import os
import sys
import time
import webbrowser
from pathlib import Path

# Fix ZMQ/Proactor warning on Windows with Python 3.8+
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Force matplotlib to use the non-interactive Agg backend so charts render
# without a display (inherited by every notebook kernel spawned below)
os.environ["MPLBACKEND"] = "Agg"

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError


ROOT     = Path(__file__).parent
NB_DIR   = ROOT / "notebooks"
HTML_DIR = ROOT / "reports"

NOTEBOOKS = [
    "01_bronze_data_ingestion.ipynb",
    "02_silver_data_cleaning.ipynb",
    "03_gold_feature_engineering.ipynb",
    "04_exploratory_data_analysis.ipynb",
    "05_insights_and_presentation.ipynb",
]

TITLES = [
    "Bronze  -- Raw Data Ingestion",
    "Silver  -- Data Cleaning & Transformation",
    "Gold    -- Business Aggregations",
    "EDA     -- Exploratory Data Analysis",
    "Insights -- Hidden Patterns & Executive Presentation",
]


def _bar(pct: float, width: int = 30) -> str:
    filled = int(width * pct)
    return f"[{'#' * filled}{'-' * (width - filled)}] {pct:.0%}"


def execute_notebook(nb_path: Path, timeout: int = 600) -> nbformat.NotebookNode:
    with open(nb_path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(
        timeout=timeout,
        kernel_name="python3",
    )
    # Run from notebooks/ so that Path.cwd().parent inside each notebook
    # correctly resolves to the project root (where data/ and src/ live)
    ep.resources["metadata"] = {"path": str(nb_path.parent)}
    ep.preprocess(nb)

    # Write executed notebook back so outputs are saved for later inspection
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    return nb


def export_html(nb: nbformat.NotebookNode, dest: Path) -> None:
    exporter = HTMLExporter()
    exporter.theme = "light"
    body, _ = exporter.from_notebook_node(nb)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body, encoding="utf-8")


def run(notebooks: list, export_html_flag: bool = True) -> None:
    HTML_DIR.mkdir(exist_ok=True)
    total  = len(notebooks)
    passed = []
    failed = []

    print()
    print("=" * 62)
    print("   Employee Attrition  --  Notebook Execution Runner")
    print("=" * 62)
    print(f"  Notebooks to run : {total}")
    print(f"  HTML export      : {'yes  ->  reports/' if export_html_flag else 'no'}")
    print()

    overall_start = time.time()

    for i, filename in enumerate(notebooks, 1):
        nb_path   = NB_DIR / filename
        stem      = Path(filename).stem
        idx       = NOTEBOOKS.index(filename) if filename in NOTEBOOKS else -1
        title     = TITLES[idx] if idx >= 0 else stem
        html_dest = HTML_DIR / f"{stem}.html"

        print(f"  [{i}/{total}]  {title}")

        if not nb_path.exists():
            print(f"         SKIP -- file not found: {nb_path}\n")
            failed.append(filename)
            continue

        t0 = time.time()
        try:
            nb      = execute_notebook(nb_path)
            elapsed = time.time() - t0

            print(f"         {_bar(1.0)}  {elapsed:.1f}s  PASSED")

            if export_html_flag:
                export_html(nb, html_dest)
                print(f"         HTML -> reports/{html_dest.name}")

            passed.append(filename)

        except CellExecutionError as e:
            elapsed = time.time() - t0
            print(f"         {_bar(1.0)}  {elapsed:.1f}s  FAILED (cell error)")
            print(f"\n         {str(e)[:400]}\n")
            failed.append(filename)

        except Exception as e:
            elapsed = time.time() - t0
            print(f"         {_bar(1.0)}  {elapsed:.1f}s  FAILED ({type(e).__name__})")
            print(f"\n         {e}\n")
            failed.append(filename)

        print()

    total_elapsed = time.time() - overall_start

    print("=" * 62)
    print(f"  Passed : {len(passed)}/{total}    Total time : {total_elapsed:.1f}s")
    if failed:
        print(f"  Failed : {', '.join(failed)}")
    print("=" * 62)

    if passed and export_html_flag:
        last_html = HTML_DIR / f"{Path(passed[-1]).stem}.html"
        if last_html.exists():
            print(f"\n  Opening {last_html.name} in your browser...")
            webbrowser.open(last_html.as_uri())

    print()
    if failed:
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execute all Employee Attrition notebooks in order and export HTML reports."
    )
    parser.add_argument(
        "--only",
        nargs="+",
        type=int,
        metavar="N",
        help="Run only specific notebook numbers, e.g. --only 4 5",
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Skip HTML export (notebooks are still executed and outputs saved)",
    )
    args = parser.parse_args()

    if args.only:
        selected = []
        for n in args.only:
            matches = [nb for nb in NOTEBOOKS if nb.startswith(f"{n:02d}_")]
            if not matches:
                print(f"No notebook found for number {n}. Available: 1-{len(NOTEBOOKS)}")
                sys.exit(1)
            selected.extend(matches)
        notebooks = selected
    else:
        notebooks = NOTEBOOKS

    run(notebooks, export_html_flag=not args.no_html)


if __name__ == "__main__":
    main()
