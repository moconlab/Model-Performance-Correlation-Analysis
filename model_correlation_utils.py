"""Spearman correlation helpers for model properties vs performance outcomes."""

from __future__ import annotations

from typing import Iterable

import pandas as pd

try:
    from scipy import stats as scipy_stats
except ImportError:  # pragma: no cover
    scipy_stats = None  # type: ignore[assignment]

DEFAULT_PROPERTY_COLUMNS = [
    "PolyCount",
    "Objects",
    "Areas",
    "NonEmptyAreas",
    "UnitVolume",
    "Polys/UnitVolume",
    "Objects/UnitVolume",
    "empty_area_fraction",
    "ms_max_TotalPolyCount",
    "ms_mean_[Time]Render",
]

DEFAULT_OUTCOME_COLUMNS = [
    "init_time_ms",
    "stage_duration_sec",
    "fps",
    "peak_memory_kb",
    "TimeToSee_ms",
    "TimeToBuildBVH_ms",
]


def columns_present(df: pd.DataFrame, candidates: Iterable[str]) -> list[str]:
    return [c for c in candidates if c in df.columns]


def spearman_pair(
    x: pd.Series,
    y: pd.Series,
) -> tuple[float, float, int]:
    pair = pd.concat([x, y], axis=1).dropna()
    n = len(pair)
    if n < 5:
        return float("nan"), float("nan"), n
    if scipy_stats is not None:
        rho, pval = scipy_stats.spearmanr(pair.iloc[:, 0], pair.iloc[:, 1])
        return float(rho), float(pval), n
    # Pandas Spearman also imports scipy; rank + Pearson works without it.
    ranked = pair.rank(method="average")
    rho = ranked.iloc[:, 0].corr(ranked.iloc[:, 1], method="pearson")
    return float(rho), float("nan"), n


def spearman_correlation_table(
    data: pd.DataFrame,
    properties: list[str],
    outcomes: list[str],
    *,
    min_samples: int = 5,
) -> pd.DataFrame:
    """Long-form Spearman ρ and p-value for each property × outcome pair."""
    rows: list[dict[str, object]] = []
    for outcome in outcomes:
        for prop in properties:
            rho, pval, n = spearman_pair(data[prop], data[outcome])
            if n < min_samples:
                continue
            rows.append(
                {
                    "outcome": outcome,
                    "property": prop,
                    "spearman_rho": rho,
                    "p_value": pval,
                    "n": n,
                }
            )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["abs_rho"] = out["spearman_rho"].abs()
    return out.sort_values(["outcome", "abs_rho"], ascending=[True, False])


def top_correlations_for_outcome(
    corr_table: pd.DataFrame,
    outcome: str,
    *,
    top_n: int = 8,
) -> pd.DataFrame:
    subset = corr_table[corr_table["outcome"] == outcome]
    return subset.head(top_n)


def spearman_matrix(
    data: pd.DataFrame,
    row_cols: list[str],
    col_cols: list[str],
) -> pd.DataFrame:
    block = data[row_cols + col_cols]
    ranked = block.rank(method="average")
    full = ranked.corr(method="pearson")
    return full.loc[row_cols, col_cols]
