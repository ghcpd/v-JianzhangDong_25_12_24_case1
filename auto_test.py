import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
VENV_PY = ROOT / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "test_run.log"


def ensure_logs():
    LOG_DIR.mkdir(exist_ok=True)


def run_project(python_exe, env):
    # run app.py once to show startup output
    proc = subprocess.run([str(python_exe), "app.py"], capture_output=True, text=True, env=env)
    return proc


def run_pytest(python_exe, env):
    # collect python files under tests/ and pass them explicitly to pytest
    test_dir = ROOT / "tests"
    test_files = sorted([str(p) for p in test_dir.glob("*.py")])
    if not test_files:
        # nothing to run
        return subprocess.CompletedProcess(args=[], returncode=0, stdout="no test files found\n", stderr="")
    cmd = [str(python_exe), "-m", "pytest", *test_files, "-q"]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return proc


def main():
    ensure_logs()

    if not VENV_PY.exists():
        print("ERROR: .venv not found. Create it first (python -m venv .venv and install requirements)." )
        sys.exit(2)

    env = os.environ.copy()
    env["APP_MODE"] = "production"

    with open(LOG_FILE, "w", encoding="utf-8") as fh:
        fh.write("=== auto_test.py run ===\n")

        fh.write("\n-- Starting app.py --\n")
        app_proc = run_project(VENV_PY, env)
        fh.write(app_proc.stdout)
        if app_proc.stderr:
            fh.write("\n[app stderr]\n")
            fh.write(app_proc.stderr)

        fh.write("\n-- Running pytest --\n")
        test_proc = run_pytest(VENV_PY, env)
        fh.write(test_proc.stdout)
        if test_proc.stderr:
            fh.write("\n[pytest stderr]\n")
            fh.write(test_proc.stderr)

    # mirror results to console
    print("App exit code:", app_proc.returncode)
    print(test_proc.stdout)
    print("Tests exit code:", test_proc.returncode)

    sys.exit(test_proc.returncode)


if __name__ == "__main__":
    main()