# Healthcare Data Privacy Analyzer 

### Privacy-Preserving Release of Healthcare Microdata

A Python-based privacy analysis tool designed to identify **re-identification risks** in healthcare datasets and apply privacy-preserving masking techniques while maintaining useful data for analysis.


---

## Dashboard

![Healthcare Data Privacy Analyzer Dashboard](https://res.cloudinary.com/wpop4xyo/image/upload/v1790508462/Screenshot_2026-09-27_165228.png)

The dashboard provides:

- Dataset overview
- Attribute classification
- Re-identification risk analysis
- Privacy-preserving masking
- Information loss analysis
- Privacy improvement
- Before/after dataset comparison
- Protected dataset download
- Light & Dark Theme 
---

## Key Features

- **Attribute Classification**
  - Direct Identifiers
  - Quasi-Identifiers
  - Sensitive Attributes

- **Re-identification Risk Analysis**
  - Calculates risk using quasi-identifier combinations
  - Determines group sizes
  - Displays average re-identification risk

- **Privacy-Preserving Masking**
  - Suppression
  - Generalization
  - Data Swapping
  - Combined Non-Perturbative Masking

- **Privacy & Utility Analysis**
  - Information loss calculation
  - Privacy improvement analysis
  - Original vs masked dataset comparison

- **Dataset Export**
  - Download the protected dataset based on the selected technique

---

## Privacy-Preserving Techniques

| Technique | Description |
|---|---|
| **Suppression** | Hides sensitive parts of selected data |
| **Generalization** | Replaces exact values with broader ranges |
| **Data Swapping** | Exchanges selected attribute values between records |
| **Apply All Non-Perturbative** | Combines suppression and generalization |

---

## Masking Demonstration

### Suppression

The system allows users to compare the dataset **before and after masking**.

![Before and After Masking](https://res.cloudinary.com/wpop4xyo/image/upload/v1790508485/Screenshot_2026-09-27_165251.png)

In the suppression example, the exact PIN codes are masked while preserving the remaining dataset information.

---

## Download Protected Dataset

The application allows users to download the dataset after applying the selected privacy technique.

![Download Protected Dataset](https://res.cloudinary.com/wpop4xyo/image/upload/v1790508536/Screenshot_2026-09-27_165844.png)

Each selected technique generates its corresponding protected CSV dataset.

---

## System Flow & Architecture

![System Flow and Architecture](https://res.cloudinary.com/wpop4xyo/image/upload/v1790508983/systemflow_and_architecture.png)

### System Flow

    Dataset Input
         ↓
    Attribute Classification
         ↓
    Re-identification Risk Analysis
         ↓
    Privacy-Preserving Masking
         ↓
    Utility & Privacy Analysis
         ↓
    Protected Dataset Export

---

## System Architecture

         ┌──────────────────────┐
         │     CSV Dataset      │
         │ healthcare_dataset   │
         └──────────┬───────────┘
                    │
                    ↓      
    ┌─────────────────────────────────────────┐
    │          Python Processing Layer        │
    │                                         │
    │    classification.py                    │
    │    risk_analysis.py                     │
    │    masking.py                           │
    │    utility_analysis.py                  │
    └──────────────────┬──────────────────────┘
                       ↓
    ┌─────────────────────────────────────────┐
    │          Streamlit Application          │
    │                  app.py                 │
    └──────────────────┬──────────────────────┘
                       ↕
    ┌─────────────────────────────────────────┐
    │             Web Dashboard               │
    │    Analysis • Masking • Comparison      │
    │    Information Loss • Download          │
    └─────────────────────────────────────────┘

---

## Project Structure

    Healthcare-Data-Privacy-Analyzer/
    │
    ├── app.py
    ├── requirements.txt
    │
    ├── data/
    │   └── healthcare_dataset.csv
    │
    └── modules/
        ├── __init__.py
        ├── classification.py
        ├── risk_analysis.py
        ├── masking.py
        └── utility_analysis.py

---

## Dataset

The project uses a small fictional healthcare dataset containing:

- Patient ID
- Age
- Gender
- PIN Code
- Department
- Disease
- Treatment

### Attribute Classification

| Category | Attributes |
|---|---|
| **Direct Identifier** | Patient ID |
| **Quasi-Identifier** | Age, Gender, PIN Code, Department |
| **Sensitive Attribute** | Disease, Treatment |

No real patient information is used.

---

## Re-identification Risk

The project calculates risk using:

    Risk = 1 / Number of records
           sharing the same
           quasi-identifier combination

The system calculates individual record risk as well as the average dataset risk before and after masking.

---

## Information Loss

Information loss is calculated by comparing the original dataset with the masked dataset and determining the percentage of changed cells.

    Information Loss =
    Changed Cells / Total Cells × 100

This demonstrates the trade-off between **privacy protection and data utility**.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming |
| **Pandas** | Data processing and analysis |
| **Streamlit** | Interactive web dashboard |
| **CSV** | Dataset storage |
| **Matplotlib** | Data visualization |
| **Git & GitHub** | Version control |

---

## Installation & Setup

### 1. Clone the Repository

    git clone https://github.com/Atharva-ark06/Healthcare-Data-Privacy-Analyzer.git
   ```
    cd Healthcare-Data-Privacy-Analyzer
```
### 2. Create Virtual Environment

    python -m venv venv

### 3. Activate Environment

Windows PowerShell:

    .\venv\Scripts\Activate.ps1

### 4. Install Dependencies

    pip install -r requirements.txt

### 5. Run the Application

    streamlit run app.py

The application will open in your browser.

---

## Workflow

    Healthcare Dataset
            ↓
    Attribute Classification
            ↓
    Risk Calculation
            ↓
    Select Masking Technique
            ↓
    Apply Privacy Protection
            ↓
    Calculate Information Loss
            ↓
    Compare Privacy & Utility
            ↓
    Download Protected Dataset

---

## Project Objectives

1. **To design** a system for identifying re-identification risks in healthcare microdata.

2. **To develop** privacy-preserving masking techniques including suppression, generalization, and data swapping.

3. **To implement** privacy and utility analysis through information-loss and risk evaluation.

---

## Applications

- Healthcare analytics
- Academic research
- Data publishing
- Privacy-preserving data sharing
- Educational demonstrations
- Microdata risk assessment

---

## Limitations & Future Scope

- Larger real-world style datasets
- **k-anonymity** validation
- **l-diversity**
- **t-closeness**
- Advanced privacy metrics
- Automated privacy-utility optimization
- Additional perturbation techniques
- Database integration
- Role-based access control

---

## Author

**Atharva Kulkarni**

B.Tech Computer Science & Engineering  
G M University, Davangere

**GitHub:**  
https://github.com/Atharva-ark06

---

## License

This project is developed for academic and educational purposes.
```
