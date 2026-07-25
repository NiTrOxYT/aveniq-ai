# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ AI Organization**—the centralized, production-ready runtime knowledge layer, ingestion pipeline, autonomous Strategy Department, evidence-backed Research Department, operational Planning Department, multi-channel Content Department, visual Creative Department, quality gatekeeper Editorial Department, and multi-format Delivery Department for AVENIQ software engineering and AI automation systems.

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
├── editorial/                    # 8. Editorial Department (AI Editor-in-Chief)
│   ├── context/                  # Editorial Context Builder (Content + Research + Planning + Brand)
│   ├── issues/                   # Structured Issue Tracker (Severity, Category, Location, Fix, Status)
│   ├── reviewers/                # Grammar, SEO, Brand, Readability, Hallucination, Duplicate, Copyright, Claims, Legal & Accessibility Reviewers
│   ├── analyzers/                # Editorial Scorecard (0-100), Evidence Mapper (Statement -> Citation -> URL), Red Flag Detector & Risk Evaluator
│   ├── engine/                   # Policy Engine (Configurable threshold rules), Publishing Readiness Engine, Diff Engine, Approval Engine
│   ├── workflow/                 # 12-Stage Editorial Approval Workflow
│   ├── models/                   # Dataclasses (EditorialScorecard, ApprovalDecision, EvidenceMap, ApprovedContentPackage, etc.)
│   ├── reports/                  # Master Approved Content Package Generator
│   ├── storage/                  # Storage Manager (reviews/, approvals/, revisions/, reports/, versions/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (11 mandatory editorial checklist gates)
│
├── delivery/                     # 9. Delivery Department (AI Delivery Manager)
│   ├── context/                  # Delivery Context Builder (ApprovedContent + Media + Research + Planning)
│   ├── manifest/                 # Canonical Delivery Manifest Builder (SHA-256 Checksums, Asset Inventory, Status)
│   ├── platforms/                # Platform Capability Profiles (LinkedIn, Instagram, Facebook, X, Threads, Telegram, Website, Newsletter)
│   ├── bundles/                  # Dedicated Platform Bundle Builders (Platform-isolated folders & assets)
│   ├── packagers/                # Content, Media, Attachment, Metadata, Platform Packagers
│   ├── analyzers/                # Delivery Scorecard (0-100), Dependency Checker, Asset Integrity & Completeness Checker
│   ├── engine/                   # Readiness Engine, Master Delivery Packaging Engine, Multi-Format Exporter Engine
│   ├── exporters/                # JSON, Markdown (README.md, article.md), HTML, PDF Summary, ZIP Archive Exporters
│   ├── models/                   # Dataclasses (DeliveryManifest, PlatformBundle, AttachmentItem, DeliveryPackage, DeliveryScore, etc.)
│   ├── reports/                  # Master Delivery Package Report Generator
│   ├── storage/                  # Storage Manager (deliveries/, exports/, history/, versions/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (11 mandatory delivery checklist gates)
│
├── scripts/
│   ├── brain.py                  # Brain Loader CLI Control Center
│   ├── strategy.py               # Strategy Department CLI Control Center
│   ├── research.py               # Research Department CLI Control Center
│   ├── planning.py               # Planning Department CLI Control Center
│   ├── content.py                # Content Department CLI Control Center
│   ├── creative.py               # Creative Department CLI Control Center
│   ├── editorial.py              # Editorial Department CLI Control Center
│   ├── delivery.py               # Delivery Department CLI Control Center
│   └── validate_company_brain.py # Validation test suite script
│
└── tests/                        # Comprehensive Unit Test Suite
```

---

# Delivery Department (AI Delivery Manager)

The **Delivery Department** acts as AVENIQ's AI Delivery Manager—the final packaging, multi-platform folder preparation, SHA-256 checksum verification, and multi-format export layer. It DOES NOT create or edit content/media; its sole responsibility is assembling approved assets into a release-ready **DeliveryPackage**:

- **Canonical Delivery Manifest**: Single source of truth recording Delivery ID, Campaign ID, Package Version, Timestamps, Platform Bundles, Asset Inventory, Reports, Checksums, and Delivery Status.
- **Dedicated Platform Bundles**: Assembles platform-isolated directories (`LinkedIn/`, `Instagram/`, `Facebook/`, `X/`, `Threads/`, `Telegram/`, `Website/`, `Newsletter/`) tailored using platform capability profiles (max caption lengths, allowed media types, recommended aspect ratios, best posting windows).
- **SHA-256 Asset Integrity Checksums**: Generates SHA-256 hashes for all asset files (`hero.webp`, `carousel.pdf`, `reel.mp4`, `thumbnail.png`, `delivery.zip`, `manifest.json`) for physical dependency verification.
- **Multi-Format Exporters**: Emits JSON manifests, Markdown files (`README.md`, `article.md`, `linkedin.md`), HTML preview page, PDF summary report, and complete `.zip` delivery archive.
- **11 Mandatory Quality Gates**:
  1. Content approved
  2. Media approved
  3. Attachments verified
  4. Metadata complete
  5. Platform folders complete
  6. References included
  7. Export generated
  8. Validation passed
  9. Delivery report generated
  10. Confidence calculated (Minimum 85.0% threshold)
  11. Package archived

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
```

### Editorial Department CLI
```bash
python3 scripts/editorial.py approve   # Run full editorial review & generate Approved Content Package
```

### Delivery Department CLI
```bash
python3 scripts/delivery.py package     # Assemble complete multi-platform Delivery Package
python3 scripts/delivery.py export      # Generate multi-format exports (JSON, Markdown, HTML, PDF, ZIP)
python3 scripts/delivery.py attachments # Display asset inventory & SHA-256 checksums
python3 scripts/delivery.py validate    # Run delivery readiness validation & quality gates
python3 scripts/delivery.py report      # Display full Delivery Package Report
python3 scripts/delivery.py explain     # Display delivery manifest & platform bundles
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

### Editorial REST API (Port 8085)
`python3 editorial/api/routes.py` (`GET /editorial/review`, `/report`, `/grammar`, `/seo`, `/claims`, `/approve`, `/health`)

### Delivery REST API (Port 8086)
`python3 delivery/api/routes.py` (`GET /delivery/package`, `/report`, `/attachments`, `/export`, `/validate`, `/health`)

---

# Unit Testing

Run all unit tests across the codebase:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
