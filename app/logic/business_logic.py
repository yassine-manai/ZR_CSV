import csv
import os

def load_file_headers(path):
    if not os.path.exists(path):
        return None, "File does not exist."

    try:
        delimiter = ',' if path.lower().endswith('.csv') else '|' or ';'
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            if path.lower().endswith('.PSV'):
                next(reader, None)  
            headers = next(reader, None)
            return headers, None
    except csv.Error:
        return None, "Failed to read the file. Please ensure it's a valid CSV or PSV file."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def load_file_columns(path):
    if not os.path.exists(path):
        return None, "File does not exist."

    try:
        delimiter = ',' if path.lower().endswith('.csv') else '|' or ';'
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            if path.lower().endswith('.PSV'):
                next(reader, None)  # Skip the first row for PSV files
            first_row = next(reader, None)
            if first_row:
                return [f"Column {i+1}" for i in range(15)], None
            else:
                return None, "The file appears to be empty."
    except csv.Error:
        return None, "Failed to read the file. Please ensure it's a valid CSV or PSV file."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def get_column_data(path, column1, column2):
    if not os.path.exists(path):
        return None, "File does not exist."

    try:
        delimiter = ',' if path.lower().endswith('.csv') else '|' or ';'
        with open(path, 'r') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            data = [(row[column1], row[column2]) for row in reader]
            return data, None
    except csv.Error:
        return None, "Failed to read the file. Please ensure it's a valid CSV or PSV file."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"