# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ AI Organization**—the centralized, production-ready runtime knowledge layer, ingestion pipeline, autonomous Strategy Department, evidence-backed Research Department, operational Planning Department, multi-channel Content Department, visual Creative Department, quality gatekeeper Editorial Department, multi-format Delivery Department, permanent institutional memory Archive Department, continuous improvement Learning Department, interactive Human Approval System, Calendar & Campaign Management module, Brand Growth Intelligence module, Workflow Engine OS Orchestrator, External Integration Platform, Autonomous Execution Platform, Performance Analytics Platform, Multi-Tenant Workspace & Organization Platform, and the **AVENIQ Publishing & Distribution Platform (Phase 7)** for AVENIQ software engineering and AI automation systems.

---

# Architecture Overview

```
aveniq-ai/
├── knowledge/                    # 1. Company Brain Knowledge Layer
├── brain/                        # 2. Ingestion Pipeline Layer (Brain Loader)
├── strategy/                     # 3. Strategy Department (AI Chief Marketing Officer)
├── research/                     # 4. Research Department (Senior Research Analyst)
├── planning/                     # 5. Planning Department (AI Chief Operations Officer)
├── content/                      # 6. Content Department (AI Content Director)
├── creative/                     # 7. Creative Department (AI Creative Director)
├── editorial/                    # 8. Editorial Department (AI Editor-in-Chief)
├── delivery/                     # 9. Delivery Department (AI Delivery Manager)
├── archive/                      # 10. Archive Department (AI Archivist)
├── learning/                     # 11. Learning Department (AI Learning Manager)
├── approval/                     # 12. Human Approval System (Human-in-the-Loop)
├── calendar_dept/                # 13. Calendar & Campaign Management Module
├── growth/                       # 14. Brand Growth Intelligence Module
├── workflow/                     # 15. Workflow Engine (Operating System Orchestrator)
├── integrations/                 # 16. External Integration Platform
├── automation/                   # 17. Autonomous Execution Platform
├── analytics/                    # 18. Performance Analytics Platform
├── workspace/                    # 19. Multi-Tenant Workspace Platform
│
├── config/                       # Configuration Profiles (providers.yaml)
│
├── publishing/                   # 20. Publishing & Distribution Platform (Phase 7)
│   ├── models/                   # Publication Data Model & PublicationState Lifecycle State Machine
│   ├── adaptation/               # Content Adaptation Layer (Content, Image, Metadata Adapters)
│   ├── assets/                   # Publication Asset Manager (Images, Videos, Thumbnails, Alt Text)
│   ├── providers/                # Provider-Agnostic Channel Publishers (LinkedIn, X, FB, IG, WP, Medium, Ghost, Dev.to, Hashnode, Webhook)
│   ├── capability/               # Provider Capability Registry (SCHEDULING, ROLLBACK, CAROUSEL, VIDEO, DRAFT)
│   ├── router/                   # Master Publisher, Formatter & Scheduler
│   ├── history/                  # Publication Store Persistence Manager
│   ├── queue/                    # Async Publishing Queue with Dead-Letter Queue & Retries
│   ├── verification/             # Delivery Verifier (URL & Payload Validation)
│   ├── rollback/                 # Rollback Manager (Unpublish & Post Deletion)
│   ├── audit/                    # Immutable Publication Audit Logger
│   ├── monitoring/               # Publishing Metrics & Analytics Hooks
│   └── api/                      # REST API Router & JSON Endpoints
│
├── run.py                        # Top-Level Entry Point: python3 run.py
├── scripts/
│   ├── publish.py                # Publishing CLI Control Center
│   ├── workspace.py
│   ├── analytics.py
│   ├── automation.py
│   ├── integrations.py
│   ├── workflow.py
│   ├── brain.py
│   ├── strategy.py
│   ├── research.py
│   ├── planning.py
│   ├── content.py
│   ├── creative.py
│   ├── editorial.py
│   ├── delivery.py
│   ├── archive.py
│   ├── learning.py
│   ├── approval.py
│   ├── calendar.py
│   └── growth.py
│
└── tests/                        # Comprehensive Unit Suite across all 20 components
```

---

# Publishing & Distribution Platform (Phase 7)

The **Publishing & Distribution Platform** distributes human-approved marketing campaigns across 10 supported channels via provider abstractions:

- **10 Provider Abstractions**: `LinkedIn`, `X`, `Facebook`, `Instagram`, `WordPress`, `Medium`, `Ghost`, `Dev.to`, `Hashnode`, and `Generic Webhook`.
- **Publication State Machine**: Validates transitions (`CREATED` → `QUEUED` → `SCHEDULED` → `PUBLISHING` → `PUBLISHED` → `VERIFIED` / `FAILED` / `RETRYING` / `ROLLED_BACK` / `CANCELLED`).
- **Content Adaptation Layer**: Optimizes assets per channel without altering original campaigns (e.g. X 280-char thread splitting, LinkedIn hashtags, WordPress HTML, Dev.to/Medium Markdown).
- **Capability Registry**: Advertises channel capabilities (`SCHEDULING`, `ROLLBACK`, `CAROUSEL`, `VIDEO`, `DRAFT`, `THREADING`).
- **Delivery Verifier & Rollback**: Verifies published URLs and handles post unpublishing / deletion where supported.
- **Async Queue & Dead-Letter Queue**: Handles delayed execution, retries, and dead-letter queueing for failed deliveries.

---

# CLI & Quickstart Usage

### Top-Level Organization Execution
```bash
python3 run.py                         # Execute all 13 departments end-to-end
```

### Publishing Platform CLI
```bash
python3 scripts/publish.py publish --channel LinkedIn # Publish approved campaign to target channel
python3 scripts/publish.py providers                # Display supported channels & capabilities
python3 scripts/publish.py history                  # Display publication history & delivery URLs
python3 scripts/publish.py rollback --pub-id <ID>    # Unpublish post from target channel
python3 scripts/publish.py status                   # Display publishing queue status
```

### Other Platform CLIs
- Workspace Platform: `python3 scripts/workspace.py create`
- Analytics Platform: `python3 scripts/analytics.py report`
- Automation Platform: `python3 scripts/automation.py run`
- Integration Platform: `python3 scripts/integrations.py health`
- Workflow OS: `python3 scripts/workflow.py run`

---

# REST API Endpoints

### Publishing REST API (Port 8096)
`python3 publishing/api/routes.py` (`POST /publish`, `POST /publish/schedule`, `POST /publish/cancel`, `POST /publish/rollback`, `GET /publish/history`, `GET /publish/status`, `GET /publish/providers`, `GET /publish/health`)

---

# Unit & Integration Testing

Run all 99 unit, integration, automation, analytics, workspace, and publishing tests across the codebase:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
