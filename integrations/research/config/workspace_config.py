"""
Workspace Research Source Configuration and Competitor Profile Manager.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class WorkspaceResearchConfig:
    workspace_id: str
    enabled_sources: List[str] = field(default_factory=lambda: ["reddit", "hackernews", "google_trends", "github", "devto", "producthunt", "ai_news", "rss", "crawler"])
    custom_rss_feeds: List[str] = field(default_factory=lambda: ["https://news.ycombinator.com/rss", "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"])
    competitor_domains: List[str] = field(default_factory=lambda: ["competitor.ai", "techrival.com"])
    monitored_keywords: List[str] = field(default_factory=lambda: ["AI Agents", "Model Context Protocol", "Autonomous Workflows"])
    excluded_keywords: List[str] = field(default_factory=lambda: ["crypto", "spam", "casino"])
    preferred_languages: List[str] = field(default_factory=lambda: ["en"])

@dataclass
class CompetitorProfile:
    company_name: str
    domains: List[str]
    rss_feeds: List[str] = field(default_factory=list)
    github_org: str = ""
    producthunt_account: str = ""
    monitored_keywords: List[str] = field(default_factory=list)
