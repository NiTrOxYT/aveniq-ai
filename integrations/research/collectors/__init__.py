"""
Real Market Intelligence Collectors Package.
"""

from integrations.research.collectors.reddit import (
    RedditCollector, HackerNewsCollector, GoogleTrendsCollector, GitHubCollector, DevToCollector
)

__all__ = [
    "RedditCollector",
    "HackerNewsCollector",
    "GoogleTrendsCollector",
    "GitHubCollector",
    "DevToCollector"
]
