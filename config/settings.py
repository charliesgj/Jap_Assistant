from dotenv import load_dotenv
from types import SimpleNamespace
import os
load_dotenv()
class Settings:
    def __init__(self):
        settings_dict = {
            "openai": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-3.5-turbo",
            "temperature": 0.5,
            "max_retries": 3,
            "max_tokens": 1000
        },
        "anthropic": {
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "model": "claude-3-7-sonnet-20250219",
            "temperature": 0.5,
            "max_retries": 3,
            "max_tokens": 1000
        },
        "llama": {
            "base_url": "http://localhost:11434",
            "api_key": "LLAMA_API_KEY",
            "model": "llama3-8b-8192",
            "temperature": 0.5,
            "max_retries": 3,
            "max_tokens": 1000
        }
    }
        for key, value in settings_dict.items():
            setattr(self, key, SimpleNamespace(**value))

def get_settings():
    return Settings()