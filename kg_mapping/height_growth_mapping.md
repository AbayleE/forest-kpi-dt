# A-TR-002 Height Growth Rate — Knowledge Graph Mapping

## Level

Tree

## Input entities / observations

- `Tree`
- `HeightObservation`
- `Timestamp`
- `InstrumentOrProduct`

## KPI result node

- `HeightGrowthRateResult`

## Core relations

```text
Tree -> hasObservation -> HeightObservation
HeightObservation -> hasValue -> float
HeightObservation -> hasUnit -> "m"
HeightObservation -> observedAt -> datetime
HeightObservation -> measuredWith -> InstrumentOrProduct
Tree -> hasKPI -> HeightGrowthRateResult
HeightGrowthRateResult -> hasValue -> float
HeightGrowthRateResult -> hasUnit -> "m/yr"
HeightGrowthRateResult -> computedFrom -> HeightObservation
HeightGrowthRateResult -> hasMethodVersion -> string
HeightGrowthRateResult -> hasFlag -> string
```

## DQ / QC flags

- `INSUFFICIENT_OBSERVATIONS`
- `INVALID_TIME_WINDOW`
- `NEGATIVE_GROWTH`
- `EXTREME_GROWTH`
- `LOW_CONFIDENCE_EO`

## Provenance / versioning

- `instrument_id` or `product_id`
- `instrument_method` or `processing_chain`
- `calibration_date` when applicable
- `method_version`
- `validation_error` or `confidence_score` for EO products

## Source modality / canopy zone

- `Inventory_Field (BelowCanopy)`
- `Below-canopy LiDAR / TLS (BelowCanopy)`
- `UAV LiDAR (AboveCanopy)`
- `EO imagery (AboveCanopy)`

## Temporal logic

Computed from earliest and latest valid height observations; EO-derived height should carry explicit uncertainty and confidence metadata.
