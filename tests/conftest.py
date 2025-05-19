'''
Configuration test for code to ensure you are in the correct layer of the 
directory for relative imports to run stably
'''
import pytest
from pathlib import Path

EXPECTED_ROOT = Path(__file__).resolve().parent.parent

def pytest_configure():
    cwd = Path.cwd().resolve()
    if cwd != EXPECTED_ROOT:
        msg = (
            f"\n\n Tests must be run from the project root: {EXPECTED_ROOT}\n"
            f"Current working directory: {cwd}\n"
            f"Use:\n  cd {EXPECTED_ROOT}\n  pytest\n"
        )
        pytest.exit(msg)
