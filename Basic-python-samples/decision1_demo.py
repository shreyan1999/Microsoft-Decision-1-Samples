"""
Calling Microsoft-Decision-1 from Python.

Two options are shown:
  1. The OpenRouter Python SDK  (pip install openrouter)
  2. A plain HTTP call with requests (pip install requests)

Both need an OpenRouter API key:
  export OPENROUTER_API_KEY="sk-or-..."

Note: Microsoft-Decision-1 uses the Decisions API, not the chat
completions endpoint, so the OpenAI / chat SDKs will not work with it.
"""

import os

STATE = (
    "The checkout service has been unavailable for 20 minutes. "
    "Customers cannot complete purchases, and there is no workaround."
)

QUESTIONS = {
    "urgent": {
        "type": "noul",
        "instructions": "Does this incident require immediate attention?",
    },
    "priority": {
        "type": "score",
        "instructions": "How high is the priority of this incident?",
        "criteria": [
            "Routine, no time pressure",
            "Important, some time pressure",
            "Urgent, immediate attention needed",
        ],
    },
}

MODEL = "microsoft/microsoft-decision-1"


# ---------------------------------------------------------------------------
# Option 1: OpenRouter Python SDK
# ---------------------------------------------------------------------------
def run_with_sdk():
    from openrouter import OpenRouter

    with OpenRouter(api_key=os.environ["OPENROUTER_API_KEY"]) as client:
        res = client.alpha.decisions.create(
            model=MODEL,
            state=STATE,
            questions=QUESTIONS,
        )
    print(res)


# ---------------------------------------------------------------------------
# Option 2: Plain HTTP with requests
# ---------------------------------------------------------------------------
def run_with_requests():
    import requests

    response = requests.post(
        "https://openrouter.ai/api/alpha/decisions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={"model": MODEL, "state": STATE, "questions": QUESTIONS},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    answers = data["answers"]
    urgent = answers["urgent"]["noul"]        # probability of "yes", 0-1
    priority = answers["priority"]["score"]   # weighted position, 0-2 here

    print(f"urgent   : {urgent:.4f}")
    print(f"priority : {priority:.4f}")
    print(f"usage    : {data.get('usage')}")

    # Act on the decision with thresholds in code
    if urgent > 0.9 and priority > 1.5:
        print("Action: page the on-call engineer")
    elif urgent < 0.2 and priority < 0.5:
        print("Action: file as a routine ticket")
    else:
        print("Action: send to a human reviewer")


if __name__ == "__main__":
    run_with_requests()
