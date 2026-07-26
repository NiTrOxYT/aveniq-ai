"""
Global Provider Registry and Provider Auto-registration.
"""

from integrations.registry.provider_registry import ProviderRegistry
from integrations.mocks.framework import (
    MockLLMProvider, MockImageProvider, MockResearchProvider, MockCompanyBrainProvider
)
from integrations.llm.router import OpenAIProvider, AnthropicProvider, GeminiProvider, QwenProvider
from integrations.image.router import GPTImageProvider, FluxProvider, StableDiffusionProvider
from integrations.company_brain.document import MarkdownBrainProvider, JSONBrainProvider, YAMLBrainProvider
from integrations.research.document import RedditConnector, HackerNewsConnector, GitHubTrendingConnector

global_registry = ProviderRegistry()

# Register Mock Providers
global_registry.register(MockLLMProvider())
global_registry.register(MockImageProvider())
global_registry.register(MockResearchProvider())
global_registry.register(MockCompanyBrainProvider())

# Register Real Providers
global_registry.register(OpenAIProvider())
global_registry.register(AnthropicProvider())
global_registry.register(GeminiProvider())
global_registry.register(QwenProvider())

global_registry.register(GPTImageProvider())
global_registry.register(FluxProvider())
global_registry.register(StableDiffusionProvider())

global_registry.register(MarkdownBrainProvider())
global_registry.register(JSONBrainProvider())
global_registry.register(YAMLBrainProvider())

global_registry.register(RedditConnector())
global_registry.register(HackerNewsConnector())
global_registry.register(GitHubTrendingConnector())
