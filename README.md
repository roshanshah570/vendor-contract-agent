# Vendor Contract Review Agent 

An ambient AI agent that monitors incoming vendor contracts and renewal notices, automatically flags cost-saving opportunities, and routes
high-value or high-risk decisions to a human for approval before taking any action.

## What It Does

Companies routinely overpay for SaaS and vendor subscriptions because nobody has time to manually audit every contract for usage mismatches,
auto-renewal traps, or unfavorable terms. This agent solves that by:

1. **Watching for incoming contracts/renewal notices** (simulated locally via a Pub/Sub-style webhook trigger, designed to integrate with a   real event source such as Gmail or Google Drive in production)
2. **Extracting structured terms** from unstructured text using an LLM, 
   vendor name, price, renewal date, notice period, and usage tier
3. **Calculating a flagged savings opportunity** by comparing contracted
   spend against actual usage
4. **Routing automatically**:
   - Low-value findings (< $500/year) are auto-logged with no human
     review required
   - High-value findings (≥ $500/year) pause the workflow and require
     explicit human approval before any further action is taken
5. **Drafting a renegotiation/cancellation email** once a human approves.
   This is the agent's actual deliverable. Rather than just notifying someone that "this contract looks wasteful," the agent writes a complete, ready-to-send email citing the specific usage mismatch, dollar amount, and contractual notice period, so the reviewer's job becomes "read, tweak if needed, and send" instead of writing it from scratch.


## Security Features

Because this agent processes untrusted external text (contract documents
and emails), it includes two layers of defense before any content reaches
the LLM or gets stored:

- **PII Redaction**: Personally identifiable information (e.g., SSNs) is
  detected and redacted before being passed to the LLM or persisted in
  session state.
- **Prompt-Injection Defense**: Incoming text is screened for attempts to
  manipulate agent behavior (e.g., "ignore previous instructions,"
  "auto-approve this"). Any detected injection attempt forces the
  submission into the human-review path — regardless of the dollar
  amount the attacker claims — and surfaces an explicit security warning
  to the reviewer.



## Project Structure

```
vendor-contract-agent/
├── app/         # Core agent code
│   ├── agent.py               # Main agent logic
│   ├── fast_api_app.py        # FastAPI Backend server
│   └── app_utils/             # App utilities and helpers
├── tests/                     # Unit, integration, and load tests
├── GEMINI.md                  # AI-assisted development guide
└── pyproject.toml             # Project dependencies
```


## Prerequisites

- **uv**: Python package manager — [Install](https://docs.astral.sh/uv/getting-started/installation/)
- **agents-cli**: `uv tool install google-agents-cli`
- **A Google AI Studio API key** — [Get one here](https://aistudio.google.com/apikey) (free, no Google Cloud project or billing required for local development)
- *(Optional)* Google Cloud SDK — only needed if you plan to deploy to Agent Runtime

## Setup

1. Install dependencies:
```bash
   agents-cli install
```

2. Create a `.env` file in the project root with your AI Studio key:
  - GOOGLE_GENAI_USE_VERTEXAI=False
  - GOOGLE_API_KEY=your-api-key-here

3. Start the local server:
```bash
   agents-cli playground
```
   (or `make dev` to run the FastAPI server directly on port 8000)

## Testing the Agent

Simulate an incoming contract trigger (base64-encoded contract/email text):

```bash
curl -X POST http://localhost:8000/apps/app/trigger/pubsub \
  -H "Content-Type: application/json" \
  -d '{"message": {"data": "<base64-encoded-text>", "messageId": "test-001"}, "subscription": "local-test-sub"}'
```

Check the resulting session state:

```bash
curl -s "http://localhost:8000/apps/app/users/local-test-sub/sessions" | python3 -m json.tool
```

For a high-value contract flagged as `pending-approval`, submit a decision to resume the workflow:

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"appName": "app", "userId": "local-test-sub", "sessionId": "<session-id>", "newMessage": {"role": "user", "parts": [{"functionResponse": {"id": "approve_renegotiation", "name": "adk_request_input", "response": {"decision": "approve"}}}]}}'
```

## Commands

| Command | Description |
|---|---|
| `agents-cli install` | Install dependencies using uv |
| `agents-cli playground` | Launch local development environment |
| `agents-cli lint` | Run code quality checks |
| `agents-cli eval` | Evaluate agent behavior |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests |

## Status

Fully tested locally end-to-end, including the fast-path/HITL routing, the pause-and-resume approval mechanism, and both security defenses. Not currently connected to a live Gmail/Drive source or deployed to production, local triggers are simulated via direct API calls, standing in for what a real Pub/Sub subscription would deliver automatically.
