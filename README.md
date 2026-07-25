# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ AI Organization**—the centralized, production-ready runtime knowledge layer, ingestion pipeline, autonomous Strategy Department, evidence-backed Research Department, operational Planning Department, multi-channel Content Department, visual Creative Department, quality gatekeeper Editorial Department, multi-format Delivery Department, permanent institutional memory Archive Department, continuous improvement Learning Department, interactive Human Approval System, and Calendar & Campaign Management module for AVENIQ software engineering and AI automation systems.

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
├── learning/                     # 11. Learning Department (AI Learning Manager)
│   ├── context/                  # Learning Context Builder (Archive + Delivery + Prior Learning Memory)
│   ├── memory/                   # Learning Memory Persistence & Recommendation Lifecycle Manager (PROPOSED -> APPROVED -> IMPLEMENTED -> REJECTED)
│   ├── proposals/                # Company Brain Knowledge Proposal Registry & Validator
│   ├── feedback/                 # Cross-Department Feedback Matrix Generators (Strategy, Research, Planning, Content, Creative, Editorial, Delivery)
│   ├── analyzers/                # Publishing, Campaign, Topic, Duplicate, Brand, Prompt & Baseline Impact Analyzers
│   ├── recommenders/             # Prompt, Strategy, Content, Creative & Editorial Recommenders
│   ├── engine/                   # Recommendation Confidence Engine, Pattern Recognition Engine, Master Learning Engine
│   ├── explainability/           # Rationale, Evidence, & Impact Explanation Engine
│   ├── models/                   # Dataclasses (PublishingAnalysis, DuplicateReport, RecommendationItem, KnowledgeProposal, LearningPackage, etc.)
│   ├── reports/                  # Master Learning Package Optimization Report Generator
│   ├── storage/                  # Storage Manager (history/, learning/, memory/, proposals/, versions/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (11 mandatory learning checklist gates)
│
├── approval/                     # 12. Human Approval System (Human-in-the-Loop)
│   ├── context/                  # Approval Context Builder (Delivery + Editorial + Media + Research)
│   ├── workflow/                 # Approval State Machine (CREATED -> PENDING_REVIEW -> IN_REVIEW -> CHANGES_REQUESTED -> REGENERATING -> APPROVED/REJECTED -> ARCHIVED)
│   ├── routing/                  # Centralized Action Router & Department Routing Engine (Strategy, Content, Creative, Editorial, Delivery)
│   ├── review/                   # Threaded Review Manager & Comment Tracker
│   ├── comparison/               # Regenerated Content & Asset Diff Engine
│   ├── telegram/                 # Telegram Dashboard Renderer & Interactive Inline Keyboards
│   ├── notifications/            # Multi-Channel Notification Dispatcher
│   ├── actions/                  # Action Handlers (Approve, Reject, Rewrite, Technical, Simplify, RegenerateHero, GenerateVideo)
│   ├── feedback/                 # Feedback Collector & Immutable Decision Audit Logger
│   ├── engine/                   # Workflow State Machine Engine & Master Human Approval Engine
│   ├── models/                   # Dataclasses (ApprovalSession, HumanDecision, ActionRequest, TelegramDashboardMarkup, ReviewComment, etc.)
│   ├── reports/                  # Master Approval Report Generator
│   ├── storage/                  # Storage Manager (sessions/, decisions/, history/, versions/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (8 mandatory approval checklist gates)
│
├── calendar_dept/                # 13. Calendar & Campaign Management Module
│   ├── context/                  # Calendar Context Builder (Strategy + Planning + History)
│   ├── workflow/                 # Campaign State Machine (PLANNED -> SCHEDULED -> IN_PROGRESS -> READY_FOR_APPROVAL -> APPROVED -> PUBLISHED -> COMPLETED)
│   ├── dependencies/             # Campaign Dependency Graph Builder & Downstream Shift Resolver
│   ├── capacity/                 # Production Capacity & Resource Overbooking Checker
│   ├── templates/                # Reusable Campaign Templates (Product Launch, Webinar, Conference, Educational Series)
│   ├── priority/                 # Strategic & Business Priority Engine
│   ├── blackout/                 # Legal Embargo & Holiday Blackout Window Manager
│   ├── timezone/                 # Timezone & Platform Posting Window Optimizer
│   ├── campaigns/                # Campaign Manager & Constraint Builder
│   ├── schedule/                 # 30-Day Rolling Calendar Builder & Weekly/Daily Schedulers
│   ├── events/                   # National Holiday, Tech Conference, & Product Launch Trackers
│   ├── planners/                 # Cadence, Theme, & Sequence Planners
│   ├── analyzers/                # Overlap, Repetition, & Workload Balancer Analyzers
│   ├── engine/                   # Master Calendar & Campaign Orchestration Engine
│   ├── explainability/           # Scheduling Rationale, Dependency, & Event Explanation Engine
│   ├── models/                   # Dataclasses (CampaignItem, CalendarDay, WeeklyTheme, EventItem, Calendar30Day, Roadmap90Day, CalendarPackage, etc.)
│   ├── reports/                  # Master Calendar Package Scheduling Generator
│   ├── storage/                  # Storage Manager (calendars/, schedules/, history/, versions/)
│   ├── api/                      # REST API Router & JSON Endpoints
│   └── utils/                    # Quality Gate Verifier (10 mandatory calendar checklist gates)
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
│   ├── learning.py               # Learning Department CLI Control Center
│   ├── approval.py               # Human Approval System CLI Control Center
│   ├── calendar.py               # Calendar & Campaign Management CLI Control Center
│   └── validate_company_brain.py # Validation test suite script
│
└── tests/                        # Comprehensive Unit Test Suite
```

---

# Calendar & Campaign Management

The **Calendar & Campaign Management** module acts as AVENIQ's temporal planning engine—the scheduling, campaign orchestration, event awareness, seasonal planning, and conflict prevention layer. It DOES NOT generate or edit content; its sole responsibility is organizing long-term marketing calendars into structured **CalendarPackages**:

- **30-Day Rolling Calendar & 90-Day Roadmap**: Manages daily posting slots, weekly strategic themes, content pillar balance, and quarterly roadmap objectives.
- **Industry Event & Holiday Tracker**: Integrates tech conferences (Gartner, AWS re:Invent, QCon), national holidays (Labor Day, Thanksgiving), and product launch embargoes.
- **Blackout Window & Legal Embargo Manager**: Blocks publishing slots during company holidays, legal blackout windows, or maintenance periods.
- **Campaign Dependency Graph**: Auto-resolves downstream schedule shifts if an upstream campaign (Product Launch → Announcement → Tutorial → Case Study) changes.
- **Production Capacity & Priority Engine**: Evaluates writer/designer capacity and business priority to prevent resource overbooking and protect high-priority campaigns.
- **10 Mandatory Quality Gates**:
  1. Calendar generated
  2. Weekly themes assigned
  3. Monthly campaigns scheduled
  4. No duplicate topics
  5. Publishing cadence validated
  6. Event conflicts checked
  7. Campaign dependencies resolved
  8. Workload balanced
  9. Calendar versioned
  10. Calendar archived

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
```

