import importlib
import sys
import traceback

def test_import(module_name):
    try:
        importlib.import_module(module_name)
        print(f"SUCCESS: {module_name}")
    except ImportError:
        print(f"IMPORT ERROR in {module_name}:")
        traceback.print_exc()
    except Exception:
        print(f"OTHER ERROR in {module_name}:")
        traceback.print_exc()

print("Tracing app.main import...")
test_import("app.main")
