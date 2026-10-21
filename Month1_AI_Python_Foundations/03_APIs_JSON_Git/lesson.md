# Lesson 03: APIs, JSON & Git/GitHub

*Month 1, Week 3 (first half). Reading time: about 70 minutes. Assumes Lessons 01–02.*

This lesson covers three tools that always show up together in real work:

- **APIs** let your program talk to other programs over the internet.
- **JSON** is the format those programs use to send data back and forth.
- **Git/GitHub** save every version of your code and share it with the world.

---

## 🛠️ Setup for this lesson

| You need | Why | How to get it |
|---|---|---|
| **Git** | Saves versions of your code | `xcode-select --install` (Mac) · `winget install --id Git.Git -e` (Windows) · Step 6 |
| **GitHub account** | Stores your code online; your future portfolio | github.com/signup (pick a professional username) |
| **GitHub CLI** (`gh`) | The easiest way to log in so `git push` works | `brew install gh` · `winget install --id GitHub.cli -e` |
| **requests**, **python-dotenv**, **pydantic**, **pandas** | Call APIs, load secrets from `.env`, validate JSON | `uv add` (below) |
| No API keys | The APIs used here are free and need no key | - |

**Install:**

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

**Check it works:**

```bash
git --version
gh auth status       # "Logged in to github.com"
uv run python -c "import requests; print(requests.get('https://api.github.com').status_code)"   # 200
```

Stuck? See the step-by-step instructions and the troubleshooting table in [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md).

---

## 1. The big picture

### What is this, in simple words?

So far your programs have lived alone on your computer, reading local files. Real software talks to other software: weather services, payment systems, maps, and (most importantly for us) **AI models**.

**API** stands for **Application Programming Interface**. That's a fancy name for **a menu of requests one program can make to another.**

Analogy: a restaurant. You (your program) don't walk into the kitchen (the other company's servers). You read the **menu** (the API documentation), tell the **waiter** your order in a set format (a request), and the waiter brings back your food (a response). You never need to know how the kitchen works.

**JSON** (JavaScript Object Notation, pronounced "JAY-son") is the most common way the food is packaged: a plain-text format that looks almost exactly like Python dicts and lists.

**Git** is a tool that takes snapshots of your project folder every time you say "save this version." **GitHub** is a website that stores those snapshots online so you can back them up, share them, and work with others.

Analogy for Git: the "save game" feature in a video game. You can always go back to an earlier save if something breaks. GitHub is like cloud saves, plus a public trophy shelf.

### Which field does it belong to?

APIs and JSON belong to **web development** and **software integration** (making systems work together). Git belongs to **software engineering practice**, specifically **version control**: tracking changes to files over time.

### Why does it matter?

| Topic | Why it matters for AI engineering |
|---|---|
| APIs | Every large language model (Month 2) is used through an API. Agents (Month 3) work by calling APIs. |
| JSON | AI APIs send and receive JSON. "Structured outputs" and "tool calling" are JSON. |
| Git/GitHub | Every employer looks at your GitHub. Every deployment (Lesson 16) starts from a Git repository. |

> **In simple words:** APIs let your code order data or services from other programs. JSON is the package format. Git saves versions of your code, and GitHub stores and shows them online. All three are daily tools for AI engineers.

---

## 2. Core concepts

### Part A: How the web works (just enough)

#### 2.1 Clients, servers and HTTP

The internet works by **requests** and **responses**:

- A **client** is the program asking for something (your browser, or your Python script).
- A **server** is a computer that waits for requests and answers them.
- **HTTP** (HyperText Transfer Protocol) is the agreed set of rules for how they talk. **HTTPS** is the secure, encrypted version: always use it.

```
   YOUR PYTHON SCRIPT (client)                          SERVER (e.g. weather service)
   ───────────────────────────    HTTP request  ────▶   ──────────────────────────────
   "GET me the weather for Pune"                         looks it up in its database
                                 ◀────  HTTP response
                                       status 200 + JSON data
```

