"""
Data Loader Module
Handles loading Excel data
"""

import pandas as pd


def load_excel_data(file_path):
    """
    Load data from Excel file.
    """
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    return df


def get_schema_description(df):
    """
    Generate schema description for the LLM.
    """
    schema = f"""
DataFrame Schema (variable name: df):
- Total Records: {len(df)}
- Columns: {', '.join(df.columns.tolist())}

Column Details:
"""
    for col in df.columns:
        dtype = df[col].dtype
        if dtype == 'object':
            unique_vals = df[col].nunique()
            sample = df[col].dropna().head(3).tolist()
            schema += f"- {col}: text (unique values: {unique_vals}, examples: {sample})\n"
        elif dtype in ['int64', 'float64']:
            schema += f"- {col}: number (min: {df[col].min()}, max: {df[col].max()}, avg: {df[col].mean():.2f})\n"
        else:
            schema += f"- {col}: {dtype}\n"

    return schema
