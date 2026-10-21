# START HERE: Zero to AI Engineer, Your 3-Month Plan

*Built from `Plan.jpeg`. Last checked against current tools: October 2026.*

This folder turns the 3-month roadmap in `Plan.jpeg` into a full course you can work through on your own. **Every bullet in the image has its own folder**, and each folder holds two files:

| File | What it is | How to use it |
|---|---|---|
| `lesson.md` | A 10–15 page beginner explanation, written like a patient teacher | Read it start to finish, slowly. Don't skip the "In simple words" boxes. |
| `practice_and_test.md` | Warm-up drills, hands-on exercises, a quiz, and a full answer key | Do it **after** the lesson. Cover the answer key until you've tried. |

Each month also ends with a **Month Final Test** that mixes all its topics.

---

## 1. The whole map on one page

```
MONTH 1 — AI + Python Foundations 🐍          (you learn to talk to computers)
  01 Python fundamentals
  02 NumPy, Pandas & data handling
  03 APIs, JSON & Git/GitHub
  04 Machine learning basics
  05 Build 2–3 small projects
  ── Month1_Final_Test.md

MONTH 2 — LLMs + Generative AI 🧠              (you learn to use AI models)
  06 LLM fundamentals
  07 Prompt engineering
  08 LLM APIs
  09 Embeddings & vector databases
  10 RAG applications
  11 Build an AI-powered project
  ── Month2_Final_Test.md

MONTH 3 — AI Engineering + Agents ⚡           (you learn to build AI systems)
  12 AI agents & tool calling
  13 Agentic workflows
  14 LangChain / LangGraph
  15 AI automation
  16 Build and deploy a complete AI project
  17 Put your projects on GitHub + portfolio
  ── Month3_Final_Test.md
```

Why this order? Each month is a floor of a building:

| Floor | You can… | You need this because… |
|---|---|---|
| Month 1 | write Python, handle data, call web services, save your work with Git, understand what "learning from data" means | Every AI tool is used *through* Python code and data |
| Month 2 | send text to a large AI model, control its answers, and connect it to your own documents | This is the core skill of modern "AI engineering" |
| Month 3 | let the AI take actions, chain steps together, run on its own, and put it online | This is what companies actually hire for |

---

## 2. Week-by-week schedule (12 weeks)

Assumes about **2 hours a day, 6 days a week** (~12 hours/week). If you have less time, stretch each week to two; the order matters more than the speed.

### Month 1 — AI + Python Foundations

| Week | Topic folder | Daily rhythm | Done when… |
|---|---|---|---|
| 1 | `01_Python_Fundamentals` | Day 1–2: read lesson. Day 3–5: type every example yourself, do exercises. Day 6: quiz. | You can write a small program with lists, dicts, loops, functions and a file read, without looking things up every line. |
| 2 | `02_NumPy_Pandas_Data` | Day 1–2: read. Day 3–5: practise on a real CSV. Day 6: quiz. | You can load a CSV, clean it, group it and make a chart. |
| 3 | `03_APIs_JSON_Git` + `04_Machine_Learning_Basics` (first half) | Day 1–3: APIs/JSON/Git. Day 4–6: start ML. | All your code so far lives on GitHub. You've called a public API. |
| 4 | `04_Machine_Learning_Basics` (finish) + `05_Small_Projects` | Day 1–2: train & evaluate a model. Day 3–6: build projects. | 2–3 small projects on GitHub with READMEs. **Take `Month1_Final_Test.md`.** |

### Month 2 — LLMs + Generative AI

| Week | Topic folder | Done when… |
|---|---|---|
| 5 | `06_LLM_Fundamentals` + `07_Prompt_Engineering` | You can explain tokens, context window and temperature to a friend, and you've rewritten a bad prompt into a good one. |
| 6 | `08_LLM_APIs` | You've called an LLM from Python, streamed a reply, and got structured JSON back. |
| 7 | `09_Embeddings_Vector_Databases` + `10_RAG_Applications` (start) | You've stored documents in a vector database and searched them by meaning. |
| 8 | `10_RAG_Applications` (finish) + `11_AI_Powered_Project` | A working "chat with your documents" app on GitHub. **Take `Month2_Final_Test.md`.** |

