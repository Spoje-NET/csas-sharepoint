#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSAS to SharePoint Statement Uploader

This application automates the process of:
1. Downloading bank statements from Česká spořitelna (CSAS)
2. Uploading them to SharePoint

Author: Vítězslav Dvořák <info@vitexsoftware.cz>
Created: Sep 16, 2025
"""

import os
import sys
import subprocess
import tempfile
import glob
import logging
from pathlib import Path
from typing import List, Optional
import argparse


class CSASSharePointUploader:
    """
    Orchestrates CSAS statement download and SharePoint upload.
    """
    
    def __init__(self, temp_dir: Optional[str] = None):
        """
        Initialize the uploader.
        
        Args:
            temp_dir: Optional temporary directory for downloaded files
        """
        self.logger = self._setup_logging()
        self.temp_dir = temp_dir or tempfile.mkdtemp(prefix='csas_statements_')
        self.downloaded_files: List[str] = []
        
        # Ensure temp directory exists
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Using temporary directory: {self.temp_dir}")
    
    def _setup_logging(self) -> logging.Logger:
        """
        Set up logging configuration.
        
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger('CSASSharePointUploader')
        
        # Check if logger already has handlers to avoid duplicates
        if not logger.handlers:
            level = logging.DEBUG if os.getenv('DEBUG', '').lower() == 'true' else logging.INFO
            logger.setLevel(level)
            
            # Create console handler
            handler = logging.StreamHandler()
            handler.setLevel(level)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            
            logger.addHandler(handler)
        
        return logger
    
    def _check_environment(self) -> bool:
        """
        Check if required environment variables are set.
        
        Returns:
            True if all required variables are present
        """
        required_csas = ['CSAS_API_KEY', 'CSAS_ACCESS_TOKEN']
        required_csas_account = ['CSAS_ACCOUNT_UUID', 'CSAS_ACCOUNT_IBAN']  # At least one needed
        required_office365 = ['OFFICE365_TENANT', 'OFFICE365_SITE']
        
        missing = []
        
        # Check CSAS credentials
        for var in required_csas:
            if not os.getenv(var):
                missing.append(var)
        
        # Check CSAS account (at least one needed)
        if not any(os.getenv(var) for var in required_csas_account):
            missing.extend(required_csas_account)
        
        # Check Office 365 basic config
        for var in required_office365:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            self.logger.error(f"Missing required environment variables: {', '.join(missing)}")
            return False
        
        return True
    
    def download_statements(self, 
                          format_type: str = 'pdf', 
                          scope: Optional[str] = None) -> bool:
        """
        Download bank statements from CSAS.
        
        Args:
            format_type: Statement format (pdf, xml, abo-standard, etc.)
            scope: Time scope for statements (last_month, current_month, etc.)
            
        Returns:
            True if download was successful
        """
        self.logger.info(f"Downloading CSAS statements (format: {format_type})")
        
        cmd = [
            'csas-statement-downloader',
            '-d', self.temp_dir,
            '-f', format_type
        ]
        
        # Set environment variables for the command
        env = os.environ.copy()
        if scope:
            env['CSAS_STATEMENT_SCOPE'] = scope
        
        try:
            result = subprocess.run(
                cmd, 
                env=env, 
                capture_output=True, 
                text=True, 
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Find downloaded files
                self.downloaded_files = glob.glob(os.path.join(self.temp_dir, '*'))
                self.logger.info(f"Successfully downloaded {len(self.downloaded_files)} statement(s)")
                
                for file_path in self.downloaded_files:
                    self.logger.debug(f"Downloaded: {os.path.basename(file_path)}")
                
                return True
            else:
                self.logger.error(f"CSAS downloader failed: {result.stderr}")
                if result.stdout:
                    self.logger.debug(f"CSAS downloader stdout: {result.stdout}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("CSAS statement download timed out")
            return False
        except subprocess.CalledProcessError as e:
            self.logger.error(f"CSAS downloader error: {e}")
            return False
    
    def upload_to_sharepoint(self, sharepoint_path: str = '') -> bool:
        """
        Upload downloaded files to SharePoint.
        
        Args:
            sharepoint_path: Target path in SharePoint
            
        Returns:
            True if upload was successful
        """
        if not self.downloaded_files:
            self.logger.warning("No files to upload to SharePoint")
            return False
        
        self.logger.info(f"Uploading {len(self.downloaded_files)} file(s) to SharePoint")
        
        success_count = 0
        
        for file_path in self.downloaded_files:
            if not os.path.exists(file_path):
                self.logger.warning(f"File not found: {file_path}")
                continue
            
            self.logger.debug(f"Uploading: {os.path.basename(file_path)}")
            
            cmd = [
                'file2sharepoint',
                file_path,
                sharepoint_path
            ]
            
            try:
                result = subprocess.run(
                    cmd,
                    env=os.environ.copy(),
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minute timeout per file
                )
                
                if result.returncode == 0:
                    success_count += 1
                    self.logger.info(f"Successfully uploaded: {os.path.basename(file_path)}")
                    if result.stdout.strip():
                        self.logger.info(f"SharePoint URL: {result.stdout.strip()}")
                else:
                    self.logger.error(f"Failed to upload {os.path.basename(file_path)}: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                self.logger.error(f"Upload timeout for: {os.path.basename(file_path)}")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Upload error for {os.path.basename(file_path)}: {e}")
        
        self.logger.info(f"Upload complete: {success_count}/{len(self.downloaded_files)} files uploaded")
        return success_count > 0
    
    def cleanup(self) -> None:
        """
        Clean up temporary files.
        """
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.logger.debug(f"Cleaned up temporary directory: {self.temp_dir}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup temporary directory: {e}")
    
    def run(self, 
            format_type: str = 'pdf', 
            scope: Optional[str] = None,
            sharepoint_path: str = '',
            cleanup: bool = True) -> int:
        """
        Run the complete CSAS to SharePoint upload process.
        
        Args:
            format_type: Statement format for download
            scope: Time scope for statements
            sharepoint_path: Target SharePoint path
            cleanup: Whether to cleanup temp files after completion
            
        Returns:
            Exit code (0 for success)
        """
        try:
            if not self._check_environment():
                return 1
            
            # Step 1: Download statements
            if not self.download_statements(format_type, scope):
                return 2
            
            # Step 2: Upload to SharePoint
            if not self.upload_to_sharepoint(sharepoint_path):
                return 3
            
            self.logger.info("CSAS to SharePoint upload completed successfully")
            return 0
            
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return 4
        finally:
            if cleanup:
                self.cleanup()


def main() -> int:
    """
    Main entry point for the application.
    
    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description='Download CSAS bank statements and upload to SharePoint',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  CSAS_API_KEY         - CSAS API key
  CSAS_ACCESS_TOKEN    - CSAS access token
  CSAS_ACCOUNT_UUID    - CSAS account UUID (or CSAS_ACCOUNT_IBAN)
  CSAS_ACCOUNT_IBAN    - CSAS account IBAN (alternative to UUID)
  CSAS_STATEMENT_SCOPE - Default scope for statement download
  STATEMENT_FORMAT     - Default format for statements (MultiFlexi)
  
  OFFICE365_TENANT     - Office 365 tenant name
  OFFICE365_SITE       - SharePoint site name
  OFFICE365_PATH       - Target path in SharePoint
  SHAREPOINT_LIBRARY   - SharePoint document library
  OFFICE365_USERNAME   - Office 365 username (for user auth)
  OFFICE365_PASSWORD   - Office 365 password (for user auth)
  OFFICE365_CLIENTID   - Office 365 client ID (for app auth)
  OFFICE365_CLSECRET   - Office 365 client secret (for app auth)
  
  DEBUG                - Enable debug logging (true/false)
  APP_DEBUG            - Enable application debug mode
  EASE_LOGGER          - Logging method (console/syslog/eventlog)
  RESULT_FILE          - Output JSON report file

Formats: pdf, xml, xml-data, abo-standard, abo-internal, csv-comma, csv-semicolon, mt940
Scopes: yesterday, current_month, last_month, last_two_months, previous_month, this_year
        """
    )
    
    parser.add_argument(
        '-f', '--format',
        default=os.getenv('STATEMENT_FORMAT', 'pdf'),
        help='Statement format (default: pdf or STATEMENT_FORMAT env var)'
    )
    
    parser.add_argument(
        '-s', '--scope',
        help='Time scope for statements (default: from CSAS_STATEMENT_SCOPE env var)'
    )
    
    parser.add_argument(
        '-p', '--sharepoint-path',
        default='',
        help='Target path in SharePoint'
    )
    
    parser.add_argument(
        '-t', '--temp-dir',
        help='Temporary directory for downloads'
    )
    
    parser.add_argument(
        '--no-cleanup',
        action='store_true',
        help='Do not cleanup temporary files'
    )
    
    args = parser.parse_args()
    
    # Load environment from .env file if it exists
    env_file = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ.setdefault(key, value)
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}", file=sys.stderr)
    
    uploader = CSASSharePointUploader(args.temp_dir)
    
    return uploader.run(
        format_type=args.format,
        scope=args.scope,
        sharepoint_path=args.sharepoint_path,
        cleanup=not args.no_cleanup
    )


if __name__ == "__main__":
    sys.exit(main())
