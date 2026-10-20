import unittest

import pandas as pd

from modules.privacy_models import analyze_privacy_models


def privacy_df():
    return pd.DataFrame({
        "Age": [20, 20, 30, 30, 40, 40],
        "Gender": ["F", "F", "M", "M", "F", "F"],
        "PIN Code": ["A", "A", "B", "B", "C", "C"],
        "Department": ["Cardiology", "Cardiology", "General", "General", "Surgery", "Surgery"],
        "Disease": ["Asthma", "Diabetes", "Asthma", "Diabetes", "Asthma", "Asthma"],
    })


class PrivacyModelTests(unittest.TestCase):
    def test_group_sizes_and_k_anonymity(self):
        result = analyze_privacy_models(privacy_df(), k=2, l=2, t=1.0)
        self.assertTrue(result["k"]["passed"])
        self.assertEqual(result["k"]["observed_minimum"], 2)
        self.assertEqual(result["group_count"], 3)

    def test_k_anonymity_fails_for_singleton_group(self):
        df = privacy_df()
        df.loc[0, "PIN Code"] = "unique"
        result = analyze_privacy_models(df, k=2, l=1, t=1.0)
        self.assertFalse(result["k"]["passed"])

    def test_l_diversity_uses_distinct_sensitive_values(self):
        result = analyze_privacy_models(privacy_df(), k=2, l=2, t=1.0)
        self.assertFalse(result["l"]["passed"])
        self.assertEqual(result["l"]["observed_minimum"], 1)

    def test_t_closeness_distance_is_bounded(self):
        result = analyze_privacy_models(privacy_df(), k=2, l=1, t=1.0)
        distances = result["groups"]["T-Closeness Distance"]
        self.assertTrue(((distances >= 0) & (distances <= 1)).all())
        self.assertTrue(result["t"]["passed"])

    def test_missing_sensitive_values_are_counted_as_category(self):
        df = privacy_df()
        df.loc[0, "Disease"] = None
        result = analyze_privacy_models(df, k=2, l=1, t=1.0)
        self.assertEqual(result["record_count"], 6)
        self.assertEqual(result["groups"]["Distinct Sensitive Values"].min(), 1)

    def test_missing_required_columns_raise_clear_error(self):
        with self.assertRaisesRegex(ValueError, "Disease"):
            analyze_privacy_models(pd.DataFrame({"Age": [20]}))

    def test_empty_dataset_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            analyze_privacy_models(privacy_df().iloc[0:0])

    def test_thresholds_are_validated(self):
        with self.assertRaisesRegex(ValueError, "k must"):
            analyze_privacy_models(privacy_df(), k=0)
        with self.assertRaisesRegex(ValueError, "between 0 and 1"):
            analyze_privacy_models(privacy_df(), t=1.5)

    def test_sensitive_attribute_cannot_be_quasi_identifier(self):
        with self.assertRaisesRegex(ValueError, "cannot also"):
            analyze_privacy_models(privacy_df(), quasi_identifiers=["Age", "Disease"])


if __name__ == "__main__":
    unittest.main()
