from pathlib import Path
from typing import Iterable, List

import pandas as pd

from models.kpi_model import KPIResult


def print_insufficient_result(tree_id: str, measurement_type: str) -> None:
    print("-----")
    print(
        f"Tree: {tree_id} [{measurement_type.upper()}]  [REJECTED — insufficient observations]"
    )


def print_kpi_result(result: KPIResult, measurement_type: str) -> None:
    status = "REJECTED" if result.is_rejected else "ACCEPTED"

    print("-----")
    print(f"Tree: {result.tree_id} [{measurement_type.upper()}]  [{status}]")
    print(f"KPI: {result.kpi_name}")
    print(f"Value: {result.value:.4f} {result.unit}")
    if result.flags:
        print(f"Flags: {result.flags}")
    if result.rejection_reasons:
        print(f"Rejection reasons: {result.rejection_reasons}")
    print(f"Provenance: {result.provenance}")


def write_output_csv(results: Iterable[KPIResult], output_path: Path) -> None:
    results_list: List[KPIResult] = list(results)
    pd.DataFrame([result.__dict__ for result in results_list]).to_csv(output_path, index=False)
