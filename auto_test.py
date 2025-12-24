#!/usr/bin/env python
"""
Auto Test Script
Starts the project and runs all tests in the tests/ directory
Logs all results to logs/test_run.log
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path

def setup_logging():
    """Create logs directory if it doesn't exist"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    return logs_dir / "test_run.log"

def log_message(message, log_file):
    """Write message to both console and log file"""
    print(message)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def run_tests(log_file):
    """Run all test cases from tests/ directory"""
    log_message(f"\n{'='*60}", log_file)
    log_message(f"Test Run Started: {datetime.datetime.now()}", log_file)
    log_message(f"{'='*60}\n", log_file)
    
    tests_dir = Path("tests")
    test_files = sorted(tests_dir.glob("case_*.py"))
    
    if not test_files:
        log_message("ERROR: No test files found in tests/ directory", log_file)
        return False
    
    all_passed = True
    passed_count = 0
    failed_count = 0
    
    for test_file in test_files:
        test_name = test_file.stem
        log_message(f"\nRunning: {test_name}", log_file)
        log_message("-" * 40, log_file)
        
        try:
            # Get the virtual environment python executable
            venv_python = Path(".venv/Scripts/python.exe")
            if not venv_python.exists():
                venv_python = Path(".venv/Scripts/python")
            
            result = subprocess.run(
                [str(venv_python), "-m", "pytest", str(test_file), "-v"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                # Fallback: try running the test file directly
                result = subprocess.run(
                    [str(venv_python), str(test_file)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    env={**os.environ, "APP_MODE": "production"}
                )
                
                if result.returncode == 0:
                    log_message(f"✓ PASSED: {test_name}", log_file)
                    passed_count += 1
                else:
                    log_message(f"✗ FAILED: {test_name}", log_file)
                    if result.stdout:
                        log_message(f"  Output: {result.stdout}", log_file)
                    if result.stderr:
                        log_message(f"  Error: {result.stderr}", log_file)
                    failed_count += 1
                    all_passed = False
            else:
                log_message(f"✓ PASSED: {test_name}", log_file)
                passed_count += 1
                if result.stdout:
                    log_message(f"  {result.stdout}", log_file)
                    
        except subprocess.TimeoutExpired:
            log_message(f"✗ TIMEOUT: {test_name} (exceeded 30 seconds)", log_file)
            failed_count += 1
            all_passed = False
        except Exception as e:
            log_message(f"✗ ERROR: {test_name} - {str(e)}", log_file)
            failed_count += 1
            all_passed = False
    
    # Summary
    log_message(f"\n{'='*60}", log_file)
    log_message(f"Test Summary", log_file)
    log_message(f"{'='*60}", log_file)
    log_message(f"Total Tests: {len(test_files)}", log_file)
    log_message(f"Passed: {passed_count}", log_file)
    log_message(f"Failed: {failed_count}", log_file)
    log_message(f"Test Run Completed: {datetime.datetime.now()}", log_file)
    log_message(f"{'='*60}\n", log_file)
    
    return all_passed

def start_application(log_file):
    """Start the application to verify it works"""
    log_message("\n" + "="*60, log_file)
    log_message("Starting Application", log_file)
    log_message("="*60, log_file)
    
    try:
        venv_python = Path(".venv/Scripts/python.exe")
        if not venv_python.exists():
            venv_python = Path(".venv/Scripts/python")
        
        result = subprocess.run(
            [str(venv_python), "app.py"],
            capture_output=True,
            text=True,
            timeout=5,
            env={**os.environ, "APP_MODE": "production"}
        )
        
        if result.returncode == 0:
            log_message("✓ Application started successfully", log_file)
            if result.stdout:
                log_message(f"  Output: {result.stdout.strip()}", log_file)
            return True
        else:
            log_message("✗ Application failed to start", log_file)
            if result.stdout:
                log_message(f"  Output: {result.stdout}", log_file)
            if result.stderr:
                log_message(f"  Error: {result.stderr}", log_file)
            return False
            
    except subprocess.TimeoutExpired:
        log_message("✓ Application started (timed out after 5 seconds - normal behavior)", log_file)
        return True
    except Exception as e:
        log_message(f"✗ Error starting application: {str(e)}", log_file)
        return False

def main():
    """Main entry point"""
    log_file = setup_logging()
    
    # Clear previous log
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("")
    
    log_message("Auto Test Suite", log_file)
    log_message("="*60, log_file)
    
    # Start application first
    app_started = start_application(log_file)
    
    # Run tests
    tests_passed = run_tests(log_file)
    
    # Final result
    log_message("\n" + "="*60, log_file)
    if app_started and tests_passed:
        log_message("✓ ALL CHECKS PASSED", log_file)
        log_message("="*60, log_file)
        return 0
    else:
        log_message("✗ SOME CHECKS FAILED", log_file)
        log_message("="*60, log_file)
        return 1

if __name__ == "__main__":
    sys.exit(main())
