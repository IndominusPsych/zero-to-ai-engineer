# Practice & Test 08: LLM APIs

> **🛠️ Before you start:** you need a Claude API key with a spending limit; anthropic, python-dotenv, pydantic, pandas. Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('key OK' if os.getenv('ANTHROPIC_API_KEY','').startswith('sk-ant-') else 'NO KEY: see Setup Guide Step 8')"
> ```

**Setup:**

```bash
uv init llm_practice && cd llm_practice
uv add anthropic python-dotenv pydantic pandas
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
printf ".env\n.venv/\n__pycache__/\n" > .gitignore
```

💰 **Budget tip:** set a monthly spending limit (e.g. $5–10) in the Claude Console before you start. Every exercise here costs cents. For cheap bulk experiments you can set `MODEL = "claude-haiku-5-5"` in your own config, but **measure** before trusting a smaller model on anything important.

Put your model choice in one variable so you can swap it:

```python
MODEL = "claude-opus-5-5"
```

---

## Part A: Basics

**A1. Hello API.** Send "Give me 3 fun facts about octopuses." Print the text, `stop_reason`, input and output tokens, and the estimated cost.

**A2. System prompt.** Make the same request with three different system prompts: a pirate, a 5-year-old's teacher, a marine biologist. Compare.

**A3. Truncation on purpose.** Request a 500-word essay with `max_tokens=50`. Print `stop_reason`. Write code that detects `max_tokens` and warns "Answer was cut off."

**A4. Chat loop.** Build a terminal chatbot (`while True: input(...)`) that remembers the conversation. Commands: `/reset` clears history, `/tokens` prints total tokens used so far, `/quit` exits.

**A5. Streaming.** Turn A4 into a streaming chatbot so replies appear word by word.

**A6. Effort experiment.** Ask a tricky reasoning question (e.g. *"I have 3 boxes. One has only apples, one only oranges, one both. All labels are wrong. Picking one fruit from one box, how can I relabel all boxes correctly?"*) at effort `low` and `high`. Compare answer quality, output tokens, and latency (`time.perf_counter()`). Also print the summarised thinking with `thinking={"type": "adaptive", "display": "summarized"}`.

---

## Part B: Structured outputs

**B1. Contact extractor.** Define a Pydantic model `Contact(name: str, email: str | None, phone: str | None, company: str | None)` and extract from 5 messy email signatures you write yourself.

**B2. Literal categories.** Classify 10 tweets into `Literal["positive", "negative", "neutral"]` plus a `confidence: float` between 0 and 1 and a short `reason`.

**B3. Nested schema.** Extract a recipe from free text into:

```python
class Ingredient(BaseModel):
    name: str
    quantity: str
class Recipe(BaseModel):
    title: str
    servings: int
    ingredients: list[Ingredient]
    steps: list[str]
