import re
from typing import Optional, List
from pydantic import BaseModel

class BulletAnalysis(BaseModel):
    has_action_verb: bool
    has_metric: bool
    length_ok: bool
    suggested_improvement: Optional[str] = None

class SkillIntelligenceService:
    ACTION_VERBS = {
        "led", "designed", "implemented", "developed", "managed", 
        "optimized", "increased", "decreased", "improved", "created",
        "spearheaded", "coordinated", "executed", "initiated", "built",
        "automated", "mentored", "delivered", "presented", "analyzed"
    }

    @staticmethod
    def analyze_bullet_point(text: str) -> BulletAnalysis:
        if not text:
            return BulletAnalysis(
                has_action_verb=False,
                has_metric=False,
                length_ok=False,
                suggested_improvement="Please provide a bullet point to analyze."
            )

        # 1. Action Verb Check (First word or beginning of the sentence)
        words = text.lower().strip().split()
        if not words:
            return BulletAnalysis(has_action_verb=False, has_metric=False, length_ok=False)
            
        first_word = words[0].rstrip(',.')
        has_action_verb = first_word in SkillIntelligenceService.ACTION_VERBS

        # 2. Metric Detection (numbers, percentages)
        # Regex for numbers, decimals, and percentage signs
        metric_pattern = r'\d+(?:\.\d+)?%?'
        has_metric = bool(re.search(metric_pattern, text))

        # 3. Length Validation (8-35 words)
        word_count = len(words)
        length_ok = 8 <= word_count <= 35

        # 4. Rule-based suggestions
        suggestions = []
        if not has_action_verb:
            suggestions.append("Start with a strong action verb (e.g., 'Developed', 'Optimized').")
        if not has_metric:
            suggestions.append("Add a measurable outcome or metric (e.g., 'improved performance by 20%').")
        if word_count < 8:
            suggestions.append("This bullet point is a bit short. Try to add more detail about your impact.")
        elif word_count > 35:
            suggestions.append("This bullet point is quite long. Try to keep it concise and focused on one key achievement.")

        suggested_improvement = " ".join(suggestions) if suggestions else None

        return BulletAnalysis(
            has_action_verb=has_action_verb,
            has_metric=has_metric,
            length_ok=length_ok,
            suggested_improvement=suggested_improvement
        )