### Month 3 — AI Engineering + Agents

| Week | Topic folder | Done when… |
|---|---|---|
| 9 | `12_AI_Agents_Tool_Calling` + `13_Agentic_Workflows` | You've written an agent loop by hand that uses at least two tools. |
| 10 | `14_LangChain_LangGraph` + `15_AI_Automation` | You've rebuilt your agent in LangGraph and automated one real task (e.g. a daily email summary). |
| 11 | `16_Build_and_Deploy` | Your capstone project has a public URL. |
| 12 | `17_GitHub_and_Portfolio` | Polished GitHub profile, pinned repos, a portfolio page, a demo video. **Take `Month3_Final_Test.md`.** |

---

## 3. How to study each topic (the loop)

```
 ┌─────────────┐   ┌──────────────┐   ┌───────────────┐   ┌────────────┐   ┌──────────────┐
 │ 1. READ the │──▶│ 2. TYPE every│──▶│ 3. DO the     │──▶│ 4. TAKE the│──▶│ 5. EXPLAIN it│
 │ lesson once │   │ code example │   │ exercises     │   │ quiz       │   │ out loud in  │
 │ fully       │   │ (no copy-    │   │ (struggle is  │   │ (score it  │   │ 2 minutes    │
 │             │   │ paste!)      │   │ the point)    │   │ honestly)  │   │ (Feynman)    │
 └─────────────┘   └──────────────┘   └───────────────┘   └────────────┘   └──────────────┘
                                                                │
                                         score < 70%? ──────────┘──▶ re-read sections you missed
```

**Scoring rule for every quiz:** 85%+ = move on. 70–84% = re-read the sections of the questions you missed, then move on. Below 70% = redo the lesson's "How it works" section and exercises, then retake in 2 days.

---

## 4. What to install before Week 1

| Tool | What it is (plain words) | Where |
|---|---|---|
| **Python 3.13 or 3.14** | The programming language. 3.14 is the current stable line (3.14.7 as of Aug 2026). | python.org/downloads |
| **VS Code** | A free text editor made for writing code | code.visualstudio.com |
| **uv** | A fast tool for installing Python packages and making isolated project folders. You'll meet it in Lesson 01. | docs.astral.sh/uv |
| **Git** | Saves versions of your code. Lesson 03. | git-scm.com |
| **GitHub account** | A website that stores your Git projects online. Lesson 03. | github.com |
| **An LLM API key** (Month 2) | A password that lets your code use an AI model. Lesson 08. | console.anthropic.com or platform.openai.com |

Don't worry if these words mean nothing yet. Each lesson explains its tools from zero.

**👉 Step-by-step install instructions** (macOS, Windows and Linux), the API-key and spending-limit walkthrough, Docker/Render/Node/Slack setup and a troubleshooting table are in **[`00_SETUP_Install_Guide.md`](00_SETUP_Install_Guide.md)**. Do its Steps 1–4 before Lesson 01. After that, **every lesson starts with a "🛠️ Setup for this lesson" box** listing exactly what to install and a command to check it works, and every practice file and final test has a short "🛠️ Before you start" note. To check your whole computer at once, run [`check_setup.py`](check_setup.py) (Setup Guide Section 14).

