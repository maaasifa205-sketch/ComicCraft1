from datetime import datetime
from pathlib import Path

from fpdf import FPDF

from app.config import EXPORTS_DIR, STATIC_DIR
from app.models import Panel


def _filesystem_path(
    web_path: str,
) -> Path:

    relative = web_path.removeprefix(
        "/static/"
    )

    return STATIC_DIR / relative


def _pdf_safe(text: str) -> str:

    # FPDF's built-in Helvetica font does not
    # support every Unicode character.
    return (
        text.encode(
            "latin-1",
            "replace",
        ).decode("latin-1")
    )


def create_pdf(
    title: str,
    panels: list[Panel],
) -> str:

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    safe_title = "".join(
        character
        if character.isalnum()
        or character in "-_"
        else "_"
        for character in title
    )[:40]

    filename = (
        f"comic_{safe_title}_"
        f"{timestamp}.pdf"
    )

    output_path = (
        EXPORTS_DIR / filename
    )

    pdf = FPDF(
        "P",
        "mm",
        "A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=12,
    )

    for panel in panels:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18,
        )

        pdf.multi_cell(
            0,
            9,
            _pdf_safe(
                f"Panel {panel.number}: "
                f"{panel.title}"
            ),
        )

        pdf.ln(3)

        image_path = _filesystem_path(
            panel.image_path
        )

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=15,
                y=38,
                w=180,
            )

        pdf.set_y(150)

        pdf.set_font(
            "Helvetica",
            "I",
            10,
        )

        pdf.multi_cell(
            0,
            6,
            _pdf_safe(
                panel.scene_description
            ),
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.multi_cell(
            0,
            6,
            _pdf_safe(
                panel.caption
            ),
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        pdf.multi_cell(
            0,
            6,
            _pdf_safe(
                panel.narration
            ),
        )

    pdf.output(
        str(output_path)
    )

    return (
        f"/static/exports/{filename}"
    )