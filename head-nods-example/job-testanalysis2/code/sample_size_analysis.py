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

print("=" * 120)
print("SAMPLE SIZE ANALYSIS: Are Affirmation Groups Large Enough for Statistical Testing?")
print("=" * 120)

# Summary table
summary_data = []

for language in df_filtered['language'].unique():
    lang_data = df_filtered[df_filtered['language'] == language].copy()
    feedback = lang_data[lang_data['Label'] == 'feedback']
    affirmation = lang_data[lang_data['Label'] == 'affirmation']
    
    print(f"\n{'='*120}")
    print(f"LANGUAGE: {language}")
    print(f"{'='*120}")
    
    for measurement in measurements:
        # Remove outliers
        feedback_clean = remove_outliers(feedback, measurement)
        affirmation_clean = remove_outliers(affirmation, measurement)
        
        n_feedback = len(feedback_clean)
        n_affirmation = len(affirmation_clean)
        
        print(f"\n{measurement}:")
        print(f"  Original: Feedback n={len(feedback)}, Affirmation n={len(affirmation)}")
        print(f"  After outlier removal: Feedback n={n_feedback}, Affirmation n={n_affirmation}")
        print(f"  Affirmation represents {100*n_affirmation/(n_feedback+n_affirmation):.1f}% of total sample")
        
        # Sample size recommendations for different tests
        print(f"\n  Sample Size Guidelines:")
        
        # For t-test (general rule of thumb)
        if n_affirmation >= 30:
            t_test_adequate = "✅ YES (n≥30, CLT applies)"
        elif n_affirmation >= 15:
            t_test_adequate = "⚠️  MARGINAL (15≤n<30, use with caution)"
        else:
            t_test_adequate = "❌ NO (n<15, too small for t-test)"
        print(f"    T-test: {t_test_adequate}")
        
        # For Mann-Whitney U test (more flexible)
        if n_affirmation >= 20:
            mw_adequate = "✅ YES (n≥20, good power)"
        elif n_affirmation >= 10:
            mw_adequate = "⚠️  ACCEPTABLE (10≤n<20, reduced power)"
        elif n_affirmation >= 5:
            mw_adequate = "⚠️  MINIMAL (5≤n<10, very low power)"
        else:
            mw_adequate = "❌ NO (n<5, insufficient)"
        print(f"    Mann-Whitney U: {mw_adequate}")
        
        # Calculate effect size from actual data
        feedback_values = feedback_clean[measurement].values
        affirmation_values = affirmation_clean[measurement].values
        
        pooled_std = np.sqrt((np.std(feedback_values)**2 + np.std(affirmation_values)**2) / 2)
        observed_effect = abs(np.mean(feedback_values) - np.mean(affirmation_values)) / pooled_std if pooled_std > 0 else 0
        
        # Power analysis approximation for Mann-Whitney U
        # Rule of thumb: minimum n ≈ 16/d² for 80% power at α=0.05 (balanced groups)
        if observed_effect > 0:
            recommended_n_large = int(np.ceil(16 / (observed_effect**2)))
            recommended_n_medium = int(np.ceil(16 / (0.5**2)))  # d=0.5
            recommended_n_small = int(np.ceil(16 / (0.2**2)))   # d=0.2
        else:
            recommended_n_large = recommended_n_medium = recommended_n_small = 999
        
        print(f"\n  Power Analysis (for 80% power at α=0.05):")
        print(f"    Observed effect size (Cohen's d): {observed_effect:.3f}")
        print(f"    Recommended n for observed effect: ~{min(recommended_n_large, 999)} per group")
        print(f"    Recommended n for medium effect (d=0.5): ~{recommended_n_medium} per group")
        print(f"    Recommended n for small effect (d=0.2): ~{recommended_n_small} per group")
        
        # Overall assessment
        if n_affirmation >= recommended_n_large and recommended_n_large < 999:
            power_assessment = "✅ ADEQUATE for observed effect"
        elif n_affirmation >= 20:
            power_assessment = "✅ ADEQUATE for medium-large effects, may miss small effects"
        elif n_affirmation >= 10:
            power_assessment = "⚠️  LOW POWER - can detect only large effects"
        else:
            power_assessment = "❌ UNDERPOWERED - likely to miss true effects"
        
        print(f"\n  📊 Overall Assessment: {power_assessment}")
        
        # Store for summary table
        summary_data.append({
            'Language': language,
            'Measurement': measurement,
            'n_feedback': n_feedback,
            'n_affirmation': n_affirmation,
            'percent_affirmation': 100*n_affirmation/(n_feedback+n_affirmation),
            'observed_cohens_d': observed_effect,
            't_test_adequate': 'Yes' if n_affirmation >= 30 else 'Marginal' if n_affirmation >= 15 else 'No',
            'mw_adequate': 'Yes' if n_affirmation >= 20 else 'Acceptable' if n_affirmation >= 10 else 'Minimal' if n_affirmation >= 5 else 'No',
            'power_assessment': power_assessment.split('-')[0].strip()
        })

# Create summary dataframe
summary_df = pd.DataFrame(summary_data)

print(f"\n\n{'='*120}")
print("SUMMARY TABLE")
print(f"{'='*120}\n")
print(summary_df.to_string(index=False))

