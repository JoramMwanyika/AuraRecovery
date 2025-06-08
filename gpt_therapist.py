import os
import openai

class GPTTherapist:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        self.client = openai.OpenAI(api_key=self.api_key)

    def get_response(self, messages):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm having trouble connecting right now. Please try again later. Error: {str(e)}" 