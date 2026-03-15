import importlib
import sys
import traceback

print("Surgical Trace Start...")
try:
    importlib.import_module("app.main")
    print("SUCCESS")
except ImportError:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb = traceback.extract_tb(exc_traceback)
    for frame in tb:
        print(f"File: {frame.filename}, Line: {frame.lineno}, In: {frame.name}")
        print(f"  Code: {frame.line}")
    print(f"ERROR: {exc_value}")
except Exception as e:
    print(f"OTHER ERROR: {e}")
    traceback.print_exc()
