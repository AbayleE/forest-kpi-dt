from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd

from models.kpi_model import Measurement


def _optional_value(row: pd.Series, key: str) -> Optional[str]:
    value = row.get(key)
    if pd.isna(value):
        return None
    return str(value)


def load_measurements(csv_path: Path) -> List[Measurement]:
    dataframe = pd.read_csv(csv_path)
    measurements: List[Measurement] = []

    for _, row in dataframe.iterrows():
        measurements.append(
            Measurement(
                tree_id=str(row["tree_id"]),
                date=datetime.fromisoformat(str(row["date"])),
                measurement_type=str(row["measurement_type"]),
                value=float(row["value"]),
                instrument_id=str(row["instrument_id"]),
                species=_optional_value(row, "species"),
                instrument_method=_optional_value(row, "instrument_method"),
            )
        )

    return measurements
