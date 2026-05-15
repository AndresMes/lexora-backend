import os

from app.modules.llm_extractor.llm_extractor import LLMExtractor


def get_llm_extractor() -> LLMExtractor:
    return LLMExtractor(model_name=os.getenv("GEMINI_MODEL"))