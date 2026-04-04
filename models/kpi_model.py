from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Provenance:
    instrument_id: str
    calibration_date: Optional[str]
    method_version: str
    instrument_method: Optional[str] = None
    # Set when instrument_method is diameter_tape or digital_caliper
    precision_cm: Optional[float] = None
    # Set when instrument_method is field_inventory or satellite_remote_sensing
    precision_m: Optional[float] = None
    # Set when instrument_method is electronic_dbh (reported as-is, no conversion)
    accuracy_percent: Optional[float] = None


@dataclass
class Measurement:
    tree_id: str
    date: datetime
    measurement_type: str          # "dbh" | "height"
    value: float
    instrument_id: str
    species: Optional[str] = None
    instrument_method: Optional[str] = None


@dataclass
class KPIResult:
    tree_id: str
    kpi_name: str
    value: Optional[float]
    unit: str
    timestamp: datetime
    flags: List[str]
    provenance: Provenance
    is_rejected: bool = False
    rejection_reasons: List[str] = field(default_factory=list)