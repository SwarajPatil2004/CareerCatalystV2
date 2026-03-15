import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

print("Inspecting app.db.models load...")
try:
    import app.db.models as models
    print(f"SUCCESS: Models loaded. Keys: {[k for k in dir(models) if not k.startswith('_')]}")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    # Attempt to see what was loaded so far if possible
    if 'app.db.models' in sys.modules:
        m = sys.modules['app.db.models']
        print(f"Partially loaded models keys: {[k for k in dir(m) if not k.startswith('_')]}")
except Exception as e:
    print(f"OTHER ERROR: {e}")

print("Done.")
