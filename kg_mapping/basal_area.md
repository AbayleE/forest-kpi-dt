# Basal Area — Knowledge Graph Mapping

## Entities

- Plot
- BasalArea

## Relations

```
Plot → hasKPI → BasalArea

BasalArea → value → float
BasalArea → unit → "m²/ha"
BasalArea → computedFrom → Tree DBH measurements (latest per tree)
BasalArea → timestamp → null
BasalArea → hasFlag → "MISSING_DBH_COUNT: N" (when DBH rows skipped)
BasalArea → hasFlag → "WARNING: OUT_OF_TYPICAL_RANGE" (if value < 10 or > 60 m²/ha)
```

## Notes

- `timestamp` is not set (null) — basal area is a plot-level aggregate without a single inventory date
- Missing DBH counts are encoded as a flag string, not a separate field
