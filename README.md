# CSAS to SharePoint Statement Uploader

![Logo](csas-sharepoint.svg?raw=true)

This project provides a Python application to automate the process of downloading bank statements from Česká spořitelna (CSAS) and uploading them to SharePoint with comprehensive reporting and result management.

## Features

- **Automated Bank Statement Processing**: Download bank statements using [csas-statement-tools](https://github.com/VitexSoftware/csas-statement-tools)
- **SharePoint Integration**: Upload statements to SharePoint using [file2sharepoint](https://github.com/VitexSoftware/file2sharepoint)
- **Comprehensive Reporting**: Generates detailed reports conforming to the MultiFlexi report schema
- **Result File Management**: Captures and preserves detailed information from both download and upload operations
- **Robust Error Handling**: UTF-8 encoding issues resolved, graceful handling of missing/malformed data
- **Command-line Interface**: Easy automation with flexible configuration options
- **Comprehensive Logging**: Debug and operational logging with configurable levels
- **MultiFlexi Framework**: Fully compatible with the MultiFlexi automation platform
- **Schema Validation**: Reports validate against the official MultiFlexi report schema

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

⚠️ **CRITICAL**: ČSAS access tokens expire after only 5 minutes! Always run `make token` to refresh the token before testing or using the application.

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

# Result File (optional) - MultiFlexi compatible JSON report
RESULT_FILE=report.json

# Debug Settings
DEBUG=true
APP_DEBUG=true
EASE_LOGGER=console
```

### Token Management

⚠️ **IMPORTANT**: ČSAS access tokens are valid for only 5 minutes!

```bash
# Refresh CSAS access token before any operations
make token

# This updates the CSAS_ACCESS_TOKEN in your .env file
# Always run this immediately before testing or using the application
```

**Token Refresh Workflow:**
1. Run `make token` to get a fresh 5-minute token
2. Immediately run your tests or application
3. If you get authentication errors, run `make token` again

## Usage

### Using the Installed Application

Basic usage:

```bash
csas-sharepoint
```

With custom options:

```bash
csas-sharepoint --format pdf --scope last_month --sharepoint-path "statements/2024"
```

### Using the Source Code

```bash
python3 src/main.py --format pdf --scope yesterday --sharepoint-path "Shared Documents/"
```

### Command Line Arguments

- `-f, --format` - Statement format (default: pdf)
  - Available: pdf, xml, abo-standard, csv-comma, mt940
- `-s, --scope` - Time scope for statements
  - Available: yesterday, current_month, last_month, last_two_months
- `-p, --sharepoint-path` - Target path in SharePoint
- `-t, --temp-dir` - Temporary directory for downloads
- `--no-cleanup` - Do not cleanup temporary files

## Result Reporting

The application generates comprehensive reports that conform to the [MultiFlexi report schema](https://raw.githubusercontent.com/VitexSoftware/php-vitexsoftware-multiflexi-core/refs/heads/main/multiflexi.report.schema.json).

### Report Structure

When `RESULT_FILE` is specified in the environment, the application generates a detailed JSON report:

```json
{
  "status": "success|warning|error",
  "timestamp": "2025-09-19T10:16:51+02:00",
  "message": "Human readable status message",
  "artifacts": {
    "downloaded_statements": ["file1.pdf", "file2.pdf"],
    "uploaded_statements": ["https://sharepoint.com/file1.pdf"]
  },
  "metrics": {
    "files_downloaded": 2,
    "upload_attempts": 2,
    "successful_uploads": 2,
    "download_success": "true"
  },
  "download_details": {
    "source": "download",
    "success": true,
    "data": { /* Complete csas-statement-downloader report */ }
  },
  "upload_details": [
    {
      "source": "upload", 
      "success": true,
      "data": { /* Complete file2sharepoint report */ }
    }
  ],
  "csas_downloader_report": { /* Direct access to downloader data */ },
  "file2sharepoint_reports": [ /* Per-file SharePoint reports */ ]
}
```

### Report Features

- **MultiFlexi Schema Compliance**: All reports validate against the official schema
- **Detailed Tool Reports**: Preserves complete output from `csas-statement-downloader` and `file2sharepoint`
- **Status Determination**: Intelligent status assignment based on operation outcomes
- **Comprehensive Metrics**: File counts, success rates, timing information
- **Artifact Management**: Lists of downloaded files and SharePoint URLs
- **Error Handling**: Graceful handling of missing or malformed data

### Status Levels

- **`success`**: All operations completed successfully
- **`warning`**: Partial success (e.g., download successful but some uploads failed, or no statements available)
- **`error`**: Critical failure (e.g., download failed)

### Validating Reports

You can validate generated reports against the MultiFlexi schema:

```bash
# Using the included validation script
python3 validate_report.py report.json

# Or using external tools
jsonschema -i report.json https://raw.githubusercontent.com/VitexSoftware/php-vitexsoftware-multiflexi-core/refs/heads/main/multiflexi.report.schema.json
```

## Testing

Run unit tests with:

```bash
python3 -m unittest discover tests -v
```

### Testing Result Processing

You can test the result processing functionality with mock data:

```bash
python3 test_result_loading.py
```

### Testing with Debug Mode

Enable debug logging to see detailed operation information:

```bash
DEBUG=true csas-sharepoint -f pdf -s yesterday -p "test/"
```

## Troubleshooting

### Common Issues

1. **UTF-8 Encoding Errors**: The application now handles UTF-8 encoding issues gracefully. If you encounter encoding problems, ensure your `.env` file uses proper UTF-8 encoding.

2. **Missing Dependencies**: Ensure both `csas-statement-downloader` and `file2sharepoint` are installed and accessible in your PATH.

3. **Authentication Issues**: Verify your CSAS API credentials and Office 365 configuration.

4. **No Statements Available**: This is normal and results in a `warning` status. Check the date scope and ensure statements exist for the requested period.

### Debug Information

Enable comprehensive logging:

```bash
export DEBUG=true
export APP_DEBUG=true
export EASE_LOGGER=console
```

## Project Structure

```
src/main.py                           # Main application with enhanced result management
tests/test_main.py                    # Unit tests
test_result_loading.py                # Test script for result processing functionality
validate_report.py                    # MultiFlexi report schema validation script
multiflexi/csas-sharepoint.app.json   # MultiFlexi configuration
debian/                               # Debian packaging files
.env                                  # Configuration file (create from template)
README.md                             # This documentation
```

## MultiFlexi

CSas to Sharepoint is ready for run as [MultiFlexi](https://multiflexi.eu) application.
See the full list of ready-to-run applications within the MultiFlexi platform on the [application list page](https://www.multiflexi.eu/apps.php).

[![MultiFlexi App](https://github.com/VitexSoftware/MultiFlexi/blob/main/doc/multiflexi-app.svg)](https://www.multiflexi.eu/apps.php)

## Changelog

### Latest Version

- ✅ **Enhanced Result Reporting**: Comprehensive reports conforming to MultiFlexi schema
- ✅ **Result File Management**: Captures detailed information from both `csas-statement-downloader` and `file2sharepoint`
- ✅ **UTF-8 Encoding Fix**: Resolved UTF-8 decoding issues when reading configuration files
- ✅ **Robust Error Handling**: Graceful handling of missing/malformed data and tool failures
- ✅ **Schema Validation**: Built-in validation against MultiFlexi report schema
- ✅ **Backup System**: Individual result files are backed up for each operation
- ✅ **Status Intelligence**: Smart status determination based on operation outcomes
- ✅ **Comprehensive Logging**: Enhanced debug logging with configurable levels
- ✅ **Artifact Management**: Proper tracking of downloaded files and SharePoint URLs

### Previous Versions

- Basic CSAS statement download and SharePoint upload functionality
- MultiFlexi framework integration
- Command-line interface
- Environment-based configuration

## License

MIT

## Author

VitexSoftware, Spoje-NET
