try:
    from app.main import app
    print("SUCCESS: Imported app.main.app")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
