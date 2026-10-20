import pandas as pd


QUASI_IDENTIFIERS = ["Age", "Gender", "PIN Code", "Department"]


def calculate_risk(df):
    """Return a per-record uniqueness-based risk proxy.

    Risk is estimated as 100 / the number of records sharing the same
    quasi-identifier combination. This is a simple educational proxy, not a
    formal privacy guarantee. Direct identifiers are not used in the score.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    missing = [column for column in QUASI_IDENTIFIERS if column not in df.columns]
    if missing:
        raise ValueError(
            "Missing required quasi-identifier column(s): " + ", ".join(missing)
        )

    result = df.copy()
    if result.empty:
        result["Group Size"] = pd.Series(dtype="int64")
        result["Re-identification Risk"] = pd.Series(dtype="float64")
        return result

    group_sizes = (
        result.groupby(QUASI_IDENTIFIERS, dropna=False, observed=True)
        .size()
        .reset_index(name="Group Size")
    )

    # A temporary row key preserves row order and handles duplicate indexes.
    result = result.reset_index(drop=True)
    result["_risk_row_order"] = range(len(result))
    result = result.merge(group_sizes, on=QUASI_IDENTIFIERS, how="left", sort=False)
    result = result.sort_values("_risk_row_order").drop(columns="_risk_row_order")
    result["Re-identification Risk"] = 100.0 / result["Group Size"]
    return result
