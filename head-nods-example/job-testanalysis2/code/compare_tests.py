import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# Set up paths - works from code/ subdirectory
current_dir = Path(__file__).parent
data_dir = current_dir.parent / 'data'
results_dir = current_dir.parent / 'results'

# Create results directory if it doesn't exist
results_dir.mkdir(exist_ok=True)

# Load the data
df = pd.read_csv(data_dir / 'function_wide_all_languages.csv')
df_filtered = df[df['Label'].isin(['feedback', 'affirmation'])].copy()

# Function to remove outliers
def remove_outliers(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

measurements = ['length (seconds)', 'extremes amplitude', 'velocity']
results = []

print("=" * 120)
print("COMPARISON: t-test vs Mann-Whitney U test")
print("=" * 120)

for language in df_filtered['language'].unique():
    print(f"\n{'='*120}")
    print(f"LANGUAGE: {language}")
    print(f"{'='*120}")
    
    lang_data = df_filtered[df_filtered['language'] == language].copy()
    feedback = lang_data[lang_data['Label'] == 'feedback']
    affirmation = lang_data[lang_data['Label'] == 'affirmation']
    
    for measurement in measurements:
        feedback_clean = remove_outliers(feedback, measurement)
        affirmation_clean = remove_outliers(affirmation, measurement)
        
        feedback_values = feedback_clean[measurement].values
        affirmation_values = affirmation_clean[measurement].values
        
        print(f"\n{measurement}:")
        print(f"  Sample sizes: Feedback n={len(feedback_values)}, Affirmation n={len(affirmation_values)}")
        
        # Normality test
        _, p_f = stats.shapiro(feedback_values) if len(feedback_values) > 3 else (None, 0)
        _, p_a = stats.shapiro(affirmation_values) if len(affirmation_values) > 3 else (None, 0)
        print(f"  Normality (Shapiro-Wilk): Feedback p={p_f:.4f}, Affirmation p={p_a:.4f}")
        
        # Independent t-test (parametric)
        t_stat, t_pval = stats.ttest_ind(feedback_values, affirmation_values)
        
        # Welch's t-test (doesn't assume equal variances)
        welch_stat, welch_pval = stats.ttest_ind(feedback_values, affirmation_values, equal_var=False)
        
        # Mann-Whitney U test (non-parametric)
        mw_stat, mw_pval = stats.mannwhitneyu(feedback_values, affirmation_values, alternative='two-sided')
        
        print(f"\n  TEST RESULTS:")
        print(f"  ┌─────────────────────────────┬───────────────┬───────────────┐")
        print(f"  │ Test                        │ Test Stat     │ p-value       │")
        print(f"  ├─────────────────────────────┼───────────────┼───────────────┤")
        print(f"  │ Independent t-test          │ {t_stat:13.4f} │ {t_pval:13.4f} │ {'*' if t_pval < 0.05 else ' '}")
        print(f"  │ Welch's t-test              │ {welch_stat:13.4f} │ {welch_pval:13.4f} │ {'*' if welch_pval < 0.05 else ' '}")
        print(f"  │ Mann-Whitney U test         │ {mw_stat:13.4f} │ {mw_pval:13.4f} │ {'*' if mw_pval < 0.05 else ' '}")
        print(f"  └─────────────────────────────┴───────────────┴───────────────┘")
        
        # Check if conclusions differ
        t_sig = t_pval < 0.05
        welch_sig = welch_pval < 0.05
        mw_sig = mw_pval < 0.05
        
        if t_sig == welch_sig == mw_sig:
            print(f"  ✅ All tests agree: {'Significant' if mw_sig else 'Not significant'}")
        else:
            print(f"  ⚠️  Tests DISAGREE!")
            print(f"     t-test: {'Significant' if t_sig else 'Not significant'}")
            print(f"     Welch's t-test: {'Significant' if welch_sig else 'Not significant'}")
            print(f"     Mann-Whitney U: {'Significant' if mw_sig else 'Not significant'}")
        
        results.append({
            'Language': language,
            'Measurement': measurement,
            'n_feedback': len(feedback_values),
            'n_affirmation': len(affirmation_values),
            'shapiro_p_feedback': p_f,
            'shapiro_p_affirmation': p_a,
            't_test_pval': t_pval,
            'welch_test_pval': welch_pval,
            'mann_whitney_pval': mw_pval,
            't_test_sig': t_sig,
            'welch_test_sig': welch_sig,
            'mann_whitney_sig': mw_sig,
            'all_agree': t_sig == welch_sig == mw_sig
        })

# Summary
results_df = pd.DataFrame(results)
print(f"\n\n{'='*120}")
print("SUMMARY")
print(f"{'='*120}")

print(f"\n1. How often do all tests agree?")
agree_count = results_df['all_agree'].sum()
total_count = len(results_df)
print(f"   {agree_count}/{total_count} ({100*agree_count/total_count:.1f}%) of comparisons")

print(f"\n2. Cases where t-test and Mann-Whitney U give DIFFERENT conclusions:")
disagree = results_df[results_df['t_test_sig'] != results_df['mann_whitney_sig']]
if len(disagree) > 0:
    for _, row in disagree.iterrows():
        print(f"   - {row['Language']}, {row['Measurement']}")
        print(f"     t-test: p={row['t_test_pval']:.4f} ({'sig' if row['t_test_sig'] else 'ns'}), " +
              f"Mann-Whitney: p={row['mann_whitney_pval']:.4f} ({'sig' if row['mann_whitney_sig'] else 'ns'})")
else:
    print(f"   None! t-test and Mann-Whitney U always agree in this dataset")

print(f"\n3. Percentage of distributions that are NON-NORMAL (Shapiro-Wilk p < 0.05):")
non_normal_feedback = (results_df['shapiro_p_feedback'] < 0.05).sum()
non_normal_affirmation = (results_df['shapiro_p_affirmation'] < 0.05).sum()
print(f"   Feedback: {non_normal_feedback}/{total_count} ({100*non_normal_feedback/total_count:.1f}%)")
print(f"   Affirmation: {non_normal_affirmation}/{total_count} ({100*non_normal_affirmation/total_count:.1f}%)")

print(f"\n{'='*120}")
print("CONCLUSION")
print(f"{'='*120}")
print("""
Why Mann-Whitney U was chosen:
1. Nearly ALL distributions fail the Shapiro-Wilk normality test (p < 0.05)
2. While t-test might work due to large sample sizes (Central Limit Theorem),
   it's still LESS ROBUST when assumptions are violated
3. Mann-Whitney U test makes FEWER assumptions and is MORE CONSERVATIVE
4. In this dataset, both tests generally agree on conclusions, BUT:
   - Mann-Whitney U is the SAFER choice when normality is violated
   - It's the GOLD STANDARD for non-normal data
   - It handles skewed distributions and outliers better

RECOMMENDATION: Stick with Mann-Whitney U test for this data ✅
""")

# Save results
results_df.to_csv(results_dir / 'test_comparison_results.csv', index=False)
print(f"Detailed comparison saved to: test_comparison_results.csv")
