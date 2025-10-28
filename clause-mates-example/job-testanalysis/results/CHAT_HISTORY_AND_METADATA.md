# Chat History and Metadata - Clause Mates Analysis Project

## Session Information

**Date**: October 14, 2025  
**Project**: German Clause Mates Linguistic Analysis  
**Working Directory**: `c:\GitHub\pyws\clause-mates-example\`  
**Primary Dataset**: `unified_relationships.csv` (1,904 rows × 44 columns)  
**Shell Environment**: PowerShell (pwsh.exe)

---

## Project Context

### Research Domain
German linguistic research investigating clause mate relationships and pronoun usage patterns in annotated discourse data.

### Data Structure
- **Unit of analysis**: Pronoun-clause mate combinations
- **Annotation format**: WebAnno TSV 3.3 (German corpus)
- **Key features**: 
  - Critical pronouns (3rd person, D-pronouns, demonstratives)
  - Coreference chains with chain IDs and occurrence numbers
  - Grammatical roles (Subject, Object, Oblique)
  - Thematic roles (Proto-Agent, Proto-Patient, Recipient)
  - Animacy and givenness annotations

---

## Chat History Timeline

### Phase 1: Initial Data Cleaning Request

**User Request**: Clean three clause mate columns by removing numbers and brackets:
- `clause_mate_grammatical_role`
- `clause_mate_thematic_role`
- `clause_mate_coreference_type`

**Action Taken**:
1. Created `clean_clause_mate_columns.py` script
2. Implemented regex-based cleaning function: `r'\[\d+\]'`
3. Generated `unified_relationships_cleaned.csv` with 3 new cleaned columns
4. Created `CLEANING_REPORT.md` documentation

**Results**:
- Original: 1,904 rows × 44 columns
- Output: 1,904 rows × 47 columns (+3 cleaned columns)
- Preserved original columns alongside cleaned versions

**Examples of Cleaning**:
- `Oblique[5]` → `Oblique`
- `Proto-Ag[7]` → `Proto-Ag`
- `defNP[134]` → `defNP`
- `PersPron[78]` → `PersPron`

---

### Phase 2: Thematic Role Hypothesis Testing

**User Request**: Test two hypotheses about pronoun types and thematic roles:

**Hypothesis 1**: Personal pronouns appear more often in clauses with clause mates having Patient/Recipient roles than Agent roles

**Hypothesis 2**: Demonstrative pronouns appear more often in clauses with clause mates having Agent roles than Patient/Recipient roles

**Action Taken**:
1. Created `analyze_pronoun_thematic_roles.py` script
2. Implemented pronoun classification:
   - `PersPron[*]` → Personal
   - `D-Pron[*]` or `demNP[*]` → Demonstrative
3. Implemented thematic role categorization:
   - `Proto-Ag` → Agent
   - `Proto-Pat` or `Recipient` → Patient/Recipient
4. Performed statistical tests:
   - Chi-square test of independence
   - Fisher's exact test (2×2 table)
   - Effect size calculation (Cramér's V)
5. Generated visualizations (4-panel analysis + percentage comparison)
6. Created result summaries and documentation

**Statistical Results**:
- **Sample size**: 1,307 relationships (after filtering)
- **Chi-square**: χ² = 1.1541, p = 0.283 (not significant)
- **Fisher's exact**: OR = 1.17, p = 0.257 (not significant)
- **Effect size**: Cramér's V = 0.030 (very small)

**Contingency Table**:
```
                   Agent    Patient/Recipient    Total
