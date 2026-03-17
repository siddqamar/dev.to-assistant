# Dev.to Weekend Challenge Analyzer

A multi-agent system powered by Gemini to scan, analyze, and summarize "Weekend Challenge" posts on Dev.to.

## Features
- **Smart Scanning:** Fetches posts from Dev.to (default tag: `#weekendchallenge`) across multiple pages.
- **AI Analysis:** Uses Google Gemini to extract key insights from each post:
    - **Pain Point:** What problem is being solved?
    - **Hook:** What makes this post interesting?
    - **Solution:** Brief technical summary.
- **Interactive UI:** Built with Gradio for easy interaction and data visualization.
- **Exportable Results:** Presents data in a clean, sortable table.

## Tech Stack
- **Backend:** FastAPI
- **Frontend:** Gradio
- **AI:** Google GenAI SDK (Gemini)
- **Data:** Pandas

## Setup
1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Set up `.env` with `GOOGLE_API_KEY`.
4.  Run the app: `python main.py`
