# A-TR-003 Aboveground Biomass (AGB) — Knowledge Graph Mapping

## Level

Tree

## Input entities / observations

- `Tree`
- `DBHObservation`
- optional `HeightObservation`
- optional `Species`
- optional `WoodDensityParameter`

## KPI result node

- `AGBResult`

## Core relations

```text
Tree -> hasKPI -> AGBResult
AGBResult -> hasValue -> float
AGBResult -> hasUnit -> "kg/tree"
AGBResult -> computedFrom -> DBHObservation
AGBResult -> computedFrom -> HeightObservation (optional)
AGBResult -> usesParameter -> WoodDensityParameter
AGBResult -> hasEquationType -> "pantropical" | "DBH_only"
AGBResult -> hasModelVersion -> string
AGBResult -> hasFlag -> string
```

## DQ / QC flags

- `INVALID_DBH`
- `NO_HEIGHT`
- `ASSUMED_DENSITY`
- `INVALID_AGB`
- `OUT_OF_RANGE_WARNING`

## Provenance / versioning

- `model_version`
- `equation_type`
- `parameter_source`
- `instrument_id` inherited from upstream measurements
- `uncertainty_estimate`

## Source modality / canopy zone

- `Inventory_Field (BelowCanopy)` as primary structural source
- upstream height may additionally come from `Below-canopy LiDAR / TLS`, `UAV LiDAR`, or `EO imagery` depending on the observation used

## Temporal logic

Point-in-time estimate using the most recent valid structural observations available for the tree.
