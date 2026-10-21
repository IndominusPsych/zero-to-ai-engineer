# SETUP: Install Everything You Need for the Course

*Read this after `00_START_HERE_Master_Plan.md` and before Lesson 01. Checked October 2026 on macOS, with Windows and Linux commands included. Every package in this course was installed together on Python 3.14.7 and checked with `check_setup.py`.*

You don't need to install everything on day one. Section 1 shows what each week needs. **Do Steps 1–4 before Lesson 01.** Do the rest when a lesson's "🛠️ Setup for this lesson" box tells you to.

---

## 0. A few words first

- **Terminal** (also called the command line or shell) is a window where you type commands instead of clicking.
  - **macOS:** press `Cmd + Space`, type *Terminal*, press Enter.
  - **Windows:** press Start, type *PowerShell*, open it. (Windows Terminal is the nicer app around it.)
  - **Linux:** `Ctrl + Alt + T` on most systems.
- **Command:** a line you type into the terminal and run with Enter. In this guide, commands sit in grey boxes. Don't type the `#` comments; they're notes for you.
- **Install:** copying a program onto your computer so you can use it.
- **PATH:** the list of folders where your terminal looks for programs. If you get "command not found" right after installing something, **close the terminal and open a new one**. That reloads the PATH and fixes most problems.

- **Windows users, one important note:** a few commands in this course create small files with `echo`, `printf` or `touch` (for example `.env`, `.gitignore`, `hello.py`). Those are Mac/Linux commands. In Windows PowerShell, **create those files in VS Code instead** (File → New File, paste the line, save with the exact name), because PowerShell's `echo ... > file` can save in an encoding Python can't read. Every other command (`uv`, `git`, `gh`, `docker`, `npx`) works the same on Windows.

**In simple words:** you'll type a few commands into a text window. If a new command "isn't found", open a fresh window.

---

## 1. What each part of the course needs

| When | Tool / account | Why | Cost | Step |
|---|---|---|---|---|
| Before Lesson 01 | **VS Code** | The editor where you write code | Free | 1 |
| Before Lesson 01 | **uv** (and Python 3.14 through it) | Installs Python and packages; makes project folders | Free | 2–3 |
| Before Lesson 01 | A `ai-engineer-projects` folder | One tidy place for all your code | Free | 4 |
| Lesson 02 | Jupyter support in VS Code | Run code in small cells and see tables and charts inline | Free | 5 |
| Lesson 03 | **Git** + **GitHub account** (+ optional `gh`) | Save versions of your code and publish it | Free | 6 |
| Lesson 06–07 | A chat assistant (Claude.ai, ChatGPT or Gemini) | Experiments with prompts | Free tier is enough | 7 |
| Lesson 08 onwards | **Claude API key** + a spending limit | Lets your code call an LLM | Pay as you go; **about $5–15 for the whole course** | 8 |
| Lesson 09 | ~2 GB of free disk space | Embedding models + PyTorch download on first use | Free | 9 |
| Lesson 15 | **Node.js** (for the MCP Inspector) | Test MCP servers in your browser | Free | 10 |
| Lesson 15 | Slack or Discord workspace (optional) | Receive automated messages via a webhook | Free | 11 |
| Lesson 16 | **Docker Desktop** (optional but recommended) + **Render** account | Package and deploy your app | Free tiers | 12 |
| Lesson 17 | GitHub Pages | Free portfolio website | Free | 13 |

**Computer:** any Mac (Apple Silicon or Intel), Windows 10/11 or Linux laptop from the last ~7 years. 8 GB RAM is enough; 16 GB is more comfortable for Lesson 09 onwards. You don't need a GPU anywhere in this course.

**In simple words:** four free installs on day one, an API key in Month 2, and a few optional extras in Month 3.

---

## Step 1: Install VS Code (the code editor)

1. Download it from **code.visualstudio.com** and install it like any app.
   - macOS alternative: `brew install --cask visual-studio-code` (if you use Homebrew, a package manager for Mac).
   - Windows alternative: `winget install -e --id Microsoft.VisualStudioCode`
