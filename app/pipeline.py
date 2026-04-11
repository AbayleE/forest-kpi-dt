from typing import Dict, List, Optional, Set, Tuple

from app.config_loader import AppConfig
from app.dashboard import write_dashboard
from app.data_loader import load_measurements, load_plots
from app.reporting import print_kpi_result, write_output_csv
from kg.graph_builder import build_forest_graph
from kg.serializer import serialize_graph
from kpi.agb import compute_agb
from kpi.basal_area import compute_basal_area
from kpi.dbh_growth import compute_dbh_growth
from kpi.height_growth import compute_height_growth
from kpi.regeneration_density import compute_regeneration_from_measurements
from kpi.shannon_index import compute_shannon_from_measurements
from kpi.stand_density import compute_stand_density
from kpi.utils import get_latest_dbh_per_tree
from models.kpi_model import KPIResult, Measurement

ALL_KPIS: Set[str] = {
    "dbh_growth",
    "height_growth",
    "agb",
    "basal_area",
    "shannon",
    "regeneration_density",
    "stand_density",
}


def _latest_valid(measurements: List[Measurement]) -> Optional[Measurement]:
    valid_measurements = []

    for m in measurements:
        if m.value is not None and m.date is not None:
            valid_measurements.append(m)

    if not valid_measurements:
        return None

    latest = max(valid_measurements, key=lambda m: m.date)
    return latest


def _compute_growth_results(
    grouped: Dict, config: AppConfig, selected_kpis: Set[str]
) -> List[KPIResult]:

    results: List[KPIResult] = []

    for (tree_id, mtype), tree_measurements in grouped.items():

        if mtype == "dbh" and "dbh_growth" in selected_kpis:
            result = compute_dbh_growth(
                tree_id,
                tree_measurements,
                species_config=config.dbh_species_config,
                instrument_config=config.instrument_config,
            )
        elif mtype == "height" and "height_growth" in selected_kpis:
            result = compute_height_growth(
                tree_id,
                tree_measurements,
                species_config=config.height_species_config,
                instrument_config=config.instrument_config,
            )
        else:
            continue

        if result:
            results.append(result)

    return results


def _compute_agb_results(
    grouped: Dict,
    config: AppConfig,
    selected_kpis: Set[str],
) -> List[KPIResult]:

    if "agb" not in selected_kpis:
        return []

    results: List[KPIResult] = []
    tree_ids = set(tree_id for tree_id, _ in grouped.keys())

    for tree_id in sorted(tree_ids):
        dbh_measurements = grouped.get((tree_id, "dbh"), [])
        dbh = _latest_valid(dbh_measurements)
        if dbh is None:
            continue

        height_measurements = grouped.get((tree_id, "height"), [])
        height = _latest_valid(height_measurements)

        species = dbh.species
        rho = config.wood_density_config.get(species) if species else None

        agb_result = compute_agb(
            tree_id=tree_id,
            dbh_cm=dbh.value,
            height_m=height.value if height else None,
            rho=rho,
            instrument_id=dbh.instrument_id,
        )

        if agb_result:
            results.append(agb_result)

    return results


def _compute_plot_results(
    measurements: List[Measurement],
    plots: Dict[str, float],
    selected_kpis: Set[str],
) -> List[KPIResult]:
    results: List[KPIResult] = []

    for plot_id, area_ha in plots.items():
        plot_measurements = [m for m in measurements if m.plot_id == plot_id]

        results_for_plot = []

        if "basal_area" in selected_kpis:
            results_for_plot.append(
                compute_basal_area(
                    plot_id, area_ha, get_latest_dbh_per_tree(plot_measurements)
                )
            )
        if "shannon" in selected_kpis:
            results_for_plot.append(
                compute_shannon_from_measurements(plot_id, plot_measurements)
            )
        if "regeneration_density" in selected_kpis:
            results_for_plot.append(
                compute_regeneration_from_measurements(
                    plot_id, plot_measurements, area_ha
                )
            )
        if "stand_density" in selected_kpis:
            results_for_plot.append(
                compute_stand_density(plot_id, area_ha, plot_measurements)
            )

        for result in results_for_plot:
            if result:
                results.append(result)

    return results


def run_pipeline(config: AppConfig, selected_kpis: Set[str]) -> List[KPIResult]:
    tree_measurements = load_measurements(config.data_path)

    grouped: Dict[Tuple[str, str], List[Measurement]] = {}
    for m in tree_measurements:
        grouped.setdefault((m.tree_id, m.measurement_type), []).append(m)

    plots = load_plots(config.plots_path)

    results: List[KPIResult] = []
    results += _compute_growth_results(grouped, config, selected_kpis)
    results += _compute_agb_results(grouped, config, selected_kpis)
    results += _compute_plot_results(tree_measurements, plots, selected_kpis)

    for result in results:
        print_kpi_result(result)

    write_output_csv(results, config.output_csv_path)
    write_dashboard(results, tree_measurements, config.dashboard_path)

    kg = build_forest_graph(tree_measurements, results)
    serialize_graph(kg, config.kg_output_path)

    return results
