import re

from rdflib import URIRef

from kg.namespace import FD

__all__ = ["tree_uri", "plot_uri", "measurement_uri", "kpi_uri", "instrument_uri"]

_SAFE = re.compile(r"[^A-Za-z0-9_.\-]")


def _make_url_safe(value: str) -> str:
    return _SAFE.sub("_", value)


def tree_uri(tree_id: str) -> URIRef:
    return FD[f"tree/{_make_url_safe(tree_id)}"]


def plot_uri(plot_id: str) -> URIRef:
    return FD[f"plot/{_make_url_safe(plot_id)}"]


def measurement_uri(tree_id: str, mtype: str, date_iso: str) -> URIRef:
    key = (
        f"{_make_url_safe(tree_id)}_{_make_url_safe(mtype)}_{_make_url_safe(date_iso)}"
    )
    return FD[f"measurement/{key}"]


def kpi_uri(subject_id: str, kpi_name: str) -> URIRef:
    return FD[f"kpi/{_make_url_safe(subject_id)}/{_make_url_safe(kpi_name)}"]


def instrument_uri(instrument_id: str) -> URIRef:
    return FD[f"instrument/{_make_url_safe(instrument_id)}"]