Demonstrative      199 (64.19%)   111 (35.81%)    310
Personal          604 (60.58%)   393 (39.42%)    997
```

**Hypothesis Outcomes**:
- **H1**: ❌ NOT SUPPORTED - Personal pronouns actually prefer Agent roles (opposite of prediction)
- **H2**: ✅ DESCRIPTIVELY SUPPORTED - Demonstrative pronouns do prefer Agent roles, but not statistically significant

**Key Finding**: No statistically significant association between pronoun type and clause mate thematic role (p = 0.283)

**Files Generated**:
- `thematic_role_analysis_summary.csv`
- `thematic_role_analysis_statistics.txt`
- `pronoun_thematic_role_analysis.png` (4-panel visualization)
- `pronoun_thematic_role_percentages.png`
- `THEMATIC_ROLE_ANALYSIS_RESULTS.md`

---

### Phase 3: Script Enhancement - Pronoun Column Cleaning

**User Request**: Update cleaning script to also clean pronoun columns, creating cleaner categorical variables for analysis

**Action Taken**:
1. **Updated `clean_clause_mate_columns.py`**:
   - Added cleaning for `pronoun_coreference_type` → `pronoun_coreference_type_clean`
   - Added cleaning for `pronoun_grammatical_role` → `pronoun_grammatical_role_clean`
   - Added cleaning for `pronoun_thematic_role` → `pronoun_thematic_role_clean`
   - Updated output documentation sections
   - New output: 1,904 rows × 50 columns (+6 cleaned columns total)

2. **Updated `analyze_pronoun_thematic_roles.py`**:
   - Changed to use `pronoun_coreference_type_clean` instead of raw column
   - Now classifies from clean values: `PersPron`, `D-Pron` instead of `PersPron[78]`, etc.
   - Verified results remain identical (data integrity check)

3. **Updated Documentation**:
   - Enhanced `CLEANING_REPORT.md` with pronoun column sections
   - Added methodology section to `THEMATIC_ROLE_ANALYSIS_RESULTS.md`
   - Created `DATA_CLEANING_AND_ANALYSIS_SUMMARY.md` (comprehensive overview)
   - Created `UPDATE_SUMMARY.md` (change log)

**Pronoun Column Statistics** (after cleaning):
- `pronoun_coreference_type_clean`: `PersPron` (1,358), `D-Pron` (402)
- `pronoun_grammatical_role_clean`: `Subj` (1,447), `dirObj` (244), `indirObj` (134), `Oblique` (77)
- `pronoun_thematic_role_clean`: `Proto-Ag` (1,519), `Proto-Pat` (312), `*` (48), `Recipient` (23)

**Verification**: Re-ran analysis to confirm identical results with cleaned columns ✓

---

## Complete File Inventory

### Python Scripts
1. **`clean_clause_mate_columns.py`** (180+ lines)
   - Purpose: Clean annotation columns by removing indices and chain IDs
   - Input: `unified_relationships.csv`
   - Output: `unified_relationships_cleaned.csv`
   - Cleans: 6 columns (3 clause mate + 3 pronoun)

2. **`analyze_pronoun_thematic_roles.py`** (350+ lines)
   - Purpose: Statistical analysis of pronoun types vs thematic roles
   - Methods: Chi-square, Fisher's exact, Cramér's V
   - Visualizations: 2 multi-panel figures
   - Output: CSV, TXT, PNG files

### Data Files
1. **`unified_relationships.csv`** (original)
   - 1,904 rows × 44 columns
   - Contains raw annotations with chain IDs

2. **`unified_relationships_cleaned.csv`** (cleaned)
   - 1,904 rows × 50 columns
   - Contains 6 additional cleaned columns
   - Preserves all original columns

### Analysis Output Files
1. **`thematic_role_analysis_summary.csv`**
   - Numerical summary table
   - Pronoun types × thematic role counts and percentages

2. **`thematic_role_analysis_statistics.txt`**
   - Chi-square test results
   - Fisher's exact test results
   - Hypothesis testing outcomes

3. **`pronoun_thematic_role_analysis.png`**
   - 4-panel visualization (2×2 grid)
   - Stacked bars, grouped bars, heatmaps, residuals

4. **`pronoun_thematic_role_percentages.png`**
   - Percentage comparison bar chart
   - Shows distribution within each pronoun type

### Documentation Files
1. **`CLEANING_REPORT.md`**
   - Detailed data cleaning documentation
   - Examples and statistics for all 6 cleaned columns
   - Before/after comparisons

2. **`THEMATIC_ROLE_ANALYSIS_RESULTS.md`**
   - Complete analysis results summary
   - Methodology, findings, interpretation
   - Statistical test details and hypothesis outcomes

3. **`DATA_CLEANING_AND_ANALYSIS_SUMMARY.md`**
   - Comprehensive project overview
   - Phase 1 (cleaning) + Phase 2 (analysis)
   - Key insights and next steps

4. **`UPDATE_SUMMARY.md`**
   - Change log for Phase 3 updates
   - Script modifications documented
   - Verification notes

5. **`CHAT_HISTORY_AND_METADATA.md`** (this file)
   - Complete session documentation
   - Request-response timeline
   - Technical metadata

---

## Technical Metadata

### Software Stack
- **Language**: Python 3.x
- **Shell**: PowerShell (Windows)
- **Key Libraries**:
  - `pandas` - Data manipulation and analysis
  - `numpy` - Numerical operations
  - `scipy.stats` - Statistical tests (chi2_contingency, fisher_exact)
  - `matplotlib` - Base plotting library
  - `seaborn` - Statistical visualizations
  - `re` - Regular expressions for string cleaning

### Statistical Methods Used

1. **Chi-Square Test of Independence**
   - Tests association between two categorical variables
   - Null hypothesis: Variables are independent
   - Used for 2×2 contingency table (pronoun type × thematic role)

2. **Fisher's Exact Test**
   - Exact test for 2×2 tables (alternative to chi-square)
   - More accurate for small sample sizes
   - Calculates exact p-value and odds ratio

3. **Cramér's V**
   - Effect size measure for categorical associations
   - Range: 0 (no association) to 1 (perfect association)
   - Interpretation: < 0.1 (small), 0.1-0.3 (medium), > 0.3 (large)

4. **Standardized Residuals**
   - Cell-level deviations from expected frequencies
   - Values > |2| indicate significant deviation
   - Used in heatmap visualization

### Data Cleaning Pattern

**Regex Pattern**: `r'\[\d+\]'`
- Matches: `[` followed by one or more digits followed by `]`
- Examples: `[5]`, `[78]`, `[134]`
- Applied with: `re.sub(pattern, '', string)`
- Post-processing: `.strip('|').strip()` to clean pipes and spaces

**Function Signature**:
```python
def clean_annotation(value):
    """Remove numbers in brackets like [5] or [11] from annotation strings."""
    if pd.isna(value) or value == '_':
        return value
    cleaned = re.sub(r'\[\d+\]', '', str(value))
    cleaned = cleaned.strip('|').strip()
    return cleaned
