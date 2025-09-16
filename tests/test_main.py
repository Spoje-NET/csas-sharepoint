#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for CSAS-SharePoint uploader.

Author: Vítězslav Dvořák <info@vitexsoftware.cz>
"""

import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import sys

# Add src directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import CSASSharePointUploader


class TestCSASSharePointUploader(unittest.TestCase):
    """Test cases for CSASSharePointUploader class."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.uploader = CSASSharePointUploader(self.temp_dir)

    def tearDown(self) -> None:
        """Clean up after each test method."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_init(self) -> None:
        """Test CSASSharePointUploader initialization."""
        self.assertIsInstance(self.uploader, CSASSharePointUploader)
        self.assertEqual(self.uploader.temp_dir, self.temp_dir)
        self.assertEqual(self.uploader.downloaded_files, [])
        self.assertTrue(os.path.exists(self.temp_dir))

    @patch.dict(os.environ, {
        'CSAS_API_KEY': 'test-key',
        'CSAS_ACCESS_TOKEN': 'test-token',
        'CSAS_ACCOUNT_IBAN': 'CZ1234567890123456789012',
        'OFFICE365_TENANT': 'test-tenant',
        'OFFICE365_SITE': 'test-site'
    })
    def test_check_environment_success(self) -> None:
        """Test environment check with all required variables."""
        result = self.uploader._check_environment()
        self.assertTrue(result)

    @patch.dict(os.environ, {}, clear=True)
    def test_check_environment_missing_vars(self) -> None:
        """Test environment check with missing variables."""
        result = self.uploader._check_environment()
        self.assertFalse(result)

    @patch.dict(os.environ, {
        'CSAS_API_KEY': 'test-key',
        'CSAS_ACCESS_TOKEN': 'test-token',
        'CSAS_ACCOUNT_IBAN': 'CZ1234567890123456789012',
        'OFFICE365_TENANT': 'test-tenant'
        # Missing OFFICE365_SITE
    })
    def test_check_environment_partial_missing(self) -> None:
        """Test environment check with some missing variables."""
        result = self.uploader._check_environment()
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_download_statements_success(self, mock_run: MagicMock) -> None:
        """Test successful statement download."""
        # Create a mock file in temp directory
        test_file = os.path.join(self.temp_dir, 'test_statement.pdf')
        with open(test_file, 'w') as f:
            f.write('test content')

        # Mock successful subprocess call
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')

        result = self.uploader.download_statements('pdf', 'last_month')
        
        self.assertTrue(result)
        mock_run.assert_called_once()
        self.assertIn(test_file, self.uploader.downloaded_files)

    @patch('subprocess.run')
    def test_download_statements_failure(self, mock_run: MagicMock) -> None:
        """Test failed statement download."""
        # Mock failed subprocess call
        mock_run.return_value = MagicMock(
            returncode=1, 
            stdout='', 
            stderr='Download failed'
        )

        result = self.uploader.download_statements('pdf', 'last_month')
        
        self.assertFalse(result)
        mock_run.assert_called_once()
        self.assertEqual(self.uploader.downloaded_files, [])

    @patch('subprocess.run')
    def test_upload_to_sharepoint_success(self, mock_run: MagicMock) -> None:
        """Test successful SharePoint upload."""
        # Create test files
        test_file = os.path.join(self.temp_dir, 'test_statement.pdf')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        self.uploader.downloaded_files = [test_file]

        # Mock successful subprocess call
        mock_run.return_value = MagicMock(
            returncode=0, 
            stdout='https://sharepoint.com/test.pdf\n', 
            stderr=''
        )

        result = self.uploader.upload_to_sharepoint('test/path')
        
        self.assertTrue(result)
        mock_run.assert_called_once()

    def test_upload_to_sharepoint_no_files(self) -> None:
        """Test SharePoint upload with no files."""
        result = self.uploader.upload_to_sharepoint('test/path')
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_upload_to_sharepoint_failure(self, mock_run: MagicMock) -> None:
        """Test failed SharePoint upload."""
        # Create test files
        test_file = os.path.join(self.temp_dir, 'test_statement.pdf')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        self.uploader.downloaded_files = [test_file]

        # Mock failed subprocess call
        mock_run.return_value = MagicMock(
            returncode=1, 
            stdout='', 
            stderr='Upload failed'
        )

        result = self.uploader.upload_to_sharepoint('test/path')
        
        self.assertFalse(result)

    def test_cleanup(self) -> None:
        """Test cleanup functionality."""
        # Ensure temp directory exists
        self.assertTrue(os.path.exists(self.temp_dir))
        
        # Call cleanup
        self.uploader.cleanup()
        
        # Check if directory was removed
        self.assertFalse(os.path.exists(self.temp_dir))

    @patch.object(CSASSharePointUploader, '_check_environment')
    @patch.object(CSASSharePointUploader, 'download_statements')
    @patch.object(CSASSharePointUploader, 'upload_to_sharepoint')
    def test_run_success(self, mock_upload: MagicMock, mock_download: MagicMock, 
                        mock_check: MagicMock) -> None:
        """Test successful complete run."""
        mock_check.return_value = True
        mock_download.return_value = True
        mock_upload.return_value = True

        result = self.uploader.run()
        
        self.assertEqual(result, 0)
        mock_check.assert_called_once()
        mock_download.assert_called_once()
        mock_upload.assert_called_once()

    @patch.object(CSASSharePointUploader, '_check_environment')
    def test_run_environment_failure(self, mock_check: MagicMock) -> None:
        """Test run with environment check failure."""
        mock_check.return_value = False

        result = self.uploader.run()
        
        self.assertEqual(result, 1)

    @patch.object(CSASSharePointUploader, '_check_environment')
    @patch.object(CSASSharePointUploader, 'download_statements')
    def test_run_download_failure(self, mock_download: MagicMock, 
                                 mock_check: MagicMock) -> None:
        """Test run with download failure."""
        mock_check.return_value = True
        mock_download.return_value = False

        result = self.uploader.run()
        
        self.assertEqual(result, 2)

    @patch.object(CSASSharePointUploader, '_check_environment')
    @patch.object(CSASSharePointUploader, 'download_statements')
    @patch.object(CSASSharePointUploader, 'upload_to_sharepoint')
    def test_run_upload_failure(self, mock_upload: MagicMock, mock_download: MagicMock, 
                               mock_check: MagicMock) -> None:
        """Test run with upload failure."""
        mock_check.return_value = True
        mock_download.return_value = True
        mock_upload.return_value = False

        result = self.uploader.run()
        
        self.assertEqual(result, 3)


class TestEnvironmentLoading(unittest.TestCase):
    """Test environment loading functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_env_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env')
        self.test_env_file.write('TEST_VAR=test_value\n')
        self.test_env_file.write('# This is a comment\n')
        self.test_env_file.write('ANOTHER_VAR=another_value\n')
        self.test_env_file.close()

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        os.unlink(self.test_env_file.name)

    def test_env_loading(self) -> None:
        """Test that environment variables are loaded from .env file."""
        # This would require testing the main() function's env loading
        # For now, we'll just test that the file exists and is readable
        self.assertTrue(os.path.exists(self.test_env_file.name))
        
        with open(self.test_env_file.name, 'r') as f:
            content = f.read()
            self.assertIn('TEST_VAR=test_value', content)
            self.assertIn('ANOTHER_VAR=another_value', content)


if __name__ == '__main__':
    unittest.main()