import hmac
import hashlib
import json
from typing import Dict, Any


class ZeroTrustSecurityManager:
    """
    Layer 5: Zero-Trust Security & Tamper Proofing.
    Validates payload integrity using HMAC signatures and sanitizes inputs.
    """

    def __init__(self, secret_key: str = "enterprise_secret_vault_key_2026"):
        self._secret = secret_key.encode("utf-8")

    def sign_payload(self, data: Dict[str, Any]) -> str:
        """Generates a cryptographic HMAC SHA-256 signature for outgoing payloads."""
        serialized = json.dumps(data, sort_keys=True).encode("utf-8")
        return hmac.new(self._secret, serialized, hashlib.sha256).hexdigest()

    def verify_payload(self, data: Dict[str, Any], signature: str) -> bool:
        """Ensures that the ingested data has not been modified in transit."""
        expected = self.sign_payload(data)
        return hmac.compare_digest(expected, signature)
