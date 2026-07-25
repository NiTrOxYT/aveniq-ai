# AVENIQ AI Agent Retrieval Guide

This document establishes the official query routing architecture, priority ordering, and retrieval strategies for AI agents, RAG engines, n8n workflows, and automated systems accessing the AVENIQ Company Brain.

---

## 1. Retrieval Priority Architecture

Knowledge modules within the Company Brain are categorized into six strict retrieval priorities. AI agents must evaluate higher-priority sources first before querying lower-priority repositories:

```
Priority 1: Core Identity (Company & Brand)
   ↓
Priority 2: Capabilities (Services & Architecture)
   ↓
Priority 3: Business Evidence (Pricing & Portfolio)
   ↓
Priority 4: Customer Guidance (FAQs & Support)
   ↓
Priority 5: Market Intelligence (Competitors)
   ↓
Priority 6: Promotional Assets (Campaigns & Marketing)
```

### Detailed Priority Hierarchy

| Priority Level | Knowledge Module | Path | Description / Relevance |
| :---: | :--- | :--- | :--- |
| **Priority 1** | Company Profile | [company.md](file:///Users/sourik/projects/aveniq-ai/knowledge/company/company.md) | Mission, core services, target markets, tech stack overview. |
| **Priority 1** | Brand Guide | [brand.md](file:///Users/sourik/projects/aveniq-ai/knowledge/brand/brand.md) | Brand voice, tone, principles, forbidden words, CTA styles. |
| **Priority 2** | Services Catalog | [services/](file:///Users/sourik/projects/aveniq-ai/knowledge/services/) | Deep technical & business specs for all 10 core services. |
| **Priority 2** | Global Taxonomy | [taxonomy.yaml](file:///Users/sourik/projects/aveniq-ai/knowledge/taxonomy.yaml) | Standardized values for technologies, industries, categories. |
| **Priority 2** | Relationships | [relationships.yaml](file:///Users/sourik/projects/aveniq-ai/knowledge/relationships.yaml) | Knowledge Graph edges between services and entities. |
| **Priority 2** | Glossary | [glossary.md](file:///Users/sourik/projects/aveniq-ai/knowledge/glossary.md) | Canonical definitions for software and technical terms. |
| **Priority 3** | Pricing Model | `knowledge/pricing/` | Custom quotation principles & pricing guidelines. |
| **Priority 3** | Portfolio Case Studies | `knowledge/portfolio/` | Project case studies, client testimonials, results. |
| **Priority 4** | FAQs & Support | `knowledge/faqs/` | General client FAQs, resolution paths, support rules. |
| **Priority 5** | Competitor Intelligence | `knowledge/competitors/` | Market positioning, competitor feature comparisons. |
| **Priority 6** | Marketing Campaigns | `knowledge/campaigns/` | Active promotional campaigns, copy templates, assets. |

---

## 2. Query Routing Strategy Matrix

When an AI agent receives a query or task, it uses the routing matrix to select the relevant knowledge modules to retrieve:

### 1. Pricing & Quotation Enquiries
- **Target Modules**: `Priority 3 (Pricing)` → `Priority 2 (Services)`
- **Strategy**: Retrieve pricing quotation rules (`"Custom quotation based on project requirements."`) and cross-reference specific service scope requirements.

### 2. Brand Tone & Voice Alignment
- **Target Modules**: `Priority 1 (Brand)` → `Priority 1 (Company)`
- **Strategy**: Inject brand voice rules, forbidden hype words ("guaranteed", "best company", "magic"), and preferred CTAs into system prompts.

### 3. Proposal & Pitch Deck Generation
- **Target Modules**: `Priority 1 (Company)` + `Priority 1 (Brand)` + `Priority 2 (Services)` + `Priority 3 (Pricing)` + `Priority 3 (Portfolio)`
- **Strategy**: Assemble company context, brand guidelines, target service specifications, custom pricing models, and relevant portfolio case studies.

### 4. Technical Implementation & Architecture Specs
- **Target Modules**: `Priority 2 (Services)` → `Priority 2 (Glossary)` → `Priority 2 (Taxonomy)`
- **Strategy**: Retrieve H2 sections for `Technology Stack`, `Deliverables`, and `Development Process` for target services alongside canonical glossary terms.

### 5. Sales & Lead Qualification
- **Target Modules**: `Priority 2 (Services)` → `Priority 3 (Portfolio)` → `Priority 4 (FAQs)`
- **Strategy**: Match customer pain points against service `Ideal Customers` and `Problems We Solve` sections, backed by case study evidence.

### 6. Customer Support & Issue Resolution
- **Target Modules**: `Priority 4 (FAQs)` → `Priority 2 (Services: maintenance-support.md)`
- **Strategy**: Match customer questions against standard Q&A pairs and SLA maintenance response protocols.

### 7. Competitive Positioning Analysis
- **Target Modules**: `Priority 5 (Competitors)` → `Priority 2 (Services)` → `Priority 1 (Company)`
- **Strategy**: Retrieve competitor comparison matrix and contrast against AVENIQ's unique value propositions.

---

## 3. Role-Based Agent Knowledge Discovery

Future AI agents discover knowledge sources based on their assigned role:

### 1. Sales Agent
- **Allowed Priorities**: 1, 2, 3, 4
- **Primary Modules**: `company.md`, `services/`, `portfolio/`, `pricing/`, `faqs/`
- **Goal**: Qualify leads, match service solutions, communicate pricing policies, and answer prospect questions.

### 2. Marketing Agent
- **Allowed Priorities**: 1, 2, 3, 5, 6
- **Primary Modules**: `brand.md`, `services/`, `portfolio/`, `campaigns/`, `competitors/`
- **Goal**: Generate on-brand copy, promotional campaigns, social posts, and collateral adhering to brand rules.

### 3. Proposal Agent
- **Allowed Priorities**: 1, 2, 3, 4
- **Primary Modules**: `company.md`, `brand.md`, `services/`, `pricing/`, `portfolio/`, `glossary.md`
- **Goal**: Draft customized, technical project proposals, scope specifications, timelines, and quotations.

### 4. Support Agent
- **Allowed Priorities**: 1, 2, 4
- **Primary Modules**: `faqs/`, `services/maintenance-support.md`, `glossary.md`
- **Goal**: Diagnose user tickets, provide SLA guidance, answer system FAQs, and route escalations.

### 5. Technical Consultant Agent
- **Allowed Priorities**: 1, 2, 4
- **Primary Modules**: `services/`, `taxonomy.yaml`, `relationships.yaml`, `glossary.md`
- **Goal**: Recommend optimal technology stacks, architecture diagrams, cloud setups, and API integrations.

### 6. Project Manager Agent
- **Allowed Priorities**: 1, 2
- **Primary Modules**: `services/` (sections: `Development Process`, `Estimated Timeline`, `Deliverables`)
- **Goal**: Structure milestone timelines, deliverable checklists, sprint plans, and operational workflows.

### 7. Content Writer Agent
- **Allowed Priorities**: 1, 2, 3, 6
- **Primary Modules**: `brand.md`, `services/`, `glossary.md`, `campaigns/`
- **Goal**: Produce educational articles, documentation, technical blog posts, and website copy.

---

## 4. RAG Retrieval Mechanics & Search Pipeline

### 1. Hybrid Search Execution (Vector + Keyword)
- **Vector Search**: Query `text-embedding-3-large` embeddings in PostgreSQL `pgvector` using cosine distance to capture semantic intent.
- **Keyword Search**: BM25 keyword search across Markdown headings, internal tags, and keywords.
- **Hybrid Fusion**: Combine vector score (0.7 weight) and BM25 score (0.3 weight) to score results.

### 2. Knowledge Graph Pre-Filtering
Before executing vector similarity searches, AI agents inspect [relationships.yaml](file:///Users/sourik/projects/aveniq-ai/knowledge/relationships.yaml). If a primary service dependency exists (e.g., SaaS Development → UI/UX Design), context from the related service is automatically retrieved to enrich the context window.

### 3. Reranking & Context Window Assembly
- Top 8 candidate chunks are retrieved from PostgreSQL.
- Cohere Rerank v3 reranks candidates to return the top 5 most relevant chunks.
- Selected chunks are formatted into a markdown context block within a 4,000 token budget.

---

## 5. Knowledge Lifecycle States

All knowledge sources within the Company Brain progress through a structured seven-stage lifecycle:

```
Draft ──> Reviewed ──> Approved ──> Embedded ──> Indexed ──> Active ──> Archived
```

1. **Draft**: Content created or edited by human contributor or AI agent; pending review.
2. **Reviewed**: Technical and brand accuracy verified against `brand.md` and `taxonomy.yaml`.
3. **Approved**: Final approval granted by knowledge maintainers.
4. **Embedded**: Semantic vector embeddings generated via `text-embedding-3-large`.
5. **Indexed**: Vectors and metadata stored in PostgreSQL `pgvector` and Graph tables.
6. **Active**: Fully indexed and live for AI agent retrieval.
7. **Archived**: Superseded knowledge retained for historical record but excluded from active AI retrieval.
