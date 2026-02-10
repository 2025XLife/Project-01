import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from openai import OpenAI
from config_loader import get_config
from core.llm.utils import parse_messages_to_str, parse_response_to_str


def get_llm_client() -> OpenAI:
    config = get_config()
    return OpenAI(
        api_key=config["api_model"]["api_key"],
        base_url=config["api_model"]["base_url"]
    )


def get_model_name() -> str:
    config = get_config()
    return config.get("api_model", {}).get("model", "deepseek-chat")


class LLMClient:

    def __init__(self, model: Optional[str] = None):
        self.client = get_llm_client()
        self.model = model or get_model_name()

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        **kwargs
        ) -> str:
        start_time = datetime.now()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        content = resp.choices[0].message.content
        return content

    def chat_with_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        **kwargs
        ) -> dict:
        start_time = datetime.now()
        # Filter out unsupported parameters that cause TypeError
        unsupported_params = ['temperature', 'top_p', 'top_k']
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in unsupported_params}
        resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                response_format={'type': 'json_object'},
                **filtered_kwargs
            )
        content = resp.choices[0].message.content
        return content

    def extract_keywords(self, question: str, max_count: int = 3) -> List[str]:
        prompt = f"Extract {max_count} medical/health entity keywords from the following question, only return JSON list format:\nQuestion: {question}"
        messages = [{"role": "user", "content": prompt}]
        try:
            content = self.chat(messages, temperature=0.1)
            import re
            match = re.search(r'\[.*\]', content)
            if match:
                return json.loads(match.group())
            return []
        except Exception as e:
            print(f"Failed to extract keywords: {e}")
            return []


_llm_client: Optional[LLMClient] = None


def get_llm():
    """Get global LLM client instance, use api/local model preferentially"""
    global _llm_client
    if _llm_client is None:
        from core.llm.local_llm import is_local_mode, get_local_llm
        _llm_client = LLMClient()
        """
        if is_local_mode():
            _llm_client = get_local_llm()
        else:
            _llm_client = LLMClient()
        """
    return _llm_client
