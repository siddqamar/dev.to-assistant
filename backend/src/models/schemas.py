"""
Pydantic schemas for request / response validation.

These models provide a typed contract for the data flowing between
the scanner, analyzer, compiler, and API layers.
"""

from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    """Single post analysis produced by the PostAnalyzer agent."""

    id: int
    pain_point: str = "N/A"
    tech_stack: str = "N/A"
    solution: str = "N/A"
    github_url: str = "N/A"


class CompiledPost(BaseModel):
    """Row in the compiled DataFrame / Gradio table."""

    title: str
    user: str = Field(alias="User")
    reactions: int = Field(alias="Reactions")
    comments: int = Field(alias="Comments")
    pain_point: str = Field(alias="Pain Point")
    tech_stack: str = Field(alias="Tech Stack")
    solution: str = Field(alias="Solution")
    github_url: str = Field(alias="GitHub URL")
    url: str = Field(alias="URL")
    published: str = Field(alias="Published")


class FrontendPost(BaseModel):
    """Shape returned by ``GET /api/analyze`` for the Next.js frontend."""

    id: int
    author: str
    avatar: str
    date: str
    topic: str
    tech_stack: str = "N/A"
    problem: str = "N/A"
    solution: str = "N/A"
    github_url: str = "N/A"
    reacts: int = 0
    comments: int = 0
    url: str
