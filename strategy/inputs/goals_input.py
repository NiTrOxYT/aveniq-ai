"""
Analytics Input Normalizer.
"""
class AnalyticsInputNormalizer:
    def load_historical_performance(self):
        return {
            "top_performing_topics": ["AI Agents", "SaaS Multi-Tenancy", "n8n Automation"],
            "avg_engagement_rate": 0.048,
            "historical_conversion_rate": 0.032,
            "past_recommendation_count": 14
        }

"""
Campaign Input Normalizer.
"""
class CampaignInputNormalizer:
    def load_active_campaigns(self):
        return [
            {
                "id": "camp_ai_week",
                "name": "AI Automation Week",
                "goal": "Lead Generation",
                "duration_days": 7,
                "primary_audience": "Startup Founders & Tech Executives",
                "target_platforms": ["LinkedIn", "Website", "X"]
            }
        ]

"""
Calendar Input Normalizer.
"""
class CalendarInputNormalizer:
    def load_publishing_calendar(self):
        return {
            "schedule": "Daily",
            "preferred_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "blackout_dates": []
        }

"""
Goals Input Normalizer.
"""
class GoalsInputNormalizer:
    def load_current_goals(self):
        return [
            "Lead Generation",
            "Brand Authority",
            "SEO Growth",
            "Product Awareness"
        ]
