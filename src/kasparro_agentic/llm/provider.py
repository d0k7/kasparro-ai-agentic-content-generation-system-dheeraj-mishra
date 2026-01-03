from __future__ import annotations

import json
import logging
import os
import re
from typing import TypeVar, cast

import requests
from pydantic import BaseModel

from kasparro_agentic.models import (
    ComparisonPage,
    FAQPage,
    FictionalProduct,
    ProductPage,
    QuestionList,
)

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


def _truthy_env(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "y", "on"}


def _extract_first_json_object(text: str) -> dict:
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in model output.")
    return json.loads(match.group(0))


def _extract_product_name(prompt: str) -> str:
    m = re.search(r"-\s*product_name:\s*(.+)", prompt)
    if m:
        return m.group(1).strip()
    m2 = re.search(r'product:\s*"(.*?)"', prompt, re.IGNORECASE)
    if m2:
        return m2.group(1).strip()
    return "the product"


# ----------------------------
# Deterministic mock payloads (CI/test safe)
# ----------------------------
def _mock_question_list(product_name: str) -> dict:
    # IMPORTANT: First 3 questions match your test assertions exactly.
    questions = [
        {"category": "Benefits", "question": f"What are the main benefits of using {product_name}?"},
        {"category": "Usage", "question": f"How do I apply {product_name}?"},
        {"category": "Usage", "question": "Is it suitable for all skin types?"},
        {"category": "Ingredients", "question": f"What are the key ingredients in {product_name}?"},
        {"category": "Routine", "question": f"Can I use {product_name} with other skincare products?"},
        {"category": "Frequency", "question": f"How often should I use {product_name}?"},
        {"category": "Safety", "question": f"Are there any precautions or side effects of {product_name}?"},
        {"category": "Storage", "question": f"How should I store {product_name} properly?"},
        {"category": "Results", "question": f"How long does it take to see results with {product_name}?"},
        {"category": "Sunscreen", "question": f"Should I apply sunscreen when using {product_name}?"},
        {"category": "Layering", "question": f"Can I layer {product_name} with retinol or acids?"},
        {"category": "Irritation", "question": f"What should I do if {product_name} irritates my skin?"},
        {"category": "Price", "question": f"Is {product_name} worth its price?"},
        {"category": "Vitamin C %", "question": f"What is the concentration of actives in {product_name}?"},
        {"category": "Informational", "question": f"What is {product_name} used for?"},
    ]
    return {"questions": questions}


MOCK_FAQ = {
    "page_type": "faq",
    "product_name": "GlowBoost Vitamin C Serum",
    "disclaimer": "Informational only. Not medical advice. Patch test when trying new skincare.",
    "items": [
        {
            "category": "Informational",
            "question": "What is GlowBoost Vitamin C Serum?",
            "answer": "GlowBoost Vitamin C Serum is a Vitamin C serum generated only from the provided dataset fields.",
        }
    ],
}

MOCK_PRODUCT_PAGE = {
    "page_type": "product_page",
    "product_name": "GlowBoost Vitamin C Serum",
    "brand": "GlowBoost",
    "price_inr": 799,
    "summary": "A Vitamin C serum described only using the provided dataset fields.",
    "highlights": {
        "best_for": "Oily, Combination",
        "key_ingredients": ["Vitamin C", "Hyaluronic Acid", "Niacinamide"],
        "benefits": ["Brightening", "Even skin tone", "Antioxidant support"],
        "skin_types": ["Oily", "Combination"],
    },
}

MOCK_FICTIONAL_PRODUCT = {
    "product_name": "GlowBoost Radiance C+ Serum",
    "brand": "GlowBoost Labs",
    "category": "Skincare",
    "price_inr": 999,
    "key_ingredients": ["8% Vitamin C", "Ferulic Acid", "Vitamin E"],
    "benefits": ["Brightening", "Helps reduce dullness", "Antioxidant support"],
    "skin_type": ["Normal", "Combination"],
    "concentration": "8% Vitamin C",
    "how_to_use": "Apply 2–3 drops on clean face in the morning. Follow with moisturizer and sunscreen.",
    "side_effects": "Not specified in the provided dataset.",
}

