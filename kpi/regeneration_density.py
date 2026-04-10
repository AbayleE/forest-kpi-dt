# Regeneration Density — saplings (DBH < threshold) per hectare
from typing import List, Optional

from kpi.utils import get_latest_dbh_per_tree, inventory_provenance
from models.kpi_model import KPIResult, Measurement


def compute_regeneration_from_measurements(
    plot_id: str,
    measurements: List[Measurement],
    area_ha: float,
    dbh_threshold_cm: float = 5.0,
    method_version: str = "regen_density_v2",
) -> Optional[KPIResult]:

    flags = []

    if area_ha is None or area_ha <= 0:
        return None

    trees = get_latest_dbh_per_tree(measurements)

    if not trees:
        return None

    saplings = [
        t for t in trees
        if t.value is not None and t.value < dbh_threshold_cm
    ]

    sap_count = len(saplings)
    regen_density = sap_count / area_ha

    if regen_density > 50000:
        flags.append("EXTREME_DENSITY")

    if len(trees) < 10:
        flags.append("LOW_SAMPLE_SIZE")

    return KPIResult(
        entity_id=plot_id,
        kpi_name="Regeneration_Density",
        value=round(regen_density, 2),
        unit="saplings/ha",
        timestamp=max(t.date for t in trees),
        flags=flags,
        provenance=inventory_provenance(method_version),
        is_rejected=False,
        rejection_reasons=[],
    )