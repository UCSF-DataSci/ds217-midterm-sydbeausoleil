#!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
# These utilities will be imported and used in Q4-Q7 notebooks.

import pandas as pd
import numpy as np

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates and replace sentinel values with NaN.
    """
    if remove_duplicates:
        df = df.drop_duplicates()

    df = df.replace(sentinel_value, np.nan)
    return df


def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Return count of missing values per column.
    """
    return df.isna().sum()


def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    """
    Fill missing values in a column using specified strategy.
    """
    if column not in df.columns:
        print(f"Column '{column}' not found in DataFrame.")
        return df

    if strategy == 'mean':
        fill_value = df[column].mean()
    elif strategy == 'median':
        fill_value = df[column].median()
    elif strategy == 'ffill':
        df[column] = df[column].fillna(method='ffill')
        return df
    else:
        print(f"Unsupported fill strategy: {strategy}")
        return df

    df[column] = df[column].fillna(fill_value)
    return df


def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    """
    Apply a list of filters to DataFrame in sequence.
    """
    filtered_df = df.copy()
    for f in filters:
        col = f.get('column')
        cond = f.get('condition')
        val = f.get('value')

        if col not in filtered_df.columns:
            print(f"Column '{col}' not found.")
            continue

        if cond == 'equals':
            filtered_df = filtered_df[filtered_df[col] == val]
        elif cond == 'greater_than':
            filtered_df = filtered_df[filtered_df[col] > val]
        elif cond == 'less_than':
            filtered_df = filtered_df[filtered_df[col] < val]
        elif cond == 'in_range' and isinstance(val, (list, tuple)) and len(val) == 2:
            filtered_df = filtered_df[(filtered_df[col] >= val[0]) & (filtered_df[col] <= val[1])]
        elif cond == 'in_list' and isinstance(val, list):
            filtered_df = filtered_df[filtered_df[col].isin(val)]
        else:
            print(f"Unsupported filter condition: {cond}")

    return filtered_df


def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """
    Convert column data types based on mapping.
    """
    for col, t in type_map.items():
        if col not in df.columns:
            print(f"Column '{col}' not found for type conversion.")
            continue

        if t == 'datetime':
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif t == 'numeric':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif t == 'category':
            df[col] = df[col].astype('category')
        elif t == 'string':
            df[col] = df[col].astype(str)
        else:
            print(f"Unsupported type conversion: {t}")

    return df


def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().
    """
    if column not in df.columns:
        print(f"Column '{column}' not found for binning.")
        return df

    if new_column is None:
        new_column = f"{column}_binned"

    df[new_column] = pd.cut(df[column], bins=bins, labels=labels, include_lowest=True)
    return df


def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    """
    Group data and apply aggregations.
    """
    if group_col not in df.columns:
        print(f"Group column '{group_col}' not found.")
        return pd.DataFrame()

    if agg_dict is None:
        return df.groupby(group_col).describe()

    return df.groupby(group_col).agg(agg_dict)


if __name__ == '__main__':
    print("Data utilities loaded successfully!")
    print("Available functions:")
    print("  - load_data()")
    print("  - clean_data()")
    print("  - detect_missing()")
    print("  - fill_missing()")
    print("  - filter_data()")
    print("  - transform_types()")
    print("  - create_bins()")
    print("  - summarize_by_group()")

    # Simple test example
    test_df = pd.DataFrame({
        'age': [25, np.nan, 40, 25],
        'bmi': [22, -999, 28, 22],
        'site': ['A', 'B', 'A', 'A']
    })
    print("\n Test DataFrame:")
    print(test_df)

    test_df = clean_data(test_df)
    print("\nAfter cleaning:")
    print(test_df)

    print("\nMissing values per column:")
    print(detect_missing(test_df))

    filled_df = fill_missing(test_df, 'age', strategy='median')
    print("\nAfter filling missing values in 'age':")
    print(filled_df)

    filtered_df = filter_data(filled_df, [{'column': 'site', 'condition': 'equals', 'value': 'A'}])
    print("\nFiltered data (site == 'A'):")
    print(filtered_df)
