# Shannon Species Diversity Index — H' = -Σ p_i * ln(p_i)
import math
from collections import Counter
from typing import List

from kpi.utils import get_latest_dbh_per_tree, inventory_provenance
from models.kpi_model import KPIResult, Measurement


def compute_shannon_from_measurements(
    plot_id: str,
    measurements: List[Measurement],
    method_version: str = "shannon_v2",
) -> KPIResult:

    flags = []
    rejection_reasons = []

    trees = get_latest_dbh_per_tree(measurements)

    if len(trees) < 5:
        return KPIResult(
            entity_id=plot_id,
            kpi_name="Species_Diversity_Shannon",
            value=None,
            unit="dimensionless",
            timestamp=None,
            flags=["INSUFFICIENT_SAMPLE_SIZE"],
            provenance=inventory_provenance(method_version),
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
        H -= p * math.log(p)

    return KPIResult(
        entity_id=plot_id,
        kpi_name="Species_Diversity_Shannon",
        value=round(H, 4),
        unit="dimensionless",
        timestamp=max(t.date for t in trees),
        flags=flags,
        provenance=inventory_provenance(method_version),
        is_rejected=False,
        rejection_reasons=[],
    )