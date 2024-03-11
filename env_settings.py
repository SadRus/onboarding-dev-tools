from pydantic import BaseSettings, validator


# Написать вложенную схему валидации переменных окружения
class TelegramSettings(BaseSettings):
    BOT_TOKEN: str
    CHAT_ID: int

    @validator('BOT_TOKEN')
    def token_must_contain_colon(cls, v):
        if ':' not in v:
            raise ValueError('token must contain a colon')
        return v


class EnvSettings(BaseSettings):
    TG: TelegramSettings

    class Config:
        env_nested_delimiter = '__'
        case_sensitive = True
