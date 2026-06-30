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
   This is the agent's actual deliverable. Rather than just notifying someone that "this contract looks wasteful," the agent writes a complete,
   ready-to-send email citing the specific usage mismatch, dollar amount,
   and contractual notice period, so the reviewer's job becomes "read,
   tweak if needed, and send" instead of writing it from scratch.


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

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **agents-cli**: Agents CLI - Install with `uv tool install google-agents-cli`
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)


## Quick Start

Install `agents-cli` and its skills if not already installed:

```bash
uvx google-agents-cli setup
```

Install required packages:

```bash
agents-cli install
```

Test the agent with a local web server:

```bash
agents-cli playground
```

You can also use features from the [ADK](https://adk.dev/) CLI with `uv run adk`.

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `agents-cli install` | Install dependencies using uv                                                         |
| `agents-cli playground` | Launch local development environment                                                  |
| `agents-cli lint`    | Run code quality checks                                                               |
| `agents-cli eval`    | Evaluate agent behavior (generate, grade, analyze, and more — see `agents-cli eval --help`) |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests                                                        || [A2A Inspector](https://github.com/a2aproject/a2a-inspector) | Launch A2A Protocol Inspector                                                        |

## 🛠️ Project Management

| Command | What It Does |
|---------|--------------|
| `agents-cli scaffold enhance` | Add CI/CD pipelines and Terraform infrastructure |
| `agents-cli infra cicd` | One-command setup of entire CI/CD pipeline + infrastructure |
| `agents-cli scaffold upgrade` | Auto-upgrade to latest version while preserving customizations |

---

## Development

Edit your agent logic in `app/agent.py` and test with `agents-cli playground` - it auto-reloads on save.

## Deployment

```bash
gcloud config set project <your-project-id>
agents-cli deploy
```

To add CI/CD and Terraform, run `agents-cli scaffold enhance`.
To set up your production infrastructure, run `agents-cli infra cicd`.

## Observability

Built-in telemetry exports to Cloud Trace, BigQuery, and Cloud Logging.

## A2A Inspector

This agent supports the [A2A Protocol](https://a2a-protocol.org/). Use the [A2A Inspector](https://github.com/a2aproject/a2a-inspector) to test interoperability.
See the [A2A Inspector docs](https://github.com/a2aproject/a2a-inspector) for details.

Simple ReAct agent
Agent generated with `agents-cli` version `0.6.1`
