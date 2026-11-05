# Basic Python samples

Minimal Python scripts that call **Microsoft-Decision-1** through its **Decisions API**. Each script describes a situation in plain text (`state`), asks one or more structured `questions`, and acts on the numeric answers with thresholds in code.

> Decision-1 uses the Decisions API, **not** the chat completions endpoint, so the OpenAI / chat SDKs do not work with it.

## Answer types used in these samples

| Type | Returns | Meaning |
|---|---|---|
| `noul` | probability `0–1` | Likelihood the answer is "yes" |
| `score` | weighted value over the `criteria` scale | Position across ordered criteria (e.g. `0–2`) |
| `choice` | one key from `criteria` | The selected category |

## The scripts

| File | Endpoint / auth | Transport | What it does |
|---|---|---|---|
| [decision1_demo.py](./decision1_demo.py) | OpenRouter (`OPENROUTER_API_KEY`) | OpenRouter SDK **or** `requests` | Scores an incident for urgency and priority, then prints an action |
| [decision1_foundry.py](./decision1_foundry.py) | Microsoft Foundry (API key **or** Entra ID) | `requests` | Same incident triage, running against a Foundry deployment |
| [incident_classifier.py](./incident_classifier.py) | Microsoft Foundry (API key **or** Entra ID) | `requests` | Classifies an incident from a CLI argument into one `category` (`choice`) |
| [payout_foundry.py](./payout_foundry.py) | Microsoft Foundry (API key) | `urllib` (stdlib) | Classifies a payout request for urgency (`noul`) and routes it to a team (`choice`) |

### [decision1_demo.py](./decision1_demo.py) — OpenRouter

Shows two ways to call the hosted model on OpenRouter: the `openrouter` Python SDK and a plain HTTP `requests` call.

```powershell
python -m pip install requests        # or: openrouter
$env:OPENROUTER_API_KEY = "sk-or-..."
python .\decision1_demo.py
```

### [decision1_foundry.py](./decision1_foundry.py) — Foundry incident triage

Same two questions (`urgent`, `priority`) against a Foundry deployment. Uses the deployment API key when `FOUNDRY_API_KEY` is set, otherwise signs in with Microsoft Entra ID.

```powershell
python -m pip install requests azure-identity python-dotenv
python .\decision1_foundry.py
```

### [incident_classifier.py](./incident_classifier.py) — Foundry classifier (CLI)

Takes the incident text as a command-line argument and returns exactly one category.

```powershell
python -m pip install requests azure-identity python-dotenv
python .\incident_classifier.py "Checkout is down for all customers."
```

### [payout_foundry.py](./payout_foundry.py) — Foundry payout routing

Classifies a synthetic payout request, printing the full JSON response. Uses only the Python standard library (`urllib`) for the HTTP call.

```powershell
python -m pip install python-dotenv
python .\payout_foundry.py
```

## Configuration

Set values in the environment or in a `.env` file beside the script. Existing process environment variables take precedence over `.env`.

### OpenRouter ([decision1_demo.py](./decision1_demo.py))

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ | OpenRouter API key (`sk-or-...`) |

### Microsoft Foundry (the other three scripts)

| Variable | Required | Description |
|---|---|---|
| `FOUNDRY_DECISIONS_URL` | ✅ | Full decision target URI from the Decision-1 deployment |
| `FOUNDRY_DEPLOYMENT` | ✅ | Deployment name (e.g. `Decision-1`) |
| `FOUNDRY_API_KEY` | optional* | Deployment key. If omitted, scripts that support it use Entra ID (`az login`) |

\* [payout_foundry.py](./payout_foundry.py) requires `FOUNDRY_API_KEY`. [decision1_foundry.py](./decision1_foundry.py) and [incident_classifier.py](./incident_classifier.py) fall back to Microsoft Entra ID when the key is absent — run `az login` first, with a Foundry role (e.g. Foundry User) on the project.

[incident_classifier.py](./incident_classifier.py) also accepts `AZURE_ENDPOINT` (resource base URL) and `DEPLOYMENT_NAME`, which, when nonempty, take precedence over the matching `FOUNDRY_*` settings.

Example `.env`:

```dotenv
FOUNDRY_DECISIONS_URL=https://<resource>.services.ai.azure.com/providers/microsoft/v1/systemone
FOUNDRY_DEPLOYMENT=Decision-1
FOUNDRY_API_KEY=<your-deployment-key>
```

## Requirements

- Python 3.10+
- Packages per script: `requests`, `azure-identity`, `python-dotenv`, and/or `openrouter` (install only what the script you run needs)

## Reference

- [Use Microsoft Decision models in Foundry](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision)
