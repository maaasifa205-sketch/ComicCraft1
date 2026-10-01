import re

from app.config import PANELS_DIR, settings
from app.services.mock_ai import make_mock_image


def _safe_filename(text: str) -> str:

    value = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        text,
    ).strip("_")

    return value[:50] or "comic_panel"


def generate_panel_image(
    prompt: str,
    panel_number: int,
    character_name: str,
) -> str:

    filename = (
        f"panel_{panel_number}_"
        f"{_safe_filename(character_name)}.png"
    )

    output_path = PANELS_DIR / filename

    # First run: local demo image.
    if settings.mock_mode:

        make_mock_image(
            output_path,
            panel_number,
            character_name,
        )

        return (
            f"/static/panels/{filename}"
        )

    if not settings.hf_token:

        raise RuntimeError(
            "HF_TOKEN is missing. "
            "Add it to .env or keep MOCK_MODE=true."
        )

    try:

        from huggingface_hub import InferenceClient

        client = InferenceClient(
            provider=settings.hf_provider,
            api_key=settings.hf_token,
        )

        image = client.text_to_image(
            prompt=prompt,
            model=settings.hf_image_model,
            width=1024,
            height=768,
        )

        image.save(
            output_path,
            "PNG",
        )

    except Exception as exc:

        raise RuntimeError(
            "Hugging Face image generation failed. "
            "Check HF_TOKEN, the image model and "
            f"your internet connection. Original error: {exc}"
        ) from exc

    return (
        f"/static/panels/{filename}"
    )