from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVER_IP: str
    SERVER_PORT: int
    SERVER_PASSWORD: str

    BOT_TOKEN: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()