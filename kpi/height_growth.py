# Height Growth Rate — annual change in total tree height (m/yr)
from typing import Dict, List, Optional

from kpi.validation import compute_growth
from models.kpi_model import KPIResult, Measurement

DEFAULT_MAX_GROWTH_RATE = 1.5  # m/yr


def compute_height_growth(
    tree_id: str,
    measurements: List[Measurement],
    method_version: str = "v1.1",
    species_config: Optional[Dict[str, float]] = None,
    instrument_config: Optional[Dict] = None,
    default_max_rate: float = DEFAULT_MAX_GROWTH_RATE,
) -> Optional[KPIResult]:
    return compute_growth(
        tree_id=tree_id,
        measurements=measurements,
        kpi_name="Height_Growth_Rate",
        unit="m/yr",
        method_version=method_version,
        species_config=species_config,
        instrument_config=instrument_config,
        default_max_rate=default_max_rate,
    )