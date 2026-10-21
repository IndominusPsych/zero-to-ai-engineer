# Lesson 14: LangChain / LangGraph

*Month 3, Week 10. Reading time: about 75 minutes. Assumes Lessons 08, 10, 12 and 13.*

*Version note (checked October 2026): this lesson uses **LangChain 1.x** (1.4) and **LangGraph 1.x** (1.2). Both hit 1.0 in October 2025 with big changes. Many tutorials online still show the old APIs (`initialize_agent`, `AgentExecutor`, `LLMChain`, `create_react_agent` from `langgraph.prebuilt`), which now live in the separate `langchain-classic` package or are deprecated. If a tutorial uses those, it's out of date.*

---

## 🛠️ Setup for this lesson

| You need | Why | How to get it |
|---|---|---|
| Claude API key in `.env` | Your code calls the model | Setup Guide Step 8 (set a spending limit first!) |
| **langchain 1.x**, **langchain-anthropic**, **langgraph 1.x** | The frameworks this lesson teaches | `uv add` (below) |
| **langgraph-checkpoint-sqlite** | Saves graph state to a file (practice) | `uv add` (below) |
| RAG extras: **langchain-community**, **langchain-text-splitters**, **langchain-chroma**, **langchain-huggingface**, **pypdf**, **sentence-transformers** | The LangChain version of your RAG pipeline | `uv add` (below) |
| Optional: **LangSmith** account | See every step of a run in a web UI | smith.langchain.com → API key → `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY=...` in `.env` |

**Install:**

```bash
cd ~/ai-engineer-projects
uv init lc_lab && cd lc_lab
uv add langchain langchain-anthropic langgraph langgraph-checkpoint-sqlite python-dotenv requests
uv add langchain-community langchain-text-splitters langchain-chroma langchain-huggingface pypdf sentence-transformers
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
```

**Check it works:**

```bash
uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('key OK' if os.getenv('ANTHROPIC_API_KEY','').startswith('sk-ant-') else 'NO KEY: see Setup Guide Step 8')"
uv run python -c "import langchain, langchain_anthropic; from importlib.metadata import version; print('langchain', langchain.__version__, '| langgraph', version('langgraph'))"
# Both must start with 1. If you see 0.x, run: uv add "langchain>=1" "langgraph>=1"
```

Old tutorials say `pip install langchain-openai` and use `AgentExecutor`. Ignore them: this lesson uses the 1.x APIs. To use OpenAI models instead, `uv add langchain-openai`.

Stuck? See the step-by-step instructions and the troubleshooting table in [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md).

---

## 1. The big picture

### What is this, in simple words?

In Lessons 08–13 you wrote everything by hand: API calls, message lists, retrieval, the agent loop, workflow state, approval steps. That's the best way to *understand* AI systems. But in real projects you'd rewrite the same plumbing again and again.

**LangChain** and **LangGraph** are open-source Python libraries (frameworks) that package this plumbing:

- **LangChain** gives you standard building blocks: a common interface to many model providers, tools, document loaders, text splitters, vector stores, and a one-line way to create an agent (`create_agent`).
- **LangGraph** is a lower-level framework for building **workflows and agents as graphs**: boxes (steps) connected by arrows (what happens next), with shared **state**, **checkpoints** (save and resume), and **human-in-the-loop** pauses built in.

LangChain's agents actually run *on top of* LangGraph.

Analogy: you've been building furniture by cutting your own planks and making your own screws. LangChain is a hardware store with standard parts that fit together. LangGraph is the assembly blueprint system: it lets you lay out complex builds step by step, pause halfway, and resume tomorrow exactly where you left off.

### Which field does it belong to?

These are **AI engineering frameworks**, part of the wider "LLM tooling" ecosystem, alongside alternatives such as LlamaIndex (strong for RAG), the OpenAI Agents SDK, the Claude Agent SDK, PydanticAI, CrewAI and Microsoft's agent frameworks.

### Why does it matter?

