"""
Unified Image Provider Factory.
Instantiates and configures the active Image Provider based on IMAGE_PROVIDER environment variable.
Supports 'pollinations' (default) and 'gemini'.
"""

import os
from typing import Optional
from image_generation.providers.gemini_image import BaseImageGenProvider

def get_image_provider(provider_name: Optional[str] = None) -> BaseImageGenProvider:
    name = (
        provider_name
        or os.environ.get("IMAGE_PROVIDER")
        or "pollinations"
    ).strip().lower()

    if name == "pollinations":
        from image_generation.providers.pollinations import PollinationsImageProvider
        return PollinationsImageProvider()
    elif name == "gemini":
        from image_generation.providers.gemini_image import GeminiImageProvider
        return GeminiImageProvider()
    else:
        from image_generation.providers.pollinations import PollinationsImageProvider
        return PollinationsImageProvider()
