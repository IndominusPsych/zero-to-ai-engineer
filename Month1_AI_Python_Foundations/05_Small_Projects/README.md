# 05 · Build 2–3 Small Projects

*Month 1, Week 4. Reading time: about 50 minutes. Then 4–5 days of building. Assumes Lessons 01–04.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Scope and the MVP
- Requirements
- Project structure
- Interfaces: how people use your program
- Testing
- Logging and error messages
- Code quality basics
- The README
- Iteration: the build loop
- Using AI assistants while learning

## Quick setup

```bash
cd ~/ai-engineer-projects
# Project A (walked through in Section 3)
uv init --package expense-analyzer && cd expense-analyzer
uv add pandas matplotlib
uv add --dev pytest ruff
git init && gh repo create expense-analyzer --public --source=. --remote=origin   # when ready to publish

# Project B adds:  uv add requests streamlit
# Project C adds:  uv add scikit-learn joblib streamlit
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [04 · Machine Learning Basics](../04_Machine_Learning_Basics/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [06 · LLM Fundamentals](../../Month2_LLMs_Generative_AI/06_LLM_Fundamentals/README.md) ➡️
