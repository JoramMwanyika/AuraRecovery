import os
import requests
from config import Config

class GPTTherapist:
    def __init__(self):
        self.api_key = Config.OPENAI_ROUTER_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI Router API key not found. Please set the OPENAI_ROUTER_API_KEY environment variable.")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def get_response(self, messages):
        try:
            data = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": messages
            }
            
            response = requests.post(self.api_url, json=data, headers=self.headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"I apologize, but I'm having trouble connecting right now. Please try again later. Error: {str(e)}" 