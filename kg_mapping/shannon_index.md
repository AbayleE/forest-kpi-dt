# A-PL-014 Species Diversity (Shannon) — Knowledge Graph Mapping

## Level

Plot / Stand

## Input entities / observations

- `Plot`
- `Tree`
- `SpeciesAssignment` per tree

## KPI result node

- `ShannonDiversityResult`

## Core relations

```text
Plot -> hasMember -> Tree
Tree -> hasSpecies -> SpeciesAssignment
Plot -> hasKPI -> ShannonDiversityResult
ShannonDiversityResult -> hasValue -> float
ShannonDiversityResult -> hasUnit -> "dimensionless"
ShannonDiversityResult -> computedFrom -> SpeciesAssignment
ShannonDiversityResult -> hasFlag -> string
```

## DQ / QC flags

- `UNKNOWN_SPECIES_PRESENT`
- `LOW_SPECIES_CONFIDENCE`
- `INSUFFICIENT_SAMPLE_SIZE`

## Provenance / versioning

- `inventory_date`
- `taxonomy_normalization_version`
- `method_version`
- `tree_count_used`
- `tree_count_total`
- `species_count`

## Source modality / canopy zone

- `Inventory_Field (BelowCanopy)`

## Temporal logic

Snapshot diversity calculation from the current species distribution of trees in the plot.
