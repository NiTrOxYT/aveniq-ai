"""
pytest conftest.py — project-wide test fixtures and environment setup.

Responsibilities:
1. Remove scripts/ from sys.path to prevent local scripts (calendar.py, etc.)
   from shadowing Python stdlib modules (fixes ImportError in google-genai).
2. Auto-load .env so GEMINI_API_KEY and other credentials are available
   in unit tests without requiring shell-level `source .env`.
"""

import os
import sys

# ── Fix sys.path: remove scripts/ so it doesn't shadow stdlib ────────────────
_scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
_scripts_dir = os.path.abspath(_scripts_dir)
if _scripts_dir in sys.path:
    sys.path.remove(_scripts_dir)

# ── Load .env into os.environ ─────────────────────────────────────────────────
_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
_env_path = os.path.abspath(_env_path)
if os.path.isfile(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                os.environ.setdefault(_k.strip(), _v.strip())
