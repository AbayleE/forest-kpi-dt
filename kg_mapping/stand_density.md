Plot → hasKPI → StandDensity

StandDensity → value → float
StandDensity → unit → "trees/ha"
StandDensity → computedFrom → Measurement (latest DBH per tree, status = alive)
StandDensity → timestamp → max(measurement date)
StandDensity → treeCountUsed → integer (alive trees counted)
StandDensity → treeCountTotal → integer (all trees with a DBH measurement)
StandDensity → methodVersion → "stand_density_v1"

Tree → belongsTo → Plot
Tree → hasMeasurement → DBHMeasurement
Tree → hasStatus → "alive" | "dead" | null

## Notes

- Only trees with `status = "alive"` are counted in the density value
- Trees with missing `status` are excluded and their count is added as flag `MISSING_STATUS_COUNT: N`
- Density < 50 trees/ha → flag `OUTLIER_LOW`; > 10 000 trees/ha → flag `OUTLIER_HIGH`
- `treeCountUsed` and `treeCountTotal` are real fields on `KPIResult`