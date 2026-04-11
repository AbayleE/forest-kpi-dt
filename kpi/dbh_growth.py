# DBH Growth Rate — annual change in diameter at breast height (cm/yr)
from typing import Dict, List, Optional

from kpi.validation import compute_growth
from models.kpi_model import KPIResult, Measurement

DEFAULT_MAX_GROWTH_RATE = 2.0


def compute_dbh_growth(
    tree_id: str,
    measurements: List[Measurement],
    method_version: str = "v1.0",
    species_config: Optional[Dict[str, float]] = None,
    instrument_config: Optional[Dict] = None,
    default_max_rate: float = DEFAULT_MAX_GROWTH_RATE,
) -> Optional[KPIResult]:

    return compute_growth(
        tree_id=tree_id,
        measurements=measurements,
        kpi_name="DBH_Growth_Rate",
        unit="cm/yr",
        method_version=method_version,
        species_config=species_config,
        instrument_config=instrument_config,
        default_max_rate=default_max_rate,
    )
