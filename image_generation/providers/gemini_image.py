"""
Production Google Imagen 3 Image Generation Provider (google-genai SDK v2.x).
Extracts and validates real image bytes directly returned by Google GenAI SDK.
Includes structured error classification (INVALID_API_KEY, MODEL_NOT_FOUND, QUOTA_EXHAUSTED, etc.).
Zero fake/placeholder/gradient assets. Fully transparent production-grade execution.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
import os
import sys
import time
import logging

logger = logging.getLogger("ImagenProvider")
logging.basicConfig(level=logging.INFO)

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class ImagenAPIError(Exception):
    def __init__(self, error_code: str, reason: str, http_status: int = 400, model: str = "imagen-3.0-generate-002"):
        self.error_code = error_code
        self.reason = reason
        self.http_status = http_status
        self.model = model
        super().__init__(f"[{error_code}] {reason}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": "ERROR",
            "error_code": self.error_code,
            "reason": self.reason,
            "http_status": self.http_status,
            "provider": "gemini_image",
            "model": self.model
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
        self.model_name = (
            os.environ.get("GOOGLE_IMAGEN_MODEL")
            or os.environ.get("GEMINI_IMAGE_MODEL")
            or "imagen-3.0-generate-002"
        ).strip()
        self.storage_dir = os.environ.get("WORKSPACE_STORAGE", "storage/campaigns/assets")
        self.initialize()

    def initialize(self):
        os.makedirs(self.storage_dir, exist_ok=True)
        api_key = (
            os.environ.get("GOOGLE_IMAGEN_API_KEY")
            or os.environ.get("GEMINI_API_KEY")
        )
        if api_key and api_key.strip():
            try:
                from google import genai
                self._client = genai.Client(api_key=api_key.strip())
            except Exception as e:
                logger.error(f"[Imagen Init Failed] google.genai Client initialization error: {str(e)}")
                self._client = None
        self._initialized = True

    def _classify_error(self, e: Exception, model_name: str) -> ImagenAPIError:
        err_msg = str(e)
        err_lower = err_msg.lower()

        if "401" in err_msg or "unauthenticated" in err_lower or "api key" in err_lower:
            return ImagenAPIError("INVALID_API_KEY", f"Invalid API Key: {err_msg}", http_status=401, model=model_name)
        elif "404" in err_msg or "not found" in err_lower or "not supported" in err_lower:
            return ImagenAPIError("MODEL_NOT_FOUND", f"Model '{model_name}' not found or not enabled on project: {err_msg}", http_status=404, model=model_name)
        elif "429" in err_msg or "quota" in err_lower or "resource_exhausted" in err_lower:
            return ImagenAPIError("QUOTA_EXHAUSTED", f"API quota exhausted for model '{model_name}': {err_msg}", http_status=429, model=model_name)
        elif "connection" in err_lower or "timeout" in err_lower or "socket" in err_lower:
            return ImagenAPIError("NETWORK_ERROR", f"Network failure connecting to Google API: {err_msg}", http_status=503, model=model_name)
        elif "500" in err_msg or "503" in err_msg or "service" in err_lower:
            return ImagenAPIError("GOOGLE_SERVICE_ERROR", f"Google API service error: {err_msg}", http_status=500, model=model_name)
        else:
            return ImagenAPIError("GOOGLE_SERVICE_ERROR", f"Google API error ({type(e).__name__}): {err_msg}", http_status=400, model=model_name)

    def generate_image(self, prompt: str, width: int = 512, height: int = 512) -> ImageProviderResponse:
        start_time = time.time()
        if not self._initialized:
            self.initialize()

        if not self._client:
            raise ImagenAPIError("INVALID_API_KEY", "GOOGLE_IMAGEN_API_KEY or GEMINI_API_KEY missing/uninitialized in environment (.env)", http_status=401, model=self.model_name)

        image_id = f"img_{abs(hash(prompt + str(datetime.now().timestamp()))) % 100000:05d}"
        png_filename = f"{image_id}.png"
        png_path = os.path.join(self.storage_dir, png_filename)

        # Structured Runtime Diagnostics (Phase 3)
        try:
            import google.genai
            sdk_ver = getattr(google.genai, "__version__", "v2.x")
        except Exception:
            sdk_ver = "v2.x"

        logger.info(f"--- [IMAGEN REQUEST DIAGNOSTICS] ---")
        logger.info(f"Prompt: '{prompt}'")
        logger.info(f"Configured model: '{self.model_name}'")
        logger.info(f"SDK version: google-genai {sdk_ver}")
        logger.info(f"Python version: {sys.version.split()[0]}")

        model_candidates = [self.model_name]
        for fallback_m in ["imagen-3.0-generate-002", "imagen-3.0-fast-generate-001", "imagen-3.0-generate-001"]:
            if fallback_m not in model_candidates:
                model_candidates.append(fallback_m)

        last_classified_error = None
        for current_model in model_candidates:
            try:
                logger.info(f"Executing client.models.generate_images(model='{current_model}')...")
                result = self._client.models.generate_images(
                    model=current_model,
                    prompt=prompt,
                    config=dict(number_of_images=1, aspect_ratio="1:1" if width == height else "16:9")
                )

                logger.info(f"Raw response class: {type(result).__name__}")
                if hasattr(result, '__dict__'):
                    logger.info(f"Response fields: {list(result.__dict__.keys())}")

                if not result or not hasattr(result, 'generated_images') or not result.generated_images:
                    raise ImagenAPIError("INVALID_RESPONSE", f"Google API returned empty response without generated_images for model '{current_model}'", http_status=500, model=current_model)

                gen_count = len(result.generated_images)
                logger.info(f"Generated image count: {gen_count}")

                first_image = result.generated_images[0]
                img_bytes = getattr(first_image.image, 'image_bytes', None)
                if not img_bytes and hasattr(first_image, 'image') and hasattr(first_image.image, '_image_bytes'):
                    img_bytes = first_image.image._image_bytes

                # Response Integrity Verification (Phase 7)
                if not img_bytes or len(img_bytes) == 0:
                    raise ImagenAPIError("IMAGE_EXTRACTION_FAILED", f"Extracted image bytes are empty (0 bytes) for model '{current_model}'", http_status=500, model=current_model)

                # Verify valid image binary header (PNG header \x89PNG\r\n\x1a\n or JPEG \xff\xd8\xff)
                if not (img_bytes.startswith(b"\x89PNG\r\n\x1a\n") or img_bytes.startswith(b"\xff\xd8\xff")):
                    raise ImagenAPIError("IMAGE_EXTRACTION_FAILED", f"Returned bytes failed PNG/JPEG header validation (corrupted bytes)", http_status=500, model=current_model)

                duration_ms = int((time.time() - start_time) * 1000)
                logger.info(f"Image MIME type: image/png")
                logger.info(f"Image byte length: {len(img_bytes)} bytes")
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
                    mime_type="image/png",
                    metadata={
                        "image_id": image_id,
                        "prompt": prompt,
                        "provider": "gemini_image",
                        "model": current_model,
                        "mime_type": "image/png",
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
                    classified = self._classify_error(e, current_model)
                logger.error(f"[Imagen Generation Failed for {current_model}] {classified.error_code}: {classified.reason}")
                last_classified_error = classified

        # Explicitly raise classified error. ZERO fallback / fake image generation.
        raise last_classified_error

    def generate_variations(self, prompt: str, count: int = 3) -> List[ImageProviderResponse]:
        return [self.generate_image(f"{prompt} (variation {i+1})") for i in range(count)]

    def health(self) -> Dict[str, Any]:
        return {"provider": self.provider_name, "status": "Healthy" if self._client else "Uninitialized", "model": self.model_name}

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
