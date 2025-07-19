import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.config = {
            "HOST": os.getenv("HOST", None),
            "PORT": os.getenv("PORT", None),
            "DATABASE": os.getenv("DATABASE", None),
            "USER": os.getenv("USER", None),
            "PASSWORD": os.getenv("PASSWORD", None),
        }

    def get(self, key: str, default=None):
        value = self.config.get(key, default)
        if value is None:
            raise ValueError(f'Variable de entorno"{key}" es requerida ')
        return value


config = Settings()
