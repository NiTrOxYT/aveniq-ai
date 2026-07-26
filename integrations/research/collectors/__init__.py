"""
Real Production Market Intelligence Collectors Package.
Exports Reddit, GitHub, RSS, Google News, Product Hunt, Competitor Website Crawler, HackerNews, and Google Trends collectors.
"""

from integrations.research.collectors.reddit import RedditCollector
from integrations.research.collectors.github import GitHubCollector
from integrations.research.collectors.rss import RSSCollector
from integrations.research.collectors.google_news import GoogleNewsCollector
from integrations.research.collectors.product_hunt import ProductHuntCollector
from integrations.research.collectors.website import WebsiteCrawlerCollector

__all__ = [
    "RedditCollector",
    "GitHubCollector",
    "RSSCollector",
    "GoogleNewsCollector",
    "ProductHuntCollector",
    "WebsiteCrawlerCollector"
]
