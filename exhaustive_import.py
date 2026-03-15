import os
import importlib
import sys

def walk_and_import(package_path, package_name):
    for root, dirs, files in os.walk(package_path):
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                relative_path = os.path.relpath(os.path.join(root, file), package_path)
                module_name = f"{package_name}." + relative_path[:-3].replace(os.path.sep, ".")
                try:
                    importlib.import_module(module_name)
                    print(f"SUCCESS: {module_name}")
                except ImportError as e:
                    print(f"IMPORT ERROR in {module_name}: {e}")
                except Exception as e:
                    print(f"ERROR in {module_name}: {e}")

print("Starting exhaustive import test...")
walk_and_import("app", "app")
print("Finished exhaustive import test.")
