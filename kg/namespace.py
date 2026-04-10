"""
RDF namespace definitions for the Forest KPI knowledge graph.

Two namespaces are used throughout the ``kg`` package:

* ``FOREST`` (``http://forest-kpi.org/ontology#``) — ontology terms: RDF
  classes (e.g. ``FOREST.Tree``) and properties (e.g. ``FOREST.hasKPI``).
* ``FD`` (``http://forest-kpi.org/data/``) — data instance URIs for
  concrete entities such as individual trees, plots, measurements and
  computed KPI results.

The attribute accesses on ``FOREST`` and ``FD`` below serve as a
living catalogue of the vocabulary; rdflib resolves them dynamically so
no explicit declaration is strictly required, but listing them here
makes the ontology self-documenting.
"""

from rdflib import Namespace
from rdflib.namespace import RDF, XSD  # re-exported for convenience

__all__ = ["FOREST", "FD", "RDF", "XSD"]

# Ontology namespace — class and property URIs
FOREST = Namespace("http://forest-kpi.org/ontology#")

# Data namespace — instance URIs
FD = Namespace("http://forest-kpi.org/data/")

# ── Classes ──────────────────────────────────────────────────────────────────
# Core domain classes
FOREST.Tree
FOREST.Plot
FOREST.Measurement
FOREST.KPIResult

# KPI sub-classes (one per computed indicator)
FOREST.BasalArea
FOREST.AbovegroundBiomass
FOREST.DBHGrowth
FOREST.HeightGrowth
FOREST.SpeciesDiversity
FOREST.RegenerationDensity
FOREST.StandDensity

# ── Object properties ─────────────────────────────────────────────────────────
FOREST.isIn            # Tree → isIn → Plot
FOREST.hasKPI          # Tree/Plot → hasKPI → KPIResult
FOREST.hasMeasurement  # Tree → hasMeasurement → Measurement
FOREST.computedFrom    # KPIResult → computedFrom → Measurement

# ── Datatype properties ───────────────────────────────────────────────────────
FOREST.value
FOREST.unit
FOREST.timestamp
FOREST.hasFlag
FOREST.isRejected
FOREST.rejectionReason
FOREST.methodVersion
FOREST.instrumentId
FOREST.treeCountUsed
FOREST.treeCountTotal