| Without a framework | With LangChain / LangGraph |
|---|---|
| Write your own loop, retries, message handling | `create_agent(model, tools)` |
| Different code for every provider | One interface: swap `"anthropic:..."` for `"openai:..."` |
| Build your own state, checkpoints, resume | Built in (`StateGraph`, checkpointers) |
| Hand-roll human approval pauses | `interrupt()` / human-in-the-loop middleware |
| Write loaders and splitters per file type | Hundreds of integrations |
| DIY tracing | LangSmith tracing with one environment variable |

They're among the most-requested skills in AI-engineering job posts. Knowing them, **and** knowing what they do underneath (which you now do), is a strong combination.

> **In simple words:** LangChain provides standard parts (models, tools, loaders, vector stores, a ready-made agent). LangGraph lets you build workflows and agents as graphs with shared state, saving, resuming and human approval. Because you built these by hand first, you'll understand exactly what they're doing.

---

## 2. Core concepts

### 2.1 Installing

```bash
uv add langchain langchain-anthropic langgraph
# optional integrations:
uv add langchain-openai langchain-chroma langchain-text-splitters langchain-community
```

LangChain is split into packages:

| Package | Contains |
|---|---|
| `langchain-core` | Base interfaces: messages, tools, runnables |
| `langchain` | Agents (`create_agent`), middleware, `init_chat_model` |
| `langchain-anthropic`, `langchain-openai`, … | **Integration packages** for each provider |
| `langchain-text-splitters`, `langchain-chroma`, `langchain-community` | Splitters, vector stores, many third-party integrations |
| `langgraph` | Graphs, state, checkpoints, interrupts |
| `langchain-classic` | Old (pre-1.0) chains and agents, for legacy code |

### 2.2 Chat models: one interface for many providers

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("anthropic:claude-opus-5-5")     # "provider:model-id"
reply = model.invoke("Explain LangGraph in one sentence.")
print(reply.content)
```

`init_chat_model` reads your `ANTHROPIC_API_KEY` from the environment. Swap providers by changing the string (e.g. `"openai:<model>"` after installing `langchain-openai`). `invoke` means "run this with this input"; you'll see it everywhere.

**Messages** are objects: `SystemMessage`, `HumanMessage` (the user), `AIMessage` (the model), `ToolMessage` (a tool result). You can also pass plain dicts like `{"role": "user", "content": "..."}`.

```python
reply = model.invoke([
    {"role": "system", "content": "You are a terse assistant."},
    {"role": "user", "content": "What's RAG?"},
])
for chunk in model.stream("Write a haiku about graphs"):   # streaming
    print(chunk.content, end="", flush=True)
```

Under the hood: exactly the `messages.create` call from Lesson 08.

### 2.3 Runnables and LCEL (a quick look)

In LangChain, models, prompts, parsers and retrievers are all **Runnables**: objects with `.invoke()`, `.stream()` and `.batch()`. You can pipe them together with `|`. This is called **LCEL** (LangChain Expression Language):

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You summarise text for a {audience}."),
    ("user", "{text}"),
])
chain = prompt | model | StrOutputParser()          # template → model → plain string
print(chain.invoke({"audience": "10-year-old", "text": "Photosynthesis is ..."}))
```

`ChatPromptTemplate` is a prompt template (Lesson 07) with `{placeholders}`. In LangChain 1.x, LCEL is still handy for small linear chains; for anything with branching, loops or state, use LangGraph.

### 2.4 Tools

Turn any type-hinted Python function with a docstring into a tool with the `@tool` decorator:

```python
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city. Use for any weather question."""
    ...  # your Lesson 12 implementation
```

LangChain reads the name, docstring and type hints to build the JSON Schema (Lesson 12) automatically: `get_weather.name`, `get_weather.description`, `get_weather.args`.

### 2.5 `create_agent`: the ready-made agent

