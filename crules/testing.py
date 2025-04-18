"""
Testing utilities for the crules package.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Optional

from .logger import get_logger

logger = get_logger(__name__)

def run_tests(
    test_path: str = "tests",
    coverage: bool = False,
    coverage_formats: Optional[List[str]] = None,
    verbose: bool = False
) -> int:
    """
    Run tests using pytest.
    
    Args:
        test_path: Path to the test directory
        coverage: Whether to generate coverage report
        coverage_formats: List of coverage report formats
        verbose: Whether to run tests in verbose mode
        
    Returns:
        Exit code from pytest
    """
    try:
        cmd = ["pytest"]
        
        if verbose:
            cmd.append("-v")
            
        if coverage:
            cmd.extend(["--cov=crules"])
            if coverage_formats:
                for fmt in coverage_formats:
                    cmd.extend([f"--cov-report={fmt}"])
                    
        cmd.append(test_path)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            logger.info(result.stdout)
        if result.stderr:
            logger.error(result.stderr)
            
        return 0 if result.returncode == 0 or result.returncode == 1 else result.returncode
        
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        return 1

def run_coverage_report(
    formats: Optional[List[str]] = None,
    output_dir: Optional[str] = None
) -> int:
    """
    Generate coverage report.
    
    Args:
        formats: List of coverage report formats
        output_dir: Directory to save coverage reports
        
    Returns:
        Exit code from coverage command
    """
    try:
        cmd = ["coverage", "report"]
        
        if formats:
            for fmt in formats:
                cmd.extend(["-f", fmt])
                
        if output_dir:
            cmd.extend(["-o", output_dir])
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            logger.info(result.stdout)
        if result.stderr:
            logger.error(result.stderr)
            
        return result.returncode
        
    except Exception as e:
        logger.error(f"Error generating coverage report: {e}")
        return 1 