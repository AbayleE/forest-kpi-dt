# C-PL-004 CO₂ Median (7d) — Knowledge Graph Mapping

## Level

Plot / Stand

## Input entities / observations

- `Plot`
- `CO2Observation`
- `Sensor`

## KPI result node

- `CO2Median7dResult`

## Core relations

```text
Plot -> hasObservation -> CO2Observation
CO2Observation -> measuredWith -> Sensor
Plot -> hasKPI -> CO2Median7dResult
CO2Median7dResult -> hasValue -> float
CO2Median7dResult -> hasUnit -> "ppm"
CO2Median7dResult -> computedFrom -> CO2Observation
CO2Median7dResult -> hasFlag -> string
```

## DQ / QC flags

- `LOW_COVERAGE`
- `SPIKE_REMOVAL_APPLIED`
- `CALIBRATION_WARNING`
- `OUT_OF_RANGE_WARNING`

## Provenance / versioning

- `sensor_id`
- `calibration_date`
- `method_version`

## Source modality / canopy zone

- `CO₂ sensor (BelowCanopy)`

## Temporal logic

Rolling 7-day median over quality-controlled CO₂ observations ending on the computation date.
