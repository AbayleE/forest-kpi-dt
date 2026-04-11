from collections import defaultdict
from datetime import datetime as dt
from html import escape
from pathlib import Path
from typing import Dict, Iterable, List, Set

import pandas as pd

from models.kpi_model import KPIResult, Provenance



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


def write_dashboard(
    kpi_results: Iterable[KPIResult],
    measurements_df: pd.DataFrame,
    path: Path,
    selected_kpis: Set[str] = None,
) -> None:
    results_list: List[KPIResult] = list(kpi_results)
    accepted = [r for r in results_list if not r.is_rejected]
    rejected = [r for r in results_list if r.is_rejected]

    plot_kpi_names = {"Basal_Area", "Species_Diversity_Shannon", "Regeneration_Density", "Stand_Density"}
    tree_results: List[KPIResult] = [r for r in results_list if r.kpi_name not in plot_kpi_names]
    plot_results: Dict[str, List[KPIResult]] = defaultdict(list)
    for r in results_list:
        if r.kpi_name in plot_kpi_names:
            plot_results[r.tree_id].append(r)

    # ── tree-level rows ─────────────────────────────────────────────────────
    tree_rows_html = ""
    for r in tree_results:
        val = f"{r.value:.4f}" if r.value is not None else "&mdash;"
        row_cls = ' class="rejected"' if r.is_rejected else ""
        status = "Rejected" if r.is_rejected else "Accepted"
        tree_rows_html += (
            f"<tr{row_cls}>"
            f"<td>{_disp(r.tree_id)}</td>"
            f"<td>{_disp(r.kpi_name.replace('_', ' '))}</td>"
            f"<td>{val}</td>"
            f"<td>{escape(r.unit)}</td>"
            f"<td>{_disp(r.provenance.instrument_id)}</td>"
            f"<td>{_precision_str(r.provenance)}</td>"
            f"<td>{status}</td>"
            f"<td>{_notes(r.flags, r.rejection_reasons)}</td>"
            "</tr>"
        )

    # ── plot-level rows ──────────────────────────────────────────────────────
    plot_rows_html = ""
    for pid in sorted(plot_results):
        for r in plot_results[pid]:
            val = f"{r.value:.4f}" if r.value is not None else "&mdash;"
            row_cls = ' class="rejected"' if r.is_rejected else ""
            status = "Rejected" if r.is_rejected else "Accepted"
            trees_used = (
                f"{r.tree_count_used} / {r.tree_count_total}"
                if r.tree_count_used is not None else "&mdash;"
            )
            plot_rows_html += (
                f"<tr{row_cls}>"
                f"<td>{_disp(pid)}</td>"
                f"<td>{_disp(r.kpi_name.replace('_', ' '))}</td>"
                f"<td>{val}</td>"
                f"<td>{escape(r.unit)}</td>"
                f"<td>{trees_used}</td>"
                f"<td>{status}</td>"
                f"<td>{_notes(r.flags, r.rejection_reasons)}</td>"
                "</tr>"
            )

    # ── raw input rows ───────────────────────────────────────────────────────
    input_rows_html = ""
    for _, row in measurements_df.iterrows():
        input_rows_html += (
            "<tr>"
            f"<td>{_disp(row['tree_id'])}</td>"
            f"<td>{_disp(row.get('plot_id'))}</td>"
            f"<td>{_disp(row['date'])}</td>"
            f"<td>{_disp(str(row['measurement_type']).upper())}</td>"
            f"<td>{_disp(row['value'])}</td>"
            f"<td>{_disp(row.get('species'))}</td>"
            f"<td>{_disp(row['instrument_id'])}</td>"
            f"<td>{_disp(row.get('instrument_method'))}</td>"
            f"<td>{_disp(row.get('status'))}</td>"
            "</tr>"
        )

    tree_section = f"""
    <h2>Tree-Level Results</h2>
    <div class="tbl-wrap">
      <table>
        <thead><tr>
          <th>Tree</th><th>KPI</th><th>Value</th><th>Unit</th>
          <th>Instrument</th><th>Precision</th><th>Status</th><th>Notes</th>
        </tr></thead>
        <tbody>{tree_rows_html}</tbody>
      </table>
    </div>""" if tree_rows_html else ""

    plot_section = f"""
    <h2>Plot-Level Results</h2>
    <div class="tbl-wrap">
      <table>
        <thead><tr>
          <th>Plot</th><th>KPI</th><th>Value</th><th>Unit</th>
          <th>Trees Used</th><th>Status</th><th>Notes</th>
        </tr></thead>
        <tbody>{plot_rows_html}</tbody>
      </table>
    </div>""" if plot_rows_html else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Forest KPI Dashboard</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #f5f6f7;
    color: #1a1a1a;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    line-height: 1.6;
  }}
  header {{
    background: #fff;
    border-bottom: 1px solid #e0e0e0;
    padding: 28px 40px;
  }}
  header h1 {{
    font-size: 1.25rem;
    font-weight: 600;
    color: #1a1a1a;
  }}
  header .sub {{
    color: #888;
    font-size: 0.78rem;
    margin-top: 3px;
  }}
  .summary {{
    display: flex;
    gap: 16px;
    padding: 24px 40px 0;
  }}
  .card {{
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 20px 24px;
    flex: 1;
  }}
  .card .num {{
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a1a;
  }}
  .card.c-rej .num {{ color: #b94040; }}
  .card .lbl {{
    font-size: 0.72rem;
    color: #888;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }}
  .body {{
    padding: 28px 40px 60px;
    display: flex;
    flex-direction: column;
    gap: 36px;
  }}
  h2 {{
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #555;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid #e0e0e0;
  }}
  .tbl-wrap {{ overflow-x: auto; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    overflow: hidden;
  }}
  th {{
    background: #fafafa;
    color: #888;
    text-align: left;
    padding: 9px 14px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    border-bottom: 1px solid #e0e0e0;
  }}
  td {{
    padding: 9px 14px;
    border-bottom: 1px solid #f0f0f0;
    color: #1a1a1a;
    vertical-align: middle;
  }}
  tr:last-child td {{ border-bottom: none; }}
  tr.rejected td {{ background: #fff8f8; color: #b94040; }}
  tr:not(.rejected):hover td {{ background: #fafafa; }}
  details {{
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    overflow: hidden;
  }}
  summary {{
    cursor: pointer;
    padding: 12px 16px;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #555;
    background: #fafafa;
    border-bottom: 1px solid #e0e0e0;
    list-style: none;
    display: flex;
    align-items: center;
    gap: 8px;
    user-select: none;
  }}
  summary::before {{
    content: "\\25B6";
    font-size: 0.55rem;
    transition: transform 0.2s;
    color: #aaa;
  }}
  details[open] summary::before {{ transform: rotate(90deg); }}
  details .tbl-wrap {{ padding: 0; }}
</style>
</head>
<body>

<header>
  <h1>Forest KPI Dashboard</h1>
  <div class="sub">Generated {dt.now().strftime("%Y-%m-%d %H:%M")} &nbsp;&middot;&nbsp; {len(results_list)} result(s) across {len(plot_results)} plot(s)</div>
</header>

<div class="summary">
  <div class="card">
    <div class="num">{len(results_list)}</div>
    <div class="lbl">Total Results</div>
  </div>
  <div class="card">
    <div class="num">{len(accepted)}</div>
    <div class="lbl">Accepted</div>
  </div>
  <div class="card c-rej">
    <div class="num">{len(rejected)}</div>
    <div class="lbl">Rejected</div>
  </div>
  <div class="card">
    <div class="num">{len(plot_results)}</div>
    <div class="lbl">Plots</div>
  </div>
</div>

<div class="body">
  {tree_section}
  {plot_section}

  <details>
    <summary>Raw Input Measurements &nbsp;({len(measurements_df)} rows)</summary>
    <div class="tbl-wrap">
      <table>
        <thead><tr>
          <th>Tree</th><th>Plot</th><th>Date</th><th>Type</th><th>Value</th>
          <th>Species</th><th>Instrument</th><th>Method</th><th>Status</th>
        </tr></thead>
        <tbody>{input_rows_html}</tbody>
      </table>
    </div>
  </details>
</div>

</body>
</html>"""

    path.write_text(html, encoding="utf-8")
    print(f"\nDashboard written -> {path.name}")
