from app.models import (
    ComicRequest,
    ComicResult,
    Panel,
)

from app.services.gemini_service import (
    generate_story,
)

from app.services.image_service import (
    generate_panel_image,
)

from app.services.pdf_service import (
    create_pdf,
)


def create_comic(
    request: ComicRequest,
) -> ComicResult:

    story = generate_story(
        story_prompt=request.story_prompt,
        character_name=request.character_name,
        setting=request.setting,
        tone=request.tone,
        art_style=request.art_style,
    )

    panels: list[Panel] = []

    for item in story:

        image_path = generate_panel_image(
            prompt=item["image_prompt"],
            panel_number=int(
                item["number"]
            ),
            character_name=request.character_name,
        )

        panels.append(
            Panel(
                number=int(
                    item["number"]
                ),
                title=item["title"],
                scene_description=(
                    item["scene_description"]
                ),
                caption=item["caption"],
                narration=item["narration"],
                image_prompt=item["image_prompt"],
                image_path=image_path,
            )
        )

    title = (
        f"{request.character_name}'s Comic"
    )

    pdf_path = create_pdf(
        title,
        panels,
    )

    return ComicResult(
        title=title,
        panels=panels,
        pdf_path=pdf_path,
    )