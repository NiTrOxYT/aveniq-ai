-- AVENIQ Company Brain PostgreSQL DDL Migration
-- Enables pgvector extension, creates core tables, indices, and foreign keys.

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Versions Table
CREATE TABLE IF NOT EXISTS versions (
    version VARCHAR(32) PRIMARY KEY,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL
);

-- 2. Documents Table
CREATE TABLE IF NOT EXISTS documents (
    id VARCHAR(128) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL UNIQUE,
    content_type VARCHAR(32) NOT NULL,
    priority INT NOT NULL DEFAULT 3,
    embedding_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    raw_content TEXT NOT NULL,
    frontmatter JSONB DEFAULT '{}'::jsonb,
    merged_metadata JSONB DEFAULT '{}'::jsonb,
    version VARCHAR(32) NOT NULL DEFAULT '1.0.0',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_documents_content_type ON documents(content_type);
CREATE INDEX IF NOT EXISTS idx_documents_priority ON documents(priority);
CREATE INDEX IF NOT EXISTS idx_documents_metadata ON documents USING gin(merged_metadata);

-- 3. Chunks Table
CREATE TABLE IF NOT EXISTS chunks (
    id VARCHAR(160) PRIMARY KEY,
    document_id VARCHAR(128) NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    document_title VARCHAR(255) NOT NULL,
    section_title VARCHAR(255) NOT NULL,
    heading_hierarchy TEXT[] NOT NULL DEFAULT '{}',
    text TEXT NOT NULL,
    token_estimate INT NOT NULL,
    keywords TEXT[] NOT NULL DEFAULT '{}',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_keywords ON chunks USING gin(keywords);
CREATE INDEX IF NOT EXISTS idx_chunks_metadata ON chunks USING gin(metadata);
CREATE INDEX IF NOT EXISTS idx_chunks_fts ON chunks USING gin(to_tsvector('english', text));

-- 4. Embeddings Table (pgvector integration)
CREATE TABLE IF NOT EXISTS embeddings (
    id VARCHAR(160) PRIMARY KEY,
    chunk_id VARCHAR(160) NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
    provider VARCHAR(64) NOT NULL,
    model_name VARCHAR(128) NOT NULL,
    vector vector(3072), -- Matches OpenAI text-embedding-3-large
    dimensions INT NOT NULL DEFAULT 3072,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_embeddings_chunk_id ON embeddings(chunk_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_vector_hnsw ON embeddings USING hnsw (vector vector_cosine_ops);

-- 5. Relationships Table (Knowledge Graph Edges)
CREATE TABLE IF NOT EXISTS relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id VARCHAR(128) NOT NULL,
    target_id VARCHAR(128) NOT NULL,
    relationship_type VARCHAR(64) NOT NULL,
    weight NUMERIC(3, 2) DEFAULT 1.0,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_relationship UNIQUE(source_id, target_id, relationship_type)
);

CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_id);
CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_id);

-- 6. Taxonomy Table
CREATE TABLE IF NOT EXISTS taxonomy (
    category VARCHAR(64) PRIMARY KEY,
    values TEXT[] NOT NULL DEFAULT '{}',
    metadata JSONB DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Metadata Audit Table
CREATE TABLE IF NOT EXISTS metadata (
    key VARCHAR(128) PRIMARY KEY,
    value JSONB NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Record Initial Migration Version
INSERT INTO versions (version, description)
VALUES ('1.0.0', 'Initial Company Brain Schema with pgvector support')
ON CONFLICT (version) DO NOTHING;
