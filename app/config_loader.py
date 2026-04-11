from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict, Optional


ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass()
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


def load_app_config(root_dir: Optional[Path] = None) -> AppConfig:
    base_dir = root_dir or ROOT_DIR
    config_path = base_dir / "config" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    return AppConfig(
        dbh_species_config = config["species_max_dbh_rates"],
        height_species_config = config["species_max_height_rates"],
        wood_density_config = config["species_wood_density"],
        instrument_config = config["instrument_precision"],
        data_path = base_dir / "data" / "tree_measurements.csv",
        plots_path = base_dir / "data" / "plots.csv",
        output_csv_path = base_dir / "output" / "output.csv",
        dashboard_path = base_dir / "output" / "dashboard.html",
        kg_output_path = base_dir / "output" / "forest_kg.ttl",
    )
