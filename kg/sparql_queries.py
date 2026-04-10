from typing import Any, Dict, List

import pandas as pd
from rdflib import Graph
from rdflib.query import Result

from kg.uri_factory import plot_uri, tree_uri

__all__ = [
    "query_all_kpis",
    "query_kpis_for_plot",
    "query_tree_kpis",
    "query_flagged_kpis",
    "query_rejected_kpis",
    "query_trees_in_plot",
    "query_measurements_for_tree",
]

_PREFIXES = """
PREFIX forest: <http://forest-kpi.org/ontology#>
PREFIX fd:     <http://forest-kpi.org/data/>
PREFIX rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>
"""

_SPARQL_ALL_KPIS = (
    _PREFIXES
    + """
SELECT ?kpi ?kpiType ?subject ?value ?unit
WHERE {
    ?subject forest:hasKPI ?kpi .
    ?kpi     rdf:type      ?kpiType ;
             forest:value  ?value ;
             forest:unit   ?unit .
}
ORDER BY ?subject ?kpiType
"""
)

_SPARQL_KPIS_FOR_PLOT = (
    _PREFIXES
    + """
SELECT ?kpi ?kpiType ?value ?unit ?isRejected
WHERE {
    <{plot_uri}> forest:hasKPI ?kpi .
    ?kpi rdf:type       ?kpiType ;
         forest:value   ?value ;
         forest:unit    ?unit ;
         forest:isRejected ?isRejected .
}
"""
)

_SPARQL_TREE_KPIS = (
    _PREFIXES
    + """
SELECT ?kpi ?kpiType ?value ?unit ?isRejected
WHERE {
    <{tree_uri}> forest:hasKPI ?kpi .
    ?kpi rdf:type       ?kpiType ;
         forest:value   ?value ;
         forest:unit    ?unit ;
         forest:isRejected ?isRejected .
}
"""
)

_SPARQL_FLAGGED_KPIS = (
    _PREFIXES
    + """
SELECT ?kpi ?kpiType ?subject ?value ?unit ?flag
WHERE {
    ?subject forest:hasKPI ?kpi .
    ?kpi     rdf:type      ?kpiType ;
             forest:value  ?value ;
             forest:unit   ?unit ;
             forest:hasFlag ?flag .
}
ORDER BY ?subject ?kpi
"""
)

_SPARQL_REJECTED_KPIS = (
    _PREFIXES
    + """
SELECT ?kpi ?kpiType ?subject ?value ?unit ?reason
WHERE {
    ?subject forest:hasKPI ?kpi .
    ?kpi     rdf:type         ?kpiType ;
             forest:value     ?value ;
             forest:unit      ?unit ;
             forest:isRejected true .
    OPTIONAL { ?kpi forest:rejectionReason ?reason . }
}
ORDER BY ?subject ?kpi
"""
)

_SPARQL_TREES_IN_PLOT = (
    _PREFIXES
    + """
SELECT ?tree
WHERE {
    ?tree rdf:type   forest:Tree ;
          forest:isIn <{plot_uri}> .
}
ORDER BY ?tree
"""
)

_SPARQL_MEASUREMENTS_FOR_TREE = (
    _PREFIXES
    + """
SELECT ?measurement ?value ?timestamp
WHERE {
    <{tree_uri}> forest:hasMeasurement ?measurement .
    OPTIONAL { ?measurement forest:value     ?value . }
    OPTIONAL { ?measurement forest:timestamp ?timestamp . }
}
ORDER BY ?timestamp
"""
)


def _rows_to_df(results: Result) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for row in results:
        rows.append({str(var): str(val) if val is not None else None for var, val in row.asdict().items()})
    return pd.DataFrame(rows)


def query_all_kpis(graph: Graph) -> pd.DataFrame:
    return _rows_to_df(graph.query(_SPARQL_ALL_KPIS))


def query_kpis_for_plot(graph: Graph, plot_id: str) -> pd.DataFrame:
    sparql = _SPARQL_KPIS_FOR_PLOT.replace("{plot_uri}", str(plot_uri(plot_id)))
    return _rows_to_df(graph.query(sparql))


def query_tree_kpis(graph: Graph, tree_id: str) -> pd.DataFrame:
    sparql = _SPARQL_TREE_KPIS.replace("{tree_uri}", str(tree_uri(tree_id)))
    return _rows_to_df(graph.query(sparql))


def query_flagged_kpis(graph: Graph) -> pd.DataFrame:
    return _rows_to_df(graph.query(_SPARQL_FLAGGED_KPIS))


def query_rejected_kpis(graph: Graph) -> pd.DataFrame:
    return _rows_to_df(graph.query(_SPARQL_REJECTED_KPIS))


def query_trees_in_plot(graph: Graph, plot_id: str) -> pd.DataFrame:
    sparql = _SPARQL_TREES_IN_PLOT.replace("{plot_uri}", str(plot_uri(plot_id)))
    return _rows_to_df(graph.query(sparql))


def query_measurements_for_tree(graph: Graph, tree_id: str) -> pd.DataFrame:
    sparql = _SPARQL_MEASUREMENTS_FOR_TREE.replace("{tree_uri}", str(tree_uri(tree_id)))
    return _rows_to_df(graph.query(sparql))
