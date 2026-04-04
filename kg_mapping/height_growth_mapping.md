Tree → hasMeasurement → HeightObservation
HeightObservation → value → float
HeightObservation → timestamp → datetime

Tree → hasKPI → HeightGrowthRate

HeightGrowthRate → value → float
HeightGrowthRate → unit → "m/year"
HeightGrowthRate → timestamp → datetime
HeightGrowthRate → computedFrom → HeightObservation
HeightGrowthRate → methodVersion → string
HeightGrowthRate → instrument_id → string
HeightGrowthRate → hasFlag → string