# Practice & Test 15: AI Automation

> **🛠️ Before you start:** you need a Claude API key; anthropic, python-dotenv, feedparser, requests, pydantic, mcp 2.x, apscheduler, fastapi, uvicorn; Node.js for the MCP Inspector; a GitHub repo with Actions secrets; optional Slack/Discord webhook. Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> node --version && uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('key OK' if os.getenv('ANTHROPIC_API_KEY','').startswith('sk-ant-') else 'NO KEY: see Setup Guide Step 8')"
> ```

**Setup:**

```bash
uv init automation_lab && cd automation_lab
uv add anthropic python-dotenv feedparser requests pydantic mcp apscheduler
```

You'll need: a GitHub account (Lesson 03), and optionally a free Slack workspace (or Discord server) for webhooks.

---

## Part A: Concept checks

**A1. Cron.** Write cron expressions for: (a) every day at 07:15, (b) every 10 minutes, (c) 17:00 on the 1st of every month, (d) 09:00 Monday and Thursday. Then convert (a) to UTC for your own time zone.

**A2. Triggers.** Choose the best trigger (schedule, webhook, polling, event/queue, manual) for:
1. Summarise each new Stripe payment dispute as it's opened.
2. A Monday-morning report of last week's sales.
3. Check a public website without an API for price changes every hour.
4. Process each PDF uploaded to a cloud storage bucket.
5. A Slack command `/standup` that summarises the team's updates.

**A3. Batch or real-time?** (a) Drafting replies to live chat messages. (b) Tagging yesterday's 5,000 support tickets by topic. (c) Translating a product catalogue weekly. (d) Detecting fraud on card payments.

**A4. Idempotency.** Your automation appends a row to a Google Sheet for each new email. It crashed halfway and GitHub re-ran it. What goes wrong and how do you prevent it?

**A5. MCP.** What are the three things an MCP server can expose? What's the difference between the stdio and streamable HTTP transports?

**A6. Risk.** You want an automation that reads incoming customer emails and automatically issues refunds under $20. List the risks and the guardrails you'd add.

---

## Part B: Hands-on

**B1. Slack (or Discord) webhook.** Create an incoming webhook and post "Hello from Python" with `requests.post(url, json={"text": ...})`. (Discord: `json={"content": ...}`.) Store the URL in `.env`.

**B2. Email.** Send yourself an email with `smtplib` + `email.message.EmailMessage` using an email provider's SMTP settings (for Gmail you need 2-step verification + an "app password"). Or use an email API's free tier.

**B3. RSS collector with SQLite dedup.** Build `collect()` that stores processed links in a SQLite table `seen(link TEXT PRIMARY KEY, first_seen TEXT)` and only returns unseen items. Run it twice; the second run should return 0 new items.

**B4. Local scheduler.** Use APScheduler's `BlockingScheduler` to run B3 every 2 minutes and print how many new items arrived. Stop with Ctrl+C.

**B5. The full digest.** Build Lesson 15's News Digest. Run with `--dry-run`, then for real to Slack. Add your own feeds and interests.

**B6. GitHub Actions.** Push the digest to a GitHub repo, add the two secrets, add the workflow YAML, and run it with the **Run workflow** button. Find the logs. Then break it on purpose (wrong secret name) and confirm you get a failure alert and a failed run.

**B7. Batch API.** Rewrite `make_digest` to summarise every collected item individually using the **Message Batches API** (`client.messages.batches.create(...)`), poll until finished, and collect results by `custom_id`. Compare cost with individual calls. (Results can arrive in any order; always match by `custom_id`.)

**B8. Build an MCP server.** Build `notes_server.py` from the lesson. Test it with the MCP Inspector (`npx @modelcontextprotocol/inspector uv run --with mcp python notes_server.py`). Then connect it to Claude Code (`claude mcp add notes -- uv run --with mcp python /full/path/notes_server.py`) or Claude Desktop and use it in a conversation. Add a third tool, `list_recent(n: int)`.

**B9. MCP for your digest.** Create `digest_server.py` exposing `todays_items()` and `search_items(query)` as MCP tools (reuse B3's SQLite). Ask an MCP client "anything about Python packaging in my feeds this week?"

**B10. Webhook receiver (preview of Lesson 16).** `uv add fastapi uvicorn`. Write a tiny FastAPI app with `POST /webhook` that accepts JSON `{"text": ...}`, classifies it with an LLM (`Literal["bug", "question", "praise"]`), and appends the result to `inbox.jsonl`. Run with `uv run uvicorn app:app --reload` and test with `curl -X POST localhost:8000/webhook -H "Content-Type: application/json" -d '{"text":"The app crashes on login"}'`.

---

## Part C: Mini-project: automate something real (half a day)

Pick a repetitive task from your own life or a past job and automate it end to end. Ideas:

| Idea | Trigger | AI step | Output |
|---|---|---|---|
| **Job-post watcher** | Daily schedule | Extract role/skills/salary (structured) and score fit vs your CV | Slack/email shortlist + Google Sheet |
| **GitHub repo assistant** | Webhook or schedule on new issues | Label and summarise issues; suggest duplicates | Labels + comment draft |
| **Meeting-notes pipeline** | New file in a folder (polling) | Extract decisions/action items/owners | Markdown file + Slack post |
| **Expense receipts** | New photo in a folder | Vision extraction (Lesson 08) → category | Append to a CSV/Sheet (idempotent!) |
| **Study reminder** | Daily schedule | Quiz yourself on 3 random notes (StudyBuddy, Lesson 11) | Slack/email with questions; answers next day |

Requirements:
1. Trigger + workflow + at least one real integration.
2. Structured outputs and input/output guardrails.
3. Dedup/idempotency and a `--dry-run` flag.
4. Secrets in the platform; `.env.example` in the repo.
5. Logging, failure alerts, and a cost cap.
6. A human-in-the-loop step if any action is consequential.
7. README: diagram, how to run/schedule, costs per run, limitations, kill switch.

**Rubric (20):** works end to end on its trigger (5), integrations (3), guardrails & structured outputs (3), idempotency & dry-run (3), monitoring & cost cap (3), README (3).

---

## Part D: Quiz (20 minutes)

1. AI automation is best described as:
   a) Training a model b) A no-code website c) Trigger + AI workflow + integrations running on its own d) Chatting with an AI

2. A webhook is:
   a) A fishing tool b) A cron expression c) An API key d) An HTTP request another system sends you when something happens

3. `0 8 * * 1-5` means:
   a) 8 minutes past every hour b) 08:00 on weekdays c) Every 8 days d) 08:00 on weekends

4. GitHub Actions scheduled workflows run in which time zone by default?
   a) UTC b) Your local time c) Pacific time d) The repo owner's time zone

5. Polling is:
   a) Instant notification b) A voting pattern c) Repeatedly checking for something new d) An MCP transport

6. Batch processing is a good default when:
   a) Nobody needs the result immediately b) A user is waiting live c) Latency must be under 100 ms d) Never

7. Idempotency means:
   a) The job uses AI b) The job is fast c) The job has no inputs d) Re-running the job doesn't cause duplicate effects

8. Where should an automation's API keys live on GitHub Actions?
   a) In a commit message b) In repository Secrets c) In the README d) In the YAML file

9. A "dead-man's switch" alerts you when:
   a) The job crashes loudly b) Costs drop c) A user logs in d) The job fails to run/check in on time

10. In MCP, "tools" are:
    a) Functions the AI can call b) User accounts c) Read-only data d) Vector databases

11. The stdio transport means:
    a) A database b) Email c) The client launches the server as a local process and talks through its input/output d) A public web service

12. In MCP Python SDK 2.x, the server class is:
    a) `FastMCP` b) `MCPServer` c) `ToolRunner` d) `Flask`

13. Content from RSS feeds and emails should be treated as:
    a) Secrets b) System prompts c) Trusted instructions d) Untrusted data (possible prompt injection)

14. No-code tools like Zapier, Make and n8n are best for:
    a) Simple glue between apps b) Writing unit tests c) Replacing databases d) Training models

15. For an automation that issues refunds, the safest pattern is:
    a) Fully automatic for all amounts b) Disable alerts c) Confidence routing/limits with human approval for anything risky, plus logs d) Never log anything

**Short answer.**

16. Describe the three parts of an AI automation with an example.
17. List four monitoring practices for automations.
18. How does the News Digest avoid duplicates on GitHub Actions, and how would you do it on a server?
19. What are the security considerations when installing or writing MCP servers?
20. When would you choose a no-code tool over writing Python?

---

## Answer Key

### Part A

**A1.** (a) `15 7 * * *` (b) `*/10 * * * *` (c) `0 17 1 * *` (d) `0 9 * * 1,4`. UTC example for India (UTC+5:30): 07:15 IST = 01:45 UTC → `45 1 * * *`.

**A2.** 1 webhook · 2 schedule · 3 polling (scheduled check) · 4 event/queue · 5 manual/chat (Slack slash command → webhook).

**A3.** (a) real-time (b) batch (c) batch (d) real-time.

**A4.** Rows processed before the crash are appended again → duplicates. Prevent with a processed-IDs store (skip seen email IDs), or idempotent writes (upsert by email ID), and checkpointing.

**A5.** Tools (callable functions), resources (read-only data), prompts (reusable templates). stdio: the client starts your server locally and communicates over standard input/output; streamable HTTP: the server runs as a web service that clients connect to over the network.

**A6.** Risks: prompt injection ("refund me $19.99 five times"), misclassification, duplicates, fraud, policy violations. Guardrails: hard code limits (≤ $20, max one per order, order exists and is eligible), idempotent refund keyed by order ID, injection-safe prompts, confidence routing (uncertain → human), daily human review of all refunds, alerts on anomalies, a kill switch.

### Part B: reference snippets

```python
# B2
import os, smtplib
from email.message import EmailMessage
msg = EmailMessage()
msg["Subject"], msg["From"], msg["To"] = "Test", os.environ["SMTP_USER"], os.environ["SMTP_USER"]
msg.set_content("Hello from Python")
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
    s.login(os.environ["SMTP_USER"], os.environ["SMTP_APP_PASSWORD"])
    s.send_message(msg)

