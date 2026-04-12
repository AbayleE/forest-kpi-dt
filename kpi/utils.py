from typing import Dict, List, Optional

from models.kpi_model import Measurement, Provenance


def inventory_provenance(method_version: str) -> Provenance:

    return Provenance(
        instrument_id="inventory",
        method_version=method_version,
        instrument_method="field_inventory",
    )


def get_latest_dbh_per_tree(measurements: List[Measurement]) -> List[Measurement]:
    latest_by_tree: Dict[str, Measurement] = {}

    for m in measurements:
        if m.measurement_type != "dbh" or m.value is None:
            continue

        existing = latest_by_tree.get(m.tree_id)

        if existing is None or m.date > existing.date:
            latest_by_tree[m.tree_id] = m

    return list(latest_by_tree.values())


def get_max_growth_rate(
    species: Optional[str],
    species_config: Dict[str, float],
    default: float,
) -> float:

    if species is None:
        return default

    if species in species_config:
        return species_config[species]

    return default


def resolve_instrument_precision(
    instrument_method: Optional[str],
    instrument_config: Dict,
) -> Dict[str, float]:

    if instrument_method is None:
        return {}

    if instrument_method in instrument_config:
        return instrument_config[instrument_method]

    return {}
