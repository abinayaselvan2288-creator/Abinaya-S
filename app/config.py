from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "PocketSmart AI"

    secret_key: str = "change-this-in-production"

    gemini_api_key: str = ""

    # Keep this configurable because Gemini model names can change.
    gemini_model: str = "gemini-2.5-flash"

    database_url: str = "sqlite:///./pocketsmart.db"

    allowed_origins_raw: str = (
        "http://127.0.0.1:8000,"
        "http://localhost:8000"
    )

    token_expire_minutes: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def allowed_origins(self):
        return [
            origin.strip()
            for origin in self.allowed_origins_raw.split(",")
            if origin.strip()
        ]


settings = Settings()