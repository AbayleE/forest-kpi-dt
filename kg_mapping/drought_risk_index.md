# A-FO-022 Drought Risk Index — Knowledge Graph Mapping

## Level

Forest

## Input entities / observations

- `SoilMoistureAnomalyResult` or soil moisture deficit input
- `AirTemperatureAnomalyResult`
- `PrecipitationDeficit30dResult`
- weighting parameter

## KPI result node

- `DroughtRiskIndexResult`

## Core relations

```text
AOI -> hasKPI -> DroughtRiskIndexResult
DroughtRiskIndexResult -> hasValue -> float
DroughtRiskIndexResult -> hasUnit -> "index 0..1"
DroughtRiskIndexResult -> computedFrom -> SoilMoistureAnomalyResult
DroughtRiskIndexResult -> computedFrom -> AirTemperatureAnomalyResult
DroughtRiskIndexResult -> computedFrom -> PrecipitationDeficit30dResult
DroughtRiskIndexResult -> usesParameter -> WeightVector
DroughtRiskIndexResult -> hasFlag -> string
```

## DQ / QC flags

- `LOW_COMPONENT_COVERAGE`
- `MISSING_COMPONENT`
- `LOW_CONFIDENCE_COMPOSITE`

## Provenance / versioning

- `weight_vector`
- `normalization_method`
- `method_version`

## Source modality / canopy zone

- `Derived multi-source index (Ground/Soil + BelowCanopy + AboveCanopy)`

## Temporal logic

Rolling 30-day composite inheriting the effective temporal window of its component indicators.
