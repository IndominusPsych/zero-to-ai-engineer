# Practice & Test 13: Agentic Workflows

> **🛠️ Before you start:** you need a Claude API key; anthropic, python-dotenv, pydantic, pytest. Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('key OK' if os.getenv('ANTHROPIC_API_KEY','').startswith('sk-ant-') else 'NO KEY: see Setup Guide Step 8')"
> ```

**Setup:** build the support workflow from Lesson 13 Section 3 (`uv add anthropic python-dotenv pydantic`). Exercises reuse its `ask()` helper.

---

## Part A: Pattern recognition

**A1.** Name the best pattern (chaining, routing, parallelisation-sectioning, parallelisation-voting, orchestrator–workers, evaluator–optimiser, or agent):
1. Translate a marketing page, then check the translation keeps the brand tone, revising until it does.
2. A helpdesk where billing, technical and sales questions need different knowledge bases.
3. Review a pull request for security, performance and style at the same time.
4. "Write a market report on electric scooters in 5 countries": the needed research subtasks depend on what's found.
5. Generate an outline, then write each section, then add a summary.
6. Decide if a user comment violates policy, using 3 independent judgements.
7. "Investigate why last night's data pipeline failed" with access to logs, code and dashboards.

**A2.** Draw (in text) a workflow for: *"Turn a raw job description into (1) a cleaned version, (2) a list of required skills, (3) 5 interview questions, and (4) check none of the questions are illegal or discriminatory."* Mark which steps can run in parallel and where a gate goes.

**A3.** What's the difference between parallelisation-sectioning and orchestrator–workers?

**A4.** Your evaluator–optimiser loop sometimes runs 6 rounds and costs too much. Give three fixes.

**A5.** Why use structured outputs between workflow steps?

---

## Part B: Hands-on

**B1. Prompt chain with a gate.** Build `blog_chain(topic)`: (1) outline as a Pydantic list of headings, (2) **gate**: code checks 3–6 headings and no duplicates, else retry once, (3) write each section, (4) a final polish step. Print token usage per step.

**B2. Router with cost savings.** Build a router that classifies questions as `simple` or `complex`. Route `simple` to `effort="low"` with a short answer limit and `complex` to `effort="high"`. Run 10 mixed questions and compare total cost vs sending everything to `high`.

**B3. Voting.** Implement `is_spam(message)` that runs 3 calls with slightly different prompts in parallel and returns the majority vote. Test on 10 messages you label yourself. Does voting beat a single call?

**B4. Sectioning.** Write `review_contract(text)` that checks payment terms, liability and termination clauses **in parallel** (three calls, each with a focused prompt and a `Findings` schema) and merges them into one report. Measure time vs doing them in sequence.

**B5. Orchestrator–workers.** Build `research(question)`:
- The orchestrator returns a `Plan` (list of 2–5 subtasks, each with a `query` and `purpose`).
- Workers answer each subtask (give them a search tool or your Lesson 10 RAG `retrieve` as context).
- The orchestrator synthesises a final answer citing which subtask each claim came from.

**B6. Evaluator–optimiser with code-based evaluation.** Generator writes a Python function `slugify(title: str) -> str` from a spec. Evaluator = **real unit tests** run with `exec` in a separate namespace (OK here because you control the input; never do this with untrusted users) or better, saved to a file and run with `subprocess.run(["uv", "run", "pytest", ...])`. Feed failing test output back to the generator. Stop after 3 rounds.

**B7. Checkpointing.** Make B1 save its state (a Pydantic model) to `state/<run_id>.json` after every step. Kill the script mid-run (Ctrl+C), then add a `--resume <run_id>` flag that continues from the last completed step.

**B8. Workflow eval.** For the Lesson 13 support workflow, create 20 test emails (incl. 4 injection/abuse). Measure: router accuracy, guard catch rate (and false alarms), % passing review in round 0, average rounds, average cost and latency. Present a table.

---

## Part C: Mini-project: "Content Repurposing Pipeline" (half a day)

Input: a long article (blog post, talk transcript). Output: a LinkedIn post, a tweet thread (≤ 5 tweets), a 3-question quiz, and an email newsletter blurb.

Required design:
1. **Step 1:** extract key points (structured: `KeyPoints` with 5–8 points + quotes).
2. **Step 2 (parallel sectioning):** four writers, each a specialist prompt, generate the four formats from the key points.
3. **Step 3 (evaluator–optimiser per format):** a reviewer checks each piece against a format-specific rubric (length limits, no claims not in the key points, tone) and requests revisions (max 2 rounds).
4. **Step 4 (gate):** code checks hard limits (tweet length ≤ 280 chars, quiz has 4 options each).
5. **State object** logged per run to `runs/`.
6. **Human-in-the-loop:** a CLI shows all four outputs; the user can approve, or type feedback for one format that triggers a revision.
7. **Eval:** run on 5 different articles; report pass rates per format, average review rounds, cost and time.

**Rubric (20):** clean step functions with schemas (4), correct parallelism (3), evaluator loops with limits (4), code gates (3), state logging & human approval (3), eval report (3).

---

## Part D: Quiz (20 minutes)

1. In a workflow, who decides the order of steps?
   a) The model b) The user every time c) Random d) Your code

2. Prompt chaining is best for:
   a) Tasks that split cleanly into fixed steps b) Voting c) Unpredictable tasks d) Embeddings

3. A "gate" is:
   a) A firewall b) A code check between steps that can stop or redirect c) A model d) An API key

4. Routing helps reduce cost by:
   a) Removing tools b) Using more tokens c) Sending easy inputs to cheaper/faster settings d) Caching embeddings

5. Running a safety check at the same time as the main task is:
   a) Chaining b) Orchestrator–workers c) Parallelisation (sectioning) d) Voting

6. Voting is useful when:
   a) You have no prompts b) You want to save money c) Steps depend on each other d) You need more confidence in a judgement

7. Orchestrator–workers differs from sectioning because:
   a) Subtasks are decided at runtime by the model b) It's slower c) It has no LLMs d) Workers can't use tools

8. Evaluator–optimiser needs:
   a) Two API keys b) Clear evaluation criteria and a round limit c) Infinite loops d) No criteria

9. Explicit state objects make workflows:
   a) Impossible to parallelise b) Non-deterministic c) Easier to log, test, resume and debug d) Slower only

10. Idempotency means:
    a) Re-running a step doesn't cause double effects b) Using the same model c) Steps never fail d) Steps run twice give double effects

11. Checkpointing allows:
    a) Removing state b) Resuming a workflow after a failure c) Faster tokens d) Better embeddings

12. A multi-agent system is a good idea when:
    a) Never b) Always c) It sounds impressive d) Roles and contexts genuinely differ and one agent's context overloads

13. Trajectory evaluation checks:
    a) The sequence of steps/tool calls an agent took b) The final answer only c) Embedding quality d) Token prices

14. The best evaluator for generated code is often:
    a) Asking the user b) Counting lines c) Another vague prompt d) Running real unit tests

15. Most production "agents" are best described as:
    a) Fine-tuned models b) Workflows with a few agentic steps c) Fully autonomous with no limits d) Single prompts

**Short answer.**

16. Describe the five workflow patterns in one sentence each.
17. When should you choose an agent over a workflow?
18. Name four reliability techniques for workflows.
19. How would you evaluate a routing step?
20. Draw the Lesson 13 support workflow from memory.

---

## Answer Key

### Part A

**A1.** 1 evaluator–optimiser · 2 routing · 3 parallelisation-sectioning · 4 orchestrator–workers · 5 prompt chaining · 6 parallelisation-voting · 7 agent.

**A2.**
```
JD ─▶ [clean JD] ─┬─▶ [extract skills] ─────────┐
                  └─▶ [write 5 questions] ─▶ [legality check] ─▶ GATE: any flagged? ─yes─▶ rewrite flagged / human
                                                                      │ no
                                                                      ▼
                                                           combine: cleaned JD + skills + questions
