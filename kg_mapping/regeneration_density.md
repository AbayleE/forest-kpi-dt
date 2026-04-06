Plot → hasKPI → RegenerationDensity

RegenerationDensity → value → float
RegenerationDensity → unit → "saplings/ha"
RegenerationDensity → computedFrom → Tree DBH measurements
RegenerationDensity → timestamp → inventory_date
RegenerationDensity → saplingCount → integer
RegenerationDensity → areaUsed → float
RegenerationDensity → saplingThresholdDBH → float
RegenerationDensity → methodVersion → "regen_density_v2"

Tree → belongsTo → Plot
Tree → hasMeasurement → DBHMeasurement
DBHMeasurement → value → float

Tree → classifiedAs → Sapling (if DBH < threshold)