"""
Section-Aware Text Splitter and Chunk Relationship Graph Generator.
"""

from typing import List, Dict, Any
from knowledge.documents.document import KnowledgeDocument, DocumentChunk

class SemanticTextSplitter:
    @staticmethod
    def split_document(document: KnowledgeDocument, max_chunk_words: int = 150) -> List[DocumentChunk]:
        # Pre-process content to insert double newlines before markdown headings
        raw_text = document.content
        lines = raw_text.split("\n")
        blocks = []
        curr_block = []

        for line in lines:
            if line.strip().startswith("#") and curr_block:
                blocks.append("\n".join(curr_block))
                curr_block = [line]
            else:
                curr_block.append(line)
        if curr_block:
            blocks.append("\n".join(curr_block))

        chunks: List[DocumentChunk] = []
        current_heading = [document.title]
        prev_chunk_id = None

        for i, block in enumerate(blocks):
            block_str = block.strip()
            if not block_str:
                continue

            b_lines = block_str.split("\n")
            if b_lines[0].startswith("#"):
                current_heading = [document.title, b_lines[0].lstrip("#").strip()]
                body_text = "\n".join(b_lines[1:]).strip()
            else:
                body_text = block_str

            if not body_text:
                continue

            chunk_id = f"chk_{document.id}_{len(chunks)+1:03d}"
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                parent_document_id=document.id,
                content=body_text,
                heading_hierarchy=list(current_heading),
                previous_chunk_id=prev_chunk_id,
                next_chunk_id=None,
                token_count=len(body_text.split()),
                metadata={
                    "workspace_id": document.workspace_id,
                    "collection": document.collection,
                    "source_type": document.source_type
                }
            )

            if chunks:
                chunks[-1].next_chunk_id = chunk_id

            chunks.append(chunk)
            prev_chunk_id = chunk_id

        document.chunks = chunks
        return chunks