# B3
import sqlite3, datetime, feedparser
db = sqlite3.connect("seen.db")
db.execute("CREATE TABLE IF NOT EXISTS seen (link TEXT PRIMARY KEY, first_seen TEXT)")

def collect(feeds):
    new = []
    for url in feeds:
        for e in feedparser.parse(url).entries:
            link = e.get("link")
            if not link:
                continue
            cur = db.execute("INSERT OR IGNORE INTO seen VALUES (?, ?)",
                             (link, datetime.datetime.now().isoformat()))
            if cur.rowcount:                      # 1 if inserted (new), 0 if already seen
                new.append({"title": e.get("title", ""), "link": link})
    db.commit()
    return new

# B4
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
sched.add_job(lambda: print(len(collect(FEEDS)), "new"), "interval", minutes=2)
sched.start()

# B10
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
import json, anthropic
app = FastAPI(); client = anthropic.Anthropic()
class Incoming(BaseModel):
    text: str
class Label(BaseModel):
    label: Literal["bug", "question", "praise"]

@app.post("/webhook")
def webhook(item: Incoming):
    r = client.messages.parse(model="claude-opus-5-5", max_tokens=200, output_config={"effort": "low"},
                              messages=[{"role": "user", "content": f"Classify:\n<text>{item.text}</text>"}],
                              output_format=Label)
    record = {"text": item.text, "label": r.parsed_output.label}
    with open("inbox.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")
    return record
