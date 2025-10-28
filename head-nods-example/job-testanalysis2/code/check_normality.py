import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

# Set up paths - works from code/ subdirectory
current_dir = Path(__file__).parent
data_dir = current_dir.parent / 'data'
results_dir = current_dir.parent / 'results'

# Create results directory if it doesn't exist
results_dir.mkdir(exist_ok=True)

# Load the data
df = pd.read_csv(data_dir / 'function_wide_all_languages.csv')

# Filter to only feedback and affirmation
df_filtered = df[df['Label'].isin(['feedback', 'affirmation'])].copy()

# Function to remove outliers using IQR method
def remove_outliers(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

# Measurements to analyze
measurements = ['length (seconds)', 'extremes amplitude', 'velocity']

print("=" * 100)
print("NORMALITY TESTS: Shapiro-Wilk Test (p > 0.05 indicates normal distribution)")
print("=" * 100)

# Create figure for histograms and Q-Q plots
fig, axes = plt.subplots(4, 6, figsize=(24, 16))
fig.suptitle('Normality Assessment: Histograms and Q-Q Plots', fontsize=16, fontweight='bold')

row = 0
for language in df_filtered['language'].unique():
    print(f"\n{'='*100}")
    print(f"LANGUAGE: {language}")
    print(f"{'='*100}")
    
    lang_data = df_filtered[df_filtered['language'] == language].copy()
    
    # Separate feedback and affirmation
    feedback = lang_data[lang_data['Label'] == 'feedback']
    affirmation = lang_data[lang_data['Label'] == 'affirmation']
    
    for col_idx, measurement in enumerate(measurements):
        print(f"\n{measurement}:")
        
        # Remove outliers for each group separately
        feedback_clean = remove_outliers(feedback, measurement)
        affirmation_clean = remove_outliers(affirmation, measurement)
        
        # Get the cleaned data
        feedback_values = feedback_clean[measurement].values
        affirmation_values = affirmation_clean[measurement].values
        
        # Shapiro-Wilk test for normality
        if len(feedback_values) > 3:
            stat_f, p_f = stats.shapiro(feedback_values)
            is_normal_f = "YES" if p_f > 0.05 else "NO"
            print(f"  Feedback (n={len(feedback_values)}):    p={p_f:.4f} - Normal? {is_normal_f}")
        else:
            p_f = 0
            is_normal_f = "N/A (too few samples)"
            print(f"  Feedback (n={len(feedback_values)}):    {is_normal_f}")
        
        if len(affirmation_values) > 3:
            stat_a, p_a = stats.shapiro(affirmation_values)
            is_normal_a = "YES" if p_a > 0.05 else "NO"
            print(f"  Affirmation (n={len(affirmation_values)}): p={p_a:.4f} - Normal? {is_normal_a}")
        else:
            p_a = 0
            is_normal_a = "N/A (too few samples)"
            print(f"  Affirmation (n={len(affirmation_values)}): {is_normal_a}")
        
        # Levene's test for equal variances
        stat_lev, p_lev = stats.levene(feedback_values, affirmation_values)
        equal_var = "YES" if p_lev > 0.05 else "NO"
        print(f"  Equal variances (Levene): p={p_lev:.4f} - Equal? {equal_var}")
        
        # Recommendation
        both_normal = (p_f > 0.05 and p_a > 0.05) if len(feedback_values) > 3 and len(affirmation_values) > 3 else False
        large_samples = len(feedback_values) > 30 and len(affirmation_values) > 30
        
        if both_normal and large_samples:
            print(f"  ✅ RECOMMENDATION: t-test is appropriate (both normal, n>30)")
        elif both_normal:
            print(f"  ⚠️  RECOMMENDATION: t-test could work (both normal, but small n)")
        elif large_samples:
            print(f"  ⚠️  RECOMMENDATION: t-test might work (large n, CLT applies) BUT Mann-Whitney U is safer")
        else:
            print(f"  ❌ RECOMMENDATION: Use Mann-Whitney U test (non-normal distribution and/or small n)")
        
        # Create histogram for feedback
        ax_hist_f = axes[row, col_idx * 2]
        ax_hist_f.hist(feedback_values, bins=30, edgecolor='black', alpha=0.7)
        ax_hist_f.set_title(f'{language}\n{measurement}\nFeedback (n={len(feedback_values)})', fontsize=9)
        ax_hist_f.set_ylabel('Frequency')
        ax_hist_f.text(0.95, 0.95, f'p={p_f:.4f}\n{"Normal" if p_f > 0.05 else "Non-normal"}', 
                      transform=ax_hist_f.transAxes, ha='right', va='top',
                      bbox=dict(boxstyle='round', facecolor='lightgreen' if p_f > 0.05 else 'lightcoral', alpha=0.7))
        
        # Create histogram for affirmation
        ax_hist_a = axes[row, col_idx * 2 + 1]
        ax_hist_a.hist(affirmation_values, bins=15, edgecolor='black', alpha=0.7, color='orange')
        ax_hist_a.set_title(f'{language}\n{measurement}\nAffirmation (n={len(affirmation_values)})', fontsize=9)
        ax_hist_a.set_ylabel('Frequency')
        ax_hist_a.text(0.95, 0.95, f'p={p_a:.4f}\n{"Normal" if p_a > 0.05 else "Non-normal"}', 
                      transform=ax_hist_a.transAxes, ha='right', va='top',
                      bbox=dict(boxstyle='round', facecolor='lightgreen' if p_a > 0.05 else 'lightcoral', alpha=0.7))
    
    row += 1

plt.tight_layout()
plt.savefig(results_dir / 'normality_assessment.png', dpi=300, bbox_inches='tight')
print(f"\n\n{'='*100}")
print("Visualization saved to: normality_assessment.png")
print("="*100)

# Summary statistics
print("\n\n" + "="*100)
print("SUMMARY: When to use t-test vs Mann-Whitney U test")
print("="*100)
print("""
T-TEST (Parametric) Requirements:
1. Data is normally distributed (Shapiro-Wilk p > 0.05)
2. OR sample size is large (n > 30) so Central Limit Theorem applies
3. Independent samples
4. (For standard t-test) Equal variances (or use Welch's t-test if unequal)

MANN-WHITNEY U TEST (Non-parametric) Use when:
1. Data is NOT normally distributed (Shapiro-Wilk p < 0.05)
2. Sample size is small (n < 30) AND data is non-normal
3. Data has outliers (even after removal)
4. Data is ordinal or has ties
5. You want a more robust test with fewer assumptions

In this dataset:
- Most distributions are NON-NORMAL (Shapiro-Wilk p < 0.05)
- Some groups have small sample sizes (especially affirmation groups)
- Even after outlier removal, distributions remain skewed
- Therefore, Mann-Whitney U test is the SAFER and MORE APPROPRIATE choice
""")
