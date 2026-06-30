# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Centralized configuration for the vendor contract agent.

Authentication:
  - If GOOGLE_API_KEY is set → AI Studio mode (no GCP project needed).
  - Otherwise → Vertex AI mode (requires GOOGLE_CLOUD_PROJECT + gcloud login).

Set GOOGLE_GENAI_USE_VERTEXAI=False and GOOGLE_API_KEY in .env for local dev.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Authentication bootstrap
# ---------------------------------------------------------------------------
if os.getenv("GOOGLE_API_KEY"):
    # AI Studio path — no Vertex AI project required
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")
else:
    # Vertex AI path — fall back to ADC credentials
    try:
        import google.auth

        _, project_id = google.auth.default()
        os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id or "")
        os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
    except Exception:
        pass
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


# ---------------------------------------------------------------------------
# Agent config
# ---------------------------------------------------------------------------


@dataclass
class VendorContractConfig:
    """Agent configuration with sensible defaults.

    Attributes:
        model: Gemini model alias to use for all LLM agents.
        review_threshold: Annual savings/risk (USD) at or above which the
            HITL path is triggered.  Below this, the fast path auto-logs.
    """

    model: str = os.getenv("MODEL", "gemini-flash-latest")
    review_threshold: float = float(os.getenv("REVIEW_THRESHOLD", "500.0"))


config = VendorContractConfig()
