import os


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "NoteFlow Auth Service")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "127.0.0.1")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5433")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "noteflow")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "noteflow_user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "noteflow_pass")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )


settings = Settings()