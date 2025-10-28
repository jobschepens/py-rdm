#!/usr/bin/env python3
"""
Count columns (variables) in a CSV file.

Usage:
    python count_csv_vars.py path/to/file.csv [--names] [--delimiter DELIM]

Options:
    --names        Print the header names (first row) instead of just the count
    --delimiter    Specify a single-character delimiter (optional)

The script uses Python's csv module so it correctly handles quoted fields.
"""

from __future__ import annotations
import argparse
import csv
import sys
from pathlib import Path


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


def main() -> int:
    p = argparse.ArgumentParser(description="Count CSV columns (variables) in a file")
    p.add_argument("csv", help="Path to CSV file")
    p.add_argument("--names", action="store_true", help="Print header names (first row) rather than just the count")
    p.add_argument("--delimiter", help="Single-character delimiter to use instead of autodetect")
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
