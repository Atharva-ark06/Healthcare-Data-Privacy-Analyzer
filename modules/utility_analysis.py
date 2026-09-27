def calculate_information_loss(original_df, masked_df):
    """
    Calculates the percentage of cells that changed
    between the original and masked datasets.
    """

    total_cells = original_df.shape[0] * original_df.shape[1]

    changed_cells = 0

    for column in original_df.columns:
        if column in masked_df.columns:
            for original, masked in zip(
                original_df[column],
                masked_df[column]
            ):
                if str(original) != str(masked):
                    changed_cells += 1

    information_loss = (
        changed_cells / total_cells
    ) * 100

    return round(information_loss, 2)


def privacy_improvement(original_risk, masked_risk):
    """
    Calculates the percentage reduction in
    average re-identification risk.
    """

    if original_risk == 0:
        return 0

    improvement = (
        (original_risk - masked_risk)
        / original_risk
    ) * 100

    return round(improvement, 2)