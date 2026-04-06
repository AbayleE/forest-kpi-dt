from typing import List, Optional

from models.kpi_model import KPIResult, Measurement, Provenance


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

    latest_per_tree = {}

    for m in measurements:
        if m.measurement_type != "dbh":
            continue

        if m.tree_id not in latest_per_tree or m.date > latest_per_tree[m.tree_id].date:
            latest_per_tree[m.tree_id] = m

    trees = list(latest_per_tree.values())

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
        tree_id=plot_id,
        kpi_name="Regeneration_Density",
        value=round(regen_density, 2),
        unit="saplings/ha",
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