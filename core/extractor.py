from typing import Dict, Any, List, Optional
from core.stealth_session import StealthSessionManager


class PrivateAPIExtractor:
    """
    Layer 2: Extraction Core & Private API Engine.
    Interacts directly with mobile/private JSON endpoints, bypassing frontend HTML DOM.
    """

    def __init__(self, session_manager: Optional[StealthSessionManager] = None):
        self.session = session_manager or StealthSessionManager()

    def fetch_endpoint(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Fetches structured JSON payload directly from private backend endpoints."""
        response = self.session.request("GET", url, params=params)
        
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as exc:
                raise ValueError(f"Failed to parse JSON response: {exc}")
        else:
            raise RuntimeError(f"Endpoint request failed with status: {response.status_code}")

    def sanitize_schema(self, raw_data: Dict[str, Any], target_fields: List[str]) -> Dict[str, Any]:
        """Strips out redundant metadata and extracts clean, AI-ready target fields."""
        sanitized = {}
        for field in target_fields:
            sanitized[field] = raw_data.get(field, None)
        return sanitized
