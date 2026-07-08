from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.api import routes


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


def test_read_root_returns_health_message(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Dev.to Analyzer API is running. Go to /gradio for the UI."
    }


def test_analyze_endpoint_returns_empty_list_when_scanner_finds_no_posts(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    class ScannerStub:
        def __init__(self, tag: str) -> None:
            self.tag = tag

        def fetch_posts(self, pages: int, progress):  # noqa: ANN001
            assert self.tag == "python"
            assert pages == 2
            return []

    class AnalyzerStub:
        def analyze_batch(self, posts):  # noqa: ANN001
            raise AssertionError("Analyzer should not be called when there are no posts")

    async def fake_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(routes, "DevToScanner", ScannerStub)
    monkeypatch.setattr(routes, "PostAnalyzer", AnalyzerStub)
    monkeypatch.setattr(routes.asyncio, "sleep", fake_sleep)

    response = client.get("/api/analyze", params={"tag": "python", "pages": 2})

    assert response.status_code == 200
    assert response.json() == []


def test_analyze_endpoint_transforms_scanner_and_analyzer_output(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    raw_posts = [
        {
            "id": 101,
            "title": "Async API Patterns",
            "published_at": "2026-07-08T12:00:00Z",
            "public_reactions_count": 12,
            "comments_count": 3,
            "url": "https://dev.to/example/async-api-patterns",
            "user": {
                "name": "Ada Lovelace",
                "profile_image_90": "https://images.dev/avatar.png",
            },
        }
    ]

    class ScannerStub:
        def __init__(self, tag: str) -> None:
            self.tag = tag

        def fetch_posts(self, pages: int, progress):  # noqa: ANN001
            assert self.tag == "fastapi"
            assert pages == 1
            progress(1.0, desc="stub")
            return [post.copy() for post in raw_posts]

        def get_post_details(self, post_id: int) -> str:
            assert post_id == 101
            return "Body markdown with https://github.com/acme/project"

    class AnalyzerStub:
        def analyze_batch(self, posts):  # noqa: ANN001
            assert posts[0]["body_markdown"] == "Body markdown with https://github.com/acme/project"
            return [
                {
                    "id": 101,
                    "tech_stack": "FastAPI, Python",
                    "pain_point": "Blocking requests slowed the API.",
                    "solution": "Move IO to async endpoints.",
                    "github_url": "https://github.com/acme/project",
                }
            ]

    async def fake_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(routes, "DevToScanner", ScannerStub)
    monkeypatch.setattr(routes, "PostAnalyzer", AnalyzerStub)
    monkeypatch.setattr(routes.asyncio, "sleep", fake_sleep)

    response = client.get("/api/analyze", params={"tag": "fastapi", "pages": 1})

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 101,
            "author": "Ada Lovelace",
            "avatar": "https://images.dev/avatar.png",
            "date": "2026-07-08",
            "topic": "Async API Patterns",
            "tech_stack": "FastAPI, Python",
            "problem": "Blocking requests slowed the API.",
            "solution": "Move IO to async endpoints.",
            "github_url": "https://github.com/acme/project",
            "reacts": 12,
            "comments": 3,
            "url": "https://dev.to/example/async-api-patterns",
        }
    ]
