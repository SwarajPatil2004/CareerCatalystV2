from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Roadmap, RoadmapPhase, RoadmapTask

def seed_roadmap():
    db = SessionLocal()
    try:
        # Check if exists
        if db.query(Roadmap).filter(Roadmap.slug == "full-stack-web").first():
            print("Roadmap already seeded.")
            return

        roadmap = Roadmap(
            name="Full-Stack Web Development",
            slug="full-stack-web",
            description="Master modern web development from frontend to backend.",
            career_type="web_development"
        )
        db.add(roadmap)
        db.flush()

        # Phase 1: Frontend Fundamentals
        p1 = RoadmapPhase(roadmap_id=roadmap.id, phase_index=1, title="Frontend Fundamentals", description="Learn HTML, CSS, and basic JavaScript.")
        db.add(p1)
        db.flush()

        db.add_all([
            RoadmapTask(phase_id=p1.id, title="Semantic HTML", description="Learn about semantic elements like <header>, <nav>, etc.", resource_link="https://developer.mozilla.org/en-US/docs/Glossary/Semantics", xp=15),
            RoadmapTask(phase_id=p1.id, title="CSS Layouts", description="Master Flexbox and Grid.", resource_link="https://css-tricks.com/snippets/css/a-guide-to-flexbox/", xp=20),
            RoadmapTask(phase_id=p1.id, title="JavaScript Basics", description="Variables, loops, and functions.", xp=25)
        ])

        # Phase 2: React & Modern UI
        p2 = RoadmapPhase(roadmap_id=roadmap.id, phase_index=2, title="React & Modern UI", description="Build dynamic user interfaces with React.")
        db.add(p2)
        db.flush()

        db.add_all([
            RoadmapTask(phase_id=p2.id, title="React Hooks", description="useState, useEffect, and custom hooks.", xp=30),
            RoadmapTask(phase_id=p2.id, title="State Management", description="Context API and Redux Toolkit.", xp=40),
            RoadmapTask(phase_id=p2.id, title="Tailwind CSS", description="Utility-first styling approach.", xp=20)
        ])

        db.commit()
        print("Roadmap seeded successfully!")
    except Exception as e:
        print(f"Error seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_roadmap()
