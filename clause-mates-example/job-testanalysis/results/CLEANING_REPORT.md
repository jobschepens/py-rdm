# Data Column Cleaning - Summary Report

## Task Completed
Successfully removed numbers and brackets from clause mate and pronoun annotation columns, creating new cleaned variables.

## Files Created
- **Script**: `clean_clause_mate_columns.py`
- **Output**: `unified_relationships_cleaned.csv`

## Original vs Cleaned Columns

### Clause Mate Columns

#### 1. `clause_mate_grammatical_role` → `clause_mate_grammatical_role_clean`
Removed index numbers like `[5]`, `[6]`, `[7]` from grammatical role annotations.

**Examples of cleaning:**
- `Oblique[5]` → `Oblique`
- `Subj[7]` → `Subj`
- `dirObj[11]` → `dirObj`
- `indirObj` → `indirObj` (no change needed)

**Most common cleaned values:**
- `Subj`: 852 instances (Subject)
- `Oblique`: 474 instances
- `dirObj`: 409 instances (Direct Object)
- `indirObj`: 92 instances (Indirect Object)

---

### 2. `clause_mate_thematic_role` → `clause_mate_thematic_role_clean`
Removed index numbers from thematic role annotations.

**Examples of cleaning:**
- `Proto-Ag[7]` → `Proto-Ag` (Proto-Agent)
- `Proto-Pat[11]` → `Proto-Pat` (Proto-Patient)
- `*[5]` → `*` (unspecified/other)
- `Proto-Pat` → `Proto-Pat` (no change needed)

**Most common cleaned values:**
- `Proto-Ag`: 876 instances (Proto-Agent)
- `Proto-Pat`: 497 instances (Proto-Patient)
- `*`: 438 instances (unspecified)
- `Recipient`: 16 instances

---

### 3. `clause_mate_coreference_type` → `clause_mate_coreference_type_clean`
Removed coreference chain IDs like `[78]`, `[134]`, etc.

**Examples of cleaning:**
- `defNP[134]` → `defNP` (definite NP)
- `PersPron[78]` → `PersPron` (personal pronoun)
- `D-Pron[78]` → `D-Pron` (demonstrative pronoun)
- `EN[21]` → `EN` (proper name/Eigenname)
- `indefNP[74]` → `indefNP` (indefinite NP)

**Most common cleaned values:**
- `defNP`: 458 instances (definite noun phrase)
- `PersPron`: 456 instances (personal pronoun)
- `EN`: 238 instances (proper name)
- `PossPron`: 182 instances (possessive pronoun)
- `indefNP`: 126 instances (indefinite noun phrase)
- `D-Pron`: 110 instances (demonstrative pronoun)
- `zero`: 79 instances (zero pronoun)
- `IndefPron`: 68 instances (indefinite pronoun)
- `Quant`: 62 instances (quantifier)
- `RelPron`: 43 instances (relative pronoun)

---

### Pronoun Columns

#### 4. `pronoun_coreference_type` → `pronoun_coreference_type_clean`
Removed coreference chain IDs from pronoun type annotations.

**Examples of cleaning:**
- `PersPron[78]` → `PersPron` (personal pronoun)
- `PersPron[95]` → `PersPron`
- `D-Pron[78]` → `D-Pron` (demonstrative pronoun)
- `D-Pron[116]` → `D-Pron`

**Cleaned values:**
- `PersPron`: 1,358 instances (71.3%)
- `D-Pron`: 402 instances (21.1%)
- Other/missing: 144 instances (7.6%)

---

#### 5. `pronoun_grammatical_role` → `pronoun_grammatical_role_clean`
Removed index numbers from pronoun grammatical role annotations.

**Examples of cleaning:**
- `Subj` → `Subj` (most have no indices)
- `Subj[14]` → `Subj` (rare cases)
- Similar pattern for other roles

**Most common cleaned values:**
- `Subj`: 1,447 instances (76.0%) - Subject
- `dirObj`: 244 instances (12.8%) - Direct Object
- `indirObj`: 134 instances (7.0%) - Indirect Object
- `Oblique`: 77 instances (4.0%)

---

#### 6. `pronoun_thematic_role` → `pronoun_thematic_role_clean`
Removed index numbers from pronoun thematic role annotations.

**Examples of cleaning:**
- `Proto-Ag` → `Proto-Ag` (most have no indices)
- `Proto-Pat` → `Proto-Pat`

**Most common cleaned values:**
- `Proto-Ag`: 1,519 instances (79.8%) - Proto-Agent
- `Proto-Pat`: 312 instances (16.4%) - Proto-Patient
- `*`: 48 instances (2.5%) - Unspecified
- `Recipient`: 23 instances (1.2%)

---

## Data Summary
- **Original shape**: 1,904 rows × 44 columns
- **New shape**: 1,904 rows × 50 columns
- **New columns added**: 6 cleaned versions (3 clause mate + 3 pronoun)

## Note on Original Columns
The original columns with numbers and brackets are **preserved** in the dataset. The new `*_clean` columns are additions, not replacements, allowing for comparison and validation.

---

## Next Steps for Analysis
The cleaned columns are now ready for the linguistic analyses outlined in your task:

1. ✅ **Thematic role analysis**: Test if pronoun types correlate with clause mate thematic roles (Agent vs Patient/Recipient) - uses `pronoun_coreference_type_clean` and `clause_mate_thematic_role_clean`
2. ✅ **Grammatical role analysis**: Test if pronoun types correlate with clause mate grammatical roles (Subject vs Object) - uses `pronoun_coreference_type_clean` and `clause_mate_grammatical_role_clean`
3. ✅ **Clause mate count effects**: Test if number of clause mates affects pronoun form
4. ✅ **Linear distance analysis**: Test antecedent distance with/without clause mates

All analyses can now use the cleaned columns without dealing with numeric indices and chain IDs.
