# job-testanalysis: count_csv_vars

Small helper to count the number of variables (columns) in a CSV file.

Usage examples (run from repository root):

```bash
python job-testanalysis/count_csv_vars.py head-nods-example/feedback_affirmation_analysis_results.csv
# prints the number of columns

# print header names instead:
python job-testanalysis/count_csv_vars.py head-nods-example/feedback_affirmation_analysis_results.csv --names

# specify a non-standard delimiter, e.g. semicolon:
python job-testanalysis/count_csv_vars.py data.csv --delimiter ';'
```

Exit codes:
- 0: success
- 2: file not found
- 3: path not a file
- 4: invalid delimiter argument
- 5: error reading CSV

The script uses Python's builtin csv module so it correctly handles quoted fields.
