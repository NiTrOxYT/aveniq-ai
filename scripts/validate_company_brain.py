#!/usr/bin/env python3
"""
AVENIQ Company Brain Automated Validation Suite
Verifies knowledge manifests, taxonomy schemas, config files, graph relationships,
service documents, index integrity, and markdown readability.
"""

import os
import sys
import re

# Optional YAML parser fallback
try:
    import yaml
    HAS_PYYAML = True
except ImportError:
    HAS_PYYAML = False

SERVICES = [
    "web-development",
    "saas-development",
    "custom-software-development",
    "ai-automation",
    "ai-agents",
    "mobile-app-development",
    "ui-ux-design",
    "api-integration",
    "cloud-deployment",
    "maintenance-support"
]

REQUIRED_CORE_FILES = [
    "knowledge/manifest.yaml",
    "knowledge/taxonomy.yaml",
    "knowledge/config.yaml",
    "knowledge/relationships.yaml",
    "knowledge/glossary.md",
    "knowledge/retrieval.md",
    "knowledge/services/index.yaml"
]

REQUIRED_SERVICE_SECTIONS = [
    "## Overview",
    "## Business Value",
    "## Ideal Customers",
    "## Problems We Solve",
    "## Features",
    "## Deliverables",
    "## Technology Stack",
    "## Development Process",
    "## Estimated Timeline",
    "## Pricing Model",
    "## Maintenance",
    "## Frequently Asked Questions",
    "## Cross Sell Opportunities",
    "## Keywords",
    "## Internal Tags"
]

EXACT_PRICING_STRING = "Custom quotation based on project requirements."

def run_validation():
    errors = []
    warnings = []
    successes = []

    print("==================================================")
    print("  AVENIQ COMPANY BRAIN VALIDATION SUITE (Phase 1.5+)")
    print("==================================================\n")

    # 1. Verify Core Files Existence
    for filepath in REQUIRED_CORE_FILES:
        if not os.path.exists(filepath):
            errors.append(f"Missing core file: {filepath}")
        else:
            successes.append(f"Core file present: {filepath}")

    # 2. Validate manifest.yaml and referenced paths
    manifest_path = "knowledge/manifest.yaml"
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_content = f.read()
        
        # Check basic keys
        for key in ["version:", "company_name:", "modules:"]:
            if key not in manifest_content:
                errors.append(f"manifest.yaml missing expected key '{key}'")
            else:
                successes.append(f"manifest.yaml contains '{key}'")

        # Extract paths referenced in manifest
        paths = re.findall(r'path:\s*"([^"]+)"', manifest_content)
        for p in paths:
            if not os.path.exists(p):
                errors.append(f"manifest.yaml references non-existent path: '{p}'")
            else:
                successes.append(f"Manifest path verified: '{p}'")

    # 3. Validate taxonomy.yaml
    taxonomy_path = "knowledge/taxonomy.yaml"
    if os.path.exists(taxonomy_path):
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            tax_content = f.read()
        
        required_tax_keys = [
            "industries:", "technologies:", "programming_languages:", "frameworks:",
            "databases:", "cloud_platforms:", "ai_models:", "ai_tools:",
            "automation_tools:", "customer_types:", "business_sizes:", "service_categories:",
            "project_types:", "deployment_types:", "communication_channels:", "integrations:"
        ]
        for tax_k in required_tax_keys:
            if tax_k not in tax_content:
                errors.append(f"taxonomy.yaml missing category '{tax_k}'")
            else:
                successes.append(f"taxonomy.yaml contains '{tax_k}'")

    # 4. Validate config.yaml
    config_path = "knowledge/config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg_content = f.read()
        for cfg_k in ["brain_version:", "embedding_model:", "chunk_size:", "retrieval:", "hybrid_search:", "vector_database:"]:
            if cfg_k not in cfg_content:
                errors.append(f"config.yaml missing setting '{cfg_k}'")
            else:
                successes.append(f"config.yaml contains '{cfg_k}'")

    # 5. Validate relationships.yaml
    rel_path = "knowledge/relationships.yaml"
    if os.path.exists(rel_path):
        with open(rel_path, "r", encoding="utf-8") as f:
            rel_content = f.read()
        for s in SERVICES:
            if f"{s}:" not in rel_content:
                errors.append(f"relationships.yaml missing relationship mapping for service '{s}'")
            else:
                successes.append(f"relationships.yaml maps service '{s}'")

    # 6. Validate index.yaml references every service
    index_path = "knowledge/services/index.yaml"
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index_content = f.read()
        for s in SERVICES:
            expected_id = f"service_{s.replace('-', '_')}"
            if expected_id not in index_content:
                errors.append(f"index.yaml missing service entry '{expected_id}'")
            else:
                successes.append(f"index.yaml references service '{expected_id}'")

    # 7. Validate all 10 service Markdown and Metadata files
    for s in SERVICES:
        md_file = f"knowledge/services/{s}.md"
        meta_file = f"knowledge/services/{s}.metadata.yaml"

        # Check metadata file
        if not os.path.exists(meta_file):
            errors.append(f"Missing metadata file: {meta_file}")
        else:
            with open(meta_file, "r", encoding="utf-8") as f:
                mcontent = f.read()
                if "id: service_" in mcontent and "name:" in mcontent:
                    successes.append(f"Service metadata verified: {meta_file}")
                else:
                    errors.append(f"{meta_file} missing id/name keys")

        # Check markdown file readability & structure
        if not os.path.exists(md_file):
            errors.append(f"Missing markdown file: {md_file}")
            continue

        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Frontmatter
            if not content.startswith("---"):
                errors.append(f"{md_file}: Missing YAML frontmatter")

            # Word count
            word_count = len(content.split())
            if word_count < 800 or word_count > 1850:
                errors.append(f"{md_file}: Word count ({word_count}) out of target range 800-1850")
            else:
                successes.append(f"{md_file}: Word count readable ({word_count} words)")

            # Required section headings
            for req_sec in REQUIRED_SERVICE_SECTIONS:
                if req_sec not in content:
                    errors.append(f"{md_file}: Missing section heading '{req_sec}'")

            # Pricing string
            if EXACT_PRICING_STRING not in content:
                errors.append(f"{md_file}: Pricing section missing exact string '{EXACT_PRICING_STRING}'")

        except Exception as e:
            errors.append(f"Failed to read markdown file {md_file}: {e}")

    # 8. Report Results
    print("--------------------------------------------------")
    print(f"Passed Checks : {len(successes)}")
    print(f"Warnings      : {len(warnings)}")
    print(f"Failed Errors : {len(errors)}")
    print("--------------------------------------------------\n")

    if errors:
        print("❌ STATUS: FAIL\n")
        print("Diagnostic Failure Details:")
        for err in errors:
            print(f"  - ❌ {err}")
        print("\nPlease fix the above diagnostics before deployment.")
        sys.exit(1)
    else:
        print("✅ STATUS: PASS\n")
        print("All Company Brain core architecture files, schemas, manifests, and services are fully validated!")
        sys.exit(0)

if __name__ == "__main__":
    run_validation()
