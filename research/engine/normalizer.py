"""
Unified Research Model and Normalizer for AVENIQ AI Research Engine.
Normalizes raw payloads from 20+ providers into a single schema.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import hashlib
from typing import List, Dict, Any, Optional


@dataclass
class ResearchItem:
    id: str
    provider: str
    category: str
    title: str
    summary: str
    url: str
    author: str
    published_at: str
    score: float = 0.0
    tags: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def generate_item_id(provider: str, unique_key: str) -> str:
    """Generate stable unique ID for a research item."""
    raw_str = f"{provider}:{unique_key}"
    return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()[:16]


def format_iso_timestamp(ts: Optional[Any] = None) -> str:
    if not ts:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    if isinstance(ts, str):
        return ts
    return datetime.now(timezone.utc).isoformat()


def normalize_github_repo(repo: Dict[str, Any]) -> ResearchItem:
    repo_id = str(repo.get('id') or repo.get('full_name') or repo.get('name'))
    full_name = repo.get('full_name') or repo.get('name') or 'unknown/repo'
    return ResearchItem(
        id=generate_item_id('github', repo_id),
        provider='github',
        category='code',
        title=full_name,
        summary=repo.get('description') or f"GitHub repository {full_name}",
        url=repo.get('html_url') or f"https://github.com/{full_name}",
        author=(repo.get('owner') or {}).get('login', '') if isinstance(repo.get('owner'), dict) else '',
        published_at=format_iso_timestamp(repo.get('created_at') or repo.get('pushed_at')),
        score=float(repo.get('stargazers_count') or repo.get('stars') or 0),
        tags=[t for t in [repo.get('language'), 'github', 'repository'] if t],
        raw={
            'stars': repo.get('stargazers_count', 0),
            'forks': repo.get('forks_count', 0),
            'open_issues': repo.get('open_issues_count', 0),
            'language': repo.get('language')
        }
    )


def normalize_reddit_post(post: Dict[str, Any]) -> ResearchItem:
    data = post.get('data', post)
    post_id = str(data.get('id') or data.get('url'))
    return ResearchItem(
        id=generate_item_id('reddit', post_id),
        provider='reddit',
        category='community',
        title=data.get('title') or 'Reddit Post',
        summary=data.get('selftext') or data.get('title') or '',
        url=data.get('permalink', '').startswith('/') and f"https://reddit.com{data.get('permalink')}" or (data.get('url') or ''),
        author=data.get('author') or 'anonymous',
        published_at=format_iso_timestamp(data.get('created_utc')),
        score=float(data.get('score') or data.get('ups') or 0),
        tags=[t for t in [data.get('subreddit'), 'reddit'] if t],
        raw={
            'subreddit': data.get('subreddit'),
            'num_comments': data.get('num_comments', 0),
            'upvote_ratio': data.get('upvote_ratio', 1.0)
        }
    )


def normalize_hackernews_item(item: Dict[str, Any]) -> ResearchItem:
    item_id = str(item.get('id'))
    return ResearchItem(
        id=generate_item_id('hackernews', item_id),
        provider='hackernews',
        category='community',
        title=item.get('title') or 'Hacker News Item',
        summary=item.get('text') or item.get('title') or '',
        url=item.get('url') or f"https://news.ycombinator.com/item?id={item_id}",
        author=item.get('by') or 'anonymous',
        published_at=format_iso_timestamp(item.get('time')),
        score=float(item.get('score') or 0),
        tags=['hackernews', 'tech'],
        raw={
            'comments_count': item.get('descendants', 0),
            'type': item.get('type', 'story')
        }
    )


def normalize_rss_entry(entry: Dict[str, Any], provider_name: str, category: str = 'search') -> ResearchItem:
    entry_id = str(entry.get('guid') or entry.get('link') or entry.get('title'))
    return ResearchItem(
        id=generate_item_id(provider_name, entry_id),
        provider=provider_name,
        category=category,
        title=entry.get('title') or f"{provider_name} Entry",
        summary=entry.get('summary') or entry.get('description') or entry.get('title') or '',
        url=entry.get('link') or entry.get('url') or '',
        author=entry.get('author') or provider_name,
        published_at=format_iso_timestamp(entry.get('published') or entry.get('pubDate')),
        score=1.0,
        tags=[provider_name, category],
        raw=entry
    )


def normalize_pypi_package(pkg: Dict[str, Any]) -> ResearchItem:
    info = pkg.get('info', pkg)
    name = info.get('name') or 'unknown-package'
    return ResearchItem(
        id=generate_item_id('pypi', name),
        provider='pypi',
        category='code',
        title=f"Python Package: {name}",
        summary=info.get('summary') or info.get('description') or '',
        url=info.get('package_url') or f"https://pypi.org/project/{name}/",
        author=info.get('author') or info.get('maintainer') or '',
        published_at=format_iso_timestamp(),
        score=float(pkg.get('downloads', {}).get('last_month', 0) if isinstance(pkg.get('downloads'), dict) else 0),
        tags=['pypi', 'python', 'package'],
        raw={'version': info.get('version'), 'license': info.get('license')}
    )


def normalize_npm_package(pkg: Dict[str, Any]) -> ResearchItem:
    name = pkg.get('name') or 'unknown-package'
    return ResearchItem(
        id=generate_item_id('npm', name),
        provider='npm',
        category='code',
        title=f"npm Package: {name}",
        summary=pkg.get('description') or '',
        url=f"https://www.npmjs.com/package/{name}",
        author=(pkg.get('author') or {}).get('name', '') if isinstance(pkg.get('author'), dict) else str(pkg.get('author') or ''),
        published_at=format_iso_timestamp(),
        score=float(pkg.get('downloads', 0)),
        tags=['npm', 'javascript', 'package'],
        raw={'version': pkg.get('version')}
    )


def normalize_huggingface_model(model: Dict[str, Any]) -> ResearchItem:
    model_id = str(model.get('id') or model.get('modelId') or 'unknown-model')
    return ResearchItem(
        id=generate_item_id('huggingface', model_id),
        provider='huggingface',
        category='ai',
        title=f"HuggingFace Model: {model_id}",
        summary=f"HuggingFace ML Model {model_id}. Pipeline: {model.get('pipeline_tag', 'N/A')}",
        url=f"https://huggingface.co/{model_id}",
        author=model.get('author') or model_id.split('/')[0] if '/' in model_id else '',
        published_at=format_iso_timestamp(model.get('createdAt') or model.get('lastModified')),
        score=float(model.get('likes') or model.get('downloads') or 0),
        tags=[t for t in [model.get('pipeline_tag'), 'huggingface', 'ai'] if t],
        raw={'downloads': model.get('downloads', 0), 'likes': model.get('likes', 0)}
    )
