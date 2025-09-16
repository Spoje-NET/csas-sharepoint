# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python application that automates downloading bank statements from Česká spořitelna (CSAS) and uploading them to SharePoint. The project is set up as a MultiFlexi-compatible application with Debian packaging support.

## Architecture

### Core Components
- **Main Application**: `src/main.py` - Currently contains a basic template that needs to be replaced with the actual CSAS-SharePoint integration logic
- **MultiFlexi Integration**: `multiflexi/csas-sharepoint.app.json` - Configuration schema for MultiFlexi framework integration
- **Debian Packaging**: `debian/` directory contains complete Debian package configuration
- **Testing Framework**: `tests/` directory set up for unit tests

### Key Dependencies and APIs
The application is designed to work with:
- CSAS Banking API (requires API key, access token, account details)
- Office 365 SharePoint API (requires OAuth credentials and site configuration)
- MultiFlexi framework for application deployment and configuration

### Configuration Schema
The application follows MultiFlexi configuration patterns with these environment variables:
- CSAS API credentials: `CSAS_API_KEY`, `CSAS_ACCESS_TOKEN`, `CSAS_ACCOUNT_UUID`, `CSAS_ACCOUNT_IBAN`
- SharePoint credentials: `OFFICE365_USERNAME`, `OFFICE365_PASSWORD`, `OFFICE365_CLIENTID`, etc.
- Debug settings: `DEBUG`, `APP_DEBUG`, `EASE_LOGGER`

## Development Commands

### Environment Setup
```bash
# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt

# Or using the current pyproject.toml setup
pip install -e .
```

### Running the Application
```bash
# Run main application
python3 src/main.py

# Run with MultiFlexi configuration
python3 src/main.py  # Uses environment variables from MultiFlexi
```

### Testing
```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_module_name
```

### CSAS Token Management
```bash
# Refresh CSAS access token (requires csas-statement-tools)
make token
```

### Docker Operations
```bash
# Build Docker image
make buildimage

# Build multi-platform image and push
make buildx

# Run containerized application
make drun
```

### Debian Package Development
```bash
# Build Debian package
debuild -us -uc

# Clean build artifacts
debian/rules clean
```

## Code Standards

All code must follow these guidelines from the project's Copilot instructions:
- Write all code comments and messages in English
- Include docblocks for all functions and classes with purpose, parameters, and return types
- Use type hints for function parameters and return types
- Use meaningful variable names and avoid magic numbers/strings
- Always create/update unit tests when creating/updating classes
- Handle exceptions properly with meaningful error messages
- Ensure compatibility with the latest Python version

## Schema Compliance

- MultiFlexi app configurations in `multiflexi/*.app.json` must conform to: https://raw.githubusercontent.com/VitexSoftware/php-vitexsoftware-multiflexi-core/refs/heads/main/multiflexi.app.schema.json
- All produced reports must conform to: https://raw.githubusercontent.com/VitexSoftware/php-vitexsoftware-multiflexi-core/refs/heads/main/multiflexi.report.schema.json

## Build System

The project uses:
- **Python**: pyproject.toml for Python packaging (requires Python 3.13+)
- **Make**: Makefile for common development tasks
- **Debian**: Complete debian/ packaging configuration
- **Docker**: Multi-platform container builds
- **CI/CD**: Salsa CI for Debian packaging, Dependabot for dependency updates