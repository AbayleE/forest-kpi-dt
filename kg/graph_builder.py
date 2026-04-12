from typing import List
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD

from kg.namespace import FOREST, FD
from kg.uri_factory import instrument_uri, kpi_uri, measurement_uri, plot_uri, tree_uri
from models.kpi_model import KPILevel, KPIResult, Measurement

__all__ = ["build_forest_graph"]


# Maps kpi_name values to the ontology RDF class.
_KPI_CLASS_MAP = {
    "Basal_Area": FOREST.BasalAreaResult,
    "Species_Diversity_Shannon": FOREST.ShannonDiversityResult,
    "Regeneration_Density": FOREST.RegenerationDensityResult,
    "Stand_Density": FOREST.StandDensityResult,
    "Aboveground_Biomass": FOREST.AGBResult,
    "DBH_Growth_Rate": FOREST.DBHGrowthRateResult,
    "Height_Growth_Rate": FOREST.HeightGrowthRateResult,
}


_MEASUREMENT_TYPE_MAP = {
    "dbh": FOREST.DBHObservation,
    "height": FOREST.HeightObservation,
}


def add_measurements_to_graph(graph: Graph, measurements: List[Measurement]) -> None:
    for m in measurements:
        t_uri = tree_uri(m.tree_id)
        graph.add((t_uri, RDF.type, FOREST.Tree))

        if m.plot_id:
            p_uri = plot_uri(m.plot_id)
            graph.add((p_uri, RDF.type, FOREST.Plot))
            graph.add((t_uri, FOREST.isIn, p_uri))

        date_iso = m.date.isoformat() if m.date else None
        m_uri = measurement_uri(
            m.tree_id,
            m.measurement_type,
            date_iso or "unknown",
        )
        obs_class = _MEASUREMENT_TYPE_MAP.get(m.measurement_type, FOREST.Observation)
        graph.add((m_uri, RDF.type, obs_class))
        graph.add((t_uri, FOREST.hasObservation, m_uri))

        if m.value is not None:
            graph.add((m_uri, FOREST.value, Literal(m.value)))

        if date_iso:
            graph.add((m_uri, FOREST.observedAt, Literal(date_iso)))

        if m.instrument_id:
            graph.add((m_uri, FOREST.measuredWith, instrument_uri(m.instrument_id)))


def add_kpi_results_to_graph(graph: Graph, kpi_results: List[KPIResult]) -> None:
    for result in kpi_results:
        rdf_class = _KPI_CLASS_MAP.get(result.kpi_name, FOREST.KPIResult)
        level = result.kpi_level

        subject_uri = (
            plot_uri(result.entity_id)
            if level == KPILevel.PLOT
            else tree_uri(result.entity_id)
        )

        k_uri = kpi_uri(result.entity_id, result.kpi_name)

        graph.add((k_uri, RDF.type, rdf_class))
        graph.add((subject_uri, FOREST.hasKPI, k_uri))

        if result.value is not None:
            graph.add((k_uri, FOREST.value, Literal(result.value)))

        graph.add((k_uri, FOREST.unit, Literal(result.unit)))
        graph.add((k_uri, FOREST.isRejected, Literal(result.is_rejected)))

        if result.timestamp is not None:
            graph.add((k_uri, FOREST.timestamp, Literal(result.timestamp)))

        for flag in result.flags:
            graph.add((k_uri, FOREST.hasFlag, Literal(flag)))

        for reason in result.rejection_reasons or []:
            graph.add((k_uri, FOREST.rejectionReason, Literal(reason)))

        graph.add(
            (k_uri, FOREST.hasMethodVersion, Literal(result.provenance.method_version))
        )
        graph.add(
            (k_uri, FOREST.instrumentId, Literal(result.provenance.instrument_id))
        )

        if result.provenance.instrument_method is not None:
            graph.add(
                (
                    k_uri,
                    FOREST.instrumentMethod,
                    Literal(result.provenance.instrument_method),
                )
            )

        if result.tree_count_used is not None:
            graph.add((k_uri, FOREST.treeCountUsed, Literal(result.tree_count_used)))

        if result.tree_count_total is not None:
            graph.add((k_uri, FOREST.treeCountTotal, Literal(result.tree_count_total)))

        for obs_uri in result.computed_from_uris:
            graph.add((k_uri, FOREST.computedFrom, URIRef(obs_uri)))


def build_forest_graph(
    measurements: List[Measurement],
    kpi_results: List[KPIResult],
) -> Graph:
    graph = Graph()
    graph.bind("forest", FOREST)
    graph.bind("fd", FD)

    add_measurements_to_graph(graph, measurements)
    add_kpi_results_to_graph(graph, kpi_results)

    return graph
