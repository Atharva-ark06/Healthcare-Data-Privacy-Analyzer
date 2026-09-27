import pandas as pd


def calculate_risk(df):
    """
    Calculates re-identification risk using:
    
    Risk = 1 / Number of records having
           the same quasi-identifier combination
    """

    quasi_identifiers = [
        "Age",
        "Gender",
        "PIN Code",
        "Department"
    ]

    # Count identical quasi-identifier combinations
    group_sizes = (
        df.groupby(quasi_identifiers, dropna=False)
        .size()
        .reset_index(name="Group Size")
    )

    # Add group size to each record
    result = df.merge(
        group_sizes,
        on=quasi_identifiers,
        how="left"
    )

    # Calculate risk
    result["Re-identification Risk"] = (
        1 / result["Group Size"]
    ) * 100

    return result