"""
Analyze the relationship between pronoun types and clause mate thematic roles.

Research Questions:
1. Do personal pronouns appear more often with clause mates having Patient/Recipient roles?
2. Do demonstrative pronouns appear more often with clause mates having Agent roles?
"""
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact  # type: ignore
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set up paths - works from code/ subdirectory
current_dir = Path(__file__).parent
data_dir = current_dir.parent / 'processed_data'
results_dir = current_dir.parent / 'results'

# Create results directory if it doesn't exist
results_dir.mkdir(exist_ok=True)

# Read the cleaned data
df = pd.read_csv(data_dir / 'unified_relationships_cleaned.csv') # type: ignore

print("="*80)
print("PRONOUN TYPE vs CLAUSE MATE THEMATIC ROLE ANALYSIS")
print("="*80)

# First, let's classify pronoun types based on pronoun_coreference_type_clean
print("\n1. Classifying Pronoun Types")
print("-"*80)

# Check unique pronoun types in the data
print("\nUnique pronoun coreference types (cleaned):")
print(df['pronoun_coreference_type_clean'].value_counts())

# Classify pronouns into categories
def classify_pronoun_type(coref_type):
    """Classify pronouns as Personal or Demonstrative."""
    if pd.isna(coref_type):
        return 'Other'
    coref_str = str(coref_type)
    if 'PersPron' in coref_str:
        return 'Personal'
    elif 'D-Pron' in coref_str or 'demNP' in coref_str:
        return 'Demonstrative'
    else:
        return 'Other'

df['pronoun_type'] = df['pronoun_coreference_type_clean'].apply(classify_pronoun_type) # type: ignore

print("\nPronoun type distribution:")
print(df['pronoun_type'].value_counts())

# Clean thematic roles - focus on main categories
print("\n2. Analyzing Clause Mate Thematic Roles")
print("-"*80)

print("\nClause mate thematic role distribution (cleaned):")
print(df['clause_mate_thematic_role_clean'].value_counts())

# Simplify thematic roles into Agent vs Patient/Recipient
def classify_thematic_role(role):
    """Classify thematic roles into Agent vs Patient/Recipient."""
    if pd.isna(role) or role == '_' or role == '*':
        return 'Unspecified'
    role_str = str(role)
    if 'Proto-Ag' in role_str or 'Agent' in role_str:
        return 'Agent'
    elif 'Proto-Pat' in role_str or 'Patient' in role_str or 'Recipient' in role_str:
        return 'Patient/Recipient'
    else:
        return 'Other'

df['thematic_role_category'] = df['clause_mate_thematic_role_clean'].apply(classify_thematic_role)

print("\nThematic role categories:")
print(df['thematic_role_category'].value_counts())

# Filter to only Personal and Demonstrative pronouns with Agent or Patient/Recipient roles
df_filtered = df[
    (df['pronoun_type'].isin(['Personal', 'Demonstrative'])) &
    (df['thematic_role_category'].isin(['Agent', 'Patient/Recipient']))
].copy()

print(f"\nFiltered dataset size: {len(df_filtered)} rows")
print(f"(Removed {len(df) - len(df_filtered)} rows with 'Other' or 'Unspecified' categories)")

# Create contingency table
print("\n" + "="*80)
print("3. CONTINGENCY TABLE")
print("="*80)

contingency_table = pd.crosstab(
    df_filtered['pronoun_type'],
    df_filtered['thematic_role_category'],
    margins=True
)

print("\nAbsolute counts:")
print(contingency_table)

# Calculate percentages
print("\n" + "-"*80)
print("Row percentages (within each pronoun type):")
print("-"*80)
contingency_pct_row = pd.crosstab(
    df_filtered['pronoun_type'],
    df_filtered['thematic_role_category'],
    normalize='index'
) * 100

print(contingency_pct_row.round(2))

print("\n" + "-"*80)
print("Column percentages (within each thematic role):")
print("-"*80)
contingency_pct_col = pd.crosstab(
    df_filtered['pronoun_type'],
    df_filtered['thematic_role_category'],
    normalize='columns'
) * 100

print(contingency_pct_col.round(2))

# Statistical test: Chi-square test
print("\n" + "="*80)
print("4. CHI-SQUARE TEST OF INDEPENDENCE")
print("="*80)

# Get the contingency table without margins
ct_no_margins = pd.crosstab(
    df_filtered['pronoun_type'],
    df_filtered['thematic_role_category']
)

chi2, p_value, dof, expected = chi2_contingency(ct_no_margins)

