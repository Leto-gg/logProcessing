import pandas as pd
import re
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

def list_csv_files(directory):
    """List all CSV files in the given directory."""
    return [f for f in os.listdir(directory) if f.endswith('.csv')]

def extract_urls_from_csv(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)

    # Regular expression for matching URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # List to store URLs
    urls = []

    # Iterate over each cell in the DataFrame
    for _, row in data.iterrows():
        for item in row:
            # Find all URLs in the current cell and add them to the list
            found_urls = re.findall(url_pattern, str(item))
            urls.extend(found_urls)

    return urls

def submit_url_to_cuckoo(url):
    command = ["cuckoo", "submit", "--url", url]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully submitted URL: {url}")
            print(result.stdout)
            return extract_task_id_from_result(result.stdout)
        else:
            print(f"Error submitting URL: {url}")
            print(result.stderr)
            return None
    except Exception as e:
        print(f"Exception occurred while submitting URL: {e}")
        return None

def extract_task_id_from_result(result):
    # Regular expression to match 'task with ID #<number>'
    match = re.search(r"task with ID #(\d+)", result)
    if match:
        # Extract and return the task ID
        return int(match.group(1))
    else:
        print("Task ID not found in the output.")
        return None

def process_logs(input_directory, output_directory):
    for csv_file in list_csv_files(input_directory):
        file_path = os.path.join(input_directory, csv_file)
        urls = extract_urls_from_csv(file_path)

        task_ids = []
        for url in urls:
            task_id = submit_url_to_cuckoo(url)
            if task_id is not None:
                print(f"Task ID for URL {url}: {task_id}")
                task_ids.append(task_id)

        # Write task IDs to corresponding file in logReports folder
        report_file_path = os.path.join(output_directory, f"report_{csv_file}")
        with open(report_file_path, 'a') as f:
            for task_id in task_ids:
                f.write(f"{task_id}\n")

# Example usage
input_directory = 'logs'
output_directory = 'logReports'
process_logs(input_directory, output_directory)
