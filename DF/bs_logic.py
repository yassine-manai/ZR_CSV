import pandas as pd
import os

def load_file_headers(path):
    if not os.path.exists(path):
        return None, "File does not exist."

    try:
        if path.lower().endswith('.csv'):
            df = pd.read_csv(path)
        elif path.lower().endswith('.psv'):
            df = pd.read_csv(path, sep='|')
        else:
            return None, "Unsupported file format. Please use a .csv or .psv file."
        
        headers = df.columns.tolist()
        return headers, None
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def load_file_columns(path):
    if not os.path.exists(path):
        return None, "File does not exist."

    try:
        if path.lower().endswith('.csv'):
            df = pd.read_csv(path, nrows=1)
        elif path.lower().endswith('.psv'):
            df = pd.read_csv(path, sep='|', nrows=1)
        else:
            return None, "Unsupported file format. Please use a .csv or .psv file."
        
        if df.empty:
            return None, "The file appears to be empty."
        return [f"Column {i+1}" for i in range(len(df.columns))], None
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def get_column_data(file_path, *column_indices):
    try:
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith('.psv'):
            df = pd.read_csv(file_path, sep='|')
        else:
            return None, "Unsupported file format. Please use a .csv or .psv file."
        
        selected_columns = df.iloc[:, list(column_indices)]
        return selected_columns, None
    except Exception as e:
        return None, str(e)