import os


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "NoteFlow Auth Service")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()