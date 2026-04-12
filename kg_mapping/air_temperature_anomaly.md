# C-PL-003 Air Temperature Anomaly — Knowledge Graph Mapping

## Level

Plot / Stand

## Input entities / observations

- `Plot`
- `AirTemperatureObservation` or reanalysis input
- baseline parameter

## KPI result node

- `AirTemperatureAnomalyResult`

## Core relations

```text
Plot -> hasObservation -> AirTemperatureObservation
Plot -> hasKPI -> AirTemperatureAnomalyResult
AirTemperatureAnomalyResult -> hasValue -> float
AirTemperatureAnomalyResult -> hasUnit -> "°C"
AirTemperatureAnomalyResult -> computedFrom -> AirTemperatureObservation
AirTemperatureAnomalyResult -> usesBaseline -> parameter
AirTemperatureAnomalyResult -> hasFlag -> string
```

## DQ / QC flags

- `MISSING_BASELINE`
- `LOW_COVERAGE`
- `RESOLUTION_NOTE`

## Provenance / versioning

- `sensor_id` or `product_id`
- `baseline_definition`
- `method_version`

## Source modality / canopy zone

- `AirTempSensor (BelowCanopy)`
- `Reanalysis (AboveCanopy)`

## Temporal logic

Rolling anomaly relative to the chosen baseline definition.
