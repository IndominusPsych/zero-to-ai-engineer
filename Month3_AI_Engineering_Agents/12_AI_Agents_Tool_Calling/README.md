# 12 · AI Agents & Tool Calling

*Month 3, Week 9. Reading time: about 75 minutes. Assumes Month 2 (especially Lessons 07, 08 and 10).*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Workflows vs agents: the spectrum
- What a tool is
- The tool-calling round trip
- Parallel tool calls
- Errors are results too
- The agent loop
- Tool choice and strict tools
- Tool runners: letting the SDK run the loop
- Server tools: tools the provider runs
- MCP: a standard plug for tools
- Memory for agents
- Designing good tools
- Safety: agents can do real damage

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init travel_agent && cd travel_agent
uv add anthropic python-dotenv requests
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [11 · Build an AI-Powered Project](../../Month2_LLMs_Generative_AI/11_AI_Powered_Project/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [13 · Agentic Workflows](../13_Agentic_Workflows/README.md) ➡️
