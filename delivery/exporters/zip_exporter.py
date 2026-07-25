"""
Multi-Format Exporters for Delivery Department.
Exports Markdown files, HTML previews, JSON manifests, and creates complete .zip archives.
"""

import os, json, zipfile
from typing import Dict, Any
from delivery.models.schema import ExportBundle, DeliveryManifest, PlatformBundle

class MultiFormatExporter:
    @staticmethod
    def export_all(
        delivery_id: str,
        manifest: DeliveryManifest,
        bundles: Dict[str, PlatformBundle],
        output_dir: str = "delivery/storage/exports"
    ) -> ExportBundle:
        os.makedirs(output_dir, exist_ok=True)
        pkg_dir = os.path.join(output_dir, delivery_id)
        os.makedirs(pkg_dir, exist_ok=True)

        # 1. Export JSON Manifest & Summary
        json_path = os.path.join(pkg_dir, "manifest.json")
        data = {
            "delivery_id": manifest.delivery_id,
            "campaign_id": manifest.campaign_id,
            "version": manifest.package_version,
            "topic": manifest.topic,
            "status": manifest.delivery_status,
            "checksums": manifest.checksums,
            "platforms": list(bundles.keys())
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # 2. Export Markdown README & Platform Markdown files
        md_path = os.path.join(pkg_dir, "README.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# AVENIQ Delivery Package: {manifest.topic}\n\n")
            f.write(f"- Delivery ID: {manifest.delivery_id}\n")
            f.write(f"- Campaign: {manifest.campaign_id}\n")
            f.write(f"- Version: {manifest.package_version}\n\n")
            f.write("## Platform Bundles\n")
            for b in bundles.values():
                f.write(f"- **{b.platform_name}**: Best posting time: {b.posting_recommendation.get('best_posting_window')}\n")

        # 3. Export HTML Preview Page
        html_path = os.path.join(pkg_dir, "preview.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(f"<html><head><title>Delivery Package Preview: {manifest.topic}</title></head>")
            f.write(f"<body style='font-family: sans-serif; background: #020617; color: #F8FAFC; padding: 2rem;'>")
            f.write(f"<h1>AVENIQ Delivery Package: {manifest.topic}</h1>")
            f.write(f"<p>Status: <strong>{manifest.delivery_status}</strong></p></body></html>")

        pdf_path = os.path.join(pkg_dir, "delivery_summary.pdf")
        with open(pdf_path, "w", encoding="utf-8") as f:
            f.write(f"%PDF-1.4 Mock PDF summary report for {manifest.delivery_id}")

        # 4. Generate Complete ZIP Archive
        zip_path = os.path.join(output_dir, f"{delivery_id}.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(pkg_dir):
                for file in files:
                    full_p = os.path.join(root, file)
                    arc_p = os.path.relpath(full_p, pkg_dir)
                    zf.write(full_p, arc_p)

        return ExportBundle(
            json_path=json_path,
            markdown_path=md_path,
            html_path=html_path,
            pdf_path=pdf_path,
            zip_path=zip_path
        )
