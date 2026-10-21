# Lesson 05: Build 2–3 Small Projects

*Month 1, Week 4. Reading time: about 50 minutes. Then 4–5 days of building. Assumes Lessons 01–04.*

---

## 🛠️ Setup for this lesson

| You need | Why | How to get it |
|---|---|---|
| Everything from Lessons 01–04 | uv, Python, Git, GitHub | Setup Guide Steps 1–6 |
| *Ruff* VS Code extension + `ruff` | Formats code and spots mistakes | Extensions panel; `uv add --dev ruff` |
| **pytest** | Runs your automated tests | `uv add --dev pytest` |
| **streamlit** | Turns a script into a web app (Projects B and C, optional for A) | `uv add streamlit` |
| **requests** / **scikit-learn** + **joblib** | Project B (live API data) / Project C (ML model) | `uv add` in that project |

**Install:**

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

**Check it works:**

```bash
uv run pytest            # "no tests ran" is fine before you write tests
uv run ruff check .
uv run python -c "import streamlit; print('streamlit', streamlit.__version__)"   # after uv add streamlit
```

Stuck? See the step-by-step instructions and the troubleshooting table in [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md).

---

## 1. The big picture

### What is this, in simple words?

A **project** is a small, complete program that solves one real problem from start to finish, that someone else could download and run.

So far you've done exercises: short pieces of practice, like scales on a piano. A project is playing a whole song. It's where the separate skills (Python, Pandas, APIs, Git, ML) finally join up.

### Which field does it belong to?

This is **software engineering practice**: the habits that turn "code that worked once on my laptop" into "software someone else can use." It's also the start of your **portfolio**: the public collection of work that shows employers what you can do (Lesson 17 polishes it).

### Why does it matter?

| Reason | Explanation |
|---|---|
| **Learning sticks** | You'll hit problems no tutorial covered. Solving them is where real learning happens. |
| **Proof of skill** | "I know Pandas" is a claim. A GitHub repo that cleans a real dataset is evidence. |
| **Confidence** | Finishing something complete changes how you see yourself: from "learner" to "builder." |
| **Foundation for Months 2–3** | Month 2's AI project and Month 3's deployed capstone reuse the same structure you set up now. |

> **In simple words:** Projects are complete mini-programs that join all your skills together. They're how you really learn and how you prove what you know.

---

## 2. Core concepts

### 2.1 Scope and the MVP

**Scope** means *how much* the project tries to do. Beginners almost always choose too much ("I'll build a full stock-trading AI!") and never finish.

The cure is the **MVP**, the **Minimum Viable Product**: the smallest version that genuinely works and is useful. Build it first, then add features.

Analogy: if the goal is "transport," the MVP is a skateboard, then a scooter, then a bicycle, then a car. Each stage is a usable vehicle. Building a car's wheels first gives you nothing to ride for months.

```
 ❌ wheel → axle → chassis → engine → car     (nothing usable until the very end)
 ✅ skateboard → scooter → bike → motorbike → car   (usable at every step)
```

A good beginner project is **finishable in 1–2 days** for the MVP.

### 2.2 Requirements

**Requirements** are a short list of what the program must do, written *before* coding. Write them as user-facing statements:

- "The user can load a CSV of bank transactions."
- "The program shows total spending per category."
- "The program saves a chart as PNG."

Split them into **must-have** (MVP) and **nice-to-have** (later). This list becomes your to-do list and part of your README.

### 2.3 Project structure

A tidy folder makes a project easy to understand. A standard layout:

```
expense-analyzer/
├── README.md            ← front page: what, why, how to run
├── pyproject.toml       ← project info + dependency list (created by uv)
├── uv.lock              ← exact versions, so others get the same setup
├── .gitignore
├── .env.example         ← shows WHICH env variables are needed (no real secrets)
├── data/
│   └── sample.csv       ← small example data so anyone can try it
├── src/
│   └── expense_analyzer/
│       ├── __init__.py  ← marks the folder as a Python package
│       ├── loader.py    ← reading & cleaning
│       ├── analysis.py  ← calculations
│       └── cli.py       ← the command-line interface
└── tests/
    └── test_analysis.py ← automated tests
```

