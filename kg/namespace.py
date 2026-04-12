from rdflib import Namespace
from enum import Enum

__all__ = ["FOREST", "FD"]

# Ontology namespace — (classes like Tree, Plot)
FOREST = Namespace("http://forest-kpi.org/ontology#")

# Data namespace — instance URIs
FD = Namespace("http://forest-kpi.org/data/")