```

---

## Key Research Insights

### Pronoun Distribution in German Corpus
- **Personal pronouns dominate**: 71.3% of all pronouns (1,358/1,904)
- **Demonstrative pronouns**: 21.1% (402/1,904)
- **Subject position most common**: 76.0% of pronouns (1,447/1,904)
- **Proto-Agent role predominates**: 79.8% of pronouns (1,519/1,904)

### Clause Mate Characteristics
- **Subject clause mates**: 44.7% (852/1,904)
- **Agent role clause mates**: 46.0% (876/1,904)
- **Most common referent types**: 
  - Definite NPs: 24.0% (458/1,904)
  - Personal pronouns: 23.9% (456/1,904)
  - Proper names (EN): 12.5% (238/1,904)

### Statistical Relationship Finding
**Main conclusion**: Pronoun type (Personal vs Demonstrative) and clause mate thematic role (Agent vs Patient/Recipient) show **no statistically significant association** in this German discourse corpus.

**Implications**:
- Both pronoun types show similar distributional patterns
- Thematic role of clause mates may not be primary driver of pronoun choice
- Other factors likely more influential: syntax, animacy, givenness, discourse structure
- Genre/register effects may play a role

---

## Future Research Directions

Based on user's original task list, remaining analyses to implement:

1. **Grammatical Role Analysis**
   - Test: Personal pronouns with Object clause mates vs Demonstrative pronouns with Subject clause mates
   - Variables: `pronoun_coreference_type_clean` × `clause_mate_grammatical_role_clean`

2. **Clause Mate Count Effects**
   - Test: Effect of `num_clause_mates` on pronoun choice
   - Analysis: ANOVA or regression predicting pronoun type from count
   - Could also test effects on grammatical/thematic roles

3. **Linear Distance Analysis**
   - Test: Antecedent distance differences when clause mates present vs absent
   - Variables: 
     - `pronoun_most_recent_antecedent_distance`
     - `pronoun_first_antecedent_distance`
   - Group by: `num_clause_mates` (0 vs >0)
   - Method: t-test or Mann-Whitney U test

4. **Multivariate Analysis**
   - Multiple factors simultaneously: thematic role, grammatical role, animacy, givenness
   - Method: Logistic regression predicting pronoun type
   - Interaction effects between clause mate features

---

## Reproducibility Information

### To Reproduce Analysis

1. **Clean the data**:
   ```powershell
   cd c:\GitHub\pyws\clause-mates-example
   python clean_clause_mate_columns.py
   ```
   - Generates: `unified_relationships_cleaned.csv` (50 columns)

2. **Run thematic role analysis**:
   ```powershell
   python analyze_pronoun_thematic_roles.py
   ```
   - Generates: CSV, TXT, and PNG output files

### Expected Output
- Console output with contingency tables and statistics
- 4 output files created in working directory
- Execution time: ~5-10 seconds per script

### Dependencies Check
If missing libraries, install with:
```powershell
pip install pandas numpy scipy matplotlib seaborn
```

---

## Session Workflow Summary

```
1. User Request: Clean 3 clause mate columns
   ↓
