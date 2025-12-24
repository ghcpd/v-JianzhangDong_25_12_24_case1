import os
import sys
import subprocess
import importlib.util

# Set environment variable
os.environ['APP_MODE'] = 'production'

# Function to run a test function from a module
def run_test(module_name, test_func_name):
    try:
        # Import the module
        spec = importlib.util.spec_from_file_location(module_name, f"tests/{module_name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Get the test function
        test_func = getattr(module, test_func_name)
        # Run the test
        test_func()
        return f"PASS: {module_name}.{test_func_name}"
    except Exception as e:
        return f"FAIL: {module_name}.{test_func_name} - {str(e)}"

# Create logs directory if not exists
os.makedirs('logs', exist_ok=True)

# Run all tests
results = []
results.append(run_test('case_1', 'test_app_starts'))
results.append(run_test('case_2', 'test_output_contains_port'))
results.append(run_test('case_3', 'test_correct_port'))

# Write results to log
with open('logs/test_run.log', 'w') as f:
    for result in results:
        f.write(result + '\n')
        print(result)