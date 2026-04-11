from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Provenance:
    instrument_id: str
    calibration_date: Optional[datetime]
    method_version: str
    instrument_method: Optional[str] = None
    precision_cm: Optional[float] = None
    precision_m: Optional[float] = None
    accuracy_percent: Optional[float] = None


@dataclass
class Measurement:
    tree_id: str
    date: datetime
    measurement_type: str  # "dbh" | "height"
    value: float
    instrument_id: str
    species: Optional[str] = None
    instrument_method: Optional[str] = None
    plot_id: Optional[str] = None
    status: Optional[str] = None


@dataclass
class KPIResult:
    # entity_id holds a tree ID for tree-level KPIs, or a plot ID for plot-level KPIs
    entity_id: str
    kpi_name: str
    value: Optional[float]
    unit: str
    timestamp: Optional[datetime]
    flags: List[str]
    provenance: Provenance
    is_rejected: bool = False
    rejection_reasons: List[str] = None
    tree_count_used: Optional[int] = None
    tree_count_total: Optional[int] = None