#### 2.2 URLs and endpoints

A **URL** (web address) tells the request where to go:

```
https://api.open-meteo.com/v1/forecast?latitude=18.52&longitude=73.86&current=temperature_2m
└─┬──┘ └───────┬─────────┘└────┬─────┘└──────────────────────┬──────────────────────────────┘
scheme        host            path                    query parameters (key=value, joined by &)
```

An **endpoint** is one specific URL path an API offers for one job, like `/v1/forecast`. An API is a collection of endpoints. **Query parameters** (after `?`) are options you pass, like function arguments.

#### 2.3 HTTP methods: what you want to do

| Method | Means | Restaurant analogy | Example |
|---|---|---|---|
| **GET** | Read/fetch data | "Show me the menu" | Get the weather |
| **POST** | Send data / create something | "Place an order" | Send a prompt to an AI model |
| **PUT / PATCH** | Update something | "Change my order" | Update your profile |
| **DELETE** | Remove something | "Cancel my order" | Delete a file |

AI APIs mostly use **POST**, because you're *sending* your question in the request.

#### 2.4 Requests have parts

| Part | What it is | Example |
|---|---|---|
| **Method + URL** | What and where | `POST https://api.example.com/v1/messages` |
| **Headers** | Extra info, like labels on an envelope | `Content-Type: application/json`, your API key |
| **Body** | The actual data you send (for POST) | `{"prompt": "Hello"}` |

#### 2.5 Status codes: did it work?

Every response comes with a three-digit **status code**:

| Code | Meaning | What to do |
|---|---|---|
| **200** OK | Success | 🎉 Read the data |
| **201** Created | Success, something was created | 🎉 |
| **400** Bad Request | Your request is malformed | Check your parameters/body |
| **401** Unauthorized | Missing/wrong API key | Check your key |
| **403** Forbidden | Key is fine but you're not allowed | Check permissions/plan |
| **404** Not Found | Wrong URL | Check the endpoint |
| **429** Too Many Requests | You hit the **rate limit** | Wait and retry |
| **500 / 502 / 503** | Server's problem | Wait and retry |

Rule of thumb: **2xx = success, 4xx = your mistake, 5xx = their mistake.**

A **rate limit** is a cap on how many requests you may make in a period (e.g. 50 per minute). AI APIs all have them.

#### 2.6 Authentication and API keys

Most APIs need to know who you are, to bill you and prevent abuse. The usual method is an **API key**: a long secret string, like a password for your code. You send it in a header.

**Golden rule: never put an API key directly in your code, and never upload it to GitHub.** Bots scan GitHub constantly for leaked keys and can run up huge bills within minutes.

Instead, store keys in **environment variables**: named values stored by your operating system or terminal session, outside your code. The common pattern is a `.env` file:

```
# .env   (this file must NEVER be committed to Git)
WEATHER_API_KEY=abc123secret
```

```python
# uv add python-dotenv
import os
from dotenv import load_dotenv

load_dotenv()                                 # reads .env into environment variables
api_key = os.environ["WEATHER_API_KEY"]       # or os.getenv("WEATHER_API_KEY")
```

### Part B: JSON

#### 2.7 What JSON looks like

```json
{
  "city": "Pune",
  "temperature": 31.5,
  "is_raining": false,
  "forecast": [
    {"day": "Mon", "high": 32},
    {"day": "Tue", "high": 30}
  ],
  "alerts": null
}
```

It's just text, but structured. JSON has only a few building blocks, and each maps to a Python type:

| JSON | Python | Note |
|---|---|---|
| `{ }` object | `dict` | keys **must** be in double quotes |
| `[ ]` array | `list` | |
| `"text"` | `str` | **double quotes only** |
| `42`, `3.14` | `int`, `float` | |
| `true` / `false` | `True` / `False` | lowercase in JSON |
| `null` | `None` | |

#### 2.8 Converting between JSON and Python

