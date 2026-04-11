import math
from collections import Counter
from typing import List

from models.kpi_model import KPIResult, Measurement, Provenance


def compute_shannon_from_measurements(
    plot_id: str,
    measurements: List[Measurement],
    method_version: str = "shannon_v2",
) -> KPIResult:

    flags = []
    rejection_reasons = []

    latest_per_tree = {}

    for m in measurements:
        if m.measurement_type != "dbh":
            continue

        if m.tree_id not in latest_per_tree or m.date > latest_per_tree[m.tree_id].date:
            latest_per_tree[m.tree_id] = m

    trees = list(latest_per_tree.values())

    if len(trees) < 5:
        return KPIResult(
            tree_id=plot_id,
            kpi_name="Species_Diversity_Shannon",
            value=None,
            unit="dimensionless",
            timestamp=None,
            flags=["INSUFFICIENT_SAMPLE_SIZE"],
            provenance=Provenance(
                instrument_id="inventory",
                calibration_date=None,
                method_version=method_version,
                instrument_method="field_inventory",
            ),
            is_rejected=True,
            rejection_reasons=["INSUFFICIENT_SAMPLE_SIZE"],
        )

    known = [t for t in trees if t.species]
    unknown = [t for t in trees if not t.species]

    if unknown:
        flags.append("UNKNOWN_SPECIES_PRESENT")

    coverage = len(known) / len(trees)

    if coverage < 0.9:
        flags.append("LOW_SPECIES_CONFIDENCE")

    species_counts = Counter(t.species for t in known)

    H = 0.0
    for count in species_counts.values():
        p = count / len(known)
        if p > 0:
            H -= p * math.log(p)

    return KPIResult(
        tree_id=plot_id,
        kpi_name="Species_Diversity_Shannon",
        value=round(H, 4),
        unit="dimensionless",
        timestamp=max(t.date for t in trees),
        flags=flags,
        provenance=Provenance(
            instrument_id="inventory",
            calibration_date=None,
            method_version=method_version,
            instrument_method="field_inventory",
        ),
        is_rejected=False,
        rejection_reasons=[],
    )