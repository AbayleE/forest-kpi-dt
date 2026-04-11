# A-FO-023 Fire Weather Index (Proxy) — Knowledge Graph Mapping

## Level

Forest

## Input entities / observations

- `WeatherSeries` with temperature, relative humidity, wind, and precipitation

## KPI result node

- `FireWeatherIndexResult`

## Core relations

```text
AOI -> hasKPI -> FireWeatherIndexResult
FireWeatherIndexResult -> hasValue -> float
FireWeatherIndexResult -> hasUnit -> "index"
FireWeatherIndexResult -> computedFrom -> WeatherSeries
FireWeatherIndexResult -> hasMethodVersion -> string
FireWeatherIndexResult -> hasFlag -> string
```

## DQ / QC flags

- `MISSING_DRIVER`
- `UNIT_HARMONIZATION_WARNING`
- `LOW_TEMPORAL_COVERAGE`

## Provenance / versioning

- `data_source`
- `formula_variant`
- `method_version`

## Source modality / canopy zone

- `Weather observations / reanalysis (AboveCanopy)`

## Temporal logic

Daily or rolling fire-weather proxy derived from the required weather-driver time series.
