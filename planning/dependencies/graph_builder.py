"""
Asset-First Dependency Graph Engine for Planning Department.
Tracks Requires, Produces, Blocks, and Depends On relationships.
"""

from typing import List, Dict, Any
from planning.models.schema import DependencyNode, DependencyGraph

class DependencyGraphBuilder:
    @staticmethod
    def build_graph() -> DependencyGraph:
        nodes = [
            DependencyNode(
                deliverable_id="del_001_research",
                title="Research Package",
                requires=[],
                produces=["Verified Statistics", "Technical Specs"],
                blocks=["del_002_plan"],
                depends_on=[]
            ),
            DependencyNode(
                deliverable_id="del_002_plan",
                title="Master Planning Package",
                requires=["del_001_research"],
                produces=["Asset Checklist", "Publishing Calendar"],
                blocks=["del_003_hero_image", "del_004_diagram"],
                depends_on=["del_001_research"]
            ),
            DependencyNode(
                deliverable_id="del_003_hero_image",
                title="Dark Glassmorphism Hero Image",
                requires=["del_002_plan"],
                produces=["hero_image.png"],
                blocks=["del_005_technical_guide"],
                depends_on=["del_002_plan"]
            ),
            DependencyNode(
                deliverable_id="del_004_diagram",
                title="MCP Architecture Diagram",
                requires=["del_002_plan"],
                produces=["mcp_diagram.mermaid"],
                blocks=["del_005_technical_guide", "del_006_linkedin_carousel"],
                depends_on=["del_002_plan"]
            ),
            DependencyNode(
                deliverable_id="del_005_technical_guide",
                title="Master Technical Guide",
                requires=["del_003_hero_image", "del_004_diagram"],
                produces=["technical_guide.md"],
                blocks=["del_006_linkedin_carousel", "del_007_newsletter"],
                depends_on=["del_003_hero_image", "del_004_diagram"]
            ),
            DependencyNode(
                deliverable_id="del_006_linkedin_carousel",
                title="LinkedIn Architecture Carousel",
                requires=["del_005_technical_guide"],
                produces=["linkedin_carousel.pdf"],
                blocks=["del_007_newsletter"],
                depends_on=["del_005_technical_guide"]
            ),
            DependencyNode(
                deliverable_id="del_007_newsletter",
                title="Technical Newsletter",
                requires=["del_006_linkedin_carousel"],
                produces=["newsletter_issue.html"],
                blocks=[],
                depends_on=["del_006_linkedin_carousel"]
            )
        ]

        critical_path = [
            "Research Package",
            "Master Planning Package",
            "Hero Image & Diagrams",
            "Master Technical Guide",
            "LinkedIn Carousel",
            "Technical Newsletter"
        ]

        return DependencyGraph(
            nodes=nodes,
            critical_path=critical_path,
            max_dependency_depth=6
        )
