from typing import List, Optional

from app.config_loader import AppConfig
from app.grouping import MeasurementGroups
from kpi.dbh_growth import compute_dbh_growth
from kpi.height_growth import compute_height_growth
from models.kpi_model import KPIResult, Measurement


SUPPORTED_MEASUREMENT_TYPES = {"dbh", "height"}


def is_supported_measurement_type(measurement_type: str) -> bool:
    return measurement_type in SUPPORTED_MEASUREMENT_TYPES


def dispatch_kpi(
    tree_id: str,
    measurement_type: str,
    tree_measurements: List[Measurement],
    grouped_measurements: MeasurementGroups,
    config: AppConfig,
) -> Optional[KPIResult]:
    if measurement_type == "dbh":
        return compute_dbh_growth(
            tree_id,
            tree_measurements,
            species_config=config.dbh_species_config,
            instrument_config=config.instrument_config,
        )

    if measurement_type == "height":
        return compute_height_growth(
            tree_id,
            tree_measurements,
            species_config=config.height_species_config,
            instrument_config=config.instrument_config,
        )

    raise ValueError(f"Unsupported measurement type: {measurement_type}")
