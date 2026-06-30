PROJECT_ID ?= $(shell gcloud config get-value project 2>/dev/null)
REGION ?= us-east1

# ---------------------------------------------------------------------------
# Local development
# ---------------------------------------------------------------------------

install:
	@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.6.12/install.sh | sh; source $$HOME/.local/bin/env; }
	uv sync

dev:
	uv run python app/fast_api_app.py

playground:
	uv run adk web --port 8501

lint:
	uv run ruff check . --fix
	uv run ruff format .

# ---------------------------------------------------------------------------
# Local Testing (Simulating Pub/Sub)
# ---------------------------------------------------------------------------

# Send a contract under the $500 threshold (Fast path)
test-fast-path:
	@echo "Testing fast path (< \$$500 savings)..."
	curl -X POST http://localhost:8000/apps/app/trigger/pubsub -H "Content-Type: application/json" -d '{"message": {"data": "ewogICJ0ZXh0IjogIkhpIHRoZXJlLCB3ZSBhcmUgcmVuZXdpbmcgeW91ciBTdGFydGVyIHBsYW4gZm9yICQxMjAveWVhci4gSXQgd2lsbCBhdXRvLXJlbmV3IGluIDMwIGRheXMuIgp9", "messageId": "12345"}, "subscription": "local-test-sub"}'

# Send a contract over the $500 threshold (HITL path)
test-hitl-path:
	@echo "Testing HITL path (>= \$$500 savings)..."
	curl -X POST http://localhost:8000/apps/app/trigger/pubsub -H "Content-Type: application/json" -d '{"message": {"data": "ewogICJ0ZXh0IjogIkRlYXIgY3VzdG9tZXIsIHlvdXIgRW50ZXJwcmlzZSBhY2NvdW50IHdpbGwgcmVuZXcgZm9yICQxMCwwMDAvWWVhci4gWW91ciBjdXJyZW50IHVzYWdlIGlzIG9ubHkgNSBzZWF0cy4gQ2FuY2VsbGF0aW9uIHJlcXVpcmVzIDYwIGRheXMgbm90aWNlLiIKfQ==", "messageId": "67890"}, "subscription": "local-test-sub"}'
