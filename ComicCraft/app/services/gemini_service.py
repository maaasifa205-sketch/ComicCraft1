import json
import re

from app.config import settings
from app.services.mock_ai import make_mock_story


def _get_client():

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add it to .env or keep MOCK_MODE=true."
        )

    from google import genai

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def _extract_json(text: str):

    text = text.strip()

    # Remove Markdown code fences.
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    # Try to find a JSON array inside the response.
    start = text.find("[")
    end = text.rfind("]")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "Gemini did not return valid JSON."
        )

    return json.loads(
        text[start:end + 1]
    )


def generate_story(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> list[dict]:

    if settings.mock_mode:

        return make_mock_story(
            character_name,
            setting,
            tone,
            art_style,
        )

    client = _get_client()

    prompt = f"""
You are the story engine for an application called ComicCraft.

Create exactly {settings.panel_count} connected comic panels.

User story idea:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

Return ONLY a JSON array.

Do not use Markdown.
Do not add explanations.

Each item MUST contain:

number
title
scene_description
caption
narration
image_prompt

Rules:

1. Use panel numbers 1 through {settings.panel_count}.
2. The story must have a clear beginning, development, challenge and ending.
3. Keep the same main character throughout.
4. Keep narration short and natural.
5. image_prompt must describe visual content.
6. Do not put text, speech bubbles, logos or watermarks inside image_prompt.
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    data = _extract_json(
        response.text
    )

    if (
        not isinstance(data, list)
        or len(data) != settings.panel_count
    ):
        count = (
            len(data)
            if isinstance(data, list)
            else 0
        )

        raise ValueError(
            f"Gemini returned {count} panels; "
            f"expected {settings.panel_count}."
        )

    cleaned = []

    for index, item in enumerate(
        data,
        start=1,
    ):

        if not isinstance(item, dict):
            raise ValueError(
                f"Panel {index} is not a JSON object."
            )

        cleaned.append(
            {
                "number": index,
                "title": str(
                    item.get(
                        "title",
                        f"Panel {index}",
                    )
                ),
                "scene_description": str(
                    item.get(
                        "scene_description",
                        "",
                    )
                ),
                "caption": str(
                    item.get(
                        "caption",
                        "",
                    )
                ),
                "narration": str(
                    item.get(
                        "narration",
                        "",
                    )
                ),
                "image_prompt": str(
                    item.get(
                        "image_prompt",
                        "",
                    )
                ),
            }
        )

    return cleaned