"""
Production Google AI Studio Image Generation Provider (google-genai SDK v2.x).
Uses official client.models.generate_content() API with multimodal image models (default: gemini-2.5-flash-image).
Single authoritative configuration: GOOGLE_IMAGEN_MODEL.
Parses real image bytes directly returned in response inline_data.
Zero fake/placeholder/gradient/SVG assets. Structured error classification.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import os
import sys
import time
import base64
import logging

logger = logging.getLogger("ImagenProvider")
logging.basicConfig(level=logging.INFO)

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class ImagenAPIError(Exception):
    def __init__(
        self,
        error_code: str,
        reason: str,
        http_status: int = 400,
        model: str = "gemini-2.5-flash-image",
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
            "provider": "gemini_image",
            "configured_model": self.telemetry.get("configured_model", self.model),
            "runtime_model": self.model,
            "backend": self.telemetry.get("backend", "AI Studio"),
            "sdk_version": self.telemetry.get("sdk_version", "v2.x"),
            "python_version": self.telemetry.get("python_version", sys.version.split()[0]),
            "api_version": self.telemetry.get("api_version", "v1beta"),
        }

@dataclass
class ImageProviderResponse:
    success: bool
    image_url_or_path: str
    provider: str
    width: int
    height: int
    mime_type: str = "image/png"
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseImageGenProvider(ABC):
    provider_name: str = "base_image"
    enabled: bool = True

    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def generate_image(self, prompt: str, width: int = 1024, height: int = 1024) -> ImageProviderResponse: pass

    @abstractmethod
    def generate_variations(self, prompt: str, count: int = 3) -> List[ImageProviderResponse]: pass

    @abstractmethod
    def health(self) -> Dict[str, Any]: pass

    @abstractmethod
    def shutdown(self): pass

class GeminiImageProvider(BaseImageGenProvider):
    provider_name = "gemini_image"
    enabled = True

    def __init__(self):
        self._initialized = False
        self._client = None
        self._backend_type = "AI Studio"
        self._sdk_version = "v2.x"
        self.storage_dir = os.environ.get("WORKSPACE_STORAGE", "storage/campaigns/assets")
        self.initialize()

    @property
    def model_name(self) -> str:
        """Single source of truth for image model configuration (default: gemini-2.5-flash-image)."""
        return (
            os.environ.get("GOOGLE_IMAGEN_MODEL")
            or os.environ.get("GEMINI_IMAGE_MODEL")
            or "gemini-2.5-flash-image"
        ).strip()

    @property
    def fallback_models(self) -> List[str]:
        """Explicit fallbacks configured via environment variable only."""
        raw = os.environ.get("GOOGLE_IMAGEN_FALLBACK", "").strip()
        if not raw:
            return []
        return [m.strip() for m in raw.split(",") if m.strip() and m.strip() != self.model_name]

    def initialize(self):
        os.makedirs(self.storage_dir, exist_ok=True)

        try:
            import google.genai
            self._sdk_version = getattr(google.genai, "__version__", "google-genai v2.x")
        except Exception:
            self._sdk_version = "google-genai v2.x"

        api_key = (
            os.environ.get("GOOGLE_IMAGEN_API_KEY")
            or os.environ.get("GEMINI_API_KEY")
        )
        if api_key and api_key.strip():
            try:
                from google import genai
                self._client = genai.Client(api_key=api_key.strip())

                # Detect backend type (AI Studio vs Vertex AI)
                api_client = getattr(self._client, "_api_client", None)
                if api_client and getattr(api_client, "vertexai", False):
                    self._backend_type = "Vertex AI"
                else:
                    self._backend_type = "AI Studio"
            except Exception as e:
                logger.error(f"[Imagen Init Failed] google.genai Client initialization error: {str(e)}")
                self._client = None
        self._initialized = True

    def _discover_models_diagnostic(self) -> List[str]:
        """Diagnostic model discovery via client.models.list(). Does not alter production execution."""
        if not self._client:
            return []
        try:
            available = []
            for m in self._client.models.list():
                m_name = getattr(m, "name", str(m))
                if "imagen" in m_name.lower() or "image" in m_name.lower():
                    available.append(m_name)
            logger.info(f"[Imagen Diagnostic Discovery] Found {len(available)} image-capable models: {available}")
            return available
        except Exception as e:
            logger.warning(f"[Imagen Diagnostic Discovery] Model listing failed: {str(e)}")
            return []

    def _extract_image_bytes(self, response: Any) -> Tuple[Optional[bytes], str]:
        """Extracts raw image bytes and mime_type from google-genai generate_content response."""
        if not response or not hasattr(response, "candidates") or not response.candidates:
            return None, "image/png"

        for candidate in response.candidates:
            content = getattr(candidate, "content", None)
            if not content:
                continue
            parts = getattr(content, "parts", []) or []
            for part in parts:
                inline_data = getattr(part, "inline_data", None)
                if inline_data:
                    data = getattr(inline_data, "data", None)
                    mime = getattr(inline_data, "mime_type", "image/png") or "image/png"
                    if isinstance(data, str):
                        try:
                            data = base64.b64decode(data)
                        except Exception:
                            pass
                    if isinstance(data, bytes) and len(data) > 0:
                        return data, mime

                for attr in ["image_bytes", "data", "_image_bytes", "bytes"]:
                    raw_b = getattr(part, attr, None)
                    if isinstance(raw_b, bytes) and len(raw_b) > 0:
                        return raw_b, "image/png"

        return None, "image/png"

    def _classify_error(self, e: Exception, model_name: str, available_models: Optional[List[str]] = None) -> ImagenAPIError:
        err_msg = str(e)
        err_lower = err_msg.lower()

        telemetry = {
            "configured_model": self.model_name,
            "runtime_model": model_name,
            "backend": self._backend_type,
            "sdk_version": self._sdk_version,
            "python_version": sys.version.split()[0],
            "api_version": "v1beta"
        }

        if "401" in err_msg or "unauthenticated" in err_lower or "api key" in err_lower:
            return ImagenAPIError("INVALID_API_KEY", f"Invalid API Key: {err_msg}", http_status=401, model=model_name, telemetry=telemetry)
        elif "vertex" in err_lower or "vertexai" in err_lower:
            return ImagenAPIError("VERTEX_REQUIRED", f"Model '{model_name}' requires Vertex AI backend: {err_msg}", http_status=400, model=model_name, telemetry=telemetry)
        elif "403" in err_msg or "permission_denied" in err_lower or "permission" in err_lower:
            return ImagenAPIError("PERMISSION_DENIED", f"Permission denied for model '{model_name}': {err_msg}", http_status=403, model=model_name, telemetry=telemetry)
        elif "429" in err_msg or "quota" in err_lower or "resource_exhausted" in err_lower:
            return ImagenAPIError("QUOTA_EXHAUSTED", f"API quota exhausted for model '{model_name}': {err_msg}", http_status=429, model=model_name, telemetry=telemetry)
        elif "not supported" in err_lower or "is not supported" in err_lower:
            return ImagenAPIError("API_NOT_SUPPORTED", f"API method or model unsupported for '{model_name}': {err_msg}", http_status=400, model=model_name, telemetry=telemetry)
        elif "404" in err_msg or "not found" in err_lower or "no longer available" in err_lower or (available_models and model_name not in available_models and f"models/{model_name}" not in available_models):
            return ImagenAPIError("MODEL_NOT_AVAILABLE", f"Model '{model_name}' not found or no longer available on project: {err_msg}", http_status=404, model=model_name, telemetry=telemetry)
        elif "connection" in err_lower or "timeout" in err_lower or "socket" in err_lower:
            return ImagenAPIError("NETWORK_ERROR", f"Network failure connecting to Google API: {err_msg}", http_status=503, model=model_name, telemetry=telemetry)
        elif isinstance(e, (AttributeError, TypeError, KeyError, ValueError)):
            return ImagenAPIError("SDK_ERROR", f"SDK contract/type error ({type(e).__name__}): {err_msg}", http_status=400, model=model_name, telemetry=telemetry)
        elif "500" in err_msg or "503" in err_msg or "service" in err_lower:
            return ImagenAPIError("GOOGLE_SERVICE_ERROR", f"Google API service error: {err_msg}", http_status=500, model=model_name, telemetry=telemetry)
        else:
            return ImagenAPIError("GOOGLE_SERVICE_ERROR", f"Google API error ({type(e).__name__}): {err_msg}", http_status=400, model=model_name, telemetry=telemetry)

    def generate_image(self, prompt: str, width: int = 512, height: int = 512) -> ImageProviderResponse:
        start_time = time.time()
        if not self._initialized:
            self.initialize()

        telemetry = {
            "configured_model": self.model_name,
            "runtime_model": self.model_name,
            "backend": self._backend_type,
            "sdk_version": self._sdk_version,
            "python_version": sys.version.split()[0],
            "api_version": "v1beta"
        }

        if not self._client:
            raise ImagenAPIError("INVALID_API_KEY", "GOOGLE_IMAGEN_API_KEY or GEMINI_API_KEY missing/uninitialized in environment (.env)", http_status=401, model=self.model_name, telemetry=telemetry)

        request_id = f"img_{abs(hash(prompt + str(datetime.now().timestamp()))) % 100000:05d}"
        png_filename = f"{request_id}.png"
        png_path = os.path.join(self.storage_dir, png_filename)

        # Diagnostic model discovery (Diagnostic only)
        available_models = self._discover_models_diagnostic()

        # Build execution queue: primary configured model + explicit env fallbacks ONLY
        model_queue = [self.model_name] + [m for m in self.fallback_models if m not in [self.model_name]]

        last_classified_error = None

        for current_model in model_queue:
            # Diagnostics log trace immediately before API call
            logger.info("--- [AI STUDIO IMAGE REQUEST DIAGNOSTICS] ---")
            logger.info(f"Request ID: {request_id}")
            logger.info(f"Prompt: '{prompt}'")
            logger.info(f"Configured model: '{self.model_name}'")
            logger.info(f"Runtime model: '{current_model}'")
            logger.info(f"Explicit Fallbacks: {self.fallback_models}")
            logger.info(f"Backend: {self._backend_type}")
            logger.info(f"SDK version: google-genai {self._sdk_version}")
            logger.info(f"Python version: {sys.version.split()[0]}")
            logger.info(f"API endpoint: https://generativelanguage.googleapis.com")
            logger.info(f"API version: v1beta")
            logger.info(f"Executing client.models.generate_content(model='{current_model}')...")

            try:
                result = self._client.models.generate_content(
                    model=current_model,
                    contents=f"Generate an image: {prompt}"
                )

                logger.info(f"Raw response class: {type(result).__name__}")
                img_bytes, mime_type = self._extract_image_bytes(result)

                # Response Integrity Verification
                if not img_bytes or len(img_bytes) == 0:
                    raise ImagenAPIError("SDK_ERROR", f"Google API returned response without valid image bytes for model '{current_model}'", http_status=500, model=current_model, telemetry=telemetry)

                # Verify valid image binary header (PNG header \x89PNG\r\n\x1a\n or JPEG \xff\xd8\xff)
                if not (img_bytes.startswith(b"\x89PNG\r\n\x1a\n") or img_bytes.startswith(b"\xff\xd8\xff")):
                    raise ImagenAPIError("SDK_ERROR", f"Returned bytes failed PNG/JPEG header validation (corrupted bytes)", http_status=500, model=current_model, telemetry=telemetry)

                duration_ms = int((time.time() - start_time) * 1000)
                logger.info(f"Image MIME type: {mime_type}")
                logger.info(f"Image byte size: {len(img_bytes)} bytes")
                logger.info(f"Generation duration: {duration_ms} ms")

                # Save ONLY verified real image bytes
                with open(png_path, "wb") as f:
                    f.write(img_bytes)

                return ImageProviderResponse(
                    success=True,
                    image_url_or_path=png_path,
                    provider="gemini_image",
                    width=width,
                    height=height,
                    mime_type=mime_type,
                    metadata={
                        "image_id": request_id,
                        "prompt": prompt,
                        "provider": "gemini_image",
                        "configured_model": self.model_name,
                        "runtime_model": current_model,
                        "backend": self._backend_type,
                        "sdk_version": self._sdk_version,
                        "python_version": sys.version.split()[0],
                        "api_version": "v1beta",
                        "mime_type": mime_type,
                        "byte_length": len(img_bytes),
                        "duration_ms": duration_ms,
                        "generation_time": _get_utc_now(),
                        "workspace": os.environ.get("WORKSPACE_ID", "default_workspace")
                    }
                )
            except Exception as e:
                if isinstance(e, ImagenAPIError):
                    classified = e
                else:
                    classified = self._classify_error(e, current_model, available_models)
                logger.error(f"[Image Generation Failed for {current_model}] {classified.error_code}: {classified.reason}")
                last_classified_error = classified

        # Explicitly raise classified error. ZERO fake/placeholder image generation.
        raise last_classified_error

    def generate_variations(self, prompt: str, count: int = 3) -> List[ImageProviderResponse]:
        return [self.generate_image(f"{prompt} (variation {i+1})") for i in range(count)]

    def health(self) -> Dict[str, Any]:
        return {
            "provider": self.provider_name,
            "status": "Healthy" if self._client else "Uninitialized",
            "configured_model": self.model_name,
            "runtime_model": self.model_name,
            "backend": self._backend_type,
            "sdk_version": self._sdk_version,
            "python_version": sys.version.split()[0],
            "api_version": "v1beta"
        }

    def shutdown(self):
        self._initialized = False
        self._client = None

# Skeleton Providers
class OpenAIImageProvider(BaseImageGenProvider):
    provider_name = "openai_image"
    enabled = False
    def initialize(self): pass
    def generate_image(self, prompt: str, width: int = 1024, height: int = 1024) -> ImageProviderResponse: raise RuntimeError("OpenAI Image Provider disabled.")
    def generate_variations(self, prompt: str, count: int = 3) -> List[ImageProviderResponse]: return []
    def health(self) -> Dict[str, Any]: return {"provider": self.provider_name, "status": "Disabled", "enabled": False}
    def shutdown(self): pass

class FluxImageProvider(BaseImageGenProvider):
    provider_name = "flux"
    enabled = False
    def initialize(self): pass
    def generate_image(self, prompt: str, width: int = 1024, height: int = 1024) -> ImageProviderResponse: raise RuntimeError("Flux Provider disabled.")
    def generate_variations(self, prompt: str, count: int = 3) -> List[ImageProviderResponse]: return []
    def health(self) -> Dict[str, Any]: return {"provider": self.provider_name, "status": "Disabled", "enabled": False}
    def shutdown(self): pass
