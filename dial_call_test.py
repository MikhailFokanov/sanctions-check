import openai
 
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_key = '0665d80e70914305bbbd2117c17f9ff5'
openai.api_base = "https://ai-proxy.lab.epam.com"

deployment_name = "gpt-35-turbo"
# Please only use this one if you absolutely need it. It's slower and more expensive.
# deployment_name = "gpt-4"
# deployment_name = "gpt-4-32k"

# For embeddings only, but small private models may perform better and cheaper
# https://huggingface.co/spaces/mteb/leaderboard
# deployment_name = "text-embedding-ada-002"
message = "how are you?"

print(openai.ChatCompletion.create(
  engine=deployment_name,
  temperature=0,
  messages=[
    {
      "role": "assistant",
      "content": message
    }
  ]
))