```

**B4. Raw JSON Schema.** Do B2 again using `output_config={"format": {"type": "json_schema", "schema": {...}}}` with a hand-written schema, then `json.loads` the text.

---

## Part C: Robustness and cost

**C1. Error handling.** Trigger and catch each: a wrong model ID (`NotFoundError` or `BadRequestError`), a wrong API key (`AuthenticationError`, temporarily pass `api_key="bad"`). Print friendly messages.

**C2. Token counting.** Use `client.messages.count_tokens` on a long text file (e.g. a Wikipedia article you saved). Estimate the cost of summarising 1,000 such articles with your chosen model.

**C3. Usage logger.** Write a function `ask(prompt, **kwargs) -> str` that calls the API and appends a row to `usage_log.csv` (timestamp, model, input tokens, output tokens, cost, latency, stop reason, request ID). Use it for the rest of the exercises.

**C4. Prompt caching.** Put a long (2,000+ word) document in the system prompt with `cache_control={"type": "ephemeral"}`. Ask 3 different questions in a row. Print `usage.cache_creation_input_tokens` and `usage.cache_read_input_tokens` for each call. What changes after the first call?

**C5. Async batch.** Summarise 10 short texts concurrently with `AsyncAnthropic`, `asyncio.gather` and a `Semaphore(3)`. Compare total time to doing them one after another.

**C6. Images.** Send a photo (a receipt, a chart, a whiteboard) and extract structured data with `messages.parse`.

---

## Part D: Mini-project: "Inbox Triage" automation (2–3 hours)

Build the system from Lesson 08 Section 3, end to end, and make it your own.

1. Write `data/emails.csv` with **25** realistic emails and expected categories (include angry, polite, multiple-issue, non-English, and 2 prompt-injection emails).
2. Implement `config.py`, `schema.py`, `prompts.py`, `llm.py`, `triage.py`.
3. Run it. Record accuracy, cost, average latency.
4. Make **two** improvements (prompt change, examples, schema field descriptions, model or effort change). Re-run after each and keep a table:

| Version | Change | Accuracy | Cost | Avg latency |
|---|---|---|---|---|
| v1 | baseline | | | |
| v2 | | | | |
| v3 | | | | |

5. Add a `--dry-run` flag that only counts tokens and estimates cost without calling `messages.create`.
6. README: problem, architecture diagram, results table, cost per 1,000 emails, limitations.

**Rubric (15 points):** structured outputs (3), stop-reason & error handling (2), usage/cost logging (2), eval with ≥ 25 cases (3), measured iterations table (3), README (2).

---

## Part E: Quiz (20 minutes)

1. What three things does every LLM API request contain?
   a) Model, messages, settings like max_tokens b) Temperature, top-p, seed only c) Image, audio, video d) Username, password, URL

2. Where should your API key live?
   a) In the model ID b) In a git-ignored `.env` loaded as an environment variable c) In the README d) In `first_call.py`

3. `response.content` is:
   a) A number b) A Pydantic model always c) A string d) A list of content blocks

4. `stop_reason == "max_tokens"` means:
   a) Perfect answer b) The model wants a tool c) The answer was cut off at your limit d) The model refused

5. Why must you re-send earlier messages each turn?
   a) It's optional b) The API is stateless: it doesn't remember c) To pay more d) To train the model

6. Streaming is mainly used to:
   a) Increase accuracy b) Reduce price c) Show text as it's generated and avoid timeouts on long outputs d) Encrypt data

7. Higher effort generally means:
   a) More thorough work and more tokens b) Less thinking and cheaper c) Faster responses always d) No change

8. The most reliable way to get output matching a schema is:
   a) Bold text b) Asking nicely c) High temperature d) Structured outputs (e.g. `messages.parse` with a Pydantic model)

9. Which error should you NOT retry?
   a) 529 overloaded b) 400 bad request c) Connection error d) 429

10. Prompt caching helps when:
    a) You use images b) You stream c) Every request is totally different d) A long prefix (system prompt/document) repeats across requests

11. The Batch API is best for:
    a) Large, non-urgent jobs at a discount b) Live chat c) Debugging d) Streaming

12. `client.messages.count_tokens` is used to:
    a) Count words in output b) Generate text c) Measure input tokens before sending d) Check rate limits

13. Why might sending `temperature` fail on some new models?
    a) It's always required b) Temperature only works with images c) It's a typo d) Some newest reasoning models don't allow changing it

14. A semaphore in async code:
    a) Stores the API key b) Speeds up the model c) Limits how many requests run at once d) Caches outputs

15. Best way to choose a model for a task:
    a) Random b) Measure quality, cost and latency on an eval and pick what meets the bar c) Always the cheapest d) Always the biggest

**Short answer.**

16. Write (from memory) the minimal Python code to call Claude and print the text answer.
17. Explain how a chatbot "remembers" earlier messages when the API is stateless.
18. Describe three ways to reduce API cost.
19. Why should all your LLM calls go through one wrapper function?
20. What would you log for every LLM call, and why?

---

## Answer Key

### Selected reference solutions

```python
# A1 + C3 helper
import time, csv, datetime, anthropic
from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic()
MODEL, PRICE_IN, PRICE_OUT = "claude-opus-5-5", 4.00, 20.00

