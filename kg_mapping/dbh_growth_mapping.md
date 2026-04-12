# A-TR-001 DBH Growth Rate — Knowledge Graph Mapping

## Level

Tree

## Input entities / observations

- `Tree`
- `DBHObservation`
- `Timestamp`
- `Instrument`

## KPI result node

- `DBHGrowthRateResult`

## Core relations

```text
Tree -> hasObservation -> DBHObservation
DBHObservation -> hasValue -> float
DBHObservation -> hasUnit -> "cm"
DBHObservation -> observedAt -> datetime
DBHObservation -> measuredWith -> Instrument
Tree -> hasKPI -> DBHGrowthRateResult
DBHGrowthRateResult -> hasValue -> float
DBHGrowthRateResult -> hasUnit -> "cm/yr"
DBHGrowthRateResult -> computedFrom -> DBHObservation
DBHGrowthRateResult -> hasMethodVersion -> string
DBHGrowthRateResult -> hasFlag -> string
```

## DQ / QC flags

- `INSUFFICIENT_OBSERVATIONS`
- `INVALID_TIME_WINDOW`
- `NEGATIVE_GROWTH`
- `EXTREME_GROWTH`
- `SHORT_INTERVAL_WARNING`

## Provenance / versioning

- `instrument_id`
- `instrument_method`
- `calibration_date`
- `method_version`
- `species_threshold_source`

## Source modality / canopy zone

- `Inventory_Field (BelowCanopy)`

## Temporal logic

Computed from earliest and latest valid DBH observations; annualized over the observed interval.