```python
from langchain.agents import create_agent

agent = create_agent(
    model="anthropic:claude-opus-5-5",
    tools=[get_weather, convert_currency, calculate],
    system_prompt="You are a concise travel helper. Use tools; never guess numbers.",
)
result = agent.invoke({"messages": [{"role": "user", "content": "Weather in Lisbon and 500 USD in EUR?"}]})
print(result["messages"][-1].content)
```

That's the whole Lesson 12 agent loop: call model → run requested tools → feed results back → repeat until done. The result contains the full list of messages, so you can inspect every tool call.

`create_agent` also supports:

| Option | Does |
|---|---|
| `response_format=MyPydanticModel` | Ask for a structured final answer (result in `result["structured_response"]`). Check your model/provider is supported. |
| `checkpointer=...` | Remember conversations across calls (memory) using a thread ID |
| `middleware=[...]` | Plug-in behaviours around the loop (next section) |

### 2.6 Middleware: customising the agent loop

**Middleware** is code that runs at fixed points in the agent loop (before/after the model call, around tool calls), so you can add behaviour without rewriting the loop. LangChain 1.x ships useful ones:

| Middleware | What it adds |
|---|---|
| `HumanInTheLoopMiddleware` | Pause before chosen tools run so a person can approve, edit or reject |
| `SummarizationMiddleware` | Summarise old messages when the conversation gets long (context management, Lesson 12) |
| Others (PII redaction, retries, call limits…) | Check the docs for the current list |

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="anthropic:claude-opus-5-5",
    tools=[get_weather, book_hotel],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"book_hotel": True})],  # pause before booking
    checkpointer=InMemorySaver(),        # pausing requires saving state
)
```

How pausing and resuming works is explained with LangGraph below (2.12).

### 2.7 RAG building blocks

LangChain has standard pieces for Lesson 10's pipeline:

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs = PyPDFLoader("handbook.pdf").load()          # one Document per page, with metadata
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = splitter.split_documents(docs)            # metadata (source, page) is kept
```

A **Document** object has `page_content` (text) and `metadata` (dict). Vector-store integrations (e.g. `langchain-chroma`) take an **embeddings** object and expose `.similarity_search(query, k=5)` and `.as_retriever()`. You then expose retrieval as a **tool** so the agent can search when it decides to: that's **agentic RAG** (Lesson 10, 2.12).

```python
@tool
def search_handbook(query: str) -> str:
    """Search the employee handbook. Use for any question about company policy."""
    hits = vector_store.similarity_search(query, k=4)
    return "\n\n".join(f"[{d.metadata['source']} p.{d.metadata.get('page')}] {d.page_content}" for d in hits)
```

### 2.8 LangGraph: thinking in graphs

LangGraph models a workflow (Lesson 13) as a **graph**:

| Graph concept | Meaning | Lesson 13 equivalent |
|---|---|---|
| **State** | A shared typed dict passed through the graph | The `RunState` object |
| **Node** | A Python function: takes the state, returns updates | A workflow step |
| **Edge** | "After node A, go to node B" | Fixed order (chaining) |
| **Conditional edge** | A function that looks at the state and picks the next node | Gates and routing |
| **START / END** | Special entry and exit points | Beginning and end of `handle()` |
| **Cycle** | An edge back to an earlier node | Evaluator–optimiser loop, agent loop |

```
        START
          │
      ┌───▼────┐
      │ node A │
      └───┬────┘
          │ conditional edge: look at state
     ┌────┴─────┐
 ┌───▼───┐  ┌───▼───┐
 │node B │  │node C │──┐
 └───┬───┘  └───────┘  │ cycle back
     │          ▲──────┘
     ▼
    END
```

### 2.9 State and reducers

State is usually a `TypedDict` (a dict with declared key types):

```python
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    question: str
    notes: Annotated[list[str], add]      # a REDUCER: new values are appended, not overwritten
    answer: str
```

Each node returns a **partial update** (only the keys it changes). By default a returned value **replaces** the old one. A **reducer** (here `operator.add`, declared with `Annotated`) says how to **combine** updates instead, e.g. append to a list. This matters when parallel nodes write to the same key. For chat agents, LangGraph provides `MessagesState` with a built-in message-appending reducer.

