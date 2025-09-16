# csas-sharepoint

This project automates the process of downloading bank statements from Česká spořitelna in ABO format and uploading them to SharePoint.

## Prerequisites
- Python 3.x
- Installed CLI tools:
  - `csas-statement-downloader` (from [csas-statement-tools](https://github.com/VitexSoftware/csas-statement-tools))
  - `file2sharepoint` (from [file2sharepoint](https://github.com/VitexSoftware/file2sharepoint))
- Properly configured `.env` file with credentials for both Česká spořitelna API and SharePoint (see the documentation of the respective tools).

## Usage
1. Edit `csas2sharepoint.py` and set the correct paths for your `.env` file and SharePoint folder.
2. Run the script:
   ```bash
   python3 csas2sharepoint.py
   ```
   - The script will download ABO statements to the `statements/` directory and upload all `.abo` files to SharePoint.

## Configuration
- `.env` file must contain all required variables for both tools. See:
  - [csas-statement-tools configuration](https://github.com/VitexSoftware/csas-statement-tools#configuration)
  - [file2sharepoint configuration](https://github.com/VitexSoftware/file2sharepoint#configuration)

## References
- [csas-statement-tools](https://github.com/VitexSoftware/csas-statement-tools)
- [file2sharepoint](https://github.com/VitexSoftware/file2sharepoint)

## License
See LICENSE of the referenced projects.
