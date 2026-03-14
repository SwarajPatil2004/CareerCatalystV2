from app.services.skill_intelligence import SkillIntelligenceService

def test_analysis():
    test_cases = [
        "Led a team of 5 to increase revenue by 20% within 6 months.",
        "Worked on various technologies and fixed some bugs.",
        "Implemented a new caching layer using Redis which reduced latency significantly.",
        "Designed and built a full-stack application for managing library resources using React and Node.js.",
        "a short bullet",
        "This is a very long bullet point that tries to explain every single detail of the project but ends up being way too wordy and hard to read for a recruiter who only spends 6 seconds on a resume anyway so keep it short."
    ]

    for i, text in enumerate(test_cases):
        print(f"\nTest Case {i+1}: '{text}'")
        analysis = SkillIntelligenceService.analyze_bullet_point(text)
        print(f"  Verb: {analysis.has_action_verb}")
        print(f"  Metric: {analysis.has_metric}")
        print(f"  Length OK: {analysis.length_ok}")
        if analysis.suggested_improvement:
            print(f"  Suggestion: {analysis.suggested_improvement}")
        else:
            print("  Status: Excellent bullet!")

if __name__ == "__main__":
    test_analysis()
