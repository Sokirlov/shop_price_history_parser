from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_URL_CATEGORIES: str
    API_URL_PRODUCTS: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()