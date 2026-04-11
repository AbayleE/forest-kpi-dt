# C-PL-001 Soil Moisture (7d Mean) — Knowledge Graph Mapping

## Level

Plot / Stand

## Input entities / observations

- `Plot`
- `SoilMoistureObservation`
- `Sensor`

## KPI result node

- `SoilMoisture7dMeanResult`

## Core relations

```text
Plot -> hasObservation -> SoilMoistureObservation
SoilMoistureObservation -> measuredWith -> Sensor
Plot -> hasKPI -> SoilMoisture7dMeanResult
SoilMoisture7dMeanResult -> hasValue -> float
SoilMoisture7dMeanResult -> hasUnit -> "%" | "m3/m3"
SoilMoisture7dMeanResult -> computedFrom -> SoilMoistureObservation
SoilMoisture7dMeanResult -> hasFlag -> string
```

## DQ / QC flags

- `LOW_COVERAGE`
- `RANGE_WARNING`
- `DRIFT_WARNING`

## Provenance / versioning

- `sensor_id`
- `calibration_date`
- `depth`
- `method_version`

## Source modality / canopy zone

- `SoilMoistureSensor (Ground/Soil)`

## Temporal logic

Rolling 7-day mean over valid soil-moisture observations ending on the computation date.
