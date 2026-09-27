import streamlit as st
import pandas as pd

from modules.classification import classify_attributes
from modules.risk_analysis import calculate_risk
from modules.masking import (
    suppress_pin,
    generalize_age,
    swap_age,
    apply_all_masking
)
from modules.utility_analysis import calculate_information_loss


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Healthcare Data Privacy Analyzer",
    page_icon="🔐",
    layout="wide"
)


# =========================================================
# LOAD DATASET
# =========================================================

DATA_PATH = "data/healthcare_dataset.csv"

df = pd.read_csv(DATA_PATH)

original_df = df.copy()


# =========================================================
# HEADER
# =========================================================

st.title("Healthcare Data Privacy Analyzer")

st.subheader(
    "Privacy-Preserving Release of Healthcare Microdata"
)

st.write(
    "Analyze healthcare data for re-identification risk "
    "and apply privacy-preserving masking techniques."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Privacy Controls")

masking_option = st.sidebar.selectbox(
    "Select Masking Technique",
    [
        "None",
        "Suppression",
        "Generalization",
        "Data Swapping",
        "Apply All Non-Perturbative"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Suppression hides selected data, "
    "generalization replaces exact values with ranges, "
    "and data swapping exchanges values between records."
)


# =========================================================
# DATASET OVERVIEW
# =========================================================

st.header("1. Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Records",
        df.shape[0]
    )

with col2:
    st.metric(
        "Total Attributes",
        df.shape[1]
    )

with col3:
    st.metric(
        "Dataset Size",
        f"{df.shape[0]} × {df.shape[1]}"
    )

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# ATTRIBUTE CLASSIFICATION
# =========================================================

st.header("2. Attribute Classification")

classification_result = classify_attributes(df)

st.dataframe(
    classification_result,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# ORIGINAL RISK
# =========================================================

st.header("3. Re-identification Risk Analysis")

risk_result = calculate_risk(original_df)

display_risk = risk_result[
    [
        "Patient ID",
        "Age",
        "Gender",
        "PIN Code",
        "Department",
        "Group Size",
        "Re-identification Risk"
    ]
].copy()

display_risk["Re-identification Risk"] = (
    display_risk["Re-identification Risk"]
    .round(2)
    .astype(str)
    + "%"
)

st.dataframe(
    display_risk,
    use_container_width=True,
    hide_index=True
)

average_original_risk = risk_result[
    "Re-identification Risk"
].mean()

st.metric(
    "Average Original Risk",
    f"{average_original_risk:.2f}%"
)


# =========================================================
# APPLY SELECTED MASKING
# =========================================================

if masking_option == "Suppression":

    masked_df = suppress_pin(original_df)

    technique_description = (
        "PIN Code values are suppressed by hiding "
        "the last three digits."
    )

elif masking_option == "Generalization":

    masked_df = generalize_age(original_df)

    technique_description = (
        "Exact ages are converted into age ranges "
        "to reduce precision."
    )

elif masking_option == "Data Swapping":

    masked_df = swap_age(original_df)

    technique_description = (
        "Age values are exchanged between selected "
        "records while preserving the overall values."
    )

elif masking_option == "Apply All Non-Perturbative":

    masked_df = apply_all_masking(original_df)

    technique_description = (
        "Suppression and age generalization are applied "
        "together."
    )

else:

    masked_df = original_df.copy()

    technique_description = (
        "No masking technique has been selected."
    )


# =========================================================
# MASKING RESULT
# =========================================================

st.header("4. Privacy-Preserving Masking")

st.info(
    f"**Selected Technique:** {masking_option}\n\n"
    f"{technique_description}"
)

if masking_option != "None":

    st.subheader("Before Masking")

    st.dataframe(
        original_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("After Masking")

    st.dataframe(
        masked_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.dataframe(
        masked_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# CHANGED VALUES
# =========================================================

st.subheader("Masking Changes")

changes = []

for column in original_df.columns:

    changed = (
        original_df[column].astype(str)
        != masked_df[column].astype(str)
    ).sum()

    if changed > 0:

        changes.append(
            {
                "Attribute": column,
                "Changed Records": int(changed)
            }
        )

if changes:

    changes_df = pd.DataFrame(changes)

    st.dataframe(
        changes_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No values were changed.")


# =========================================================
# INFORMATION LOSS
# =========================================================

st.header("5. Information Loss Analysis")

information_loss = calculate_information_loss(
    original_df,
    masked_df
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Information Loss",
        f"{information_loss:.2f}%"
    )

with col2:

    changed_cells = int(
        (original_df.astype(str) != masked_df.astype(str))
        .sum()
        .sum()
    )

    total_cells = (
        original_df.shape[0]
        * original_df.shape[1]
    )

    st.metric(
        "Changed Cells",
        f"{changed_cells} / {total_cells}"
    )


# =========================================================
# PRIVACY ANALYSIS
# =========================================================

st.header("6. Privacy Analysis")

if masking_option == "None":

    st.info(
        "Select a masking technique to compare "
        "the protected dataset with the original dataset."
    )

else:

    masked_risk_result = calculate_risk(masked_df)

    average_masked_risk = masked_risk_result[
        "Re-identification Risk"
    ].mean()

    st.write(
        "The assignment risk formula uses the complete "
        "quasi-identifier combination. With this small "
        "5-record dataset, some masking techniques may "
        "change values without creating duplicate "
        "quasi-identifier combinations."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Original Average Risk",
            f"{average_original_risk:.2f}%"
        )

    with col2:

        st.metric(
            "Masked Average Risk",
            f"{average_masked_risk:.2f}%"
        )


# =========================================================
# ORIGINAL VS MASKED
# =========================================================

st.header("7. Original vs Masked Dataset")

comparison_rows = []

for column in original_df.columns:

    original_value = str(
        original_df[column].iloc[0]
    )

    masked_value = str(
        masked_df[column].iloc[0]
    )

    comparison_rows.append(
        {
            "Attribute": column,
            "Original": original_value,
            "Masked": masked_value,
            "Changed": (
                "Yes"
                if original_value != masked_value
                else "No"
            )
        }
    )

comparison_df = pd.DataFrame(
    comparison_rows
)

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DOWNLOAD
# =========================================================

# =========================================================
# DOWNLOAD PROTECTED DATASET
# =========================================================

st.header("8. Download Protected Dataset")

# Create a technique-specific filename
filename_map = {
    "None": "original_healthcare_dataset.csv",
    "Suppression": "suppressed_healthcare_dataset.csv",
    "Generalization": "generalized_healthcare_dataset.csv",
    "Data Swapping": "swapped_healthcare_dataset.csv",
    "Apply All Non-Perturbative": "masked_healthcare_dataset.csv"
}

download_filename = filename_map[masking_option]

# Convert the CURRENT masked dataset to CSV
csv_data = masked_df.to_csv(index=False).encode("utf-8")

st.write(
    f"Download the dataset after applying: **{masking_option}**"
)

st.download_button(
    label=f"Download {masking_option} Dataset",
    data=csv_data,
    file_name=download_filename,
    mime="text/csv",
    key=f"download_{masking_option}"
)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
### Healthcare Data Privacy Analyzer

**Privacy techniques implemented**

- Attribute Classification
- Re-identification Risk Analysis
- Suppression
- Generalization
- Data Swapping
- Information Loss Analysis
- Privacy Analysis
- Protected Dataset Export

**Technology:** Python · Pandas · Streamlit
"""
)