### Learning Department CLI
```bash
python3 scripts/learning.py analyze     # Run full continuous learning analysis sweep
```

### Human Approval System CLI
```bash
python3 scripts/approval.py session     # Create & render interactive Approval Session dashboard
```

### Calendar & Campaign Management CLI
```bash
python3 scripts/calendar.py month       # Display 30-Day Rolling Marketing Calendar
python3 scripts/calendar.py week        # Display Weekly Strategic Themes & Content Pillars
python3 scripts/calendar.py roadmap     # Display 90-Day Strategic Roadmap & Milestones
python3 scripts/calendar.py events      # Display Industry Conferences, Tech Summits, & Holidays
python3 scripts/calendar.py validate    # Run Calendar Quality Gate & Conflict Audit
python3 scripts/calendar.py explain     # Display scheduling rationale, blackout window checks, & capacity plans
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

### Learning REST API (Port 8088)
`python3 learning/api/routes.py` (`GET /learning/report`, `/recommendations`, `/trends`, `/duplicates`, `/package`, `/health`)

### Approval REST API (Port 8089)
`python3 approval/api/routes.py` (`GET /approval/session`, `POST /approval/approve`, `POST /approval/reject`, `POST /approval/action`, `GET /approval/history`, `GET /approval/health`)

### Calendar REST API (Port 8090)
`python3 calendar_dept/api/routes.py` (`GET /calendar/month`, `/week`, `/day`, `/campaigns`, `/events`, `/package`, `/health`)

---

# Unit Testing

Run all unit tests across the codebase:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
