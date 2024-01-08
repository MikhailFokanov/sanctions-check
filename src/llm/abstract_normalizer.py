import openai

from sqlalchemy import select
from loguru import logger
from abc import ABC, abstractmethod

from ..database.models import LLMResponse


class Normalizer(ABC):
    @abstractmethod
    def _parse_model_ans(self, completion):
        pass

    def _chat_completion(self, prompt):
        chat_completion = openai.ChatCompletion.create(
            # engine=self.model_name,
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        logger.info(chat_completion)
        return self._parse_model_ans(chat_completion.choices[0].message.content)

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