The principle is **separation of concerns**: each file has one job. Loading code doesn't know about charts; chart code doesn't know about files.

**Dependencies** are the packages your project needs. With uv they're listed in `pyproject.toml` automatically when you `uv add`. Anyone can recreate your environment with `uv sync`. (Older projects use a `requirements.txt` file instead; `uv pip compile` or `uv export` can produce one if needed.)

### 2.4 Interfaces: how people use your program

An **interface** is how a user interacts with your program. Three beginner-friendly options:

| Interface | What it is | Good for | Tool |
|---|---|---|---|
| **Script** | Edit a setting at the top, run the file | Quick personal tools | plain Python |
| **CLI** (Command-Line Interface) | Run with options in the terminal: `uv run analyze --file bank.csv --month 2026-09` | Tools for developers | `argparse` (built in) or `typer` |
| **Web app** | A page in the browser with buttons and charts | Showing non-programmers | **Streamlit** (turns a Python script into a web app) |

Streamlit in 6 lines:

```python
# app.py   (uv add streamlit, then: uv run streamlit run app.py)
import streamlit as st
import pandas as pd

st.title("Expense Analyzer")
file = st.file_uploader("Upload your CSV")
if file:
    df = pd.read_csv(file)
    st.bar_chart(df.groupby("category")["amount"].sum())
```

### 2.5 Testing

A **test** is a small piece of code that checks your code gives the right answer. **Automated tests** run with one command, so you know instantly if a change broke something.

**pytest** is the standard Python testing tool. A test is just a function whose name starts with `test_` and uses `assert` (which means "this must be true, or fail"):

```python
# tests/test_analysis.py
from expense_analyzer.analysis import totals_by_category
import pandas as pd

def test_totals_by_category():
    df = pd.DataFrame({"category": ["food", "food", "bus"], "amount": [2.0, 3.0, 1.5]})
    result = totals_by_category(df)
    assert result["food"] == 5.0
    assert result["bus"] == 1.5
```

```bash
uv add --dev pytest
uv run pytest
```

`--dev` means "only needed while developing, not by users."

What to test: the core calculations, edge cases (empty file, missing values), and bugs you've fixed (so they never return).

### 2.6 Logging and error messages

**Logging** means recording what your program is doing, for debugging. It's better than scattered `print()` calls because you can turn detail levels up or down.

```python
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info("Loaded %d rows", len(df))
log.warning("Dropped %d rows with missing amounts", dropped)
```

Error messages for users should say **what went wrong and what to do**: "Couldn't find `bank.csv`. Check the path or run with `--file`." is far better than a raw traceback.

### 2.7 Code quality basics

| Habit | Why | Tool |
|---|---|---|
| Consistent formatting | Easy to read | **Ruff** (`uv add --dev ruff`, then `uv run ruff format .`) |
| Catch common bugs automatically | Finds unused imports, typos | `uv run ruff check .` (a **linter**: a tool that flags suspicious code) |
| Small functions with clear names | Easy to test and change | Your judgement |
| Type hints and docstrings | Self-documenting | You learned these in Lesson 01 |
| No hard-coded file paths | Works on others' computers | Use `pathlib.Path` and CLI options |

### 2.8 The README

The README is the most important file for anyone visiting your project. A good one has:

