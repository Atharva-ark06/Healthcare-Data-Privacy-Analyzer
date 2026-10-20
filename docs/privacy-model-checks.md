# Formal Privacy Model Checks

The dashboard includes educational checks for three common privacy models.

## K-anonymity

For each group sharing the selected quasi-identifiers, count the records in that group. A group passes a threshold (k) when its size is at least (k). The dataset passes only when every group passes.

## L-diversity

For each quasi-identifier group, count distinct values of the selected sensitive attribute. This implementation uses distinct-value l-diversity; it does not implement entropy or recursive variants. A group passes when its distinct count is at least (l).

## T-closeness

For each group, compare its sensitive-attribute distribution with the distribution in the entire dataset. The implementation reports total-variation distance:

`distance = 0.5 * sum(abs(group_probability - global_probability))`

The group passes when its distance is less than or equal to the selected (t) threshold. The distance is between 0 and 1.

## Interpretation and limitations

- Quasi-identifiers default to Age, Gender, PIN Code, and Department.
- The user selects Disease or Treatment as the sensitive attribute.
- Missing sensitive values are counted as a distinct category; missing quasi-identifier values are grouped together.
- These checks use exact combinations of the current quasi-identifiers. Different generalization or threat models may produce different results.
- K-anonymity can remain vulnerable to homogeneity and background-knowledge attacks; l-diversity and t-closeness have their own limitations.
- Passing these checks does not prove that data is anonymous or safe to publish. Review data minimization, consent, legal obligations, and the intended release context before sharing any real health data.
