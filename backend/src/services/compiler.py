"""
ResultCompiler — Agent responsible for compiling and formatting results.

Merges raw Dev.to post metadata with analyser output into a sorted
Pandas DataFrame ready for display or export.
"""

from typing import Dict, List

import pandas as pd


class ResultCompiler:
    """Agent responsible for compiling and formatting results."""

    def compile(
        self,
        raw_posts: List[Dict],
        analysis_results: List[Dict],
    ) -> pd.DataFrame:
        """Merge raw posts with analysis into a sorted DataFrame.

        Args:
            raw_posts: List of raw post dicts from the Dev.to API.
            analysis_results: List of analysis dicts from ``PostAnalyzer``.

        Returns:
            A ``pd.DataFrame`` sorted by *Reactions* descending.
        """
        # Create a lookup for analysis
        analysis_map = {
            item["id"]: item for item in analysis_results if "id" in item
        }

        compiled_data: List[Dict] = []
        for post in raw_posts:
            p_id = post["id"]
            analysis = analysis_map.get(p_id, {})

            compiled_data.append(
                {
                    "Title": post["title"],
                    "User": post["user"]["name"],
                    "Reactions": post["public_reactions_count"],
                    "Comments": post["comments_count"],
                    "Pain Point": analysis.get("pain_point", "N/A"),
                    "Tech Stack": analysis.get("tech_stack", "N/A"),
                    "Solution": analysis.get("solution", "N/A"),
                    "GitHub URL": analysis.get("github_url", "N/A"),
                    "URL": post["url"],
                    "Published": post["published_at"].split("T")[0],
                }
            )

        df = pd.DataFrame(compiled_data)
        # Sort by Reactions descending
        return df.sort_values(by="Reactions", ascending=False)
