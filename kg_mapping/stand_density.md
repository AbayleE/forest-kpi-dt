# A-PL-012 Stand Density — Knowledge Graph Mapping

## Level

Plot / Stand

## Input entities / observations

- `Plot`
- `Tree`
- latest valid structural observation per tree
- `PlotArea`
- `TreeStatus`

## KPI result node

- `StandDensityResult`

## Core relations

```text
Plot -> hasMember -> Tree
Tree -> hasStatus -> TreeStatus
Plot -> hasKPI -> StandDensityResult
StandDensityResult -> hasValue -> float
StandDensityResult -> hasUnit -> "trees/ha"
StandDensityResult -> computedFrom -> TreeStatus
StandDensityResult -> usesPlotArea -> PlotArea
StandDensityResult -> hasFlag -> string
```

## DQ / QC flags

- `INVALID_AREA`
- `NO_DATA`
- `MISSING_STATUS_COUNT`
- `OUTLIER_LOW`
- `OUTLIER_HIGH`

## Provenance / versioning

- `inventory_date`
- `measurement_method`
- `method_version`
- `tree_count_used`
- `tree_count_total`

## Source modality / canopy zone

- `Inventory_Field (BelowCanopy)`

## Temporal logic

Snapshot aggregate over alive trees per hectare for the selected plot state.
