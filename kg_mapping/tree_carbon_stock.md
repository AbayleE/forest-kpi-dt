# A-TR-004 Tree Carbon Stock — Knowledge Graph Mapping

## Level

Tree

## Input entities / observations

- `Tree`
- `AGBResult`
- `CarbonFractionParameter`

## KPI result node

- `TreeCarbonStockResult`

## Core relations

```text
Tree -> hasKPI -> TreeCarbonStockResult
TreeCarbonStockResult -> hasValue -> float
TreeCarbonStockResult -> hasUnit -> "kgC/tree"
TreeCarbonStockResult -> computedFrom -> AGBResult
TreeCarbonStockResult -> usesParameter -> CarbonFractionParameter
TreeCarbonStockResult -> hasMethodVersion -> string
TreeCarbonStockResult -> hasFlag -> string
```

## DQ / QC flags

- `INVALID_AGB`
- `DEFAULT_C_FRAC`

## Provenance / versioning

- `method_version`
- `carbon_fraction_source`
- inherited provenance from AGB result

## Source modality / canopy zone

- `Derived model (—)`

## Temporal logic

Triggered on each valid AGB update; inherits the effective timestamp from the source AGB result.
