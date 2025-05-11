from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file=r"D:\Restful\backend\.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:123456@localhost/lab"

    SMTP_TLS: bool = False
    SMTP_SSL: bool = True
    SMTP_PORT: int = 465
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None

settings = Settings()