- **Parsing** (also called **deserialising** or **decoding**): JSON text → Python objects.
- **Serialising** (**encoding**): Python objects → JSON text.

```python
import json

text = '{"name": "Asha", "skills": ["python", "ai"], "active": true}'
data = json.loads(text)          # "load string" → dict
print(data["skills"][0])         # python

back = json.dumps(data, indent=2)   # "dump string" → pretty JSON text
print(back)

# files
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
with open("data.json") as f:
    data = json.load(f)
```

Memory trick: the **s** in `loads`/`dumps` means **string**. Without the s, it works with **files**.

#### 2.9 Navigating nested JSON

API responses are often deeply nested. Walk into them one level at a time:

```python
response = {
  "results": [
    {"name": {"first": "Asha", "last": "K"}, "location": {"city": "Pune"}}
  ]
}
first_person = response["results"][0]
print(first_person["name"]["first"])          # Asha
print(first_person.get("email", "no email"))  # safe if missing
```

Tip: print with `json.dumps(obj, indent=2)` to see the structure clearly, then walk in step by step.

#### 2.10 JSON Schema (a peek ahead)

A **JSON Schema** is a description of what a JSON object *should* look like: which keys, which types, which are required. In Month 2 you'll give schemas to AI models so they reply in exactly the right shape, and in Month 3 every tool an agent uses is described by one. Python's **Pydantic** library lets you write schemas as classes:

```python
# uv add pydantic
from pydantic import BaseModel

class Weather(BaseModel):
    city: str
    temperature: float
    is_raining: bool

w = Weather.model_validate({"city": "Pune", "temperature": 31.5, "is_raining": False})
print(w.temperature)              # 31.5
print(Weather.model_json_schema())  # the JSON Schema, generated for you
```

If the data has the wrong shape, Pydantic raises a clear error. This **validation** step is how professionals avoid surprises.

### Part C: Calling APIs from Python

#### 2.11 The `requests` library

```bash
uv add requests
```

```python
import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": 18.52, "longitude": 73.86, "current": "temperature_2m"}

resp = requests.get(url, params=params, timeout=10)
print(resp.status_code)          # 200
data = resp.json()               # parse JSON body → dict
print(data["current"]["temperature_2m"])
```

A POST with a JSON body and a key in the header:

```python
resp = requests.post(
    "https://api.example.com/v1/items",
    headers={"Authorization": f"Bearer {api_key}"},
    json={"name": "notebook", "price": 3.5},     # json= serialises the dict for you
    timeout=10,
)
resp.raise_for_status()      # raise an error if status is 4xx/5xx
```

`timeout=10` means "give up after 10 seconds instead of waiting forever." Always set it.

#### 2.12 Handling failure gracefully: retries

Networks fail. Servers get busy. Good code expects this. For 429 and 5xx errors, wait and try again, waiting longer each time. This is called **exponential backoff** (wait 1s, then 2s, then 4s…).

```python
import time

def get_with_retry(url: str, params: dict, tries: int = 3) -> dict:
    for attempt in range(tries):
        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code in (429, 500, 502, 503):
                raise requests.HTTPError(f"retryable {resp.status_code}")
            resp.raise_for_status()
            return resp.json()
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
            if attempt == tries - 1:
                raise
            wait = 2 ** attempt
            print(f"Attempt {attempt + 1} failed ({e}); retrying in {wait}s")
            time.sleep(wait)
```

**Pagination:** APIs often return big results in **pages** (e.g. 100 items at a time). You request page 1, then page 2, etc., until there are no more. The docs say how (often a `page` or `cursor` parameter).

#### 2.13 SDKs

An **SDK** (Software Development Kit) is a package a company provides that wraps their API in friendly Python functions, so you don't build HTTP requests by hand. In Month 2 you'll use the `anthropic` and `openai` SDKs. Underneath, they're doing exactly what you just learned: HTTP POST requests with JSON bodies and API keys in headers.

