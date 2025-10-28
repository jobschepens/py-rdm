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

# Store results
results = []

print("=" * 100)
print("STATISTICAL ANALYSIS: Feedback vs Affirmation by Language")
print("=" * 100)

# Analyze each language
for language in df_filtered['language'].unique():
    print(f"\n{'='*100}")
    print(f"LANGUAGE: {language}")
    print(f"{'='*100}")
    
    lang_data = df_filtered[df_filtered['language'] == language].copy()
    
    # Separate feedback and affirmation
    feedback = lang_data[lang_data['Label'] == 'feedback']
    affirmation = lang_data[lang_data['Label'] == 'affirmation']
    
    print(f"\nOriginal counts - Feedback: {len(feedback)}, Affirmation: {len(affirmation)}")
    
    for measurement in measurements:
        print(f"\n{'-'*100}")
        print(f"MEASUREMENT: {measurement}")
        print(f"{'-'*100}")
        
        # Remove outliers for each group separately
        feedback_clean = remove_outliers(feedback, measurement)
        affirmation_clean = remove_outliers(affirmation, measurement)
        
        n_feedback_removed = len(feedback) - len(feedback_clean)
        n_affirmation_removed = len(affirmation) - len(affirmation_clean)
        
        print(f"After outlier removal:")
        print(f"  Feedback: {len(feedback_clean)} (removed {n_feedback_removed} outliers)")
        print(f"  Affirmation: {len(affirmation_clean)} (removed {n_affirmation_removed} outliers)")
        
        # Get the cleaned data
        feedback_values = feedback_clean[measurement].values
        affirmation_values = affirmation_clean[measurement].values
        
        # Descriptive statistics
        print(f"\nDescriptive Statistics:")
        print(f"  Feedback    - Mean: {np.mean(feedback_values):.4f}, Median: {np.median(feedback_values):.4f}, SD: {np.std(feedback_values):.4f}")
        print(f"  Affirmation - Mean: {np.mean(affirmation_values):.4f}, Median: {np.median(affirmation_values):.4f}, SD: {np.std(affirmation_values):.4f}")
        print(f"  Difference  - Mean: {np.mean(feedback_values) - np.mean(affirmation_values):.4f}")
        
        # Test for normality (Shapiro-Wilk test)
        _, p_feedback_norm = stats.shapiro(feedback_values) if len(feedback_values) > 3 else (None, 0)
        _, p_affirmation_norm = stats.shapiro(affirmation_values) if len(affirmation_values) > 3 else (None, 0)
        
        # Choose appropriate test based on normality and sample size
        if p_feedback_norm > 0.05 and p_affirmation_norm > 0.05 and len(feedback_values) > 20 and len(affirmation_values) > 20:
            # Use parametric test (independent t-test)
            statistic, p_value = stats.ttest_ind(feedback_values, affirmation_values)
            test_used = "Independent t-test (parametric)"
        else:
            # Use non-parametric test (Mann-Whitney U test)
            statistic, p_value = stats.mannwhitneyu(feedback_values, affirmation_values, alternative='two-sided')
            test_used = "Mann-Whitney U test (non-parametric)"
        
        # Effect size (Cohen's d)
        pooled_std = np.sqrt((np.std(feedback_values)**2 + np.std(affirmation_values)**2) / 2)
        cohens_d = (np.mean(feedback_values) - np.mean(affirmation_values)) / pooled_std if pooled_std > 0 else 0
        
        # Interpret effect size
        if abs(cohens_d) < 0.2:
            effect_interpretation = "negligible"
        elif abs(cohens_d) < 0.5:
            effect_interpretation = "small"
        elif abs(cohens_d) < 0.8:
            effect_interpretation = "medium"
        else:
            effect_interpretation = "large"
        
        # Determine significance
        is_significant = "YES" if p_value < 0.05 else "NO"
        
        print(f"\nStatistical Test: {test_used}")
        print(f"  Test statistic: {statistic:.4f}")
        print(f"  p-value: {p_value:.4f}")
        print(f"  Significant difference (α=0.05): {is_significant}")
        print(f"  Effect size (Cohen's d): {cohens_d:.4f} ({effect_interpretation})")
        
        # Store results
        results.append({
            'Language': language,
            'Measurement': measurement,
            'Feedback_N': len(feedback_clean),
            'Affirmation_N': len(affirmation_clean),
            'Feedback_Mean': np.mean(feedback_values),
            'Affirmation_Mean': np.mean(affirmation_values),
            'Difference': np.mean(feedback_values) - np.mean(affirmation_values),
            'Test': test_used,
            'p_value': p_value,
            'Significant': is_significant,
            'Cohens_d': cohens_d,
            'Effect_Size': effect_interpretation
        })

# Create summary table
print(f"\n\n{'='*100}")
print("SUMMARY TABLE")
print(f"{'='*100}\n")

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

# Save results to CSV
results_df.to_csv(results_dir / 'feedback_affirmation_analysis_results.csv', index=False)
print(f"\n\nResults saved to: feedback_affirmation_analysis_results.csv")

# Create a visualization
fig, axes = plt.subplots(3, 4, figsize=(20, 15))
fig.suptitle('Feedback vs Affirmation by Language (Outliers Removed)', fontsize=16, fontweight='bold')

languages = df_filtered['language'].unique()

for idx, measurement in enumerate(measurements):
    for jdx, language in enumerate(languages):
        ax = axes[idx, jdx]
        
        # Get data for this language
        lang_data = df_filtered[df_filtered['language'] == language].copy()
        feedback = lang_data[lang_data['Label'] == 'feedback']
        affirmation = lang_data[lang_data['Label'] == 'affirmation']
        
        # Remove outliers
        feedback_clean = remove_outliers(feedback, measurement)
        affirmation_clean = remove_outliers(affirmation, measurement)
        
        # Create box plot
        data_to_plot = [feedback_clean[measurement], affirmation_clean[measurement]]
        bp = ax.boxplot(data_to_plot, labels=['Feedback', 'Affirmation'], patch_artist=True)
        
        # Color the boxes
        bp['boxes'][0].set_facecolor('lightblue')
        bp['boxes'][1].set_facecolor('lightgreen')
        
        # Add title and labels
        ax.set_title(f'{language}', fontweight='bold')
        if jdx == 0:
            ax.set_ylabel(measurement, fontweight='bold')
        
        # Add p-value annotation
        result = results_df[(results_df['Language'] == language) & (results_df['Measurement'] == measurement)]
        if not result.empty:
            p_val = result['p_value'].values[0]
            sig = result['Significant'].values[0]
            if sig == 'YES':
                ax.text(0.5, 0.95, f'p={p_val:.4f}*', transform=ax.transAxes, 
                       ha='center', va='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
            else:
                ax.text(0.5, 0.95, f'p={p_val:.4f}', transform=ax.transAxes, 
                       ha='center', va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
        
        ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(results_dir / 'feedback_affirmation_comparison.png', dpi=300, bbox_inches='tight')
print(f"Visualization saved to: feedback_affirmation_comparison.png")

print("\n" + "="*100)
print("ANALYSIS COMPLETE")
print("="*100)
