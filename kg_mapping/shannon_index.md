Plot → hasKPI → SpeciesDiversity

SpeciesDiversity → value → float
SpeciesDiversity → unit → "dimensionless"
SpeciesDiversity → computedFrom → Tree species distribution (latest DBH per tree)
SpeciesDiversity → timestamp → max(measurement date)
SpeciesDiversity → methodVersion → "shannon_v2"
SpeciesDiversity → hasFlag → "UNKNOWN_SPECIES_PRESENT" (if any tree has no species)
SpeciesDiversity → hasFlag → "LOW_SPECIES_CONFIDENCE" (if species coverage < 90%)
SpeciesDiversity → hasFlag → "INSUFFICIENT_SAMPLE_SIZE" (rejected, if < 5 trees)

Tree → belongsTo → Plot
Tree → hasSpecies → Species

## Notes

- `treeCountUsed`, `treeCountTotal`, `speciesCount`, and `coverage` are not separate fields;
  coverage threshold and sample-size checks are encoded as flags

## Implementation

- KPI computation: `kpi/shannon_index.py` → `compute_shannon_from_measurements()`
- RDF triples: `kg/graph_builder.py` → `add_kpi_results_to_graph()`, class `FOREST.SpeciesDiversity`
- SPARQL queries: `kg/sparql_queries.py` → `query_kpis_for_plot(graph, plot_id)`