Plot → hasKPI → RegenerationDensity

RegenerationDensity → value → float
RegenerationDensity → unit → "saplings/ha"
RegenerationDensity → computedFrom → Tree DBH measurements
RegenerationDensity → timestamp → inventory_date
RegenerationDensity → saplingCount → integer
RegenerationDensity → areaUsed → float
RegenerationDensity → saplingThresholdDBH → float
RegenerationDensity → methodVersion → "regen_density_v2"

Tree → belongsTo → Plot
Tree → hasMeasurement → DBHMeasurement
DBHMeasurement → value → float

Tree → classifiedAs → Sapling (if DBH < threshold)

## Implementation

- KPI computation: `kpi/regeneration_density.py` → `compute_regeneration_from_measurements()`
- RDF triples: `kg/graph_builder.py` → `add_kpi_results_to_graph()`, class `FOREST.RegenerationDensity`
- SPARQL queries: `kg/sparql_queries.py` → `query_kpis_for_plot(graph, plot_id)`