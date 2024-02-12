import os
import csv

def list_csv_files(directory):
    """List all CSV files in the given directory."""
    return [f for f in os.listdir(directory) if f.endswith('.csv')]

def read_csv(file_path):
    """Read a CSV file and return its contents."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def process_data(data):
    """Process the data by adding an extra comma (empty field) to each row."""
    processed_data = []
    for row in data:
        # Add an empty field to the end of each row
        modified_row = row + ['']
        processed_data.append(modified_row)
    return processed_data

def write_csv(file_path, data):
    """Write data to a CSV file."""
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def process_folder(input_folder, output_folder):
    """Process all CSV files in the input folder and save them in the output folder."""
    for csv_file in list_csv_files(input_folder):
        input_path = os.path.join(input_folder, csv_file)
        # Add 'report' prefix to the output filename
        output_file_name = f"report_{csv_file}"
        output_path = os.path.join(output_folder, output_file_name)

        data = read_csv(input_path)
        processed_data = process_data(data)
        write_csv(output_path, processed_data)

# Example usage
input_directory = 'logs'
output_directory = 'logReports'
process_folder(input_directory, output_directory)
