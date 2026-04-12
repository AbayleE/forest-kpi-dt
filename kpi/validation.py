# Shared helpers for growth-rate KPI computations (dbh_growth + height_growth)
from typing import Dict, List, Optional, Tuple

from kpi.utils import get_max_growth_rate, resolve_instrument_precision
from models.kpi_model import KPILevel, KPIResult, Measurement, Provenance

DAYS_PER_YEAR = 365.25


def prepare_growth_window(
    measurements: List[Measurement],
) -> Optional[Tuple[Measurement, Measurement, float, List[str]]]:

    flags: List[str] = []
    valid = []

    for m in measurements:
        if m.value is not None and m.date is not None:
            valid.append(m)

    if len(valid) < 2:
        return None

    valid.sort(key=lambda m: m.date)

    earliest = valid[0]
    latest = valid[-1]

    delta_days = (latest.date - earliest.date).days
    delta_years = delta_days / DAYS_PER_YEAR

    if delta_years <= 0:
        return None

    if earliest.value <= 0 or latest.value <= 0:
        return None

    return earliest, latest, delta_years, flags


def build_provenance(
    measurement: Measurement,
    method_version: str,
    instrument_config: Optional[Dict] = None,
) -> Provenance:

    precision_info = resolve_instrument_precision(
        measurement.instrument_method,
        instrument_config or {},
    )

    return Provenance(
        instrument_id=measurement.instrument_id,
        calibration_date=None,
        method_version=method_version,
        instrument_method=measurement.instrument_method,
        precision_cm=precision_info.get("precision_cm"),
        precision_m=precision_info.get("precision_m"),
        accuracy_percent=precision_info.get("accuracy_percent"),
    )


def compute_growth(
    tree_id: str,
    measurements: List[Measurement],
    kpi_name: str,
    unit: str,
    method_version: str,
    species_config: Optional[Dict[str, float]] = None,
    instrument_config: Optional[Dict] = None,
    default_max_rate: float = 2.0,
    kpi_level: KPILevel = KPILevel.TREE,
) -> Optional[KPIResult]:

    if species_config is None:
        species_config = {}

    if instrument_config is None:
        instrument_config = {}

    window = prepare_growth_window(measurements)
    if not window:
        return None

    rejection_reasons: List[str] = []

    earliest, latest, delta_t, flags = window

    growth_rate = (latest.value - earliest.value) / delta_t
    if growth_rate < 0:
        flags.append("WARNING: NEGATIVE_GROWTH")
        rejection_reasons.append("NEGATIVE_GROWTH")

    species = latest.species
    max_rate = get_max_growth_rate(species, species_config, default=default_max_rate)

    if growth_rate > max_rate:
        flags.append(
            f"WARNING: EXCEEDS_MAX_GROWTH ({growth_rate:.4f} > {max_rate} {unit}, species={species})"
        )
        rejection_reasons.append(
            f"EXCEEDS_MAX_GROWTH (species={species}, max={max_rate} {unit})"
        )

    provenance = build_provenance(latest, method_version, instrument_config)

    return KPIResult(
        entity_id=tree_id,
        kpi_name=kpi_name,
        value=round(growth_rate, 4),
        unit=unit,
        timestamp=latest.date,
        flags=flags,
        provenance=provenance,
        kpi_level=kpi_level,
        is_rejected=len(rejection_reasons) > 0,
        rejection_reasons=rejection_reasons,
    )
