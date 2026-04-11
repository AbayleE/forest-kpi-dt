# Stand Density — living trees per hectare (status == "alive" only)
from typing import List, Optional

from kpi.utils import get_latest_dbh_per_tree, inventory_provenance
from models.kpi_model import KPIResult, Measurement


def compute_stand_density(
    plot_id: str,
    area_ha: float,
    measurements: List[Measurement],
    method_version: str = "stand_density_v1",
) -> Optional[KPIResult]:
    if area_ha is None or area_ha <= 0:
        return None

    trees = get_latest_dbh_per_tree(measurements)

    if not trees:
        return None

    count_total = len(trees)
    count_alive = 0
    missing_status = 0

    for tree in trees:
        if tree.status is None:
            missing_status += 1
            continue
        if tree.status.lower() == "alive":
            count_alive += 1

    density = count_alive / area_ha

    flags: List[str] = []

    if missing_status > 0:
        flags.append(f"MISSING_STATUS_COUNT: {missing_status}")

    if density > 10000:
        flags.append("OUTLIER_HIGH")

    if density < 50:
        flags.append("OUTLIER_LOW")

    return KPIResult(
        entity_id=plot_id,
        kpi_name="Stand_Density",
        value=round(density, 2),
        unit="trees/ha",
        timestamp=max(t.date for t in trees),
        flags=flags,
        provenance=inventory_provenance(method_version),
        is_rejected=False,
        rejection_reasons=[],
        tree_count_used=count_alive,
        tree_count_total=count_total,
    )