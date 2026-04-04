import math
from typing import List, Optional

from models.kpi_model import KPIResult, Measurement, Provenance

MIN_TYPICAL_BA_HA = 10   # m²/ha
MAX_TYPICAL_BA_HA = 60   # m²/ha


def compute_basal_area(
    plot_id: str,
    area_ha: float,
    measurements: List[Measurement],
) -> Optional[KPIResult]:
    if area_ha is None or area_ha <= 0:
        return None

    if not measurements:
        return None

    total_ba = 0.0
    tree_count = 0
    missing_count = 0

    for measurement in measurements:
        if measurement.value is None or measurement.value <= 0:
            missing_count += 1
            continue

        radius_m = (measurement.value / 2) / 100
        total_ba += math.pi * (radius_m ** 2)
        tree_count += 1

    if tree_count == 0:
        return None

    basal_area_ha = total_ba / area_ha

    flags: List[str] = []
    rejection_reasons: List[str] = []

    if missing_count > 0:
        flags.append(f"MISSING_DBH_COUNT: {missing_count}")

    if basal_area_ha < MIN_TYPICAL_BA_HA or basal_area_ha > MAX_TYPICAL_BA_HA:
        flags.append("WARNING: OUT_OF_TYPICAL_RANGE")

    provenance = Provenance(
        instrument_id="INVENTORY",
        calibration_date=None,
        method_version="basal_area_v1",
    )

    return KPIResult(
        tree_id=plot_id,
        kpi_name="Basal_Area",
        value=round(basal_area_ha, 4),
        unit="m2/ha",
        timestamp=None,
        flags=flags,
        provenance=provenance,
        is_rejected=len(rejection_reasons) > 0,
        rejection_reasons=rejection_reasons,
    )