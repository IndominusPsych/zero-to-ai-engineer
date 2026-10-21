# 13 · Agentic Workflows

*Month 3, Week 9. Reading time: about 70 minutes. Assumes Lessons 07, 08 and 12.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- The building block: the augmented LLM
- Pattern 1: Prompt chaining (a pipeline)
- Pattern 2: Routing
- Pattern 3: Parallelisation
- Pattern 4: Orchestrator–workers
- Pattern 5: Evaluator–optimiser (a feedback loop)
- When to use which
- State
- Reliability engineering for workflows
- Multi-agent systems (briefly)
- Evaluating workflows and agents
- Observability: traces again

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init support_workflow && cd support_workflow
uv add anthropic python-dotenv pydantic
uv add --dev pytest
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [12 · AI Agents & Tool Calling](../12_AI_Agents_Tool_Calling/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [14 · LangChain / LangGraph](../14_LangChain_LangGraph/README.md) ➡️
