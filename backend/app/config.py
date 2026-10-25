from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite+aiosqlite:///./opspilot.db"
    session_secret: str = "change-me-in-development"
    token_encryption_key: str = "ZGF2ZWxvcG1lbnQta2V5LWZvci1vcHNwaWxvdC0xMjM0NTY3OA=="
    github_client_id: str = ""
    github_client_secret: str = ""
    app_url: str = "http://localhost:8000"

settings = Settings()
