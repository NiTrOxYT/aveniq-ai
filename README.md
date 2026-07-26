# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ AI Organization**—the centralized, production-ready runtime knowledge layer, ingestion pipeline, autonomous Strategy Department, evidence-backed Research Department, operational Planning Department, multi-channel Content Department, visual Creative Department, quality gatekeeper Editorial Department, multi-format Delivery Department, permanent institutional memory Archive Department, continuous improvement Learning Department, interactive Human Approval System, Calendar & Campaign Management module, Brand Growth Intelligence module, Workflow Engine OS Orchestrator, External Integration Platform, Autonomous Execution Platform, Performance Analytics Platform, Multi-Tenant Workspace Platform, Publishing Platform, Web Dashboard & Customer Portal, Real Market Intelligence Platform, Real LLM Router Platform, Knowledge & Retrieval Platform, Image Generation Platform, and the **Closed-Loop Learning Platform (Phase 11)** for AVENIQ software engineering and AI automation systems.

---

# Architecture Overview

```
aveniq-ai/
├── learning/                     # 1. Closed-Loop Learning Platform (Phase 11)
│   ├── bus/                      # Organization-Wide Learning Event Bus (LearningEvent)
│   ├── extractors/               # Positive & Negative Knowledge Extractors
│   ├── patterns/                 # Cross-Campaign Pattern Recognizer
│   ├── simulation/               # Impact Simulation & Forecasting Engine
│   ├── proposals/                # KnowledgeProposal Manager & Impact Ranking
│   ├── governance/               # Human-in-the-Loop Gatekeeper & Traceability Matrix
│   ├── timeline/                 # Organizational Memory Timeline
│   ├── monitoring/               # Learning Readiness Score Engine (0-100 Score)
│   └── reports/                  # Executive Learning Reporter
├── knowledge/                    # 2. Knowledge & Retrieval Platform
├── brain/                        # 3. Ingestion Pipeline Layer (Brain Loader)
├── strategy/                     # 4. Strategy Department (AI Chief Marketing Officer)
├── research/                     # 5. Research Department (Senior Research Analyst)
├── planning/                     # 6. Planning Department (AI Chief Operations Officer)
├── content/                      # 7. Content Department (AI Content Director)
├── creative/                     # 8. Creative Department (AI Creative Director)
├── image_generation/             # 9. Image Generation Platform
├── editorial/                    # 10. Editorial Department (AI Editor-in-Chief)
├── delivery/                     # 11. Delivery Department (AI Delivery Manager)
├── archive/                      # 12. Archive Department (AI Archivist)
├── approval/                     # 13. Human Approval System (Human-in-the-Loop)
├── calendar_dept/                # 14. Calendar & Campaign Management Module
├── growth/                       # 15. Brand Growth Intelligence Module
├── workflow/                     # 16. Workflow Engine (Operating System Orchestrator)
├── integrations/                 # 17. External Integration Platform & LLM Router
├── automation/                   # 18. Autonomous Execution Platform
├── analytics/                    # 19. Performance Analytics Platform
├── workspace/                    # 20. Multi-Tenant Workspace Platform
├── publishing/                   # 21. Publishing & Distribution Platform
├── apps/dashboard/               # 22. Web Dashboard & Customer Portal
│
├── run.py                        # Top-Level Entry Point: python3 run.py
├── scripts/
│   ├── learning_loop.py          # Closed-Loop Learning Platform CLI
│   ├── image.py
│   ├── knowledge.py
│   ├── llm.py
│   ├── integrations.py
│   ├── dashboard.py
│   ├── publish.py
│   ├── workspace.py
│   ├── analytics.py
│   ├── automation.py
│   └── workflow.py
│
└── tests/                        # Comprehensive Unit Suite across all 26 components
```

---

# Closed-Loop Learning Platform (Phase 11)

The **Closed-Loop Learning Platform** continuously improves future campaigns by extracting insights from execution history, performance metrics, and human feedback:

- **Organization-Wide Event Bus**: Subscribes 15 system components to publish `LearningEvent` models (`CONTENT_APPROVED`, `CONTENT_REJECTED`, `LOW_CTR`, `BRAND_VIOLATION`, etc.).
- **Positive & Negative Extractors**: Identifies winning headlines, CTAs, layout preferences, and negative lessons from rejections or low CTRs.
- **Cross-Campaign Pattern Recognizer**: Identifies multi-campaign trends (e.g. 5-slide carousels outperforming static posts by +34% CTR).
- **Proposal Impact Simulator**: Forecasts expected CTR delta, conversion changes, and approval probability before proposing changes.
- **Human Governance Gatekeeper**: Manages proposal lifecycles across 10 categories (`PROPOSED` → `UNDER_REVIEW` → `APPROVED` → `IMPLEMENTED`). Zero automatic mutations to Company Brain without explicit human approval.
- **Learning Readiness Score (0-100)**: Evaluates organizational learning velocity, backlog, freshness, and implementation rate.

---

# CLI & Quickstart Usage

### Top-Level Organization Execution
```bash
python3 run.py                                         # Execute all 13 departments end-to-end
```

### Closed-Loop Learning CLI
```bash
python3 scripts/learning_loop.py proposals             # List knowledge improvement proposals & forecasted CTR impact
python3 scripts/learning_loop.py patterns              # List cross-campaign pattern recognition insights
python3 scripts/learning_loop.py readiness             # Calculate Learning Readiness Score (0-100)
python3 scripts/learning_loop.py timeline              # Display chronological organizational memory timeline
python3 scripts/learning_loop.py reports               # Generate executive organizational learning report
python3 scripts/learning_loop.py approve --prop-id <ID># Approve a knowledge proposal (Human Governance)
python3 scripts/learning_loop.py status                # Display learning platform status & event count
```

### Other Platform CLIs
- Image Generation: `python3 scripts/image.py generate`
- Knowledge Platform: `python3 scripts/knowledge.py index`
- Real LLM Router: `python3 scripts/llm.py test`
- Real Market Intelligence: `python3 scripts/integrations.py research`
- Web Dashboard Portal: `python3 scripts/dashboard.py start`
- Publishing Platform: `python3 scripts/publish.py publish`
- Workspace Platform: `python3 scripts/workspace.py create`
- Analytics Platform: `python3 scripts/analytics.py report`
- Automation Platform: `python3 scripts/automation.py run`
- Workflow OS: `python3 scripts/workflow.py run`

---

# Unit & Integration Testing

Run all 132 unit, integration, automation, analytics, workspace, publishing, dashboard, research, LLM, knowledge, image, and learning tests across the codebase:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
