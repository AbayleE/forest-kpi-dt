import os
import sys

from app.pipeline import ALL_KPIS

KPI_DISPLAY = {
    "dbh_growth":           "DBH Growth Rate",
    "height_growth":        "Height Growth Rate",
    "agb":                  "Aboveground Biomass (AGB)",
    "basal_area":           "Basal Area",
    "shannon":              "Species Diversity (Shannon)",
    "regeneration_density": "Regeneration Density",
    "stand_density":        "Stand Density",
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