import boto3
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_user_email(cognito_client, user_pool_id, user_id):
    try:
        response = cognito_client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=user_id
        )
        for attr in response['UserAttributes']:
            if attr['Name'] == 'email':
                return attr['Value']
        return None
    except cognito_client.exceptions.UserNotFoundException:
        print("User not found")
        return None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None


# Function to extract user IDs from file names in logReports
def extract_user_ids_from_filenames(directory):
    user_ids = []
    for filename in os.listdir(directory):
        match = re.search(r'report_([a-zA-Z0-9\-]+)_sample', filename)
        if match:
            user_ids.append(match.group(1))
    return user_ids

# Usage
region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')  # Default to 'us-east-1' if not specified
client = boto3.client('cognito-idp', region_name=region)
user_pool_id = os.getenv('COGNITO_USER_POOL_ID')

log_reports_directory = 'logReports'  # Adjust the path if necessary
user_ids = extract_user_ids_from_filenames(log_reports_directory)

for user_id in user_ids:
    email = get_user_email(client, user_pool_id, user_id)
    if email:
        print(f"Email for user ID {user_id}: {email}")
    else:
        print(f"Email not found for user ID {user_id}")