1. **Title + one-line description**
2. **Screenshot or example output** (people decide in 5 seconds)
3. **Features**
4. **How to install and run** (exact commands that actually work)
5. **How it works** (a short explanation, maybe a diagram)
6. **What I learned / challenges**
7. **Next steps** (what you'd add)

### 2.9 Iteration: the build loop

Projects aren't written top to bottom. You **iterate**: repeat a small loop many times.

```
   ┌──▶ pick the next smallest requirement
   │         │
   │         ▼
   │    write a little code ──▶ run it ──▶ broken? ──yes──▶ read error, fix
   │                                │no
   │                                ▼
   │                      (add a test) → git commit
   └────────────────────────────────┘
```

**Debugging** is the process of finding and fixing problems ("bugs"). Core debugging moves: read the error's last line, print the values just before the crash, shrink the problem to the smallest example that fails, and use VS Code's **debugger** (click left of a line number to set a **breakpoint**: a spot where the program pauses so you can inspect every variable).

### 2.10 Using AI assistants while learning

AI coding assistants (Claude, ChatGPT, GitHub Copilot, Cursor) are now normal at work. For *learning*, use them wisely:

| ✅ Good uses | ❌ Harmful uses (while learning) |
|---|---|
| "Explain this error to me." | "Write the whole project for me." |
| "Why is my approach slow?" | Pasting code you don't understand |
| "Review my function; what could be cleaner?" | Skipping the struggle every time |
| "Give me a hint, not the answer." | Not testing what it gives you |

Rule: **never commit code you can't explain line by line.** Interviewers will ask.

> **In simple words:** Pick a small scope and build an MVP first. Write requirements, use a clean folder structure, choose a simple interface (script, CLI or Streamlit), add a few pytest tests, log sensibly, write a great README, and iterate in small commit-sized steps.

---

## 3. How it works: building Project A start to finish

We'll build **Project A: Personal Expense Analyzer** together. Projects B and C are specified in `practice_and_test.md` for you to build yourself.

### Step 1: Requirements (10 minutes, on paper)

**Problem:** "I don't know where my money goes each month."

| Must-have (MVP) | Nice-to-have |
|---|---|
| Load a CSV of transactions (date, description, amount) | Auto-categorise using keywords |
| Clean it (types, duplicates, missing values) | Streamlit web version |
| Total per category and per month | Budget alerts |
| Save a bar chart PNG | Export a monthly PDF report |
| Command-line options for file and month | |

### Step 2: Set up

```bash
uv init --package expense-analyzer && cd expense-analyzer
uv add pandas matplotlib
uv add --dev pytest ruff
git init
```

`--package` creates the `src/expense_analyzer/` layout for you. Add a `.gitignore` (Lesson 03) and commit: `git commit -am "Project skeleton"` (after `git add .`).

### Step 3: Sample data

`data/sample.csv`:

```
date,description,amount,category
2026-09-01,Coffee shop,3.50,food
2026-09-01,Metro card,20.00,transport
2026-09-03,Supermarket,45.20,food
2026-09-05,Netflix,9.99,
2026-09-05,Netflix,9.99,
2026-09-10,Pharmacy,12.00,health
2026-10-02,Coffee shop,3.80,food
2026-10-04,Train ticket,15.00,transport
```

Note the deliberate mess: a missing category and a duplicate row.

### Step 4: Loader (one job: read and clean)

```python
# src/expense_analyzer/loader.py
from pathlib import Path
import logging
import pandas as pd

log = logging.getLogger(__name__)
REQUIRED = {"date", "description", "amount"}

def load_transactions(path: Path) -> pd.DataFrame:
    """Read a transactions CSV and return a clean DataFrame."""
    if not path.exists():
        raise FileNotFoundError(f"Couldn't find {path}. Check the path or use --file.")
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing columns: {', '.join(sorted(missing))}")

    before = len(df)
    df = df.drop_duplicates()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date", "amount"])
    if "category" not in df.columns:
        df["category"] = "uncategorised"
    df["category"] = df["category"].fillna("uncategorised").str.strip().str.lower()
    log.info("Loaded %d rows (%d removed while cleaning)", len(df), before - len(df))
    return df
```

Run a quick check in the terminal: `uv run python -c "from pathlib import Path; from expense_analyzer.loader import load_transactions; print(load_transactions(Path('data/sample.csv')))"`. Works? **Commit.**

### Step 5: Analysis (one job: calculate)

```python
# src/expense_analyzer/analysis.py
import pandas as pd

def filter_month(df: pd.DataFrame, month: str | None) -> pd.DataFrame:
    """Keep rows from one month like '2026-09'; None keeps everything."""
    if month is None:
        return df
    return df[df["date"].dt.strftime("%Y-%m") == month]

def totals_by_category(df: pd.DataFrame) -> pd.Series:
    return df.groupby("category")["amount"].sum().sort_values(ascending=False)

def totals_by_month(df: pd.DataFrame) -> pd.Series:
    return df.groupby(df["date"].dt.strftime("%Y-%m"))["amount"].sum()
```

### Step 6: Tests

```python
# tests/test_analysis.py
import pandas as pd
from expense_analyzer.analysis import totals_by_category, filter_month

def make_df():
    return pd.DataFrame({
        "date": pd.to_datetime(["2026-09-01", "2026-09-02", "2026-10-01"]),
        "amount": [2.0, 3.0, 4.0],
        "category": ["food", "food", "bus"],
    })

def test_totals_by_category():
    t = totals_by_category(make_df())
    assert t["food"] == 5.0 and t["bus"] == 4.0

def test_filter_month_keeps_only_that_month():
    assert len(filter_month(make_df(), "2026-09")) == 2

def test_filter_month_none_keeps_all():
    assert len(filter_month(make_df(), None)) == 3
```

`uv run pytest` → 3 passed. **Commit.**

### Step 7: CLI (one job: talk to the user)

```python
# src/expense_analyzer/cli.py
import argparse, logging
from pathlib import Path
import matplotlib.pyplot as plt
from .loader import load_transactions
from .analysis import filter_month, totals_by_category, totals_by_month

def main():
    parser = argparse.ArgumentParser(description="Analyse your spending.")
    parser.add_argument("--file", type=Path, default=Path("data/sample.csv"))
    parser.add_argument("--month", help="e.g. 2026-09 (default: all months)")
    parser.add_argument("--chart", type=Path, default=Path("spending.png"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    try:
        df = filter_month(load_transactions(args.file), args.month)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise SystemExit(1)

    if df.empty:
        print("No transactions found for that selection.")
        return

    cats = totals_by_category(df)
    print("\nSpending by category:\n", cats.to_string())
    print("\nSpending by month:\n", totals_by_month(df).to_string())
    print(f"\nTotal: {df['amount'].sum():.2f}")

    cats.plot(kind="bar", title=f"Spending by category ({args.month or 'all'})")
    plt.tight_layout(); plt.savefig(args.chart)
    print(f"Chart saved to {args.chart}")
```

Register the command in `pyproject.toml`:

```toml
[project.scripts]
analyze = "expense_analyzer.cli:main"
```

Now run: `uv run analyze --month 2026-09`. **Commit.**

### Step 8: README, polish, push

Write the README (section 2.8 checklist) with the chart screenshot. Run `uv run ruff format . && uv run ruff check .`. Push to GitHub.

### Step 9: One nice-to-have

Add keyword auto-categorisation: a dict like `{"coffee": "food", "metro": "transport"}`; when category is missing, check the description. Write a test for it first, then the code. **Commit.**

### What you just practised

```
 requirements ─▶ skeleton + git ─▶ sample data ─▶ loader ─▶ analysis ─▶ tests ─▶ CLI ─▶ README ─▶ push
       (scope)       (structure)                  └──── one job per file ────┘   (interface) (portfolio)
                         every arrow = run it + commit
```

> **In simple words:** Write requirements, set up the skeleton, add sample data, then build one small file at a time (loader → analysis → tests → CLI), committing after each working step, and finish with a README and a push.

---

## 4. Key terms (in order)

| Term | Plain meaning |
|---|---|
| **Project** | A small, complete program that solves one real problem. |
| **Portfolio** | Your public collection of projects. |
| **Scope** | How much the project tries to do. |
| **MVP** | Minimum Viable Product: the smallest version that works and is useful. |
| **Requirements** | A list of what the program must do. |
| **Must-have / nice-to-have** | MVP features / later features. |
| **Project structure** | How files and folders are organised. |
| **Separation of concerns** | Each file/function has one job. |
| **Dependencies** | Packages your project needs. |
| **pyproject.toml / uv.lock** | Project info and dependency list / exact pinned versions. |
| **requirements.txt** | Older-style dependency list file. |
| **.env.example** | Template showing needed environment variables, with no real secrets. |
| **Interface** | How a user interacts with your program. |
| **CLI** | A program used from the terminal with options. |
| **argparse** | Python's built-in tool for CLI options. |
| **Streamlit** | Library that turns a Python script into a simple web app. |
| **Test / automated test** | Code that checks your code's results, run with one command. |
| **pytest / assert** | Python's testing tool / "this must be true." |
| **Edge case** | An unusual input (empty, missing, huge) that might break things. |
| **Logging** | Recording what the program does, with levels (INFO, WARNING…). |
| **Formatter / linter / Ruff** | Tool that tidies code / flags suspicious code / a fast tool doing both. |
| **Iteration** | Repeating small build-run-fix-commit loops. |
| **Bug / debugging** | A mistake in code / finding and fixing it. |
| **Debugger / breakpoint** | Tool to pause and inspect a running program / the pause point. |
| **AI coding assistant** | An AI tool that explains, reviews or writes code. |

> **In simple words:** MVP, requirements, structure, interface, tests, README: the six words that turn code into a project.

---

## 5. The people involved

| Who | Role | What projects mean for them |
|---|---|---|
| **You** | Builder | Each project = new skills + portfolio evidence. |
| **Users** | People who run your program | Need clear instructions, sample data and friendly errors. Even if the only user is you in 3 months! |
| **Hiring managers / recruiters** | Decide on interviews | Spend ~1–2 minutes per GitHub repo: README, screenshot, clean structure, tests. |
| **Technical interviewers** | Test your understanding | Ask "walk me through this project" and "why did you choose X?" |
| **Mentors / peers / online communities** | Give feedback | Reddit r/learnpython, Discord servers, local meetups: share your projects for review. |
| **Open-source authors** | Wrote the libraries you use | You may file issues or small fixes later; a great portfolio item. |

> **In simple words:** Your projects serve users first, then reviewers and employers. Write them so a stranger can understand and run them.

---

## 6. Common misconceptions and beginner mistakes

| Mistake | Fix |
|---|---|
| Choosing a giant first project | Pick something finishable in a weekend. Grow it later. |
| "Tutorial projects" copied line by line | Change something meaningful: your own data, a new feature, a different question. |
| Waiting until it's perfect to push | Push the MVP. Commit history showing progress is a plus. |
| No README, or README says only "my project" | Use the 7-part checklist. Add a screenshot. |
| "It works on my machine." | Test from a fresh clone: `git clone …`, `uv sync`, run. |
| Hard-coded paths like `/Users/me/Desktop/data.csv` | Use relative paths and CLI options. |
| Secrets in the repo | `.env` + `.gitignore` + `.env.example`. |
| No tests at all | Even 3 tests on core functions show professionalism. |
| One 500-line file | Split by responsibility. |
| Letting an AI write it all | You won't learn, and you won't survive the interview. Ask for hints and reviews. |
| Abandoning when stuck | Shrink the problem. Ask for help. Take a break. Finishing is the skill. |

> **In simple words:** Small, finished, documented and tested beats big, perfect and never shipped.

---

## 7. One-page recap

### The 10 things to remember

1. **A project solves one real problem end to end.**
2. **Start with an MVP** (skateboard before car).
3. **Write requirements first;** split must-have vs nice-to-have.
4. **One job per file:** loader, analysis, interface.
5. **Pick a simple interface:** script, CLI (`argparse`) or Streamlit.
6. **Add a few pytest tests** for core logic and edge cases.
7. **Friendly errors and logging** instead of raw tracebacks and stray prints.
8. **Commit after every working step;** push early.
9. **README with screenshot + exact run commands.**
10. **Never commit code you can't explain.**

### Your Month 1 project set

| Project | Skills shown | Spec |
|---|---|---|
| **A. Personal Expense Analyzer** | Python, Pandas, CLI, tests, charts | Walked through above |
| **B. Live Data Dashboard** (API → Pandas → Streamlit) | APIs, JSON, Pydantic, Streamlit | `practice_and_test.md` |
| **C. ML Predictor App** | scikit-learn pipeline, evaluation, saved model, Streamlit | `practice_and_test.md` |

Do A and B for sure; C if time allows (it's excellent prep for Month 2).

### What to learn next

➡️ **Take `Month1_Final_Test.md`**, then start **Month 2, Lesson 06: LLM Fundamentals**: what large language models are and how they work under the hood.