```

(APScheduler's API differs between major versions; if `BlockingScheduler` isn't found, check the installed version's docs.)

### Part D: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | c | 6 | a | 11 | c |
| 2 | d | 7 | d | 12 | b |
| 3 | b | 8 | b | 13 | d |
| 4 | a | 9 | d | 14 | a |
| 5 | c | 10 | a | 15 | c |

**16.** Trigger (what starts it: e.g. a daily 08:00 schedule), workflow/agent (the steps: collect RSS → LLM picks and summarises), integrations (input/output: RSS feeds in, Slack webhook out).

**17.** Per-run logs (items, errors, cost); failure alerts; heartbeat/dead-man's-switch monitoring; cost caps and spending limits; periodic quality spot-checks.

**18.** It only takes items published in the last ~26 hours and de-duplicates links within the run (GitHub runners start fresh each time). On a server, store processed IDs/links in SQLite (or use a watermark timestamp) and skip ones already seen.

**19.** Servers run with your permissions and can read/modify what you can, so only install trusted servers, review their code/permissions, give your own servers least privilege (e.g. one folder, read-only where possible), keep secrets out of tool outputs, and treat tool outputs as untrusted data.

**20.** When the flow is simple glue between supported apps, non-programmers need to own it, and you don't need custom logic, tests, version control, evals or very high volume.

**Scoring:** out of 25. ≥ 21 move on.
