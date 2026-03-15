import importlib
import sys
import traceback

with open("traceback.txt", "w") as f:
    try:
        importlib.import_module("app.main")
        f.write("SUCCESS")
    except ImportError:
        traceback.print_exc(file=f)
    except Exception:
        traceback.print_exc(file=f)
