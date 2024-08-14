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

    def generate_reply(self, post_content: str, comment_content: str) -> str:
        prompt = f"""
            Post: {post_content}.
            Comment: {comment_content}.
            Reply:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                                   "Please generate a relevant and thoughtful reply "
                                   "to the following comment in the context of the post. "
                                   "Keep the reply within the allowed token limit and "
                                   "ensure the full response does not exceed 300 characters."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    },
                ],
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
            )

            reply = response.choices[0].message.content.strip()

            return reply
        except Exception as e:
            print(f"Error generating reply: {e}")
            return "Sorry, I couldn't generate a reply at this time."


open_ai_service = OpenAIService()
