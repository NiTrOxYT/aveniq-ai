# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ AI Organization**—the centralized, production-ready runtime knowledge layer, ingestion pipeline, autonomous Strategy Department, evidence-backed Research Department, operational Planning Department, multi-channel Content Department, visual Creative Department, quality gatekeeper Editorial Department, multi-format Delivery Department, and permanent institutional memory Archive Department for AVENIQ software engineering and AI automation systems.

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
├── archive/                      # 10. Archive Department (AI Archivist)
│   ├── context/                  # Archive Context Builder (Delivery + ApprovedContent + Media + Research + Planning)
│   ├── events/                   # Immutable Append-Only Event Store (Lifecycle event replay engine)
│   ├── graph/                    # Directed Knowledge Graph Builder (Multi-hop relationship traversal)
│   ├── embeddings/               # pgvector Vector Embedding Generator & Similarity Search
│   ├── archivists/               # Campaign, Content, Media, Research, Report, Keyword, Topic & Version Archivists
│   ├── indexers/                 # Campaign, Keyword, Topic, Asset SHA-256 & Relationship Indexers
│   ├── search/                   # Multi-Attribute & Full-Text Search Engine across all archived assets
│   ├── engine/                   # Time-Travel Snapshot Engine, Master Archive Engine, Persistence & Retrieval Engine
│   ├── storage/                  # PostgreSQL DDL tables, Supabase Storage buckets & SHA-256 Deduplication Engine
│   ├── repository/               # Local Repository Manager (packages/, manifests/, indexes/, history/, versions/)
│   ├── models/                   # Dataclasses (ArchiveManifest, RelationshipGraph, ArchiveEvent, SnapshotRecord, ArchivePackage, etc.)
│   ├── reports/                  # Master Archive Package Audit Generator
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (11 mandatory archive checklist gates)
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
│   ├── archive.py                # Archive Department CLI Control Center
│   └── validate_company_brain.py # Validation test suite script
│
└── tests/                        # Comprehensive Unit Test Suite
```

---

# Archive Department (AI Archivist)

The **Archive Department** acts as AVENIQ's AI Archivist—the permanent persistence, multi-hop knowledge graph indexing, vector search, time-travel snapshot, and institutional memory layer. It DOES NOT create or edit content; its sole responsibility is preserving every campaign, asset, report, version, and relationship in immutable storage:

- **Immutable Event Store**: Chronologically logs append-only events (`StrategyFormulated`, `ResearchCompleted`, `PlanningCreated`, `ContentGenerated`, `CreativeApproved`, `EditorialPassed`, `DeliveryPackaged`, `ArchiveStored`).
- **Knowledge Graph Builder**: Builds directed multi-hop relationship graph (`Campaign` → `Topic` → `Research` → `Planning` → `Content` → `Creative` → `Editorial` → `Delivery` → `Assets`).
- **Historical Snapshots & Time-Travel Engine**: Generates versioned campaign state snapshots supporting historical retrieval ("Retrieve Campaign v2", "Compare Snapshot v2 vs v5") without data mutation.
- **pgvector Vector Embeddings & Full-Text Search**: Computes 128-dimensional vector embeddings and full-text search indexes across articles, prompts, research, and reports.
- **SHA-256 Asset Deduplication Engine**: Verifies SHA-256 checksums before storage to prevent redundant asset duplication.
- **Lifecycle State Management**: Manages immutable states: `ACTIVE`, `ARCHIVED`, `SUPERSEDED`, `RESTORED`, `LOCKED`.
- **11 Mandatory Quality Gates**:
  1. Delivery package exists
  2. Manifest valid
  3. Metadata complete
  4. Checksums verified
  5. Assets uploaded
  6. Relationships indexed
  7. Versions recorded
  8. Database committed
  9. Storage synchronized
  10. Archive manifest created
  11. Retrieval verified

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
```

### Archive Department CLI
```bash
python3 scripts/archive.py archive      # Persist Delivery Package into immutable Archive Package
python3 scripts/archive.py search       # Execute multi-attribute search query across archived packages
python3 scripts/archive.py retrieve     # Retrieve exact Archive Package by ID or version snapshot
python3 scripts/archive.py validate     # Run archive integrity validation & quality gates
python3 scripts/archive.py report       # Display full Archive Package & Audit Report
python3 scripts/archive.py explain      # Display relationship graph, event log, & vector embedding metrics
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

### Archive REST API (Port 8087)
`python3 archive/api/routes.py` (`GET /archive/search`, `/campaign`, `/package`, `/assets`, `/version`, `/health`)

---

# Unit Testing

Run all unit tests across the codebase:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
