import boto3
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to get user email from Cognito
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

# Function to send email
def send_email(toaddr, subject, body, attachment_path=None):
    fromaddr = "your_email@example.com"  # Sender's email address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Add attachment if provided
    if attachment_path:
        filename = os.path.basename(attachment_path)
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={filename}")
        msg.attach(part)

    # SMTP configuration
    server = smtplib.SMTP('smtp.example.com', 587)  # SMTP server address and port
    server.starttls()
    server.login(fromaddr, "YourPassword")  # Sender's email password
    text = msg.as_string()

    # Send the email
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# Function to extract user IDs from file names in logReports
def extract_user_ids_from_filenames(directory):
    user_ids = []
    for filename in os.listdir(directory):
        match = re.search(r'report_([a-zA-Z0-9\-]+)_sample', filename)
        if match:
            user_ids.append(match.group(1))
    return user_ids

# Main flow
def main():
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    client = boto3.client('cognito-idp', region_name=region)
    user_pool_id = os.getenv('COGNITO_USER_POOL_ID')

    log_reports_directory = 'logSend'  # Adjust the path if necessary
    user_ids = extract_user_ids_from_filenames(log_reports_directory)

    for user_id in user_ids:
        email = get_user_email(client, user_pool_id, user_id)
        if email:
            print(f"Sending email to user ID {user_id} at {email}")
            # Here you can define the subject and body of your email, or make them dynamic
            send_email(email, "Subject of the Mail", "This is the body of the email")
        else:
            print(f"Email not found for user ID {user_id}")

if __name__ == "__main__":
    main()
