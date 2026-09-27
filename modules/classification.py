import pandas as pd


def classify_attributes(df):
    """
    Classifies healthcare dataset attributes into:
    Direct Identifiers, Quasi-Identifiers, and Sensitive Attributes.
    """

    classification = {
        "Direct Identifier": ["Patient ID"],
        "Quasi-Identifier": ["Age", "Gender", "PIN Code", "Department"],
        "Sensitive Attribute": ["Disease", "Treatment"]
    }

    results = []

    for column in df.columns:
        attribute_type = "Unknown"

        for category, columns in classification.items():
            if column in columns:
                attribute_type = category
                break

        results.append({
            "Attribute": column,
            "Classification": attribute_type
        })

    return pd.DataFrame(results)