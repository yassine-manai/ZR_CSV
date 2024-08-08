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
                next(reader, None)  
            first_row = next(reader, None)
            if first_row:
                return [f"Column {i+1}" for i in range(15)], None
            else:
                return None, "The file appears to be empty."
    except csv.Error:
        return None, "Failed to read the file. Please ensure it's a valid CSV or PSV file."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"



""" def get_column_data(path, *column_indices):
    try:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader) 
            data = []
            for row in reader:
                data.append([row[i] for i in column_indices])
        return data, None
    except Exception as e:
        return None, str(e) """
    
    

def get_columns_data(path, *columns):
    if not os.path.exists(path):
        return None, "File does not exist."
    
    try:
        # Determine the delimiter based on the file extension
        if path.lower().endswith('.csv'):
            delimiter = ','
        elif path.lower().endswith('.psv'):
            with open(path, 'r') as file:
                first_line = file.readline()
                delimiter = '|' if '|' in first_line else ';'
        else:
            return None, "Unsupported file format. Please use a .csv or .psv file."
        
        with open(path, 'r') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            
            # Check if the columns exist in the file
            missing_columns = [col for col in columns if col not in reader.fieldnames]
            if missing_columns:
                return None, f"Missing columns: {', '.join(missing_columns)}"
            
            data = [list(row[col] for col in columns) for row in reader]  # Convert to list
            print(type(data))
            print(f"{data}")
            return data, None
    except csv.Error:
        return None, "Failed to read the file. Please ensure it's a valid CSV or PSV file."
    except Exception as e:
        return None, f"An error occurred: {str(e)}" 


def get_column_data(file_path, *column_indices):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip the header row if present
            data = []
            for row in reader:
                data.append([row[i] for i in column_indices if i < len(row)])
        return data, None
    except Exception as e:
        return None, str(e)