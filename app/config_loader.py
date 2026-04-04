from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict


ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AppConfig:
    dbh_species_config: Dict[str, float]
    height_species_config: Dict[str, float]
    instrument_config: Dict[str, Dict[str, Any]]
    data_path: Path
    output_csv_path: Path
    dashboard_path: Path
    plot_area_ha: float = 1.0


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_app_config(root_dir: Path | None = None) -> AppConfig:
    base_dir = root_dir or ROOT_DIR
    config_dir = base_dir / "config"

    return AppConfig(
        dbh_species_config=_load_json(config_dir / "species_max_rates.json"),
        height_species_config=_load_json(config_dir / "species_max_height_rates.json"),
        instrument_config=_load_json(config_dir / "instrument_precision.json"),
        data_path=base_dir / "data" / "tree_measurements.csv",
        output_csv_path=base_dir / "output.csv",
        dashboard_path=base_dir / "dashboard.html",
    )
