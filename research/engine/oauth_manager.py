"""
Generic Reusable OAuth Token Manager for AVENIQ Research Engine.
Handles OAuth2 token acquisition, in-memory caching, expiry tracking, and automatic token refresh.
Supported by Reddit, GitHub, Product Hunt, Google, etc.
"""

import time
import base64
import json
import ssl
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional, Tuple


class OAuthTokenManager:
    """Generic in-memory OAuth Token Manager with token caching and automatic refresh."""
    def __init__(self, provider: str):
        self.provider = provider
        self.access_token: Optional[str] = None
        self.token_type: str = "bearer"
        self.expires_at: float = 0.0
        self.grant_type: str = "client_credentials"
        self.fetch_count: int = 0
        self.last_error: Optional[str] = None

    def is_valid(self, buffer_seconds: int = 60) -> bool:
        """Returns True if access token is present and not expired (with safety buffer)."""
        if not self.access_token:
            return False
        return time.time() < (self.expires_at - buffer_seconds)

    def fetch_reddit_token(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        force_refresh: bool = False
    ) -> Tuple[Optional[str], Dict[str, Any]]:
        """Fetch or return cached Reddit OAuth token using client_credentials or password grant."""
        if not force_refresh and self.is_valid():
            return self.access_token, {
                "status": "Cached",
                "grant_type": self.grant_type,
                "expires_in_seconds": round(max(0.0, self.expires_at - time.time()), 1),
                "fetch_count": self.fetch_count,
                "reused": True
            }

        if not client_id or not client_secret:
            self.last_error = "Missing REDDIT_CLIENT_ID or REDDIT_CLIENT_SECRET"
            return None, {"status": "Missing Configuration", "error": self.last_error}

        auth_str = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
        headers = {
            "Authorization": f"Basic {auth_str}",
            "User-Agent": user_agent or "AVENIQ Research Engine/1.0"
        }

        # Determine grant type
        if username and password:
            self.grant_type = "password"
            body = {"grant_type": "password", "username": username, "password": password}
        else:
            self.grant_type = "client_credentials"
            body = {"grant_type": "client_credentials"}

        data = urllib.parse.urlencode(body).encode('utf-8')
        req = urllib.request.Request("https://www.reddit.com/api/v1/access_token", data=data, headers=headers)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        start = time.time()
        try:
            with urllib.request.urlopen(req, timeout=10, context=context) as resp:
                raw = resp.read().decode('utf-8', errors='ignore')
                res = json.loads(raw)
                token = res.get("access_token")
                expires_in = res.get("expires_in", 3600)
                
                if token:
                    self.access_token = token
                    self.token_type = res.get("token_type", "bearer")
                    self.expires_at = time.time() + float(expires_in)
                    self.fetch_count += 1
                    self.last_error = None
                    return token, {
                        "status": "Token Acquired",
                        "grant_type": self.grant_type,
                        "expires_in_seconds": float(expires_in),
                        "fetch_count": self.fetch_count,
                        "reused": False,
                        "latency_ms": round((time.time() - start) * 1000, 2)
                    }
                else:
                    err_msg = res.get("error", "Invalid OAuth response")
                    self.last_error = err_msg
                    return None, {"status": "OAuth Failed", "error": err_msg}

        except urllib.error.HTTPError as e:
            err_msg = f"HTTP {e.code}: {e.reason}"
            self.last_error = err_msg
            return None, {"status": "Authentication Failed", "error": err_msg, "http_code": e.code}
        except Exception as e:
            err_msg = str(e)
            self.last_error = err_msg
            return None, {"status": "Network Error", "error": err_msg}


# Global instances per provider
reddit_oauth_manager = OAuthTokenManager("reddit")
