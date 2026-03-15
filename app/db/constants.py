import enum

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TPO = "tpo"

class InstitutionType(str, enum.Enum):
    ENGINEERING = "engineering"
    MANAGEMENT = "management"
    OTHER = "other"

class DriveStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class StudentDriveStatus(str, enum.Enum):
    INVITED = "invited"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    SELECTED = "selected"
