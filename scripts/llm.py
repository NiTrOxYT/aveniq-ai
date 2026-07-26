#!/usr/bin/env python3
"""
AVENIQ Real LLM Router CLI Control Center
Command Line Tool for inspecting LLM providers, model mappings, health summary, and testing GPT-5 & Gemini 2.5 Pro inference.

Commands:
  providers  - List active & disabled LLM providers.
  models     - List supported provider models.
  mapping    - Display department-to-model assignments across all 13 departments.
  health     - Display provider health status.
  test       - Test LLM inference for a specific provider.
  status     - Display overall LLM router metrics & cost summary.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from integrations.llm.registry.provider_registry import global_llm_registry
from integrations.llm.configuration.department_mapping import DepartmentMappingRegistry
from integrations.llm.router.llm_router import global_real_llm_router
from integrations.llm.monitoring.cost_tracker import global_cost_tracker

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Real LLM Router CLI Control Center")
    subparsers = parser.add_subparsers(dest="command", help="LLM router commands")

    subparsers.add_parser("providers", help="List registered LLM providers")
    subparsers.add_parser("models", help="List supported LLM models")
    subparsers.add_parser("mapping", help="Display department-to-model assignments")
    subparsers.add_parser("health", help="Display provider health summary")
    
    p_test = subparsers.add_parser("test", help="Test LLM inference")
    p_test.add_argument("--provider", default="openai", choices=["openai", "gemini", "gpt_image"], help="Provider name")
    p_test.add_argument("--department", default="planning", help="Target department")
    p_test.add_argument("--prompt", default="Formulate campaign operational plan", help="Prompt text")

    subparsers.add_parser("status", help="Display router cost & usage metrics")

    args = parser.parse_args()

    if args.command == "providers":
        print("\n=== REGISTERED LLM PROVIDERS ===")
        print(json.dumps({
            "enabled_providers": global_llm_registry.enabled_providers(),
            "disabled_providers": global_llm_registry.disabled_providers()
        }, indent=2))
    elif args.command == "models":
        print("\n=== SUPPORTED PROVIDER MODELS ===")
        print(json.dumps({
            "OpenAI": ["GPT-5", "GPT Image"],
            "Google Gemini": ["Gemini 2.5 Pro"],
            "Anthropic (Disabled)": ["Claude 3.5 Sonnet"],
            "DeepSeek (Disabled)": ["DeepSeek V3"],
            "Qwen (Disabled)": ["Qwen 2.5 72B"]
        }, indent=2))
    elif args.command == "mapping":
        print("\n=== DEPARTMENT MODEL MAPPINGS ===")
        print(json.dumps(DepartmentMappingRegistry.list_mappings(), indent=2))
    elif args.command == "health":
        print("\n=== LLM PROVIDER HEALTH SUMMARY ===")
        print(json.dumps(global_llm_registry.health_summary(), indent=2))
    elif args.command == "test":
        resp = global_real_llm_router.generate(prompt=args.prompt, department=args.department)
        print(f"\n=== TESTING LLM ROUTER ({args.provider.upper()} | Department: '{args.department}') ===")
        print(json.dumps({
            "id": resp.id,
            "provider": resp.provider,
            "model_name": resp.model_name,
            "text": resp.text_content,
            "finish_reason": resp.finish_reason
        }, indent=2))
    elif args.command == "status":
        print("\n=== LLM ROUTER METRICS & COST SUMMARY ===")
        print(json.dumps(global_cost_tracker.get_summary(), indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
