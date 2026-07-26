"""
Semantic Topic Clustering Engine for Research Documents.
Groups related documents into unified topic clusters prior to LLM summarization.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from integrations.research.document import ResearchDocument

@dataclass
class ResearchCluster:
    cluster_id: str
    topic_name: str
    documents: List[ResearchDocument] = field(default_factory=list)
    avg_freshness: float = 95.0
    avg_credibility: float = 90.0

class SemanticClusterer:
    @staticmethod
    def cluster_documents(documents: List[ResearchDocument]) -> List[ResearchCluster]:
        if not documents:
            return []

        clusters: Dict[str, List[ResearchDocument]] = {}
        for doc in documents:
            # Simple keyword-based semantic grouping
            key = doc.tags[0] if doc.tags else "general"
            if key not in clusters:
                clusters[key] = []
            clusters[key].append(doc)

        result = []
        for i, (topic, docs) in enumerate(clusters.items()):
            avg_fresh = sum(d.freshness_score for d in docs) / len(docs)
            avg_cred = sum(d.credibility_score for d in docs) / len(docs)
            result.append(ResearchCluster(
                cluster_id=f"cls_{i+1:03d}",
                topic_name=topic.capitalize(),
                documents=docs,
                avg_freshness=round(avg_fresh, 1),
                avg_credibility=round(avg_cred, 1)
            ))
        return result
