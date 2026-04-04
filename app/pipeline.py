from typing import List, Optional

import pandas as pd

from app.config_loader import AppConfig
from app.dashboard import write_dashboard
from app.data_loader import load_measurements
from app.dispatch import dispatch_kpi, is_supported_measurement_type
from app.grouping import MeasurementGroups, group_measurements_by_tree_and_type
from app.reporting import print_insufficient_result, print_kpi_result, write_output_csv
from kpi.agb import compute_agb
from kpi.basal_area import compute_basal_area
from models.kpi_model import KPIResult, Measurement


def _latest_valid(measurements: List[Measurement]) -> Optional[Measurement]:
    valid = [m for m in measurements if m.value is not None and m.date is not None]
    if not valid:
        return None
    return max(valid, key=lambda m: m.date)


def _collect_latest_dbh(grouped: MeasurementGroups) -> List[Measurement]:
    latest: List[Measurement] = []
    for (_, mtype), measurements in grouped.items():
        if mtype != "dbh":
            continue
        m = _latest_valid(measurements)
        if m is not None:
            latest.append(m)
    return latest


def _compute_agb_results(
    grouped: MeasurementGroups,
) -> List[KPIResult]:
    tree_ids = {tid for (tid, _) in grouped}
    results: List[KPIResult] = []

    for tree_id in sorted(tree_ids):
        dbh = _latest_valid(grouped.get((tree_id, "dbh"), []))
        if dbh is None:
            continue

        height = _latest_valid(grouped.get((tree_id, "height"), []))
        result = compute_agb(
            tree_id=tree_id,
            dbh_cm=dbh.value,
            height_m=height.value if height else None,
            instrument_id=dbh.instrument_id,
        )
        if result is not None:
            results.append(result)

    return results


def run_pipeline(config: AppConfig) -> List[KPIResult]:
    measurements = load_measurements(config.data_path)
    measurements_df = pd.DataFrame([m.__dict__ for m in measurements])
    grouped = group_measurements_by_tree_and_type(measurements)

    results: List[KPIResult] = []

    # Tree-level growth KPIs
    for (tree_id, measurement_type), tree_measurements in grouped.items():
        if not is_supported_measurement_type(measurement_type):
            continue

        result = dispatch_kpi(
            tree_id,
            measurement_type,
            tree_measurements,
            grouped,
            config,
        )

        if result is None:
            print_insufficient_result(tree_id, measurement_type)
            continue

        print_kpi_result(result, measurement_type)
        results.append(result)

    # Derived tree-level KPI: AGB
    for agb_result in _compute_agb_results(grouped):
        print_kpi_result(agb_result, "agb")
        results.append(agb_result)

    # Plot-level KPI: Basal Area
    ba_result = compute_basal_area(
        plot_id="PLOT_1",
        area_ha=config.plot_area_ha,
        measurements=_collect_latest_dbh(grouped),
    )
    if ba_result is not None:
        print_kpi_result(ba_result, "basal_area")
        results.append(ba_result)

    write_output_csv(results, config.output_csv_path)
    write_dashboard(results, measurements_df, config.dashboard_path)

    return results
