import json
import re


class FakeLLM:
    """Pretend AI for tests. Returns answers we queue up. Free and offline."""

    def __init__(self, responses: list[dict]):
        self.responses = list(responses)
        self.calls = []                  # remembers every question, for tests

    def complete_json(self, system: str, user: str) -> dict:
        self.calls.append((system, user))
        return self.responses.pop(0)


class OllamaLLM:
    """Free local open model via Ollama. Nothing leaves your laptop."""

    def __init__(self, model: str = "qwen3:8b"):
        self.model = model

    def complete_json(self, system: str, user: str) -> dict:
        import httpx
        r = httpx.post(
            "http://localhost:11434/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "format": "json",             # reply must be valid JSON
                "think": False,               # skip the <think> block, faster
                "stream": False,              # wait for the full answer
                "options": {"num_ctx": 8192}, # 8K context saves memory
            },
            timeout=600,
        )
        r.raise_for_status()
        return json.loads(r.json()["message"]["content"])


class ClaudeLLM:
    """Real Claude, for later when you buy API credits."""

    def __init__(self, model: str):
        from anthropic import Anthropic
        self.client = Anthropic()        # reads ANTHROPIC_API_KEY from .env
        self.model = model

    def complete_json(self, system: str, user: str) -> dict:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = msg.content[0].text
        return json.loads(re.search(r"\{.*\}", text, re.S).group(0))