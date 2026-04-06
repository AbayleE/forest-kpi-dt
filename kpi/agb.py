from typing import List, Optional

from models.kpi_model import KPIResult, Provenance

# Chave et al. (2014) pantropical allometric coefficients
CHAVE_COEFFICIENT = 0.0673
CHAVE_EXPONENT = 0.976

# Fallback DBH-only power-law coefficients
DBH_ONLY_COEFFICIENT = 0.1
DBH_ONLY_EXPONENT = 2.5

# Default wood density (g/cm³) when species-specific value is unavailable
DEFAULT_WOOD_DENSITY = 0.57


def compute_agb(
    tree_id: str,
    dbh_cm: float,
    height_m: Optional[float] = None,
    rho: Optional[float] = None,
    instrument_id: str = "UNKNOWN",
) -> Optional[KPIResult]:
    if dbh_cm <= 0:
        return None

    flags: List[str] = []
    rejection_reasons: List[str] = []

    if rho is None:
        rho = DEFAULT_WOOD_DENSITY
        flags.append("ASSUMED_DENSITY")

    if height_m is not None:
        agb = CHAVE_COEFFICIENT * ((rho * (dbh_cm ** 2) * height_m) ** CHAVE_EXPONENT)
        model_version = "Chave2014"
    else:
        agb = DBH_ONLY_COEFFICIENT * (dbh_cm ** DBH_ONLY_EXPONENT)
        model_version = "DBH_only"
        flags.append("NO_HEIGHT")

    if agb <= 0:
        flags.append("WARNING: INVALID_RESULT")
        rejection_reasons.append("INVALID_RESULT")

    provenance = Provenance(
        instrument_id=instrument_id,
        calibration_date=None,
        method_version=model_version,
    )

    return KPIResult(
        tree_id=tree_id,
        kpi_name="Aboveground_Biomass",
        value=round(agb, 4),
        unit="kg/tree",
        timestamp=None,
        flags=flags,
        provenance=provenance,
        is_rejected=len(rejection_reasons) > 0,
        rejection_reasons=rejection_reasons,
    )