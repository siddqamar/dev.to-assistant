# Dev.to Weekend Challenge Analyzer

A multi-agent system powered by Gemma4 to scan, analyze, and summarize "Weekend Challenge" posts on Dev.to.

## Features

- **Smart Scanning:** Fetches posts from Dev.to (default tag: `#weekendchallenge`) across multiple pages.
- **AI Analysis:** Uses Google Gemini to extract key insights from each post:
  - **Pain Point:** What problem is being solved?
  - **Tech Stack:** Technologies mentioned across the post (Python, SQL, AWS, etc.).
  - **Solution:** Brief technical summary.
  - **GitHub URL:** Repository link if mentioned in the post.
- **Interactive UI:** Gradio app for quick exploration and CSV exports.
- **API Output for Frontend:** FastAPI endpoint (`/api/analyze`) used by the UI dashboard.
- **Exportable Results:** Presents data in a clean, sortable table with downloadable CSV output.

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** Gradio + Next.js (UI folder)
- **AI:** Google GenAI SDK (Gemma4)
- **Data:** Pandas
- **Dependency Management:** UV (`pyproject.toml` + `uv.lock`)

## Setup

1.  Clone the repository.
2.  Install dependencies with UV: `uv sync`
3.  Set up `.env` with `GOOGLE_API_KEY`.
4.  Run the app: `uv run python main.py`

## API Response Fields (`/api/analyze`)

Each analyzed post includes:

- `author`
- `topic`
- `problem`
- `solution`
- `tech_stack`
- `github_url`
- `url` (Dev.to post URL)
- engagement metadata (`reacts`, `comments`)
