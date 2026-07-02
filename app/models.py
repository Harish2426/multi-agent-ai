from google import genai
from google.genai import errors

from app.config import GEMINI_API_KEY

import time


class GeminiClient:

    def __init__(self):

        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(self, prompt):

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                return response.text

            except errors.ServerError:

                if attempt < 2:
                    time.sleep(2)
                    continue

                return "Gemini server is busy. Please try again."

            except Exception as e:

                return f"Error: {e}"


gemini = GeminiClient()