# 15 · AI Automation

*Month 3, Week 10. Reading time: about 70 minutes. Assumes Lessons 03, 08, 12 and 13.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Triggers
- Schedules and cron
- Integrations: talking to the outside world
- No-code and low-code automation tools
- Batch vs real-time
- Idempotency, deduplication and state
- Secrets in automation
- MCP: making your own tools pluggable
- Coding agents as automation
- Monitoring and alerting
- Human-in-the-loop for automations
- Responsible automation

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init automation_lab && cd automation_lab
uv add anthropic python-dotenv feedparser requests pydantic mcp apscheduler fastapi uvicorn
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
echo "SLACK_WEBHOOK_URL=https://hooks.slack.com/services/..." >> .env   # optional
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [14 · LangChain / LangGraph](../14_LangChain_LangGraph/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [16 · Build and Deploy a Complete AI Project](../16_Build_and_Deploy/README.md) ➡️
