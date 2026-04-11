# DBH Growth — Knowledge Graph Mapping

## Entities

- Tree
- DBH_Observation
- DBH_Growth_KPI

## Relations

```
Tree → hasMeasurement → DBH_Observation

DBH_Observation → value → float
DBH_Observation → timestamp → datetime

Tree → hasKPI → DBH_Growth_KPI

DBH_Growth_KPI → value → float
DBH_Growth_KPI → unit → "cm/yr"
DBH_Growth_KPI → timestamp → datetime
DBH_Growth_KPI → computedFrom → DBH_Observation
DBH_Growth_KPI → methodVersion → string
DBH_Growth_KPI → instrument_id → string
DBH_Growth_KPI → hasFlag → string
```

## Implementation

- KPI computation: `kpi/dbh_growth.py` → `compute_dbh_growth()`
- RDF triples: `kg/graph_builder.py` → `add_kpi_results_to_graph()`, class `FOREST.DBHGrowth`
- SPARQL queries: `kg/sparql_queries.py` → `query_tree_kpis(graph, tree_id)`
