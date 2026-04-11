import argparse
import os
import sys
from typing import Dict, Set

from app.config_loader import load_app_config
from app.pipeline import ALL_KPIS, run_pipeline

_KPI_DISPLAY: Dict[str, str] = {
    "dbh_growth":           "DBH Growth Rate",
    "height_growth":        "Height Growth Rate",
    "agb":                  "Aboveground Biomass (AGB)",
    "basal_area":           "Basal Area",
    "shannon":              "Species Diversity (Shannon)",
    "regeneration_density": "Regeneration Density",
    "stand_density":        "Stand Density",
}

_ORDERED = list(_KPI_DISPLAY.items())
_W = 58


def _cls() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _select_interactively() -> Set[str]:
    while True:
        _cls()
        print("=" * _W)
        print("  Forest KPI Digital Twin")
        print("=" * _W)
        print()
        print("  Which KPIs would you like to compute?")
        print()
        for i, (_, label) in enumerate(_ORDERED, start=1):
            print(f"    {i}. {label}")
        print()
        print("  Enter numbers separated by spaces, or 'all'.")
        print("  Example:  1 3 5")
        print()

        try:
            raw = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            _cls()
            sys.exit(0)

        if raw in ("q", "quit"):
            _cls()
            sys.exit(0)

        if raw == "all":
            return set(_KPI_DISPLAY.keys())

        tokens = raw.split()
        selected: Set[str] = set()
        error = ""
        for token in tokens:
            if token.isdigit() and 1 <= int(token) <= len(_ORDERED):
                selected.add(_ORDERED[int(token) - 1][0])
            else:
                error = f"'{token}' is not valid — enter numbers between 1 and {len(_ORDERED)}."
                break

        if error:
            print(f"\n  ! {error}")
            input("  Press Enter to try again...")
            continue

        if not selected:
            print("\n  ! Please enter at least one number.")
            input("  Press Enter to try again...")
            continue

        return selected


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="forest-kpi",
        description="Forest KPI Digital Twin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "KPI keys:\n"
            + "\n".join(f"  {k:<22} {v}" for k, v in _KPI_DISPLAY.items())
        ),
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="Compute all KPIs without prompting.")
    group.add_argument(
        "--kpis",
        nargs="+",
        choices=sorted(ALL_KPIS),
        metavar="KPI",
        help="Space-separated KPI keys to compute.",
    )
    args = parser.parse_args()

    if args.all:
        selected: Set[str] = set(ALL_KPIS)
        _cls()
        print("=" * _W)
        print("  Forest KPI Digital Twin")
        print("=" * _W)
        print(f"\n  Running all {len(selected)} KPIs...\n")
    elif args.kpis:
        selected = set(args.kpis)
        _cls()
        print("=" * _W)
        print("  Forest KPI Digital Twin")
        print("=" * _W)
        labels = ", ".join(_KPI_DISPLAY.get(k, k) for k in sorted(selected))
        print(f"\n  Running: {labels}\n")
    else:
        selected = _select_interactively()
        _cls()
        print("=" * _W)
        print("  Forest KPI Digital Twin")
        print("=" * _W)
        labels = ", ".join(_KPI_DISPLAY.get(k, k) for k in sorted(selected))
        print(f"\n  Running: {labels}\n")

    print("=" * _W)
    config = load_app_config()
    run_pipeline(config, selected_kpis=selected)
    print()
    print("=" * _W)
    print("  Done.")
    print("=" * _W)
    print()


if __name__ == "__main__":
    main()
