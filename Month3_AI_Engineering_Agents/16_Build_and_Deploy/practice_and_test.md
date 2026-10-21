# Practice & Test 16: Build and Deploy a Complete AI Project

> **🛠️ Before you start:** you need a Claude API key (a separate one for production); fastapi, uvicorn, anthropic, pydantic-settings, pytest, httpx, ruff; Docker Desktop; Render and GitHub accounts. Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> docker run --rm hello-world && uv run pytest
> ```

This is the **capstone** lesson. Part B walks through deployment skills; Part C is your capstone project brief and grading rubric.

**Setup:** build the Handbook Assistant from Lesson 16 Section 3 first. Install Docker Desktop (docker.com) if you want to run containers locally.

---

## Part A: Concept checks

**A1.** A friend's app calls the Anthropic API directly from browser JavaScript "to keep it simple." Explain the problem and the fix.

**A2.** Match each platform to the best use: Streamlit Community Cloud, Hugging Face Spaces, Render, Google Cloud Run, Vercel.
(a) A Next.js frontend. (b) A quick Streamlit demo. (c) A Gradio ML demo for the HF community. (d) A FastAPI Docker backend with Git auto-deploys. (e) A production container that scales to zero.

**A3.** Your app saves user feedback to `feedback.jsonl` inside the container. After a redeploy, it's all gone. Why, and what should you do?

**A4.** Order these CI/CD steps: deploy to host · open pull request · run tests · merge to main · push branch · tests pass.

**A5.** List five protections for a public AI demo and what each stops.

**A6.** What's the difference between average latency and p95 latency, and why does p95 matter for LLM apps?

**A7.** Why should CI tests mock the LLM? Where do real-model evals run instead?

---

## Part B: Hands-on deployment skills

**B1. FastAPI basics.** Build `/health`, `POST /echo` (Pydantic model with `text: str = Field(max_length=200)`), and explore `/docs`. Send an over-long text and read the 422 response.

**B2. Streaming endpoint.** Add `POST /stream` that streams a Claude answer with `StreamingResponse`. Test with `curl -N -X POST localhost:8000/stream -H "Content-Type: application/json" -d '{"text":"Tell me a short story"}'` (`-N` disables buffering so you see it stream).

**B3. Docker.** Write the Dockerfile and `.dockerignore`. Build and run the Handbook Assistant in a container. Confirm `.env` is **not** inside the image: `docker run --rm handbook-assistant ls -a /app`.

**B4. Tests + CI.** Add the 5 tests from the lesson plus one more (e.g. the daily cap returns 503). Add the GitHub Actions CI workflow and a CI status badge to your README (GitHub shows the badge Markdown under Actions → your workflow → "Create status badge").

**B5. Deploy.** Deploy to Render, Railway, Fly.io or Cloud Run. Configure the health check path, environment variables (production key with a spending limit!) and auto-deploy. Share the URL with a friend and ask them to try it.

**B6. Abuse test (your own app only).** Script 15 rapid requests at your deployed `/ask` and confirm 429s appear after the limit. Send a 10,000-character question and confirm 422. Send a request without the access code and confirm 401.

**B7. Streamlit deploy.** Deploy your Lesson 11 project (StudyBuddy or similar) to Streamlit Community Cloud with the API key in its Secrets settings (`st.secrets["ANTHROPIC_API_KEY"]` or as an environment variable, per its docs).

**B8. Observability.** Add a free uptime monitor for `/health`. Add Sentry (`uv add sentry-sdk`, `sentry_sdk.init(dsn=...)`) and trigger a test error. Write a small script that parses your host's downloaded logs (JSON lines) into a Pandas table of tokens, cache reads and latency, and computes p95 latency and cost per request.

**B9. Postgres + pgvector (stretch).** Create a free managed Postgres (Neon or Supabase), enable the `vector` extension, and port Lesson 10's retrieval to it (`uv add psycopg[binary] pgvector`). Store chunks in a table with an `embedding vector(384)` column and query with `ORDER BY embedding <=> %s LIMIT 5` (`<=>` is pgvector's cosine-distance operator).

---

## Part C: 🎓 Capstone project brief

Build and deploy **one complete AI application** that combines at least **three** of: RAG, structured outputs, tool calling/agents, a LangGraph workflow, automation/triggers, MCP. It should solve a specific problem for a specific user (Lesson 11 Section 2.1).

### Suggested capstones

| Capstone | Combines |
|---|---|
| **Support Copilot**: inbox webhook → LangGraph triage workflow (classify, guard, route, draft, review) → human approval UI → send | Workflows, tools, structured outputs, interrupts, automation, deploy |
| **Research Assistant**: question → orchestrator plans → workers search your documents (RAG) + web → cited brief → critique loop → PDF/Markdown export | Orchestrator–workers, RAG, evaluator–optimiser, deploy |
| **Personal Finance Agent** (Practice 12 Part C) with a web UI, scheduled weekly summary to email, and an MCP server so you can query it from Claude | Agents, tools, automation, MCP, deploy |
| **StudyBuddy Pro**: Lesson 11 + agentic tutor that picks weak topics from quiz history, daily study-reminder automation, progress dashboard | RAG, structured outputs, agents, automation, database, deploy |
| **Job Hunt Copilot**: daily job-feed collection, structured extraction, CV-fit scoring, tailored cover-letter drafts with human approval | Automation, structured outputs, workflows, deploy |

### Required deliverables

1. **Live URL** (with access code or login if it costs you money).
2. **GitHub repo** with: README (Lesson 17 template), architecture diagram (Mermaid), `.env.example`, Dockerfile (if API backend), CI workflow with passing badge.
3. **Evals:** ≥ 30 cases covering normal, edge, adversarial (injection) and out-of-scope inputs; results table with at least 3 iterations.
4. **Guardrails:** input/output limits, rate limiting, injection resistance, human approval for consequential actions.
5. **Observability:** structured logs with request IDs, tokens, cost and latency; uptime monitor; a cost-per-request figure in the README.
6. **Demo video** (2–3 minutes): problem → live demo → architecture → evals → what you'd improve.
7. **Limitations** section.

### Timeline (Week 11)

| Day | Goal |
|---|---|
| 1 | Spec, architecture, eval plan; skeleton repo with CI green |
| 2–3 | Core features working locally; first eval run |
| 4 | Guardrails, logging, UI polish; second eval run |
| 5 | Docker + deploy; abuse tests; uptime monitor |
| 6 | Third eval iteration; README, diagram, demo video |

### Capstone rubric (100 points)

| Area | Criteria | Points |
|---|---|---|
| Problem & product | Specific user and pain; coherent MVP; good UX (streaming, sources, errors, disclosure) | 15 |
| AI engineering | Sound prompts; structured outputs; appropriate pattern (single call / workflow / agent) justified in README | 15 |
| Retrieval / tools / workflow | Correctly implemented and measured (retrieval metrics, tool-call traces, graph structure) | 15 |
| Evals | ≥ 30 cases, code + LLM-judge graders, 3+ iterations with numbers | 15 |
| Safety & guardrails | Limits, injection tests, approvals, least privilege | 10 |
| Deployment | Live, Dockerised or platform-native, secrets handled, health check | 10 |
| CI/CD & tests | CI green with mocked LLM tests; auto-deploy or documented deploy | 5 |
| Observability & cost | Logs with request IDs, cost/request, uptime monitor | 5 |
| Documentation & demo | README, diagram, limitations, video | 10 |
| **Total** | | **100** (≥ 80 = excellent portfolio centrepiece) |

---

## Part D: Quiz (20 minutes)

1. Where must the LLM API key live in a web app?
   a) In the HTML b) Only on the backend server c) In the README d) In the browser's JavaScript

2. FastAPI automatically rejects invalid request bodies because of:
   a) Pydantic models in the route signature b) Uvicorn c) Docker d) CORS

3. `/docs` in FastAPI shows:
   a) Server logs b) The Dockerfile c) Your README d) Auto-generated interactive API documentation

4. A Docker image is:
   a) A database b) A screenshot c) The built, frozen package of your app and its dependencies d) A running container

5. Inside a container, uvicorn should listen on:
   a) Port 22 b) 0.0.0.0 (and the PORT the host provides) c) 127.0.0.1 d) localhost only

6. `.dockerignore` should include:
   a) `uv.lock` b) `pyproject.toml` c) `app/` d) `.env` and `.venv/`

7. A "cold start" is:
   a) A Docker error b) A frozen server c) The slow first request after a serverless/free app was idle d) A failed build

8. Files written inside many hosted containers:
   a) May disappear on restart/redeploy (ephemeral) b) Persist forever c) Are backed up automatically d) Go to GitHub

9. Rate limiting protects against:
   a) Typos b) Slow models c) CORS d) One user or bot sending too many requests and running up costs

10. CORS controls:
    a) Database access b) Which websites' browser code may call your API c) Docker networking d) Model choice

11. CI usually runs:
    a) The paid eval suite on every commit b) Only in production c) Lint and tests automatically on every push/PR d) Once a year

12. Why mock the LLM in CI tests?
    a) Fast, free, deterministic tests b) Mocks are smarter c) To hide bugs d) It's required by GitHub

13. A health check endpoint is used by:
    a) The LLM b) Hosts and uptime monitors to know the app is alive c) Docker to build d) Users to log in

14. Making the app "stateless" means:
    a) It has no database b) It can't stream c) It has no code d) Important state lives in a database, not in container memory, so any container can serve any request

15. The safest production key setup is:
    a) Share one key across all apps and friends b) Commit the key c) A separate production key with a spending limit, stored as a host secret d) Reuse your personal key

**Short answer.**

16. Draw the architecture of the deployed Handbook Assistant.
17. Explain Docker's dockerfile → image → container in your own words.
18. List the steps from `git push` to a live update with CI/CD.
19. What would you monitor for a deployed AI app, and why?
20. Why did the lesson use long context + caching instead of RAG, and when would you switch?

---

## Answer Key

### Part A

**A1.** Browser code is visible to anyone; the key would be stolen and abused. Fix: the browser calls your backend; only the backend holds the key and calls the LLM.

**A2.** (a) Vercel (b) Streamlit Community Cloud (c) Hugging Face Spaces (d) Render (e) Google Cloud Run.

**A3.** The container's filesystem is ephemeral, so redeploys start from the image. Store feedback in a managed database (Postgres/SQLite on a persistent disk) instead.

**A4.** push branch → open pull request → run tests → tests pass → merge to main → deploy to host.

**A5.** Rate limiting (request floods), input length limits (huge costly prompts), output `max_tokens` (runaway generation), access code/auth (strangers using it), spending cap/daily cap (surprise bills); also CORS (other sites calling your API), injection guardrails (misuse).

**A6.** Average hides slow outliers; p95 is the time 95% of requests beat. LLM latency varies a lot (long answers, retries, cold starts), so p95 shows what slow-but-common experiences feel like.

**A7.** Real calls are slow, cost money and give non-deterministic outputs, making tests flaky. Mocks make CI fast, free and repeatable. Real-model evals run manually before releases, on a schedule (nightly), or when prompts/models change.

### Part B: reference snippets

```python
# B2
from fastapi.responses import StreamingResponse
import anthropic
aclient = anthropic.AsyncAnthropic()

