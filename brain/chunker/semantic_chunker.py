"""
Heading-Based Semantic Chunker for AVENIQ Brain Loader.
Splits documents at logical heading boundaries, targets 800-1200 tokens,
preserves heading context hierarchy, and extracts key keywords.
"""

import re
from typing import List, Dict, Any
from brain.models.schema import DocumentModel, ChunkModel, SectionNode

class SemanticChunker:
    def __init__(self, target_chunk_tokens: int = 1000, max_chunk_tokens: int = 1400):
        self.target_chunk_tokens = target_chunk_tokens
        self.max_chunk_tokens = max_chunk_tokens

    def estimate_tokens(self, text: str) -> int:
        # Standard rough token estimation: ~4 characters per token or ~0.75 words per token
        words = text.split()
        return int(len(words) * 1.3)

    def extract_keywords(self, text: str, top_n: int = 8) -> List[str]:
        # Simple frequency-based keyword extraction removing common stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with",
            "by", "about", "against", "between", "into", "through", "during", "before",
            "after", "above", "below", "from", "up", "down", "in", "out", "on", "off",
            "over", "under", "again", "further", "then", "once", "here", "there", "when",
            "where", "why", "how", "all", "any", "both", "each", "few", "more", "most",
            "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
            "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do",
            "does", "did", "this", "that", "these", "those", "we", "our", "you", "your"
        }
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        filtered = [w for w in words if w not in stop_words]
        counts = {}
        for w in filtered:
            counts[w] = counts.get(w, 0) + 1
        sorted_kw = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return [kw for kw, _ in sorted_kw[:top_n]]

    def chunk_document(self, doc: DocumentModel) -> List[ChunkModel]:
        chunks: List[ChunkModel] = []
        chunk_counter = 1

        for sec in doc.sections:
            sec_text = f"## {sec.title}\n\n{sec.content}".strip()
            tokens = self.estimate_tokens(sec_text)

            # If section text fits within max_chunk_tokens, keep as a single intact chunk
            if tokens <= self.max_chunk_tokens:
                chunk_id = f"{doc.id}_chunk_{chunk_counter:03d}"
                chunks.append(ChunkModel(
                    id=chunk_id,
                    document_id=doc.id,
                    document_title=doc.title,
                    section_title=sec.title,
                    heading_hierarchy=[doc.title, sec.title],
                    text=sec_text,
                    token_estimate=tokens,
                    keywords=self.extract_keywords(sec_text),
                    metadata={
                        "file_path": doc.file_path,
                        "priority": doc.priority,
                        "content_type": doc.content_type,
                        "merged_metadata": doc.merged_metadata
                    }
                ))
                chunk_counter += 1
            else:
                # Sub-chunk longer sections gracefully across paragraphs
                paragraphs = sec.content.split("\n\n")
                current_p_buffer = []
                current_tokens = 0

                for p in paragraphs:
                    p_tokens = self.estimate_tokens(p)
                    if current_tokens + p_tokens > self.target_chunk_tokens and current_p_buffer:
                        sub_text = f"## {sec.title} (Part)\n\n" + "\n\n".join(current_p_buffer)
                        chunk_id = f"{doc.id}_chunk_{chunk_counter:03d}"
                        chunks.append(ChunkModel(
                            id=chunk_id,
                            document_id=doc.id,
                            document_title=doc.title,
                            section_title=sec.title,
                            heading_hierarchy=[doc.title, sec.title],
                            text=sub_text.strip(),
                            token_estimate=self.estimate_tokens(sub_text),
                            keywords=self.extract_keywords(sub_text),
                            metadata={
                                "file_path": doc.file_path,
                                "priority": doc.priority,
                                "content_type": doc.content_type,
                                "merged_metadata": doc.merged_metadata
                            }
                        ))
                        chunk_counter += 1
                        current_p_buffer = [p]
                        current_tokens = p_tokens
                    else:
                        current_p_buffer.append(p)
                        current_tokens += p_tokens

                if current_p_buffer:
                    sub_text = f"## {sec.title}\n\n" + "\n\n".join(current_p_buffer)
                    chunk_id = f"{doc.id}_chunk_{chunk_counter:03d}"
                    chunks.append(ChunkModel(
                        id=chunk_id,
                        document_id=doc.id,
                        document_title=doc.title,
                        section_title=sec.title,
                        heading_hierarchy=[doc.title, sec.title],
                        text=sub_text.strip(),
                        token_estimate=self.estimate_tokens(sub_text),
                        keywords=self.extract_keywords(sub_text),
                        metadata={
                            "file_path": doc.file_path,
                            "priority": doc.priority,
                            "content_type": doc.content_type,
                            "merged_metadata": doc.merged_metadata
                        }
                    ))
                    chunk_counter += 1

        return chunks
