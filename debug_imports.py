import importlib
import sys

models_to_check = [
    'User', 'UserRole', 'Institution', 'InstitutionType', 'TPOProfile', 
    'StudentProfile', 'Skill', 'Experience', 'Certificate', 'Achievement', 
    'Project', 'PlacementDrive', 'StudentDriveJoin', 'StudentDriveStatus', 
    'Roadmap', 'RoadmapPhase', 'RoadmapTask', 'UserRoadmapProgress', 
    'AnalyticsEvent', 'StudentMetrics', 'InstitutionBudget', 'AICostLog', 
    'InterviewSession', 'InterviewQuestion', 'InterviewResponse', 
    'InterviewProctoringLog', 'ProjectSubmission', 'ProjectReview', 
    'ReviewQueue', 'Season', 'Squad', 'UserGamificationStats', 
    'Badge', 'UserBadge', 'Company', 'Recruiter', 'Shortlist', 
    'SkillBadge', 'ProjectDefense', 'AuditLog', 'UserConsent'
]

print("Importing app.db.models...")
try:
    import app.db.models
    print("SUCCESS: Imported app.db.models")
except Exception as e:
    print(f"FAILURE: Could not import app.db.models: {e}")
    sys.exit(1)

for model in models_to_check:
    try:
        getattr(app.db.models, model)
        print(f"SUCCESS: {model} is present")
    except AttributeError:
        print(f"FAILURE: {model} is NOT present")
    except Exception as e:
        print(f"ERROR checking {model}: {e}")
