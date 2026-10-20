"""Aggregate privacy audit summaries and self-contained HTML report export.

Reports intentionally avoid exporting raw records or exact quasi-identifier values.
This is an educational diagnostic, not a legal or clinical compliance certification.
"""
from __future__ import annotations

from html import escape
from datetime import datetime, timezone
from typing import Any

import pandas as pd


def build_audit_summary(
    *,
    technique: str,
    record_count: int,
    attribute_count: int,
    information_loss: float,
    original_risk: float,
    masked_risk: float,
    model_result: dict[str, Any],
) -> dict[str, Any]:
    """Build a validated, aggregate-only audit summary from analysis results."""
    if not isinstance(technique, str) or not technique.strip():
        raise ValueError("technique must be a non-empty string")
    if isinstance(record_count, bool) or not isinstance(record_count, int) or record_count < 0:
        raise ValueError("record_count must be a non-negative integer")
    if isinstance(attribute_count, bool) or not isinstance(attribute_count, int) or attribute_count < 0:
        raise ValueError("attribute_count must be a non-negative integer")
    for name, value in (("information_loss", information_loss), ("original_risk", original_risk), ("masked_risk", masked_risk)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be numeric")
        if not 0 <= float(value) <= 100:
            raise ValueError(f"{name} must be between 0 and 100")
    if not isinstance(model_result, dict) or not all(key in model_result for key in ("k", "l", "t", "groups")):
        raise ValueError("model_result must contain k, l, t, and groups results")

    groups = model_result["groups"]
    if not isinstance(groups, pd.DataFrame):
        raise TypeError("model_result['groups'] must be a DataFrame")
    required = {"Passes K-Anonymity", "Passes L-Diversity", "Passes T-Closeness"}
    if not required.issubset(groups.columns):
        raise ValueError("group results are missing required pass/fail columns")

    checks = {
        "k-anonymity": bool(model_result["k"]["passed"]),
        "l-diversity": bool(model_result["l"]["passed"]),
        "t-closeness": bool(model_result["t"]["passed"]),
    }
    failed = groups.loc[~groups[list(required)].all(axis=1)]
    failed_conditions = {
        "k-anonymity": int((~groups["Passes K-Anonymity"]).sum()),
        "l-diversity": int((~groups["Passes L-Diversity"]).sum()),
        "t-closeness": int((~groups["Passes T-Closeness"]).sum()),
    }
    recommendations = []
    if not checks["k-anonymity"]:
        recommendations.append("Review rare quasi-identifier groups; consider broader generalization or suppression, then rerun the checks.")
    if not checks["l-diversity"]:
        recommendations.append("Review groups with limited sensitive-value diversity; reduce disclosure risk before release.")
    if not checks["t-closeness"]:
        recommendations.append("Review groups whose sensitive-value distribution differs from the dataset baseline; consider stronger grouping or suppression.")
    if float(information_loss) > 30:
        recommendations.append("Information loss is high; assess whether the protected data remains useful for its intended analysis.")
    if not recommendations:
        recommendations.append("No configured model threshold failed. Review the assumptions and dataset context before any release.")

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "technique": technique.strip(),
        "record_count": record_count,
        "attribute_count": attribute_count,
        "information_loss": round(float(information_loss), 2),
        "original_risk": round(float(original_risk), 2),
        "masked_risk": round(float(masked_risk), 2),
        "risk_change": round(float(masked_risk) - float(original_risk), 2),
        "checks": checks,
        "group_count": int(len(groups)),
        "failed_group_count": int(len(failed)),
        "failed_conditions": failed_conditions,
        "recommendations": recommendations,
    }


def render_audit_html(summary: dict[str, Any]) -> str:
    """Render a self-contained HTML report without raw records or group identifiers."""
    required = {"generated_at", "technique", "record_count", "attribute_count", "information_loss",
                "original_risk", "masked_risk", "risk_change", "checks", "group_count",
                "failed_group_count", "failed_conditions", "recommendations"}
    if not isinstance(summary, dict) or not required.issubset(summary):
        raise ValueError("summary is missing required audit fields")

    esc = lambda value: escape(str(value))
    checks = "".join(
        f"<tr><th>{esc(name)}</th><td class=\"{'pass' if passed else 'fail'}\">{'PASS' if passed else 'FAIL'}</td></tr>"
        for name, passed in summary["checks"].items()
    )
    failures = "".join(
        f"<tr><th>{esc(name)}</th><td>{int(count)}</td></tr>"
        for name, count in summary["failed_conditions"].items()
    )
    recommendations = "".join(f"<li>{esc(item)}</li>" for item in summary["recommendations"])
    risk_change = float(summary["risk_change"])
    change_label = "increased" if risk_change > 0 else "decreased" if risk_change < 0 else "did not change"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Healthcare Data Privacy Audit</title>
<style>
body{{font:16px/1.55 system-ui,sans-serif;max-width:900px;margin:36px auto;padding:0 20px;color:#172033}}
h1,h2{{line-height:1.2}} .muted{{color:#596579}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}
.card{{border:1px solid #d7deea;border-radius:10px;padding:14px}} table{{border-collapse:collapse;width:100%;margin:12px 0 24px}}
th,td{{border:1px solid #d7deea;padding:9px;text-align:left}} .pass{{color:#167345;font-weight:700}} .fail{{color:#b42318;font-weight:700}}
.notice{{background:#f4f6fa;padding:14px;border-radius:8px}} @media print{{body{{margin:0;max-width:none}}}}
</style></head><body>
<h1>Healthcare Data Privacy Audit</h1>
<p class="muted">Generated {esc(summary["generated_at"])} · Educational diagnostic report</p>
<div class="grid">
<div class="card"><strong>Masking technique</strong><br>{esc(summary["technique"])}</div>
<div class="card"><strong>Records / attributes</strong><br>{int(summary["record_count"])} / {int(summary["attribute_count"])}</div>
<div class="card"><strong>Information loss</strong><br>{float(summary["information_loss"]):.2f}%</div>
<div class="card"><strong>Original risk proxy</strong><br>{float(summary["original_risk"]):.2f}%</div>
<div class="card"><strong>Masked risk proxy</strong><br>{float(summary["masked_risk"]):.2f}%</div>
<div class="card"><strong>Risk proxy change</strong><br>{abs(risk_change):.2f} percentage points {change_label}</div>
</div>
<h2>Formal privacy model checks</h2><table><thead><tr><th>Model</th><th>Result</th></tr></thead><tbody>{checks}</tbody></table>
<h2>Group-level failures</h2>
<p>{int(summary["failed_group_count"])} of {int(summary["group_count"])} groups fail at least one configured check.</p>
<table><thead><tr><th>Failed condition</th><th>Number of groups</th></tr></thead><tbody>{failures}</tbody></table>
<h2>Recommended follow-up</h2><ul>{recommendations}</ul>
<div class="notice"><strong>Important limitations:</strong> This report contains aggregate diagnostics only and intentionally excludes raw records and exact quasi-identifier values. Risk scores are simplified educational proxies. Passing these checks does not guarantee anonymity, prevent all re-identification, or certify legal/regulatory compliance. Confirm thresholds, data provenance, consent, access controls, and the intended release context with a qualified reviewer.</div>
</body></html>"""
