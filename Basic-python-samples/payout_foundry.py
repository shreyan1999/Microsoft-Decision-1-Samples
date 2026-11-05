"""Classify a synthetic payout request with Microsoft-Decision-1.

Install the dependency with:
    python -m pip install python-dotenv

Set FOUNDRY_DECISIONS_URL (the full /providers/microsoft/v1/systemone URL),
FOUNDRY_API_KEY, and FOUNDRY_DEPLOYMENT in the environment or .env file.
Run: python .\\payout_foundry.py

Decision-1 uses `noul` for a yes/no probability and `choice` with a `criteria`
mapping for routing. HTTP failures include the server's error response.
"""

import json
import os
import urllib.error
import urllib.request
from dotenv import load_dotenv

load_dotenv()

# Fetch credentials from environment variables
api_url = os.getenv("FOUNDRY_DECISIONS_URL")
api_key = os.getenv("FOUNDRY_API_KEY")
deployment_name = os.getenv("FOUNDRY_DEPLOYMENT") # Your Foundry deployment identifier

if not api_url or not api_key or not deployment_name:
    raise ValueError(
        "Set FOUNDRY_DECISIONS_URL, FOUNDRY_API_KEY, and FOUNDRY_DEPLOYMENT."
    )

# Construct the structured decision payload
payload = {
    "model": deployment_name,
    "state": "Help! My payouts have been failing for 3 days and I need to pay rent.",
    "questions": {
        "is_urgent": {
            "type": "noul",
            "instructions": "Does this message convey financial urgency or immediate distress?",
            "criteria": {
                "true": "Explicitly time-sensitive or severe impact",
                "false": "Standard request or no urgency expressed"
            }
        },
        "team": {
            "type": "choice",
            "instructions": "Which department should handle this request?",
            "criteria": {
                "billing": "Payouts, payments, invoices, and refunds",
                "technical_support": "Software bugs, errors, and integration issues",
                "account_security": "Unauthorized access, fraud, and compromised accounts"
            }
        }
    }
}

# Configure and send the standard HTTP POST request
req = urllib.request.Request(
    api_url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "api-key": api_key,
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
        print(json.dumps(result, indent=2))
except urllib.error.HTTPError as error:
    detail = error.read().decode("utf-8", errors="replace")
    raise SystemExit(
        f"API Call Failed: HTTP {error.code} {error.reason}\n{detail}"
    ) from error
except urllib.error.URLError as error:
    raise SystemExit(f"API Call Failed: {error.reason}") from error
