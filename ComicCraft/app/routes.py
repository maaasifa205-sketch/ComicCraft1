from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR, settings
from app.models import ComicRequest
from app.services.comic_service import create_comic


router = APIRouter()

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "mock_mode": settings.mock_mode
        },
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic_from_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        comic_request = ComicRequest(
            story_prompt=story_prompt.strip(),
            character_name=character_name.strip(),
            setting=setting.strip(),
            tone=tone.strip(),
            art_style=art_style.strip(),
        )

        comic = create_comic(comic_request)

        return templates.TemplateResponse(
            request=request,
            name="comic.html",
            context={
                "comic": comic
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": str(exc)
            },
            status_code=500,
        )


@router.post("/api/generate")
async def generate_comic_api(payload: ComicRequest):
    try:
        comic = create_comic(payload)

        return comic.model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "mock_mode": settings.mock_mode,
    }