"""
Scene Graph Builder & Visual Specification Engine for Creative Department.
Creates structured representations of composition, lighting, camera, and scene objects.
"""

from typing import Dict, Any
from creative.models.schema import SceneGraph, CreativeSpecification
from creative.adapters.midjourney_adapter import PromptAdapterEngine

class SceneGraphBuilder:
    @staticmethod
    def build_scene_graph(topic: str) -> SceneGraph:
        return SceneGraph(
            background="Dark obsidian grid with subtle floating particle nodes and glowing cyan light beams.",
            foreground="Translucent glassmorphism cards displaying system metrics and active execution states.",
            primary_subject=f"Central glowing AI Agent core processing {topic}",
            secondary_subject="Interconnected PostgreSQL vector database nodes and MCP protocol interfaces",
            environment="High-tech dark futuristic server vault",
            lighting="Volumetric cyan spotlights with rim lighting on glass edges",
            camera="Isometric 35° angle, medium shot, slight depth of field",
            text_elements=["AVENIQ", "MCP PROTOCOL", "SUB-10MS LATENCY"],
            brand_elements=["AVENIQ Cyan Logo", "Obsidian Glass Card"]
        )

class VisualSpecificationBuilder:
    @staticmethod
    def build_visual_spec(topic: str) -> CreativeSpecification:
        scene = SceneGraphBuilder.build_scene_graph(topic)
        prompts = PromptAdapterEngine.generate_all_prompts(scene, topic)

        return CreativeSpecification(
            asset_id=f"spec_{abs(hash(topic)) % 10000:04d}",
            asset_type="Hero Image",
            intent="High-impact technical visual representation for enterprise software guide",
            audience="CTOs, Tech Founders, Senior System Architects",
            composition="Rule of thirds with focal center on glowing AI agent core",
            scene_graph=scene,
            prompts=prompts
        )
