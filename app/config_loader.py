from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict


ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AppConfig:
    dbh_species_config: Dict[str, float]
    height_species_config: Dict[str, float]
    wood_density_config: Dict[str, float]
    instrument_config: Dict[str, Dict[str, Any]]
    data_path: Path
    plots_path: Path
    output_csv_path: Path
    dashboard_path: Path
    kg_output_path: Path


def load_app_config(root_dir: Path | None = None) -> AppConfig:
    base_dir = root_dir or ROOT_DIR
    config_path = base_dir / "config" / "config.json"

    with config_path.open(encoding="utf-8") as f:
        cfg = json.load(f)

    return AppConfig(
        dbh_species_config=cfg["species_max_dbh_rates"],
        height_species_config=cfg["species_max_height_rates"],
        wood_density_config=cfg["species_wood_density"],
        instrument_config=cfg["instrument_precision"],
        data_path=base_dir / "data" / "tree_measurements.csv",
        plots_path=base_dir / "data" / "plots.csv",
        output_csv_path=base_dir / "output.csv",
        dashboard_path=base_dir / "dashboard.html",
        kg_output_path=base_dir / "output" / "forest_kg.ttl",
    )
