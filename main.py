import os
import time
import json
import asyncio
import requests
import pandas as pd
import gradio as gr
from typing import List, Dict, Any
from fastapi import FastAPI
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Configuration
DEVTO_API_URL = "https://dev.to/api/articles"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini Client
client = genai.Client(api_key=GOOGLE_API_KEY)

class DevToScanner:
    """Agent responsible for scanning Dev.to posts."""
    
    def __init__(self, tag: str = "weekendchallenge"):
        self.tag = tag

    def fetch_posts(self, pages: int = 7, per_page: int = 30, progress=gr.Progress()) -> List[Dict]:
        """Fetches posts from Dev.to API across multiple pages."""
        all_posts = []
        
        for page in range(1, pages + 1):
            progress(page / pages, desc=f"Scanning Page {page}/{pages}...")
            try:
                params = {
                    "tag": self.tag,
                    "page": page,
                    "per_page": per_page
                }
                response = requests.get(DEVTO_API_URL, params=params)
                response.raise_for_status()
                
                posts = response.json()
                if not posts:
                    break
                    
                all_posts.extend(posts)
                time.sleep(0.5) # Polite delay
                
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                
        return all_posts

    def get_post_details(self, post_id: int) -> str:
        """Fetches the full markdown content of a post."""
        try:
            url = f"{DEVTO_API_URL}/{post_id}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get("body_markdown", "")
            return ""
        except:
            return ""

