"""
Business Goals module for AVENIQ Strategy Department.
Defines the 11 core organizational objectives and strategic alignment rules.
"""

from typing import List, Dict, Any

SUPPORTED_BUSINESS_GOALS = [
    "Lead Generation",
    "Brand Authority",
    "SEO Growth",
    "Product Awareness",
    "Product Launch",
    "Customer Education",
    "Community Growth",
    "Newsletter Growth",
    "Partnership Acquisition",
    "Recruitment",
    "Customer Retention"
]

GOAL_DEFINITIONS = {
    "Lead Generation": {
        "description": "Drive qualified discovery calls, quote inquiries, and project consultations.",
        "preferred_ctas": ["Schedule a discovery call", "Request a custom quotation", "Get in touch with our engineering team"],
        "primary_kpis": ["Discovery Calls Booked", "Inbound Contact Form Submissions"]
    },
    "Brand Authority": {
        "description": "Establish AVENIQ as the premium leader in custom software engineering and AI automation.",
        "preferred_ctas": ["Explore our technical architecture guides", "Read our full case study", "Learn more about our development methodology"],
        "primary_kpis": ["Executive Engagement", "Brand Mentions", "Organic Backlinks"]
    },
    "SEO Growth": {
        "description": "Expand search engine visibility across target commercial and technical keywords.",
        "preferred_ctas": ["Explore our full service guide", "View technical specifications", "Read related engineering case studies"],
        "primary_kpis": ["Organic Keyword Rankings", "Domain Authority", "Organic Traffic Volume"]
    },
    "Product Awareness": {
        "description": "Increase market awareness for AVENIQ's specialized service offerings (e.g. SaaS, AI Agents, n8n).",
        "preferred_ctas": ["Discover our AI Agent solutions", "See how SaaS development works", "Schedule a product walkthrough"],
        "primary_kpis": ["Service Page Views", "Product Page Engagement"]
    },
    "Product Launch": {
        "description": "Announce and drive initial user adoption for newly engineered products, MVPs, or platforms.",
        "preferred_ctas": ["Join the early access program", "Explore the launch demo", "Request launch pricing"],
        "primary_kpis": ["Early Access Sign-Ups", "Launch Demo Views"]
    },
    "Customer Education": {
        "description": "Educate clients on software best practices, workflow automation ROI, and AI adoption frameworks.",
        "preferred_ctas": ["Download the automation framework", "Read the implementation guide", "Schedule an executive briefing"],
        "primary_kpis": ["Document Downloads", "Time-on-Page", "Content Shares"]
    },
    "Community Growth": {
        "description": "Build an engaged network of tech founders, CTOs, and business operations leaders.",
        "preferred_ctas": ["Follow AVENIQ on LinkedIn", "Join our developer & founder circle", "Subscribe to strategic insights"],
        "primary_kpis": ["Follower Growth", "Community Discussions"]
    },
    "Newsletter Growth": {
        "description": "Grow subscriber base for AVENIQ's executive AI and software engineering newsletter.",
        "preferred_ctas": ["Subscribe to our weekly AI strategy briefing", "Get strategic insights delivered to your inbox"],
        "primary_kpis": ["Newsletter Subscribers", "Open Rate", "Click-Through Rate"]
    },
    "Partnership Acquisition": {
        "description": "Attract technology partners, cloud vendors, and complementary agency collaborators.",
        "preferred_ctas": ["Explore strategic partnership opportunities", "Connect with our team"],
        "primary_kpis": ["Partner Inquiries", "Strategic Co-Marketing Agreements"]
    },
    "Recruitment": {
        "description": "Attract top-tier software engineers, AI developers, and UI/UX designers to join AVENIQ.",
        "preferred_ctas": ["View career opportunities at AVENIQ", "Learn about our engineering culture"],
        "primary_kpis": ["Engineering Applications Received", "Talent Pool Growth"]
    },
    "Customer Retention": {
        "description": "Demonstrate continuous value to active clients to promote service contract renewals.",
        "preferred_ctas": ["Schedule a quarterly system review", "Explore new feature add-ons"],
        "primary_kpis": ["Contract Retention Rate", "Account Expansion MRR"]
    }
}

def get_goal_info(goal_name: str) -> Dict[str, Any]:
    return GOAL_DEFINITIONS.get(goal_name, {
        "description": "General business objective",
        "preferred_ctas": ["Schedule a consultation"],
        "primary_kpis": ["Overall Business Engagement"]
    })
