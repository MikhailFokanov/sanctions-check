#!/usr/bin/env python3
import ast
import json
import logging
import os
import openai
from src.config import openai_settings
from sqlalchemy import select
from src.database.models import GPTResponse


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class GPTNormalizer():
    def __init__(self, db) -> None:
        openai.api_key = openai_settings.OPENAI_API_KEY
        self.db = db
        
    def _gpt_chat_completion(self, prompt, model_name=openai_settings.OPENAI_MODEL_NAME, verbose=False):
        chat_completion = openai.ChatCompletion.create(model=model_name, messages=[{"role": "user", "content": prompt}])
        if verbose:
            return chat_completion
        return chat_completion.choices[0].message.content

    def _get_cached_normalization(self, name):
        res = self.db.sql_query(query=select(GPTResponse).where(GPTResponse.keyword == name))
        if res:
            return res.normalized
        return None


    def gpt_name_normalize(self, name):
        cached_normalization = self._get_cached_normalization(name)

        if cached_normalization:
            logging.info(f'{name} - normalization is in cache')
            return cached_normalization
        else:
            logging.info(f'{name} - normalization is not in cache, requesting by api')
            prompt = f"Please provide english normalized name for "+name+'. The response MUST CONTAIN ONLY JSON LIKE THIS:  {"name": "THE_ENGLISH_NAME_HERE"}'
            normalized = json.loads(self._gpt_chat_completion(prompt))['name']
            self.db.create_object(model_class=GPTResponse,
                                  keyword=name,
                                  normalized=normalized)
            return normalized

# def gpt_response(prompt, model_name=MODEL_NAME, verbose=False):
#     response = gpt_chat_completion(prompt=prompt, model_name=model_name, verbose=verbose)
#     print(response)
#     return response

# def start_chat(model_name=MODEL_NAME):
#     while True:
#         user_input = input("Вы: ")
#         if user_input.lower() == 'exit':
#             break
#         elif user_input != "":
#             print(f"Чат {model_name}: ", gpt_chat_completion(prompt=user_input, model_name=model_name))



if __name__ == '__main__':

    # question = 'В чём смысл жизни?'
    # response = gpt_chat_completion(question)
    # print(response)
    # gpt_response(question)
    # start_chat()

    # import sys
    # sys.path.append('..')
    # from gpt_module import start_chat
    # import openai

    # openai.api_type = "azure"
    # openai.api_version = "2023-03-15-preview"
    # openai.api_key = '0665d80e70914305bbbd2117c17f9ff5'
    # openai.api_base = "https://ai-proxy.lab.epam.com"

    # deployment_name = "gpt-35-turbo"

    # Please only use this one if you absolutely need it. It's slower and more expensive.
    # deployment_name = "gpt-4"
    # deployment_name = "gpt-4-32k"

    # For embeddings only, but small private models may perform better and cheaper
    # https://huggingface.co/spaces/mteb/leaderboard
    # deployment_name = "text-embedding-ada-002"

    # message = "how are you?"

    # print(openai.ChatCompletion.create(
    #     engine=deployment_name,
    #     temperature=0,
    #     messages=[
    #     {
    #         "role": "assistant",
    #         "content": message
    #     }
    #     ]
    # ))



    #print(gpt_name_normalization("иванов иван иванович"))

    print(gpt_name_normalization("جهاد محمد سلطان"))