2. Created cleaning script → 47 columns output
   ↓
3. User Request: Test pronoun type vs thematic role hypotheses
   ↓
4. Created analysis script → Statistical results + visualizations
   ↓
5. User Request: Also clean pronoun columns + update docs
   ↓
6. Updated both scripts → 50 columns output
   ↓
7. Updated all documentation files
   ↓
8. User Request: Document chat history
   ↓
9. Created this comprehensive metadata file
```

---

## Quality Assurance Notes

### Verification Steps Taken
- ✅ Re-ran cleaning script after pronoun column updates
- ✅ Re-ran analysis script with cleaned pronoun columns
- ✅ Confirmed identical statistical results (p-values, chi-square, etc.)
- ✅ Verified column counts: 44 → 47 → 50
- ✅ Checked all files generated successfully
- ✅ Validated documentation accuracy

### Code Quality
- ✅ Scripts are self-contained (no external dependencies beyond libraries)
- ✅ Clear function documentation with docstrings
- ✅ Comprehensive print statements for transparency
- ✅ Error handling for missing values (pd.isna checks)
- ✅ Type checking through pandas operations

### Documentation Quality
- ✅ Multiple documentation files for different purposes
- ✅ Examples provided for all cleaned columns
- ✅ Statistical interpretation included
- ✅ Methodology clearly explained
- ✅ File inventory complete

---

## Contact and Project Information

**Repository**: clausemate (GitHub: jobschepens)  
**Branch**: main  
**Working Directories**: 
- Main: `c:\GitHub\clausemate\`
- Analysis: `c:\GitHub\pyws\clause-mates-example\`

**Related Projects**:
- `clausemate-private-data/` - TSV source files
- `robert/` - Related research analysis tools

---

## Appendix: Complete Column List

### Original Dataset (44 columns)
1. chapter_file
2. chapter_number
3. chapter_id
4. global_sentence_id
5. cross_chapter
6. source_file_path
7. sentence_id
8. sentence_id_numeric
9. sentence_id_prefixed
10. sentence_num
11. first_words
12. pronoun_text
13. pronoun_token_idx
14. pronoun_grammatical_role
15. pronoun_thematic_role
16. pronoun_givenness
17. pronoun_coref_ids
18. pronoun_coref_base_num
19. pronoun_coref_occurrence_num
20. pronoun_coreference_link
21. pronoun_coref_link_base_num
22. pronoun_coref_link_occurrence_num
23. pronoun_coreference_type
24. pronoun_inanimate_coreference_link
25. pronoun_inanimate_coref_link_base_num
26. pronoun_inanimate_coref_link_occurrence_num
27. pronoun_inanimate_coreference_type
28. pronoun_most_recent_antecedent_text
29. pronoun_most_recent_antecedent_distance
30. pronoun_first_antecedent_text
31. pronoun_first_antecedent_distance
32. pronoun_antecedent_choice
33. num_clause_mates
34. clause_mate_text
35. clause_mate_coref_id
36. clause_mate_coref_base_num
37. clause_mate_coref_occurrence_num
38. clause_mate_start_idx
39. clause_mate_end_idx
40. clause_mate_grammatical_role
41. clause_mate_thematic_role
42. clause_mate_coreference_type
43. clause_mate_animacy
44. clause_mate_givenness

### Cleaned Dataset (50 columns = 44 + 6 new)
45. **clause_mate_grammatical_role_clean** ⭐ NEW
46. **clause_mate_thematic_role_clean** ⭐ NEW
47. **clause_mate_coreference_type_clean** ⭐ NEW
48. **pronoun_coreference_type_clean** ⭐ NEW
49. **pronoun_grammatical_role_clean** ⭐ NEW
50. **pronoun_thematic_role_clean** ⭐ NEW

---

*Document created: October 14, 2025*  
*Last updated: October 14, 2025*  
*Session: Complete*
