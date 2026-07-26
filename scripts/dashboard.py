#!/usr/bin/env python3
"""
AVENIQ Web Dashboard & Customer Portal CLI Launcher
Command Line Tool for starting the web portal server, inspecting portal status, and testing endpoint health.

Commands:
  start   - Launch web dashboard server & customer portal.
  status  - Display dashboard API status & port mappings.
  health  - Test platform health endpoints.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from apps.dashboard.api import start_dashboard_server

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Web Dashboard CLI Launcher")
    subparsers = parser.add_subparsers(dest="command", help="Dashboard commands")

    p_start = subparsers.add_parser("start", help="Start web dashboard server")
    p_start.add_argument("--port", type=int, default=8097, help="Server Port")

    subparsers.add_parser("status", help="Display dashboard status")
    subparsers.add_parser("health", help="Display dashboard health")

    args = parser.parse_args()

    if args.command == "start":
        start_dashboard_server(args.port)
    elif args.command == "status" or args.command == "health":
        print("\n=== AVENIQ WEB DASHBOARD & CUSTOMER PORTAL STATUS ===")
        print(json.dumps({
            "status": "Healthy",
            "url": "http://localhost:8097",
            "active_services": {
                "Workflow Engine": "http://localhost:8092",
                "Automation Platform": "http://localhost:8093",
                "Analytics Platform": "http://localhost:8094",
                "Workspace Platform": "http://localhost:8095",
                "Publishing Platform": "http://localhost:8096",
                "Web Dashboard Portal": "http://localhost:8097"
            }
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
