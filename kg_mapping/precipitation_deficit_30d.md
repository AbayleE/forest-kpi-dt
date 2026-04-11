# A-FO-021 Precipitation Deficit (30d) — Knowledge Graph Mapping

## Level

Forest

## Input entities / observations

- `AOI`
- `WeatherSeries` or `ReanalysisSeries`
- baseline parameter

## KPI result node

- `PrecipitationDeficit30dResult`

## Core relations

```text
AOI -> hasKPI -> PrecipitationDeficit30dResult
PrecipitationDeficit30dResult -> hasValue -> float
PrecipitationDeficit30dResult -> hasUnit -> "mm"
PrecipitationDeficit30dResult -> computedFrom -> WeatherSeries
PrecipitationDeficit30dResult -> usesBaseline -> parameter
PrecipitationDeficit30dResult -> hasFlag -> string
```

## DQ / QC flags

- `MISSING_BASELINE`
- `LOW_TEMPORAL_COVERAGE`
- `RESOLUTION_MISMATCH_WARNING`

## Provenance / versioning

- `data_source`
- `baseline_definition`
- `method_version`

## Source modality / canopy zone

- `Weather / reanalysis series (AboveCanopy)`

## Temporal logic

Rolling 30-day window ending on the computation date.
