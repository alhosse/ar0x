import os
import yaml
import httpx
from pathlib import Path
from typing import Dict, Any, Optional


class UnifiedLLMClient:
    """
    Model-Agnostic LLM Client for ar0x.
    Supports:
      - Local LLMs via Ollama (qwen2.5-coder, llama3.1, mistral, etc.)
      - Google Gemini API (gemini-2.5-flash, gemini-2.5-pro)
      - OpenAI / Compatible APIs (gpt-4o, gpt-4o-mini, Groq, DeepSeek, OpenRouter)
      - Anthropic Claude API (claude-3-5-sonnet, etc.)
    """

    def __init__(
        self,
        config_path: str = "config/settings.yaml",
        provider_override: Optional[str] = None,
        model_override: Optional[str] = None,
    ):
        cfg_file = Path(config_path)
        if cfg_file.exists():
            config = yaml.safe_load(cfg_file.read_text(encoding="utf-8")) or {}
            llm_cfg = config.get("llm", {})
        else:
            llm_cfg = {}

        self.provider = (provider_override or llm_cfg.get("provider", "ollama")).lower()
        self.model = model_override or llm_cfg.get("model", "qwen2.5-coder:7b")
        self.base_url = llm_cfg.get("base_url", "http://127.0.0.1:11434")
        self.temperature = float(llm_cfg.get("temperature", 0.1))
        self.timeout = int(llm_cfg.get("timeout_seconds", 60))

        # Load API key from config or environment variables (AR0X_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY, etc.)
        self.api_key = (
            llm_cfg.get("api_key")
            or os.getenv("AR0X_API_KEY")
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
            or ""
        )

    def generate_reasoning(self, finding: Dict[str, Any]) -> str:
        """
        Dispatches the security finding to the configured LLM provider (Cloud or Local)
        to generate contextual XAI reasoning and remediation code.
        """
        prompt = (
            "You are an expert Web Application Security Auditor within the ar0x framework.\n"
            "Analyze the following verified security finding and provide a concise, "
            "2-sentence technical explanation and secure remediation example:\n"
            f"- Title: {finding.get('title')}\n"
            f"- CWE: {finding.get('cwe_id')}\n"
            f"- OWASP: {finding.get('owasp_category')}\n"
            f"- Evidence: {finding.get('evidence')}\n"
        )

        try:
            if self.provider == "ollama":
                return self._call_ollama(prompt)
            elif self.provider == "gemini":
                return self._call_gemini(prompt)
            elif self.provider in ("openai", "groq", "deepseek", "openrouter"):
                return self._call_openai_compatible(prompt)
            elif self.provider == "anthropic":
                return self._call_anthropic(prompt)
            else:
                return f"[Unsupported LLM Provider '{self.provider}'] Fallback: {finding.get('remediation', '')}"
        except Exception:
            return f"[Offline Fallback - {self.provider.upper()} unreachable]: {finding.get('remediation', '')}"

    def _call_ollama(self, prompt: str) -> str:
        url = f"{self.base_url.rstrip('/')}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self.temperature},
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json().get("response", "").strip()

    def _call_gemini(self, prompt: str) -> str:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": self.temperature},
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    def _call_openai_compatible(self, prompt: str) -> str:
        default_urls = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "groq": "https://api.groq.com/openai/v1/chat/completions",
            "deepseek": "https://api.deepseek.com/v1/chat/completions",
            "openrouter": "https://openrouter.ai/api/v1/chat/completions",
        }
        url = default_urls.get(self.provider, f"{self.base_url.rstrip('/')}/v1/chat/completions")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()

    def _call_anthropic(self, prompt: str) -> str:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": 512,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()["content"][0]["text"].strip()
