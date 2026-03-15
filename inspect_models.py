import app.db.models
print(f"File loaded: {app.db.models.__file__}")
print("Members in app.db.models:")
members = [m for m in dir(app.db.models) if not m.startswith("__")]
print(", ".join(members))

if "StudentDriveAssociation" in members:
    print("SUCCESS: StudentDriveAssociation is present")
else:
    print("FAILURE: StudentDriveAssociation is NOT present")