2. Open VS Code, click the **Extensions** icon (four squares) on the left, and install:
   - **Python** (by Microsoft): runs and checks Python code.
   - **Jupyter** (by Microsoft): notebooks, for Lesson 02 onwards.
   - **Ruff** (by Astral): tidies your code and spots mistakes, for Lesson 05 onwards.
   - **Markdown Preview Mermaid Support** (by Matt Bierner): draws the diagrams in the course files.
   - **Markdown All in One** (by Yu Zhang): handy shortcuts and a clickable table of contents.
   - Optional: **Docker** (by Microsoft) for Lesson 16.

   Shortcut: when you open this course folder in VS Code, a pop-up offers to install the recommended extensions. Click **Install** (they're listed in `.vscode/extensions.json`).
3. **Read the lessons in preview mode.** The course files are Markdown (`.md`): plain text with symbols like `#` and `|` that turn into headings and tables. Open a file and press `Cmd+Shift+V` (Mac) or `Ctrl+Shift+V` (Windows/Linux) to see it formatted. The [README's "How to read this course" section](README.md#-how-to-read-this-course) has all the preview tips.
4. Turn on the `code` command so you can open folders from the terminal:
   - macOS: in VS Code press `Cmd+Shift+P`, type *Shell Command: Install 'code' command in PATH*, press Enter.
   - Windows/Linux: it's set up by the installer.

Check it works: in a **new** terminal, type `code --version`.

---

## Step 2: Install uv (installs Python and packages)

**uv** is a free tool that downloads Python for you, makes a private "box" of packages for each project, and installs packages very fast. Lesson 01 Section 2.2 explains it properly.

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or, on a Mac with Homebrew:
brew install uv
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# or:
winget install --id=astral-sh.uv -e
```

Close the terminal, open a new one, and check:

```bash
uv --version        # e.g. uv 0.12.x
```

Later, keep it up to date with `uv self update` (or `brew upgrade uv` if you used Homebrew).

---

## Step 3: Install Python with uv

```bash
uv python install 3.14
uv run --python 3.14 python --version     # should print Python 3.14.x
```

Notes:

- **Python 3.14** is the current version and every package in this course works with it. **Python 3.13** also works perfectly. Avoid 3.11 and older, because some current packages (like pandas 3.0) need newer Python.
- Your Mac may already have an old `python3` (3.9) from Apple. **Ignore it.** Always run code with `uv run`, which uses the right version.
- **Windows:** don't use the "python" entry from the Microsoft Store. uv handles Python for you.
- Prefer the classic installer? Download it from **python.org/downloads** and, on Windows, **tick "Add python.exe to PATH"** in the installer. uv will find it.

---

## Step 4: Make your course folder

Keep all your practice code in one place, separate from these lesson files:

```bash
# macOS / Linux
mkdir -p ~/ai-engineer-projects && cd ~/ai-engineer-projects
code .
```

```powershell
# Windows
mkdir $HOME\ai-engineer-projects; cd $HOME\ai-engineer-projects
code .
```

Each lesson asks you to create a project inside it with `uv init <name>`, for example `uv init python_practice`. A project is a folder containing your code, a `pyproject.toml` file (the list of packages it needs) and a hidden `.venv` folder (the private box where they're installed). Recent uv versions also add a `src/` folder; older ones add a `main.py` instead. Either is fine: you'll create your own `.py` files next to them.

**Your first test:**

```bash
uv init hello && cd hello
echo 'print("Hello, I am ready!")' > hello.py
uv run hello.py                # prints: Hello, I am ready!
```

If that prints the message, **you're ready for Lesson 01.** 🎉

---

## Step 5: Jupyter notebooks (Lesson 02)

A **notebook** (`.ipynb` file) lets you run code in small blocks ("cells") and see tables and charts underneath each one. It's great for exploring data.

Inside any project folder:

```bash
uv add --dev ipykernel
```

Then in VS Code: create `explore.ipynb`, click **Select Kernel** (top right) → **Python Environments** → choose the one inside your project's `.venv`. Type `1 + 1` in a cell and press `Shift+Enter`.

Prefer the classic browser version? `uv run --with jupyter jupyter lab`

---

## Step 6: Git, GitHub and the GitHub CLI (Lesson 03)

**Git** saves versions of your code on your computer. **GitHub** is a website that stores those versions online. Lesson 03 Section 2 explains both.

**1. Install Git**

| System | Command |
|---|---|
| macOS | `xcode-select --install` (installs Apple's Git), or `brew install git` |
| Windows | `winget install --id Git.Git -e`, or the installer from git-scm.com (the default options are fine) |
| Ubuntu/Debian | `sudo apt install git` |

Check it: `git --version`

**2. Tell Git who you are** (once per computer; use the email you'll sign up to GitHub with):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

**3. Create a GitHub account** at **github.com/signup**. Pick a professional username, because it will appear in your portfolio (Lesson 17). Turn on two-factor authentication under Settings → Password and authentication.

**4. Install the GitHub CLI and log in** (the easiest way to let your computer push code to GitHub):

| System | Command |
|---|---|
| macOS | `brew install gh` |
| Windows | `winget install --id GitHub.cli -e` |
| Linux | see cli.github.com |

```bash
gh auth login      # choose: GitHub.com → HTTPS → Yes (authenticate Git) → Login with a web browser
gh auth status     # should say "Logged in to github.com"
```

Prefer not to use `gh`? An SSH key works too (docs.github.com → "Connecting to GitHub with SSH").

---

## Step 7: A chat assistant (Lessons 06–07)

Make a free account on any of **claude.ai**, **chatgpt.com** or **gemini.google.com**. These lessons use them for prompt experiments, no code needed.

---

## Step 8: Your Claude API key (Lesson 08 onwards)

An **API key** is a secret password that lets your code use the model and puts the cost on your account. Lesson 08 explains APIs and keys in full.

1. Go to **platform.claude.com** (the Claude Console; the old address console.anthropic.com takes you there) and sign up.
2. **Billing:** add a payment method and buy a small amount of credit (**$5–10** is plenty to start).
3. **Set a spending limit** under Settings → Limits (for example $10/month). Then a bug can't cost you more than that.
4. **API Keys → Create Key.** Name it `zero-to-ai-engineer-laptop`. **Copy it now**: it starts with `sk-ant-` and you can only see it once.
5. In each project that calls the API, create a file called `.env`:

   ```bash
   echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
   printf ".env\n.venv/\n__pycache__/\n" >> .gitignore
   ```

   The second line makes sure Git never uploads your key. **Never paste your key into code, a chat, a screenshot or GitHub.** If it leaks, delete it in the Console and create a new one.

6. Test it (from a project folder with `.env`):

   ```bash
   uv add anthropic python-dotenv
   uv run python -c "from dotenv import load_dotenv; load_dotenv(); import anthropic; print(anthropic.Anthropic().messages.create(model='claude-haiku-5-5', max_tokens=20, messages=[{'role':'user','content':'Say hi'}]).content[0].text)"
   ```

   Seeing a greeting means it works. That test cost a fraction of a cent.

**Cost guide:** Lessons 08–17 plus the Month 2 and Month 3 tests usually come to **$5–15 in total**. To save money while experimenting, use `claude-haiku-5-5` (the cheapest model) and switch to `claude-opus-5-5` when you want the best quality. Lesson 08 explains pricing and token counting.

**Using OpenAI or Gemini instead?** That's fine. Get a key from platform.openai.com or aistudio.google.com, run `uv add openai` (or `google-genai`), and translate the calls with the provider's docs. The ideas in every lesson are the same.

---

## Step 9: Disk space for embeddings (Lesson 09)

`sentence-transformers` installs **PyTorch**, a big machine-learning library (~1 GB). The first time you run Lesson 09's code it also downloads the `all-MiniLM-L6-v2` model (~90 MB) and keeps it in a cache folder. Make sure you have **~2 GB free**, use a decent internet connection, and expect the first `uv add` to take a minute or two. It runs fine without a GPU.

---

## Step 10: Node.js (Lesson 15, for the MCP Inspector)

**Node.js** runs JavaScript programs outside a browser. You only need it for the **MCP Inspector**, a web page for testing the tool servers you build in Lesson 15. `npx` comes with Node and runs a tool without installing it permanently.

| System | Command |
|---|---|
| macOS | `brew install node` |
| Windows | `winget install OpenJS.NodeJS.LTS` |
| Any | the **LTS** installer from nodejs.org |

Check: `node --version` and `npx --version`.

---

## Step 11: Slack or Discord webhook (Lesson 15, optional)

A **webhook URL** is a secret web address. Anything sent to it appears as a message in your channel.

- **Slack:** create a free workspace at slack.com → api.slack.com/apps → *Create New App* → *From scratch* → **Incoming Webhooks** → turn it on → *Add New Webhook to Workspace* → pick a channel → copy the URL.
- **Discord:** Server Settings → Integrations → Webhooks → *New Webhook* → copy the URL.

Put it in `.env` as `SLACK_WEBHOOK_URL=...` and treat it like a password. No webhook? Lesson 15's `--dry-run` mode just prints the message instead.

**GitHub Actions secrets** (for the scheduled automation in Lesson 15): in your repo, go to **Settings → Secrets and variables → Actions → New repository secret** and add `ANTHROPIC_API_KEY` (and `SLACK_WEBHOOK_URL`). Actions are free for public repos and have a monthly free allowance for private ones.

---

## Step 12: Docker Desktop and Render (Lesson 16)

**Docker** packs your app and everything it needs into a "container" that runs the same anywhere. **Render** is a hosting service that runs your container on the internet. Lesson 16 explains both from zero.

1. **Docker Desktop:** download it from **docker.com/products/docker-desktop** (choose Apple Silicon or Intel on a Mac).
   - macOS alternative: `brew install --cask docker`, then open the Docker app once.
   - Windows: the installer sets up **WSL 2** (a built-in Linux layer) if needed; restart when asked.
   - Linux: install **Docker Engine** with your distribution's instructions at docs.docker.com/engine/install.
2. Check it (Docker Desktop must be running, with the whale icon in your menu bar or system tray):

   ```bash
   docker --version
   docker run --rm hello-world     # prints "Hello from Docker!"
   ```

3. **Render:** sign up at **render.com** with your GitHub account. The free tier is enough. You'll add your `ANTHROPIC_API_KEY` as an environment variable in Render's dashboard, never in the code.

Can't install Docker (old or locked-down computer)? You can skip running it locally. Render can build from your `Dockerfile`, or run the app directly with Python.

---

## Step 13: GitHub Pages (Lesson 17)

Nothing to install. Create a public repo named exactly `<your-username>.github.io`, add an `index.html`, then go to **Settings → Pages** and choose *Deploy from a branch → main*. Your site goes live at `https://<your-username>.github.io` within a minute or two.

---

## 14. Optional: install everything at once and check it

Want to check your computer can handle the whole course on day one? This installs every Python package used in the course (about 1.5 GB) into one test project and runs a checker:

```bash
cd ~/ai-engineer-projects
uv init --python 3.14 setup_check && cd setup_check
uv add numpy pandas matplotlib scikit-learn joblib requests python-dotenv pydantic pydantic-settings \
  anthropic tiktoken sentence-transformers chromadb rank-bm25 pypdf streamlit \
  langchain langchain-anthropic langgraph langgraph-checkpoint-sqlite langchain-community \
  langchain-text-splitters langchain-chroma langchain-huggingface \
  feedparser mcp apscheduler fastapi uvicorn
uv add --dev pytest ruff httpx ipykernel
cp /path/to/zero-to-ai-engineer/check_setup.py .      # the checker that sits next to this guide
uv run check_setup.py
```

(On Windows, put the `uv add` command on one line, or end each line with a backtick `` ` `` instead of `\`.)

You should see `OK` next to each package, plus `git`, `node` and `docker` if you've installed them. Here's what it printed on the test machine in October 2026:

```
Python 3.14.7 OK
Month 1:  numpy 2.5 · pandas 3.0 · matplotlib 3.11 · scikit-learn 1.9 · pydantic 2.14 · pytest 9.1
Month 2:  anthropic 1.17 · sentence-transformers 6.2 · chromadb 1.5 · pypdf 6.21 · streamlit 1.66
Month 3:  langchain 1.4 · langchain-anthropic 1.7 · fastapi 0.158 · uvicorn 0.54 · mcp 2.x
```

Newer version numbers are fine. **Older major versions are not** (for example pandas 2.x, langchain 0.x or mcp 1.x), because the lessons use their newer APIs. Delete the test project afterwards if you like: each lesson makes its own.

---

## 15. Fixing common problems

| Problem | Fix |
|---|---|
| `command not found: uv` (or git, code, node) | Close and reopen the terminal. Still broken? Rerun the installer and read its last lines; it tells you which folder to add to PATH. |
| Windows: `SyntaxError: ... null bytes` or the `.env` key isn't found | The file was made with PowerShell `echo`. Delete it and recreate it in VS Code (Step 0). |
| `python --version` shows 3.9 or "not found" | Normal. Use `uv run python ...`, which uses the project's Python. |
| Windows: "running scripts is disabled on this system" | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell once. |
| `uv add` fails building a package | Check you're on Python 3.13/3.14 (`uv run python --version`). Then `uv cache clean` and try again. |
| VS Code shows red squiggles on `import pandas` | Bottom right of VS Code → select interpreter → choose `.venv` inside your project. |
| `ModuleNotFoundError` | You're in the wrong folder or forgot `uv add <package>`. Run `uv add` in the project folder, then use `uv run`. |
| `AuthenticationError` / 401 from the API | The key is wrong or `.env` isn't in the folder you run from. Check that `load_dotenv()` is called before you create the client. |
| `credit balance is too low` | Add credit in the Claude Console under Billing. |
| `git push` asks for a password | Run `gh auth login` (Step 6). GitHub no longer accepts account passwords for Git. |
| `Cannot connect to the Docker daemon` | Open the Docker Desktop app and wait for it to finish starting. |
| Lesson 09 install is slow or huge | Expected: PyTorch is ~1 GB. Give it time; you only download it once per machine thanks to uv's cache. |
| Corporate laptop blocks installs | Ask IT, or use **GitHub Codespaces** (github.com/codespaces): a free-tier cloud computer with VS Code in your browser. Run Step 2 inside it. |

---

## 16. One-page checklist

- [ ] VS Code + Python, Jupyter and Ruff extensions
- [ ] `uv --version` works
- [ ] `uv python install 3.14` done
- [ ] `~/ai-engineer-projects` folder created; `uv run hello.py` printed hello
- [ ] Lesson 02: `ipykernel` works in a notebook
- [ ] Lesson 03: `git --version`, `git config` done, GitHub account, `gh auth status` OK
- [ ] Lesson 08: Claude Console account, credit, **spending limit**, key in `.env`, `.env` in `.gitignore`, test call works
- [ ] Lesson 09: ~2 GB free disk
- [ ] Lesson 15: `node --version`; optional Slack/Discord webhook; GitHub Actions secrets
- [ ] Lesson 16: `docker run --rm hello-world` works (optional); Render account
- [ ] Lesson 17: `<username>.github.io` repo

Now go back to `00_START_HERE_Master_Plan.md`, or start `Month1_AI_Python_Foundations/01_Python_Fundamentals/lesson.md`.
