from datetime import datetime as dt
from html import escape
from pathlib import Path
from typing import Iterable, List

import pandas as pd

from models.kpi_model import KPIResult, Provenance


def _precision_str(provenance: Provenance) -> str:
    if provenance.precision_cm is not None:
        return f"&plusmn;{provenance.precision_cm} cm"
    if provenance.precision_m is not None:
        return f"&plusmn;{provenance.precision_m} m"
    if provenance.accuracy_percent is not None:
        return f"{provenance.accuracy_percent}% accuracy"
    return "&mdash;"


def _display_text(value: object) -> str:
    if value is None:
        return "&mdash;"

    text = str(value)
    if text == "" or text.lower() == "nan":
        return "&mdash;"

    return escape(text)


def write_dashboard(
    kpi_results: Iterable[KPIResult],
    measurements_df: pd.DataFrame,
    path: Path,
) -> None:
    results_list: List[KPIResult] = list(kpi_results)
    accepted = [result for result in results_list if not result.is_rejected]
    rejected = [result for result in results_list if result.is_rejected]

    input_rows_html = []
    for _, row in measurements_df.iterrows():
        input_rows_html.append(
            "<tr>"
            f"<td>{_display_text(row['tree_id'])}</td>"
            f"<td>{_display_text(row['date'])}</td>"
            f"<td>{_display_text(str(row['measurement_type']).upper())}</td>"
            f"<td>{_display_text(row['value'])}</td>"
            f"<td>{_display_text(row.get('species'))}</td>"
            f"<td>{_display_text(row['instrument_id'])}</td>"
            f"<td>{_display_text(row.get('instrument_method'))}</td>"
            "</tr>"
        )

    rows_html = []
    for result in results_list:
        status_cls = "rejected" if result.is_rejected else "accepted"
        status_label = "REJECTED" if result.is_rejected else "ACCEPTED"
        notes_parts = list(result.flags) + list(result.rejection_reasons)
        notes = "; ".join(notes_parts) if notes_parts else "&mdash;"
        provenance = result.provenance

        rows_html.append(
            f'<tr class="{status_cls}">'
            f"<td>{_display_text(result.tree_id)}</td>"
            f"<td>{_display_text(result.kpi_name)}</td>"
            f"<td>{escape(f'{result.value:.4f} {result.unit}')}</td>"
            f"<td>{_display_text(provenance.instrument_method)}</td>"
            f"<td>{_precision_str(provenance)}</td>"
            f"<td>{_display_text(provenance.method_version)}</td>"
            f'<td><span class="badge {status_cls}">{status_label}</span></td>'
            f"<td>{notes if notes == '&mdash;' else escape(notes)}</td>"
            "</tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Forest KPI Dashboard</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f4f6f4; color: #222; }}
    header {{ background: #2d6a4f; color: #fff; padding: 20px 32px; }}
    header h1 {{ margin: 0; font-size: 1.4rem; }}
    header p {{ margin: 4px 0 0; font-size: 0.8rem; opacity: .75; }}
    .summary {{ display: flex; gap: 16px; padding: 24px 32px 0; }}
    .card {{ background: #fff; border-radius: 6px; padding: 18px 24px; flex: 1;
             box-shadow: 0 1px 3px rgba(0,0,0,.1); }}
    .card .num {{ font-size: 2.2rem; font-weight: bold; }}
    .card .lbl {{ font-size: 0.78rem; color: #666; margin-top: 4px; }}
    .card.c-total .num {{ color: #2d6a4f; }}
    .card.c-acc .num {{ color: #1b7a4a; }}
    .card.c-rej .num {{ color: #c0392b; }}
    .section {{ padding: 24px 32px 0; }}
    .section h2 {{ font-size: 0.95rem; color: #2d6a4f; margin: 0 0 12px;
                   text-transform: uppercase; letter-spacing: .5px; }}
    .tbl-wrap {{ padding: 24px 32px 48px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff;
             border-radius: 6px; overflow: hidden;
             box-shadow: 0 1px 3px rgba(0,0,0,.1); }}
    th {{ background: #2d6a4f; color: #fff; text-align: left;
          padding: 10px 14px; font-size: 0.82rem; }}
    td {{ padding: 9px 14px; font-size: 0.82rem; border-bottom: 1px solid #eee; }}
    tr.rejected td {{ background: #fff6f6; }}
    tr:last-child td {{ border-bottom: none; }}
    .badge {{ display: inline-block; padding: 2px 10px; border-radius: 99px;
              font-size: 0.72rem; font-weight: bold; }}
    .badge.accepted {{ background: #d8f3dc; color: #1b4332; }}
    .badge.rejected {{ background: #ffe0e0; color: #7b0000; }}
  </style>
</head>
<body>
  <header>
    <h1>Forest KPI Dashboard</h1>
    <p>Generated {dt.now().strftime("%Y-%m-%d %H:%M")}</p>
  </header>
  <div class="summary">
    <div class="card c-total">
      <div class="num">{len(results_list)}</div>
      <div class="lbl">Total KPIs</div>
    </div>
    <div class="card c-acc">
      <div class="num">{len(accepted)}</div>
      <div class="lbl">Accepted</div>
    </div>
    <div class="card c-rej">
      <div class="num">{len(rejected)}</div>
      <div class="lbl">Rejected</div>
    </div>
  </div>
  <div class="section">
    <h2>Input Measurements</h2>
  </div>
  <div class="tbl-wrap">
    <table>
      <thead>
        <tr>
          <th>Tree</th><th>Date</th><th>Type</th><th>Value</th>
          <th>Species</th><th>Instrument ID</th><th>Method</th>
        </tr>
      </thead>
      <tbody>
        {''.join(input_rows_html)}
      </tbody>
    </table>
  </div>
  <div class="section">
    <h2>KPI Results</h2>
  </div>
  <div class="tbl-wrap">
    <table>
      <thead>
        <tr>
          <th>Tree</th><th>KPI</th><th>Value</th><th>Instrument</th>
          <th>Precision</th><th>Version</th><th>Status</th><th>Notes</th>
        </tr>
      </thead>
      <tbody>
        {''.join(rows_html)}
      </tbody>
    </table>
  </div>
</body>
</html>"""

    path.write_text(html, encoding="utf-8")
    print(f"\nDashboard written → {path.name}")
