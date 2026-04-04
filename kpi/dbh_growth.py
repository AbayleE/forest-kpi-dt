from typing import Dict, List, Optional

from kpi.utils import get_max_growth_rate
from kpi.validation import build_provenance, prepare_growth_window
from models.kpi_model import KPIResult, Measurement

DEFAULT_MAX_GROWTH_RATE = 2.0  # cm/yr (aligned with KPI spec)


def compute_dbh_growth(
    tree_id: str,
    measurements: List[Measurement],
    method_version: str = "v2.0",
    species_config: Optional[Dict[str, float]] = None,
    instrument_config: Optional[Dict] = None,
    default_max_rate: float = DEFAULT_MAX_GROWTH_RATE,
) -> Optional[KPIResult]:

    species_config = species_config or {}
    instrument_config = instrument_config or {}

    rejection_reasons: List[str] = []

    window = prepare_growth_window(measurements)
    if window is None:
        return None

    earliest, latest, delta_t, flags = window

    delta_dbh = latest.value - earliest.value
    growth_rate = delta_dbh / delta_t

    species = latest.species
    species_label = species if species else "unknown"

    max_rate = get_max_growth_rate(
        species, species_config, default=default_max_rate
    )

    if growth_rate < 0:
        flags.append("WARNING: NEGATIVE_GROWTH")
        rejection_reasons.append("NEGATIVE_GROWTH")

    if growth_rate > max_rate:
        flags.append(
            f"WARNING: EXCEEDS_MAX_GROWTH ({growth_rate:.2f} > {max_rate} cm/yr, species={species_label})"
        )
        rejection_reasons.append(
            f"EXCEEDS_MAX_GROWTH (species={species_label}, max={max_rate} cm/yr)"
        )

    provenance = build_provenance(latest, method_version, instrument_config)

    return KPIResult(
        tree_id=tree_id,
        kpi_name="DBH_Growth_Rate",
        value=round(growth_rate, 4),
        unit="cm/yr",
        timestamp=latest.date,
        flags=flags,
        provenance=provenance,
        is_rejected=len(rejection_reasons) > 0,
        rejection_reasons=rejection_reasons,
    )