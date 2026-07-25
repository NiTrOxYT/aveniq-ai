# AVENIQ Company Brain Glossary

A standardized dictionary of core technical concepts, software architecture patterns, and business terminology used across AVENIQ software products, AI systems, and business documentation.

---

## Technical & Business Terminology

### Software Architecture & Products

#### Software-as-a-Service (SaaS)
A cloud-based software licensing and delivery model in which applications are centrally hosted and accessed by customers over the internet on a recurring subscription basis.

#### Customer Relationship Management (CRM)
A specialized software system designed to manage an organization's interactions, communications, lead pipelines, customer data, and sales histories in a centralized database.

#### Enterprise Resource Planning (ERP)
An integrated software suite used by organizations to manage core daily operational processes—including inventory, procurement, human resources, accounting, and supply chain management.

#### Multi-Tenancy
A software architecture in which a single software instance serves multiple distinct customer accounts (tenants), maintaining strict data isolation and privacy between accounts while sharing computing resources efficiently.

#### Row-Level Security (RLS)
A database security feature—commonly implemented in PostgreSQL and Supabase—that restricts table row access based on the authenticated user's security context or tenant ID, ensuring strict data isolation.

---

## APIs & Integration Protocols

#### Application Programming Interface (API)
A set of defined protocols, functions, and rules that allow separate software applications to communicate and exchange data with one another automatically.

#### REST (Representational State Transfer)
An architectural style for engineering web APIs that utilizes standard HTTP requests (GET, POST, PUT, DELETE) to manipulate stateless resources formatted in JSON or XML.

#### GraphQL
A query language and server runtime for web APIs that enables client applications to request precisely the data fields they need, reducing payload overhead and round-trip requests.

#### Webhooks
Event-driven HTTP callbacks that automatically push real-time data payloads from a source system to a target receiver application immediately when a specific trigger event occurs.

---

## Infrastructure & DevOps

#### Docker
An open-source containerization platform that packages software applications and all their runtime dependencies into lightweight, portable containers, ensuring consistent execution across development, staging, and production environments.

#### Cloudflare
A global edge network provider offering Domain Name System (DNS) resolution, Content Delivery Network (CDN) edge caching, Web Application Firewall (WAF) threat security, and SSL encryption.

#### Infrastructure as Code (IaC)
The practice of managing and provisioning computing infrastructure (servers, firewalls, container networks) through machine-readable configuration code files rather than manual server configurations.

#### Continuous Integration / Continuous Deployment (CI/CD)
Automated DevOps pipelines—such as GitHub Actions—that automatically run unit tests, build application containers, and deploy code changes to production servers whenever developers commit code updates.

#### Service Level Agreement (SLA)
A formal contractual commitment defining guaranteed technical performance standards, uptime expectations, and response time windows for customer support and bug resolution.

---

## Databases & Storage

#### PostgreSQL
A powerful, open-source object-relational database management system (ORDBMS) known for high data integrity, robust SQL support, extensible data types, and enterprise scalability.

#### Supabase
An open-source backend-as-a-service platform built on PostgreSQL that provides instant RESTful/GraphQL APIs, real-time database subscriptions, built-in user authentication, and row-level security.

#### Vector Database
A specialized database engine designed to store, index, and query high-dimensional vector embeddings, enabling ultra-fast mathematical similarity searches for RAG engines and AI applications.

#### Embeddings
Dense numerical vector representations of text, images, or data created by AI models (such as `text-embedding-3-large`) that capture semantic meaning and contextual relationships mathematically.

---

## Artificial Intelligence & Automation

#### Artificial Intelligence Agent (AI Agent)
An autonomous software agent powered by Large Language Models (LLMs) that can reason through goals, break down complex tasks, dynamically select tools, query APIs/databases, and execute multi-step workflows.

#### Retrieval-Augmented Generation (RAG)
An AI architecture pattern that retrieves relevant factual context from a vector database or knowledge base and injects it into an LLM prompt, enabling accurate, context-aware answers without hallucination.

#### Model Context Protocol (MCP)
An open standard framework that allows AI models and agents to securely interface with external corporate databases, file repositories, developer tools, and SaaS APIs through standardized tool-calling interfaces.

#### n8n
An enterprise-grade, self-hostable workflow automation engine used to connect software APIs, process data pipelines, and orchestrate complex background business workflows using visual nodes and custom code.

---

## Security & User Interface

#### Authentication (AuthN)
The security process of verifying the identity of a user or system (e.g., verifying passwords, social logins, magic links, or biometrics).

#### Authorization (AuthZ)
The security process of determining what specific resources, features, or data records an authenticated user or role is permitted to access within an application.

#### User Interface (UI)
The visual and interactive elements of a software application—including screens, buttons, navigation menus, and typography—with which human users directly interact.

#### User Experience (UX)
The overall quality, intuition, ease of use, and efficiency experienced by a human user when interacting with a digital product or service.
