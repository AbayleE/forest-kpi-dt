# Basal Area — total cross-sectional stem area, scaled to m²/ha
# Formula per tree: BA = π × (DBH / 200)²  (DBH cm → radius m)
import math
from typing import List, Optional

from kg.uri_factory import measurement_uri
from kpi.utils import inventory_provenance
from models.kpi_model import KPILevel, KPIResult, Measurement


def compute_basal_area(
    plot_id: str,
    area_ha: float,
    dbh_measurements: List[Measurement],
    method_version: str = "basal_area_v1",
) -> Optional[KPIResult]:

    if area_ha is None or area_ha <= 0:
        return None

    if not dbh_measurements:
        return None

    total_ba = 0.0
    tree_count = 0
    missing_count = 0
    used_uris: List[str] = []

    for measurement in dbh_measurements:
        if measurement.value is None or measurement.value <= 0:
            missing_count += 1
            continue

        radius_m = (measurement.value / 2) / 100
        total_ba += math.pi * (radius_m**2)
        tree_count += 1
        if measurement.date is not None:
            used_uris.append(
                str(
                    measurement_uri(
                        measurement.tree_id,
                        measurement.measurement_type,
                        measurement.date.isoformat(),
                    )
                )
            )

    if tree_count == 0:
        return None

    basal_area_ha = total_ba / area_ha

    flags: List[str] = []
    rejection_reasons: List[str] = []

    if missing_count > 0:
        flags.append(f"WARNING: MISSING_DBH_COUNT: {missing_count}")

    provenance = inventory_provenance(method_version)

    return KPIResult(
        entity_id=plot_id,
        kpi_name="Basal_Area",
        value=round(basal_area_ha, 4),
        unit="m²/ha",
        timestamp=None,
        flags=flags,
        provenance=provenance,
        kpi_level=KPILevel.PLOT,
        is_rejected=len(rejection_reasons) > 0,
        rejection_reasons=rejection_reasons,
        computed_from_uris=used_uris,
    )
