"""
Production Pollinations AI Image Provider.
Generates real high-quality images via Pollinations AI API.
Supports configurable models (default: flux), custom dimensions, seed generation, and optional Bearer API key authentication.
Zero fake/placeholder/gradient assets. Fully transparent production-grade execution.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import os
import sys
import time
import random
import urllib.request
import urllib.parse
import urllib.error
import logging

logger = logging.getLogger("PollinationsProvider")
logging.basicConfig(level=logging.INFO)

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class PollinationsAPIError(Exception):
    def __init__(
        self,
        error_code: str,
        reason: str,
        http_status: int = 400,
        model: str = "flux",
        telemetry: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        self.reason = reason
        self.http_status = http_status
        self.model = model
        self.telemetry = telemetry or {}
        super().__init__(f"[{error_code}] {reason}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": "ERROR",
            "error_code": self.error_code,
            "reason": self.reason,
            "http_status": self.http_status,
            "provider": "pollinations",
            "configured_model": self.telemetry.get("configured_model", self.model),
            "runtime_model": self.model,
            "backend": "Pollinations AI",
            "sdk_version": "v1.0-http",
            "python_version": sys.version.split()[0],
            "api_version": "v1"
        }

@dataclass
class ImageProviderResponse:
    success: bool
    image_url_or_path: str
    provider: str
    width: int
    height: int
    mime_type: str = "image/jpeg"
    metadata: Dict[str, Any] = field(default_factory=dict)

from image_generation.providers.gemini_image import BaseImageGenProvider

class PollinationsImageProvider(BaseImageGenProvider):
    provider_name = "pollinations"
    enabled = True

    def __init__(self):
        self._initialized = False
        self.storage_dir = os.environ.get("WORKSPACE_STORAGE", "storage/campaigns/assets")
        self.initialize()

    @property
    def model_name(self) -> str:
        """Single source of truth for Pollinations image model (default: flux)."""
        return os.environ.get("POLLINATIONS_MODEL", "flux").strip()

    @property
    def api_key(self) -> Optional[str]:
        """Optional Pollinations API Key from environment."""
        key = os.environ.get("POLLINATIONS_API_KEY", "").strip()
        return key if key else None

    def initialize(self):
        os.makedirs(self.storage_dir, exist_ok=True)
        self._initialized = True

    def _classify_error(self, e: Exception, model_name: str) -> PollinationsAPIError:
        err_msg = str(e)
        err_lower = err_msg.lower()

        telemetry = {
            "configured_model": self.model_name,
            "runtime_model": model_name,
            "backend": "Pollinations AI",
            "sdk_version": "v1.0-http",
            "python_version": sys.version.split()[0],
            "api_version": "v1"
        }

        if isinstance(e, urllib.error.HTTPError):
            code = e.code
            if code in (401, 403):
                return PollinationsAPIError("INVALID_API_KEY", f"Pollinations API Key invalid or unauthorized (HTTP {code}): {e.reason}", http_status=code, model=model_name, telemetry=telemetry)
            elif code == 429:
                return PollinationsAPIError("RATE_LIMITED", f"Pollinations API rate limit reached (HTTP 429): {e.reason}", http_status=429, model=model_name, telemetry=telemetry)
            else:
                return PollinationsAPIError("API_ERROR", f"Pollinations API HTTP Error {code}: {e.reason}", http_status=code, model=model_name, telemetry=telemetry)
        elif "connection" in err_lower or "timeout" in err_lower or "socket" in err_lower:
            return PollinationsAPIError("NETWORK_ERROR", f"Network connection failed to Pollinations API: {err_msg}", http_status=503, model=model_name, telemetry=telemetry)
        else:
            return PollinationsAPIError("API_ERROR", f"Pollinations generation error ({type(e).__name__}): {err_msg}", http_status=400, model=model_name, telemetry=telemetry)

    def generate_image(self, prompt: str, width: int = 512, height: int = 512) -> ImageProviderResponse:
        start_time = time.time()
        if not self._initialized:
            self.initialize()

        request_id = f"img_pol_{abs(hash(prompt + str(datetime.now().timestamp()))) % 100000:05d}"
        seed = random.randint(1000, 999999)

        # Build Pollinations image endpoint URL
        encoded_prompt = urllib.parse.quote(prompt)
        endpoint = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model={self.model_name}&width={width}&height={height}&seed={seed}&nologo=true"

        # Diagnostic logging (never logging API key)
        logger.info("--- [POLLINATIONS AI REQUEST DIAGNOSTICS] ---")
        logger.info(f"Request ID: {request_id}")
        logger.info(f"Prompt: '{prompt}'")
        logger.info(f"Configured model: '{self.model_name}'")
        logger.info(f"Dimensions: {width}x{height}")
        logger.info(f"Seed: {seed}")
        logger.info(f"Has API Key: {bool(self.api_key)}")
        logger.info(f"Executing HTTP GET to Pollinations AI...")

        headers = {
            "User-Agent": "AVENIQ-AI/1.0",
            "Accept": "image/jpeg, image/png, image/*"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = urllib.request.Request(endpoint, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                http_status = resp.status
                content_type = resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
                img_bytes = resp.read()

                # Extension & MIME detection
                ext = ".png" if "png" in content_type else ".jpg"
                mime_type = "image/png" if "png" in content_type else "image/jpeg"
                saved_filename = f"{request_id}{ext}"
                saved_path = os.path.join(self.storage_dir, saved_filename)

                # Integrity Verification (valid binary signature)
                if not img_bytes or len(img_bytes) == 0:
                    telemetry = {"configured_model": self.model_name, "runtime_model": self.model_name, "backend": "Pollinations AI"}
                    raise PollinationsAPIError("INVALID_RESPONSE", "Pollinations API returned empty 0-byte image payload", http_status=500, model=self.model_name, telemetry=telemetry)

                if not (img_bytes.startswith(b"\x89PNG\r\n\x1a\n") or img_bytes.startswith(b"\xff\xd8\xff")):
                    telemetry = {"configured_model": self.model_name, "runtime_model": self.model_name, "backend": "Pollinations AI"}
                    raise PollinationsAPIError("INVALID_RESPONSE", "Returned payload failed binary image signature validation (corrupted bytes)", http_status=500, model=self.model_name, telemetry=telemetry)

                duration_ms = int((time.time() - start_time) * 1000)
                logger.info(f"Image MIME type: {mime_type}")
                logger.info(f"Image byte size: {len(img_bytes)} bytes")
                logger.info(f"Generation duration: {duration_ms} ms")

                with open(saved_path, "wb") as f:
                    f.write(img_bytes)

                return ImageProviderResponse(
                    success=True,
                    image_url_or_path=saved_path,
                    provider="pollinations",
                    width=width,
                    height=height,
                    mime_type=mime_type,
                    metadata={
                        "image_id": request_id,
                        "prompt": prompt,
                        "provider": "pollinations",
                        "configured_model": self.model_name,
                        "runtime_model": self.model_name,
                        "backend": "Pollinations AI",
                        "sdk_version": "v1.0-http",
                        "python_version": sys.version.split()[0],
                        "api_version": "v1",
                        "mime_type": mime_type,
                        "byte_length": len(img_bytes),
                        "duration_ms": duration_ms,
                        "generation_time": _get_utc_now(),
                        "workspace": os.environ.get("WORKSPACE_ID", "default_workspace")
                    }
                )
        except Exception as e:
            if isinstance(e, PollinationsAPIError):
                classified = e
            else:
                classified = self._classify_error(e, self.model_name)
            logger.error(f"[Pollinations Generation Failed] {classified.error_code}: {classified.reason}")
            raise classified

    def generate_variations(self, prompt: str, count: int = 3) -> List[ImageProviderResponse]:
        return [self.generate_image(f"{prompt} (variation {i+1})") for i in range(count)]

    def health(self) -> Dict[str, Any]:
        return {
            "provider": self.provider_name,
            "status": "Healthy",
            "configured_model": self.model_name,
            "runtime_model": self.model_name,
            "backend": "Pollinations AI",
            "sdk_version": "v1.0-http",
            "python_version": sys.version.split()[0],
            "api_version": "v1"
        }

    def shutdown(self):
        self._initialized = False
