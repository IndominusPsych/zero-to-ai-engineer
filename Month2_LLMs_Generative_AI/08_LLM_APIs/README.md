# 08 · LLM APIs

*Month 2, Week 6. Reading time: about 75 minutes. Assumes Lessons 03 (APIs/JSON), 06 and 07.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Providers and the shape every LLM API shares
- Getting an API key and setting it safely
- Your first API call
- The response object
- System prompts
- Multi-turn conversations: you manage the memory
- Streaming: show the answer as it's written
- Thinking and effort
- Structured outputs: guaranteed JSON
- Multimodal input: images and PDFs
- Tokens, cost and counting
- Errors, retries and rate limits
- Async and concurrency (a quick look)
- Designing LLM code well

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init llm_practice && cd llm_practice
uv add anthropic python-dotenv pydantic pandas
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [07 · Prompt Engineering](../07_Prompt_Engineering/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [09 · Embeddings & Vector Databases](../09_Embeddings_Vector_Databases/README.md) ➡️
