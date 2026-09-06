# Enterprise Knowledge Assistant — Demo Script

This folder contains six sample company-policy documents plus a step-by-step
script so you (or anyone reviewing the project) can run a convincing live
demo in under 5 minutes.

## 1. Setup (one-time)

1. Copy the six files from this `data/` folder into your project's own
   `enterprise_knowledge_assistant/data/` folder (creating it if it doesn't
   exist).
2. Make sure `.env` has a valid `OPENAI_API_KEY` (see the security note
   below).
3. Run the app:
   ```
   streamlit run app.py
   ```
   or double-click `run.bat` / `run.ps1`.

> **Security note:** the `_env` file you had included a live-looking OpenAI
> key. Rotate/revoke that key in your OpenAI account and put a fresh one only
> in your local `.env` — never in anything you share or commit.

## 2. Build the index

1. In the sidebar, confirm it shows **"Documents in `data/`: 6"**.
2. Click **🔄 Build / Rebuild Index**.
3. Wait for the success message: *"Indexed 6 documents into N chunks."*

## 3. Suggested demo flow (talk track included)

Say this while you type, so the audience follows the story:

| # | You type | What to point out afterward |
|---|----------|------------------------------|
| 1 | `What is the leave policy?` | Answer cites `Leave_Policy.txt`; mentions the 18-day annual + 12-day sick entitlement. |
| 2 | `What about carry-forward?` | No need to repeat "leave" — **conversation memory** resolves the follow-up. Answer gives the 5-day cap and March 31 deadline. |
| 3 | `How should I report a phishing email?` | Pulls from `IT_Policy.txt` — shows it can switch topics/documents seamlessly. |
| 4 | `What is required for business travel?` | Pulls from `Travel_Policy.txt`; mentions pre-approval and booking lead time. |
| 5 | `Who should I contact about benefit eligibility?` | Pulls from `Benefits.txt` — a "who do I ask" question, not just "what is the rule." |
| 6 | `What's the policy on accepting vendor gifts?` | Pulls from `Code_of_Conduct.txt` — the $100 gift threshold. |

After any answer, open:
- **📄 Sources used** — show the exact document(s) cited.
- **🔎 Retrieved / reranked context** — show the retrieval method (vector /
  BM25 / fused) and score per chunk, to demonstrate the hybrid pipeline is
  really doing the work, not just the LLM guessing.

## 4. Stress-test questions (optional, shows honesty/grounding)

Ask something **not** covered by any document, e.g.:

```
What is the company's stock buyback policy?
```

The assistant should say it cannot find this in the provided documents,
rather than making something up — this demonstrates the hallucination
mitigation described in the README.

## 5. Reset for a clean re-run

Click **🗑️ Clear Conversation** in the sidebar between demo runs so
conversation memory doesn't carry over into the next audience.

## Files in this folder

| File | Use |
|---|---|
| `data/Leave_Policy.txt` | Sample leave policy (annual, sick, carry-forward, etc.) |
| `data/IT_Policy.txt` | Sample IT/security policy (passwords, phishing, devices) |
| `data/Travel_Policy.txt` | Sample business travel policy |
| `data/Employee_Handbook.txt` | Sample general handbook (hours, conduct, reviews) |
| `data/Benefits.txt` | Sample benefits overview (insurance, retirement, wellness) |
| `data/Code_of_Conduct.txt` | Sample ethics & compliance code of conduct |

All six are fictional documents for **Acme Corp**, written specifically to
match the example questions already listed in your project's `README.md`.
