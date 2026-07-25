# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ AI Organization**—the centralized, production-ready runtime knowledge layer, ingestion pipeline, and autonomous Strategy Department for AVENIQ software engineering and AI automation systems.

---

# Architecture Overview

```
aveniq-ai/
├── knowledge/                    # 1. Company Brain Knowledge Layer
│   ├── manifest.yaml             # Master entry point catalog
│   ├── config.yaml               # Global RAG runtime settings
│   ├── taxonomy.yaml             # Canonical vocabulary (16 dimensions)
│   ├── relationships.yaml        # Knowledge Graph edge definitions
│   ├── glossary.md               # Standardized technical & business dictionary
│   ├── retrieval.md              # AI agent query routing matrix
│   └── services/                 # Services Knowledge Base (.md & .metadata.yaml)
│
├── brain/                        # 2. Ingestion Pipeline Layer (Brain Loader)
│   ├── loader/                   # Discovery, Validation, & Metadata Merger
│   ├── parser/                   # Markdown AST Parser
│   ├── chunker/                  # Heading-Based Semantic Chunker (800-1200 tokens)
│   ├── embeddings/               # Provider Abstractions (OpenAI, Gemini, Mock)
│   ├── storage/                  # Storage Layer Abstractions (PostgreSQL/pgvector, Filesystem)
│   └── models/                   # Schema Models & PostgreSQL DDL migrations
│
├── strategy/                     # 3. Strategy Department (AI Chief Marketing Officer)
│   ├── inputs/                   # Strategy Input Normalizer (Brain, Market, Goals, Calendar)
│   ├── context/                  # Unified Strategy Context Builder
│   ├── goals/                    # 11 Core Business Goals & Target Rules
│   ├── guardrails/               # Brand Voice, Tone, & Compliance Engine
│   ├── analyzers/                # Deduplicator, Opportunity Ranker, Persona & Positioning
│   ├── engine/                   # Decision Engine (Rules, Reasoning, Confidence)
│   ├── planners/                 # Chief Strategy Officer & Sub-Planners (Content, SEO, Campaign)
│   ├── reports/                  # Daily, Weekly, & Monthly Report Generator
│   ├── storage/                  # Storage Manager (daily/, weekly/, monthly/, history/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Strategy Analytics Tracker
│
├── scripts/
│   ├── brain.py                  # Brain Loader CLI Control Center
│   ├── strategy.py               # Strategy Department CLI Control Center
│   └── validate_company_brain.py # Validation test suite script
│
└── tests/                        # Comprehensive Unit Test Suite
```

---

# Strategy Department (AI CMO)

The **Strategy Department** acts as AVENIQ's AI Chief Marketing Officer—the decision-making layer of the AI organization. It DOES NOT create raw creative content; its sole responsibility is making strategic decisions:

- **What should AVENIQ talk about?** (Top market opportunity matching core services)
- **Why today?** (High search growth, low competition, strong signal alignment)
- **Who should we target?** (Primary/secondary audience personas & awareness stage)
- **Which platform & format?** (LinkedIn, Website, X; Educational, Case Study, Tutorial, Framework)
- **What business goal does it support?** (Lead Generation, Brand Authority, SEO Growth)
- **What CTA should be used?** (Compliant call-to-action string)

---

# CLI Usage

### Brain Loader CLI
```bash
python3 scripts/brain.py validate   # Validate manifest schemas & file links
python3 scripts/brain.py ingest     # Run full ingestion pipeline
python3 scripts/brain.py stats      # View document/chunk stats & token cost estimates
```

### Strategy Department CLI
```bash
python3 scripts/strategy.py today         # Generate today's Daily Marketing Strategy Plan
python3 scripts/strategy.py weekly        # Generate weekly marketing strategy & campaign focus
python3 scripts/strategy.py monthly       # Generate monthly strategic roadmap
python3 scripts/strategy.py opportunities # Display ranked market opportunities
python3 scripts/strategy.py campaigns     # Display active & planned campaigns
python3 scripts/strategy.py audience      # Display target audience persona profile
python3 scripts/strategy.py seo           # Display SEO keyword priorities
python3 scripts/strategy.py explain       # Display decision reasoning & supporting evidence
```

---

# Strategy REST API Endpoints

Launch the REST API server:
```bash
python3 strategy/api/routes.py
```

JSON GET Endpoints:
- `GET /strategy/today`
- `GET /strategy/weekly`
- `GET /strategy/monthly`
- `GET /strategy/opportunities`
- `GET /strategy/campaigns`
- `GET /strategy/audience`
- `GET /strategy/seo`
- `GET /strategy/health`

---

# Unit Testing

Run all unit tests across the codebase:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
