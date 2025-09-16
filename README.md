# CSAS to SharePoint Statement Uploader

This project provides a Python application to automate the process of downloading bank statements from Česká spořitelna (CSAS) and uploading them to SharePoint.

## Features

- Download bank statements using [csas-statement-tools](https://github.com/VitexSoftware/csas-statement-tools)
- Upload statements to SharePoint using [file2sharepoint](https://github.com/VitexSoftware/file2sharepoint)
- Command-line interface for easy automation
- Error handling and comprehensive logging
- Unit tests included
- MultiFlexi framework compatible

## Requirements

- Python 3.13+
- `csas-statement-tools` (system package)
- `file2sharepoint` (system package)

## Installation

The required tools are available as Debian packages:

```bash
echo "deb http://repo.vitexsoftware.com $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/vitexsoftware.list
sudo wget -O /etc/apt/trusted.gpg.d/vitexsoftware.gpg http://repo.vitexsoftware.com/keyring.gpg
sudo apt update
sudo apt install csas-sharepoint
```

## Configuration

Create a `.env` file with the required configuration:

```bash
# CSAS Configuration
CSAS_API_KEY=your-api-key
CSAS_ACCESS_TOKEN=your-access-token
CSAS_ACCOUNT_IBAN=CZ0000000000000000000000

# CSAS Settings
CSAS_STATEMENT_SCOPE=last_month

# Office 365 / SharePoint Configuration
OFFICE365_TENANT=yourcompany
OFFICE365_SITE=yoursite

# Office 365 Authentication (choose one method)
# Method 1: Username/Password
OFFICE365_USERNAME=user@yourcompany.onmicrosoft.com
OFFICE365_PASSWORD=your-password

# Method 2: Client Credentials (recommended)
# OFFICE365_CLIENTID=your-client-id
# OFFICE365_CLSECRET=your-client-secret

# SharePoint Library/Path
SHAREPOINT_LIBRARY=Documents
OFFICE365_PATH=bank-statements

# Debug Settings
DEBUG=true
```

## Usage

Basic usage:

```bash
python3 src/main.py
```

With custom options:

```bash
python3 src/main.py --format pdf --scope last_month --sharepoint-path "statements/2024"
```

### Command Line Arguments

- `-f, --format` - Statement format (default: pdf)
  - Available: pdf, xml, abo-standard, csv-comma, mt940
- `-s, --scope` - Time scope for statements
  - Available: yesterday, current_month, last_month, last_two_months
- `-p, --sharepoint-path` - Target path in SharePoint
- `-t, --temp-dir` - Temporary directory for downloads
- `--no-cleanup` - Do not cleanup temporary files

## Testing

Run unit tests with:

```bash
python3 -m unittest discover tests -v
```

## Project Structure

```
src/main.py                  # Main application
tests/test_main.py           # Unit tests
multiflexi/csas-sharepoint.app.json  # MultiFlexi configuration
debian/                      # Debian packaging files
```

## MultiFlexi

CSas to Sharepoint is ready for run as [MultiFlexi](https://multiflexi.eu) application.
See the full list of ready-to-run applications within the MultiFlexi platform on the [application list page](https://www.multiflexi.eu/apps.php).

[![MultiFlexi App](https://github.com/VitexSoftware/MultiFlexi/blob/main/doc/multiflexi-app.svg)](https://www.multiflexi.eu/apps.php)


## License

MIT

## Author

VitexSoftware, Spoje-NET
