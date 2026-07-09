from src.services.analyzer import PostAnalyzer


def test_normalize_tech_stack_deduplicates_and_cleans_tokens() -> None:
    raw = [" FastAPI ", "Python", "python", " ", "- Docker "]

    result = PostAnalyzer._normalize_tech_stack(raw)

    assert result == "FastAPI, Python, Docker"


def test_normalize_tech_stack_returns_na_for_empty_values() -> None:
    assert PostAnalyzer._normalize_tech_stack(None) == "N/A"
    assert PostAnalyzer._normalize_tech_stack("null") == "N/A"


def test_extract_github_url_from_text_returns_first_repo_url() -> None:
    text = (
        "See https://example.com first and then "
        "https://github.com/openai/openai-python/issues/1)."
    )

    result = PostAnalyzer._extract_github_url_from_text(text)

    assert result == "https://github.com/openai/openai-python/issues/1"