#### 2.14 Reading API documentation

Every good API has **docs**. For any new API, look for these five things:

1. **Base URL** (e.g. `https://api.open-meteo.com/v1`)
2. **Authentication** (key? where does it go?)
3. **Endpoints** and their parameters
4. **Example request and response**
5. **Rate limits and errors**

### Part D: Git and GitHub

#### 2.15 Why version control?

Without it, you end up with `project_final.py`, `project_final_v2.py`, `project_REALLY_final.py`… With **Git**, you keep one set of files, and Git remembers every version.

| Git concept | Plain meaning | Video-game analogy |
|---|---|---|
| **Repository (repo)** | A project folder Git is tracking | A game save file |
| **Commit** | A saved snapshot, with a message describing it | A save point |
| **Staging area** | The "about to be saved" list | Choosing what to pack before saving |
| **Branch** | A parallel line of work | A side quest that doesn't affect the main story until you merge it |
| **Merge** | Combine a branch back into another | Bringing side-quest loot back to the main story |
| **Remote** | A copy of the repo on another computer (e.g. GitHub) | Cloud save |
| **Push / Pull** | Upload commits to / download commits from the remote | Sync to/from the cloud |
| **Clone** | Download a full copy of a remote repo | Copy someone's save to your console |

#### 2.16 The three areas of Git

```
  WORKING FOLDER          STAGING AREA            REPOSITORY (history)
  (your files as   git add  ("ready to   git commit  (saved snapshots)   git push   GitHub
   you edit them) ───────▶   save")    ────────────▶                  ─────────▶ (remote)
                                                                      ◀─────────
                                                                       git pull
```

#### 2.17 Everyday commands

One-time setup:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Starting and saving:

```bash
git init                     # turn the current folder into a repo
git status                   # what's changed? (run this constantly)
git add expense_tracker.py   # stage one file  (git add . stages everything)
git commit -m "Add expense tracker with category totals"
git log --oneline            # list of saved snapshots
git diff                     # show exact changes not yet staged
```

A good **commit message** says *what* and *why* in a short sentence: "Fix crash when price is missing", not "stuff" or "update".

#### 2.18 .gitignore: things Git should never save

A **`.gitignore`** file lists files and folders Git should ignore. **Create it before your first commit.**

```
# .gitignore
.env              # secrets!
.venv/            # your virtual environment (huge, rebuildable)
__pycache__/      # Python's temporary files
*.pyc
.DS_Store         # Mac junk
data/raw/         # large data files
.ipynb_checkpoints/
```

#### 2.19 GitHub: putting it online

1. Create a free account at github.com.
2. Click **New repository**, name it (e.g. `learn-ml`), don't add files.
3. Connect your local repo and push:

```bash
git remote add origin https://github.com/YOURNAME/learn-ml.git
git branch -M main
git push -u origin main
```

