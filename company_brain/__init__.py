"""
AVENIQ AI Company Brain Knowledge Package.
Canonical single source of truth for organizational memory, entity relationships, and knowledge retrieval.
"""

from company_brain.service import CompanyBrainService, global_company_brain_service
from company_brain.repository.knowledge_repository import KnowledgeRepository, global_knowledge_repository

__all__ = [
    "CompanyBrainService",
    "global_company_brain_service",
    "KnowledgeRepository",
    "global_knowledge_repository",
]
