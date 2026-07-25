# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ AI Organization**—the centralized, production-ready runtime knowledge layer, ingestion pipeline, autonomous Strategy Department, evidence-backed Research Department, operational Planning Department, multi-channel Content Department, and visual Creative Department for AVENIQ software engineering and AI automation systems.

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
│   └── api/                      # REST API Router & JSON Endpoints
│
├── research/                     # 4. Research Department (Senior Research Analyst)
│   ├── collectors/               # Statistics, Studies, Technical, Competitor, SEO, Case Study & Source Collectors
│   ├── analyzers/                # Source Validator, Credibility Scorer, Contradiction Detector, Evidence Ranker
│   ├── engine/                   # Research Engine, Synthesis Processor, Verification Engine
│   ├── models/                   # Dataclasses (StatisticItem, AcademicStudy, TechnicalClaim, ResearchPackage, etc.)
│   ├── reports/                  # Research Package Report Generator
│   ├── storage/                  # Storage Manager (packages/, sources/, statistics/, studies/, history/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (8 mandatory checklist gates)
│
├── planning/                     # 5. Planning Department (AI Chief Operations Officer)
│   ├── context/                  # Planning Context Builder (Strategy + Research + Brain)
│   ├── planners/                 # Campaign, Editorial, Publishing, Asset, CTA, Funnel, Distribution, Workflow Planners
│   ├── analyzers/                # Risk Analyzer, Capacity Estimator, Workload Analyzer, Timeline Optimizer
│   ├── engine/                   # Operational Decision Engine, Planning Engine, Dependency Engine, Scheduling Engine
│   ├── calendar/                 # Editorial & Publishing Calendar Engine
│   ├── workflow/                 # 7-State Approval Workflow Engine
│   ├── dependencies/             # Asset-First Dependency Graph Engine (Requires / Produces / Blocks)
│   ├── models/                   # Dataclasses (CampaignPlan, AssetChecklist, DependencyGraph, RiskAssessment, PlanningPackage, etc.)
│   ├── reports/                  # Master Operational Planning Package Generator
│   ├── storage/                  # Storage Manager (campaigns/, schedules/, calendars/, assets/, workflows/, versions/, history/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (11 mandatory operational checklist gates)
│
├── content/                      # 6. Content Department (AI Content Director)
│   ├── context/                  # Content Context Builder (Planning + Research + Brand)
│   ├── generators/               # Master Article, LinkedIn, X Thread, Newsletter, Dev.to, Medium, Landing Page, Email Generators
│   ├── editors/                  # Technical, Marketing, SEO, Grammar, Readability, Compliance Editors
│   ├── transformers/             # Content Reuse Engine (Blog -> LinkedIn -> Carousel -> Newsletter -> Email -> Telegram -> X Thread)
│   ├── analyzers/                # Multi-Dimensional Content Scoring Engine (0-100)
│   ├── engine/                   # Content Decision Engine, Content Engine, Variation Engine
│   ├── workflow/                 # 8-State Review Workflow Engine
│   ├── links/                    # Internal & Knowledge Base Linking Engine
│   ├── models/                   # Dataclasses (ArticleContent, SocialPostContent, ContentPackage, ContentScores, etc.)
│   ├── reports/                  # Master Content Package Report Generator
│   ├── storage/                  # Storage Manager (packages/, history/, drafts/, published/, versions/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (11 mandatory content checklist gates)
│
├── creative/                     # 7. Creative Department (AI Creative Director)
│   ├── context/                  # Creative Context Builder (Planning + Research + Content + Brand)
│   ├── specifications/           # Model-Agnostic Creative Specifications (Visual & Motion)
│   ├── scene/                    # Scene Graph Builder (Foreground, Background, Subject, Camera, Lighting)
│   ├── design/                   # Design Token Loader (Colors, Typography, Spacing, Shadows)
│   ├── directors/                # Art, Visual, Motion, Branding Directors
│   ├── generators/               # Hero Brief, Infographic, Carousel, Thumbnail, Storyboard, Reel, Caption Generators
│   ├── adapters/                 # AI Prompt Adapters (DALL-E 3, Midjourney v6, Flux.1, SDXL, Sora, Runway, Pika, Ideogram)
│   ├── transformers/             # Aspect Ratio Adapter (1:1, 4:5, 16:9, 9:16, 3:2, 2:3) & Accessibility Alt-Text Formatter
│   ├── analyzers/                # Multi-Dimensional Creative Scoring Engine (0-100)
│   ├── engine/                   # Creative Engine & Media Package Synthesizer
│   ├── workflow/                 # 9-State Creative Review Workflow Engine
│   ├── models/                   # Dataclasses (HeroBrief, CarouselDesign, VideoStoryboard, AIPrompts, MediaPackage, etc.)
│   ├── reports/                  # Master Media Package Report Generator
│   ├── storage/                  # Storage Manager (packages/, prompts/, storyboards/, thumbnails/, assets/, versions/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (11 mandatory creative checklist gates)
│
├── scripts/
│   ├── brain.py                  # Brain Loader CLI Control Center
│   ├── strategy.py               # Strategy Department CLI Control Center
│   ├── research.py               # Research Department CLI Control Center
│   ├── planning.py               # Planning Department CLI Control Center
│   ├── content.py                # Content Department CLI Control Center
│   ├── creative.py               # Creative Department CLI Control Center
│   └── validate_company_brain.py # Validation test suite script
│
└── tests/                        # Comprehensive Unit Test Suite
```

---

# Creative Department (AI Creative Director)

The **Creative Department** acts as AVENIQ's AI Creative Director—the visual creative direction, scene graph specification, and multi-model prompt adapter layer. It DOES NOT alter strategy, research conclusions, or written content; its sole responsibility is transforming approved Planning, Research, and Content Packages into executable **Media Packages**:

- **Model-Agnostic Specifications & Scene Graphs**: Defines visual composition, lighting, camera angles, color palettes, visual hierarchy, and scene objects before generating model-specific prompts.
- **Multi-Model AI Prompt Adapters**: Produces executable prompts tailored for **Midjourney v6**, **DALL-E 3**, **Flux.1**, **SDXL (positive & negative prompts)**, **Sora Video**, **Runway Gen-3**, **Pika Labs**, and **Ideogram**.
- **Design System Tokens**: Enforces brand colors (Obsidian background `#020617`, Cyan neon `#38BDF8`), Inter & Fira Code typography, and glassmorphism styling (`backdrop-blur: 16px`).
- **Multi-Platform Aspect Ratio Coverage**: Formats asset specifications for **1:1** (Square), **4:5** (Vertical Feed), **16:9** (Widescreen), **9:16** (Full Vertical), **3:2** (Blog Cover), and **2:3** (Document Cover).
- **Accessibility & Contrast Engine**: Generates screen-reader descriptions and verifies 14.5:1 contrast ratios meeting WCAG AAA standards.
- **11 Mandatory Quality Gates**:
  1. Planning Package loaded
  2. Content Package loaded
  3. Brand guidelines applied
  4. Color palette validated
  5. Typography validated
  6. Platform sizes generated
  7. Accessibility notes included
  8. AI prompts validated
  9. Storyboard complete
  10. Thumbnail complete
  11. Confidence calculated (Minimum 85.0% threshold)

