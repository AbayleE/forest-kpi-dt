# Shannon Species Diversity Index — H' = -Σ p_i * ln(p_i)
import math
from collections import Counter
from typing import List

from kpi.utils import get_latest_dbh_per_tree, inventory_provenance
from models.kpi_model import KPILevel, KPIResult, Measurement

MIN_TREE_SAMPLE_SIZE = 5
MIN_SPECIES_COVERAGE = 0.9


def compute_shannon_from_measurements(
    plot_id: str,
    measurements: List[Measurement],
    method_version: str = "shannon_v1",
) -> KPIResult:

    flags: List[str] = []
    rejection_reasons: List[str] = []

    trees = get_latest_dbh_per_tree(measurements)

    if len(trees) < MIN_TREE_SAMPLE_SIZE:
        return KPIResult(
            entity_id=plot_id,
            kpi_name="Species_Diversity_Shannon",
            value=None,
            unit="dimensionless",
            timestamp=None,
            flags=["WARNING: INSUFFICIENT_SAMPLE_SIZE"],
            provenance=inventory_provenance(method_version),
            kpi_level=KPILevel.PLOT,
            is_rejected=True,
            rejection_reasons=["INSUFFICIENT_SAMPLE_SIZE"],
        )

    known_species = []
    unknown_count = 0

    for t in trees:
        if t.species:
            known_species.append(t.species)
        else:
            unknown_count += 1

    if unknown_count:
        flags.append("WARNING: UNKNOWN_SPECIES_PRESENT")

    coverage = len(known_species) / len(trees)

    if coverage < MIN_SPECIES_COVERAGE:
        flags.append("WARNING: LOW_SPECIES_CONFIDENCE")

    species_counts = Counter(known_species)

    H = 0.0
    for count in species_counts.values():
        p = count / len(known_species)
        H -= p * math.log(p)

    valid_dates = [t.date for t in trees if t.date is not None]
    timestamp = max(valid_dates) if valid_dates else None

    return KPIResult(
        entity_id=plot_id,
        kpi_name="Species_Diversity_Shannon",
        value=round(H, 4),
        unit="dimensionless",
        timestamp=timestamp,
        flags=flags,
        provenance=inventory_provenance(method_version),
        kpi_level=KPILevel.PLOT,
        is_rejected=False,
        rejection_reasons=[],
    )