### 2.10 Building and running a graph

```python
from langgraph.graph import StateGraph, START, END

def research(state: State) -> dict:
    return {"notes": [f"fact about {state['question']}"]}

def write(state: State) -> dict:
    return {"answer": " / ".join(state["notes"])}

builder = StateGraph(State)
builder.add_node("research", research)
builder.add_node("write", write)
builder.add_edge(START, "research")
builder.add_edge("research", "write")
builder.add_edge("write", END)
graph = builder.compile()                   # turns the blueprint into a runnable

print(graph.invoke({"question": "octopuses", "notes": [], "answer": ""}))
```

**Conditional edges** route based on state:

```python
def needs_more(state: State) -> str:
    return "research" if len(state["notes"]) < 3 else "write"

builder.add_conditional_edges("research", needs_more, {"research": "research", "write": "write"})
```

The third argument maps each returned label to a node name. A cycle like this needs a stopping condition; LangGraph also enforces a **recursion limit** (a maximum number of steps) as a safety net.

### 2.11 Checkpointers and threads: memory and resume

A **checkpointer** saves the state after every step. Runs are grouped into **threads** by a `thread_id`:

```python
from langgraph.checkpoint.memory import InMemorySaver

graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "user-42"}}
graph.invoke({"question": "octopuses", "notes": [], "answer": ""}, config)
print(graph.get_state(config).values)          # the saved state for this thread
```

What this gives you:

- **Conversation memory:** call again with the same `thread_id` and the agent remembers.
- **Resume after crashes:** state is saved after each node (Lesson 13 checkpointing, free).
- **Time travel:** inspect or replay earlier checkpoints for debugging.
- **Human-in-the-loop** (next).

`InMemorySaver` is for development (lost when the program ends). In production use a database-backed checkpointer, e.g. SQLite or Postgres (`langgraph-checkpoint-sqlite`, `langgraph-checkpoint-postgres`).

### 2.12 Interrupts: pausing for a human

Inside any node, call `interrupt(...)` to **pause** the graph and hand a question to your app. The state is saved by the checkpointer. Later, resume with `Command(resume=...)`, and the value you pass becomes the return value of `interrupt`:

```python
from langgraph.types import interrupt, Command

def approve(state: State) -> dict:
    decision = interrupt({"draft": state["answer"], "question": "Send this? (yes/no)"})
    return {"answer": state["answer"] if decision == "yes" else "REJECTED"}

# first run: stops at the interrupt
result = graph.invoke(initial_state, config)
print(result["__interrupt__"])                 # shows what the human needs to decide

# later (seconds or days): resume the same thread
graph.invoke(Command(resume="yes"), config)
```

This is the clean, production-grade version of the `input("Approve?")` you wrote in Lessons 12–13. Your web app can show the pending decision, and resume whenever the human clicks a button. The `HumanInTheLoopMiddleware` from 2.6 uses exactly this mechanism inside `create_agent`.

### 2.13 Streaming and observability

- `graph.stream(input, config, stream_mode="updates")` yields each node's update as it happens (great for progress UIs). `stream_mode="messages"` streams LLM tokens.
- **LangSmith** is LangChain's hosted platform for tracing, evals and monitoring. Set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY=...` and every run's steps, prompts, tool calls, tokens and latencies appear in its web UI. (Langfuse and Phoenix are open-source alternatives.)
- **LangGraph Studio** visualises your graph and lets you step through runs.

### 2.14 Framework or no framework?

| Use a framework when… | Write it yourself when… |
|---|---|
| You need many integrations (loaders, vector stores, providers) | It's one or two API calls |
| You want durable state, resume, human-in-the-loop, streaming out of the box | You need maximum control or minimal dependencies |
| Your team already uses it | You're learning fundamentals (as you did) |
| You want to swap providers easily | You rely on a brand-new provider feature the framework doesn't support yet |

