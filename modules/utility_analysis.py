import math

import pandas as pd


def calculate_information_loss(original_df, masked_df):
    """Return the percentage of cells whose values changed after masking.

    Both frames must have the same shape and column order so the metric has
    an unambiguous denominator. Missing values are compared as missing values.
    """
    if not isinstance(original_df, pd.DataFrame) or not isinstance(masked_df, pd.DataFrame):
        raise TypeError("original_df and masked_df must be pandas DataFrames")
    if original_df.shape != masked_df.shape:
        raise ValueError("original_df and masked_df must have the same shape")
    if not original_df.columns.equals(masked_df.columns):
        raise ValueError("original_df and masked_df must have identical columns in the same order")

    total_cells = original_df.size
    if total_cells == 0:
        return 0.0

    equal = original_df.eq(masked_df) | (original_df.isna() & masked_df.isna())
    changed_cells = int((~equal).to_numpy().sum())
    return round((changed_cells / total_cells) * 100, 2)


def privacy_improvement(original_risk, masked_risk):
    """Calculate percentage reduction in risk; return 0 for zero baseline."""
    if not isinstance(original_risk, (int, float)) or not isinstance(masked_risk, (int, float)):
        raise TypeError("Risk values must be numeric")
    if not math.isfinite(original_risk) or not math.isfinite(masked_risk):
        raise ValueError("Risk values must be finite")
    if original_risk == 0:
        return 0.0
    return round(((original_risk - masked_risk) / original_risk) * 100, 2)
