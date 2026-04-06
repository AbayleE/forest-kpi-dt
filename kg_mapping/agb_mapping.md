# AGB (Aboveground Biomass) — Knowledge Graph Mapping

## Entities

- Tree
- AGB

## Relations

```
Tree → hasKPI → AGB

AGB → value → float
AGB → unit → "kg/tree"
AGB → timestamp → null
AGB → computedFrom → DBH
AGB → computedFrom → Height (optional)
AGB → modelVersion → "Chave2014" | "DBH_only"
AGB → woodDensitySource → species_wood_density config | default (0.57 g/cm³)
AGB → hasFlag → string
```

## Model Selection

- If `height_m` is provided: Chave et al. (2014) pantropical allometric model (`AGB = 0.0673 × (ρ × DBH² × H)^0.976`)
- If `height_m` is absent: DBH-only power-law fallback (`AGB = 0.1 × DBH^2.5`); flag `NO_HEIGHT` is added

## Wood Density

- Species-specific `ρ` (g/cm³) is read from `species_wood_density` in `config.json`
- If species is unknown or not configured, `ρ = 0.57` (pantropical mean) is used and flag `ASSUMED_DENSITY` is added