@app.post("/stream")
async def stream(body: Echo):
    async def gen():
        async with aclient.messages.stream(model="claude-opus-5-5", max_tokens=1000,
                                           messages=[{"role": "user", "content": body.text}]) as s:
            async for t in s.text_stream:
                yield t
    return StreamingResponse(gen(), media_type="text/plain; charset=utf-8")
```

```python
# B4 extra test
def test_daily_cap(monkeypatch):
    c = client(monkeypatch, access_code="", daily_request_cap=1, rate_limit_per_minute=100)
    assert [c.post("/ask", json={"question": "Leave?"}).status_code for _ in range(2)] == [200, 503]
```

```python
# B6 abuse test
import requests
URL, CODE = "https://your-app.onrender.com/ask", "your-code"
codes = [requests.post(URL, json={"question": "Leave?"}, headers={"X-Access-Code": CODE}, timeout=60).status_code
         for _ in range(15)]
print(codes)        # expect 200s then 429s
```

```sql
-- B9
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE chunks (id text PRIMARY KEY, source text, page int, text text, embedding vector(384));
-- query: SELECT id, text, 1 - (embedding <=> %s) AS score FROM chunks ORDER BY embedding <=> %s LIMIT 5;
```

### Part D: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | b | 6 | d | 11 | c |
| 2 | a | 7 | c | 12 | a |
| 3 | d | 8 | a | 13 | b |
| 4 | c | 9 | d | 14 | d |
| 5 | b | 10 | b | 15 | c |

**16.** Browser (index.html + fetch) → HTTPS → host container (uvicorn + FastAPI: /health, /ask with validation, access code, rate limit, daily cap) → Anthropic API with the handbook cached in the system prompt; secrets as host env vars; JSON logs; CI on GitHub with auto-deploy.

**17.** A Dockerfile is the recipe; building it produces an image (a frozen package of OS layer, Python, dependencies and code); running the image starts a container (a live, isolated instance). Same image → same behaviour anywhere.

**18.** Push branch → GitHub Actions runs lint/tests → open PR (CI must pass) → merge to protected main → host detects the new commit, builds the image, runs health checks → switches traffic to the new version.

**19.** Uptime/health (is it up?), error rate and exceptions (is it breaking?), latency incl. p95 (is it fast?), tokens and cost per request/day (is it affordable?), cache hit rate, stop reasons/refusals, user feedback and periodic eval scores (is it still correct?), rate-limit hits (abuse?).

**20.** The handbook is small enough to fit comfortably in the context window, and caching makes repeated use cheap, so it's simpler (no vector DB or embedding model in the container) with no retrieval misses. Switch to RAG when the knowledge base grows large (hundreds of pages+), changes often, needs per-user permissions, or costs/latency from sending everything become too high.

**Scoring:** out of 25. ≥ 21 move on. Then complete your **capstone** (Part C).
