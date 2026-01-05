import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
VENV = ROOT / ".venv"
LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)
LOG_FILE = LOGS / "test_run.log"

# Locate the venv python
if os.name == "nt":
    venv_py = VENV / "Scripts" / "python.exe"
else:
    venv_py = VENV / "bin" / "python"

if not venv_py.exists():
    print("Error: .venv not found or not created. Create the virtual env and install dependencies first.")
    sys.exit(2)

env = os.environ.copy()
env["APP_MODE"] = "production"

with open(LOG_FILE, "w", encoding="utf-8") as fh:
    fh.write("=== STARTUP CHECK ===\n")
    # Run app.py once to verify startup
    proc = subprocess.run([str(venv_py), "app.py"], capture_output=True, text=True, env=env)
    fh.write(proc.stdout)
    if proc.stderr:
        fh.write("STDERR:\n")
        fh.write(proc.stderr)

    fh.write("\n=== RUNNING TESTS ===\n")
    # Run pytest using venv python. The repository's test files are named `case_*.py` (not matching pytest's default discovery),
    # so we explicitly supply the test files found under `tests/`.
    test_files = [str(p) for p in (ROOT / "tests").glob("*.py")]
    if not test_files:
        fh.write("No test files found in tests/\n")
        class Dummy:
            returncode = 1
            stdout = ""
            stderr = "No test files found"
        test_proc = Dummy()
    else:
        test_proc = subprocess.run([str(venv_py), "-m", "pytest", "-q"] + test_files, capture_output=True, text=True, env=env)
    fh.write(test_proc.stdout)
    if getattr(test_proc, 'stderr', None):
        fh.write("STDERR:\n")
        fh.write(test_proc.stderr)

exit_code = test_proc.returncode if test_proc.returncode is not None else 1
print(f"Test run complete. See {LOG_FILE} for details.")
sys.exit(exit_code)
