"""auto_test.py

- Uses the project-local `.venv` Python to:
  1. validate the application starts with APP_MODE=production
  2. run the test-suite under that same environment
  3. write combined output to `logs/test_run.log`

Run (Windows):  .\\.venv\\Scripts\\python auto_test.py
Run (UNIX):     .venv/bin/python auto_test.py
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
VENV_DIR = ROOT / ".venv" / ("Scripts" if os.name == "nt" else "bin")
VENV_PY = VENV_DIR / ("python.exe" if os.name == "nt" else "python")
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "test_run.log"


def fail(msg, code=2):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)
    sys.exit(code)


if __name__ == "__main__":
    # Pre-flight checks
    if not (ROOT / ".venv").exists():
        fail("Required virtual environment '.venv' not found. Create it and install dependencies before running this script.")

    if not VENV_PY.exists():
        fail(f"venv python not found at {VENV_PY}")

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.setdefault("APP_MODE", "production")

    # 1) Start/validate the application (app.py performs startup validation and exits)
    with LOG_FILE.open("w", encoding="utf-8") as outf:
        outf.write("=== Application start check ===\n")

    p = subprocess.run([str(VENV_PY), "app.py"], capture_output=True, text=True, env=env)
    with LOG_FILE.open("a", encoding="utf-8") as outf:
        outf.write(p.stdout)
        outf.write(p.stderr)
        outf.write(f"EXIT_CODE: {p.returncode}\n")

    if p.returncode != 0:
        fail("Application failed startup validation. See logs/test_run.log for details.")

    # 2) Run pytest (will use the same APP_MODE env)
    with LOG_FILE.open("a", encoding="utf-8") as outf:
        outf.write("\n=== Running tests (pytest) ===\n")

    # pytest default discovery ignores files that don't match test_*.py; this repo's tests are named
    # `case_*.py`, so pass explicit file paths to ensure they are executed.
    test_dir = ROOT / "tests"
    test_files = sorted([str(p) for p in test_dir.glob("*.py")])
    if not test_files:
        fail("No test files found in tests/ directory")

    cmd = [str(VENV_PY), "-m", "pytest"] + test_files + ["-q"]
    t = subprocess.run(cmd, capture_output=True, text=True, env=env)
    with LOG_FILE.open("a", encoding="utf-8") as outf:
        outf.write(t.stdout)
        outf.write(t.stderr)
        outf.write(f"TEST_EXIT_CODE: {t.returncode}\n")

    # 3) Summary
    summary = f"Application exit={p.returncode}; tests exit={t.returncode}"
    with LOG_FILE.open("a", encoding="utf-8") as outf:
        outf.write("\n=== Summary ===\n")
        outf.write(summary + "\n")

    print(summary)
    sys.exit(t.returncode)
