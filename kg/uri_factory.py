import re

from rdflib import URIRef

from kg.namespace import FD

__all__ = ["tree_uri", "plot_uri", "measurement_uri", "kpi_uri"]

_SAFE = re.compile(r"[^A-Za-z0-9_.\-]")


def _slugify(value: str) -> str:
    return _SAFE.sub("_", value)


def tree_uri(tree_id: str) -> URIRef:
    return FD[f"tree/{_slugify(tree_id)}"]


def plot_uri(plot_id: str) -> URIRef:
    return FD[f"plot/{_slugify(plot_id)}"]


def measurement_uri(tree_id: str, mtype: str, date_iso: str) -> URIRef:
    key = f"{_slugify(tree_id)}_{_slugify(mtype)}_{_slugify(date_iso)}"
    return FD[f"measurement/{key}"]


def kpi_uri(subject_id: str, kpi_name: str) -> URIRef:
    return FD[f"kpi/{_slugify(subject_id)}/{_slugify(kpi_name)}"]
