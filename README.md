# Project Documentation

## Requirements

- Python 3.10 or higher
- pip (Python package installer)

---

## Project Structure

- `app.py` - Main application entry point
- `config.py` - Configuration loader (reads from settings.yaml and environment variables)
- `settings.yaml` - Service configuration with port settings
- `requirements.txt` - Python dependencies
- `tests/` - Test suite containing test cases
  - `case_1.py` - Test that app starts successfully
  - `case_2.py` - Test that output contains port information
  - `case_3.py` - Test that correct port (9123) is displayed

## Quick Start Guide

### 1. Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

On Linux/Mac:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Set the APP_MODE environment variable before running the application:

**Windows (Command Prompt):**
```bash
set APP_MODE=production
```

**Windows (PowerShell):**
```powershell
$env:APP_MODE="production"
```

**Linux/Mac:**
```bash
export APP_MODE=production
```

### 4. Run the application

```bash
python app.py
```

The application will output:
```
Service started successfully
Port: 9123
```

### 5. Run tests

Execute all test cases to verify the application:

```bash
python auto_test.py
```

Test results will be written to `logs/test_run.log`.

## Configuration

### Environment Variables

- `APP_MODE` - Application mode (must be set to 'production')

### Service Configuration (settings.yaml)

The service port can be configured in `settings.yaml`:
```yaml
service:
  port: 9123
```

## Dependencies

- `pyyaml>=6.0.2` - YAML parser for reading configuration files

## Testing

The project includes automated tests in the `tests/` directory. Run all tests using:

```bash
python auto_test.py
```

Test results and detailed logs are saved to `logs/test_run.log`.