# Overall statistics
print(f"\n\n{'='*120}")
print("OVERALL STATISTICS")
print(f"{'='*120}")

print(f"\nAffirmation Sample Sizes (after outlier removal):")
for lang in summary_df['Language'].unique():
    lang_data = summary_df[summary_df['Language'] == lang]
    min_n = lang_data['n_affirmation'].min()
    max_n = lang_data['n_affirmation'].max()
    avg_n = lang_data['n_affirmation'].mean()
    print(f"  {lang}: min={min_n}, max={max_n}, avg={avg_n:.1f}")

print(f"\nOverall Statistics:")
print(f"  Minimum affirmation n: {summary_df['n_affirmation'].min()}")
print(f"  Maximum affirmation n: {summary_df['n_affirmation'].max()}")
print(f"  Mean affirmation n: {summary_df['n_affirmation'].mean():.1f}")
print(f"  Median affirmation n: {summary_df['n_affirmation'].median():.1f}")

print(f"\nAdequacy for Mann-Whitney U test:")
adequate_count = (summary_df['mw_adequate'] == 'Yes').sum()
acceptable_count = (summary_df['mw_adequate'] == 'Acceptable').sum()
minimal_count = (summary_df['mw_adequate'] == 'Minimal').sum()
inadequate_count = (summary_df['mw_adequate'] == 'No').sum()
total = len(summary_df)

print(f"  ✅ Adequate (n≥20): {adequate_count}/{total} ({100*adequate_count/total:.1f}%)")
print(f"  ⚠️  Acceptable (10≤n<20): {acceptable_count}/{total} ({100*acceptable_count/total:.1f}%)")
print(f"  ⚠️  Minimal (5≤n<10): {minimal_count}/{total} ({100*minimal_count/total:.1f}%)")
print(f"  ❌ Inadequate (n<5): {inadequate_count}/{total} ({100*inadequate_count/total:.1f}%)")

# Statistical power concerns
print(f"\n\n{'='*120}")
print("RECOMMENDATIONS")
print(f"{'='*120}")

small_samples = summary_df[summary_df['n_affirmation'] < 30].copy()
if len(small_samples) > 0:
    print(f"\n⚠️  WARNING: {len(small_samples)}/{total} comparisons have affirmation n < 30")
    print(f"\nLanguages with small affirmation samples:")
    for lang in small_samples['Language'].unique():
        lang_samples = small_samples[small_samples['Language'] == lang]
        print(f"  • {lang}: n = {lang_samples['n_affirmation'].iloc[0]}-{lang_samples['n_affirmation'].max()}")

very_small = summary_df[summary_df['n_affirmation'] < 10].copy()
if len(very_small) > 0:
    print(f"\n❌ CRITICAL: {len(very_small)}/{total} comparisons have affirmation n < 10")
    print(f"   These are SEVERELY UNDERPOWERED and results should be interpreted with EXTREME CAUTION")

print(f"\n📋 Recommendations:")
print(f"   1. Mann-Whitney U test is still appropriate (works with small samples)")
print(f"   2. However, statistical POWER is reduced with small samples")
print(f"   3. Non-significant results may be due to lack of power, not lack of effect")
print(f"   4. Significant results are more trustworthy (harder to achieve with low power)")
print(f"   5. Consider reporting:")
print(f"      • Effect sizes (Cohen's d) alongside p-values")
print(f"      • Confidence intervals")
print(f"      • Power analysis or post-hoc power estimates")
print(f"      • Acknowledge sample size limitations in discussion")
print(f"   6. Consider collecting more affirmation data if possible")

# Save results
summary_df.to_csv(results_dir / 'sample_size_assessment.csv', index=False)
print(f"\n\nResults saved to: {results_dir / 'sample_size_assessment.csv'}")

print(f"\n{'='*120}")
print("KEY STATISTICAL CONCEPTS")
print(f"{'='*120}")
print("""
Sample Size Guidelines:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. MINIMUM SAMPLE SIZE (bare minimum to run the test):
   • Mann-Whitney U: n ≥ 3 per group (technically possible)
   • t-test: n ≥ 2 per group (technically possible)
   
2. PRACTICAL MINIMUM (to have any meaningful power):
   • Mann-Whitney U: n ≥ 10-15 per group
   • t-test: n ≥ 15-20 per group
   
3. RECOMMENDED FOR GOOD POWER (80% power to detect medium effect):
   • Both tests: n ≥ 30 per group
   • For small effects: n ≥ 100+ per group

4. UNEQUAL GROUP SIZES:
   • Having unequal groups reduces power
   • The smaller group determines overall power
   • Rule of thumb: try to keep ratio < 3:1

STATISTICAL POWER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Power = probability of detecting a true effect when it exists
• 80% power is considered acceptable (miss true effect 20% of time)
• Small samples = low power = high risk of Type II error (false negative)
• With low power:
  ✓ Significant results are MORE trustworthy (harder to achieve)
  ✗ Non-significant results are LESS trustworthy (may be underpowered)

Power depends on:
  1. Sample size (larger = more power)
  2. Effect size (larger = more power)
  3. Significance level (α=0.05 vs 0.01)
  4. Test type (one-tailed vs two-tailed)
""")

print(f"{'='*120}")
print("ANALYSIS COMPLETE")
print(f"{'='*120}")
