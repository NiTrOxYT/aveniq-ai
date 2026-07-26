# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ AI Organization**—the centralized, production-ready runtime knowledge layer, ingestion pipeline, autonomous Strategy Department, evidence-backed Research Department, operational Planning Department, multi-channel Content Department, visual Creative Department, quality gatekeeper Editorial Department, multi-format Delivery Department, permanent institutional memory Archive Department, continuous improvement Learning Department, interactive Human Approval System, Calendar & Campaign Management module, Brand Growth Intelligence module, Workflow Engine OS Orchestrator, External Integration Platform, Autonomous Execution Platform, Performance Analytics Platform, Multi-Tenant Workspace Platform, Publishing Platform, Web Dashboard & Customer Portal, Real Market Intelligence Platform, and the **Real LLM Router & Department Model Assignment Platform** for AVENIQ software engineering and AI automation systems.

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
│   └── llm/                      # Real LLM Router Platform
│       ├── configuration/        # Department-to-Model Mapping Registry
│       ├── prompts/              # Department Prompt Templates (Markdown variable injection)
│       ├── context/              # Context Builder & Window Manager
│       ├── memory/               # Workspace Conversation Memory
│       ├── tools/                # Provider-Agnostic Tool Calling Framework
│       ├── providers/            # Real & Skeleton LLM Providers (GPT-5, Gemini 2.5 Pro, Claude, DeepSeek, Qwen)
│       ├── registry/             # Capability-Based Provider Registry
│       ├── fallback/             # Circuit Breaker & Fallback Manager (OpenAI -> Gemini -> Fallback)
│       ├── cache/                # Prompt Semantic Cache
│       └── monitoring/           # Cost Tracker & Audit Logger
├── automation/                   # 17. Autonomous Execution Platform
├── analytics/                    # 18. Performance Analytics Platform
├── workspace/                    # 19. Multi-Tenant Workspace Platform
├── publishing/                   # 20. Publishing & Distribution Platform
├── apps/dashboard/               # 21. Web Dashboard & Customer Portal
│
├── run.py                        # Top-Level Entry Point: python3 run.py
├── scripts/
│   ├── llm.py                    # LLM Router CLI Control Center
│   ├── integrations.py
│   ├── dashboard.py
│   ├── publish.py
│   ├── workspace.py
│   ├── analytics.py
│   ├── automation.py
│   └── workflow.py
│
└── tests/                        # Comprehensive Unit Suite across all 23 components
```

---

# Real LLM Router & Department Model Assignment Platform

The **Real LLM Router & Department Model Assignment Platform** transparently routes inference requests from AI departments to assigned LLM providers and models:

- **Production LLM Providers**: OpenAI (`GPT-5`, `GPT Image`), Google Gemini (`Gemini 2.5 Pro`).
- **Disabled Skeleton Providers**: Anthropic Claude (`Claude 3.5 Sonnet`), DeepSeek (`DeepSeek V3`), Qwen (`Qwen 2.5 72B`).
- **Department Model Mapping**:
  - **Company Brain**, **Market Intelligence**, **Growth**, **Strategy**, **Learning** → **Google Gemini (`Gemini 2.5 Pro`)**
  - **Planning**, **Content**, **Creative (Text)**, **Editorial** → **OpenAI (`GPT-5`)**
  - **Creative (Images)** → **OpenAI (`GPT Image`)**
- **Context Builder & Prompt Templates**: Loads Markdown templates per department and injects variables from Company Brain, Research, Campaign, and Workflow packages.
- **Circuit Breaker & Failover**: Executes transparent failover chain (`OpenAI` → `Gemini` → `Fallback Provider` → `Error`).
- **Cost Tracker & Token Collector**: Calculates prompt/completion tokens, duration, and estimated cost across workspaces and departments.

---

# CLI & Quickstart Usage

### Top-Level Organization Execution
```bash
python3 run.py                                         # Execute all 13 departments end-to-end
```

### LLM Router CLI Control Center
```bash
python3 scripts/llm.py providers                       # List active & disabled LLM providers
python3 scripts/llm.py models                          # List supported provider models
python3 scripts/llm.py mapping                         # Display department-to-model assignments
python3 scripts/llm.py health                          # Display LLM provider health summary
python3 scripts/llm.py test --provider openai          # Test GPT-5 inference with prompt template
python3 scripts/llm.py test --provider gemini          # Test Gemini 2.5 Pro inference
python3 scripts/llm.py status                          # Display router metrics & token cost summary
```

### Other Platform CLIs
- Real Market Intelligence: `python3 scripts/integrations.py research`
- Web Dashboard Portal: `python3 scripts/dashboard.py start`
- Publishing Platform: `python3 scripts/publish.py publish`
- Workspace Platform: `python3 scripts/workspace.py create`
- Analytics Platform: `python3 scripts/analytics.py report`
- Automation Platform: `python3 scripts/automation.py run`
- Workflow OS: `python3 scripts/workflow.py run`

---

# Unit & Integration Testing

Run all 112 unit, integration, automation, analytics, workspace, publishing, dashboard, research, and LLM tests across the codebase:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