---

# CLI Usage

### Brain Loader CLI
```bash
python3 scripts/brain.py validate   # Validate manifest schemas & file links
python3 scripts/brain.py ingest     # Run full ingestion pipeline
```

### Strategy Department CLI
```bash
python3 scripts/strategy.py today         # Generate today's Daily Marketing Strategy Plan
```

### Research Department CLI
```bash
python3 scripts/research.py package     # Generate full evidence-backed Research Package
```

### Planning Department CLI
```bash
python3 scripts/planning.py report       # Generate full master operational Planning Package
```

### Content Department CLI
```bash
python3 scripts/content.py package     # Generate full multi-channel Content Package
```

### Creative Department CLI
```bash
python3 scripts/creative.py package     # Generate full multi-format Media Package
python3 scripts/creative.py hero        # Display Hero Image Brief & AI prompts (Midjourney, DALL-E 3, Flux, SDXL)
python3 scripts/creative.py infographic # Display process & architecture infographic specifications
python3 scripts/creative.py carousel    # Display multi-slide LinkedIn/Instagram carousel design
python3 scripts/creative.py video       # Display video storyboard, shot list, & Sora video prompt
python3 scripts/creative.py thumbnail   # Display YouTube/Social thumbnail spec & prompt
python3 scripts/creative.py review      # Display quality scores, accessibility alt-text, & quality gates
python3 scripts/creative.py explain     # Display art direction, scene graph, & prompt adapter breakdown
```

---

# REST API Endpoints

### Strategy REST API (Port 8080)
`python3 strategy/api/routes.py` (`GET /strategy/today`, `/weekly`, `/monthly`, `/health`)

### Research REST API (Port 8081)
`python3 research/api/routes.py` (`GET /research/package`, `/topic`, `/statistics`, `/competitors`, `/seo`, `/sources`, `/health`)

### Planning REST API (Port 8082)
`python3 planning/api/routes.py` (`GET /planning/report`, `/campaign`, `/calendar`, `/schedule`, `/assets`, `/workflow`, `/dependencies`, `/health`)

### Content REST API (Port 8083)
`python3 content/api/routes.py` (`GET /content/package`, `/article`, `/linkedin`, `/newsletter`, `/seo`, `/review`, `/health`)

### Creative REST API (Port 8084)
`python3 creative/api/routes.py` (`GET /creative/package`, `/hero`, `/carousel`, `/video`, `/thumbnail`, `/review`, `/health`)

---

# Unit Testing

Run all unit tests across the codebase:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
