"""
Data models schema for AVENIQ Content Department.
Represents ContentItem, ArticleContent, SocialPostContent, NewsletterContent,
LandingPageContent, ContentPackage, ContentQualityGate, ContentVersion, ContentVariation,
ContentContext, ContentScores, and EditorialReviewState.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ContentContext:
    planning_report: Dict[str, Any]
    research_package: Dict[str, Any]
    brand_guidelines: Dict[str, Any]
    seo_rules: Dict[str, Any]
    campaign_goals: List[str]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class ArticleContent:
    title: str
    slug: str
    meta_title: str
    meta_description: str
    hook: str
    body_markdown: str
    sections: Dict[str, str]
    faq: List[Dict[str, str]]
    word_count: int
    reading_time_minutes: int
    citations_used: List[str]
    internal_links: List[str]

@dataclass
class SocialPostContent:
    platform: str
    headline: str
    copy_text: str
    hashtags: List[str]
    call_to_action: str
    character_count: int
    media_requirements: List[str]

@dataclass
class NewsletterContent:
    subject_line: str
    preview_text: str
    editorial_body: str
    featured_section: str
    key_takeaways: List[str]
    call_to_action: str

@dataclass
class LandingPageContent:
    hero_headline: str
    hero_subheadline: str
    value_props: List[str]
    feature_highlights: List[Dict[str, str]]
    social_proof_quotes: List[str]
    cta_headline: str
    button_text: str

@dataclass
class ContentVariation:
    alternative_titles: List[str]
    alternative_hooks: List[str]
    cta_variations: List[str]
    emoji_version: str
    non_emoji_version: str
    professional_version: str
    friendly_version: str
    short_version: str
    long_version: str

@dataclass
class ContentScores:
    readability_score: float
    seo_score: float
    engagement_score: float
    brand_alignment_score: float
    grammar_score: float
    authority_score: float
    completeness_score: float
    originality_score: float
    overall_score: float

@dataclass
class EditorialReviewState:
    current_state: str  # Draft, Generated, Editorial Review, SEO Review, Brand Review, Approved, Published, Archived
    editorial_notes: List[str]
    reviewer_id: str
    approved_for_publishing: bool

@dataclass
class ContentQualityGate:
    passed: bool
    score: float
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class ContentVersion:
    version: str
    timestamp: str
    author: str
    planning_version: str
    research_version: str

@dataclass
class ContentPackage:
    id: str
    topic: str
    date: str
    executive_summary: str
    master_article: ArticleContent
    linkedin_post: SocialPostContent
    linkedin_carousel_copy: List[str]
    instagram_caption: SocialPostContent
    facebook_post: SocialPostContent
    x_thread: List[str]
    threads_post: SocialPostContent
    telegram_summary: SocialPostContent
    newsletter: NewsletterContent
    medium_article: ArticleContent
    devto_article: ArticleContent
    landing_page_copy: LandingPageContent
    email_campaign: NewsletterContent
    variations: ContentVariation
    scores: ContentScores
    workflow_state: EditorialReviewState
    version_info: ContentVersion
    quality_gate: ContentQualityGate
    decision_reasoning: Dict[str, Any]
    created_at: str = field(default_factory=_get_utc_now)
