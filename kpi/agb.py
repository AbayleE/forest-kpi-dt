# Aboveground Biomass — Chave et al. (2014) or DBH-only fallback
from typing import List, Optional
from kg.uri_factory import measurement_uri
from models.kpi_model import KPILevel, KPIResult, Measurement, Provenance

# Chave et al. (2014) pantropical allometric coefficients
CHAVE_COEFFICIENT = 0.0673
CHAVE_EXPONENT = 0.976

# Fallback DBH-only power-law coefficients
DBH_ONLY_COEFFICIENT = 0.1
DBH_ONLY_EXPONENT = 2.5

DEFAULT_WOOD_DENSITY = 0.57  # g/cm³, used when species density is unknown


def compute_agb(
    tree_id: str,
    dbh_cm: float,
    height_m: Optional[float] = None,
    rho: Optional[float] = None,
    instrument_id: str = "UNKNOWN",
    method_version: Optional[str] = None,
    dbh_measurement: Optional[Measurement] = None,
    height_measurement: Optional[Measurement] = None,
) -> Optional[KPIResult]:

    if dbh_cm <= 0:
        return None

    flags: List[str] = []
    rejection_reasons: List[str] = []

    if rho is None:
        rho = DEFAULT_WOOD_DENSITY
        flags.append("WARNING: ASSUMED_DENSITY")

    if height_m is not None:
        agb = CHAVE_COEFFICIENT * ((rho * (dbh_cm**2) * height_m) ** CHAVE_EXPONENT)
        model_version = method_version or "Chave2014"
    else:
        agb = DBH_ONLY_COEFFICIENT * (dbh_cm**DBH_ONLY_EXPONENT)
        model_version = method_version or "DBH_only"
        flags.append("WARNING: NO_HEIGHT")

    provenance = Provenance(
        instrument_id=instrument_id,
        method_version=model_version,
    )

    source_uris = []
    if dbh_measurement is not None and dbh_measurement.date is not None:
        source_uris.append(
            str(
                measurement_uri(
                    tree_id,
                    dbh_measurement.measurement_type,
                    dbh_measurement.date.isoformat(),
                )
            )
        )
    if height_measurement is not None and height_measurement.date is not None:
        source_uris.append(
            str(
                measurement_uri(
                    tree_id,
                    height_measurement.measurement_type,
                    height_measurement.date.isoformat(),
                )
            )
        )

    return KPIResult(
        entity_id=tree_id,
        kpi_name="Aboveground_Biomass",
        value=round(agb, 4),
        unit="kg/tree",
        timestamp=None,
        flags=flags,
        provenance=provenance,
        kpi_level=KPILevel.TREE,
        is_rejected=len(rejection_reasons) > 0,
        rejection_reasons=rejection_reasons,
        computed_from_uris=source_uris,
    )
