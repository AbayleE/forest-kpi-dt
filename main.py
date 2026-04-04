from app.config_loader import load_app_config
from app.pipeline import run_pipeline


def main() -> None:
    config = load_app_config()
    run_pipeline(config)


if __name__ == "__main__":
    main()
