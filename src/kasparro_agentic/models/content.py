from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Question:
    category: str
    question: str


@dataclass(frozen=True, slots=True)
class FAQItem:
    category: str
    question: str
    answer: str
