# Project: oswe-mini-m23a1s255 — quick start ✅

This repository is a small Python service. The original README contained incorrect commands and environment settings; the instructions below are tested and will allow you to run the project and the test-suite locally.

---

## Requirements

- Python 3.10+ (system Python)
- git (optional)
- A clean virtual environment (this guide uses a project-local `.venv/`)

---

## Quick start (Windows & UNIX) 🛠️

1) Create a clean virtual environment (recommended name: `.venv`)

Windows (PowerShell):

```powershell
# remove existing environment if present (ensures a clean env)
if (Test-Path .venv) { Remove-Item -Recurse -Force .venv }
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
```

2) Install runtime + test dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pytest
```

Notes:
- `requirements.txt` contains runtime deps (e.g. PyYAML). Tests require `pytest` which is installed above.

3) Required configuration

- This project uses `settings.yaml` for the service port (default: `9123`).
- **You must set the environment variable `APP_MODE=production`** when running the service or the tests — the code validates this before starting.

Windows (PowerShell):

```powershell
$env:APP_MODE = "production"
```

macOS / Linux:

```bash
export APP_MODE=production
```

4) Run the application (what to expect)

```bash
python app.py
```

Expected output (example):

```
Service started successfully
Port: 9123
```

Notes:
- The service is not a long-running HTTP server in this kata — `app.py` performs startup validation and exits with code `0` on success.
- The port value comes from `settings.yaml` (default `9123`).

5) Run the test-suite (recommended)

```bash
# from project root, with `.venv` activated and APP_MODE=production
# NOTE: pytest's default discovery requires filenames like `test_*.py` or `*_test.py`.
# This repository uses `case_*.py` filenames — to run tests with pytest directly, pass the files explicitly:
python -m pytest tests/case_*.py -q
```

Or use the provided convenience runner which creates logs and uses the project `.venv` (recommended):

```bash
.\\.venv\\Scripts\\python auto_test.py    # Windows
.venv/bin/python auto_test.py                # macOS / Linux
```

Test logs are written to `logs/test_run.log`.

---

Troubleshooting & CI hints 💡

- If you see `FileNotFoundError: settings.yaml not found` — run from the project root or ensure `settings.yaml` exists.
- If you see `EnvironmentError: APP_MODE environment variable is required` — set `APP_MODE=production` before running.
- If tests fail locally but pass in CI, ensure the virtual environment is clean (remove `.venv/`) and re-run the steps above.

---

CI / automation notes 🔧

- The repository expects `APP_MODE=production` and reads the port from `settings.yaml` (9123).
- Use the included `auto_test.py` to run the full validation (it will start the project validations and run the tests using `.venv`).

---

If anything is unclear or a step fails, open an issue with the command you ran and the full `logs/test_run.log` attached.