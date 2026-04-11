from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd

from models.kpi_model import Measurement


def optional_str(value: str):
    return None if pd.isna(value) else str(value)


def load_plots(csv_path: Path) -> Dict[str, float]:
    df = pd.read_csv(csv_path)
    # return dict(zip(df["plot_id"], df["area_ha"]))
    return df.set_index("plot_id")["area_ha"].to_dict()


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
                species=optional_str(row["species"]),
                instrument_method=optional_str(row["instrument_method"]),
                plot_id=optional_str(row["plot_id"]),
                status=optional_str(row["status"]),
            )
        )

    return measurements
