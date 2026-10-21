# Zero to AI Engineer 🚀

**A free 12-week course for complete beginners: from your first line of Python to deployed AI agents.**

Python · Pandas · Machine learning · LLMs · Prompt engineering · Claude API · Embeddings · RAG · AI agents · LangChain/LangGraph · MCP · Automation · FastAPI · Docker · Portfolio

*Updated October 2026. Uses current tools: Python 3.14, pandas 3.0, LangChain/LangGraph 1.x, MCP SDK 2.x.*

---

## ✨ What's inside

- **17 lessons**, one for every topic in the 3-month roadmap. Each is a 10–15 page explanation written for beginners, in the same 7 sections:
  1. The big picture
  2. Core concepts
  3. How it works, with one worked example from start to finish
  4. Key terms
  5. The people involved
  6. Common misconceptions
  7. A one-page recap
- **17 practice files** with warm-ups, hands-on exercises, a mini-project with a grading rubric, a quiz and a full answer key.
- **3 monthly final tests** (theory and a practical) with answer keys.
- **A setup guide** for macOS, Windows and Linux, and [`check_setup.py`](check_setup.py) to check your computer is ready.
- **Tested code:** the examples that don't need an AI model were run on current library versions before publishing.

No experience needed. Every term is explained before it's used, and each section ends with an "In simple words" summary.

---

## 🗺️ Course map

| Month | Topics | Final test |
|---|---|---|
| **[Month 1: AI + Python Foundations 🐍](Month1_AI_Python_Foundations/README.md)** | [01 Python fundamentals](Month1_AI_Python_Foundations/01_Python_Fundamentals/README.md) · [02 NumPy, Pandas & data](Month1_AI_Python_Foundations/02_NumPy_Pandas_Data/README.md) · [03 APIs, JSON & Git/GitHub](Month1_AI_Python_Foundations/03_APIs_JSON_Git/README.md) · [04 Machine learning basics](Month1_AI_Python_Foundations/04_Machine_Learning_Basics/README.md) · [05 Small projects](Month1_AI_Python_Foundations/05_Small_Projects/README.md) | [Month 1 test](Month1_AI_Python_Foundations/Month1_Final_Test.md) |
| **[Month 2: LLMs + Generative AI 🧠](Month2_LLMs_Generative_AI/README.md)** | [06 LLM fundamentals](Month2_LLMs_Generative_AI/06_LLM_Fundamentals/README.md) · [07 Prompt engineering](Month2_LLMs_Generative_AI/07_Prompt_Engineering/README.md) · [08 LLM APIs](Month2_LLMs_Generative_AI/08_LLM_APIs/README.md) · [09 Embeddings & vector DBs](Month2_LLMs_Generative_AI/09_Embeddings_Vector_Databases/README.md) · [10 RAG](Month2_LLMs_Generative_AI/10_RAG_Applications/README.md) · [11 AI-powered project](Month2_LLMs_Generative_AI/11_AI_Powered_Project/README.md) | [Month 2 test](Month2_LLMs_Generative_AI/Month2_Final_Test.md) |
| **[Month 3: AI Engineering + Agents ⚡](Month3_AI_Engineering_Agents/README.md)** | [12 Agents & tool calling](Month3_AI_Engineering_Agents/12_AI_Agents_Tool_Calling/README.md) · [13 Agentic workflows](Month3_AI_Engineering_Agents/13_Agentic_Workflows/README.md) · [14 LangChain/LangGraph](Month3_AI_Engineering_Agents/14_LangChain_LangGraph/README.md) · [15 AI automation](Month3_AI_Engineering_Agents/15_AI_Automation/README.md) · [16 Build & deploy](Month3_AI_Engineering_Agents/16_Build_and_Deploy/README.md) · [17 GitHub + portfolio](Month3_AI_Engineering_Agents/17_GitHub_and_Portfolio/README.md) | [Month 3 test](Month3_AI_Engineering_Agents/Month3_Final_Test.md) |

By the end you'll have 3 small Python projects, a "chat with your documents" app, an automation, and a deployed capstone project with a portfolio to show them.

---

## 🏁 Start here

