import os
import sys
from pathlib import Path

from rdflib import Graph

from kg.sparql_queries import results_to_df

KPI_DISPLAY = {
    "dbh_growth": "DBH Growth Rate",
    "height_growth": "Height Growth Rate",
    "agb": "Aboveground Biomass (AGB)",
    "basal_area": "Basal Area",
    "shannon": "Species Diversity (Shannon)",
    "regeneration_density": "Regeneration Density",
    "stand_density": "Stand Density",
}

MENU = list(KPI_DISPLAY.items())


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def select_kpis():
    while True:
        clear()
        print("Forest KPI Digital Twin\n")
        for i, (_, label) in enumerate(MENU, 1):
            print(f"  {i}. {label}")
        print("\nEnter numbers or 'all'\n")

        try:
            raw = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)

        if raw in ("q", "quit"):
            sys.exit(0)

        if raw == "all":
            return set(KPI_DISPLAY)

        selected = set()
        error = ""
        for token in raw.split():
            if token.isdigit() and 1 <= int(token) <= len(MENU):
                selected.add(MENU[int(token) - 1][0])
            else:
                error = f"'{token}' is not valid"
                break

        if error or not selected:
            print(f"\n! {error or 'pick at least one'}")
            input("press enter to try again...")
            continue

        return selected


_DEFAULT_TTL = Path("output") / "forest_kg.ttl"

_SPARQL_HINTS = """\
Prefixes available:
  PREFIX forest: <http://forest-kpi.org/ontology#>
  PREFIX fd:     <http://forest-kpi.org/data/>

Type your SPARQL query (empty line to run, 'exit' or 'quit' to leave):
"""


def select_mode() -> str:
    """Return 'pipeline', 'ttl', or raise SystemExit."""
    while True:
        clear()
        print("Forest KPI Digital Twin\n")
        print("  1. Run pipeline  (compute KPIs, then enter SPARQL shell)")
        print("  2. Query a saved .ttl file")
        print("  3. Quit\n")
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)

        if raw == "1":
            return "pipeline"
        if raw == "2":
            return "ttl"
        if raw in ("3", "q", "quit"):
            sys.exit(0)

        print("\n! Enter 1, 2, or 3.")
        input("press enter to try again...")


def prompt_ttl_path() -> Path:
    clear()
    print(f"Path to .ttl file (default: {_DEFAULT_TTL}):\n")
    try:
        raw = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)

    path = Path(raw) if raw else _DEFAULT_TTL
    if not path.exists():
        print(f"\n! File not found: {path}")
        sys.exit(1)
    return path


def sparql_repl(graph: Graph) -> None:
    clear()
    print(_SPARQL_HINTS)

    while True:
        lines = []
        while True:
            try:
                line = input("... " if lines else "sparql> ")
            except (EOFError, KeyboardInterrupt):
                print()
                return

            if not lines and line.strip().lower() in ("exit", "quit"):
                return

            if line == "":
                break

            lines.append(line)

        query_text = "\n".join(lines).strip()
        if not query_text:
            continue

        try:
            result = graph.query(query_text)
            df = results_to_df(result)
            if df.empty:
                print("(no results)\n")
            else:
                print(df.to_string(index=False))
                print(f"\n({len(df)} row(s))\n")
        except Exception as exc:
            print(f"! Query error: {exc}\n")
