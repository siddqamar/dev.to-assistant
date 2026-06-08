"""
DevToScanner — Agent responsible for scanning Dev.to posts.

Fetches paginated post listings and individual post details
from the Dev.to public API.
"""

import time
from typing import Any, Callable, Dict, List

import requests

from src.config import DEVTO_API_URL, PAGE_FETCH_DELAY


class DevToScanner:
    """Agent responsible for scanning Dev.to posts."""

    def __init__(self, tag: str = "weekendchallenge") -> None:
        self.tag = tag

    def fetch_posts(
        self,
        pages: int = 7,
        per_page: int = 30,
        progress: Any = None,
    ) -> List[Dict]:
        """Fetches posts from Dev.to API across multiple pages.

        Args:
            pages: Number of pages to fetch.
            per_page: Number of posts per page.
            progress: Optional Gradio progress callback or a callable
                      accepting ``(fraction, desc=...)``.

        Returns:
            Flat list of post dicts from the Dev.to API.
        """
        all_posts: List[Dict] = []

        for page in range(1, pages + 1):
            if progress is not None:
                try:
                    progress(page / pages, desc=f"Scanning Page {page}/{pages}...")
                except Exception:
                    pass

            try:
                params = {
                    "tag": self.tag,
                    "page": page,
                    "per_page": per_page,
                }
                response = requests.get(DEVTO_API_URL, params=params)
                response.raise_for_status()

                posts = response.json()
                if not posts:
                    break

                all_posts.extend(posts)
                time.sleep(PAGE_FETCH_DELAY)  # Polite delay

            except Exception as e:
                print(f"Error fetching page {page}: {e}")

        return all_posts

    def get_post_details(self, post_id: int) -> str:
        """Fetches the full markdown content of a post.

        Args:
            post_id: The Dev.to article ID.

        Returns:
            The ``body_markdown`` field, or an empty string on failure.
        """
        try:
            url = f"{DEVTO_API_URL}/{post_id}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get("body_markdown", "")
            return ""
        except Exception:
            return ""
