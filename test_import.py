try:
    from app.domains.identity.router import router
    print("SUCCESS: Imported app.domains.identity.router")
except Exception as e:
    import traceback
    traceback.print_exc()
