"""
Platform Capability Profiles & Dedicated Bundle Builders for AVENIQ Delivery Department.
"""

import hashlib
from typing import Dict, Any, List
from delivery.models.schema import PlatformProfile, PlatformBundle, AttachmentItem, DeliveryContext

class PlatformProfiles:
    @staticmethod
    def get_profiles() -> Dict[str, PlatformProfile]:
        return {
            "linkedin": PlatformProfile("LinkedIn", 3000, ["Image", "PDF Carousel", "Video"], ["1:1", "4:5"], "Tuesday 09:00 AM EST"),
            "instagram": PlatformProfile("Instagram", 2200, ["Image", "Reel Video", "Carousel"], ["1:1", "4:5", "9:16"], "Wednesday 11:00 AM EST"),
            "facebook": PlatformProfile("Facebook", 5000, ["Image", "Video", "Link"], ["16:9", "1:1"], "Thursday 01:00 PM EST"),
            "x": PlatformProfile("X / Twitter", 280, ["Image", "Video"], ["16:9", "1:1"], "Monday 08:30 AM EST"),
            "threads": PlatformProfile("Threads", 500, ["Image", "Video"], ["1:1", "9:16"], "Tuesday 06:00 PM EST"),
            "telegram": PlatformProfile("Telegram", 4096, ["Image", "Document"], ["16:9", "1:1"], "Daily 10:00 AM EST"),
            "website": PlatformProfile("Website / Blog", 50000, ["Hero Image", "Infographic", "Diagram"], ["16:9", "3:2"], "Immediate"),
            "newsletter": PlatformProfile("Newsletter", 20000, ["Header Image", "CTA Button"], ["16:9"], "Tuesday 07:00 AM EST")
        }

class DedicatedBundleBuilder:
    @staticmethod
    def build_all_bundles(context: DeliveryContext) -> Dict[str, PlatformBundle]:
        bundles = {}
        profiles = PlatformProfiles.get_profiles()

        topic = context.approved_content_package.get("topic", "AI Operations")
        hashtags = ["#AIEngineering", "#EnterpriseAI", "#MCPProtocol", "#AVENIQ", "#SoftwareArchitecture"]
        cta = "https://aveniq.ai/contact"

        # Attachments
        hero_att = AttachmentItem(
            asset_id="att_hero_001",
            filename="hero.webp",
            asset_type="Hero Image",
            relative_path="assets/hero.webp",
            mime_type="image/webp",
            sha256_checksum=hashlib.sha256(f"hero_{topic}".encode()).hexdigest(),
            file_size_bytes=420100
        )

        carousel_att = AttachmentItem(
            asset_id="att_carousel_001",
            filename="carousel.pdf",
            asset_type="PDF Carousel",
            relative_path="assets/carousel.pdf",
            mime_type="application/pdf",
            sha256_checksum=hashlib.sha256(f"carousel_{topic}".encode()).hexdigest(),
            file_size_bytes=1840000
        )

        for p_key, prof in profiles.items():
            copy_text = f"Approved content for {prof.platform_name}: {topic}. Detailed technical walkthrough available."
            att_list = [hero_att]
            if p_key in ["linkedin", "instagram"]:
                att_list.append(carousel_att)

            bundles[p_key] = PlatformBundle(
                platform_name=prof.platform_name,
                folder_name=p_key,
                copy_text=copy_text,
                hashtags=hashtags,
                cta_link=cta,
                metadata={
                    "max_caption_len": prof.max_caption_length,
                    "target_audience": "Senior Tech Leaders & Engineers"
                },
                attachments=att_list,
                posting_recommendation={
                    "best_posting_window": prof.best_posting_window,
                    "recommended_aspect_ratios": ", ".join(prof.recommended_aspect_ratios)
                }
            )

        return bundles
