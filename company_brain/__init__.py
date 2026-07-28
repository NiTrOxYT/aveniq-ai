"""
AVENIQ AI Company Brain Knowledge Package.
Canonical single source of truth for organizational memory, entity relationships, and knowledge retrieval.
"""

from company_brain.service import CompanyBrainService, global_company_brain_service, KnowledgeItem

__all__ = [
    "CompanyBrainService",
    "global_company_brain_service",
    "KnowledgeItem",
]
