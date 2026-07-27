from typing import Dict, List


class AIService:
    supported_languages = ["en", "hi", "ta", "te", "bn", "mr", "gu", "kn", "ml", "pa"]

    @staticmethod
    def generate_content(prompt: str, language: str = "en") -> str:
        return f"[AI GENERATED {language.upper()} CONTENT] {prompt}"

    @staticmethod
    def translate_text(text: str, target_language: str) -> str:
        return f"[TRANSLATED TO {target_language.upper()}] {text}"

    @staticmethod
    def analyze_sentiment(text: str) -> Dict[str, str]:
        return {"sentiment": "neutral", "confidence": "0.82"}

    @staticmethod
    def personalize_message(text: str, audience_member: dict) -> str:
        name = audience_member.get("name", "Citizen")
        return f"Dear {name}, {text}"

    @staticmethod
    def build_audience_segments(members: List[dict], filter_data: dict) -> List[dict]:
        return [m for m in members if all(m.get(key) == value for key, value in filter_data.items() if value is not None)]
