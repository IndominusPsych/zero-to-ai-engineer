# 01 · Python Fundamentals

*Month 1, Week 1. Reading time: about 60–75 minutes. Then type every example yourself.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Programs, running, and the interpreter
- Setting up a project the modern way: virtual environments and uv
- Values and data types
- Variables
- Operators: doing things with values
- Input, output and f-strings
- Comments
- Making decisions: if / elif / else
- Collections: holding many values
- Loops: repeating work
- List comprehensions (a shortcut)
- Functions: reusable recipes
- Errors and exceptions
- Files
- Modules and imports
- Classes and objects (a gentle first look)

## Quick setup

```bash
# 1. Install uv (pick your system)
curl -LsSf https://astral.sh/uv/install.sh | sh                                   # macOS / Linux
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"   # Windows
# 2. Close the terminal, open a new one, then:
uv python install 3.14
# 3. Make your course folder and this lesson's project
mkdir -p ~/ai-engineer-projects && cd ~/ai-engineer-projects
uv init python_practice && cd python_practice
code .
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [02 · NumPy, Pandas & Data Handling](../02_NumPy_Pandas_Data/README.md) ➡️
