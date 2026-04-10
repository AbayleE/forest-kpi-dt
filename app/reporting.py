from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pandas as pd

from models.kpi_model import KPIResult


def print_kpi_result(result: KPIResult) -> None:
    status = "REJECTED" if result.is_rejected else "ACCEPTED"

    print("-----")
    print(f"Entity: {result.entity_id} [{result.kpi_name}]  [{status}]")
    if result.value is not None:
        print(f"Value: {result.value:.4f} {result.unit}")
    else:
        print(f"Value: N/A {result.unit}")
    if result.flags:
        print(f"Flags: {result.flags}")
    if result.rejection_reasons:
        print(f"Rejection reasons: {result.rejection_reasons}")


def _flatten_result(result: KPIResult) -> Dict[str, Any]:
    d = asdict(result)
    prov = d.pop("provenance")
    d.update(prov)
    return d


def write_output_csv(results: Iterable[KPIResult], output_path: Path) -> None:
    results_list: List[KPIResult] = list(results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([_flatten_result(r) for r in results_list]).to_csv(output_path, index=False)
