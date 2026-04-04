from typing import Dict, List, Optional

from models.kpi_model import KPIResult, Measurement, Provenance

# Fallback when a tree's species has no entry in species_max_rates.json
DEFAULT_MAX_GROWTH_RATE = 2.5  # cm/yr


def _get_max_growth_rate(
    species: Optional[str],
    species_config: Dict[str, float],
    default: float = DEFAULT_MAX_GROWTH_RATE,
) -> float:
    if species and species in species_config:
        return species_config[species]
    return default


def _resolve_instrument_precision(
    instrument_method: Optional[str],
    instrument_config: Dict,
) -> Dict:
    if instrument_method and instrument_method in instrument_config:
        return instrument_config[instrument_method]
    return {}


def compute_dbh_growth(
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

    # Hard reject: cannot compute a rate without at least two observations
    if len(measurements) < 2:
        return None

    measurements.sort(key=lambda x: x.date)
    earliest = measurements[0]
    latest = measurements[-1]

    delta_t = (latest.date - earliest.date).days / 365.25
    if delta_t == 0:
        return None

    growth_rate = (latest.dbh_cm - earliest.dbh_cm) / delta_t

    # Resolve species-aware max threshold (falls back to default when unknown)
    species = latest.species
    max_rate = _get_max_growth_rate(species, species_config, default=default_max_rate)
    species_label = species if species else "unknown"

    flags: List[str] = []
    rejection_reasons: List[str] = []

    if growth_rate < 0:
        flags.append("WARNING: NEGATIVE_GROWTH")
        rejection_reasons.append("NEGATIVE_GROWTH")

    if growth_rate > max_rate:
        flags.append(
            f"WARNING: HIGH_GROWTH >{max_rate} cm/yr (species={species_label})"
        )
        rejection_reasons.append(
            f"HIGH_GROWTH_EXCEEDS_MAX (species={species_label}, max={max_rate} cm/yr)"
        )

    precision_info = _resolve_instrument_precision(latest.instrument_method, instrument_config)

    provenance = Provenance(
        instrument_id=latest.instrument_id,
        calibration_date="2023-01-01",
        method_version=method_version,
        instrument_method=latest.instrument_method,
        precision_cm=precision_info.get("precision_cm"),
        accuracy_percent=precision_info.get("accuracy_percent"),
    )

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