print(f"\nChi-square statistic: {chi2:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"P-value: {p_value:.6f}")
print(f"\nSignificance level interpretation:")
if p_value < 0.001:
    print("*** Highly significant (p < 0.001)")
elif p_value < 0.01:
    print("** Very significant (p < 0.01)")
elif p_value < 0.05:
    print("* Significant (p < 0.05)")
else:
    print("Not significant (p ≥ 0.05)")

print("\nExpected frequencies (under independence):")
expected_df = pd.DataFrame(
    expected,
    index=ct_no_margins.index,
    columns=ct_no_margins.columns
)
print(expected_df.round(2))

# Calculate effect size (Cramér's V)
n = ct_no_margins.sum().sum()
cramers_v = np.sqrt(chi2 / (n * (min(ct_no_margins.shape) - 1)))
print(f"\nEffect size (Cramér's V): {cramers_v:.4f}")
if cramers_v < 0.1:
    print("Effect size: Small")
elif cramers_v < 0.3:
    print("Effect size: Medium")
else:
    print("Effect size: Large")

# Fisher's exact test (alternative for 2x2 tables)
if ct_no_margins.shape == (2, 2):
    print("\n" + "="*80)
    print("5. FISHER'S EXACT TEST (for 2x2 table)")
    print("="*80)
    
    odds_ratio, fisher_p = fisher_exact(ct_no_margins)
    print(f"\nOdds ratio: {odds_ratio:.4f}")
    print(f"P-value (two-tailed): {fisher_p:.6f}")
    
    if fisher_p < 0.05:
        print("* Significant (p < 0.05)")
    else:
        print("Not significant (p ≥ 0.05)")

# Specific hypothesis tests
print("\n" + "="*80)
print("6. HYPOTHESIS-SPECIFIC ANALYSIS")
print("="*80)

print("\nHypothesis 1: Personal pronouns with Patient/Recipient roles")
print("-"*80)
personal = df_filtered[df_filtered['pronoun_type'] == 'Personal']
personal_patient_pct = (personal['thematic_role_category'] == 'Patient/Recipient').sum() / len(personal) * 100
personal_agent_pct = (personal['thematic_role_category'] == 'Agent').sum() / len(personal) * 100

print(f"Personal pronouns with Patient/Recipient: {personal_patient_pct:.2f}%")
print(f"Personal pronouns with Agent: {personal_agent_pct:.2f}%")

if personal_patient_pct > personal_agent_pct:
    print("✓ Hypothesis SUPPORTED: Personal pronouns appear more with Patient/Recipient roles")
else:
    print("✗ Hypothesis NOT supported: Personal pronouns do not appear more with Patient/Recipient roles")

print("\nHypothesis 2: Demonstrative pronouns with Agent roles")
print("-"*80)
demonstrative = df_filtered[df_filtered['pronoun_type'] == 'Demonstrative']
dem_agent_pct = (demonstrative['thematic_role_category'] == 'Agent').sum() / len(demonstrative) * 100
dem_patient_pct = (demonstrative['thematic_role_category'] == 'Patient/Recipient').sum() / len(demonstrative) * 100

print(f"Demonstrative pronouns with Agent: {dem_agent_pct:.2f}%")
print(f"Demonstrative pronouns with Patient/Recipient: {dem_patient_pct:.2f}%")

if dem_agent_pct > dem_patient_pct:
    print("✓ Hypothesis SUPPORTED: Demonstrative pronouns appear more with Agent roles")
else:
    print("✗ Hypothesis NOT supported: Demonstrative pronouns do not appear more with Agent roles")

# Visualization
print("\n" + "="*80)
print("7. CREATING VISUALIZATIONS")
print("="*80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Pronoun Type vs Clause Mate Thematic Role Analysis', fontsize=16, fontweight='bold')

# Plot 1: Stacked bar chart (row percentages)
ax1 = axes[0, 0]
contingency_pct_row.plot(kind='bar', stacked=True, ax=ax1, color=['#e74c3c', '#3498db'])
ax1.set_title('Distribution within Each Pronoun Type\n(Row Percentages)', fontweight='bold')
ax1.set_xlabel('Pronoun Type')
ax1.set_ylabel('Percentage (%)')
ax1.legend(title='Thematic Role', bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
ax1.grid(axis='y', alpha=0.3)

# Plot 2: Grouped bar chart (absolute counts)
ax2 = axes[0, 1]
ct_no_margins.plot(kind='bar', ax=ax2, color=['#e74c3c', '#3498db'])
ax2.set_title('Absolute Counts', fontweight='bold')
ax2.set_xlabel('Pronoun Type')
ax2.set_ylabel('Count')
ax2.legend(title='Thematic Role', bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
ax2.grid(axis='y', alpha=0.3)

# Plot 3: Heatmap of observed frequencies
ax3 = axes[1, 0]
sns.heatmap(ct_no_margins, annot=True, fmt='d', cmap='YlOrRd', ax=ax3, cbar_kws={'label': 'Count'})
ax3.set_title('Observed Frequencies Heatmap', fontweight='bold')
ax3.set_xlabel('Thematic Role')
ax3.set_ylabel('Pronoun Type')

# Plot 4: Heatmap of standardized residuals
ax4 = axes[1, 1]
residuals = (ct_no_margins - expected_df) / np.sqrt(expected_df)
sns.heatmap(residuals, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=ax4, 
            cbar_kws={'label': 'Standardized Residual'})
ax4.set_title('Standardized Residuals\n(deviation from expected)', fontweight='bold')
ax4.set_xlabel('Thematic Role')
ax4.set_ylabel('Pronoun Type')

plt.tight_layout()
plt.savefig(results_dir / 'pronoun_thematic_role_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved visualization: pronoun_thematic_role_analysis.png")

# Additional mosaic plot for better visualization of proportions
fig2, ax = plt.subplots(figsize=(10, 6))

# Create mosaic-like visualization using grouped bars with normalized heights
x = np.arange(len(ct_no_margins.index))
width = 0.35

agent_counts = ct_no_margins['Agent'].values
patient_counts = ct_no_margins['Patient/Recipient'].values
totals = agent_counts + patient_counts

agent_props = agent_counts / totals * 100
patient_props = patient_counts / totals * 100

ax.bar(x - width/2, agent_props, width, label='Agent', color='#e74c3c', alpha=0.8)
ax.bar(x + width/2, patient_props, width, label='Patient/Recipient', color='#3498db', alpha=0.8)

ax.set_xlabel('Pronoun Type', fontweight='bold')
ax.set_ylabel('Percentage within Pronoun Type (%)', fontweight='bold')
ax.set_title('Thematic Role Distribution by Pronoun Type\n(Shows relative preference within each pronoun type)', 
             fontweight='bold', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(ct_no_margins.index)
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 100)

# Add percentage labels on bars
for i, (a_prop, p_prop) in enumerate(zip(agent_props, patient_props)):
    ax.text(i - width/2, a_prop + 2, f'{a_prop:.1f}%', ha='center', va='bottom', fontweight='bold')
    ax.text(i + width/2, p_prop + 2, f'{p_prop:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(results_dir / 'pronoun_thematic_role_percentages.png', dpi=300, bbox_inches='tight')
print("✓ Saved visualization: pronoun_thematic_role_percentages.png")

# Save detailed results to CSV
print("\n" + "="*80)
print("8. SAVING RESULTS")
print("="*80)

results_summary = pd.DataFrame({
    'Pronoun_Type': ct_no_margins.index.tolist(),
    'Agent_Count': ct_no_margins['Agent'].values,
    'Patient_Recipient_Count': ct_no_margins['Patient/Recipient'].values,
    'Total': ct_no_margins.sum(axis=1).values,
    'Pct_Agent': contingency_pct_row['Agent'].values,
    'Pct_Patient_Recipient': contingency_pct_row['Patient/Recipient'].values
})

results_summary.to_csv(results_dir / 'thematic_role_analysis_summary.csv', index=False)
print("✓ Saved summary: thematic_role_analysis_summary.csv")

# Save statistical test results
with open(results_dir / 'thematic_role_analysis_statistics.txt', 'w') as f:
    f.write("PRONOUN TYPE vs CLAUSE MATE THEMATIC ROLE - STATISTICAL ANALYSIS\n")
    f.write("="*80 + "\n\n")
    
    f.write("CHI-SQUARE TEST OF INDEPENDENCE\n")
    f.write("-"*80 + "\n")
    f.write(f"Chi-square statistic: {chi2:.4f}\n")
    f.write(f"Degrees of freedom: {dof}\n")
    f.write(f"P-value: {p_value:.6f}\n")
    f.write(f"Cramér's V (effect size): {cramers_v:.4f}\n\n")
    
    if ct_no_margins.shape == (2, 2):
        f.write("FISHER'S EXACT TEST\n")
        f.write("-"*80 + "\n")
        f.write(f"Odds ratio: {odds_ratio:.4f}\n")
        f.write(f"P-value (two-tailed): {fisher_p:.6f}\n\n")
    
    f.write("HYPOTHESIS TESTING\n")
    f.write("-"*80 + "\n")
    f.write(f"H1: Personal pronouns with Patient/Recipient: {personal_patient_pct:.2f}%\n")
    f.write(f"H1: Personal pronouns with Agent: {personal_agent_pct:.2f}%\n")
    f.write(f"H1: Result: {'SUPPORTED' if personal_patient_pct > personal_agent_pct else 'NOT SUPPORTED'}\n\n")
    f.write(f"H2: Demonstrative pronouns with Agent: {dem_agent_pct:.2f}%\n")
    f.write(f"H2: Demonstrative pronouns with Patient/Recipient: {dem_patient_pct:.2f}%\n")
    f.write(f"H2: Result: {'SUPPORTED' if dem_agent_pct > dem_patient_pct else 'NOT SUPPORTED'}\n")

print("✓ Saved statistics: thematic_role_analysis_statistics.txt")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\nFiles created:")
print("  1. pronoun_thematic_role_analysis.png")
print("  2. pronoun_thematic_role_percentages.png")
print("  3. thematic_role_analysis_summary.csv")
print("  4. thematic_role_analysis_statistics.txt")
