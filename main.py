import json
from datetime import datetime

import pandas as pd

from kpi.dbh_growth import compute_dbh_growth
from kpi.height_growth import compute_height_growth
from models.kpi_model import Measurement

# ── Load configs ───────────────────────────────────────────────────────────────
with open("config/species_max_rates.json") as f:
    dbh_species_config = json.load(f)

with open("config/species_max_height_rates.json") as f:
    height_species_config = json.load(f)

with open("config/instrument_precision.json") as f:
    instrument_config = json.load(f)

# ── Load measurements ──────────────────────────────────────────────────────────
df = pd.read_csv("data/tree_measurements.csv")

measurements_by_key: dict = {}  # (tree_id, measurement_type) -> List[Measurement]

for _, row in df.iterrows():
    species = row["species"] if pd.notna(row.get("species")) else None
    instrument_method = row["instrument_method"] if pd.notna(row.get("instrument_method")) else None
    m = Measurement(
        tree_id=row["tree_id"],
        date=datetime.fromisoformat(row["date"]),
        measurement_type=row["measurement_type"],
        value=row["value"],
        instrument_id=row["instrument_id"],
        species=species,
        instrument_method=instrument_method,
    )
    measurements_by_key.setdefault((row["tree_id"], row["measurement_type"]), []).append(m)

# ── Compute KPIs ───────────────────────────────────────────────────────────────
results = []

for (tree_id, mtype), tree_measurements in measurements_by_key.items():
    if mtype == "dbh":
        result = compute_dbh_growth(
            tree_id,
            tree_measurements,
            species_config=dbh_species_config,
            instrument_config=instrument_config,
        )
    elif mtype == "height":
        result = compute_height_growth(
            tree_id,
            tree_measurements,
            species_config=height_species_config,
            instrument_config=instrument_config,
        )
    else:
        continue

    if result is None:
        print("-----")
        print(f"Tree: {tree_id} [{mtype.upper()}]  [REJECTED — insufficient observations]")
        continue

    status = "REJECTED" if result.is_rejected else "ACCEPTED"
    print("-----")
    print(f"Tree: {result.tree_id} [{mtype.upper()}]  [{status}]")
    print(f"KPI: {result.kpi_name}")
    print(f"Value: {result.value:.4f} {result.unit}")
    if result.flags:
        print(f"Flags: {result.flags}")
    if result.rejection_reasons:
        print(f"Rejection reasons: {result.rejection_reasons}")
    print(f"Provenance: {result.provenance}")
    results.append(result)

pd.DataFrame([r.__dict__ for r in results]).to_csv("output.csv", index=False)
