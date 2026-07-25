#!/usr/bin/env python3
"""
AVENIQ Company Brain CLI Control Center
Command Line Tool for executing Brain Loader operations.

Commands:
  validate  - Run validation suite across manifests, schemas, and files.
  ingest    - Run full ingestion pipeline (discover, parse, chunk, merge, save).
  parse     - Inspect parsed Markdown sections for a given file.
  chunk     - Inspect semantic chunks generated for knowledge documents.
  stats     - Print ingestion statistics and token cost estimates.
  inspect   - Inspect full merged document data model by document ID.
  rebuild   - Clear existing storage and re-run full ingestion pipeline.
  clear     - Wipe all generated document and chunk storage.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from brain.utils.logger import get_logger
from brain.loader.discovery import DiscoveryEngine
from brain.loader.validator import ValidationEngine
from brain.loader.metadata_merger import MetadataMerger
from brain.parser.markdown_parser import MarkdownParser
from brain.chunker.semantic_chunker import SemanticChunker
from brain.storage.filesystem import FilesystemStorageProvider
from brain.models.schema import DocumentModel
from brain.utils.stats import StatsAggregator

logger = get_logger("aveniq.brain.cli")

def cmd_validate(args):
    validator = ValidationEngine()
    issues = validator.validate_all()
    errors = [i for i in issues if i.severity == "ERROR"]
    warnings = [i for i in issues if i.severity == "WARNING"]

    if warnings:
        print("\n⚠️ VALIDATION WARNINGS:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("\n❌ VALIDATION ERRORS FOUND:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\n✅ VALIDATION PASSED! All core manifests, schemas, and files are 100% valid.")

def cmd_ingest(args):
    logger.info("Executing full Company Brain ingestion pipeline...")
    discovery = DiscoveryEngine()
    modules = discovery.discover_modules()

    parser = MarkdownParser()
    chunker = SemanticChunker()
    merger = MetadataMerger()
    storage = FilesystemStorageProvider()

    all_docs = []
    all_chunks = []

    for mod in modules:
        for file_info in mod["files"]:
            file_path = file_info["file_path"]
            if not os.path.exists(file_path):
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            frontmatter, sections, title = parser.parse(content)
            merged_meta = merger.merge(file_path, frontmatter)

            doc_id = merged_meta.get("id") or os.path.splitext(file_info["file_name"])[0]
            doc_id = doc_id.replace(".", "_")

            doc = DocumentModel(
                id=doc_id,
                title=title,
                file_path=file_path,
                content_type=file_info["extension"],
                priority=mod["priority"],
                embedding_enabled=mod["embedding_enabled"],
                raw_content=content,
                frontmatter=frontmatter,
                merged_metadata=merged_meta,
                sections=sections
            )
            all_docs.append(doc)
            storage.save_document(doc)

            chunks = chunker.chunk_document(doc)
            all_chunks.extend(chunks)
            storage.save_chunks(chunks)

    stats = StatsAggregator.calculate(all_docs, all_chunks)
    logger.info("Ingestion completed successfully.")
    print("\n=== INGESTION SUMMARY ===")
    print(json.dumps(stats, indent=2))

def cmd_parse(args):
    if not args.file:
        print("Please specify a file path using --file")
        sys.exit(1)
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()
    parser = MarkdownParser()
    frontmatter, sections, title = parser.parse(content)
    print(f"\nTitle: {title}")
    print(f"Frontmatter: {json.dumps(frontmatter, indent=2)}")
    print(f"Parsed {len(sections)} sections:")
    for s in sections:
        print(f"  - [{s.level}] {s.title} ({len(s.paragraphs)} paragraphs, {len(s.lists)} lists)")

def cmd_chunk(args):
    cmd_ingest(args)

def cmd_stats(args):
    storage = FilesystemStorageProvider()
    docs = []
    chunks = []
    if os.path.exists(storage.docs_dir):
        for f in os.listdir(storage.docs_dir):
            if f.endswith(".json"):
                doc_id = f.replace(".json", "")
                d = storage.get_document(doc_id)
                if d:
                    docs.append(d)
                    c_list = storage.get_chunks_for_document(doc_id)
                    chunks.extend(c_list)
    stats = StatsAggregator.calculate(docs, chunks)
    print("\n=== COMPANY BRAIN INGESTION STATS ===")
    print(json.dumps(stats, indent=2))

def cmd_inspect(args):
    if not args.id:
        print("Please specify document ID using --id")
        sys.exit(1)
    storage = FilesystemStorageProvider()
    doc = storage.get_document(args.id)
    if not doc:
        print(f"Document '{args.id}' not found in storage.")
        sys.exit(1)
    print(f"\n=== INSPECTING DOCUMENT: {doc.id} ===")
    print(f"Title       : {doc.title}")
    print(f"File Path   : {doc.file_path}")
    print(f"Priority    : {doc.priority}")
    print(f"Merged Meta : {json.dumps(doc.merged_metadata, indent=2)}")

def cmd_rebuild(args):
    storage = FilesystemStorageProvider()
    storage.clear_all()
    cmd_ingest(args)

def cmd_clear(args):
    storage = FilesystemStorageProvider()
    storage.clear_all()
    print("All Company Brain storage cleared successfully.")

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Company Brain CLI")
    subparsers = parser.add_subparsers(dest="command", help="Brain loader commands")

    subparsers.add_parser("validate", help="Validate manifest, schemas, and files")
    subparsers.add_parser("ingest", help="Run full ingestion pipeline")

    p_parse = subparsers.add_parser("parse", help="Parse Markdown document sections")
    p_parse.add_argument("--file", help="Path to markdown file")

    subparsers.add_parser("chunk", help="Chunk all discovered documents")
    subparsers.add_parser("stats", help="Display ingestion statistics")

    p_inspect = subparsers.add_parser("inspect", help="Inspect document model by ID")
    p_inspect.add_argument("--id", help="Document ID")

    subparsers.add_parser("rebuild", help="Rebuild ingestion pipeline from scratch")
    subparsers.add_parser("clear", help="Clear ingestion storage")

    args = parser.parse_args()

    if args.command == "validate":
        cmd_validate(args)
    elif args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "parse":
        cmd_parse(args)
    elif args.command == "chunk":
        cmd_chunk(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "inspect":
        cmd_inspect(args)
    elif args.command == "rebuild":
        cmd_rebuild(args)
    elif args.command == "clear":
        cmd_clear(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
