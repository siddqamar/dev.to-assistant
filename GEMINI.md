# Gemini CLI - Dev.to Posts Analyzer

## Mandates

### 1. Architecture
- **Backend:** FastAPI (Python).
- **Frontend:** Gradio (Python).
- **Agent Framework:** Use `google-genai` (Google GenAI SDK) following the `gemini-interactions-api` skill standards.
- **Pattern:** Multi-agent pipeline:
    1.  **Scanner:** Fetches posts from Dev.to API (tag: `weekendchallenge` or user input).
    2.  **Analyzer:** Uses Gemini to extract "Pain Point", "Hook", and "Solution" from post content.
    3.  **Compiler:** Aggregates results into a Pandas DataFrame.

### 2. Operational Constraints
- **Pagination:** Scan at least 7 pages (configurable).
- **Output:** Tabular format (DataFrame) displayed in Gradio.
- **Security:** API keys must be loaded from environment variables (`.env`). Never hardcode secrets.

### 3. Style & Standards
- **Python:** Type-hinted, modular code.
- **Documentation:** Clear docstrings.
- **Error Handling:** Graceful degradation if Dev.to API fails or rate limits are hit.
