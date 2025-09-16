# Created on : Sep 16, 2025, 10:43:48 AM
# Author     : Vítězslav Dvořák <info@vitexsoftware.cz>

"""
Main script for downloading ABO-standard statements from Česká spořitelna and uploading them to SharePoint.

Configuration is read from .env file in the project root.
"""
import os
import subprocess
import glob
from dotenv import load_dotenv

# Load configuration from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

STATEMENTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'statements')
STATEMENT_FORMAT = os.getenv('STATEMENT_FORMAT', 'abo-standard')
CSAS_API_KEY = os.getenv('CSAS_API_KEY')
CSAS_ACCESS_TOKEN = os.getenv('CSAS_ACCESS_TOKEN')
CSAS_ACCOUNT_UUID = os.getenv('CSAS_ACCOUNT_UUID')
CSAS_ACCOUNT_IBAN = os.getenv('CSAS_ACCOUNT_IBAN')
CSAS_STATEMENT_SCOPE = os.getenv('CSAS_STATEMENT_SCOPE', 'yesterday')
ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')

OFFICE365_TENANT = os.getenv('OFFICE365_TENANT')
OFFICE365_SITE = os.getenv('OFFICE365_SITE')
OFFICE365_PATH = os.getenv('OFFICE365_PATH').strip("'")

# Step 1: Download statements
os.makedirs(STATEMENTS_DIR, exist_ok=True)
print(f"Downloading statements to {STATEMENTS_DIR}...")
download_cmd = [
    "csas-statement-downloader",
    STATEMENTS_DIR,
    "abo-standard",
    ENV_PATH
]
result = subprocess.run(download_cmd, capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("Error downloading statements:", result.stderr)
    exit(result.returncode)

# Step 2: Parse report to get list of downloaded files
abo_files = glob.glob(os.path.join(STATEMENTS_DIR, "*.abo"))
if not abo_files:
    print("No ABO-standard files found for upload.")
    exit(1)
print(f"Found {len(abo_files)} ABO files for upload.")

# Step 3: Upload files to SharePoint
upload_cmd = [
    "file2sharepoint",
    f"{STATEMENTS_DIR}/*.abo",
    OFFICE365_PATH,
    ENV_PATH
]
print(f"Uploading ABO files to SharePoint folder: {OFFICE365_PATH}")
result = subprocess.run(upload_cmd, capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("Error uploading files:", result.stderr)
    exit(result.returncode)

print("All ABO-standard files uploaded successfully.")
# Created on : Sep 16, 2025, 10:43:48 AM
# Author     : Vítězslav Dvořák <info@vitexsoftware.cz>


# This is a sample Python script.

# Press Shift+F6 to execute it or replace it with your code.


def print_hi(name):
    print(f"Hi, {name}")


if __name__ == "__main__":
    print_hi("Netbeans")
