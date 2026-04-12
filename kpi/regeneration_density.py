# Regeneration Density — saplings (DBH < threshold) per hectare
from typing import List, Optional

from kpi.utils import get_latest_dbh_per_tree, inventory_provenance
from models.kpi_model import KPILevel, KPIResult, Measurement

SAPLING_DBH_THRESHOLD_CM = 5.0
MIN_TREE_SAMPLE_SIZE = 10
MAX_REGEN_DENSITY = 50000


def compute_regeneration_from_measurements(
    plot_id: str,
    measurements: List[Measurement],
    area_ha: float,
    dbh_threshold_cm: float = SAPLING_DBH_THRESHOLD_CM,
    method_version: str = "regen_density_v1",
) -> Optional[KPIResult]:

    flags: List[str] = []
    rejection_reasons: List[str] = []

    if area_ha is None or area_ha <= 0:
        rejection_reasons.append("INVALID_AREA")

    trees = get_latest_dbh_per_tree(measurements)
    if not trees:
        return None

    saplings = []
    for tree in trees:
        if tree.value is None:
            continue

        if tree.value < dbh_threshold_cm:
            saplings.append(tree)

    sap_count = len(saplings)
    regen_density = sap_count / area_ha

    if regen_density > MAX_REGEN_DENSITY:
        flags.append("WARNING: EXTREME_DENSITY")

    if len(trees) < MIN_TREE_SAMPLE_SIZE:
        flags.append("WARNING: LOW_SAMPLE_SIZE")

    if dbh_threshold_cm != SAPLING_DBH_THRESHOLD_CM:
        flags.append("WARNING: INCONSISTENT_THRESHOLD")

    valid_dates = [t.date for t in trees if t.date is not None]
    latest_date = max(valid_dates) if valid_dates else None

    return KPIResult(
        entity_id=plot_id,
        kpi_name="Regeneration_Density",
        value=round(regen_density, 2),
        unit="saplings/ha",
        timestamp=latest_date,
        flags=flags,
        provenance=inventory_provenance(method_version),
        kpi_level=KPILevel.PLOT,
        is_rejected=len(rejection_reasons) > 0,
        rejection_reasons=rejection_reasons,
    )
