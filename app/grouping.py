from typing import Dict, Iterable, List, Tuple

from models.kpi_model import Measurement


MeasurementGroups = Dict[Tuple[str, str], List[Measurement]]


def group_measurements_by_tree_and_type(
    measurements: Iterable[Measurement],
) -> MeasurementGroups:
    grouped_measurements: MeasurementGroups = {}

    for measurement in measurements:
        key = (measurement.tree_id, measurement.measurement_type)
        grouped_measurements.setdefault(key, []).append(measurement)

    return grouped_measurements
