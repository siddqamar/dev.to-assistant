"""
FastAPI router — all HTTP endpoints live here.

Endpoints:
    GET  /           → Health check / welcome message.
    GET  /api/analyze → Run the scanner → analyzer → compiler pipeline
                        and return structured results for the frontend.
"""

import asyncio
from typing import Dict, List

from fastapi import APIRouter

from src.config import API_MAX_POSTS, BATCH_SIZE
from src.services.scanner import DevToScanner
from src.services.analyzer import PostAnalyzer

router = APIRouter()


@router.get("/")
def read_root() -> Dict[str, str]:
    """Health-check endpoint."""
    return {"message": "Dev.to Analyzer API is running. Go to /gradio for the UI."}


@router.get("/api/analyze")
async def analyze_endpoint(
    tag: str = "python",
    pages: int = 3,
) -> List[Dict]:
    """Run the full scan → analyze pipeline and return results for the frontend.

    Args:
        tag: Dev.to tag to scan (e.g. ``python``, ``weekendchallenge``).
        pages: Number of API pages to fetch (each page ≈ 30 posts).

    Returns:
        JSON list of analysed post objects.
    """
    scanner = DevToScanner(tag=tag)
    analyzer = PostAnalyzer()

    # 1. Scan (Gradio progress not used here, passing dummy lambda)
    raw_posts = scanner.fetch_posts(
        pages=pages,
        progress=lambda x, desc="": None,
    )

    if not raw_posts:
        return []

    # 2. Analyze (in batches)
    analyzed_data: List[Dict] = []
    # Limit total posts for API to keep it responsive
    total_posts = min(len(raw_posts), API_MAX_POSTS)
    raw_posts = raw_posts[:total_posts]

    for i in range(0, total_posts, BATCH_SIZE):
        batch = raw_posts[i : i + BATCH_SIZE]

        # Enrich batch with full content
        for post in batch:
            post["body_markdown"] = scanner.get_post_details(post["id"])
            await asyncio.sleep(0.1)

        batch_results = analyzer.analyze_batch(batch)
        analyzed_data.extend(batch_results)
        await asyncio.sleep(0.5)

    # 3. Compile for Frontend
    analysis_map = {item["id"]: item for item in analyzed_data if "id" in item}

    frontend_data: List[Dict] = []
    for post in raw_posts:
        p_id = post["id"]
        analysis = analysis_map.get(p_id, {})

        frontend_data.append(
            {
                "id": p_id,
                "author": post["user"]["name"],
                "avatar": post["user"]["profile_image_90"],
                "date": post["published_at"].split("T")[0],
                "topic": post["title"],
                "tech_stack": analysis.get("tech_stack", "N/A"),
                "problem": analysis.get("pain_point", "N/A"),
                "solution": analysis.get("solution", "N/A"),
                "github_url": analysis.get("github_url", "N/A"),
                "reacts": post["public_reactions_count"],
                "comments": post["comments_count"],
                "url": post["url"],
            }
        )

    return frontend_data
