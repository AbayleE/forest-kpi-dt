from pathlib import Path

from rdflib import Graph

__all__ = ["serialize_graph"]

_SUPPORTED_FORMATS = {"turtle", "json-ld", "n-triples"}


def serialize_graph(graph: Graph, path: Path, fmt: str = "turtle") -> None:
    if fmt not in _SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported serialization format '{fmt}'. "
            f"Choose one of: {sorted(_SUPPORTED_FORMATS)}"
        )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(path), format=fmt)
