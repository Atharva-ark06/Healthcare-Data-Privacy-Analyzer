import unittest

import pandas as pd

from modules.classification import classify_attributes
from modules.masking import apply_all_masking, generalize_age, suppress_pin, swap_age
from modules.risk_analysis import calculate_risk
from modules.utility_analysis import calculate_information_loss, privacy_improvement


def sample_df():
    return pd.DataFrame({
        "Patient ID": ["P1", "P2", "P3", "P4"],
        "Age": [22, 22, 45, 52],
        "Gender": ["F", "F", "M", "F"],
        "PIN Code": ["577001", "577001", "577004", "577002"],
        "Department": ["Cardiology", "Cardiology", "General", "General"],
        "Disease": ["Asthma", "Asthma", "Diabetes", "Diabetes"],
        "Treatment": ["Inhaler", "Inhaler", "Medicine", "Medicine"],
    })


class ClassificationTests(unittest.TestCase):
    def test_known_and_unknown_columns(self):
        result = classify_attributes(pd.DataFrame(columns=["Patient ID", "Age", "Notes"]))
        mapping = dict(zip(result["Attribute"], result["Classification"]))
        self.assertEqual(mapping["Patient ID"], "Direct Identifier")
        self.assertEqual(mapping["Age"], "Quasi-Identifier")
        self.assertEqual(mapping["Notes"], "Unknown")


class RiskAnalysisTests(unittest.TestCase):
    def test_duplicate_quasi_identifiers_share_risk_and_id_is_not_used(self):
        df = sample_df()
        result = calculate_risk(df)
        self.assertEqual(result.loc[0, "Group Size"], 2)
        self.assertEqual(result.loc[1, "Group Size"], 2)
        self.assertEqual(result.loc[0, "Re-identification Risk"], 50.0)
        changed_id = df.copy()
        changed_id["Patient ID"] = ["X", "Y", "Z", "W"]
        pd.testing.assert_series_equal(
            calculate_risk(df)["Re-identification Risk"],
            calculate_risk(changed_id)["Re-identification Risk"],
        )

    def test_missing_quasi_identifier_has_clear_error(self):
        with self.assertRaisesRegex(ValueError, "Age"):
            calculate_risk(pd.DataFrame({"Gender": ["F"]}))

    def test_empty_dataframe_returns_empty_result_with_metric_columns(self):
        df = sample_df().iloc[0:0]
        result = calculate_risk(df)
        self.assertTrue(result.empty)
        self.assertIn("Group Size", result.columns)
        self.assertIn("Re-identification Risk", result.columns)

    def test_nan_quasi_identifiers_are_counted_consistently(self):
        df = sample_df()
        df.loc[0, "Gender"] = None
        df.loc[1, "Gender"] = None
        result = calculate_risk(df)
        self.assertEqual(result.loc[0, "Group Size"], 2)
        self.assertEqual(result.loc[1, "Group Size"], 2)

    def test_non_default_duplicate_index_preserves_row_order(self):
        df = sample_df()
        df.index = [10, 10, 4, 2]
        result = calculate_risk(df)
        self.assertEqual(result["Patient ID"].tolist(), df["Patient ID"].tolist())


class MaskingTests(unittest.TestCase):
    def test_suppression_preserves_missing_pin(self):
        df = sample_df()
        df.loc[0, "PIN Code"] = None
        result = suppress_pin(df)
        self.assertEqual(result.loc[1, "PIN Code"], "577***")
        self.assertTrue(pd.isna(result.loc[0, "PIN Code"]))

    def test_age_generalization_uses_correct_boundaries(self):
        df = pd.DataFrame({"Age": [0, 29, 30, 39, 40, 69, 70, None]})
        result = generalize_age(df)
        self.assertEqual(str(result["Age"].iloc[0]), "0-29")
        self.assertEqual(str(result["Age"].iloc[1]), "0-29")
        self.assertEqual(str(result["Age"].iloc[2]), "30-39")
        self.assertEqual(str(result["Age"].iloc[4]), "40-49")
        self.assertEqual(str(result["Age"].iloc[6]), "70+")
        self.assertTrue(pd.isna(result["Age"].iloc[7]))

    def test_swapping_works_with_non_default_index(self):
        df = pd.DataFrame({"Age": [22, 25, 31, 45]}, index=[10, 20, 30, 40])
        result = swap_age(df)
        self.assertEqual(result["Age"].tolist(), [25, 22, 45, 31])
        self.assertEqual(df["Age"].tolist(), [22, 25, 31, 45])

    def test_missing_required_column_has_clear_error(self):
        with self.assertRaisesRegex(ValueError, "PIN Code"):
            suppress_pin(pd.DataFrame({"Age": [22]}))

    def test_combined_masking_preserves_shape_and_columns(self):
        df = sample_df()
        result = apply_all_masking(df)
        self.assertEqual(result.shape, df.shape)
        self.assertEqual(result.columns.tolist(), df.columns.tolist())
        self.assertEqual(result["PIN Code"].iloc[0], "577***")


class UtilityTests(unittest.TestCase):
    def test_information_loss_counts_all_cells(self):
        original = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        masked = pd.DataFrame({"a": [1, 3], "b": ["x", "z"]})
        self.assertEqual(calculate_information_loss(original, masked), 50.0)

    def test_information_loss_treats_missing_values_as_equal(self):
        original = pd.DataFrame({"a": [None, 1]})
        masked = pd.DataFrame({"a": [None, 2]})
        self.assertEqual(calculate_information_loss(original, masked), 50.0)

    def test_information_loss_rejects_shape_or_schema_mismatch(self):
        with self.assertRaisesRegex(ValueError, "same shape"):
            calculate_information_loss(pd.DataFrame({"a": [1]}), pd.DataFrame({"a": [1, 2]}))
        with self.assertRaisesRegex(ValueError, "identical columns"):
            calculate_information_loss(pd.DataFrame({"a": [1], "b": [2]}), pd.DataFrame({"b": [2], "a": [1]}))

    def test_empty_information_loss_is_zero(self):
        self.assertEqual(calculate_information_loss(pd.DataFrame(), pd.DataFrame()), 0.0)

    def test_privacy_improvement_zero_baseline_and_reduction(self):
        self.assertEqual(privacy_improvement(0, 0), 0.0)
        self.assertEqual(privacy_improvement(80, 20), 75.0)

    def test_privacy_improvement_rejects_non_finite_values(self):
        with self.assertRaises(ValueError):
            privacy_improvement(float("nan"), 20)


if __name__ == "__main__":
    unittest.main()
