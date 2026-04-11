from collections import defaultdict
from datetime import datetime as dt
from html import escape
from pathlib import Path
from typing import Dict, List

from models.kpi_model import KPIResult, Measurement, Provenance


_PLOT_KPI_NAMES = {
    "Basal_Area",
    "Species_Diversity_Shannon",
    "Regeneration_Density",
    "Stand_Density",
}

_CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #f5f6f7;
    color: #1a1a1a;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    line-height: 1.6;
  }
  header { background: #fff; border-bottom: 1px solid #e0e0e0; padding: 28px 40px; }
  header h1 { font-size: 1.25rem; font-weight: 600; }
  header .sub { color: #888; font-size: 0.78rem; margin-top: 3px; }
  .summary { display: flex; gap: 16px; padding: 24px 40px 0; }
  .card { background: #fff; border: 1px solid #e0e0e0; border-radius: 6px; padding: 20px 24px; flex: 1; }
  .card .num { font-size: 2rem; font-weight: 700; }
  .card.c-rej .num { color: #b94040; }
  .card .lbl { font-size: 0.72rem; color: #888; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.4px; }
  .body { padding: 28px 40px 60px; display: flex; flex-direction: column; gap: 36px; }
  h2 {
    font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.6px; color: #555;
    margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px solid #e0e0e0;
  }
  .tbl-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #e0e0e0; border-radius: 6px; overflow: hidden; }
  th {
    background: #fafafa; color: #888; text-align: left; padding: 9px 14px;
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.4px; border-bottom: 1px solid #e0e0e0;
  }
  td { padding: 9px 14px; border-bottom: 1px solid #f0f0f0; vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr.rejected td { background: #fff8f8; color: #b94040; }
  tr:not(.rejected):hover td { background: #fafafa; }
  details { background: #fff; border: 1px solid #e0e0e0; border-radius: 6px; overflow: hidden; }
  summary {
    cursor: pointer; padding: 12px 16px; font-size: 0.78rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px; color: #555;
    background: #fafafa; border-bottom: 1px solid #e0e0e0;
    list-style: none; display: flex; align-items: center; gap: 8px; user-select: none;
  }
  summary::before { content: "\\25B6"; font-size: 0.55rem; transition: transform 0.2s; color: #aaa; }
  details[open] summary::before { transform: rotate(90deg); }
"""


# --- row renderers ---


def _precision_str(p: Provenance) -> str:
    if p.precision_cm is not None:
        return f"&plusmn;{p.precision_cm}&thinsp;cm"
    if p.precision_m is not None:
        return f"&plusmn;{p.precision_m}&thinsp;m"
    if p.accuracy_percent is not None:
        return f"{p.accuracy_percent}% accuracy"
    return "&mdash;"


def _disp(value: object) -> str:
    if value is None:
        return "&mdash;"
    text = str(value)
    if text == "" or text.lower() == "nan":
        return "&mdash;"
    return escape(text)


def _notes(flags: List[str], rejections: List[str]) -> str:
    parts = list(flags) + [r for r in rejections if r not in flags]
    return escape("; ".join(parts)) if parts else "&mdash;"


def _tree_row(r: KPIResult) -> str:
    val = f"{r.value:.4f}" if r.value is not None else "&mdash;"
    cls = ' class="rejected"' if r.is_rejected else ""
    status = "Rejected" if r.is_rejected else "Accepted"
    return (
        f"<tr{cls}>"
        f"<td>{_disp(r.entity_id)}</td>"
        f"<td>{_disp(r.kpi_name.replace('_', ' '))}</td>"
        f"<td>{val}</td>"
        f"<td>{escape(r.unit)}</td>"
        f"<td>{_disp(r.provenance.instrument_id)}</td>"
        f"<td>{_precision_str(r.provenance)}</td>"
        f"<td>{status}</td>"
        f"<td>{_notes(r.flags, r.rejection_reasons)}</td>"
        "</tr>"
    )


def _plot_row(pid: str, r: KPIResult) -> str:
    val = f"{r.value:.4f}" if r.value is not None else "&mdash;"
    cls = ' class="rejected"' if r.is_rejected else ""
    status = "Rejected" if r.is_rejected else "Accepted"
    trees_used = (
        f"{r.tree_count_used} / {r.tree_count_total}"
        if r.tree_count_used is not None
        else "&mdash;"
    )
    return (
        f"<tr{cls}>"
        f"<td>{_disp(pid)}</td>"
        f"<td>{_disp(r.kpi_name.replace('_', ' '))}</td>"
        f"<td>{val}</td>"
        f"<td>{escape(r.unit)}</td>"
        f"<td>{trees_used}</td>"
        f"<td>{status}</td>"
        f"<td>{_notes(r.flags, r.rejection_reasons)}</td>"
        "</tr>"
    )


def _measurement_row(m: Measurement) -> str:
    return (
        "<tr>"
        f"<td>{_disp(m.tree_id)}</td>"
        f"<td>{_disp(m.plot_id)}</td>"
        f"<td>{_disp(m.date)}</td>"
        f"<td>{_disp(m.measurement_type.upper())}</td>"
        f"<td>{_disp(m.value)}</td>"
        f"<td>{_disp(m.species)}</td>"
        f"<td>{_disp(m.instrument_id)}</td>"
        f"<td>{_disp(m.instrument_method)}</td>"
        f"<td>{_disp(m.status)}</td>"
        "</tr>"
    )


# --- section builders ---


def _table(headers: List[str], rows_html: str) -> str:
    ths = "".join(f"<th>{h}</th>" for h in headers)
    return (
        f'<div class="tbl-wrap"><table>'
        f"<thead><tr>{ths}</tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        f"</table></div>"
    )


def _section(title: str, table_html: str) -> str:
    return f"<h2>{title}</h2>{table_html}"


def _collapsible(title: str, table_html: str) -> str:
    return f"<details><summary>{title}</summary>{table_html}</details>"


# --- main entry point ---


def write_dashboard(
    kpi_results: List[KPIResult],
    measurements: List[Measurement],
    path: Path,
) -> None:
    results = list(kpi_results)
    accepted = [r for r in results if not r.is_rejected]
    rejected = [r for r in results if r.is_rejected]

    tree_results = [r for r in results if r.kpi_name not in _PLOT_KPI_NAMES]

    plot_results: Dict[str, List[KPIResult]] = defaultdict(list)
    for r in results:
        if r.kpi_name in _PLOT_KPI_NAMES:
            plot_results[r.entity_id].append(r)

    tree_rows = "".join(_tree_row(r) for r in tree_results)
    plot_rows = "".join(
        _plot_row(pid, r) for pid in sorted(plot_results) for r in plot_results[pid]
    )
    input_rows = "".join(_measurement_row(m) for m in measurements)

    tree_section = (
        _section(
            "Tree-Level Results",
            _table(
                [
                    "Tree",
                    "KPI",
                    "Value",
                    "Unit",
                    "Instrument",
                    "Precision",
                    "Status",
                    "Notes",
                ],
                tree_rows,
            ),
        )
        if tree_rows
        else ""
    )

    plot_section = (
        _section(
            "Plot-Level Results",
            _table(
                ["Plot", "KPI", "Value", "Unit", "Trees Used", "Status", "Notes"],
                plot_rows,
            ),
        )
        if plot_rows
        else ""
    )

    raw_section = _collapsible(
        f"Raw Input Measurements &nbsp;({len(measurements)} rows)",
        _table(
            [
                "Tree",
                "Plot",
                "Date",
                "Type",
                "Value",
                "Species",
                "Instrument",
                "Method",
                "Status",
            ],
            input_rows,
        ),
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Forest KPI Dashboard</title>
<style>{_CSS}</style>
</head>
<body>

<header>
  <h1>Forest KPI Dashboard</h1>
  <div class="sub">Generated {dt.now().strftime("%Y-%m-%d %H:%M")} &nbsp;&middot;&nbsp; {len(results)} result(s) across {len(plot_results)} plot(s)</div>
</header>

<div class="summary">
  <div class="card"><div class="num">{len(results)}</div><div class="lbl">Total Results</div></div>
  <div class="card"><div class="num">{len(accepted)}</div><div class="lbl">Accepted</div></div>
  <div class="card c-rej"><div class="num">{len(rejected)}</div><div class="lbl">Rejected</div></div>
  <div class="card"><div class="num">{len(plot_results)}</div><div class="lbl">Plots</div></div>
</div>

<div class="body">
  {tree_section}
  {plot_section}
  {raw_section}
</div>

</body>
</html>"""

    path.write_text(html, encoding="utf-8")
    print(f"\nDashboard written -> {path.name}")
