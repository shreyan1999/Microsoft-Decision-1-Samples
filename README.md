# Microsoft-Decision-1 Samples

Example code for **Microsoft-Decision-1**, a Microsoft Decision model that answers
structured questions about a situation in a single fast call. You describe a
situation in plain text (the `state`), ask one or more typed `questions`, and act
on the numeric answers with plain thresholds in your own code.

Decision-1 is served through the **Decisions API**, *not* the chat completions
endpoint, so the OpenAI / chat SDKs do not work with it. You can reach the model
either through **Microsoft Foundry** (a Decision-1 deployment) or through
**OpenRouter**.

## Answer types

| Type | Returns | Meaning |
|---|---|---|
| `noul` | probability `0–1` | Likelihood the answer is "yes" |
| `score` | weighted value over the `criteria` scale | Position across ordered criteria (e.g. `0–2`) |
| `choice` | one key from `criteria` | The selected category |

## What's in this repo

| Folder | What it is | Highlights |
|---|---|---|
| [Basic-python-samples](./Basic-python-samples) | Minimal Python scripts that call the Decisions API | Incident triage, classification and payout routing against OpenRouter or Foundry, using `requests`, `urllib` or the OpenRouter SDK |
| [Agentic-Gatekeeper](./Agentic-Gatekeeper) | A Streamlit app that gates an AI agent's proposed action | Checks `in_scope`, `destructive`, `injected`, `risk` and `verdict` in one call, then shows the decision, latency, tokens and cost |

### [Basic-python-samples](./Basic-python-samples)

Standalone scripts, each self-contained and runnable from the command line:

- **decision1_demo.py** — scores an incident for urgency and priority via OpenRouter
  (OpenRouter SDK or `requests`).
- **decision1_foundry.py** — the same incident triage against a Foundry deployment
  (API key or Entra ID).
- **incident_classifier.py** — classifies an incident passed as a CLI argument into
  one category (Foundry).
- **payout_foundry.py** — routes a payout request by urgency and team, using only the
  Python standard library (Foundry).

See the folder's [README](./Basic-python-samples/README.md) for per-script run
commands and configuration.

### [Agentic-Gatekeeper](./Agentic-Gatekeeper)

A Streamlit demo where an agent proposes an action and Decision-1 vets it before it
runs. It ships with built-in scenarios (harmless typo fix, destructive cleanup,
prompt-injected email, inflated refund, production pod restart) and a custom-scenario
mode. See the folder's [README](./Agentic-Gatekeeper/README.md).

```bash
cd Agentic-Gatekeeper
pip install -r requirements.txt
streamlit run app.py
```

## Getting access

- **Microsoft Foundry** — deploy Decision-1 in your Foundry project and copy the
  decision target URI from *Build > Models > Decision-1 > Details*. Authenticate with
  the deployment key or with Microsoft Entra ID (`az login`).
- **OpenRouter** — create an OpenRouter API key (`sk-or-...`) and use the
  `microsoft/microsoft-decision-1` model.

## Requirements

- Python 3.10+
- Install only the packages the script or app you run needs: `requests`,
  `azure-identity`, `python-dotenv`, `streamlit`, and/or `openrouter`.

## Reference

- [Use Microsoft Decision models in Foundry](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision)
