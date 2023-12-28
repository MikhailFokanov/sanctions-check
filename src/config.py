from pydantic_settings import BaseSettings, SettingsConfigDict


class ElasticSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    ELASTIC_URL: str


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    @property
    def db_uri(self):
        return f'postgresql://{self.POSTGRES_USER_DB}:{self.POSTGRES_PASSWORD}@localhost:5432/{self.POSTGRES_USER_DB}'


class OpenAISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str = 'gpt-3.5-turbo'


openai_settings = OpenAISettings()
elastic_settings = ElasticSettings()
postgres_settings = PostgresSettings()
