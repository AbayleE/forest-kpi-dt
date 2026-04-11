# Basal Area — Knowledge Graph Mapping

## Entities

- Plot
- BasalArea

## Relations

```
Plot → hasKPI → BasalArea

BasalArea → value → float
BasalArea → unit → "m²/ha"
BasalArea → computedFrom → Tree DBH measurements (latest per tree)
BasalArea → timestamp → null
BasalArea → hasFlag → "MISSING_DBH_COUNT: N" (when DBH rows skipped)
BasalArea → hasFlag → "WARNING: OUT_OF_TYPICAL_RANGE" (if value < 10 or > 60 m²/ha)
```

## Notes

- `timestamp` is not set (null) — basal area is a plot-level aggregate without a single inventory date
- Missing DBH counts are encoded as a flag string, not a separate field

## Implementation

- KPI computation: `kpi/basal_area.py` → `compute_basal_area()`
- RDF triples: `kg/graph_builder.py` → `add_kpi_results_to_graph()`, class `FOREST.BasalArea`
- SPARQL queries: `kg/sparql_queries.py` → `query_kpis_for_plot(graph, plot_id)`
