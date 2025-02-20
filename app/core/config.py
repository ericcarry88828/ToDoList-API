import os
from typing import Literal
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DOTENV = os.path.join(BASE_DIR, ".env")
# DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class DBSetting(BaseSettings):
    ENV: Literal["dev", "prod", "test"] = "dev"
    MYSQL_DRIVER: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD:  str
    MYSQL_DATABASE: str

    # ASYNC_DB: bool = False

    model_config = SettingsConfigDict(
        env_file=DOTENV,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        base_url = (
            f"{self.MYSQL_DRIVER}://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )
        params = {
            "charset": "utf8mb4"
        }
        return f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"


settings = DBSetting()

if __name__ == "__main__":
    print(settings.DATABASE_URL)