| Lesson | New things to install or sign up for |
|---|---|
| 01 | VS Code (+ Python extension), uv, Python 3.14 |
| 02 | numpy, pandas 3, matplotlib, Jupyter extension + ipykernel |
| 03 | Git, GitHub account, GitHub CLI (`gh`); requests, python-dotenv, pydantic |
| 04 | scikit-learn, joblib |
| 05 | pytest, ruff (+ Ruff extension), streamlit |
| 06–07 | A free chat assistant account; tiktoken |
| 08 | **Claude Console account, credit, spending limit, API key**; anthropic |
| 09 | sentence-transformers (PyTorch, ~2 GB disk), chromadb, rank-bm25; optional Voyage AI key |
| 10–11 | pypdf; optional Streamlit Community Cloud account |
| 12–13 | Nothing new (free weather/currency APIs need no key) |
| 14 | langchain 1.x, langchain-anthropic, langgraph 1.x (+ RAG extras); optional LangSmith account |
| 15 | feedparser, mcp 2.x, apscheduler, fastapi; **Node.js** (MCP Inspector); GitHub Actions secrets; optional Slack/Discord webhook |
| 16 | uvicorn, pydantic-settings, httpx; **Docker Desktop**, **Render** account, a separate production API key |
| 17 | A `<username>.github.io` repo (GitHub Pages), a screen recorder |

---

## 5. Progress tracker

Tick these off as you go (edit this file and change `[ ]` to `[x]`).

**Month 1**
- [ ] 01 Python lesson read · [ ] exercises · [ ] quiz ≥ 85%
- [ ] 02 NumPy/Pandas lesson · [ ] exercises · [ ] quiz
- [ ] 03 APIs/JSON/Git lesson · [ ] exercises · [ ] quiz
- [ ] 04 ML basics lesson · [ ] exercises · [ ] quiz
- [ ] 05 Project A · [ ] Project B · [ ] Project C (optional)
- [ ] Month 1 Final Test

**Month 2**
- [ ] 06 LLM fundamentals · [ ] 07 Prompt engineering · [ ] 08 LLM APIs
- [ ] 09 Embeddings & vector DBs · [ ] 10 RAG · [ ] 11 AI project shipped
- [ ] Month 2 Final Test

**Month 3**
- [ ] 12 Agents & tool calling · [ ] 13 Agentic workflows · [ ] 14 LangChain/LangGraph
- [ ] 15 AI automation · [ ] 16 Capstone deployed · [ ] 17 Portfolio live
- [ ] Month 3 Final Test

---

## 6. Things that changed recently (so you're not surprised by old tutorials)

Lots of YouTube videos and blog posts are out of date. Here's what's current as of October 2026:

| Area | What changed | What old tutorials will show you |
|---|---|---|
| Python packaging | **uv** has become the popular choice for beginners and pros | `pip install` + `python -m venv` (still works fine) |
| Pandas | **pandas 3.0** (Jan 2026): text columns get a real `str` type; "Copy-on-Write" is always on, so chained assignment like `df[df.a > 1]["b"] = 0` no longer works | `object` dtype for text; `SettingWithCopyWarning` |
| LangChain | **LangChain 1.0 / LangGraph 1.0** (Oct 2025): build agents with `create_agent`; old `AgentExecutor` and "chains" moved to `langchain-classic` | `initialize_agent`, `AgentExecutor`, `LLMChain` |
| OpenAI API | The **Responses API** is the main API for new work; the old Assistants API was retired Aug 26, 2026 | Assistants API, threads |
| Tools for agents | **MCP (Model Context Protocol)** is the common standard for plugging tools into AI apps; now run by the Linux Foundation's Agentic AI Foundation | Every framework had its own plug-in format |
| Models | Model names change every few months. Always check the provider's model list. | Old model names that no longer exist |

---

## 7. If you get stuck

1. Read the error message from the **bottom line up**. The last line says what went wrong.
2. Copy the last line of the error into a search engine.
3. Ask an AI assistant: paste the code, the full error, and what you expected.
4. Take a 10-minute walk. Seriously. Most "impossible" bugs are solved right after a break.
5. Lower the bar: get a smaller version working first, then grow it.

Now open `Month1_AI_Python_Foundations/01_Python_Fundamentals/lesson.md` and begin.
