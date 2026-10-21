# 16 · Build and Deploy a Complete AI Project

*Month 3, Week 11. Reading time: about 80 minutes, then several days of building. Assumes everything so far, especially Lessons 03, 05, 08, 10, 11 and 15.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Client, server, frontend, backend
- Environments
- FastAPI: building a backend API
- Frontend options
- Containers and Docker
- Where to host
- Databases in production
- Secrets in production
- Protecting a public AI app
- CI/CD: automatic testing and deployment
- Observability in production
- Scaling and performance (just enough)
- The production checklist

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init handbook-assistant && cd handbook-assistant
uv add fastapi uvicorn anthropic pydantic-settings
uv add --dev pytest httpx ruff
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [15 · AI Automation](../15_AI_Automation/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [17 · Put Your Projects on GitHub + Portfolio](../17_GitHub_and_Portfolio/README.md) ➡️
