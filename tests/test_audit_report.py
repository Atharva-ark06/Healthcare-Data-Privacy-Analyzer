import unittest

import pandas as pd

from modules.audit_report import build_audit_summary, render_audit_html


def sample_model_result():
    return {
        "k": {"passed": False},
        "l": {"passed": True},
        "t": {"passed": False},
        "groups": pd.DataFrame({
            "Passes K-Anonymity": [False, True],
            "Passes L-Diversity": [True, True],
            "Passes T-Closeness": [False, True],
            "Age": [21, 35],
            "PIN Code": ["123456", "654321"],
        }),
    }


class AuditReportTests(unittest.TestCase):
    def test_summary_is_aggregate_and_generates_recommendations(self):
        summary = build_audit_summary(
            technique="Generalization", record_count=5, attribute_count=7,
            information_loss=14.29, original_risk=100, masked_risk=80,
            model_result=sample_model_result(),
        )
        self.assertEqual(summary["failed_group_count"], 1)
        self.assertEqual(summary["failed_conditions"]["k-anonymity"], 1)
        self.assertEqual(summary["risk_change"], -20)
        self.assertGreaterEqual(len(summary["recommendations"]), 2)
        self.assertNotIn("Age", summary)

    def test_html_escapes_untrusted_technique_text(self):
        summary = build_audit_summary(
            technique="<script>alert(1)</script>", record_count=1, attribute_count=2,
            information_loss=0, original_risk=50, masked_risk=25,
            model_result={
                "k": {"passed": True}, "l": {"passed": True}, "t": {"passed": True},
                "groups": pd.DataFrame({
                    "Passes K-Anonymity": [True],
                    "Passes L-Diversity": [True],
                    "Passes T-Closeness": [True],
                }),
            },
        )
        html = render_audit_html(summary)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("does not guarantee anonymity", html)

    def test_rejects_invalid_percentages(self):
        with self.assertRaises(ValueError):
            build_audit_summary(
                technique="None", record_count=1, attribute_count=1,
                information_loss=101, original_risk=0, masked_risk=0,
                model_result=sample_model_result(),
            )

    def test_rejects_missing_group_columns(self):
        with self.assertRaises(ValueError):
            build_audit_summary(
                technique="None", record_count=1, attribute_count=1,
                information_loss=0, original_risk=0, masked_risk=0,
                model_result={"k": {"passed": True}, "l": {"passed": True},
                              "t": {"passed": True}, "groups": pd.DataFrame({"x": [1]})},
            )


if __name__ == "__main__":
    unittest.main()
