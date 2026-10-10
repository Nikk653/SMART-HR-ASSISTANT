import os
from google import genai


class GeminiAPI:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key:

            self.client = genai.Client(api_key=api_key)

        else:

            self.client = None

    def ask(self, question):

        if self.client is None:

            return None

        try:

            response = self.client.models.generate_content(

                model="gemini-2.5-flash",

                contents=question

            )

            return response.text

        except Exception:

            return None