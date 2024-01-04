#!/usr/bin/env python3
import json
import openai
import re

from loguru import logger
from sqlalchemy import select

from src.config import llama_settings
from src.database.models import LLMResponse
from .normalizer_interface import Normalizer


class LlamaNormalizer(Normalizer):
    def __init__(self, db) -> None:
        openai.api_base = llama_settings.API_BASE
        self.db = db

    def _parse_model_ans(self, completion):
        normalized_name = json.loads(completion)["name"]
        logger.info(normalized_name)
        return normalized_name

    def _chat_completion(self, prompt, model_name=llama_settings.OPENAI_MODEL_NAME):
        chat_completion = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        logger.info(chat_completion)
        return self._parse_model_ans(chat_completion)

    def _get_cached_normalization(self, name):
        res = self.db.sql_query(
            query=select(LLMResponse).where(LLMResponse.keyword == name)
        )
        if res:
            return res.normalized
        return None

    def normalize(self, name):
        cached_normalization = self._get_cached_normalization(name)

        if cached_normalization:
            logger.info(f"{name} - normalization is in cache")
            return cached_normalization
        else:
            logger.info(f"{name} - normalization is not in cache, requesting by api")
            prompt = (
                f"Please provide english normalized name for {name}. "
                + 'The response MUST CONTAIN ONLY JSON LIKE THIS:  {"name": "THE_ENGLISH_NAME_HERE"}'
            )
            normalized = self._chat_completion(prompt)
            self.db.create_object(
                model_class=LLMResponse, keyword=name, normalized=normalized
            )
            return normalized
