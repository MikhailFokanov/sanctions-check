#!/usr/bin/env python3
import json
import openai

from loguru import logger

from src.config import gpt_settings
from .abstract_normalizer import Normalizer


class GPTNormalizer(Normalizer):
    def __init__(self, db) -> None:
        openai.api_key = gpt_settings.OPENAI_API_KEY
        self.model_name = gpt_settings.OPENAI_MODEL_NAME
        self.db = db

    def _parse_model_ans(self, completion):
        normalized_name = json.loads(completion)["name"]
        logger.info(normalized_name)
        return normalized_name
