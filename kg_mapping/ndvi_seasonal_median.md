# A-FO-019 NDVI Seasonal Median — Knowledge Graph Mapping

## Level

Forest

## Input entities / observations

- `AOI`
- `EOScene` with `RED`, `NIR`, `CloudMask`

## KPI result node

- `NDVISeasonalMedianResult`

## Core relations

```text
AOI -> hasKPI -> NDVISeasonalMedianResult
NDVISeasonalMedianResult -> hasValue -> float
NDVISeasonalMedianResult -> hasUnit -> "NDVI"
NDVISeasonalMedianResult -> computedFrom -> EOScene
NDVISeasonalMedianResult -> usesMask -> CloudMask
NDVISeasonalMedianResult -> hasFlag -> string
```

## DQ / QC flags

- `LOW_VALID_PIXEL_FRACTION`
- `CLOUD_CONTAMINATION_WARNING`

## Provenance / versioning

- `scene_ids`
- `season_definition`
- `atmospheric_correction_version`
- `method_version`

## Source modality / canopy zone

- `Satellite multispectral EO / UAV multispectral imagery (AboveCanopy)`

## Temporal logic

Seasonal aggregate computed as the median of valid NDVI pixels across the AOI and selected season.
