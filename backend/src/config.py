"""
Centralized configuration for the Dev.to Posts Analyzer.

Loads environment variables, initializes the Gemini client,
and exposes all tunable constants in one place.
"""

import os

from dotenv import load_dotenv
from google import genai

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------------
# External service URLs & keys
# ---------------------------------------------------------------------------
DEVTO_API_URL: str = "https://dev.to/api/articles"
GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")

# ---------------------------------------------------------------------------
# Gemini client (shared across the app)
# ---------------------------------------------------------------------------
client: genai.Client | None = None
try:
    if GOOGLE_API_KEY:
        client = genai.Client(api_key=GOOGLE_API_KEY)
    else:
        # Fallback to default search in environment (e.g. GEMINI_API_KEY)
        client = genai.Client()
except Exception as e:
    # Do not crash the application on import; warn instead.
    print(f"Warning: Gemini client could not be initialized: {e}")

# ---------------------------------------------------------------------------
# Tunable defaults
# ---------------------------------------------------------------------------
DEFAULT_TAG: str = "weekendchallenge"
DEFAULT_PAGES: int = 7
DEFAULT_PER_PAGE: int = 30
BATCH_SIZE: int = 5
CONTENT_TRUNCATE_LIMIT: int = 15000

# Rate‑limit / politeness delays (seconds)
PAGE_FETCH_DELAY: float = 0.5
POST_DETAIL_DELAY: float = 0.1
BATCH_DELAY: float = 1.0

# Gemini model
GEMINI_MODEL: str = "gemma-4-26b-a4b-it"

# API endpoint limits
API_MAX_POSTS: int = 15
