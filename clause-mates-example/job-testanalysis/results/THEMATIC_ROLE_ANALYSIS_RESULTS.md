# Pronoun Type vs Thematic Role Analysis - Results Summary

## Research Questions

**H1**: Do personal pronouns appear more often in clauses with clause mates having Patient/Recipient roles than Agent roles?

**H2**: Do demonstrative pronouns appear more often in clauses with clause mates having Agent roles than Patient/Recipient roles?

---

## Methodology

This analysis uses **cleaned annotation columns** where chain IDs and indices have been removed:
- `pronoun_coreference_type_clean` (instead of `pronoun_coreference_type`)
- `clause_mate_thematic_role_clean` (instead of `clause_mate_thematic_role`)

**Pronoun classification:**
- `PersPron` → Personal pronouns
- `D-Pron` or `demNP` → Demonstrative pronouns

**Thematic role classification:**
- `Proto-Ag` → Agent
- `Proto-Pat` or `Recipient` → Patient/Recipient
- `*` or `_` → Unspecified (excluded from analysis)

---

## Key Findings

### Dataset
- **Total analyzed**: 1,307 pronoun-clause mate relationships
- **Personal pronouns**: 997 (76.3%)
- **Demonstrative pronouns**: 310 (23.7%)
- **Excluded**: 597 rows with unspecified or other categories

### Contingency Table (Absolute Counts)

|                    | Agent | Patient/Recipient | Total |
|--------------------|-------|-------------------|-------|
| **Demonstrative**  | 199   | 111               | 310   |
| **Personal**       | 604   | 393               | 997   |
| **Total**          | 803   | 504               | 1,307 |

### Distribution Within Each Pronoun Type

|                    | Agent | Patient/Recipient |
|--------------------|-------|-------------------|
| **Demonstrative**  | 64.19% | 35.81%           |
| **Personal**       | 60.58% | 39.42%           |

---

## Statistical Tests

### Chi-Square Test of Independence
- **χ² statistic**: 1.1541
- **Degrees of freedom**: 1
- **P-value**: 0.283 (NOT significant at α = 0.05)
- **Cramér's V**: 0.030 (very small effect size)

### Fisher's Exact Test (2×2 table)
- **Odds ratio**: 1.17
- **P-value**: 0.257 (NOT significant at α = 0.05)

**Interpretation**: There is **no statistically significant association** between pronoun type and clause mate thematic role at the p < 0.05 level.

---

## Hypothesis Testing Results

### ❌ Hypothesis 1: NOT SUPPORTED
**Claim**: Personal pronouns appear more often with Patient/Recipient roles than Agent roles

**Actual Results**:
- Personal pronouns with **Patient/Recipient**: 39.42%
- Personal pronouns with **Agent**: 60.58%

**Finding**: Personal pronouns actually appear **MORE often with Agent roles** (opposite of hypothesis)

---

### ✅ Hypothesis 2: SUPPORTED (descriptively)
**Claim**: Demonstrative pronouns appear more often with Agent roles than Patient/Recipient roles

**Actual Results**:
- Demonstrative pronouns with **Agent**: 64.19%
- Demonstrative pronouns with **Patient/Recipient**: 35.81%

**Finding**: Demonstrative pronouns do appear more with Agent roles, showing a **28.4 percentage point difference**.

**However**: While the pattern exists descriptively, the difference is **not statistically significant** (p = 0.283). This could be due to:
1. Small effect size (the difference is modest)
2. Sample size considerations
3. Natural variation in the data

---

## Interpretation

### What the data shows:

1. **Both pronoun types favor Agent roles**: Both personal (60.6%) and demonstrative (64.2%) pronouns appear more frequently with clause mates in Agent roles.

2. **Demonstrative pronouns show slightly stronger Agent preference**: The difference is 3.6 percentage points (64.2% vs 60.6%), but this is not statistically significant.

3. **The patterns are similar**: The lack of statistical significance suggests that pronoun type and clause mate thematic role may be **relatively independent** in this dataset.

### Possible explanations:

- **Discourse frequency**: Agent roles may simply be more common in discourse, affecting both pronoun types similarly
- **German syntax**: German word order and case marking may influence these patterns differently than predicted
- **Data characteristics**: The corpus may have specific genre or register features affecting the distribution

---

## Visualizations Created

1. **pronoun_thematic_role_analysis.png**: 
   - Four-panel visualization showing distributions, counts, heatmaps, and residuals

2. **pronoun_thematic_role_percentages.png**: 
   - Bar chart showing the percentage distribution within each pronoun type

---

## Files Generated

- `analyze_pronoun_thematic_roles.py` - Analysis script
- `thematic_role_analysis_summary.csv` - Numerical summary
- `thematic_role_analysis_statistics.txt` - Statistical test results
- `pronoun_thematic_role_analysis.png` - Multi-panel visualization
- `pronoun_thematic_role_percentages.png` - Percentage comparison

---

## Conclusion

While **Hypothesis 2** is descriptively supported (demonstrative pronouns do appear more with Agent roles), the association is **not statistically significant**. **Hypothesis 1** is clearly **not supported** - personal pronouns actually show the opposite pattern, appearing more with Agent roles.

The overall finding suggests that **pronoun type choice may not be strongly influenced by clause mate thematic roles** in this German corpus, or that other factors (syntax, animacy, givenness, etc.) play more important roles in determining pronoun selection.
