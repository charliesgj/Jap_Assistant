from typing import Any, Dict, List, Type
import instructor
from anthropic import Anthropic
from openai import OpenAI
from config.settings import get_settings
from pydantic import BaseModel, Field


class LLMFactory:
    def __init__(self, provider: str):
        self.provider = provider
        self.settings = getattr(get_settings(), provider)
        self.client = self._intialize_client()
        print(self.settings)
    def _intialize_client(self) -> Any:
        client_initializer = {
            "openai": lambda s: instructor.from_openai(OpenAI(api_key=s.api_key)),
            "anthropic": lambda s: instructor.from_anthropic(
                Anthropic(api_key=s.api_key),
                mode=instructor.Mode.ANTHROPIC_JSON,
            ),
            "llama": lambda s: instructor.from_llama(
                OpenAI(base_url=s.base_url, api_key=s.api_key),
                mode=instructor.Mode.JSON,
            ),
        }
        initializer = client_initializer.get(self.provider)
        if initializer:
            return initializer(self.settings)
        raise ValueError(f"Provider {self.provider} not supported")
    
    def create_completion(
            self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
            ) -> Any:

            completion_params = {
                 "model":kwargs.get("model", self.settings.model),
                 "temperature":kwargs.get("temperature", self.settings.temperature),
                 "max_retries":kwargs.get("max_retries", self.settings.max_retries),
                 "max_tokens":kwargs.get("max_tokens", self.settings.max_tokens),
                 "response_model":response_model,
                 "messages":messages,
            }
            return self.client.chat.completions.create(**completion_params)

    

if __name__ == "__main__":
    class CompletionModel(BaseModel):
          response: str = Field(description="The response to the user's message")
          reasoning: str = Field(description="The reasoning for the response")

    messages = [
        {"role": "system", 
         "content": "You are a helpful assistant that can answer questions and help with tasks."},
        {"role": "user", "content": "What is the capital of France?"},
    ]

    llm = LLMFactory(provider="anthropic")
    completion = llm.create_completion(CompletionModel, messages)
    assert isinstance(completion, CompletionModel)
    print(f"Response: {completion.response}")
    print(f"Reasoning: {completion.reasoning}")
     
