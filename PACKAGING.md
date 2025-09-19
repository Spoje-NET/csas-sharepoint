# CSAS-SharePoint Debian Packaging

## Package Information

- **Package Name**: csas-sharepoint
- **Version**: 1.1.0
- **Architecture**: all
- **Section**: utils

## Enhanced Features in v1.1.0

### New Functionality
- ✅ Enhanced Result Reporting with MultiFlexi schema compliance
- ✅ Result File Management with detailed operation tracking
- ✅ UTF-8 Encoding fixes for configuration files
- ✅ Robust Error Handling for missing/malformed data
- ✅ Schema Validation capabilities
- ✅ Backup System for result files
- ✅ Status Intelligence with smart determination
- ✅ Comprehensive Logging with configurable debug levels
- ✅ Artifact Management for file and URL tracking

### New Utilities
- ✅ `validate_report.py` - MultiFlexi schema validation
- ✅ `test_result_loading.py` - Result processing testing
- ✅ Wrapper scripts for convenient command-line access

## Installed Files

### Executables
```
/usr/bin/csas-sharepoint                    # Main application (symlink)
/usr/bin/csas-sharepoint-validate          # Report validation utility
/usr/bin/csas-sharepoint-test              # Result processing test
```

### Libraries
```
/usr/lib/csas-sharepoint/main.py           # Main application script
/usr/lib/csas-sharepoint/validate_report.py # Validation utility
/usr/lib/csas-sharepoint/test_result_loading.py # Test utility
```

### Documentation
```
/usr/share/doc/csas-sharepoint/README.md   # Comprehensive documentation
/usr/share/man/man1/csas-sharepoint.1      # Man page
/usr/share/doc/csas-sharepoint/changelog   # Version history
```

### MultiFlexi Integration
```
/usr/lib/multiflexi/apps/csas-sharepoint.app.json # MultiFlexi configuration
```

## Dependencies

### Build Dependencies
- debhelper-compat (>= 13)
- python3
- python3-setuptools  
- python3-jsonschema

### Runtime Dependencies
- python3
- python3-jsonschema
- csas-statement-tools
- file2sharepoint

### Recommended
- multiflexi

## Package Scripts

### postinst
- Makes all Python scripts executable
- Ensures proper permissions for wrapper scripts
- No manual symlink creation (handled by packaging)

### postrm
- Cleanup handled automatically by dpkg
- No manual cleanup required for packaged files

## Building the Package

```bash
# Build the package
dpkg-buildpackage -us -uc

# Install the package
sudo dpkg -i ../csas-sharepoint_1.1.0_all.deb

# Install dependencies if needed
sudo apt-get install -f
```

## Package Testing

```bash
# Test main functionality
csas-sharepoint --help

# Test validation utility
csas-sharepoint-validate --help

# Test result processing
csas-sharepoint-test

# View man page
man csas-sharepoint
```

## Changelog Highlights

### v1.1.0 (Latest)
- Comprehensive result reporting with MultiFlexi schema compliance
- Enhanced error handling and UTF-8 encoding support
- Added validation and testing utilities
- Improved documentation and man page
- Backup system for operation results
- Smart status determination and metrics

### v1.0.0
- Initial MultiFlexi integration release
- Basic CSAS to SharePoint automation

### v0.1.0-1
- Initial release
- Core download and upload functionality
- Command-line interface
- Basic error handling and logging

## Package Verification

The package includes comprehensive functionality:
- ✅ Main application with enhanced features
- ✅ Validation utilities for MultiFlexi compliance  
- ✅ Test utilities for development and troubleshooting
- ✅ Complete documentation including man page
- ✅ MultiFlexi framework integration
- ✅ Proper dependency management
- ✅ Clean installation and removal

## Schema Compliance

All generated reports validate against:
```
https://raw.githubusercontent.com/VitexSoftware/php-vitexsoftware-multiflexi-core/refs/heads/main/multiflexi.report.schema.json
```

Use the included `csas-sharepoint-validate` command to verify report compliance.