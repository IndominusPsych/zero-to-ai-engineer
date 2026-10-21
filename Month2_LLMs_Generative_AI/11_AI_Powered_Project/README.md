# 11 · Build an AI-Powered Project

*Month 2, Week 8. Reading time: about 55 minutes, then 4–5 days of building. Assumes Lessons 05–10.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Choosing a good problem
- The architecture of an LLM app
- Prompts as code
- Structured outputs everywhere code reads the result
- Evaluation-driven development
- Guardrails
- Observability: logging and tracing
- Cost and latency budgets
- UX for AI apps
- Secrets and configuration
- Documentation and demo

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init --package studybuddy && cd studybuddy
uv add anthropic python-dotenv pydantic pypdf sentence-transformers chromadb streamlit
uv add --dev pytest ruff
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
cp .env .env.example    # then edit .env.example to replace your key with a placeholder
git init
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [10 · RAG Applications](../10_RAG_Applications/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [12 · AI Agents & Tool Calling](../../Month3_AI_Engineering_Agents/12_AI_Agents_Tool_Calling/README.md) ➡️
