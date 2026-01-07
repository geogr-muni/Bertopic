import pandas as pd
from typing import Union, List

def load_data(data:Union[str,pd.DataFrame]):
    """
    Helper function to load data from a file path or a DataFrame.
    """
    if isinstance(data, pd.DataFrame):
        return data.copy()
    
    if data.endswith('.csv'):
        return pd.read_csv(data)
    elif data.endswith(('.xls', '.xlsx')):
        return pd.read_excel(data)
    raise TypeError("data must be a file path or a pandas DataFrame")

def duplicates(data:Union[str,pd.DataFrame] ,target_columns:List[str]):
    """
    Label the duplicate if it appears in any of the target col.
    Args:
        data (Union[str, pd.DataFrame]): The file path (.csv, .xlsx, xls) or DataFrame.
        target_columns (List[str]): A list of column names to check for duplicates.

    Returns:
        pd.DataFrame: The DataFrame with an added 'duplicate' column.
    """
    df = load_data(data)
    
    df['duplicate'] = False # Need another col to indicate if duplicate
    
    for col in target_columns:
        dup = df[col].dropna().astype(str).str.strip().str.lower().duplicated() & df[col].notnull()
        df['duplicate'] = df['duplicate'] | dup

    return df

def keywords(data: Union[str, pd.DataFrame], search_columns: List[str], keywords: List[str]):
    """
    Check if the provided keyworks appear in cols of a dataframe
    
    Args:
        data (Union[str, pd.DataFrame]): The file path (.csv, .xlsx) or DataFrame.
        search_columns (List[str]): List of column names to search within.
        keywords (List[str]): List of keywords to search for.

    Returns:
        pd.DataFrame: DataFrame with new boolean columns for each keyword.
    """
    df = load_data(data)
    
    df[keywords] = False
    for col in search_columns:
        for keyword in keywords:
            df[keyword] = df[col].str.lower().str.contains(keyword,regex=False) | df[keyword]
    
    return df
    