class PostAnalyzer:
    """Agent responsible for analyzing post content using Gemini."""
    
    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        self.model_name = model_name

    def analyze_batch(self, posts: List[Dict]) -> List[Dict]:
        """Analyzes a batch of posts to extract insights."""
        
        # Prepare the prompt context
        posts_context = []
        for p in posts:
            # Prefer full body markdown if available, else fall back to description
            content = p.get('body_markdown', p.get('description', ''))
            # Truncate content to avoid hitting token limits if it's huge (e.g. 10k chars)
            if len(content) > 15000:
                content = content[:15000] + "...(truncated)"
                
            content_snippet = f"ID: {p['id']}\nTitle: {p['title']}\nURL: {p['url']}\nContent:\n{content}\n"
            posts_context.append(content_snippet)
            
        prompt = """
        You are an expert technical content analyst. 
        Analyze the following Dev.to posts.
        
        For EACH post, extract:
        1. Pain Point: What specific problem is the author solving?
        2. Hook: What is the most compelling aspect of this post?
        3. Solution: A 1-sentence summary of their technical approach.
        
        Return the result as a raw JSON list of objects. Do not use markdown formatting.
        Format:
        [
            {"id": 123, "pain_point": "...", "hook": "...", "solution": "..."},
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
                )
            )
            
            return json.loads(response.text)
        except Exception as e:
            print(f"Error analyzing batch: {e}")
            # Return empty structure on failure to keep alignment
            return [{"id": p['id'], "pain_point": "Error", "hook": "Error", "solution": "Error"} for p in posts]

class ResultCompiler:
    """Agent responsible for compiling and formatting results."""
    
    def compile(self, raw_posts: List[Dict], analysis_results: List[Dict]) -> pd.DataFrame:
        # Create a lookup for analysis
        analysis_map = {item['id']: item for item in analysis_results if 'id' in item}
        
        compiled_data = []
        for post in raw_posts:
            p_id = post['id']
            analysis = analysis_map.get(p_id, {})
            
            compiled_data.append({
                "Title": post['title'],
                "User": post['user']['name'],
                "Reactions": post['public_reactions_count'],
                "Comments": post['comments_count'],
                "Pain Point": analysis.get("pain_point", "N/A"),
                "Hook": analysis.get("hook", "N/A"),
                "Solution": analysis.get("solution", "N/A"),
                "URL": post['url'],
                "Published": post['published_at'].split("T")[0]
            })
            
        df = pd.DataFrame(compiled_data)
        # Sort by Reactions descending
        return df.sort_values(by="Reactions", ascending=False)

# --- Gradio Logic ---

def run_analysis(tag_name: str, num_pages: int, progress=gr.Progress()):
    scanner = DevToScanner(tag=tag_name)
    analyzer = PostAnalyzer()
    compiler = ResultCompiler()
    
    # 1. Scan
    progress(0.1, desc="Fetching posts from Dev.to...")
    raw_posts = scanner.fetch_posts(pages=num_pages, progress=progress)
    
    if not raw_posts:
        return pd.DataFrame(columns=["Error"]), "No posts found."

    # 2. Analyze (in batches of 5)
    analyzed_data = []
    batch_size = 5
    total_posts = len(raw_posts)
    
    for i in range(0, total_posts, batch_size):
        batch = raw_posts[i:i+batch_size]
        
        # Enrich batch with full content
        for post in batch:
            post['body_markdown'] = scanner.get_post_details(post['id'])
            time.sleep(0.1) # Micro-sleep to be polite
            
        progress((0.3 + (i / total_posts) * 0.6), desc=f"Analyzing batch {i//batch_size + 1}/{(total_posts//batch_size)+1}...")
        
        batch_results = analyzer.analyze_batch(batch)
        analyzed_data.extend(batch_results)
        time.sleep(1) # Rate limit protection
        
    # 3. Compile
    progress(0.95, desc="Compiling final report...")
    df = compiler.compile(raw_posts, analyzed_data)
    
    return df, f"Successfully analyzed {len(df)} posts."

def export_to_csv(df):
    """Exports the current dataframe to a CSV file."""
    if df is None or df.empty:
        return None
    file_path = "devto_analysis_results.csv"
    df.to_csv(file_path, index=False)
    return file_path

# --- App UI ---

with gr.Blocks(title="Dev.to Posts Analyzer") as demo:
    gr.Markdown("# 🚀 Dev.to Posts Analyzer")
    gr.Markdown("Scan, analyze, and summarize Dev.to posts using AI without doomscrolling.")
    
    with gr.Row():
        tag_input = gr.Textbox(label="Tag to Scan", value="weekendchallenge")
        pages_input = gr.Slider(minimum=1, maximum=20, value=7, step=1, label="Pages to Scan")
        scan_btn = gr.Button("Start Agents", variant="primary")
    
    status_output = gr.Textbox(label="Status", interactive=False)
    
    with gr.Row():
        results_output = gr.Dataframe(
            label="Analysis Results", 
            interactive=False,
            buttons=["copy"]
        )
    
    with gr.Row():
        export_btn = gr.Button("📂 Export to CSV", variant="secondary")
        download_file = gr.File(label="Download CSV", interactive=False)
    
    scan_btn.click(
        fn=run_analysis,
        inputs=[tag_input, pages_input],
        outputs=[results_output, status_output]
    )

    export_btn.click(
        fn=export_to_csv,
        inputs=[results_output],
        outputs=[download_file]
    )

from fastapi.middleware.cors import CORSMiddleware

# --- FastAPI Integration ---

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Dev.to Analyzer API is running. Go to /gradio for the UI."}

@app.get("/api/analyze")
async def analyze_endpoint(tag: str = "python", pages: int = 3):
    scanner = DevToScanner(tag=tag)
    analyzer = PostAnalyzer()
    
    # 1. Scan (Gradio progress not used here, passing dummy lambda)
    raw_posts = scanner.fetch_posts(pages=pages, progress=lambda x, desc="": None)
    
    if not raw_posts:
        return []

    # 2. Analyze (in batches of 5)
    analyzed_data = []
    batch_size = 5
    # Limit total posts for API to keep it responsive
    total_posts = min(len(raw_posts), 15) 
    raw_posts = raw_posts[:total_posts]
    
    for i in range(0, total_posts, batch_size):
        batch = raw_posts[i:i+batch_size]
        
        # Enrich batch with full content
        for post in batch:
            post['body_markdown'] = scanner.get_post_details(post['id'])
            await asyncio.sleep(0.1)
            
        batch_results = analyzer.analyze_batch(batch)
        analyzed_data.extend(batch_results)
        await asyncio.sleep(0.5)
        
    # 3. Compile for Frontend
    analysis_map = {item['id']: item for item in analyzed_data if 'id' in item}
    
    frontend_data = []
    for post in raw_posts:
        p_id = post['id']
        analysis = analysis_map.get(p_id, {})
        
        frontend_data.append({
            "id": p_id,
            "author": post['user']['name'],
            "avatar": post['user']['profile_image_90'],
            "date": post['published_at'].split("T")[0],
            "topic": post['title'],
            "hook": analysis.get("hook", "N/A"),
            "problem": analysis.get("pain_point", "N/A"),
            "solution": analysis.get("solution", "N/A"),
            "reacts": post['public_reactions_count'],
            "comments": post['comments_count'],
            "url": post['url']
        })
        
    return frontend_data

# Mount Gradio app
app = gr.mount_gradio_app(app, demo, path="/gradio")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
