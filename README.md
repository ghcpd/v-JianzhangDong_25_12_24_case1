## Requirements

- Python 3.10+
- pip

---

## Quick Start

### 1. Create virtual environment

```bash
# Create a local virtual environment directory named `.venv`
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Or (Windows cmd)
.venv\Scripts\activate

# Or (macOS / Linux)
source .venv/bin/activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Configure environment variables

This project reads the service port from `settings.yaml` (already present in the repository) and **requires** the environment variable `APP_MODE` to be set. The application expects `APP_MODE` to be set to `production` when running the tests and for normal execution.

Examples:

Windows (PowerShell, session only):
```powershell
$env:APP_MODE = "production"
```

Windows (cmd):
```cmd
set APP_MODE=production
```

macOS / Linux:
```bash
export APP_MODE=production
```

Note: There is no `.env.example` file used by this project and `APP_ENV`, `PORT`, `DEBUG` are not used. Keep `settings.yaml` intact for service port configuration.

### 4. Run the application

Activate the virtual environment and install dependencies (see step 2), then run:

```bash
python app.py
```

Expected output on success:
```
Service started successfully
Port: 9123
```

This application is a simple startup script (it prints the port configured in `settings.yaml`) rather than a persistent HTTP server.

### 5. Run tests and verify

Install the test runner (recommended):

```bash
pip install pytest
```

Run tests with the virtual environment's Python:

```bash
python -m pytest tests
```

Or use the included helper `auto_test.py` which:
- Ensures `APP_MODE` is set to `production` for the test run
- Runs the test suite using the `.venv` environment
- Writes the combined test output to `logs/test_run.log`

Run the helper with your system Python:

```bash
python auto_test.py
```

Check `logs/test_run.log` for the detailed test output and summary.
