#!/usr/bin/env python3
import json
import openai
import re

from loguru import logger

from src.config import llama_settings
from .abstract_normalizer import Normalizer


class LlamaNormalizer(Normalizer):
    def __init__(self, db) -> None:
        openai.api_type = llama_settings.API_TYPE
        openai.api_version = llama_settings.API_VERSION
        openai.api_key = llama_settings.OPENAI_API_KEY
        openai.api_base = llama_settings.API_BASE
        self.model_name = llama_settings.OPENAI_MODEL_NAME
        self.db = db

    def _parse_model_ans(self, completion):
        json_regex = r"\{\"name\":\s*\"[^\"]+\"\}"
        model_answer = completion.choices[0].message.content
        match = re.search(json_regex, model_answer)
        try:
            parsed_json_ans = match.group(0)
        except AttributeError:
            logger.exception(f"Failed to parse model response: {model_answer}")
        normalized_name = json.loads(parsed_json_ans)["name"]

        logger.info(normalized_name)

        return normalized_name
