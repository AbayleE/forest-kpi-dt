# A-PL-010 Basal Area — Knowledge Graph Mapping

## Level

Plot / Stand

## Input entities / observations

- `Plot`
- `Tree`
- latest valid `DBHObservation` per tree
- `PlotArea`

## KPI result node

- `BasalAreaResult`

## Core relations

```text
Plot -> hasMember -> Tree
Tree -> hasObservation -> DBHObservation
Plot -> hasKPI -> BasalAreaResult
BasalAreaResult -> hasValue -> float
BasalAreaResult -> hasUnit -> "m²/ha"
BasalAreaResult -> computedFrom -> DBHObservation
BasalAreaResult -> usesPlotArea -> PlotArea
BasalAreaResult -> hasFlag -> string
```

## DQ / QC flags

- `INVALID_AREA`
- `MISSING_DBH_COUNT`
- `OUT_OF_TYPICAL_RANGE_WARNING`

## Provenance / versioning

- `inventory_date` or effective aggregation date
- `measurement_method`
- `method_version`
- `tree_count_used`
- `tree_count_total`

## Source modality / canopy zone

- `Inventory_Field (BelowCanopy)`

## Temporal logic

Snapshot-style aggregate using one valid DBH value per tree for the chosen plot state.
