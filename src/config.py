from pydantic_settings import BaseSettings, SettingsConfigDict


class ElasticSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ELASTIC_URL: str
    FORCE_LOAD_DATA: bool = False


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    @property
    def db_uri(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:5432/{self.POSTGRES_DB}"


class LlamaSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    OPENAI_API_KEY: str
    API_TYPE: str = "azure"
    API_VERSION: str = "2023-03-15-preview"
    API_BASE: str = "https://ai-proxy.lab.epam.com"
    OPENAI_MODEL_NAME: str = "Llama-2-70B-chat-AWQ"


class GPTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    OPENAI_API_KEY: str
    # OPENAI_MODEL_NAME: str = "gpt-35-turbo"
    OPENAI_MODEL_NAME: str = "gpt-3.5-turbo"
    # 'gpt-35-turbo' - for dial gpt
    # 'gpt-3.5-turbo' - for standart gpt


llama_settings = LlamaSettings()
gpt_settings = GPTSettings()
elastic_settings = ElasticSettings()
postgres_settings = PostgresSettings()
