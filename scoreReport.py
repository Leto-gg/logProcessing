import pandas as pd
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_cuckoo_score(task_id):
    """
    Retrieve the analysis score for a given task ID from the Cuckoo Sandbox API.
    """
    cuckoo_api_url = f"http://localhost:8090/tasks/report/{task_id}"  # Adjust as needed
    api_token = os.getenv('CUCKOO_API_TOKEN')  # Get API token from .env file

    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    try:
        print(f"Retrieving score for Task ID: {task_id}")
        response = requests.get(cuckoo_api_url, headers=headers)
        if response.status_code == 200:
            report_data = response.json()
            # Extract the score from report data; adjust the key as per your report structure
            return report_data.get('info', {}).get('score')
        else:
            print(f"Failed to get score for Task ID {task_id}: HTTP {response.status_code}")
    except requests.RequestException as e:
        print(f"Request error while fetching score for Task ID {task_id}: {e}")
    return None

def update_report_with_scores(input_directory):
    for report_file in os.listdir(input_directory):
        if report_file.endswith('.csv'):
            report_path = os.path.join(input_directory, report_file)
            
            # Read the report CSV file without assuming headers
            report_data = pd.read_csv(report_path, header=None)
            updated_rows = []

            for index, row in report_data.iterrows():
                # Assuming that the URL and Task ID are in the last two elements
                if len(row) < 2:
                    print(f"Invalid format in file {report_file}, row {index + 1}")
                    updated_row = row.tolist()
                else:
                    url, task_id = row.iloc[-2], row.iloc[-1]

                    # Check if task_id is a valid number
                    if pd.isna(task_id) or not str(task_id).isdigit():
                        print(f"Invalid or missing Task ID in file {report_file}, row {index + 1}")
                        updated_row = row.tolist()
                    else:
                        score = get_cuckoo_score(task_id)
                        # Append the score to the row
                        updated_row = row.tolist() + [score]

                updated_rows.append(updated_row)

            # Write the updated rows back to the CSV file
            updated_report = pd.DataFrame(updated_rows)
            updated_report.to_csv(report_path, index=False, header=False)

# Example usage
log_reports_directory = 'logReports'
update_report_with_scores(log_reports_directory)