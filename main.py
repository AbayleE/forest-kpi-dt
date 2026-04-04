import json

import pandas as pd
from datetime import datetime

from models.kpi_model import Measurement
from kpi.dbh_growth import compute_dbh_growth

# Load configuration maps
with open("config/species_max_rates.json") as f:
    species_config = json.load(f)

with open("config/instrument_precision.json") as f:
    instrument_config = json.load(f)

df = pd.read_csv("data/dbh_measurements.csv")

# convert to objects
measurements_by_tree = {}
results = []

for _, row in df.iterrows():
    species = row["species"] if "species" in df.columns and pd.notna(row["species"]) else None
    instrument_method = (
        row["instrument_method"]
        if "instrument_method" in df.columns and pd.notna(row["instrument_method"])
        else None
    )
    m = Measurement(
        tree_id=row["tree_id"],
        date=datetime.fromisoformat(row["date"]),
        dbh_cm=row["dbh_cm"],
        instrument_id=row["instrument_id"],
        species=species,
        instrument_method=instrument_method,
    )
    measurements_by_tree.setdefault(row["tree_id"], []).append(m)


# compute KPI
for tree_id, tree_measurements in measurements_by_tree.items():
    result = compute_dbh_growth(
        tree_id,
        tree_measurements,
        species_config=species_config,
        instrument_config=instrument_config,
    )

    if result is None:
        print("-----")
        print(f"Tree: {tree_id}  [REJECTED — insufficient observations]")
        continue

    status = "REJECTED" if result.is_rejected else "ACCEPTED"
    print("-----")
    print(f"Tree: {result.tree_id}  [{status}]")
    print(f"KPI: {result.kpi_name}")
    print(f"Value: {result.value:.4f} {result.unit}")
    if result.flags:
        print(f"Flags: {result.flags}")
    if result.rejection_reasons:
        print(f"Rejection reasons: {result.rejection_reasons}")
    print(f"Provenance: {result.provenance}")
    results.append(result)

pd.DataFrame([r.__dict__ for r in results]).to_csv("output.csv", index=False)
