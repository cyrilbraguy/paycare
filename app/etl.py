import pandas as pd

# Step 1: Extract
def extract_data(file_path):
    """Extracts data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        print("Data extraction successful.")
        return data
    except Exception as e:
        print(f"Error in data extraction: {e}")
        return None

# Step 2: Transform
def transform_data(data):
    """Transforms the data by cleaning and adding new features."""
    try:
        # Drop rows with missing values
        data_cleaned = data.dropna()
        
        # Add a new column for Tax (assuming a flat 10% tax rate on salary)
        data_cleaned['tax'] = data_cleaned['salary'] * 0.1
        
        # Calculate net salary after tax
        data_cleaned['net_salary'] = data_cleaned['salary'] - data_cleaned['tax']
        
        print("Data transformation successful.")
        return data_cleaned
    except Exception as e:
        print(f"Error in data transformation: {e}")
        return None

# Step 3: Load
def load_data(data, output_file_path):
    """Loads the transformed data into a new CSV file."""
    try:
        data.to_csv(output_file_path, index=False)
        print(f"Data loaded successfully to {output_file_path}.")
    except Exception as e:
        print(f"Error in data loading: {e}")

# Main ETL function
def etl_process(input_file, output_file):
    data = extract_data(input_file)
    if data is not None:
        transformed_data = transform_data(data)
        if transformed_data is not None:
            load_data(transformed_data, output_file)

if __name__ == "__main__":
    input_file = 'input_data.csv'
    output_file = 'output_data.csv'
    etl_process(input_file, output_file)