# Basal Area — Knowledge Graph Mapping

## Entities

- Plot
- BasalArea

## Relations

```
Plot → hasKPI → BasalArea

BasalArea → value → float
BasalArea → unit → "m²/ha"
BasalArea → computedFrom → Tree DBH measurements
BasalArea → timestamp → inventory_date
BasalArea → treeCountUsed → integer
BasalArea → treeCountMissing → integer
```
