from typing import Dict, List, Optional

from models.kpi_model import KPIResult, Measurement, Provenance
from kpi.utils import get_max_growth_rate, resolve_instrument_precision

DEFAULT_MAX_GROWTH_RATE = 1.5  # m/yr


def compute_height_growth(
    tree_id: str,
    measurements: List[Measurement],
    method_version: str = "v1.1",
    species_config: Optional[Dict[str, float]] = None,
    instrument_config: Optional[Dict] = None,
    default_max_rate: float = DEFAULT_MAX_GROWTH_RATE,
) -> Optional[KPIResult]:
    if species_config is None:
        species_config = {}
    if instrument_config is None:
        instrument_config = {}

    if len(measurements) < 2:
        return None

    measurements.sort(key=lambda x: x.date)
    earliest = measurements[0]
    latest = measurements[-1]

    delta_t = (latest.date - earliest.date).days / 365.25
    if delta_t == 0:
        return None

    growth_rate = (latest.value - earliest.value) / delta_t

    species = latest.species
    max_rate = get_max_growth_rate(species, species_config, default=default_max_rate)
    species_label = species if species else "unknown"

    flags: List[str] = []
    rejection_reasons: List[str] = []

    if growth_rate < 0:
        flags.append("WARNING: NEGATIVE_GROWTH")
        rejection_reasons.append("NEGATIVE_GROWTH")

    if growth_rate > max_rate:
        flags.append(
            f"WARNING: HIGH_GROWTH >{max_rate} m/yr (species={species_label})"
        )
        rejection_reasons.append(
            f"HIGH_GROWTH_EXCEEDS_MAX (species={species_label}, max={max_rate} m/yr)"
        )

    precision_info = resolve_instrument_precision(latest.instrument_method, instrument_config)

    provenance = Provenance(
        instrument_id=latest.instrument_id,
        calibration_date="2023-01-01",
        method_version=method_version,
        instrument_method=latest.instrument_method,
        precision_cm=precision_info.get("precision_cm"),
        precision_m=precision_info.get("precision_m"),
        accuracy_percent=precision_info.get("accuracy_percent"),
    )

    return KPIResult(
        tree_id=tree_id,
        kpi_name="Height_Growth_Rate",
        value=round(growth_rate, 4),
        unit="m/yr",
        timestamp=latest.date,
        flags=flags,
        provenance=provenance,
        is_rejected=len(rejection_reasons) > 0,
        rejection_reasons=rejection_reasons,
    )