GitHub will ask you to log in. The easiest way is to install the **GitHub CLI** (`gh`) and run `gh auth login`, or set up an **SSH key** (a secure key pair so you don't type passwords).

Each time you finish some work after that:

```bash
git add .
git commit -m "Describe what changed"
git push
```

#### 2.20 Branches and pull requests

A **branch** lets you try something without risking the working version.

```bash
git switch -c add-charts      # create and move to a new branch
# ...edit, add, commit...
git push -u origin add-charts
```

On GitHub you then open a **pull request (PR)**: a request to merge your branch into `main`. Teams review code in PRs before merging. Even solo, PRs are a good habit.

A **merge conflict** happens when two branches changed the same lines differently. Git marks the spot with `<<<<<<<`, `=======` and `>>>>>>>`; you choose which version to keep, delete the markers, then `add` and `commit`.

#### 2.21 README files

A **README.md** is the front page of your repo. GitHub displays it automatically. It's written in **Markdown**: a simple way to format text using symbols (`# Heading`, `**bold**`, `- bullet`, triple backticks for code). This very lesson is written in Markdown.

> **In simple words:** A client sends an HTTP request (method + URL + headers + body) to a server and gets back a status code and usually JSON. Keep API keys in `.env`, never in code. JSON maps directly to Python dicts and lists. Git saves snapshots (add → commit → push); GitHub stores them online; `.gitignore` keeps secrets and junk out.

---

## 3. How it works: a real example, start to finish

**Goal:** build a small "weather report" tool that calls a real API, saves results as JSON, and publish it on GitHub properly. We'll use **Open-Meteo**, a free weather API that needs no key, so you can run it right now.

### Step 1: Create the project and repo

```bash
uv init weather-report && cd weather-report
uv add requests python-dotenv
git init
```

Create `.gitignore` (from section 2.18). Then make the first commit:

```bash
git add .
git commit -m "Initial project setup"
```

### Step 2: Read the docs

From open-meteo.com/en/docs we learn: base URL `https://api.open-meteo.com/v1/forecast`; parameters `latitude`, `longitude`, `current=temperature_2m,wind_speed_10m`, `daily=temperature_2m_max`; no key needed.

### Step 3: Make one request and look at the raw JSON

```python
# explore.py
import json, requests

resp = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={"latitude": 18.52, "longitude": 73.86,
            "current": "temperature_2m,wind_speed_10m",
            "daily": "temperature_2m_max", "timezone": "auto"},
    timeout=10,
)
print(resp.status_code)
print(json.dumps(resp.json(), indent=2)[:800])    # first 800 characters
```

You'll see something shaped like:

```json
{
  "latitude": 18.5,
  "current": {"time": "2026-10-20T10:00", "temperature_2m": 29.4, "wind_speed_10m": 8.1},
  "daily": {"time": ["2026-10-20", "2026-10-21"], "temperature_2m_max": [31.2, 30.5]}
}
```

### Step 4: Turn exploration into clean functions

```python
# weather.py
import json
import requests
from pydantic import BaseModel

CITIES = {"Pune": (18.52, 73.86), "Delhi": (28.61, 77.21), "London": (51.51, -0.13)}
URL = "https://api.open-meteo.com/v1/forecast"

class Report(BaseModel):
    city: str
    temperature_c: float
    wind_kmh: float
    max_next_days: list[float]

def fetch_weather(lat: float, lon: float) -> dict:
    resp = requests.get(URL, params={
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max", "timezone": "auto",
    }, timeout=10)
    resp.raise_for_status()
    return resp.json()

def to_report(city: str, raw: dict) -> Report:
    return Report(
        city=city,
        temperature_c=raw["current"]["temperature_2m"],
        wind_kmh=raw["current"]["wind_speed_10m"],
        max_next_days=raw["daily"]["temperature_2m_max"],
    )

def main():
    reports = []
    for city, (lat, lon) in CITIES.items():
        try:
            reports.append(to_report(city, fetch_weather(lat, lon)))
        except requests.RequestException as e:
            print(f"Skipping {city}: {e}")
    for r in reports:
        print(f"{r.city:<7} {r.temperature_c:5.1f}°C  wind {r.wind_kmh:4.1f} km/h")
    with open("reports.json", "w") as f:
        json.dump([r.model_dump() for r in reports], f, indent=2)

if __name__ == "__main__":
    main()
```

(Install Pydantic first: `uv add pydantic`.)

### Step 5: Load it into Pandas (connecting to Lesson 02)

```python
import pandas as pd
df = pd.read_json("reports.json")
print(df.sort_values("temperature_c", ascending=False))
```

### Step 6: Commit with a meaningful message

```bash
git status
git add weather.py pyproject.toml uv.lock .gitignore
git commit -m "Fetch current weather for 3 cities and save as JSON"
```

### Step 7: Write a README, then push to GitHub

```markdown
# Weather Report

Fetches current weather for several cities from the free Open-Meteo API
and saves a JSON report.

## Run it
    uv run weather.py

## What I learned
- Calling a REST API with query parameters
- Validating JSON with Pydantic
```

```bash
git add README.md && git commit -m "Add README"
gh repo create weather-report --public --source=. --push     # or the manual remote steps
```

### Step 8: Add a feature on a branch

```bash
git switch -c add-fahrenheit
# edit weather.py to also show °F …
git commit -am "Show temperatures in Fahrenheit too"
git push -u origin add-fahrenheit
# open a Pull Request on GitHub, review it, click Merge
git switch main && git pull
```

### The whole flow

```
 docs ─▶ explore raw JSON ─▶ functions + Pydantic validation ─▶ save JSON ─▶ Pandas
                                                                     │
 git init ─▶ .gitignore ─▶ commit ─▶ README ─▶ push to GitHub ─▶ branch ─▶ PR ─▶ merge
```

> **In simple words:** Read the docs, explore one raw response, turn it into clean functions that validate the JSON, save results, and commit at every working step. Push to GitHub with a README, and use branches for new features.

---

## 4. Key terms (in order)

| Term | Plain meaning |
|---|---|
| **API** | A menu of requests one program can make to another. |
| **JSON** | A text format for structured data, like Python dicts/lists. |
| **Git** | A tool that saves snapshots (versions) of your project. |
| **GitHub** | A website that stores Git repos online and shows them publicly. |
| **Version control** | Tracking changes to files over time. |
| **Client / server** | The asker / the answerer in a network conversation. |
| **HTTP / HTTPS** | The rules for web requests; HTTPS is the encrypted version. |
| **URL** | A web address. |
| **Endpoint** | One specific URL an API offers for one job. |
| **Query parameters** | `?key=value` options added to a URL. |
| **HTTP method** | The action: GET (read), POST (send/create), PUT/PATCH (update), DELETE. |
| **Headers** | Extra labelled info sent with a request (e.g. your key). |
| **Body** | The data sent in a request (for POST). |
| **Status code** | 3-digit result: 2xx success, 4xx your error, 5xx server error. |
| **Rate limit** | Max number of requests allowed per time period. |
| **API key** | A secret string identifying your code to an API. |
| **Environment variable / .env** | A value stored outside the code; `.env` is a file of them. |
| **Parse / serialise** | JSON text → Python / Python → JSON text. |
| **JSON Schema** | A description of the shape JSON must have. |
| **Pydantic / validation** | A library that checks data matches a schema / the act of checking. |
| **requests** | The popular Python library for making HTTP calls. |
| **Timeout** | Max time to wait for a response. |
| **Exponential backoff** | Retrying with waits that double each time. |
| **Pagination** | Getting big results one page at a time. |
| **SDK** | A company's Python package that wraps its API in friendly functions. |
| **Repository (repo)** | A folder tracked by Git. |
| **Commit** | A saved snapshot with a message. |
| **Staging area** | The list of changes chosen for the next commit. |
| **Branch / merge** | A parallel line of work / combining it back. |
| **Remote / push / pull / clone** | Online copy / upload / download changes / copy a whole repo. |
| **.gitignore** | List of files Git must ignore (secrets, junk). |
| **Pull request (PR)** | A request to merge a branch, with review. |
| **Merge conflict** | Two changes to the same lines; you choose which to keep. |
| **README / Markdown** | Repo front page / the simple text-formatting language it's written in. |

> **In simple words:** Requests have methods, URLs, headers and bodies; responses have status codes and JSON. Git work is add → commit → push, with branches and PRs for new features.

---

## 5. The people involved

| Who | What they do | Day to day |
|---|---|---|
| **API provider** (e.g. a weather company, Anthropic, OpenAI) | Builds and runs the API | Publishes docs, sets rate limits and prices, keeps servers running. |
| **API consumer** (you) | Calls the API from code | Reads docs, manages keys safely, handles errors and retries. |
| **Backend developer** | Builds servers and APIs | Designs endpoints and JSON shapes others will use. You'll do a little of this in Lesson 16 with FastAPI. |
| **Frontend developer** | Builds what users see | Calls APIs from web pages and apps to show data. |
| **DevOps / platform engineer** | Keeps systems deployed and healthy | Uses Git-based workflows to deploy automatically. |
| **Teammates / code reviewers** | Review your pull requests | Comment on your code, approve merges. |
| **Recruiters and hiring managers** | Decide who gets hired | Look at your GitHub profile and READMEs (Lesson 17). |
| **Open-source maintainers** | Run public projects on GitHub | Review PRs from strangers, which is how you can contribute. |
| **GitHub** (owned by Microsoft) | Hosts repos | Also provides Actions (automation), Codespaces (cloud coding), Copilot (AI coding help). |

> **In simple words:** Providers build APIs, you consume them; teams collaborate through GitHub pull requests; and employers read your GitHub like a CV.

---

## 6. Common misconceptions and beginner mistakes

| Mistake | Fix |
|---|---|
| Pasting your API key into code | Use `.env` + `os.getenv`; add `.env` to `.gitignore` **before the first commit**. |
| "I deleted the key from my code, so it's safe." | Git history still has it. **Revoke the key** on the provider's site and make a new one. |
| Not checking the status code | `resp.raise_for_status()` or check `resp.status_code` before using the data. |
| No timeout on requests | Always pass `timeout=`. |
| Assuming every key exists in the JSON | Use `.get()` or validate with Pydantic. |
| Single quotes in JSON | JSON requires double quotes. Use `json.dumps` instead of building JSON by hand. |
| Hammering an API in a loop | Respect rate limits; add `time.sleep` and backoff. |
| Thinking Git and GitHub are the same | Git is the tool on your computer; GitHub is one website that hosts Git repos (others: GitLab, Bitbucket). |
| Committing once a week | Commit small and often, after each thing that works. |
| Messages like "update" | Describe the change: "Add retry on 429 errors". |
| Committing `.venv/` or huge data files | Put them in `.gitignore`. |
| Panicking at a merge conflict | It's just two edits to the same lines. Pick one, remove the markers, commit. |
| "My GitHub must be perfect before I make it public." | Public and imperfect beats private and perfect. Show progress. |

> **In simple words:** Protect keys, check status codes, set timeouts, validate JSON, respect rate limits, and commit small and often with clear messages.

---

## 7. One-page recap

### The 10 things to remember

1. **An API is a menu**; your code orders through HTTP requests.
2. **Request = method + URL + headers + body. Response = status code + body (usually JSON).**
3. **GET reads, POST sends.** AI APIs mostly use POST.
4. **2xx good, 4xx your fault, 5xx their fault; 429 = slow down.**
5. **API keys live in `.env`, never in code or Git.** Leaked? Revoke immediately.
6. **JSON ≈ Python dicts and lists.** `json.loads`/`dumps` for strings, `load`/`dump` for files.
7. **Validate data with Pydantic**; schemas come back big in Months 2–3.
8. **Always use `timeout` and retry with backoff.**
9. **Git: `status` → `add` → `commit -m` → `push`.** `.gitignore` first.
10. **GitHub is your public portfolio.** Every project gets a README.

### Cheat sheet

```python
resp = requests.get(url, params={...}, headers={...}, timeout=10)
resp.raise_for_status(); data = resp.json()
requests.post(url, json={...}, headers={"Authorization": f"Bearer {key}"}, timeout=10)
json.loads(s) / json.dumps(obj, indent=2) / json.load(f) / json.dump(obj, f)
os.getenv("KEY") after load_dotenv()
```

```bash
git init | git status | git add . | git commit -m "msg" | git push
git switch -c branch | git pull | git log --oneline | git diff
```

### What to learn next

➡️ **Lesson 04: Machine Learning Basics.** You can now get, clean and store data. Next: teaching a computer to find patterns in that data and make predictions, the idea that all of modern AI grows out of.
