import os

import httpx


class LLMService:
    def __init__(self):
        self.ollama_url = os.getenv(
            "OLLAMA_URL",
            "http://localhost:11434",
        )

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "qwen3:8b",
        )

    def generate(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]