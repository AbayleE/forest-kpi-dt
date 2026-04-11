from pathlib import Path

from rdflib import Graph

__all__ = ["serialize_graph"]


def serialize_graph(graph: Graph, path: Path, fmt: str = "turtle") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(path), format=fmt)