MOCK_COMPARISON = {
    "page_type": "comparison_page",
    "disclaimer": "Note: Product B is fictional and generated for comparison purposes only.",
    "product_a": {
        "product_name": "GlowBoost Vitamin C Serum",
        "price_inr": 799,
        "key_ingredients": ["Vitamin C", "Hyaluronic Acid", "Niacinamide"],
        "benefits": ["Brightening", "Even skin tone", "Antioxidant support"],
        "skin_type": ["Oily", "Combination"],
    },
    "product_b": {
        "product_name": "GlowBoost Radiance C+ Serum",
        "price_inr": 999,
        "key_ingredients": ["8% Vitamin C", "Ferulic Acid", "Vitamin E"],
        "benefits": ["Brightening", "Helps reduce dullness", "Antioxidant support"],
        "skin_type": ["Normal", "Combination"],
    },
    "comparison": {
        "similarities": {
            "key_ingredients": "Both contain Vitamin C and focus on antioxidant support.",
            "benefits": "Both aim to brighten and improve the appearance of skin tone.",
        },
        "differences": {
            "ingredients": "Product A includes hydrating/supporting ingredients; Product B focuses on antioxidant synergy ingredients.",
            "skin_type": "Product A targets oily/combination; Product B targets normal/combination.",
            "pricing": "Product A is ₹799, Product B is ₹999.",
        },
    },
}


class LLMProvider:
    def invoke_structured(self, prompt: str, schema: type[T]) -> T:
        raise NotImplementedError

    def invoke_text(self, prompt: str) -> str:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    def invoke_structured(self, prompt: str, schema: type[T]) -> T:
        product_name = _extract_product_name(prompt)

        if schema is QuestionList:
            return cast(T, schema.model_validate(_mock_question_list(product_name)))
        if schema is FAQPage:
            return cast(T, schema.model_validate(MOCK_FAQ))
        if schema is ProductPage:
            return cast(T, schema.model_validate(MOCK_PRODUCT_PAGE))
        if schema is FictionalProduct:
            return cast(T, schema.model_validate(MOCK_FICTIONAL_PRODUCT))
        if schema is ComparisonPage:
            return cast(T, schema.model_validate(MOCK_COMPARISON))

        return cast(T, schema.model_validate({}))

    def invoke_text(self, prompt: str) -> str:
        product_name = _extract_product_name(prompt)
        return (
            f"{product_name} is a skincare product.\n\n"
            "Safe-use tips:\n"
            "1) Patch test first.\n"
            "2) Apply on clean, dry skin.\n"
            "3) Start slowly and increase frequency as tolerated.\n"
            "4) Use sunscreen in daytime routines.\n"
            "5) Stop use if irritation persists."
        )


class HuggingFaceProvider(LLMProvider):
    def __init__(self) -> None:
        self.token = os.getenv("HF_API_TOKEN", "").strip()
        self.model = os.getenv("KASPARRO_HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3").strip()
        self.timeout_s = float(os.getenv("KASPARRO_HF_TIMEOUT_S", "60").strip())
        self.max_new_tokens = int(os.getenv("KASPARRO_HF_MAX_NEW_TOKENS", "700").strip())

        if not self.token:
            raise RuntimeError("HF_API_TOKEN is not set (required for KASPARRO_LLM_MODE=hf).")

        self.url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def invoke_text(self, prompt: str) -> str:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": self.max_new_tokens,
                "temperature": 0.2,
                "return_full_text": False,
            },
        }
        resp = requests.post(self.url, headers=self.headers, data=json.dumps(payload), timeout=self.timeout_s)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list) and data and isinstance(data[0], dict) and "generated_text" in data[0]:
            return str(data[0]["generated_text"]).strip()

        if isinstance(data, dict) and "generated_text" in data:
            return str(data["generated_text"]).strip()

        if isinstance(data, dict) and "error" in data:
            raise RuntimeError(f"HF error: {data['error']}")

        return str(data)

    def invoke_structured(self, prompt: str, schema: type[T]) -> T:
        strict = _truthy_env("KASPARRO_LLM_STRICT", "0")
        raw = self.invoke_text(prompt)

        try:
            obj = _extract_first_json_object(raw)
            return cast(T, schema.model_validate(obj))
        except Exception as e:  # noqa: BLE001
            if strict:
                raise RuntimeError(f"HF structured parse/validate failed: {e}\nRaw:\n{raw}") from e
            logger.warning("HF structured output invalid; falling back to mock. Error=%s", e)
            return MockLLMProvider().invoke_structured(prompt, schema)


def build_llm_provider() -> LLMProvider:
    """
    Modes:
      - mock (default): deterministic, CI-friendly, no network.
      - hf: Hugging Face Inference API (real LLM) if HF_API_TOKEN is set.
    """
    mode = os.getenv("KASPARRO_LLM_MODE", "mock").strip().lower()

    if mode in ("", "mock"):
        return MockLLMProvider()

    if mode == "hf":
        try:
            return HuggingFaceProvider()
        except Exception as e:  # noqa: BLE001
            logger.warning("HF provider init failed (%s). Falling back to mock.", e)
            return MockLLMProvider()

    # Do NOT support broken puter-sdk mode in backend (browser Puter SDK is reliable)
    logger.warning("Unknown KASPARRO_LLM_MODE=%r. Falling back to mock.", mode)
    return MockLLMProvider()
