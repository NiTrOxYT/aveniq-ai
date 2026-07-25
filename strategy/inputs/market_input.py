"""
Market Intelligence Input Normalizer for Strategy Department.
"""

from typing import Dict, Any, List

class MarketInputNormalizer:
    def load_market_signals(self) -> List[Dict[str, Any]]:
        # Structured market signals from trends, social discussions, competitor moves, and search growth
        return [
            {
                "id": "sig_ai_agent_ops",
                "title": "Autonomous AI Agents for Business Operations",
                "topic": "AI Agents in Enterprise Operations",
                "category": "Intelligent Automation",
                "target_industry": "SaaS",
                "growth_score": 92.5,
                "competition_level": "Low",
                "source_channels": ["Google Trends", "Reddit", "LinkedIn Discussions"]
            },
            {
                "id": "sig_n8n_workflow",
                "title": "n8n Open-Source Workflow Automation vs Proprietary SaaS",
                "topic": "n8n Business Automation",
                "category": "Intelligent Automation",
                "target_industry": "Professional Services",
                "growth_score": 88.0,
                "competition_level": "Medium",
                "source_channels": ["Developer Forums", "Search Volume"]
            },
            {
                "id": "sig_saas_multi_tenancy",
                "title": "Scaling SaaS Multi-Tenancy with PostgreSQL Row-Level Security",
                "topic": "SaaS Multi-Tenancy Architecture",
                "category": "Product Engineering",
                "target_industry": "SaaS",
                "growth_score": 85.0,
                "competition_level": "Medium",
                "source_channels": ["Tech Blogs", "Search Volume"]
            },
            {
                "id": "sig_restaurant_automation",
                "title": "Digitizing Hospitality & Restaurant Order Operations",
                "topic": "Hospitality Software Digitalization",
                "category": "Enterprise Solutions",
                "target_industry": "Hospitality",
                "growth_score": 80.0,
                "competition_level": "Low",
                "source_channels": ["Industry News", "Client Requests"]
            }
        ]
