"""
Calling Microsoft-Decision-1 deployed in Microsoft Foundry.

Setup
-----
pip install requests azure-identity

Set these environment variables from your deployment in the Foundry portal
(Build > Models > Decision-1 > Details):

  FOUNDRY_DECISIONS_URL   The full target URI shown for the Decision-1 deployment
  FOUNDRY_API_KEY         (optional) The deployment key. If not set, the script
                          signs in with Microsoft Entra ID instead.
  FOUNDRY_DEPLOYMENT      (optional) Deployment name, default "Decision-1"

For Entra ID sign-in, run `az login` first. Your account needs a Foundry
role (for example, Foundry User) on the project.
"""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

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


def build_headers() -> dict:
    """Use the deployment key if present, otherwise Microsoft Entra ID."""
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("FOUNDRY_API_KEY")
    if api_key:
        headers["api-key"] = api_key
    else:
        from azure.identity import DefaultAzureCredential

        token = DefaultAzureCredential().get_token("https://ai.azure.com/.default")
        headers["Authorization"] = f"Bearer {token.token}"
    return headers


def decide(state, questions) -> dict:
    """Send one Decisions request to the Foundry deployment."""
    response = requests.post(
        os.environ["FOUNDRY_DECISIONS_URL"],
        headers=build_headers(),
        json={
            "model": os.getenv("FOUNDRY_DEPLOYMENT", "Decision-1"),
            "state": state,
            "questions": questions,
        },
        timeout=30,
    )
    if not response.ok:
        raise RuntimeError(f"{response.status_code}: {response.text}")
    return response.json()


def main():
    data = decide(STATE, QUESTIONS)
    answers = data["answers"]

    urgent = answers["urgent"]["noul"]          # probability of "yes", 0-1
    priority = answers["priority"]["score"]     # weighted position, 0-2 here
    confidence = answers["priority"].get("confidence")

    print(f"urgent     : {urgent:.4f}")
    print(f"priority   : {priority:.4f}  (confidence {confidence})")
    print(f"usage      : {data.get('usage')}")

    # Act on the decision with thresholds in code
    if urgent > 0.9 and priority > 1.5:
        print("Action: page the on-call engineer")
    elif urgent < 0.2 and priority < 0.5:
        print("Action: file as a routine ticket")
    else:
        print("Action: send to a human reviewer")


if __name__ == "__main__":
    main()
 