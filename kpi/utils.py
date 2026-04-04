from typing import Dict, Optional


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
) -> Dict:
    if instrument_method and instrument_method in instrument_config:
        return instrument_config[instrument_method]
    return {}
