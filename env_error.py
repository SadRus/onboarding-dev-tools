from dotenv import load_dotenv
from pydantic import ValidationError

from env_settings import EnvSettings

load_dotenv()

# Получить ошибки валидации переменных окружения
try:
    ENV = EnvSettings()
except ValidationError as err:
    print(err)
