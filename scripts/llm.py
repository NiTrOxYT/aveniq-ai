#!/usr/bin/env python3
"""
AVENIQ Real LLM Router CLI Control Center
Command Line Tool for inspecting LLM providers, model mappings, health summary, and testing GPT-5 & Gemini Pro/Flash inference.

Commands:
  providers  - List active & disabled LLM providers with active model status.
  models     - List supported provider models.
  mapping    - Display department-to-model assignments across all 13 departments.
  health     - Display provider health status and candidate model diagnostics.
  test       - Test LLM inference for a specific provider.
  status     - Display overall LLM router metrics & cost summary.
"""

import sys
import os
import argparse
import json

# Add project root to sys.path and remove the scripts/ directory entry
# to prevent local scripts (e.g. calendar.py) from shadowing stdlib modules.
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_scripts_dir = os.path.abspath(os.path.dirname(__file__))
if _scripts_dir in sys.path:
    sys.path.remove(_scripts_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Auto-load .env from project root so credentials are available
_env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.isfile(_env_file):
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                os.environ.setdefault(_k.strip(), _v.strip())

from integrations.llm.registry.provider_registry import global_llm_registry
from integrations.llm.configuration.department_mapping import DepartmentMappingRegistry
from integrations.llm.router.llm_router import global_real_llm_router
from integrations.llm.monitoring.cost_tracker import global_cost_tracker

def _format_health_summary(summary: dict) -> dict:
    formatted = {}
    for name, data in summary.items():
        msg = data.get("message", "")
        # Attempt to parse JSON health payload
        if isinstance(msg, str) and msg.startswith("{") and msg.endswith("}"):
            try:
                parsed_msg = json.loads(msg)
                formatted[name] = {
                    "status": data.get("status"),
                    "configured_primary": parsed_msg.get("primary_model"),
                    "current_serving": parsed_msg.get("active_model"),
                    "fallback_depth": parsed_msg.get("fallback_depth"),
                    "reason": parsed_msg.get("reason"),
                    "models": parsed_msg.get("models", {})
                }
                continue
            except json.JSONDecodeError:
                pass
        formatted[name] = data
    return formatted

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
            "disabled_providers": global_llm_registry.disabled_providers(),
            "health_overview": _format_health_summary(global_llm_registry.health_summary())
        }, indent=2))
    elif args.command == "models":
        print("\n=== SUPPORTED PROVIDER MODELS ===")
        print(json.dumps({
            "OpenAI": ["GPT-5", "GPT Image"],
            "Google Gemini (Quota-Aware Fallback Chain)": [
                os.environ.get("GEMINI_PRIMARY_MODEL", "gemini-2.5-pro"),
                *(m.strip() for m in os.environ.get("GEMINI_FALLBACK_MODELS", "gemini-3.6-flash,gemini-flash-latest,gemini-2.0-flash").split(","))
            ],
            "Anthropic (Disabled)": ["Claude 3.5 Sonnet"],
            "DeepSeek (Disabled)": ["DeepSeek V3"],
            "Qwen (Disabled)": ["Qwen 2.5 72B"]
        }, indent=2))
    elif args.command == "mapping":
        print("\n=== DEPARTMENT MODEL MAPPINGS ===")
        print(json.dumps(DepartmentMappingRegistry.list_mappings(), indent=2))
    elif args.command == "health":
        print("\n=== LLM PROVIDER HEALTH SUMMARY ===")
        print(json.dumps(_format_health_summary(global_llm_registry.health_summary()), indent=2))
    elif args.command == "test":
        resp = global_real_llm_router.generate(prompt=args.prompt, department=args.department)
        print(f"\n=== TESTING LLM ROUTER ({args.provider.upper()} | Department: '{args.department}') ===")
        res_dict = {
            "id": resp.id,
            "provider": resp.provider,
            "configured_primary": resp.metadata.get("primary_model", resp.model_name),
            "current_serving": resp.metadata.get("serving_model", resp.model_name),
            "fallback_count": resp.metadata.get("fallback_count", 0),
            "fallback_reason": resp.metadata.get("fallback_reason", "None"),
            "model_name": resp.model_name,
            "text": resp.text_content,
            "finish_reason": resp.finish_reason
        }
        print(json.dumps(res_dict, indent=2))
    elif args.command == "status":
        print("\n=== LLM ROUTER METRICS & COST SUMMARY ===")
        summary = global_cost_tracker.get_summary()
        summary["gemini_active_serving_model"] = getattr(global_llm_registry.resolve("gemini"), "model_name", "unknown")
        print(json.dumps(summary, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
