"""
Entity Extraction Domain Service for Company Brain.
Extracts named entities from text with category classification.
"""

import re
from typing import Dict, List

ENTITY_PATTERNS = {
    "Technology": [r'\b(Python|JavaScript|TypeScript|Gemini|Imagen|Telegram|Docker|Redis|PostgreSQL|PyPI|npm|GitHub|GraphQL|REST|LLM|RAG|Vector)\b'],
    "Company": [r'\b(AVENIQ|Google|OpenAI|Anthropic|Microsoft|Meta|HuggingFace|Y Combinator|Reddit|Product Hunt)\b'],
    "Service": [r'\b(SaaS|Mobile App|Cloud Deployment|AI Automation|Custom Software|UI/UX Design|Web Development|Maintenance)\b']
}


class ExtractionService:
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        found = {}
        for ent_type, patterns in ENTITY_PATTERNS.items():
            matches = set()
            for pat in patterns:
                for match in re.findall(pat, text, re.IGNORECASE):
                    matches.add(match.strip())
            if matches:
                found[ent_type] = sorted(list(matches))
        return found


global_extraction_service = ExtractionService()
