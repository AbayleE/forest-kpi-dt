from typing import Dict, List, Optional

from models.kpi_model import Measurement, Provenance


def inventory_provenance(method_version: str) -> Provenance:
    return Provenance(
        instrument_id="inventory",
        calibration_date=None,
        method_version=method_version,
        instrument_method="field_inventory",
    )


def get_latest_dbh_per_tree(measurements: List[Measurement]) -> List[Measurement]:
    latest: Dict[str, Measurement] = {}
    for m in measurements:
        if m.measurement_type != "dbh" or m.value is None:
            continue
        if m.tree_id not in latest or m.date > latest[m.tree_id].date:
            latest[m.tree_id] = m
    return list(latest.values())


def get_max_growth_rate(
    species: Optional[str],
    species_config: Dict[str, float],
    default: float,
) -> float:
    if species and species in species_config:
        return species_config[species]
    return default


def resolve_instrument_precision(
    instrument_method: Optional[str],
    instrument_config: Dict,
) -> Dict[str, float]:
    if instrument_method and instrument_method in instrument_config:
        return instrument_config[instrument_method]
    return {}
