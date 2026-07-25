# AVENIQ AI Systems & Company Brain

Welcome to the **AVENIQ Company Brain** repository—the centralized, production-ready runtime knowledge layer for AVENIQ software development and AI automation systems.

---

# Company Brain Architecture

## Purpose & Overview

The **AVENIQ Company Brain** is an AI-first organizational knowledge architecture designed to serve as the permanent memory for AI agents, retrieval-augmented generation (RAG) pipelines, n8n workflow engines, proposal generators, sales assistants, and customer support bots.

Unlike traditional static marketing documentation, the Company Brain is engineered for:

- **Independent Semantic Chunking**: Heading-level knowledge units optimized for vector embeddings without relative cross-references.
- **Hybrid Retrieval (Vector + Keyword)**: Integrated support for PostgreSQL + `pgvector` cosine similarity and BM25 text search.
- **Knowledge Graph Traversal**: Explicit directional relationships connecting services, technologies, dependencies, and industries.
- **Role-Based Agent Routing**: Standardized priority ordering (Priority 1 through Priority 6) for specialized AI agent roles.
- **Machine & Human Readability**: Clean YAML schemas and structured Markdown source files version-controlled in Git.

---

## Directory Architecture & Ingestion Pipeline

```
aveniq-ai/
├── brain/                        # Ingestion Pipeline Core Package
│   ├── loader/                   # Discovery, Validation, and Metadata Merging
│   │   ├── discovery.py          # Manifest discovery engine
│   │   ├── validator.py          # Schema & link validation engine
│   │   └── metadata_merger.py    # Multi-source metadata merger
│   ├── parser/                   # Markdown AST Parser
│   │   └── markdown_parser.py    # Headings, lists, tables, & frontmatter parser
│   ├── chunker/                  # Heading-Based Semantic Chunker
│   │   └── semantic_chunker.py   # Heading-aligned chunking (800-1200 target tokens)
│   ├── embeddings/               # Provider Abstractions (Dependency Injection)
│   │   ├── base.py               # Abstract EmbeddingProvider interface
│   │   ├── openai_provider.py    # OpenAI embedding abstraction
│   │   ├── gemini_provider.py    # Google Gemini embedding abstraction
│   │   └── mock_provider.py      # Dry-run mock provider
│   ├── storage/                  # Storage Layer Abstractions
│   │   ├── base.py               # Abstract StorageProvider interface
│   │   ├── postgres.py           # PostgreSQL + pgvector storage engine
│   │   └── filesystem.py         # Filesystem local JSON storage engine
│   ├── models/                   # Data Models & DDL Schemas
│   │   ├── schema.py             # Document, Chunk, Embedding, & Relationship models
│   │   └── sql_migrations.sql    # PostgreSQL table DDL & pgvector HNSW indices
│   └── utils/
│       ├── logger.py             # Structured logger
│       └── stats.py              # Ingestion & token cost calculator
│
├── knowledge/                    # Company Knowledge Source Files
│   ├── manifest.yaml             # Master entry point catalog
│   ├── config.yaml               # Global RAG runtime settings & embedding configurations
│   ├── taxonomy.yaml             # Canonical vocabulary across 16 core dimensions
│   ├── relationships.yaml        # Knowledge Graph edge definitions
│   ├── glossary.md               # Standardized technical & business dictionary
│   ├── retrieval.md              # AI agent query routing matrix
│   └── services/                 # Services Knowledge Base (.md & .metadata.yaml)
│
├── scripts/
│   ├── brain.py                  # Brain Loader CLI Control Center
│   └── validate_company_brain.py # Validation test suite script
│
└── tests/                        # Ingestion Pipeline Unit Test Suite
    ├── test_discovery.py
    ├── test_validator.py
    ├── test_parser.py
    ├── test_chunker.py
    └── test_merger.py
```

---

## Brain Loader CLI Usage

The Brain Loader CLI (`scripts/brain.py`) provides full administrative control over the ingestion pipeline:

```bash
# 1. Validate manifest schemas, files, and links
python3 scripts/brain.py validate

# 2. Run full ingestion pipeline (discover, parse, chunk, merge, save)
python3 scripts/brain.py ingest

# 3. View ingestion statistics and token cost estimates
python3 scripts/brain.py stats

# 4. Inspect parsed sections for a specific file
python3 scripts/brain.py parse --file knowledge/services/web-development.md

# 5. Inspect merged data model by document ID
python3 scripts/brain.py inspect --id service_web_development

# 6. Rebuild ingestion cache from scratch
python3 scripts/brain.py rebuild

# 7. Clear ingestion storage cache
python3 scripts/brain.py clear
```

---

## Unit Testing & Verification

Run the full unittesting suite:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

All ingestion components (parser, chunker, validator, discovery, merger) must pass before pushing changes.
