"""Educational k-anonymity, l-diversity, and t-closeness checks.

These checks are diagnostics, not a guarantee of anonymity or safe release.
The implementation uses exact quasi-identifier groups and total-variation
distance for t-closeness.
"""
from __future__ import annotations

import math

import pandas as pd


DEFAULT_QUASI_IDENTIFIERS = ["Age", "Gender", "PIN Code", "Department"]


def _validate_thresholds(k: int, l: int, t: float) -> None:
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be an integer greater than or equal to 1")
    if isinstance(l, bool) or not isinstance(l, int) or l < 1:
        raise ValueError("l must be an integer greater than or equal to 1")
    if isinstance(t, bool) or not isinstance(t, (int, float)):
        raise TypeError("t must be a numeric value between 0 and 1")
    if not math.isfinite(t) or not 0 <= t <= 1:
        raise ValueError("t must be between 0 and 1")


def analyze_privacy_models(
    df: pd.DataFrame,
    quasi_identifiers: list[str] | None = None,
    sensitive_attribute: str = "Disease",
    k: int = 2,
    l: int = 2,
    t: float = 0.2,
) -> dict:
    """Evaluate k-anonymity, distinct-value l-diversity and t-closeness.

    T-closeness is the total-variation distance between a group's sensitive
    value distribution and the full dataset's distribution:
    0.5 * sum(abs(group_probability - global_probability)).

    Missing sensitive values are treated as an explicit category. Missing
    quasi-identifier values are grouped together by pandas' dropna=False.
    """
    _validate_thresholds(k, l, t)
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    qis = list(quasi_identifiers or DEFAULT_QUASI_IDENTIFIERS)
    if not qis:
        raise ValueError("At least one quasi-identifier is required")
    if len(set(qis)) != len(qis):
        raise ValueError("Quasi-identifiers must not contain duplicates")
    if sensitive_attribute in qis:
        raise ValueError("Sensitive attribute cannot also be a quasi-identifier")

    required = qis + [sensitive_attribute]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))
    if df.empty:
        raise ValueError("Cannot evaluate privacy models on an empty dataset")

    work = df[required].copy().reset_index(drop=True)
    # A collision-safe sentinel makes missing sensitive values count as a
    # category without confusing them with actual string values.
    missing_token = object()
    sensitive_values = work[sensitive_attribute].astype(object).where(
        work[sensitive_attribute].notna(), missing_token
    )
    work["_privacy_sensitive"] = sensitive_values

    global_counts = work["_privacy_sensitive"].value_counts(dropna=False)
    total = len(work)
    global_distribution = global_counts / total

    grouped = work.groupby(qis, dropna=False, observed=True, sort=False)
    rows = []
    for group_key, group in grouped:
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        group_size = len(group)
        counts = group["_privacy_sensitive"].value_counts(dropna=False)
        distinct_sensitive = int(counts.size)
        distribution = counts / group_size
        aligned_group, aligned_global = distribution.align(
            global_distribution, join="outer", fill_value=0.0
        )
        distance = float((aligned_group - aligned_global).abs().sum() / 2.0)

        row = {column: value for column, value in zip(qis, group_key)}
        row.update({
            "Group Size": group_size,
            "Distinct Sensitive Values": distinct_sensitive,
            "T-Closeness Distance": round(distance, 4),
            "Passes K-Anonymity": group_size >= k,
            "Passes L-Diversity": distinct_sensitive >= l,
            "Passes T-Closeness": distance <= t,
        })
        rows.append(row)

    group_results = pd.DataFrame(rows)
    min_group_size = int(group_results["Group Size"].min())
    min_l_diversity = int(group_results["Distinct Sensitive Values"].min())
    max_t_distance = float(group_results["T-Closeness Distance"].max())

    return {
        "k": {
            "threshold": k,
            "observed_minimum": min_group_size,
            "passed": bool((group_results["Group Size"] >= k).all()),
        },
        "l": {
            "threshold": l,
            "observed_minimum": min_l_diversity,
            "passed": bool((group_results["Distinct Sensitive Values"] >= l).all()),
        },
        "t": {
            "threshold": float(t),
            "observed_maximum": round(max_t_distance, 4),
            "passed": bool((group_results["T-Closeness Distance"] <= t).all()),
        },
        "groups": group_results,
        "group_count": len(group_results),
        "record_count": total,
        "sensitive_attribute": sensitive_attribute,
        "quasi_identifiers": qis,
    }
