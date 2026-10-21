# 03 · APIs, JSON & Git/GitHub

*Month 1, Week 3 (first half). Reading time: about 70 minutes. Assumes Lessons 01–02.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Clients, servers and HTTP
- URLs and endpoints
- HTTP methods: what you want to do
- Requests have parts
- Status codes: did it work?
- Authentication and API keys
- What JSON looks like
- Converting between JSON and Python
- Navigating nested JSON
- JSON Schema (a peek ahead)
- The `requests` library
- Handling failure gracefully: retries
- SDKs
- Reading API documentation
- Why version control?
- The three areas of Git
- Everyday commands
- .gitignore: things Git should never save
- GitHub: putting it online
- Branches and pull requests
- README files

## Quick setup

```bash
# one-time Git setup
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
gh auth login        # GitHub.com → HTTPS → Yes → Login with a web browser

# this lesson's project
cd ~/ai-engineer-projects
uv init api_practice && cd api_practice
uv add requests python-dotenv pydantic pandas
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [02 · NumPy, Pandas & Data Handling](../02_NumPy_Pandas_Data/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [04 · Machine Learning Basics](../04_Machine_Learning_Basics/README.md) ➡️
