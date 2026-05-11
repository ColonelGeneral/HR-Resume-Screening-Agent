from __future__ import annotations

from collections import OrderedDict
import re
from typing import Iterable


PROMPT_INJECTION_PATTERNS = (
    "ignore previous instructions",
    "system prompt",
    "developer message",
    "assistant:",
    "<|system|>",
)


SKILL_NORMALIZATION = {
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "ml": "machine learning",
    "nlp": "natural language processing",
    "llm": "large language models",
    "sqlalchemy": "sqlalchemy",
    "fastapi": "fastapi",
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    seen: OrderedDict[str, None] = OrderedDict()
    for item in items:
        cleaned = normalize_text(item).lower()
        if cleaned:
            seen.setdefault(cleaned, None)
    return list(seen.keys())


def normalize_skill(skill: str) -> str:
    cleaned = normalize_text(skill).lower().replace("/", " ")
    cleaned = re.sub(r"[^a-z0-9+\-. ]", "", cleaned)
    return SKILL_NORMALIZATION.get(cleaned, cleaned)


def normalize_skills(skills: Iterable[str]) -> list[str]:
    normalized = [normalize_skill(skill) for skill in skills]
    return dedupe_preserve_order(normalized)


def detect_prompt_injection(text: str) -> bool:
    lowered = (text or "").lower()
    return any(pattern in lowered for pattern in PROMPT_INJECTION_PATTERNS)


def mask_pii(text: str) -> str:
    masked = re.sub(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}", "[EMAIL]", text or "")
    masked = re.sub(r"\b(?:\+?\d[\d\s\-()]{7,}\d)\b", "[PHONE]", masked)
    return masked


def extract_years_from_text(text: str) -> float:
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", (text or "").lower())
    values = [float(match) for match in matches]
    return max(values) if values else 0.0


def sentence_split(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", normalize_text(text))
    return [part.strip() for part in parts if part.strip()]
