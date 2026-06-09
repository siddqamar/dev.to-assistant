"""
Gradio UI — interactive Blocks-based interface for the Dev.to analyzer.

Provides:
    - Tag input and page-count slider
    - ``run_analysis()`` orchestrator that chains scanner → analyzer → compiler
    - ``export_to_csv()`` helper for one-click CSV export
    - ``demo`` — the ``gr.Blocks`` instance, ready to be mounted on FastAPI
"""

import time
from typing import Tuple

import gradio as gr
import pandas as pd

from src.config import BATCH_SIZE, POST_DETAIL_DELAY, BATCH_DELAY
from src.services.scanner import DevToScanner
from src.services.analyzer import PostAnalyzer
from src.services.compiler import ResultCompiler


# ---------------------------------------------------------------------------
# Orchestration helpers
# ---------------------------------------------------------------------------

def run_analysis(
    tag_name: str,
    num_pages: int,
    progress: gr.Progress = gr.Progress(),
) -> Tuple[pd.DataFrame, str]:
    """End-to-end pipeline: scan → enrich → analyze → compile.

    Args:
        tag_name: Dev.to tag to scan.
        num_pages: Number of API pages to fetch.
        progress: Gradio progress callback.

    Returns:
        Tuple of (DataFrame with results, status message string).
    """
    scanner = DevToScanner(tag=tag_name)
    analyzer = PostAnalyzer()
    compiler = ResultCompiler()

    # 1. Scan
    progress(0.1, desc="Fetching posts from Dev.to...")
    raw_posts = scanner.fetch_posts(pages=num_pages, progress=progress)

    if not raw_posts:
        return pd.DataFrame(columns=["Error"]), "No posts found."

    # 2. Analyze (in batches)
    analyzed_data = []
    total_posts = len(raw_posts)

    for i in range(0, total_posts, BATCH_SIZE):
        batch = raw_posts[i : i + BATCH_SIZE]

        # Enrich batch with full content
        for post in batch:
            post["body_markdown"] = scanner.get_post_details(post["id"])
            time.sleep(POST_DETAIL_DELAY)  # Micro-sleep to be polite

        progress(
            (0.3 + (i / total_posts) * 0.6),
            desc=f"Analyzing batch {i // BATCH_SIZE + 1}/"
            f"{(total_posts // BATCH_SIZE) + 1}...",
        )

        batch_results = analyzer.analyze_batch(batch)
        analyzed_data.extend(batch_results)
        time.sleep(BATCH_DELAY)  # Rate limit protection

    # 3. Compile
    progress(0.95, desc="Compiling final report...")
    df = compiler.compile(raw_posts, analyzed_data)

    return df, f"Successfully analyzed {len(df)} posts."


def export_to_csv(df: pd.DataFrame) -> str | None:
    """Exports the current dataframe to a CSV file.

    Args:
        df: DataFrame to export.

    Returns:
        File path of the generated CSV, or ``None`` if the DF is empty.
    """
    if df is None or df.empty:
        return None
    file_path = "devto_analysis_results.csv"
    df.to_csv(file_path, index=False)
    return file_path


# ---------------------------------------------------------------------------
# Gradio Blocks UI
# ---------------------------------------------------------------------------

with gr.Blocks(title="Dev.to Posts Analyzer") as demo:
    gr.Markdown("# 🚀 Dev.to Posts Analyzer")
    gr.Markdown(
        "Scan, analyze, and summarize Dev.to posts using AI without doomscrolling."
    )

    with gr.Row():
        tag_input = gr.Textbox(label="Tag to Scan", value="weekendchallenge")
        pages_input = gr.Slider(
            minimum=1, maximum=20, value=7, step=1, label="Pages to Scan"
        )
        scan_btn = gr.Button("Start Agents", variant="primary")

    status_output = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        results_output = gr.Dataframe(
            label="Analysis Results",
            interactive=False,
            buttons=["copy"],
        )

    with gr.Row():
        export_btn = gr.Button("📂 Export to CSV", variant="secondary")
        download_file = gr.File(label="Download CSV", interactive=False)

    scan_btn.click(
        fn=run_analysis,
        inputs=[tag_input, pages_input],
        outputs=[results_output, status_output],
    )

    export_btn.click(
        fn=export_to_csv,
        inputs=[results_output],
        outputs=[download_file],
    )
