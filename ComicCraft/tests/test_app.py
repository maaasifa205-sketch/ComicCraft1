import os

os.environ["MOCK_MODE"] = "true"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "ComicCraft" in response.text

    assert (
        "Generate My Comic"
        in response.text
    )


def test_full_generation():

    payload = {

        "story_prompt":
            "A student discovers a tiny robot under the college library.",

        "character_name":
            "Rumi",

        "setting":
            "college library",

        "tone":
            "mysterious",

        "art_style":
            "comic book",
    }

    response = client.post(
        "/api/generate",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(
        data["panels"]
    ) == 5

    assert data[
        "pdf_path"
    ].endswith(".pdf")

    assert data[
        "panels"
    ][0][
        "image_path"
    ].startswith(
        "/static/panels/"
    )