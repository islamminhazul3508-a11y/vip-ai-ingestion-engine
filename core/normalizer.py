import json
import hashlib
from typing import Dict, Any, List


class AIVectorNormalizer:
    """
    Layer 4: AI Vector & Schema Normalizer.
    Transforms raw structured JSON payloads into AI-ready schema documents
    with deterministic hash IDs and semantic embedding payloads.
    """

    def __init__(self, source_name: str = "VIP_Ingestion_Engine"):
        self.source_name = source_name

    def generate_document_id(self, content: str) -> str:
        """Creates a unique SHA-256 fingerprint for data deduplication."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    def to_ai_document(self, raw_record: Dict[str, Any], text_fields: List[str]) -> Dict[str, Any]:
        """Converts raw record into an LLM/RAG vector payload with metadata."""
        combined_text = " ".join([str(raw_record.get(k, "")) for k in text_fields if k in raw_record]).strip()
        doc_id = self.generate_document_id(combined_text)

        return {
            "id": doc_id,
            "page_content": combined_text,
            "metadata": {
                "source": self.source_name,
                "original_id": raw_record.get("id"),
                "field_count": len(raw_record),
                "is_sanitized": True
            }
        }