1. 📋 **[00_START_HERE_Master_Plan.md](00_START_HERE_Master_Plan.md)**: the 12-week schedule, how to study each topic, a progress tracker, and what changed recently in the tools.
2. 🛠️ **[00_SETUP_Install_Guide.md](00_SETUP_Install_Guide.md)**: install VS Code, uv and Python (Steps 1–4) before Lesson 01. Everything else is installed when a lesson asks for it.
3. 📖 **[Lesson 01: Python Fundamentals](Month1_AI_Python_Foundations/01_Python_Fundamentals/lesson.md)**: begin.

**Time:** about 2 hours a day, 6 days a week. If you have less time, stretch each week to two.
**Cost:** everything is free except the AI model's API in Months 2–3, which typically costs **$5–15 in total**. The setup guide shows how to set a spending limit.

---

## 📖 How to read this course

The course is written in **Markdown** (`.md` files): plain text where symbols like `#`, `**` and `|` turn into headings, bold text and tables when they're displayed. Read them **formatted**, not as raw text, or the tables and diagrams won't make sense.

### Option A: on GitHub (just reading)

Click any folder or file on this page. GitHub formats Markdown automatically, including tables and diagrams. Each folder's `README.md` lists its files and links to the next topic. Use the ☰ icon at the top right of a file to jump between sections.

### Option B: in VS Code (recommended, since you'll be coding anyway)

**1. Get the course onto your computer**

```bash
git clone https://github.com/<your-username>/zero-to-ai-engineer.git
code zero-to-ai-engineer
```

No Git yet? On GitHub, click **Code → Download ZIP**, unzip it, then in VS Code use **File → Open Folder…** and pick the folder.

**2. Install the recommended extensions.** When the folder opens, VS Code shows a pop-up: *"Do you want to install the recommended extensions?"* Click **Install**. If you missed it, open the Extensions panel (`Cmd+Shift+X` / `Ctrl+Shift+X`), type `@recommended` and install the list:

| Extension | Why you need it |
|---|---|
| **Markdown Preview Mermaid Support** | Draws the flowchart diagrams (VS Code's built-in preview shows them as code without it) |
| **Markdown All in One** | Table of contents, shortcuts, and ticking `[ ]` checkboxes in the progress tracker |
| **Python**, **Jupyter**, **Ruff** | Running, exploring and tidying your code during the course |

**3. Open files in preview mode**

| What you want | Mac | Windows / Linux |
|---|---|---|
| Show the formatted preview of the open file | `Cmd+Shift+V` | `Ctrl+Shift+V` |
| Preview **side by side** with the raw text (to copy code or edit) | `Cmd+K`, then `V` | `Ctrl+K`, then `V` |
| Preview without opening the raw text first | Right-click the file in the Explorer → **Open Preview** | same |
| Jump to a section | **Outline** panel at the bottom of the Explorer sidebar, or `Cmd+Shift+O` | `Ctrl+Shift+O` |
| Search across every lesson | `Cmd+Shift+F` | `Ctrl+Shift+F` |
| Zoom the text in or out | `Cmd +` / `Cmd -` | `Ctrl +` / `Ctrl -` |

Links in the preview are clickable, so you can move from a README to a lesson to the next topic without using the sidebar.

**4. Optional: always open `.md` files in preview.** Press `Cmd+Shift+P` / `Ctrl+Shift+P`, run **Preferences: Open User Settings (JSON)**, and add:

```json
"workbench.editorAssociations": { "*.md": "vscode.markdown.preview.editor" }
```

To edit a file later (for example to tick off the progress tracker), right-click its tab → **Reopen Editor With… → Text Editor**.

**Tips**
- Keep your practice code in a **separate** folder (`~/ai-engineer-projects`, as the setup guide shows), not inside this course folder. Then you can `git pull` course updates without conflicts.
- Copy code from the side-by-side raw view (`Cmd+K V`), or better, **type it yourself**: you'll learn much faster.
- Diagrams still showing as code? Check the Mermaid extension is installed and enabled, then close and reopen the preview.

---

## 🧪 Check your computer is ready

Copy [`check_setup.py`](check_setup.py) into a project that has the course packages installed (Setup Guide Section 14 shows how), then run:

```bash
uv run check_setup.py
```

It lists every package and tool the course uses and tells you what's missing.

---

## 🤝 Contributing

Found a mistake, a broken link or an outdated command? Libraries change fast, so please [open an issue](../../issues) or a pull request. Say which file and section, and paste any error message.

## 📄 License

[MIT License](LICENSE): free to use, share and adapt, including in classes and study groups, as long as you keep the credit.
