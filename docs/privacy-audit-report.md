# Privacy Audit Report Export

## What it adds

The dashboard can export a self-contained HTML audit report after applying the selected masking technique. Open the downloaded HTML in a browser. To create a PDF copy, use the browser's **Print → Save as PDF** action.

The report includes:
- selected masking technique and dataset dimensions;
- information-loss estimate and original/masked uniqueness-risk proxy;
- pass/fail results for k-anonymity, distinct-value l-diversity, and t-closeness;
- aggregate counts of groups failing each check;
- contextual follow-up recommendations and an explicit limitations notice.

## Privacy-conscious output

The report deliberately excludes patient-level records and exact quasi-identifier values. It contains aggregate metrics only. The source dataset and exported protected dataset are not embedded in the report.

## Interpretation and limitations

- A lower uniqueness-risk proxy is not a formal guarantee against re-identification.
- k-anonymity, l-diversity, and t-closeness depend on the selected quasi-identifiers, sensitive attribute, thresholds, and implementation assumptions.
- The current t-closeness diagnostic uses total-variation distance between group and overall sensitive-value distributions.
- Passing all checks does not establish that a release is anonymous, legally compliant, or safe in every context.
- Recommendations are decision-support hints, not automatic transformations. Review data utility, consent, access controls, threat models, and applicable requirements before release.

## Local validation

From the repository root:

```powershell
python -m unittest discover -s tests
streamlit run app.py
```

The test suite checks summary validation, failed-group counts, HTML escaping, and the presence of limitations language. Run the commands locally before merging; this branch was authored through GitHub and the full app/test suite has not been executed in a local Python environment here.
