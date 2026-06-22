from dataclasses import dataclass
from pathlib import Path
import os


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    with path.open(encoding='utf-8') as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue

            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env_path = Path(path) if path else Path.cwd() / '.env'
    load_env_file(env_path)

    token = os.getenv('BOT_TOKEN')
    if not token:
        raise RuntimeError('BOT_TOKEN не задан в переменных окружения или в файле .env')

    admin_ids_value = os.getenv('ADMIN_IDS', '')
    admin_ids = [int(item.strip()) for item in admin_ids_value.split(',') if item.strip().isdigit()]

    return Config(tg_bot=TgBot(
        token=token.strip(),
        admin_ids=admin_ids
    ))
