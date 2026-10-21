# 14 · LangChain / LangGraph

*Month 3, Week 10. Reading time: about 75 minutes. Assumes Lessons 08, 10, 12 and 13.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Installing
- Chat models: one interface for many providers
- Runnables and LCEL (a quick look)
- Tools
- `create_agent`: the ready-made agent
- Middleware: customising the agent loop
- RAG building blocks
- LangGraph: thinking in graphs
- State and reducers
- Building and running a graph
- Checkpointers and threads: memory and resume
- Interrupts: pausing for a human
- Streaming and observability
- Framework or no framework?

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init lc_lab && cd lc_lab
uv add langchain langchain-anthropic langgraph langgraph-checkpoint-sqlite python-dotenv requests
uv add langchain-community langchain-text-splitters langchain-chroma langchain-huggingface pypdf sentence-transformers
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [13 · Agentic Workflows](../13_Agentic_Workflows/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [15 · AI Automation](../15_AI_Automation/README.md) ➡️
