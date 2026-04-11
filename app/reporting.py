from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pandas as pd

from models.kpi_model import KPIResult


def print_kpi_result(result: KPIResult) -> None:
    status = "REJECTED" if result.is_rejected else "ACCEPTED"

    print("-------")
    print(f"Entity: {result.entity_id} [{result.kpi_name}]  [{status}]")

    if result.value is None:
        print(f"value: N/A {result.unit}")
    else:
        print(f"value: {result.value:.4f} {result.unit}")

    if result.flags:
        print("flags:", result.flags)

    if result.rejection_reasons:
        print("Rejection reasons:", result.rejection_reasons)


def write_output_csv(results_list: List[KPIResult], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for r in results_list:
        d = asdict(r)
        d.update(d.pop("provenance"))
        rows.append(d)
    pd.DataFrame(rows).to_csv(output_path, index=False)
