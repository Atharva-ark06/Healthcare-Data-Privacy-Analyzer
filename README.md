# Healthcare Data Privacy Analyzer

**Privacy-preserving release of healthcare microdata**

A Python and Streamlit project for exploring re-identification risk, applying masking techniques, and comparing privacy-related diagnostics with data utility. Built as an educational demonstration using a small fictional healthcare dataset.

![Dashboard screenshot](https://res.cloudinary.com/wpop4xyo/image/upload/v1790508462/Screenshot_2026-09-27_165228.png)

## Contents

- [Features](#features)
- [Dashboard screenshots](#dashboard-screenshots)
- [How it works](#how-it-works)
- [Privacy techniques](#privacy-techniques)
- [Privacy model checks](#privacy-model-checks)
- [Dataset and assumptions](#dataset-and-assumptions)
- [Technology stack](#technology-stack)
- [Installation](#installation)
- [Run tests](#run-tests)
- [Project structure](#project-structure)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Author](#author)

## Features

- **Dataset overview:** inspect record and attribute counts.
- **Attribute classification:** distinguish direct identifiers, quasi-identifiers, and sensitive attributes.
- **Re-identification risk proxy:** estimate uniqueness-based risk using quasi-identifier combinations.
- **Masking:** try suppression, age generalization, data swapping, or combined non-perturbative masking.
- **Utility analysis:** estimate information loss and compare original and masked values.
- **Formal model diagnostics:** evaluate k-anonymity, distinct-value l-diversity, and t-closeness thresholds.
- **Export:** download the selected masked dataset as CSV.
- **Interactive dashboard:** explore results in a Streamlit interface.

## Dashboard screenshots

### Masking comparison

![Before and after masking](https://res.cloudinary.com/wpop4xyo/image/upload/v1790508485/Screenshot_2026-09-27_165251.png)

### Protected dataset export

![Protected dataset download](https://res.cloudinary.com/wpop4xyo/image/upload/v1790508536/Screenshot_2026-09-27_165844.png)

### System flow and architecture

![System flow and architecture](https://res.cloudinary.com/wpop4xyo/image/upload/v1790508983/systemflow_and_architecture.png)

## How it works

1. Load the healthcare CSV dataset.
2. Classify attributes and calculate a uniqueness-based risk proxy.
3. Select and apply a masking technique.
4. Compare the original and transformed datasets.
5. Calculate an information-loss estimate and evaluate privacy model thresholds.
6. Download the transformed CSV or aggregate audit report.

## Privacy techniques

| Technique | Description |
|---|---|
| **Suppression** | Masks selected PIN-code digits. |
| **Generalization** | Converts exact ages into broader age ranges. |
| **Data swapping** | Exchanges selected age values between records. |
| **Apply all non-perturbative** | Combines suppression and age generalization. |

The selected technique determines the output dataset available for download. Always inspect the resulting data before using it in any downstream workflow.

## Privacy model checks

The dashboard includes configurable diagnostic checks for:

- **k-anonymity:** each quasi-identifier group must contain at least *k* records.
- **l-diversity:** each group must contain at least *l* distinct sensitive-attribute values.
- **t-closeness:** each group's sensitive-value distribution is compared with the overall distribution using total-variation distance.

The default quasi-identifiers are Age, Gender, PIN Code, and Department. Disease or Treatment can be selected as the sensitive attribute, depending on the columns available.

These checks are educational diagnostics, not formal proof of anonymity or a guarantee against re-identification. Results depend on the selected attributes, thresholds, data, and threat model.

## Dataset and assumptions

The included sample is a small fictional dataset with the following attributes:

| Category | Attributes |
|---|---|
| Direct identifier | Patient ID |
| Quasi-identifiers | Age, Gender, PIN Code, Department |
| Sensitive attributes | Disease, Treatment |

No real patient information should be added to a public repository. Before using any real or sensitive data, review authorization, consent, access controls, and applicable institutional requirements.

## Interpreting the metrics

Treat the dashboard outputs as screening signals rather than release approval:

- A group size below the selected *k* threshold indicates a k-anonymity failure for that group.
- A group with fewer than *l* distinct sensitive values fails the configured distinct-value l-diversity check.
- A total-variation distance above *t* fails the configured t-closeness check.
- A lower uniqueness-risk proxy after masking does not establish that re-identification is impossible.
- A low information-loss estimate does not prove that the data retains every property needed for a particular research question.

The dashboard's configured thresholds should be justified for the intended use case. Avoid publishing data solely because the displayed checks pass.

## Risk and information-loss calculations

The risk module uses a simplified uniqueness-based proxy:

`risk (%) = 100 / size of the matching quasi-identifier group`

The information-loss estimate compares original and masked cells:

`information loss (%) = changed cells / total cells × 100`

These metrics are intended for learning and comparison. They are not interchangeable with a formal privacy guarantee or a complete measure of analytical utility.

## Technology stack

| Technology | Role |
|---|---|
| Python | Application logic |
| Pandas | Data manipulation and analysis |
| Streamlit | Interactive dashboard |
| CSV | Sample dataset and export format |
| unittest | Automated unit tests |
| Git and GitHub | Version control and collaboration |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Atharva-ark06/Healthcare-Data-Privacy-Analyzer.git
cd Healthcare-Data-Privacy-Analyzer
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
streamlit run app.py
```

Streamlit prints a local URL in the terminal; open it in your browser.

## Run tests

Run the unit tests from the repository root:

```bash
python -m unittest discover -s tests
```

The test suite should be run locally before submitting or merging changes. This README does not imply that tests have passed in every environment.

## Architecture and module responsibilities

The project separates the dashboard from the analysis logic:

| Component | Responsibility |
|---|---|
| `app.py` | Streamlit layout, user controls, analysis presentation, and downloads |
| `modules/classification.py` | Attribute category classification |
| `modules/risk_analysis.py` | Group sizes and uniqueness-based risk estimates |
| `modules/masking.py` | Suppression, generalization, swapping, and combined masking |
| `modules/utility_analysis.py` | Information-loss calculation |
| `modules/privacy_models.py` | k-anonymity, l-diversity, and t-closeness diagnostics |
| `tests/` | Regression and input-validation tests |
| `docs/` | Notes about privacy model checks and audit reports |

The separation makes it easier to test analytical functions independently from the Streamlit interface.

## Project structure

```text
Healthcare-Data-Privacy-Analyzer/
├── app.py
├── requirements.txt
├── data/
│   └── healthcare_dataset.csv
├── modules/
│   ├── classification.py
│   ├── risk_analysis.py
│   ├── masking.py
│   ├── utility_analysis.py
│   └── privacy_models.py
├── tests/
│   ├── test_privacy_modules.py
│   ├── test_privacy_models.py
└── docs/
    ├── privacy-model-checks.md
    └── privacy-audit-report.md
```

## Responsible data handling

This project is a learning tool, not a certified de-identification system.

- Use only synthetic or appropriately authorized data during development.
- Keep source datasets out of commits unless the repository is explicitly approved to store them.
- Do not include patient identifiers or sensitive rows in issue reports, screenshots, or pull-request examples.
- Review exported CSV and HTML files before sharing them; an aggregate report can still reveal information if custom fields or future changes add row-level details.
- Consider the possibility of linkage with external datasets, small-group disclosure, and sensitive-attribute inference.
- Document assumptions and test with edge cases such as missing values, empty inputs, and unusual group sizes.

## Limitations

- The included dataset is small and fictional; results may not generalize to real datasets.
- Uniqueness-based risk is a simplified proxy and does not model every attacker or external data source.
- Masking can reduce data utility, and changing values does not automatically make a dataset safe to publish.
- k-anonymity, l-diversity, and t-closeness do not by themselves certify legal or regulatory compliance.
- The tool does not replace a privacy impact assessment, security review, or domain-expert judgment.

### Pull request checklist

Before requesting review, confirm as many of the following as apply:

- [ ] The change has a focused scope and a descriptive commit message.
- [ ] Input validation and error behavior are covered.
- [ ] Tests cover typical inputs and relevant edge cases.
- [ ] The dashboard starts with `streamlit run app.py`.
- [ ] The unit-test command has been run and its result is reported accurately.
- [ ] Documentation reflects the actual behavior.
- [ ] No real healthcare data, secrets, or local environment files are included.
- [ ] Privacy claims are qualified and do not imply a guarantee that the implementation cannot provide.

## Contributing

Contributions that improve correctness, explainability, accessibility, documentation, and test coverage are welcome.

1. Fork the repository and create a focused feature branch.
2. Make a small, clearly scoped change.
3. Add or update tests for changed behavior.
4. Run `python -m unittest discover -s tests` and try the Streamlit dashboard.
5. Open a pull request describing the change, validation performed, and known limitations.

Please do not commit real patient data, credentials, access tokens, or other sensitive information.

## Author

**Atharva Kulkarni**  
B.Tech, Computer Science & Engineering

- GitHub: [Atharva-ark06](https://github.com/Atharva-ark06)
- Repository: [Healthcare Data Privacy Analyzer](https://github.com/Atharva-ark06/Healthcare-Data-Privacy-Analyzer)

## License

This project is developed for academic and educational purposes. Check the repository for an explicit license before reusing or redistributing the code.
