"""
Application entrypoint — wires together FastAPI, CORS, API routes, and Gradio.

Usage:
    python -m src.main          # run from the backend/ directory
    uvicorn src.main:app        # or with uvicorn directly
"""

import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.gradio_ui.app import demo

# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(title="Dev.to Posts Analyzer")

# CORS — permissive for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router)

# Mount Gradio app
app = gr.mount_gradio_app(app, demo, path="/gradio")


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
