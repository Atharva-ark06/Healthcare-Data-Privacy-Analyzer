import pandas as pd


def _require_columns(df, columns):
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))


def suppress_pin(df):
    """Suppress the last three characters of each PIN code."""
    _require_columns(df, ["PIN Code"])
    masked = df.copy()
    masked["PIN Code"] = (
        masked["PIN Code"].astype("string").str.slice(0, 3) + "***"
    )
    return masked


def generalize_age(df):
    """Convert numeric ages into consistent decade-like age bands."""
    _require_columns(df, ["Age"])
    masked = df.copy()
    ages = pd.to_numeric(masked["Age"], errors="raise")
    bins = [0, 30, 40, 50, 60, 70, float("inf")]
    labels = ["0-29", "30-39", "40-49", "50-59", "60-69", "70+"]
    masked["Age"] = pd.cut(
        ages, bins=bins, labels=labels, right=False, include_lowest=True
    )
    return masked


def swap_age(df):
    """Swap age values in the first two and next two rows, when available."""
    _require_columns(df, ["Age"])
    masked = df.copy()
    if len(masked) >= 4:
        age_position = masked.columns.get_loc("Age")
        values = masked["Age"].to_numpy(copy=True)
        values[0], values[1] = values[1], values[0]
        values[2], values[3] = values[3], values[2]
        masked.iloc[:, age_position] = values
    return masked


def apply_all_masking(df):
    """Apply PIN suppression and age generalization."""
    return generalize_age(suppress_pin(df))
