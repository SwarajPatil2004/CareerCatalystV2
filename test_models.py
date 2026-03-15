try:
    from app.db.models import StudentDriveAssociation, StudentDriveStatus
    print("SUCCESS: Imported StudentDriveAssociation and StudentDriveStatus")
except Exception as e:
    import traceback
    traceback.print_exc()
