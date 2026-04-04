# AGB (Aboveground Biomass) — Knowledge Graph Mapping

## Entities

- Tree
- AGB

## Relations

```
Tree → hasKPI → AGB

AGB → value → float
AGB → unit → "kg/tree"
AGB → timestamp → datetime
AGB → computedFrom → DBH
AGB → computedFrom → Height
AGB → modelVersion → "Chave2014"
AGB → paramSource → "species" | "default"
AGB → hasFlag → string
```
