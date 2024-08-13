from openai import OpenAI

from src.main.config import settings


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPEN_AI_KEY)

    def check_text_moderation(self, text: str) -> bool:
        """
        Checks the text for the presence of offensive language, insults, etc., using the GPT-3.5-turbo model.
        Returns True if the text contains undesirable content, otherwise False.
        """
        prompt = (
            f"Does the following text contain offensive,"
            f" inappropriate, or harmful content?"
            f" Answer 'Yes' or 'No'.\n\nText: {text}"
        )

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a content moderation assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=10,
            temperature=0.0
        )

        moderation_result = response.choices[0].message.content.strip().lower()

        if moderation_result == 'yes':
            return True

        return False


open_ai_service = OpenAIService()
