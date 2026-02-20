from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings.
    Values can be overridden using environment variables.
    """

    SECRET_KEY: str = "your-secret-key-here-change-in-production-min-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


# Create a single settings instance to be imported across the app
settings = Settings()