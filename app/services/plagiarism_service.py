import re
from typing import List, Set

class PlagiarismService:
    @staticmethod
    def tokenize(code: str) -> List[str]:
        # Remove comments and whitespace, then tokenize by common programming symbols and keywords
        # This is a basic tokenizer for Jaccard similarity
        code = re.sub(r'#.*', '', code)
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
        tokens = re.findall(r'[a-zA-Z_]\w*|[0-9]+|[\+\-\*/%=\(\)\[\]\{\};,]', code)
        return tokens

    @staticmethod
    def calculate_jaccard_similarity(code_a: str, code_b: str) -> float:
        tokens_a = set(PlagiarismService.tokenize(code_a))
        tokens_b = set(PlagiarismService.tokenize(code_b))
        
        if not tokens_a and not tokens_b:
            return 0.0
            
        intersection = tokens_a.intersection(tokens_b)
        union = tokens_a.union(tokens_b)
        
        return len(intersection) / len(union)

    @staticmethod
    def scan_submission(db_session, submission_id: int, current_code: str):
        from app.db.models import ProjectSubmission
        
        # Get all approved submissions to compare against
        others = db_session.query(ProjectSubmission).filter(
            ProjectSubmission.id != submission_id,
            ProjectSubmission.status == "approved"
        ).all()
        
        max_similarity = 0.0
        for other in others:
            # In a real app, we would fetch the code content from the code_url
            # For MVP, we'll assume we have the content or compare metadata for now
            # similarity = PlagiarismService.calculate_jaccard_similarity(current_code, other.code_content)
            pass
            
        return max_similarity
