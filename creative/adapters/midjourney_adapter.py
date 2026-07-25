"""
Prompt Adapter Layer for Creative Department.
Converts model-agnostic CreativeSpecifications and SceneGraphs into model-specific prompts
(DALL-E 3, Midjourney, Flux.1, SDXL, Sora, Runway).
"""

from typing import Dict, Any
from creative.models.schema import AIPrompts, SceneGraph

class PromptAdapterEngine:
    @staticmethod
    def generate_all_prompts(scene: SceneGraph, topic: str) -> AIPrompts:
        base_desc = f"A futuristic dark glassmorphism 3D isometric representation of {scene.primary_subject}. {scene.background} with glowing cyan (#38BDF8) electric network lines, dark obsidian background, subtle depth of field, 8k resolution, cinematic lighting."

        dalle3 = f"Ultra-detailed 3D render of {scene.primary_subject} in a dark glassmorphism style. Background features {scene.background} with glowing cyan neon accents and subtle reflection effects."

        midjourney = f"3D isometric glassmorphism render of {scene.primary_subject}, glowing neon cyan accents, dark obsidian background, octane render, 8k --ar 16:9 --v 6.0 --stylize 250 --no blur, text, watermark"

        flux = f"flux_style: dark glassmorphism, 3d render of {scene.primary_subject}, cyan electric illumination, photorealistic reflections, dark theme."

        sdxl_pos = f"masterpiece, best quality, 3d glassmorphism render, {scene.primary_subject}, cyan neon highlights, dark background, 8k resolution, raytracing."
        sdxl_neg = "blurry, low quality, distorted, oversaturated, light background, plain text, watermark, logo."

        sora = f"Cinematic 4k 60fps camera sweep across a dark glassmorphism 3D model of {scene.primary_subject}. Electric cyan energy pulses through floating nodes, volumetric fog, smooth camera motion."

        runway = f"Hyper-smooth 3D motion graphic of {scene.primary_subject}. Neon cyan light trails flowing seamlessly across dark glass surfaces, 24fps cinematic motion."

        return AIPrompts(
            dalle3_prompt=dalle3,
            midjourney_prompt=midjourney,
            flux_prompt=flux,
            sdxl_positive_prompt=sdxl_pos,
            sdxl_negative_prompt=sdxl_neg,
            sora_video_prompt=sora,
            runway_motion_prompt=runway
        )
