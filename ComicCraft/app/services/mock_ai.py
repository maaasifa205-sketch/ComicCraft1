from pathlib import Path

from PIL import Image, ImageDraw


def make_mock_story(
    character: str,
    setting: str,
    tone: str,
    art_style: str,
) -> list[dict]:

    scenes = [
        (
            "The Beginning",
            f"{character} arrives in the {setting} and notices something unusual.",
        ),
        (
            "The Discovery",
            f"{character} discovers a mysterious clue hidden inside the {setting}.",
        ),
        (
            "The Journey",
            f"Following the clue, {character} travels deeper into the {setting}.",
        ),
        (
            "The Challenge",
            f"{character} faces a difficult obstacle but refuses to give up.",
        ),
        (
            "The Ending",
            f"{character} solves the problem and returns home with a new lesson.",
        ),
    ]

    panels = []

    for number, (title, description) in enumerate(
        scenes,
        start=1,
    ):

        panels.append(
            {
                "number": number,
                "title": title,
                "scene_description": (
                    f"{description} "
                    f"The mood is {tone}."
                ),
                "caption": (
                    f"Panel {number}: "
                    "The story moves forward."
                ),
                "narration": (
                    f"{character}: "
                    "I have to keep going!"
                ),
                "image_prompt": (
                    f"{art_style} comic book illustration, "
                    f"{description}, "
                    f"main character {character}, "
                    f"setting {setting}, "
                    "cinematic composition, "
                    "expressive face, "
                    "detailed background, "
                    "consistent character design, "
                    "clean artwork, "
                    "no text, no watermark"
                ),
            }
        )

    return panels


def make_mock_image(
    output_path: Path,
    panel_number: int,
    character: str,
) -> None:

    width = 1200
    height = 750

    image = Image.new(
        "RGB",
        (width, height),
        "#f4ead5",
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (20, 20, width - 20, height - 20),
        outline="#202020",
        width=10,
    )

    draw.rectangle(
        (45, 45, width - 45, 120),
        fill="#202020",
    )

    draw.text(
        (70, 68),
        f"COMICCRAFT - PANEL {panel_number}",
        fill="white",
    )

    # Simple demo character
    draw.ellipse(
        (430, 180, 770, 520),
        fill="#ffd36a",
        outline="#202020",
        width=8,
    )

    draw.ellipse(
        (510, 280, 555, 325),
        fill="#202020",
    )

    draw.ellipse(
        (645, 280, 690, 325),
        fill="#202020",
    )

    draw.arc(
        (540, 330, 665, 425),
        10,
        170,
        fill="#202020",
        width=7,
    )

    draw.text(
        (70, 650),
        f"Main character: {character}",
        fill="#202020",
    )

    draw.text(
        (70, 690),
        "Demo artwork - set MOCK_MODE=false for real AI images",
        fill="#202020",
    )

    image.save(
        output_path,
        "PNG",
    )