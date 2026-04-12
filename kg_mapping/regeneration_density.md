# A-PL-015 Regeneration Density — Knowledge Graph Mapping

## Level

Plot / Stand

## Input entities / observations

- `Plot`
- `RegenerationObservation` or sapling classification
- `PlotArea`
- threshold parameter

## KPI result node

- `RegenerationDensityResult`

## Core relations

```text
Plot -> hasKPI -> RegenerationDensityResult
RegenerationDensityResult -> hasValue -> float
RegenerationDensityResult -> hasUnit -> "saplings/ha"
RegenerationDensityResult -> computedFrom -> RegenerationObservation
RegenerationDensityResult -> usesPlotArea -> PlotArea
RegenerationDensityResult -> usesThreshold -> parameter
RegenerationDensityResult -> hasFlag -> string
```

## DQ / QC flags

- `INVALID_AREA`
- `INVALID_COUNT`
- `INCONSISTENT_THRESHOLD`

## Provenance / versioning

- `survey_date`
- `sampling_design`
- `height_threshold_m` or sapling definition
- `method_version`

## Source modality / canopy zone

- `Field regeneration survey (BelowCanopy)`

## Temporal logic

Point-in-time or seasonal/annual survey aggregate depending on the regeneration protocol used.
