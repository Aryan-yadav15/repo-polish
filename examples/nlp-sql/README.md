# Example · NLP → SQL

A full run of the pipeline on a Next.js + FastAPI + LangChain project that turns questions into SQL.

- **Result:** [README](https://github.com/Aryan-yadav15/Database-NLP-Query) · [pull request #1](https://github.com/Aryan-yadav15/Database-NLP-Query/pull/1) (merged)
- **`cards.json`:** the card config used ([assets/](assets/) are the generated cards)
- **`steps.json`:** the GIF script (sets the model in a hidden sidebar, asks two questions, waits out a rate limit)
- **`demo.gif`:** the recorded result

What the run found and fixed:

| Stage | Finding | Action |
|---|---|---|
| Secrets | 2 Gemini API keys + DB passwords hardcoded, also in history | moved to env vars, `.env.example`, owner told to rotate |
| Hygiene | a Windows virtualenv and logs committed | untracked, `.gitignore` updated |
| Run | `langchain` unpinned; 1.x removed `AgentExecutor` → import error | pinned `>=0.3,<0.4` |
| Run | `gemini-1.5-flash` / `2.0-flash` retired | default → `gemini-2.5-flash` |
| Run | startup schema cache always crashed (tuple cursor indexed by name) | `RealDictCursor` |
| Demo | particle animation made the GIF 20 MB | hid it with `CSS=`, cropped to the chat panel → 7.6 MB |
| Demo | free tier: 5 requests/min per model | `pause` + `speed` step between questions |
| README | existing docs said the agent stopped via a custom parser | code check: it's `max_iterations=1`; README says that |
