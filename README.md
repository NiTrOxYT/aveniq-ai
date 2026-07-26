# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ AI Organization**—the centralized, production-ready runtime knowledge layer, ingestion pipeline, autonomous Strategy Department, evidence-backed Research Department, operational Planning Department, multi-channel Content Department, visual Creative Department, quality gatekeeper Editorial Department, multi-format Delivery Department, permanent institutional memory Archive Department, continuous improvement Learning Department, interactive Human Approval System, Calendar & Campaign Management module, Brand Growth Intelligence module, and the **AVENIQ Workflow Engine (Operating System Orchestrator)** for AVENIQ software engineering and AI automation systems.

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
│
├── workflow/                     # 15. Workflow Engine (Operating System Orchestrator)
│   ├── adapters/                 # Standardized Department Adapters for all 13 Departments
│   ├── events/                   # Pub/Sub Event Bus System & Typed Events
│   ├── execution/                # Enhanced PackageRegistry, DependencyManager, & ExecutionContext
│   ├── reliability/              # State Machine, Error Classifier, & 3-Retry Backoff Engine
│   ├── monitoring/               # Structured Logger, MetricsCollector, & TimelineRecorder
│   ├── engine/                   # Dynamic Pipeline Loader, Master Orchestrator, & Scheduler
│   ├── reports/                  # Multi-Format Report Exporters (JSON, Markdown, HTML)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Workflow Configuration Defaults
│
├── run.py                        # Top-Level Entry Point: python3 run.py
├── scripts/
│   ├── workflow.py               # Workflow Engine CLI Control Center
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
└── tests/                        # Comprehensive Unit Test Suite across all 15 components
```

---

# Workflow Engine (Operating System Orchestrator)

The **Workflow Engine** acts as the operating system for AVENIQ AI, orchestrating all 13 existing departments in exact sequential order:

```
Company Brain → Market Intelligence → Brand Growth Intelligence → Strategy → Calendar → Planning → Content → Creative → Editorial → Delivery → Human Approval → Archive → Learning
```

### Key Architectural Highlights
- **Zero Business Logic Modification**: Orchestration layer only. Departments remain isolated and independently testable.
- **Department Adapter Layer**: Every department is wrapped by a standardized `DepartmentAdapter` (`name`, `version`, `input_packages`, `output_package`, `execute(context)`).
- **Pub/Sub Event Bus**: Emits typed events (`WorkflowStarted`, `WorkflowCompleted`, `DepartmentStarted`, `DepartmentCompleted`, `PackageRegistered`, `RetryStarted`, etc.) without coupling.
- **Enhanced PackageRegistry**: Single source of truth for packages (`register`, `get`, `get_latest`, `get_all`, `get_by_type`, `exists`, `history`, `remove`).
- **Error Classifier & Retry Engine**: Differentiates retryable timeouts from fatal schema/dependency errors and applies exponential backoff retries.
- **Multi-Format Reports**: Exports execution reports in JSON, Markdown, and HTML.

---

# CLI & Quickstart Usage

### Top-Level Organization Execution
```bash
python3 run.py                    # Execute all 13 departments end-to-end
```

### Workflow Engine CLI
```bash
python3 scripts/workflow.py run        # Run master workflow pipeline
python3 scripts/workflow.py status     # Display execution status & metrics
python3 scripts/workflow.py report     # Display execution report (Markdown, JSON, or HTML)
python3 scripts/workflow.py timeline   # Display chronological timeline events
python3 scripts/workflow.py explain    # Display pipeline sequence & adapter registry
```

### Other Department CLIs
```bash
python3 scripts/brain.py validate      # Validate Company Brain manifests & schemas
python3 scripts/strategy.py today      # Generate today's Daily Marketing Strategy Plan
python3 scripts/research.py package    # Generate full evidence-backed Research Package
python3 scripts/planning.py report      # Generate operational Planning Package
python3 scripts/content.py package     # Generate multi-channel Content Package
python3 scripts/creative.py package    # Generate multi-format Media Package
python3 scripts/editorial.py approve   # Run editorial review & generate Approved Package
python3 scripts/delivery.py package    # Assemble multi-platform Delivery Package
python3 scripts/archive.py archive     # Persist into immutable Archive Package
python3 scripts/learning.py analyze    # Run continuous learning analysis sweep
python3 scripts/approval.py session    # Create interactive Approval Session dashboard
python3 scripts/calendar.py month      # Display 30-Day Rolling Calendar
python3 scripts/growth.py goals        # Display Business Goals & Objective Hierarchy
```

---

# REST API Endpoints

### Workflow Engine REST API (Port 8092)
`python3 workflow/api/routes.py` (`POST /workflow/run`, `GET /workflow/status`, `GET /workflow/report`, `GET /workflow/timeline`, `GET /workflow/health`)

### Department REST APIs
- Strategy: `python3 strategy/api/routes.py` (Port 8080)
- Research: `python3 research/api/routes.py` (Port 8081)
- Planning: `python3 planning/api/routes.py` (Port 8082)
- Content: `python3 content/api/routes.py` (Port 8083)
- Creative: `python3 creative/api/routes.py` (Port 8084)
- Editorial: `python3 editorial/api/routes.py` (Port 8085)
- Delivery: `python3 delivery/api/routes.py` (Port 8086)
- Archive: `python3 archive/api/routes.py` (Port 8087)
- Learning: `python3 learning/api/routes.py` (Port 8088)
- Approval: `python3 approval/api/routes.py` (Port 8089)
- Calendar: `python3 calendar_dept/api/routes.py` (Port 8090)
- Growth: `python3 growth/api/routes.py` (Port 8091)

---

# Unit Testing

Run all 69 unit tests across the codebase:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
