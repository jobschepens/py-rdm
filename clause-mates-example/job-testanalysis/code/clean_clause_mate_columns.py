"""
Clean clause mate and pronoun columns by removing numbers and brackets.
Creates new variables instead of modifying existing ones.
"""
import pandas as pd
import re
from pathlib import Path

# Set up paths - works from code/ subdirectory
current_dir = Path(__file__).parent
data_dir = current_dir.parent / 'processed_data'
results_dir = current_dir.parent / 'results'

# Create results directory if it doesn't exist
results_dir.mkdir(exist_ok=True)

# Read the CSV file
df = pd.read_csv(data_dir / 'unified_relationships.csv')

print(f"Original data shape: {df.shape}")
print("\nOriginal clause mate column samples:")
print(df[['clause_mate_grammatical_role', 'clause_mate_thematic_role', 'clause_mate_coreference_type']].head(10))

print("\nOriginal pronoun column samples:")
print(df[['pronoun_coreference_type', 'pronoun_grammatical_role', 'pronoun_thematic_role']].head(10))

# Function to remove numbers and brackets
def clean_annotation(value):
    """Remove numbers in brackets like [5] or [11] from annotation strings."""
    if pd.isna(value) or value == '_':
        return value
    # Remove pattern like [number] or [number]|[number] etc.
    cleaned = re.sub(r'\[\d+\]', '', str(value))
    # Remove any trailing or leading spaces/pipes
    cleaned = cleaned.strip('|').strip()
    return cleaned

# Create new cleaned columns for clause mates
df['clause_mate_grammatical_role_clean'] = df['clause_mate_grammatical_role'].apply(clean_annotation)
df['clause_mate_thematic_role_clean'] = df['clause_mate_thematic_role'].apply(clean_annotation)
df['clause_mate_coreference_type_clean'] = df['clause_mate_coreference_type'].apply(clean_annotation)

# Create new cleaned columns for pronouns
df['pronoun_coreference_type_clean'] = df['pronoun_coreference_type'].apply(clean_annotation)
df['pronoun_grammatical_role_clean'] = df['pronoun_grammatical_role'].apply(clean_annotation)
df['pronoun_thematic_role_clean'] = df['pronoun_thematic_role'].apply(clean_annotation)

print("\n" + "="*80)
print("Cleaned clause mate column samples:")
print(df[['clause_mate_grammatical_role_clean', 'clause_mate_thematic_role_clean', 'clause_mate_coreference_type_clean']].head(10))

print("\nCleaned pronoun column samples:")
print(df[['pronoun_coreference_type_clean', 'pronoun_grammatical_role_clean', 'pronoun_thematic_role_clean']].head(10))

# Show unique values for each cleaned column
print("\n" + "="*80)
print("CLAUSE MATE GRAMMATICAL ROLES (cleaned):")
print(df['clause_mate_grammatical_role_clean'].value_counts().head(20))

print("\n" + "="*80)
print("CLAUSE MATE THEMATIC ROLES (cleaned):")
print(df['clause_mate_thematic_role_clean'].value_counts().head(20))

print("\n" + "="*80)
print("CLAUSE MATE COREFERENCE TYPES (cleaned):")
print(df['clause_mate_coreference_type_clean'].value_counts().head(20))

print("\n" + "="*80)
print("PRONOUN COREFERENCE TYPES (cleaned):")
print(df['pronoun_coreference_type_clean'].value_counts().head(20))

print("\n" + "="*80)
print("PRONOUN GRAMMATICAL ROLES (cleaned):")
print(df['pronoun_grammatical_role_clean'].value_counts().head(20))

print("\n" + "="*80)
print("PRONOUN THEMATIC ROLES (cleaned):")
print(df['pronoun_thematic_role_clean'].value_counts().head(20))

# Save the updated dataframe
output_file = results_dir / 'unified_relationships_cleaned.csv'
df.to_csv(output_file, index=False)
print(f"\n" + "="*80)
print(f"Saved cleaned data to: {output_file}")
print(f"New data shape: {df.shape}")
print(f"\nNew columns added:")
print(f"  Clause mates: clause_mate_grammatical_role_clean, clause_mate_thematic_role_clean, clause_mate_coreference_type_clean")
print(f"  Pronouns: pronoun_coreference_type_clean, pronoun_grammatical_role_clean, pronoun_thematic_role_clean")
