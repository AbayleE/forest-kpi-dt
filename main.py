from app.cli import select_kpis
from app.config_loader import load_app_config
from app.pipeline import run_pipeline


def main() -> None:
    selected = select_kpis()
    config = load_app_config()
    run_pipeline(config, selected_kpis=selected)


if __name__ == "__main__":
    main()