```
Skills and questions run in parallel after cleaning; the gate follows the legality check.

**A3.** Sectioning splits work into subtasks **you** define in advance and runs them in parallel; orchestrator–workers lets a **model** decide the subtasks at runtime based on the input, then synthesises.

**A4.** Lower the round limit (e.g. 2) and escalate; make the rubric clearer and give the generator the rubric up front; use code checks for objective criteria; use higher effort for the generator so first drafts are better; only re-generate failing parts.

**A5.** Each step's output becomes the next step's input; structured outputs guarantee the shape so code can validate, route and log reliably instead of parsing free text.

### Part B: reference snippets

```python
# B1 gate
from pydantic import BaseModel
class Outline(BaseModel):
    headings: list[str]

def get_outline(topic, tries=2):
    for _ in range(tries):
        o = ask("Create a blog outline.", f"Topic: {topic}. 3-6 headings.", Outline)
        if 3 <= len(o.headings) <= 6 and len(set(h.lower() for h in o.headings)) == len(o.headings):
            return o
    raise ValueError("Outline failed the gate twice.")

# B3 voting
from concurrent.futures import ThreadPoolExecutor
class SpamVote(BaseModel):
    spam: bool
PROMPTS = ["Is this message spam?", "Would a careful moderator flag this as spam or scam?",
           "Is this unsolicited bulk/promotional or deceptive? Answer spam=true if so."]
def is_spam(msg):
    with ThreadPoolExecutor() as pool:
        votes = list(pool.map(lambda p: ask(p, f"<message>{msg}</message>", SpamVote).spam, PROMPTS))
    return sum(votes) >= 2

# B5 orchestrator schema
class Subtask(BaseModel):
    query: str
    purpose: str
class Plan(BaseModel):
    subtasks: list[Subtask]

# B6 code-based evaluator
import subprocess, pathlib
def run_tests(code: str) -> tuple[bool, str]:
    pathlib.Path("gen/slug.py").write_text(code)
    r = subprocess.run(["uv", "run", "pytest", "-q", "gen/test_slug.py"], capture_output=True, text=True)
    return r.returncode == 0, r.stdout[-2000:]
```

### Part D: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | d | 6 | d | 11 | b |
| 2 | a | 7 | a | 12 | d |
| 3 | b | 8 | b | 13 | a |
| 4 | c | 9 | c | 14 | d |
| 5 | c | 10 | a | 15 | b |

**16.** Chaining: fixed sequence of steps feeding each other, with gates. Routing: classify input and send it to a specialised handler. Parallelisation: run independent parts (sectioning) or repeated judgements (voting) simultaneously. Orchestrator–workers: a planner creates subtasks at runtime for workers, then synthesises. Evaluator–optimiser: generate, critique against a rubric, revise in a loop.

**17.** When the steps can't be predicted in advance, the task is open-ended and valuable enough to justify cost/latency, the model is capable at it, and errors can be caught or undone.

**18.** Retries, timeouts, idempotent steps, checkpointing/resume, fallbacks, budgets/round limits, human approval.

**19.** Build a labelled set of inputs with the correct route; measure accuracy and a confusion matrix (which categories get confused); check the cost/quality impact of misroutes.

**20.** See Lesson 13 Section 3's final diagram: parallel classify + guard → gate → route to specialist handler with tool → draft/review loop → human approval → send; every run logged.

**Scoring:** out of 25. ≥ 21 move on.
