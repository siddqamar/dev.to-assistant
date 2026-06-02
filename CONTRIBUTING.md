# Contributing to Dev.to ASSISTANT

Thanks for taking the time to improve this project. This repository is a Dev.to post analysis tool that combines a Python FastAPI backend, a Gradio-based UI, and a Next.js frontend. Contributions that improve reliability, analysis quality, UX, and deployment readiness are especially welcome.

## What This Project Is

Dev.to ASSISTANT helps users scan Dev.to posts by tag, analyze the content with an LLM, and surface structured insights such as:

- pain points
- tech stack
- proposed solution
- GitHub repository links
- engagement metrics

The current codebase is centered around:

- `main.py` for the Python backend and Gradio app
- `UI/` for the Next.js frontend
- `.env` for local secrets such as `GOOGLE_API_KEY`

## Good Contribution Ideas

If you are looking for a place to start, these areas will have the biggest impact:

- improve Dev.to API resilience and rate-limit handling
- refine the prompt and post-processing logic for more accurate summaries
- strengthen the frontend dashboard and result presentation
- add tests around parsing, normalization, and result compilation
- prepare the app for containerized local and production deployments

## Before You Start

Please check the existing README and code paths first so your changes fit the current structure. The project is intentionally small, so prefer focused changes over broad refactors unless they unlock a clear improvement.

If you are planning a larger change, open an issue or describe the approach in your pull request before investing heavily. That helps keep the project aligned and avoids duplicated effort.

## Local Setup

1. Clone the repository.
2. Create a Python 3.11+ environment and install backend dependencies with `uv sync`.
3. Add a `.env` file with `GOOGLE_API_KEY=...`.
4. Start the backend with `uv run python main.py`.
5. Install frontend dependencies in `UI/` and run `npm run dev`.

For the frontend, the key commands are:

```bash
cd UI
npm install
npm run dev
```

## Recommended Workflow

1. Create a branch for your change.
2. Keep the scope tight and make one logical change per PR.
3. Test the affected behavior manually.
4. Update docs when your change affects setup or usage.
5. Open a PR with a short summary of what changed and why.

## Coding Standards

### Python

- Prefer clear, typed functions and small modules.
- Keep error handling graceful, especially around Dev.to requests and LLM responses.
- Preserve the existing pipeline structure: scanner, analyzer, compiler.
- Avoid hardcoding secrets or environment-specific values.

### Frontend

- Keep changes consistent with the existing Next.js app structure in `UI/`.
- Reuse existing component patterns when possible.
- Make result tables, status messages, and controls easy to scan.

### Data and Output

- Keep output fields stable unless you are intentionally changing the schema.
- When you change the analysis shape, update the backend and frontend together.
- Normalize values like `N/A` consistently so the UI stays predictable.

## Testing Expectations

This repository does not yet have a full automated test suite, so contributors should at least verify the changed path manually.

Please include:

- a quick backend smoke test if you touched `main.py`
- a UI check if you changed anything under `UI/`
- sample input/output notes in your PR if the behavior is not obvious

If you add tests, prefer coverage for:

- tech stack normalization
- GitHub URL extraction
- result compilation into a dataframe or API payload
- any new parsing or transformation logic

## Pull Request Checklist

Before opening a PR, confirm that:

- your change is focused and easy to review
- docs were updated if setup or usage changed
- secrets are still loaded from environment variables only
- the UI still starts and the backend still serves the analyzer
- any new behavior is described clearly in the PR

## Containerization Direction

Container support is a strong next step for this repo, so contributions in that direction are very welcome. If you are working on Docker support, aim for the following shape:

- a backend image for the FastAPI/Gradio Python app
- a frontend image for the Next.js app
- a `docker-compose.yml` that runs both services together
- environment-variable support for `GOOGLE_API_KEY` and related configuration
- documented ports, startup commands, and health checks

When contributing container work, please keep these goals in mind:

- do not bake secrets into images
- expose the backend and frontend clearly
- make local development easy enough for a first-time contributor
- keep the setup reproducible across machines

## Security and Privacy

Never commit API keys, private URLs, or local-only configuration. If you discover a security issue or secret exposure risk, avoid opening a public issue with the details and instead flag it privately.

## Questions

If anything is unclear, open an issue or leave a note in your pull request. Specific questions, sample payloads, and screenshots are always helpful.
