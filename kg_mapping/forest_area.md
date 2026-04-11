# A-FO-017 Forest Area (Mask) — Knowledge Graph Mapping

## Level

Forest

## Input entities / observations

- `AOI`
- `ForestMaskLayer`
- `PixelArea`

## KPI result node

- `ForestAreaResult`

## Core relations

```text
AOI -> hasKPI -> ForestAreaResult
ForestAreaResult -> hasValue -> float
ForestAreaResult -> hasUnit -> "ha"
ForestAreaResult -> computedFrom -> ForestMaskLayer
ForestAreaResult -> usesPixelArea -> PixelArea
ForestAreaResult -> hasFlag -> string
```

## DQ / QC flags

- `UNDEFINED_AOI`
- `MISSING_FOREST_MASK`
- `LOW_VALID_PIXEL_COVERAGE`

## Provenance / versioning

- `product_version`
- `spatial_resolution`
- `classification_method`
- `method_version`

## Source modality / canopy zone

- `Forest mask layer / EO product (AboveCanopy)`

## Temporal logic

Point-in-time area estimate from the currently selected forest-mask product and AOI.
