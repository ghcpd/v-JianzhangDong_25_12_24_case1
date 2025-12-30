## Requirements

- Python 3.10+
- pip

---

## Quick Start (Windows)

> These instructions use the project's recommended virtual environment folder `.venv` and PowerShell/Command Prompt examples.

### 1) Create and activate the virtual environment

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Command Prompt (cmd.exe):

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
# pytest is required for running the test-suite
pip install pytest
```

### 3) Required configuration

This project reads runtime configuration from `settings.yaml` and requires an environment variable `APP_MODE`.

- Set APP_MODE to `production` before running the app (tests rely on this):
  - PowerShell: `$env:APP_MODE = 'production'`
  - cmd.exe: `set APP_MODE=production`

The service port is defined in `settings.yaml` (default: `9123`).

### 4) Run the application

```powershell
python app.py
```

You should see output similar to:

```
Service started successfully
Port: 9123
```

### 5) Run tests / automated check

A helper script `auto_test.py` is provided to:
- start the project (with `APP_MODE=production`),
- run all tests in the `tests/` folder using the `.venv` environment,
- write results to `logs/test_run.log`.

To run the helper:

```powershell
python auto_test.py
```

Or run tests directly with the `.venv` Python:

```powershell
.\.venv\Scripts\python -m pytest tests -q
```

---

Notes

- The correct entrypoint is `app.py` (not `main.py`).
- The application requires `APP_MODE=production` to start successfully.
- `settings.yaml` controls the port (default `9123`).
- The `.venv/` directory is the recommended virtual environment location and is ignored by git (see `.gitignore`).
