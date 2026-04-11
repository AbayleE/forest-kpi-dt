# Height Growth — Knowledge Graph Mapping

## Entities

- Tree
- HeightObservation
- HeightGrowthRate

## Relations

```
Tree → hasMeasurement → HeightObservation

HeightObservation → value → float
HeightObservation → timestamp → datetime

Tree → hasKPI → HeightGrowthRate

HeightGrowthRate → value → float
HeightGrowthRate → unit → "m/yr"
HeightGrowthRate → timestamp → datetime
HeightGrowthRate → computedFrom → HeightObservation
HeightGrowthRate → methodVersion → string
HeightGrowthRate → instrument_id → string
HeightGrowthRate → hasFlag → string
```

## Implementation

- KPI computation: `kpi/height_growth.py` → `compute_height_growth()`
- RDF triples: `kg/graph_builder.py` → `add_kpi_results_to_graph()`, class `FOREST.HeightGrowth`
- SPARQL queries: `kg/sparql_queries.py` → `query_tree_kpis(graph, tree_id)`
