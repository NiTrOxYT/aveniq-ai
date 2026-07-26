"""
Proposal Engine, Proposal Lifecycle Manager, and Human Governance Gatekeeper.
"""

from typing import List, Dict, Any, Optional
from learning.models.proposal import KnowledgeProposal, ProposalCategory, ProposalState, ImpactSimulation
from learning.patterns.pattern_recognizer import ImpactSimulator

class ProposalManager:
    def __init__(self):
        self._proposals: Dict[str, KnowledgeProposal] = {}

    def create_proposal(self, title: str, description: str, proposed_change: str, category: ProposalCategory, workspace_id: str = "ws_default") -> KnowledgeProposal:
        prop_id = f"prp_{abs(hash(title))%10000:04d}"
        sim = ImpactSimulator.simulate_proposal_impact(title)

        prop = KnowledgeProposal(
            proposal_id=prop_id,
            workspace_id=workspace_id,
            category=category,
            title=title,
            description=description,
            proposed_change=proposed_change,
            confidence=0.96,
            evidence_count=8,
            campaign_count=5,
            simulation=sim,
            evidence_list=["cmp_2026-07-26_001", "cmp_2026-07-26_002"],
            state=ProposalState.PROPOSED
        )
        self._proposals[prop_id] = prop
        return prop

    def list_proposals(self, workspace_id: str = None) -> List[KnowledgeProposal]:
        props = list(self._proposals.values())
        if workspace_id:
            props = [p for p in props if p.workspace_id == workspace_id]
        return props

    def approve_proposal(self, proposal_id: str, user: str = "Human Operations Lead") -> Optional[KnowledgeProposal]:
        prop = self._proposals.get(proposal_id)
        if prop:
            prop.state = ProposalState.APPROVED
            prop.approving_user = user
        return prop

    def reject_proposal(self, proposal_id: str, user: str = "Human Operations Lead") -> Optional[KnowledgeProposal]:
        prop = self._proposals.get(proposal_id)
        if prop:
            prop.state = ProposalState.REJECTED
            prop.approving_user = user
        return prop

global_proposal_manager = ProposalManager()
