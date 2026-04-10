from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd

from models.kpi_model import Measurement


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
                species=str(row["species"]) if not pd.isna(row.get("species")) else None,
                instrument_method=str(row["instrument_method"]) if not pd.isna(row.get("instrument_method")) else None,
                plot_id=str(row["plot_id"]) if not pd.isna(row.get("plot_id")) else None,
                status=str(row["status"]) if not pd.isna(row.get("status")) else None,
            )
        )

    return measurements


def load_plots(csv_path: Path) -> Dict[str, float]:
    df = pd.read_csv(csv_path)
    return dict(zip(df["plot_id"], df["area_ha"]))
