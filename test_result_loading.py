#!/usr/bin/env python3

import sys
import os
import tempfile
import json
import shutil

# Add the package directory to the path so we can import the main module
script_dir = os.path.dirname(os.path.abspath(__file__))
if '/usr/lib/csas-sharepoint' in script_dir:
    # Running from installed package
    sys.path.insert(0, '/usr/lib/csas-sharepoint')
else:
    # Running from source
    sys.path.insert(0, os.path.join(os.path.dirname(script_dir), 'src'))

from main import CSASSharePointUploader

def test_result_loading():
    """Test the result loading functionality with mock data."""
    
    print("Testing result loading functionality...")
    
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp(prefix='csas_test_')
    print(f"Using temp directory: {temp_dir}")
    
    try:
        # Set up environment for testing
        os.environ['RESULT_FILE'] = os.path.join(temp_dir, 'original_result.json')
        
        # Create uploader instance
        uploader = CSASSharePointUploader(temp_dir)
        
        # Set up temporary result file
        uploader._setup_temp_result_file()
        print(f"Temp result file: {uploader.temp_result_file}")
        
        # Test 1: Copy mock download result and test loading
        if uploader.temp_result_file:
            shutil.copy2('/tmp/mock_csas_result.json', uploader.temp_result_file)
            download_result = uploader._load_temp_result('download')
            print("\\nDownload result loaded:")
            print(json.dumps(download_result, indent=2))
            
            # Test 2: Copy mock upload result and test loading  
            shutil.copy2('/tmp/mock_sharepoint_result.json', uploader.temp_result_file)
            upload_result = uploader._load_temp_result('upload')
            print("\\nUpload result loaded:")
            print(json.dumps(upload_result, indent=2))
            
            # Test 3: Test result writing
            uploader.download_result = download_result
            uploader.upload_results = [upload_result]
            uploader.downloaded_files = ['/tmp/test1.pdf', '/tmp/test2.pdf']
            
            # Mock the original result file
            uploader.original_result_file = os.path.join(temp_dir, 'final_report.json')
            
            uploader._write_final_result()
            
            # Read and display final result
            with open(uploader.original_result_file, 'r') as f:
                final_result = json.load(f)
            
            print("\\nFinal combined result:")
            print(json.dumps(final_result, indent=2))
            
        else:
            print("No temp result file was set up")
            
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        print(f"\\nCleaned up temp directory: {temp_dir}")

if __name__ == "__main__":
    test_result_loading()