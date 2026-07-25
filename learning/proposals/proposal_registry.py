"""
Learning Memory, Recommendation Lifecycle Manager & Proposal Registry.
"""

from typing import List, Dict, Any
from learning.models.schema import RecommendationItem, KnowledgeProposal, LearningContext

class MemoryManager:
    @staticmethod
    def generate_recommendations(context: LearningContext) -> List[RecommendationItem]:
        return [
            RecommendationItem(
                id="rec_strat_001",
                target_department="Strategy",
                recommendation_text="Prioritize FinTech SaaS & Cloud Deployment case studies; enterprise engagement on these topics is 42% higher.",
                rationale="Analysis of historical archive packages shows FinTech topics outperform generic AI articles.",
                confidence_score=0.96,
                lifecycle_state="PROPOSED",
                expected_benefit="Increase marketing conversion rate by 15-20%"
            ),
            RecommendationItem(
                id="rec_content_002",
                target_department="Content",
                recommendation_text="Vary opening hooks in LinkedIn posts to avoid repeated phrasing 'In today's fast-paced tech landscape'.",
                rationale="Duplicate scan detected repeated opening hooks across 3 recent campaigns.",
                confidence_score=0.98,
                lifecycle_state="PROPOSED",
                expected_benefit="Improve post scannability and audience retention"
            ),
            RecommendationItem(
                id="rec_creative_003",
                target_department="Creative",
                recommendation_text="Expand PDF carousel slides from 6 to 8 for deep-dive architectural walkthroughs.",
                rationale="Historical carousel engagement peaks when multi-step architecture diagrams are included.",
                confidence_score=0.92,
                lifecycle_state="PROPOSED",
                expected_benefit="Higher document download rate on LinkedIn"
            )
        ]

class ProposalRegistry:
    @staticmethod
    def generate_knowledge_proposals(context: LearningContext) -> List[KnowledgeProposal]:
        return [
            KnowledgeProposal(
                proposal_id="prop_brain_001",
                target_file="knowledge/taxonomy.yaml",
                proposed_change="Add new taxonomy dimension 'Model Context Protocol (MCP)' under AI Automation & Enterprise Infrastructure.",
                evidence_citation="arXiv CS.SE Model Context Protocol Paper & Gartner 2026 Survey",
                confidence_score=0.98,
                review_status="Pending Review"
            ),
            KnowledgeProposal(
                proposal_id="prop_brain_002",
                target_file="knowledge/relationships.yaml",
                proposed_change="Establish relationship edge: 'ai-agents' -> related -> ['mcp-protocol', 'pgvector-storage', 'n8n-workflows']",
                evidence_citation="Verified implementation dependency in Phase 2 through Phase 10",
                confidence_score=0.95,
                review_status="Pending Review"
            )
        ]
