from rdflib import Graph

from app.cli import prompt_ttl_path, select_kpis, select_mode, sparql_repl
from app.config_loader import load_app_config
from app.pipeline import run_pipeline


def main() -> None:
    mode = select_mode()

    if mode == "pipeline":
        selected = select_kpis()
        config = load_app_config()
        _results, kg = run_pipeline(config, selected_kpis=selected)
        sparql_repl(kg)

    else:  # mode == "ttl"
        ttl_path = prompt_ttl_path()
        graph = Graph()
        graph.parse(str(ttl_path), format="turtle")
        print(f"Loaded {len(graph)} triples from {ttl_path}\n")
        sparql_repl(graph)


if __name__ == "__main__":
    main()
