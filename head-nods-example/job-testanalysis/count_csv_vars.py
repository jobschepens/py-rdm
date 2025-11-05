#!/usr/bin/env python3
"""
Count columns (variables) in a CSV file.

Usage:
    python count_csv_vars.py path/to/file.csv [--names] [--types] [--delimiter DELIM]

Options:
    --names        Print the header names (first row) instead of just the count
    --types        Print inferred types for each column
    --delimiter    Specify a single-character delimiter (optional)

The script uses Python's csv module so it correctly handles quoted fields.
"""

from __future__ import annotations
import argparse
import csv
import sys
from pathlib import Path


def infer_type(value: str) -> str:
    """Infer the type of a string value."""
    if not value or value.strip() == "":
        return "empty"
    
    # Try integer
    try:
        int(value)
        return "int"
    except ValueError:
        pass
    
    # Try float
    try:
        float(value)
        return "float"
    except ValueError:
        pass
    
    # Try boolean
    if value.lower() in ("true", "false", "yes", "no", "t", "f", "y", "n"):
        return "bool"
    
    # Default to string
    return "str"


def count_columns(path: Path, delimiter: str | None = None) -> tuple[int, list[str]]:
    """Return (num_columns, header_row_list). If file is empty, returns (0, [])."""
    with path.open(newline='', encoding='utf-8') as fh:
        if delimiter:
            reader = csv.reader(fh, delimiter=delimiter)
        else:
            reader = csv.reader(fh)
        try:
            row = next(reader)
        except StopIteration:
            return 0, []
        return len(row), row


def infer_column_types(path: Path, delimiter: str | None = None, sample_rows: int = 100) -> tuple[list[str], list[str]]:
    """
    Infer types for each column by sampling data rows.
    Returns (header_list, types_list).
    """
    with path.open(newline='', encoding='utf-8') as fh:
        if delimiter:
            reader = csv.reader(fh, delimiter=delimiter)
        else:
            reader = csv.reader(fh)
        
        try:
            header = next(reader)
        except StopIteration:
            return [], []
        
        num_cols = len(header)
        # Track types seen for each column
        column_types: list[set[str]] = [set() for _ in range(num_cols)]
        
        # Sample rows to infer types
        for i, row in enumerate(reader):
            if i >= sample_rows:
                break
            for col_idx, value in enumerate(row):
                if col_idx < num_cols:
                    column_types[col_idx].add(infer_type(value))
        
        # Determine final type for each column
        final_types: list[str] = []
        for types_set in column_types:
            types_set.discard("empty")  # Ignore empty values
            if not types_set:
                final_types.append("unknown")
            elif len(types_set) == 1:
                final_types.append(types_set.pop())
            elif "str" in types_set:
                final_types.append("str")  # If mixed with string, it's string
            elif "float" in types_set and "int" in types_set:
                final_types.append("float")  # int/float mix -> float
            else:
                final_types.append("mixed")
        
        return header, final_types


def main() -> int:
    p = argparse.ArgumentParser(description="Count CSV columns (variables) in a file")
    p.add_argument("csv", help="Path to CSV file")
    p.add_argument("--names", action="store_true", help="Print header names (first row) rather than just the count")
    p.add_argument("--types", action="store_true", help="Print inferred types for each column")
    p.add_argument("--delimiter", help="Single-character delimiter to use instead of autodetect")
    p.add_argument("--sample-rows", type=int, default=100, help="Number of rows to sample for type inference (default: 100)")
    args = p.parse_args()

    path = Path(args.csv)
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2
    if not path.is_file():
        print(f"Error: not a file: {path}", file=sys.stderr)
        return 3

    delim = args.delimiter
    if delim is not None and len(delim) != 1:
        print("Error: --delimiter must be a single character", file=sys.stderr)
        return 4

    try:
        if args.types:
            header, types = infer_column_types(path, delim, args.sample_rows)
            if header:
                for name, dtype in zip(header, types):
                    print(f"{name}: {dtype}")
            return 0
        else:
            n, header = count_columns(path, delim)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        return 5

    if args.names:
        if header:
            print(','.join(header))
        else:
            print("")
    else:
        print(n)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
