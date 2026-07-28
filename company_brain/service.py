"""
Centralized Company Brain Service for AVENIQ AI.
Single source of truth for organizational memory, entity extraction, deduplication, revision history, and search.
"""

import json
import os
import re
import hashlib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Set

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = WORKSPACE_ROOT / "knowledge"
STORAGE_DIR = KNOWLEDGE_DIR / "storage"
MEMORIES_FILE = STORAGE_DIR / "memories.json"
ENTITIES_FILE = STORAGE_DIR / "entities.json"
ACTIVITY_FILE = STORAGE_DIR / "activity.json"
REVISIONS_DIR = STORAGE_DIR / "revisions"

VALID_TYPES = {
    "Company", "Product", "Service", "Client", "Competitor", "Market",
    "Technology", "Prompt", "Strategy", "Campaign", "Learning",
    "Incident", "Decision", "Workflow"
}

ENTITY_PATTERNS = {
    "Technology": [r'\b(Python|JavaScript|TypeScript|Gemini|Imagen|Telegram|Docker|Redis|PostgreSQL|PyPI|npm|GitHub|GraphQL|REST|LLM|RAG|Vector)\b'],
    "Company": [r'\b(AVENIQ|Google|OpenAI|Anthropic|Microsoft|Meta|HuggingFace|Y Combinator|Reddit|Product Hunt)\b'],
    "Service": [r'\b(SaaS|Mobile App|Cloud Deployment|AI Automation|Custom Software|UI/UX Design|Web Development|Maintenance)\b']
}


@dataclass
class KnowledgeItem:
    id: str
    title: str
    type: str = "Company"
    category: str = "General"
    tags: List[str] = field(default_factory=list)
    source: str = "Knowledge Base"
    summary: str = ""
    body: str = ""
    url: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = "System"
    confidence: float = 1.0
    references: List[str] = field(default_factory=list)
    related_entities: List[str] = field(default_factory=list)
    ref_count: int = 1
    revision: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def generate_item_id(title: str, source: str) -> str:
    raw = f"{source}:{title.strip().lower()}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]


