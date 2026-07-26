"""
Provider Capability Definitions for AVENIQ Integration Platform.
"""

from enum import Enum

class ProviderCapability(str, Enum):
    STREAMING = "streaming"
    JSON_OUTPUT = "json_output"
    FUNCTION_CALLING = "function_calling"
    VISION = "vision"
    REASONING = "reasoning"
    EMBEDDINGS = "embeddings"
    IMAGE_GENERATION = "image_generation"
    FILE_UPLOAD = "file_upload"
    WEB_SEARCH = "web_search"
    RESEARCH_FETCH = "research_fetch"
    DOCUMENT_LOAD = "document_load"
