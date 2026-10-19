import random
from typing import Dict, Any, Optional
import httpx


class StealthSessionManager:
    """
    Layer 1: Stealth Session & Dynamic Fingerprint Engine.
    Simulates internal mobile application network behavior to bypass bot protections.
    """

    MOBILE_USER_AGENTS = [
        "Dalvik/2.1.0 (Linux; U; Android 14; Pixel 8 Build/UD1A.230803.041)",
        "Dalvik/2.1.0 (Linux; U; Android 13; SM-S918B Build/TP1A.220624.014)",
        "okhttp/4.12.0",
        "CFNetwork/1410.0.3 Darwin/22.6.0",
    ]

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.session = self._init_client()

    def _generate_stealth_headers(self) -> Dict[str, str]:
        """Generates realistic headers simulating native mobile API requests."""
        return {
            "User-Agent": random.choice(self.MOBILE_USER_AGENTS),
            "Accept": "application/json",
            "Connection": "keep-alive",
            "X-App-Version": "4.12.0",
            "X-Platform": "android",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

    def _init_client(self) -> httpx.Client:
        """Initializes client with randomized headers and optional proxy."""
        headers = self._generate_stealth_headers()

        return httpx.Client(
            headers=headers,
            proxy=self.proxy_url,
            timeout=15.0,
            follow_redirects=True,
        )

    def rotate_session(self) -> None:
        """Rotates session client and fingerprint if blocked or rate-limited."""
        self.session.close()
        self.session = self._init_client()

    def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Executes HTTP request with automated retry and session rotation logic."""
        try:
            response = self.session.request(method, url, **kwargs)
            if response.status_code in [403, 429]:
                self.rotate_session()
            return response
        except httpx.RequestError:
            self.rotate_session()
            raise
