from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    mock_mode: bool = True

    gemini_api_key: str = ""
    hf_token: str = ""

    gemini_model: str = "gemini-2.5-flash"

    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    hf_provider: str = "auto"

    panel_count: int = 5

    app_name: str = "ComicCraft"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

APP_DIR = BASE_DIR / "app"

TEMPLATES_DIR = APP_DIR / "templates"

STATIC_DIR = APP_DIR / "static"

PANELS_DIR = STATIC_DIR / "panels"

EXPORTS_DIR = STATIC_DIR / "exports"

PANELS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)