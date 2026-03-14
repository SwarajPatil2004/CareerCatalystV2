from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import json
import random
from typing import List, Optional
from app.db.models import InterviewSession, InterviewQuestion, InterviewResponse, InterviewProctoringLog, User
from app.services.ai_provider_service import AIProviderService
from app.core.config import settings
from app.core.exceptions import AppException
from fastapi import status
# Mock Redis or real Redis if available
try:
    import redis
    redis_client = redis.from_url(settings.REDIS_URL or "redis://localhost:6379/0")
except ImportError:
    redis_client = None

USE_REAL_AI = getattr(settings, "USE_REAL_AI", False)

DEFAULT_QUESTIONS = {
    "full_stack": [
        {"text": "Explain the difference between virtual DOM and real DOM.", "type": "technical"},
        {"text": "How do you handle state management in a large-scale React application?", "type": "technical"},
        {"text": "Tell me about a time you had to resolve a conflict within your team.", "type": "behavioral"},
        {"text": "Describe the lifecycle of an HTTP request.", "type": "technical"},
        {"text": "Why do you want to work as a Full Stack Developer?", "type": "behavioral"}
    ],
    "data_science": [
        {"text": "Explain the bias-variance tradeoff.", "type": "technical"},
        {"text": "What is the difference between L1 and L2 regularization?", "type": "technical"},
        {"text": "Describe a data project where you had to deal with missing values.", "type": "behavioral"},
        {"text": "How does the Random Forest algorithm work?", "type": "technical"},
        {"text": "How do you stay updated with the latest trends in Data Science?", "type": "behavioral"}
    ]
}

class InterviewService:
    @staticmethod
    def start_session(db: Session, user_id: int, track: str):
        # Rate limit check (3/day)
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        daily_count = db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id,
            InterviewSession.start_time >= today_start
        ).count()
        
        if daily_count >= 3:
            raise AppException("Daily interview limit reached (3 per day)", status.HTTP_429_TOO_MANY_REQUESTS)

        session = InterviewSession(user_id=user_id, track=track)
        db.add(session)
        db.flush()

        # Generate questions
        questions_data = []
        cache_key = f"questions:{track}"
        
        if redis_client:
            cached = redis_client.get(cache_key)
            if cached:
                questions_data = json.loads(cached)
        
        if not questions_data:
            if USE_REAL_AI:
                # Call AI to generate 5 questions
                prompt = f"Generate 5 interview questions (3 technical, 2 behavioral) for a {track} role. Return as JSON list."
                # response = AIProviderService.call_gemini(...) # Placeholder
                # This would be a real implementation later
                questions_data = DEFAULT_QUESTIONS.get(track, DEFAULT_QUESTIONS["full_stack"])
            else:
                questions_data = DEFAULT_QUESTIONS.get(track, DEFAULT_QUESTIONS["full_stack"])
            
            if redis_client and questions_data:
                redis_client.setex(cache_key, 86400, json.dumps(questions_data))

        for i, q in enumerate(questions_data):
            db_q = InterviewQuestion(
                session_id=session.id,
                text=q["text"],
                type=q["type"],
                order=i
            )
            db.add(db_q)
        
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def submit_response(db: Session, session_id: int, question_id: int, transcript: str):
        response = InterviewResponse(
            question_id=question_id,
            transcript=transcript
        )
        db.add(response)
        db.commit()
        
        # Trigger async evaluation (simplified here)
        return response

    @staticmethod
    def evaluate_session(db: Session, session_id: int):
        # This method would typically trigger an asynchronous task
        # to evaluate all responses for a given session using AI.
        # For now, it's a placeholder. The actual evaluation logic
        # is included in finalize_interview for simplicity.
        print(f"Triggering evaluation for session {session_id}...")
        # In a real application, this might send a message to a queue
        # for a background worker to process.
        pass

    @staticmethod
    def finalize_interview(db: Session, session_id: int):
        session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
        if not session:
            return
        
        session.status = "completed"
        session.end_time = datetime.utcnow()
        
        responses = db.query(InterviewResponse).join(InterviewQuestion).filter(
            InterviewQuestion.session_id == session_id
        ).all()
        
        # Simple scoring for now: based on length/completeness
        # In prod, this would call AIProviderService.call_gemini for each response
        total_score = 0.0
        for resp in responses:
            if USE_REAL_AI:
                try:
                    prompt = f"""
                    Analyze this interview answer for a {session.track} role.
                    Question: {resp.question.text}
                    Transcript: {resp.transcript}
                    
                    Return JSON with:
                    - score (0.0 to 1.0)
                    - feedback (1-2 sentences)
                    - missed_keywords (list)
                    """
                    # We pass user_id/institution_id for cost tracking
                    # In a real app, we'd fetch institution_id from user
                    eval_res = AIProviderService.call_gemini(db, session.user_id, 1, prompt)
                    # Mocking JSON parsing of AI response for now
                    resp.evaluation_json = {
                        "score": 0.8, # Placeholder for AI parsed score
                        "feedback": eval_res[:100],
                        "missed_keywords": ["normalization"]
                    }
                except Exception as e:
                    print(f"AI Eval failed: {e}")
                    # Fallback to simple scoring
                    word_count = len(resp.transcript.split())
                    resp.evaluation_json = {"score": min(word_count/50, 1.0), "feedback": "Manual review required due to AI error."}
            else:
                word_count = len(resp.transcript.split())
                q_score = min(max(word_count / 50.0, 0.1), 1.0)
                resp.evaluation_json = {
                    "score": q_score,
                    "feedback": "Solid technical explanation." if word_count > 20 else "Please provide more depth in your answers."
                }
            total_score += resp.evaluation_json["score"]
            
        session.total_score = (total_score / len(responses)) * 100 if responses else 0
        session.xp_earned = int(session.total_score * 0.5) # 0.5 XP per percentage point
        
        db.commit()
        return session

    @staticmethod
    def log_proctoring_event(db: Session, session_id: int, event_type: str):
        event = InterviewProctoringLog(
            session_id=session_id,
            event_type=event_type
        )
        db.add(event)
        db.commit()
        return event

    @staticmethod
    def get_session_report(db: Session, session_id: int):
        session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
        if not session:
            return None
        
        questions = db.query(InterviewQuestion).filter(InterviewQuestion.session_id == session_id).all()
        results = []
        for q in questions:
            resp = db.query(InterviewResponse).filter(InterviewResponse.question_id == q.id).first()
            results.append({
                "question": q.text,
                "type": q.type,
                "transcript": resp.transcript if resp else None,
                "evaluation": resp.evaluation_json if resp else None
            })
            
        return {
            "session_id": session.id,
            "track": session.track,
            "score": session.total_score,
            "results": results
        }
