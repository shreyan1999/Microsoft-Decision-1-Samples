# Agent Action Gatekeeper

A Streamlit demo for **Microsoft-Decision-1**. An AI agent proposes an action, and the decision model checks it in one call before it runs:

| Question | Type | Asks |
|---|---|---|
| `in_scope` | noul | Does the action match the assigned task? |
| `destructive` | noul | Is it destructive or hard to reverse? |
| `injected` | noul | Is the agent following instructions hidden in untrusted content? |
| `risk` | score | Low / Medium / High / Critical |
| `verdict` | choice | allow / ask_human / block |

The app combines the answers with plain thresholds in code (`gate()` in `app.py`) and shows the final decision, latency, tokens and cost.

## Built-in scenarios

- ✏️ **Fix a typo**: a harmless edit that should be allowed
- 🧨 **Overeager cleanup**: asked to delete old logs, the agent proposes `rm -rf /var/log/*`
- 🕵️ **Poisoned email**: a hidden instruction in an email tries to exfiltrate invoices
- 💸 **Refund with an extra zero**: a $45 refund becomes $450
- 🚑 **Restart the crashing pod**: legitimate, but touches production
- 📝 **Write your own**

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Choose the model source in the sidebar:

- **Microsoft Foundry**: paste the Decision-1 target URI from *Build > Models > Decision-1 > Details*. Add the key, or leave it empty to sign in with Entra ID (`az login`).
- **OpenRouter**: paste an OpenRouter API key.

You can also set `FOUNDRY_DECISIONS_URL`, `FOUNDRY_API_KEY`, `FOUNDRY_DEPLOYMENT` or `OPENROUTER_API_KEY` as environment variables.
