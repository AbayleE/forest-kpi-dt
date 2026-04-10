from typing import List

from rdflib import Graph, Literal
from rdflib.namespace import RDF, XSD

from kg.namespace import FOREST, FD
from kg.uri_factory import kpi_uri, measurement_uri, plot_uri, tree_uri
from models.kpi_model import KPIResult, Measurement

__all__ = ["build_forest_graph"]

# Maps kpi_name values to the ontology sub-class and whether the subject is a Plot.
_KPI_CLASS_MAP = {
    "Basal_Area":                (FOREST.BasalArea,           True),
    "Species_Diversity_Shannon": (FOREST.SpeciesDiversity,    True),
    "Regeneration_Density":      (FOREST.RegenerationDensity, True),
    "Stand_Density":             (FOREST.StandDensity,        True),
    "Aboveground_Biomass":       (FOREST.AbovegroundBiomass,  False),
    "DBH_Growth_Rate":           (FOREST.DBHGrowth,           False),
    "Height_Growth_Rate":        (FOREST.HeightGrowth,        False),
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
        graph.add((m_uri, RDF.type, FOREST.Measurement))
        graph.add((t_uri, FOREST.hasMeasurement, m_uri))

        if m.value is not None:
            graph.add((m_uri, FOREST.value, Literal(m.value, datatype=XSD.double)))

        if date_iso:
            graph.add((m_uri, FOREST.timestamp, Literal(date_iso, datatype=XSD.dateTime)))


def add_kpi_results_to_graph(graph: Graph, kpi_results: List[KPIResult]) -> None:
    for result in kpi_results:
        rdf_class, is_plot_level = _KPI_CLASS_MAP.get(
            result.kpi_name,
            (FOREST.KPIResult, False),
        )

        subject_uri = (
            plot_uri(result.entity_id) if is_plot_level else tree_uri(result.entity_id)
        )
        k_uri = kpi_uri(result.entity_id, result.kpi_name)

        graph.add((k_uri, RDF.type, rdf_class))
        graph.add((subject_uri, FOREST.hasKPI, k_uri))

        if result.value is not None:
            graph.add((k_uri, FOREST.value, Literal(result.value, datatype=XSD.double)))

        graph.add((k_uri, FOREST.unit, Literal(result.unit)))
        graph.add((k_uri, FOREST.isRejected, Literal(result.is_rejected, datatype=XSD.boolean)))

        if result.timestamp is not None:
            graph.add((k_uri, FOREST.timestamp, Literal(result.timestamp.isoformat(), datatype=XSD.dateTime)))

        for flag in result.flags:
            graph.add((k_uri, FOREST.hasFlag, Literal(flag)))

        for reason in result.rejection_reasons:
            graph.add((k_uri, FOREST.rejectionReason, Literal(reason)))

        graph.add((k_uri, FOREST.methodVersion, Literal(result.provenance.method_version)))
        graph.add((k_uri, FOREST.instrumentId, Literal(result.provenance.instrument_id)))

        if result.tree_count_used is not None:
            graph.add((k_uri, FOREST.treeCountUsed, Literal(result.tree_count_used, datatype=XSD.integer)))

        if result.tree_count_total is not None:
            graph.add((k_uri, FOREST.treeCountTotal, Literal(result.tree_count_total, datatype=XSD.integer)))


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
