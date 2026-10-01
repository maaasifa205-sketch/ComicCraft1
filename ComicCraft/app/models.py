from pydantic import BaseModel, Field


class ComicRequest(BaseModel):
    story_prompt: str = Field(min_length=5, max_length=2000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=120)
    tone: str = Field(min_length=1, max_length=50)
    art_style: str = Field(min_length=1, max_length=80)


class Panel(BaseModel):
    number: int
    title: str
    scene_description: str
    caption: str
    narration: str
    image_prompt: str
    image_path: str


class ComicResult(BaseModel):
    title: str
    panels: list[Panel]
    pdf_path: str