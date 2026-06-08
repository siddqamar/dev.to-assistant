"""
PostAnalyzer — Agent responsible for analyzing post content using Gemini.

Sends batches of Dev.to posts to the Gemini model, parses the structured
JSON response, and normalises fields (tech stack, GitHub URLs) for
downstream consumption.
"""

import json
import re
from typing import Any, Dict, List

from google.genai import types

from src.config import CONTENT_TRUNCATE_LIMIT, client, GEMINI_MODEL


class PostAnalyzer:
    """Agent responsible for analyzing post content using Gemini."""

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or GEMINI_MODEL

    # ------------------------------------------------------------------
    # Static helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_tech_stack(raw_value: Any) -> str:
        """Normalizes tech stack into a clean, comma-separated string."""
        if raw_value is None:
            return "N/A"

        if isinstance(raw_value, list):
            candidates = [str(item).strip() for item in raw_value]
        else:
            text = str(raw_value).strip()
            if not text or text.lower() in {"n/a", "none", "null"}:
                return "N/A"
            candidates = re.split(r"[,\n;/|]+", text)

        cleaned: List[str] = []
        seen: set[str] = set()
        for item in candidates:
            token = item.strip(" -•\t\r\n")
            if not token:
                continue
            token = re.sub(r"\s+", " ", token)
            key = token.lower()
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(token)

        return ", ".join(cleaned) if cleaned else "N/A"

    @staticmethod
    def _extract_github_url_from_text(text: str) -> str:
        """Extracts the first GitHub repository URL from text."""
        if not text:
            return "N/A"

        match = re.search(
            r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[^\s)\]}]*)?",
            text,
            re.IGNORECASE,
        )
        if not match:
            return "N/A"
        return match.group(0).rstrip(".,);]")

    # ------------------------------------------------------------------
    # Core analysis
    # ------------------------------------------------------------------

    def analyze_batch(self, posts: List[Dict]) -> List[Dict]:
        """Analyzes a batch of posts to extract insights.

        Args:
            posts: List of post dicts (must contain ``id``, ``title``,
                   ``url``, and ideally ``body_markdown``).

        Returns:
            List of dicts with keys ``id``, ``pain_point``, ``tech_stack``,
            ``solution``, ``github_url``.
        """
        if client is None:
            raise ValueError(
                "Gemini client is not initialized. Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable in your environment or a .env file."
            )

        # Prepare the prompt context
        posts_context: List[str] = []
        for p in posts:
            # Prefer full body markdown if available, else fall back to description
            content = p.get("body_markdown", p.get("description", ""))
            # Truncate content to avoid hitting token limits
            if len(content) > CONTENT_TRUNCATE_LIMIT:
                content = content[:CONTENT_TRUNCATE_LIMIT] + "...(truncated)"

            content_snippet = (
                f"ID: {p['id']}\nTitle: {p['title']}\nURL: {p['url']}\n"
                f"Content:\n{content}\n"
            )
            posts_context.append(content_snippet)

        prompt = """
        You are an expert technical content analyst. 
        Analyze the following Dev.to posts.
        
        For EACH post, extract:
        1. Pain Point: What specific problem is the author solving?
        2. Tech Stack: A concise list of technologies explicitly mentioned in the post
           (languages, frameworks, cloud/services, databases, tools). If none, return "N/A".
        3. Solution: A 1-sentence summary of their technical approach.
        4. GitHub URL: If the post mentions a GitHub repository URL, return it. Otherwise "N/A".
        
        Return the result as a raw JSON list of objects. Do not use markdown formatting.
        Format:
        [
            {"id": 123, "pain_point": "...", "tech_stack": "...", "solution": "...", "github_url": "..."},
            ...
        ]
        
        Here are the posts:
        """ + "\n\n".join(posts_context)

        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            parsed = json.loads(response.text)

            # Post-process analysis output for consistency and reliable
            # GitHub URL extraction.
            post_map = {p["id"]: p for p in posts}
            normalized: List[Dict] = []
            for item in parsed:
                if "id" not in item:
                    continue
                source_post = post_map.get(item["id"], {})
                source_text = "\n".join(
                    [
                        source_post.get("title", ""),
                        source_post.get("url", ""),
                        source_post.get(
                            "body_markdown",
                            source_post.get("description", ""),
                        ),
                    ]
                )
                github_from_post = self._extract_github_url_from_text(source_text)
                github_from_model = (
                    str(item.get("github_url", "N/A")).strip() or "N/A"
                )

                normalized.append(
                    {
                        "id": item["id"],
                        "pain_point": item.get("pain_point", "N/A"),
                        "tech_stack": self._normalize_tech_stack(
                            item.get("tech_stack", "N/A")
                        ),
                        "solution": item.get("solution", "N/A"),
                        "github_url": (
                            github_from_model
                            if github_from_model.upper() != "N/A"
                            else github_from_post
                        ),
                    }
                )

            return normalized

        except Exception as e:
            print(f"Error analyzing batch: {e}")
            # Return empty structure on failure to keep alignment
            return [
                {
                    "id": p["id"],
                    "pain_point": "Error",
                    "tech_stack": "Error",
                    "solution": "Error",
                    "github_url": "Error",
                }
                for p in posts
            ]