class CompanyBrainService:
    def __init__(self, knowledge_dir: Path = KNOWLEDGE_DIR):
        self.knowledge_dir = knowledge_dir
        self.storage_dir = STORAGE_DIR
        self.revisions_dir = REVISIONS_DIR
        
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.revisions_dir.mkdir(parents=True, exist_ok=True)

    def _load_json(self, file_path: Path, default: Any) -> Any:
        if not file_path.exists():
            return default
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default

    def _save_json(self, file_path: Path, data: Any):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _extract_entities_from_text(self, text: str) -> Dict[str, List[str]]:
        found = {}
        for ent_type, patterns in ENTITY_PATTERNS.items():
            matches = set()
            for pat in patterns:
                for match in re.findall(pat, text, re.IGNORECASE):
                    matches.add(match.strip())
            if matches:
                found[ent_type] = sorted(list(matches))
        return found

    def scan_knowledge_files(self) -> List[KnowledgeItem]:
        """Scan knowledge/ Markdown files and convert them into live KnowledgeItems."""
        items = []
        if not self.knowledge_dir.exists():
            return items

        for root, _, files in os.walk(self.knowledge_dir):
            if "storage" in root or "__pycache__" in root:
                continue
            for file in files:
                if file.endswith(".md"):
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(self.knowledge_dir)
                    category = rel_path.parts[0] if len(rel_path.parts) > 1 else "General"

                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        # Extract title from # header or filename
                        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                        title = title_match.group(1).strip() if title_match else file.replace(".md", "").replace("-", " ").title()

                        summary_lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#")]
                        summary = summary_lines[0] if summary_lines else content[:200]

                        # Detect type based on path
                        item_type = "Service" if "services" in root else ("Company" if "company" in root or "brand" in root else "Workflow")
                        
                        entities = self._extract_entities_from_text(content)
                        flat_entities = [item for sublist in entities.values() for item in sublist]

                        item_id = generate_item_id(title, f"knowledge/{rel_path}")
                        mtime = datetime.fromtimestamp(full_path.stat().st_mtime, tz=timezone.utc).isoformat()

                        items.append(KnowledgeItem(
                            id=item_id,
                            title=title,
                            type=item_type,
                            category=category.capitalize(),
                            tags=[category.lower(), "documentation", item_type.lower()],
                            source=f"knowledge/{rel_path}",
                            summary=summary[:300],
                            body=content[:2000],
                            url=f"file://{full_path}",
                            created_at=mtime,
                            updated_at=mtime,
                            confidence=1.0,
                            related_entities=flat_entities
                        ))
                    except Exception as e:
                        continue
        return items

    def ingest_item(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest new knowledge item with deduplication, entity extraction, and revision history."""
        title = payload.get("title") or "Untitled Knowledge Item"
        source = payload.get("source") or "Pipeline Ingestion"
        item_id = payload.get("id") or generate_item_id(title, source)

        memories = self._load_json(MEMORIES_FILE, [])
        existing = next((m for m in memories if m.get("id") == item_id or m.get("title").lower() == title.lower()), None)

        now_iso = datetime.now(timezone.utc).isoformat()
        body = payload.get("body", "") or payload.get("summary", "")
        extracted = self._extract_entities_from_text(body + " " + title)
        flat_entities = list(set(payload.get("related_entities", []) + [item for sublist in extracted.values() for item in sublist]))

        if existing:
            # Deduplicate: merge tags, increment ref_count, bump revision
            existing["ref_count"] = existing.get("ref_count", 1) + 1
            existing["revision"] = existing.get("revision", 1) + 1
            existing["updated_at"] = now_iso
            existing["summary"] = payload.get("summary") or existing.get("summary")
            existing["body"] = body or existing.get("body")
            
            # Merge tags
            existing_tags = set(existing.get("tags", []))
            existing_tags.update(payload.get("tags", []))
            existing["tags"] = sorted(list(existing_tags))
            existing["related_entities"] = list(set(existing.get("related_entities", []) + flat_entities))

            # Save revision
            rev_file = self.revisions_dir / f"{item_id}_rev_{existing['revision']}.json"
            self._save_json(rev_file, existing)

            self._save_json(MEMORIES_FILE, memories)
            self._log_activity(f"Knowledge item updated: '{title}' (rev {existing['revision']})")
            return existing
        else:
            # Create new knowledge item
            item_type = payload.get("type", "Learning")
            if item_type not in VALID_TYPES:
                item_type = "Learning"

            new_item = KnowledgeItem(
                id=item_id,
                title=title,
                type=item_type,
                category=payload.get("category", "General"),
                tags=payload.get("tags", ["ingested"]),
                source=source,
                summary=payload.get("summary") or body[:200],
                body=body,
                url=payload.get("url", ""),
                created_at=now_iso,
                updated_at=now_iso,
                created_by=payload.get("created_by", "Automation Pipeline"),
                confidence=float(payload.get("confidence", 1.0)),
                references=payload.get("references", []),
                related_entities=flat_entities
            ).to_dict()

            memories.append(new_item)
            self._save_json(MEMORIES_FILE, memories)

            # Save initial revision
            rev_file = self.revisions_dir / f"{item_id}_rev_1.json"
            self._save_json(rev_file, new_item)

            self._update_entities_and_relationships(new_item, extracted)
            self._log_activity(f"New knowledge ingested: '{title}' ({item_type})")
            return new_item

    def _update_entities_and_relationships(self, item: Dict[str, Any], extracted: Dict[str, List[str]]):
        entities_data = self._load_json(ENTITIES_FILE, {"entities": [], "relationships": []})
        ents = entities_data.setdefault("entities", [])
        rels = entities_data.setdefault("relationships", [])

        item_title = item.get("title")
        for category, names in extracted.items():
            for name in names:
                if not any(e.get("name") == name for e in ents):
                    ents.append({"name": name, "category": category, "discovered_at": datetime.now(timezone.utc).isoformat()})
                # Add relationship: Item -> mentions -> Entity
                rel_id = f"{item['id']}->{name}"
                if not any(r.get("id") == rel_id for r in rels):
                    rels.append({
                        "id": rel_id,
                        "source": item_title,
                        "predicate": "mentions",
                        "target": name,
                        "confidence": 0.95
                    })
        self._save_json(ENTITIES_FILE, entities_data)

    def _log_activity(self, message: str):
        activity = self._load_json(ACTIVITY_FILE, [])
        activity.insert(0, {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": message
        })
        self._save_json(ACTIVITY_FILE, activity[:100])

    def get_all_items(self) -> List[Dict[str, Any]]:
        """Combine scanned markdown documentation and dynamic memories."""
        scanned = [i.to_dict() for i in self.scan_knowledge_files()]
        dynamic = self._load_json(MEMORIES_FILE, [])
        
        # Deduplicate scanned vs dynamic by ID
        seen_ids = set()
        combined = []
        for item in dynamic + scanned:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                combined.append(item)
        combined.sort(key=lambda x: x.get("updated_at") or "", reverse=True)
        return combined

    def search(self, query: str = "", item_type: str = "", source: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        """Search across all knowledge items with keyword & type filters."""
        all_items = self.get_all_items()
        if not query and not item_type and not source:
            return all_items[:limit]

        q_lower = query.lower().strip()
        results = []

        for item in all_items:
            if item_type and item.get("type", "").lower() != item_type.lower():
                continue
            if source and source.lower() not in item.get("source", "").lower():
                continue
            if q_lower:
                title = (item.get("title") or "").lower()
                summary = (item.get("summary") or "").lower()
                body = (item.get("body") or "").lower()
                tags = " ".join(item.get("tags") or []).lower()
                src = (item.get("source") or "").lower()
                
                if q_lower not in title and q_lower not in summary and q_lower not in body and q_lower not in tags and q_lower not in src:
                    continue
            results.append(item)
            if len(results) >= limit:
                break

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """Calculate live metrics from actual storage and files."""
        items = self.get_all_items()
        entities_data = self._load_json(ENTITIES_FILE, {"entities": [], "relationships": []})

        total_bytes = 0
        mtimes = []
        categories = set()
        sources = set()
        tags = set()

        for item in items:
            total_bytes += len(item.get("body", "")) + len(item.get("summary", ""))
            if item.get("category"): categories.add(item.get("category"))
            if item.get("source"): sources.add(item.get("source"))
            for t in item.get("tags", []): tags.add(t)

        for root, _, files in os.walk(self.knowledge_dir):
            for f in files:
                if f.endswith(".md"):
                    p = Path(root) / f
                    total_bytes += p.stat().st_size
                    mtimes.append(p.stat().st_mtime)

        latest_update = datetime.fromtimestamp(max(mtimes), tz=timezone.utc).isoformat() if mtimes else datetime.now(timezone.utc).isoformat()

        return {
            "total_knowledge_items": len(items),
            "categories_count": len(categories),
            "entities_count": len(entities_data.get("entities", [])),
            "relationships_count": len(entities_data.get("relationships", [])),
            "sources_count": len(sources),
            "unique_tags_count": len(tags),
            "storage_size_kb": round(total_bytes / 1024, 2),
            "last_updated": latest_update
        }

    def get_overview(self) -> Dict[str, Any]:
        """Aggregate statistics, top entities, activity feed, and recent items."""
        stats = self.get_statistics()
        items = self.get_all_items()
        entities_data = self._load_json(ENTITIES_FILE, {"entities": [], "relationships": []})
        activity = self._load_json(ACTIVITY_FILE, [])

        return {
            "statistics": stats,
            "recent_items": items[:10],
            "entities": entities_data.get("entities", [])[:15],
            "relationships": entities_data.get("relationships", [])[:15],
            "activity_timeline": activity[:15]
        }


global_company_brain_service = CompanyBrainService()
