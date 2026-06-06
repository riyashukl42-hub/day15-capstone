"""
cleaning.py — Reusable data cleaning functions
Day 04 — 15-Day Data Analyst Challenge
Author: Riya Shukla
"""

import pandas as pd
import numpy as np


def check_quality(df, name="Dataset"):
    """Print a data quality report for any DataFrame."""
    print(f"\n{'='*45}")
    print(f"  Data Quality Report: {name}")
    print(f"{'='*45}")
    print(f"  Rows:           {len(df):,}")
    print(f"  Columns:        {len(df.columns)}")
    print(f"  Missing values: {df.isnull().sum().sum():,}")
    print(f"  Duplicates:     {df.duplicated().sum():,}")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) > 0:
        print(f"\n  Missing by column:")
        for col, count in missing.items():
            pct = count / len(df) * 100
            print(f"    {col}: {count} ({pct:.1f}%)")
    print(f"{'='*45}\n")


def remove_outliers_iqr(df, column):
    """Remove outliers from a column using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    before = len(df)
    df_out = df[(df[column] >= lower) & (df[column] <= upper)]
    removed = before - len(df_out)
    print(f"  Outliers removed from {column}: {removed} rows")
    return df_out


def fill_missing_median(df, columns):
    """Fill missing values in numeric columns with the column median."""
    for col in columns:
        n_missing = df[col].isnull().sum()
        if n_missing > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  Filled {n_missing} missing in '{col}' with median: {median_val:.2f}")
    return df


def fill_missing_mode(df, columns):
    """Fill missing values in categorical columns with the column mode."""
    for col in columns:
        n_missing = df[col].isnull().sum()
        if n_missing > 0:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            print(f"  Filled {n_missing} missing in '{col}' with mode: {mode_val}")
    return df


def standardise_text(df, columns):
    """Standardise text columns to Title Case with no whitespace."""
    for col in columns:
        df[col] = df[col].astype(str).str.strip().str.title()
    print(f"  Standardised text in: {columns}")
    return df


def drop_duplicates_report(df):
    """Drop duplicate rows and report how many were removed."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    print(f"  Duplicates removed: {removed}")
    return df


def quality_summary(before_df, after_df):
    """Print a before/after data quality comparison."""
    print(f"\n{'='*55}")
    print(f"  Before vs After Cleaning")
    print(f"{'='*55}")
    print(f"  {'Metric':<25} {'Before':>10} {'After':>10}")
    print(f"  {'-'*45}")
    print(f"  {'Rows':<25} {len(before_df):>10,} {len(after_df):>10,}")
    print(f"  {'Missing values':<25} {before_df.isnull().sum().sum():>10,} {after_df.isnull().sum().sum():>10,}")
    print(f"  {'Duplicates':<25} {before_df.duplicated().sum():>10,} {after_df.duplicated().sum():>10,}")
    print(f"{'='*55}\n")