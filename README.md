# Forest KPI Digital Twin

A Python pipeline for computing forest Key Performance Indicators (KPIs) from tree measurement data. Designed as part of a thesis on digital twins for forest monitoring, this project processes raw field measurements into validated, traceable KPI results with full provenance tracking.

## KPIs Computed

| KPI | Level | Unit | Description |
|-----|-------|------|-------------|
| **DBH Growth Rate** | Tree | cm/yr | Annual diameter-at-breast-height growth rate |
| **Height Growth Rate** | Tree | m/yr | Annual height growth rate |
| **Aboveground Biomass (AGB)** | Tree | kg/tree | Chave et al. (2014) allometric model |
| **Basal Area** | Plot | m²/ha | Cross-sectional area of all stems per hectare |
| **Shannon Diversity Index** | Plot | dimensionless | Species diversity from stem counts |
| **Regeneration Density** | Plot | saplings/ha | Sapling count (DBH < 5 cm) per hectare |
| **Stand Density** | Plot | trees/ha | Living tree count per hectare |

Each result includes **quality flags**, **rejection tracking**, and **instrument provenance**.

## Project Structure

```
forest-kpi-dt/
├── main.py                  # Entry point — CLI and interactive KPI selection
├── requirements.txt         # Dependencies
├── app/
│   ├── config_loader.py     # Loads config.json into AppConfig dataclass
│   ├── data_loader.py       # Parses CSV into Measurement objects; loads plots.csv
│   ├── grouping.py          # Groups measurements by (tree_id, measurement_type)
│   ├── pipeline.py          # Orchestrates full KPI computation pipeline
│   ├── dashboard.py         # Generates HTML dashboard
│   └── reporting.py         # Console output and CSV export
├── kpi/
│   ├── agb.py               # Aboveground biomass
│   ├── basal_area.py        # Plot-level basal area
│   ├── dbh_growth.py        # DBH growth rate
│   ├── height_growth.py     # Height growth rate
│   ├── regeneration_density.py  # Regeneration density
│   ├── shannon_index.py     # Shannon diversity index
│   ├── stand_density.py     # Stand density
│   ├── utils.py             # Species config lookup, instrument precision
│   └── validation.py        # Growth window prep, provenance builder
├── models/
│   └── kpi_model.py         # Dataclasses: Measurement, KPIResult, Provenance
├── config/
│   └── config.json          # Species max rates, wood densities, instrument precision
├── data/
│   ├── tree_measurements.csv   # Input measurements (tree_id, date, type, value, ...)
│   ├── plots.csv               # Plot metadata (plot_id, area_ha)
│   └── tree_measurements.json  # JSON mirror (reference only)
└── kg_mapping/              # Knowledge graph entity schemas
    ├── agb_mapping.md
    ├── basal_area.md
    ├── dbh_growth_mapping.md
    ├── height_growth_mapping.md
    ├── regeneration_density.md
    ├── shannon_index.md
    └── stand_density.md
```

## Usage

```bash
pip install -r requirements.txt
python main.py
```

### Modes

| Command | Behaviour |
|---------|-----------|
| `python main.py` | Interactive prompt — enter numbers to select KPIs |
| `python main.py --all` | Compute all 7 KPIs without prompting |
| `python main.py --kpis agb basal_area` | Compute specific KPIs by key |

**Interactive prompt example:**

```
========================================================
  Forest KPI Digital Twin
========================================================

  Which KPIs would you like to compute?

    1. DBH Growth Rate
    2. Height Growth Rate
    3. Aboveground Biomass (AGB)
    4. Basal Area
    5. Species Diversity (Shannon)
    6. Regeneration Density
    7. Stand Density

  Enter numbers separated by spaces, or 'all'.
  Example:  1 3 5

  >
```

### Outputs

- **`output.csv`** — KPI results with flags, provenance, and rejection status
- **`dashboard.html`** — self-contained HTML dashboard (white, clean tables)

## Input Data Format

### `data/tree_measurements.csv`

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `tree_id` | string | Yes | Unique tree identifier |
| `date` | ISO date | Yes | Measurement date (YYYY-MM-DD) |
| `measurement_type` | string | Yes | `dbh` or `height` |
| `value` | float | Yes | Measured value (cm for DBH, m for height) |
| `instrument_id` | string | Yes | Instrument identifier |
| `species` | string | No | Tree species (used for validation thresholds and AGB) |
| `instrument_method` | string | No | Measurement method (for precision tracking) |
| `plot_id` | string | No | Plot the tree belongs to (joins to `plots.csv`) |
| `status` | string | No | `dead` or `sapling` — affects plot-level KPIs |

### `data/plots.csv`

| Column | Type | Description |
|--------|------|-------------|
| `plot_id` | string | Unique plot identifier |
| `area_ha` | float | Plot area in hectares (used for density KPIs) |

## Validation

Results are flagged and optionally rejected based on:
- **Negative growth** — value decreased between dates
- **Exceeds species maximum** — growth rate exceeds configured threshold
- **Short interval** — less than 6 months between observations
- **Unknown species** — missing species triggers default thresholds

Rejected results remain in output with `is_rejected=True` and documented `rejection_reasons`.