A common professional stance: use **LangGraph** for orchestration (state, branching, persistence, approval) and keep each node's logic simple, often calling the provider SDK directly where you need the latest features.

> **In simple words:** `init_chat_model` gives one interface to any provider; `@tool` turns functions into tools; `create_agent` is the ready-made agent loop, extended with middleware like human approval and summarisation. LangGraph builds workflows as graphs of nodes and edges over shared typed state, with reducers, conditional edges, checkpointers (memory, resume, time travel), interrupts for humans, streaming, and LangSmith tracing.

---

## 3. How it works: rebuilding our systems with the frameworks

### Part A: The Travel Helper as a LangChain agent (from Lesson 12)

```python
# lc_agent.py
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
import tools as t                          # Lesson 12's tools.py (get_weather, convert_currency, calculate)

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Get current weather and a 3-day forecast for a city. Use for weather questions."""
    return t.get_weather(city)

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert money using today's rate. Use 3-letter codes like USD, EUR, INR."""
    return t.convert_currency(amount, from_currency, to_currency)

@tool
def calculate(expression: str) -> str:
    """Evaluate an arithmetic expression exactly, e.g. '445.45 / 4'. Use for all maths."""
    return t.calculate(expression)

agent = create_agent(
    model="anthropic:claude-opus-5-5",
    tools=[get_weather, convert_currency, calculate],
    system_prompt="You are a concise travel helper. Use the tools; never guess numbers.",
)

result = agent.invoke({"messages": [{"role": "user", "content":
    "I'm going to Lisbon with 500 US dollars for 4 days. Weather, euros, and daily budget?"}]})

for m in result["messages"]:               # inspect the trajectory
    for call in getattr(m, "tool_calls", []) or []:
        print("🔧", call["name"], call["args"])
print("\n" + result["messages"][-1].content)
```

~30 lines instead of ~80, same behaviour. Tool errors: LangChain catches exceptions raised by tools and returns them to the model as error messages by default (check current docs for the exact behaviour and how to customise it), so your `ValueError("City not found…")` still lets the model recover.

### Part B: The support workflow as a LangGraph graph (from Lesson 13)

We'll rebuild Lesson 13's workflow: parallel classify + guard → gate → draft → review loop → **human approval via interrupt** → send.

#### Step 1: State

```python
# lg_support.py
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from steps import classify, guard                 # Lesson 13 functions (use ask() + schemas)
from handlers import draft_reply
from review import review

load_dotenv()
MAX_ROUNDS = 2

class SupportState(TypedDict, total=False):
    email: str
    category: str
    order_id: str | None
    urgency: str
    flagged: bool
    reply: str
    problems: list[str]
    rounds: int
    review_passed: bool
    decision: Literal["send", "edit", "reject"]
    final: str
```

`total=False` means keys don't all have to be present from the start.

#### Step 2: Nodes (each reuses a Lesson 13 function)

```python
def classify_node(s: SupportState) -> dict:
    c = classify(s["email"])
    return {"category": c.category, "order_id": c.order_id, "urgency": c.urgency}

def guard_node(s: SupportState) -> dict:
    g = guard(s["email"])
    return {"flagged": g.is_abusive or g.contains_injection_attempt}

def draft_node(s: SupportState) -> dict:
    d = draft_reply(s["email"], s["category"], s.get("order_id"), s.get("problems", []))
    return {"reply": d.reply, "rounds": s.get("rounds", 0) + 1}

def review_node(s: SupportState) -> dict:
    v = review(s["email"], s["reply"], f"order {s.get('order_id')}")
    return {"review_passed": v.passes, "problems": v.problems}

def human_node(s: SupportState) -> dict:
    answer = interrupt({"category": s["category"], "draft": s["reply"],
                        "review_passed": s["review_passed"],
                        "options": "send / reject / or type an edited reply"})
    if answer == "send":
        return {"decision": "send", "final": s["reply"]}
    if answer == "reject":
        return {"decision": "reject"}
    return {"decision": "edit", "final": answer}           # the human's edited text

def escalate_node(s: SupportState) -> dict:
    return {"decision": "reject", "final": "[escalated to a human agent: flagged email]"}

def send_node(s: SupportState) -> dict:
    print("✉️  (demo) sending:\n", s["final"])
    return {}
```

