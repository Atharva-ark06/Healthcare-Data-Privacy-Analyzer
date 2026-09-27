import pandas as pd


def suppress_pin(df):
    """
    Suppression:
    Hides the exact PIN code and keeps only
    the first three digits.
    """
    masked = df.copy()

    masked["PIN Code"] = (
        masked["PIN Code"]
        .astype(str)
        .str[:3] + "***"
    )

    return masked


def generalize_age(df):
    """
    Generalization:
    Converts exact ages into age groups.
    """
    masked = df.copy()

    bins = [0, 29, 39, 49, 59, 69, 100]
    labels = [
        "20-29",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
        "70+"
    ]

    masked["Age"] = pd.cut(
        masked["Age"],
        bins=bins,
        labels=labels,
        right=True
    )

    return masked


def swap_age(df):
    """
    Data Swapping:
    Swaps age values between selected records.
    """

    masked = df.copy()

    if len(masked) >= 4:
        masked.loc[0, "Age"], masked.loc[1, "Age"] = (
            masked.loc[1, "Age"],
            masked.loc[0, "Age"]
        )

        masked.loc[2, "Age"], masked.loc[3, "Age"] = (
            masked.loc[3, "Age"],
            masked.loc[2, "Age"]
        )

    return masked


def apply_all_masking(df):
    """
    Applies suppression and generalization.
    Data swapping is kept as a separate option
    because it is a perturbative technique.
    """

    masked = df.copy()

    # Non-perturbative masking
    masked = suppress_pin(masked)
    masked = generalize_age(masked)

    return masked