def ask(prompt: str, **kwargs) -> str:
    t = time.perf_counter()
    r = client.messages.create(model=MODEL, max_tokens=kwargs.pop("max_tokens", 1024),
                               messages=[{"role": "user", "content": prompt}], **kwargs)
    cost = r.usage.input_tokens / 1e6 * PRICE_IN + r.usage.output_tokens / 1e6 * PRICE_OUT
    with open("usage_log.csv", "a", newline="") as f:
        csv.writer(f).writerow([datetime.datetime.now().isoformat(), MODEL, r.usage.input_tokens,
                                r.usage.output_tokens, round(cost, 6),
                                round(time.perf_counter() - t, 2), r.stop_reason, r._request_id])
    if r.stop_reason == "max_tokens":
        print("⚠️ Answer was cut off.")
    return next((b.text for b in r.content if b.type == "text"), "")

print(ask("Give me 3 fun facts about octopuses."))
```

```python
# A4/A5 - streaming chatbot with memory
messages, total = [], 0
while True:
    user = input("\nYou: ").strip()
    if user == "/quit": break
    if user == "/reset": messages.clear(); print("History cleared."); continue
    if user == "/tokens": print("Tokens so far:", total); continue
    messages.append({"role": "user", "content": user})
    print("Claude: ", end="")
    with client.messages.stream(model=MODEL, max_tokens=2000, messages=messages) as s:
        for text in s.text_stream:
            print(text, end="", flush=True)
        final = s.get_final_message()
    reply = next((b.text for b in final.content if b.type == "text"), "")
    messages.append({"role": "assistant", "content": reply})
    total += final.usage.input_tokens + final.usage.output_tokens
```

```python
# B2
from typing import Literal
from pydantic import BaseModel, Field

class Sentiment(BaseModel):
    label: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0, le=1)
    reason: str

r = client.messages.parse(model=MODEL, max_tokens=500, output_format=Sentiment,
                          messages=[{"role": "user", "content": "Tweet: 'Battery died after 2 hours. Again.'"}])
print(r.parsed_output)
```

```python
# C1
try:
    client.messages.create(model="claude-nonexistent", max_tokens=10,
                           messages=[{"role": "user", "content": "hi"}])
except anthropic.NotFoundError:
    print("That model ID doesn't exist. Check the model list.")
except anthropic.BadRequestError as e:
    print("Bad request:", e.message)

try:
    anthropic.Anthropic(api_key="bad").messages.create(model=MODEL, max_tokens=10,
                           messages=[{"role": "user", "content": "hi"}])
except anthropic.AuthenticationError:
    print("Your API key is invalid.")
```

```python
# C4 - expected pattern
# call 1: cache_creation_input_tokens ≈ size of the document, cache_read = 0
# calls 2-3: cache_creation = 0, cache_read_input_tokens ≈ size of the document → much cheaper
```

```python
# C5
import asyncio
aclient = anthropic.AsyncAnthropic()
sem = asyncio.Semaphore(3)

async def summarise(t):
    async with sem:
        r = await aclient.messages.create(model=MODEL, max_tokens=200,
                                          messages=[{"role": "user", "content": f"One-line summary:\n{t}"}])
        return next(b.text for b in r.content if b.type == "text")

async def run(texts):
    return await asyncio.gather(*(summarise(t) for t in texts))
# Concurrent total time ≈ (10 / 3) × one call, vs 10 × one call sequentially.
```

### Part E: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | a | 6 | c | 11 | a |
| 2 | b | 7 | a | 12 | c |
| 3 | d | 8 | d | 13 | d |
| 4 | c | 9 | b | 14 | c |
| 5 | b | 10 | d | 15 | b |

**16.**
```python
import anthropic
client = anthropic.Anthropic()
r = client.messages.create(model="claude-opus-5-5", max_tokens=1024,
                           messages=[{"role": "user", "content": "Hello!"}])
print(next(b.text for b in r.content if b.type == "text"))
```

**17.** The app stores every user and assistant message in a list and sends the entire list with each new request, so the model sees the whole conversation in its context window each time.

**18.** Use the smallest model/lowest effort that passes your eval; prompt caching for repeated prefixes; Batch API for non-urgent bulk work; shorter prompts/outputs and sensible `max_tokens`.

**19.** One place to add retries, logging, cost tracking, model config and error handling, so changes apply everywhere and swapping models is a one-line change.

**20.** Timestamp, model, prompt version, input/output tokens, cost, latency, stop reason, request ID (and, where privacy allows, the prompt and output). For debugging failures, tracking spend, spotting slowdowns, and comparing versions.

**Scoring:** out of 25. ≥ 21 move on.