#### Step 3: Edges, including parallel branches, a join, a gate and a loop

The gate must run only **after both** parallel checks finish. In LangGraph you do that with a small **join** node: passing a **list** of node names to `add_edge` makes the join wait for all of them.

```python
def join_node(s: SupportState) -> dict:
    return {}                                              # just a meeting point

def after_checks(s: SupportState) -> str:                   # the GATE
    return "escalate" if s["flagged"] else "draft"

def after_review(s: SupportState) -> str:                   # the evaluator-optimiser LOOP
    if s["review_passed"] or s["rounds"] > MAX_ROUNDS:
        return "human"
    return "draft"

def after_human(s: SupportState) -> str:
    return "send" if s["decision"] in ("send", "edit") else END

b = StateGraph(SupportState)
for name, fn in [("classify", classify_node), ("guard", guard_node), ("join", join_node),
                 ("draft", draft_node), ("review", review_node), ("human", human_node),
                 ("escalate", escalate_node), ("send", send_node)]:
    b.add_node(name, fn)

b.add_edge(START, "classify")              # two edges out of START → classify and guard run in PARALLEL
b.add_edge(START, "guard")
b.add_edge(["classify", "guard"], "join")  # waits for BOTH before running join
b.add_conditional_edges("join", after_checks, {"escalate": "escalate", "draft": "draft"})
b.add_edge("draft", "review")
b.add_conditional_edges("review", after_review, {"human": "human", "draft": "draft"})
b.add_conditional_edges("human", after_human, {"send": "send", END: END})
b.add_edge("send", END)
b.add_edge("escalate", END)

graph = b.compile(checkpointer=InMemorySaver())
```

#### Step 4: Run it, pause, and resume

```python
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "ticket-48213"}}
    result = graph.invoke({"email": "My order #48213 still hasn't arrived after 12 days. Where is it?"},
                          config)

    if "__interrupt__" in result:                          # paused at human_node
        pending = result["__interrupt__"][0].value
        print(f"\n[{pending['category']}] review passed: {pending['review_passed']}\n")
        print(pending["draft"])
        answer = input("\nsend / reject / or type an edited reply: ").strip()
        graph.invoke(Command(resume=answer), config)        # resumes exactly where it paused

    print("\nFinal state:", {k: v for k, v in graph.get_state(config).values.items() if k != "email"})
```

Because the checkpointer saved the state at the interrupt, the `resume` call could happen in a different process, minutes or days later (with a database checkpointer). That's how real approval queues work.

#### Step 5: See the graph

```python
print(graph.get_graph().draw_mermaid())     # paste the output into mermaid.live to see the diagram
```

**Mermaid** is a text format for diagrams; GitHub READMEs render it automatically. Great for documenting your project.

#### What changed vs Lesson 13

| Lesson 13 (hand-written) | Lesson 14 (LangGraph) |
|---|---|
| `ThreadPoolExecutor` for parallelism | Two edges from START + a join node |
| `if` statements for gate/loop | Conditional edges |
| `RunState` + manual JSONL log | `SupportState` + checkpointer (+ LangSmith tracing if enabled) |
| `input("Send?")` blocking the program | `interrupt()` / `Command(resume=...)`, resumable anytime |
| Loop counter in a `for` | `rounds` in state + conditional edge (+ recursion limit) |

The step logic (classify, guard, draft, review) didn't change at all: you reused Lesson 13's functions. **Frameworks orchestrate; your functions still do the work.**

