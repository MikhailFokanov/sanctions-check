#!/usr/bin/env python3
import ast
import json
import os
import ast
import openai
from langchain.prompts import PromptTemplate
# from dotenv import load_dotenv, find_dotenv

# _ = load_dotenv(find_dotenv('pdf_diff/diff/.env'))
# openai.api_key = os.environ.get('GPT_API_KEY')
# MODEL_NAME = os.getenv('GPT_MODEL', 'gpt-4')

openai.api_key = 'INSERT_API_KEY'
MODEL_NAME = 'gpt-4'

TEMPLATES = [
    "Please provide english normalized name for {original_name}. The response MUST CONTAIN ONLY JSON LIKE THIS: ('name': 'THE_ENGLISH_NAME_HERE')",
    '''Please provide English normalized names for the following list of names: {original_name}. The response MUST CONTAIN ONLY JSON LIKE THIS: [(original_name: normalized_english_name)]'''
]
BULK_NAMES = ['محمد يحيى معل','صالح مسفر صالح الشاعر','Иван Иванов','Бойко Драгонов','محمود ابراهيم سعيد']

def gpt_chat_completion(prompt, model_name=MODEL_NAME, verbose=False):
    chat_completion = openai.ChatCompletion.create(model=model_name, messages=[{"role": "user", "content": prompt}])
    if verbose:
        return chat_completion
    return chat_completion.choices[0].message.content

def gpt_name_normalization(orig_name, template = 0):
    task = TEMPLATES[template]
    prompt = PromptTemplate.from_template(task)
    input_prompt = prompt.format(original_name=orig_name)
    # import pdb; pdb.set_trace()
    print(input_prompt)
    response = ast.literal_eval(gpt_chat_completion(input_prompt))
    # response = json.loads(gpt_chat_completion(input_prompt))['name']
    # import pdb; pdb.set_trace()
    return response

def gpt_bulk_conseq_handling(bulk, prompt = 0):
    response = {}
    for orig_name in bulk:
        try:
            result = gpt_name_normalization(orig_name, prompt)
        except:
            continue
        # import pdb; pdb.set_trace()
        response[orig_name] = result['name']
    return response

def gpt_bulk_parallel_handling(bulk, prompt = 1, retry = 3):
    response = ''
    result = {}
    for i in range(0, retry):
        i += 1
        try:
            response = gpt_name_normalization(str(bulk), prompt)
            # print(response)
        except:
            print('oops')
            continue
        if response: break
    for pair in [{item['original_name']: item['normalized_english_name']} for item in response]:
        # import pdb; pdb.set_trace()
        result.update(pair)
    return result

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

    # print(gpt_name_normalization("جهاد محمد سلطان"))

    print(gpt_bulk_conseq_handling(BULK_NAMES, 0))
    print('______________')
    print(gpt_bulk_parallel_handling(BULK_NAMES, 1, 3))
