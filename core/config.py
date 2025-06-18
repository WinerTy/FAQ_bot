from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import BaseModel


class BotConfig(BaseModel):
    token: str


class AppConfig(BaseSettings):
    bot: BotConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        env_prefix="APP__",
    )


conf = AppConfig()