```
 START ─┬─▶ classify ─┐
        └─▶ guard ────┴─▶ join ─▶ (flagged?) ──yes──▶ escalate ─▶ END
                                      │ no
                                      ▼
                                    draft ◀────────────┐
                                      │                │ problems & rounds ≤ 2
                                      ▼                │
                                    review ────────────┘
                                      │ passed or out of rounds
                                      ▼
                             human (interrupt ⏸ … resume ▶)
                                      │ send/edit          │ reject
                                      ▼                    ▼
                                    send ─▶ END           END
```

> **In simple words:** `create_agent` replaces your hand-written agent loop in a few lines. LangGraph turns your Lesson 13 workflow into nodes and edges over a typed state: parallel branches join before a gate, conditional edges make the review loop, and `interrupt` + checkpointer pause for human approval and resume later, all reusing your existing step functions.

---

## 4. Key terms (in order)

| Term | Plain meaning |
|---|---|
| **LangChain** | Framework of standard parts for LLM apps, including `create_agent`. |
| **LangGraph** | Framework for building workflows/agents as stateful graphs. |
| **langchain-classic** | Package holding the old pre-1.0 chains and agents. |
| **Integration package** | Provider-specific package, e.g. `langchain-anthropic`. |
| **`init_chat_model`** | One function to create a chat model for any provider (`"provider:model"`). |
| **`invoke` / `stream` / `batch`** | Run once / stream output / run on many inputs. |
| **Message types** | `SystemMessage`, `HumanMessage`, `AIMessage`, `ToolMessage`. |
| **Runnable** | Any LangChain object with invoke/stream/batch. |
| **LCEL** | Piping runnables with `|` (prompt \| model \| parser). |
| **ChatPromptTemplate** | A prompt template with placeholders. |
| **Output parser** | Converts model output into a string or structure. |
| **`@tool`** | Decorator that turns a function into a tool. |
| **`create_agent`** | LangChain's ready-made agent loop. |
| **Middleware** | Plug-in code that runs at points in the agent loop. |
| **Document / loader / text splitter** | Text+metadata object / reads files / chunks text. |
| **Vector store / retriever** | LangChain wrapper around a vector DB / an object that returns relevant documents. |
| **Graph / node / edge** | Workflow diagram / step function / connection. |
| **Conditional edge** | Picks the next node based on state. |
| **START / END** | Entry and exit points. |
| **Cycle** | An edge back to an earlier node (loops). |
| **TypedDict** | A dict type with declared keys and value types. |
| **Reducer** | Rule for combining state updates (e.g. append). |
| **MessagesState** | Built-in state with a messages list and append reducer. |
| **compile** | Turn a graph blueprint into a runnable app. |
| **Recursion limit** | Max number of steps in a graph run. |
| **Checkpointer / thread / thread_id** | Saves state after each step / a run's saved history / its ID. |
| **Time travel** | Inspecting or replaying earlier checkpoints. |
| **interrupt / Command(resume=...)** | Pause for human input / continue with their answer. |
| **Join node** | A node that waits for parallel branches. |
| **stream_mode** | What to stream: node updates or LLM tokens. |
| **LangSmith / LangGraph Studio** | Tracing/eval platform / visual graph debugger. |
| **Mermaid** | Text-based diagram format. |

> **In simple words:** Models, tools, agent, middleware (LangChain); state, nodes, edges, checkpointer, interrupt (LangGraph).

---

## 5. The people involved

| Who | What they do | Day to day |
|---|---|---|
| **AI engineers** | Build with the frameworks | Compose graphs, write nodes and tools, configure checkpointers, trace runs in LangSmith. |
| **LangChain, Inc.** (company behind LangChain, LangGraph, LangSmith) | Maintain the open-source libraries and sell hosted tools | Ship releases, docs, deployment and observability platforms. |
| **Open-source contributors** | Build integrations | Hundreds of provider, loader and vector-store packages. |
| **Platform teams** | Run graphs in production | Postgres checkpointers, queues for approvals, scaling, monitoring. |
| **Reviewers / operators** | Respond to interrupts | Approve, edit, reject AI actions through an app UI. |
| **Hiring managers** | Screen candidates | "LangChain/LangGraph" appears in many job ads; they'll also check you understand what's underneath. |

