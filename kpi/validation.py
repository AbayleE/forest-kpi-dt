from typing import Dict, List, Optional, Tuple

from kpi.utils import resolve_instrument_precision
from models.kpi_model import Measurement, Provenance

DAYS_PER_YEAR = 365.25
MIN_INTERVAL_YEARS = 0.5


def prepare_growth_window(
    measurements: List[Measurement],
) -> Optional[Tuple[Measurement, Measurement, float, List[str]]]:
    flags: List[str] = []

    valid = [
        m for m in measurements
        if m.value is not None and m.date is not None
    ]
    if len(valid) < 2:
        return None

    valid.sort(key=lambda m: m.date)
    earliest = valid[0]
    latest = valid[-1]
    delta_t = (latest.date - earliest.date).days / DAYS_PER_YEAR

    if delta_t <= 0:
        return None

    if delta_t < MIN_INTERVAL_YEARS:
        flags.append("WARNING: SHORT_INTERVAL_LOW_CONFIDENCE")

    if earliest.value <= 0 or latest.value <= 0:
        return None

    return earliest, latest, delta_t, flags


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