> **In simple words:** Engineers compose graphs, LangChain Inc. and the community maintain the ecosystem, platform teams run it, and humans answer the interrupts.

---

## 6. Common misconceptions and beginner mistakes

| Myth / mistake | Reality / fix |
|---|---|
| Following pre-2025 tutorials (`initialize_agent`, `AgentExecutor`, `LLMChain`) | Use `create_agent` and LangGraph 1.x; old APIs live in `langchain-classic`. |
| "LangChain does magic; I don't need to understand LLM APIs." | It wraps the same calls you wrote. When something breaks, Lessons 08–13 knowledge is how you debug it. |
| Using LCEL chains for complex branching | Use LangGraph for branching, loops, state and persistence. |
| Forgetting the checkpointer when using interrupts or memory | Interrupts and threads need a checkpointer (`InMemorySaver` in dev, a DB in prod). |
| Reusing the same `thread_id` for different users | One thread per conversation/ticket; mixing them leaks context. |
| Nodes returning the whole state or mutating it | Return only the keys you change. |
| Parallel nodes overwriting the same key | Use a reducer (e.g. `Annotated[list, add]`) or separate keys. |
| Running a gate before parallel branches finish | Join the branches (`add_edge([a, b], "join")`). |
| Infinite cycles | Stopping conditions in state + recursion limit. |
| Ignoring tracing | Turn on LangSmith (or Langfuse) early; graphs are hard to debug blind. |
| Pinning nothing | Pin versions in `pyproject.toml`/`uv.lock`; these libraries move fast. |

> **In simple words:** Use the 1.x APIs, understand what's underneath, use LangGraph for anything non-linear, always configure a checkpointer for memory/interrupts, join parallel branches, cap cycles, trace everything, pin versions.

---

## 7. One-page recap

### The 10 things to remember

1. **LangChain = standard parts; LangGraph = stateful graphs.** LangChain agents run on LangGraph.
2. **Use the 1.x APIs** (`create_agent`, `init_chat_model`, `@tool`); old ones are in `langchain-classic`.
3. **`init_chat_model("provider:model")`** gives one interface across providers.
4. **`@tool`** builds schemas from type hints + docstrings.
5. **`create_agent(model, tools, system_prompt, middleware, checkpointer)`** = the Lesson 12 loop.
6. **Middleware** adds human approval, summarisation and more without rewriting the loop.
7. **LangGraph: State (TypedDict) + nodes + edges + conditional edges**, with reducers for merging.
8. **Checkpointers + thread IDs** give memory, resume and time travel.
9. **`interrupt()` + `Command(resume=...)`** = durable human-in-the-loop.
10. **Frameworks orchestrate; your functions do the work.** Trace with LangSmith, pin versions.

### Cheat sheet

```python
model = init_chat_model("anthropic:claude-opus-5-5"); model.invoke("hi")
@tool
def f(x: str) -> str: """Docstring = description."""
agent = create_agent(model="anthropic:claude-opus-5-5", tools=[f], system_prompt="...",
                     middleware=[HumanInTheLoopMiddleware(interrupt_on={"f": True})],
                     checkpointer=InMemorySaver())
agent.invoke({"messages": [{"role": "user", "content": "..."}]}, {"configurable": {"thread_id": "1"}})

b = StateGraph(State); b.add_node("a", a); b.add_edge(START, "a")
b.add_conditional_edges("a", route, {"x": "x", "y": "y"}); b.add_edge(["x", "y"], "join")
g = b.compile(checkpointer=InMemorySaver())
r = g.invoke(state, cfg); r["__interrupt__"]; g.invoke(Command(resume="yes"), cfg)
```

### What to learn next

➡️ **Lesson 15: AI Automation.** You can build agents and workflows. Next: making them run **on their own**, on schedules and triggers, connected to email, spreadsheets, Slack and webhooks, plus building your own MCP server.
