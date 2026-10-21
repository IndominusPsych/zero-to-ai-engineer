# Practice & Test 14: LangChain / LangGraph

> **🛠️ Before you start:** you need a Claude API key; langchain 1.x, langchain-anthropic, langgraph 1.x, langgraph-checkpoint-sqlite and the RAG extras; optional LangSmith key. Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('key OK' if os.getenv('ANTHROPIC_API_KEY','').startswith('sk-ant-') else 'NO KEY: see Setup Guide Step 8')"
> ```

**Setup:**

```bash
uv init lc_lab && cd lc_lab
uv add langchain langchain-anthropic langgraph python-dotenv requests
uv add langchain-community langchain-text-splitters langchain-chroma pypdf sentence-transformers langchain-huggingface
```

Copy Lesson 12's `tools.py` and Lesson 13's `llm.py`, `schemas.py`, `steps.py`, `handlers.py`, `review.py`, `orders.py` into this folder.

⚠️ Check versions with `uv pip list | grep -i lang`. This file assumes LangChain 1.x and LangGraph 1.x.

**Tip:** you can build and test any LangGraph graph **without an API key** by using plain Python functions as nodes. Do that first, then plug in LLM calls.

---

## Part A: Concept checks

**A1.** Match each need to the right tool: `init_chat_model`, `@tool`, `create_agent`, `HumanInTheLoopMiddleware`, `StateGraph`, conditional edge, checkpointer, `interrupt`, reducer, LangSmith.
1. Pause a graph until a manager approves.
2. Swap Claude for another provider with one string change.
3. Remember a user's conversation across requests.
4. Let two parallel nodes both add items to the same list.
5. See every prompt, tool call and latency for a run in a web UI.
6. Route to "escalate" or "draft" based on a flag in state.
7. Turn a docstring-ed function into a tool schema.
8. A ready-made agent loop.
9. Require approval before a specific tool runs inside `create_agent`.
10. Build a custom workflow with typed shared state.

**A2.** A tutorial uses `from langchain.agents import initialize_agent, AgentExecutor`. What do you conclude, and what do you use instead?

**A3.** Two parallel nodes both return `{"notes": [...]}` and the state key is a plain `list[str]`. What goes wrong? Fix it.

**A4.** Why do interrupts require a checkpointer?

**A5.** When would you choose an LCEL chain, `create_agent`, or a custom `StateGraph`?

---

## Part B: Hands-on

**B1. Chat models.** Use `init_chat_model("anthropic:claude-opus-5-5")` to (a) invoke with a string, (b) invoke with a system + user message list, (c) stream a haiku token by token, (d) `batch` three questions at once.

**B2. LCEL chain.** Build `prompt | model | StrOutputParser()` that rewrites text for a chosen audience. Run it for "a 7-year-old" and "a lawyer."

**B3. Tools + create_agent.** Rebuild the Travel Helper (Lesson 14 Part A). Print the trajectory (each tool call and args). Then add `get_local_time` from Practice 12.

**B4. Memory.** Add `checkpointer=InMemorySaver()` to the agent and use `{"configurable": {"thread_id": "me"}}`. Tell it "I'm flying to Tokyo"; next call ask "What's the weather where I'm going?" Then try a different `thread_id`. What happens?

**B5. Human-in-the-loop middleware.** Add a `book_hotel` tool guarded by `HumanInTheLoopMiddleware(interrupt_on={"book_hotel": True})`. Ask the agent to book something. Inspect `result["__interrupt__"]`, then resume with an approve decision, and separately with a reject decision. (Look up the exact resume payload format in the current LangChain human-in-the-loop docs; at the time of writing it's a `Command(resume={"decisions": [{"type": "approve"}]})`-style object.)

**B6. Your first graph (no LLM).** Build a `StateGraph` for a "number guessing referee": state `{secret, guess, attempts, message}`; nodes `check` and `hint`; a conditional edge loops back until correct or `attempts >= 5`. Use `interrupt()` in a `get_guess` node to ask the human for each guess, and a checkpointer. Run it in the terminal with a loop of `invoke(Command(resume=...))`.

**B7. Reducers.** Build a graph with two parallel nodes `pros` and `cons` that each add 3 strings to `points: Annotated[list[str], add]`, then a `summarise` node after a join. Confirm all 6 points arrive.

**B8. The support workflow graph.** Build Lesson 14 Part B. First test it with **stub** functions (fake classify/guard/draft/review that return fixed values) so you can check every path: normal → send; flagged → escalate; review fails twice → human anyway; human types an edit → send edited text. Then switch to the real Lesson 13 functions.

**B9. Visualise and trace.** Print `graph.get_graph().draw_mermaid()` and paste into mermaid.live (or a GitHub README). Then create a free LangSmith account, set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY`, rerun B8, and find the trace.

**B10. Persistent checkpoints.** `uv add langgraph-checkpoint-sqlite`. Replace `InMemorySaver` with a SQLite saver (see the package docs for the current import and constructor). Start a ticket, stop the program at the interrupt, start a **new** Python process, and resume the same `thread_id`.

**B11. Agentic RAG with LangChain parts.** Load the Practice 10 handbook with a LangChain loader, split with `RecursiveCharacterTextSplitter`, store in a LangChain Chroma vector store (with `HuggingFaceEmbeddings("BAAI/bge-small-en-v1.5")` from `langchain-huggingface`), wrap search as a `@tool`, and give it to `create_agent`. Ask a question needing two searches ("Compare sick leave and annual leave rules").

---

## Part C: Mini-project: "Research Assistant Graph" (half a day)

Build a LangGraph app that writes a short, cited research brief on a question, using your own documents (Lesson 10 index) and optionally web search.

**Graph design (required):**

```
START ─▶ plan (LLM: 2–4 sub-questions, structured) ─▶ research (one node per sub-question, run in parallel via
         the Send API or a loop node) ─▶ join ─▶ write (LLM, cites sources) ─▶ critique (LLM rubric)
         ─▶ [passes or rounds > 2] ─▶ human (interrupt: approve / request changes) ─▶ END
                     └─ else ─▶ write (revise)
```

(For a dynamic number of parallel branches, look up LangGraph's **`Send`** API in the docs: it lets a node fan out to N copies of another node. Or keep it simple with one `research` node that loops over sub-questions.)

Requirements:
1. Typed state with a reducer for collected notes.
2. Checkpointer + thread IDs; interrupt for human approval with the option to type change requests (which go back to `write`).
3. Structured outputs for plan and critique.
4. Recursion limit and round limit.
5. Mermaid diagram in the README.
6. Eval: 5 questions; report critique pass rate in round 0, average rounds, cost, time; include one LangSmith (or Langfuse) trace screenshot.

**Rubric (20):** correct graph structure (5), state & reducers (3), structured outputs (3), interrupt/resume with changes (4), limits (2), README + eval (3).

---

## Part D: Quiz (20 minutes)

1. LangChain's 1.x recommended way to create an agent is:
   a) `LLMChain` b) `initialize_agent` c) `AgentExecutor` d) `create_agent`

2. What does `init_chat_model("anthropic:claude-opus-5-5")` give you?
   a) A chat model with a standard interface b) An embedding model c) A graph d) A vector store

3. The `@tool` decorator builds a tool's schema from:
   a) The API key b) The function's type hints and docstring c) A YAML file d) The model

4. Middleware in `create_agent` is used to:
   a) Replace the model b) Speed up Python c) Add behaviours (approval, summarisation…) at points in the agent loop d) Store vectors

5. In LangGraph, a node is:
   a) A database b) A function that takes state and returns updates c) An API key d) A token

6. A conditional edge:
   a) Deletes state b) Always goes to END c) Chooses the next node based on the state d) Runs nodes in parallel

7. A reducer specifies:
   a) How to combine updates to a state key (e.g. append) b) Model temperature c) How to shrink prompts d) Token limits

8. To wait for two parallel branches before continuing, you:
   a) Use two graphs b) Add a sleep c) Can't d) Add an edge from a list of both nodes to a join node

9. A checkpointer enables:
   a) Memory across calls, resume after failure, and interrupts b) Tool schemas c) Faster tokens d) Embeddings

10. `thread_id` identifies:
    a) The user's password b) The model c) A CPU thread d) One conversation/run history in the checkpointer

11. `interrupt()` inside a node:
    a) Deletes the checkpoint b) Pauses the graph and returns a question to your app until resumed c) Restarts the run d) Crashes the graph

12. You resume an interrupted graph with:
    a) `graph.restart()` b) `interrupt(False)` c) `graph.invoke(Command(resume=value), config)` d) A new thread_id

13. LangSmith is used for:
    a) Hosting vector DBs only b) Writing prompts automatically c) Training models d) Tracing, evaluation and monitoring of runs

14. Old pre-1.0 chains and agents now live in:
    a) They were deleted with no replacement b) `langchain-classic` c) `langchain-core` d) `langgraph`

15. Which statement is true?
    a) Frameworks orchestrate; your node functions still do the work, so understanding the underlying API helps debugging b) Frameworks remove the need to understand LLM APIs c) LangGraph can't do loops d) Checkpointers are only for production

**Short answer.**

16. Explain the difference between LangChain and LangGraph.
17. Describe the parts of a LangGraph graph (state, nodes, edges, conditional edges, START/END).
18. How does human-in-the-loop work in LangGraph, step by step?
19. Give two reasons to use a framework and two reasons not to.
20. What would you check first if a tutorial's LangChain code fails with an ImportError?

---

## Answer Key

### Part A

**A1.** 1 `interrupt` (+ checkpointer) · 2 `init_chat_model` · 3 checkpointer (+ thread_id) · 4 reducer · 5 LangSmith · 6 conditional edge · 7 `@tool` · 8 `create_agent` · 9 `HumanInTheLoopMiddleware` · 10 `StateGraph`.

**A2.** The tutorial predates LangChain 1.0 (Oct 2025). Use `from langchain.agents import create_agent` (or build a LangGraph graph). Legacy code can use `langchain-classic`.

**A3.** Without a reducer, both nodes write the same key in the same step, which conflicts (LangGraph raises an error about concurrent updates) or one overwrites the other. Fix: `notes: Annotated[list[str], operator.add]`.

**A4.** The graph must save its exact state at the pause so it can continue later, possibly in another process. The checkpointer stores that state under the thread ID.

**A5.** LCEL: short linear transformations (prompt → model → parser). `create_agent`: a standard tool-using agent loop with optional middleware. `StateGraph`: custom workflows with branching, loops, parallelism, persistence and human approval.

### Part B: reference snippets

```python
# B1
from langchain.chat_models import init_chat_model
model = init_chat_model("anthropic:claude-opus-5-5")
print(model.invoke("Hi").content)
print(model.invoke([{"role": "system", "content": "Be terse."},
                    {"role": "user", "content": "What is LangGraph?"}]).content)
for c in model.stream("A haiku about graphs"): print(c.content, end="", flush=True)
print([m.content for m in model.batch(["2+2?", "Capital of Peru?", "Opposite of hot?"])])

# B6 - guessing referee (no LLM needed)
import random
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

class G(TypedDict):
    secret: int
    guess: int
    attempts: int
    message: str

def get_guess(s: G) -> dict:
    return {"guess": int(interrupt(s.get("message", "Guess 1-20"))), "attempts": s["attempts"] + 1}

def check(s: G) -> dict:
    if s["guess"] == s["secret"]:
        return {"message": f"Correct in {s['attempts']}!"}
    return {"message": "Too high" if s["guess"] > s["secret"] else "Too low"}

def route(s: G) -> str:
    return END if s["guess"] == s["secret"] or s["attempts"] >= 5 else "get_guess"

b = StateGraph(G)
b.add_node("get_guess", get_guess); b.add_node("check", check)
b.add_edge(START, "get_guess"); b.add_edge("get_guess", "check")
b.add_conditional_edges("check", route, {"get_guess": "get_guess", END: END})
g = b.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "game1"}}
r = g.invoke({"secret": random.randint(1, 20), "attempts": 0, "guess": 0, "message": "Guess 1-20"}, cfg)
while "__interrupt__" in r:
    r = g.invoke(Command(resume=input(r["__interrupt__"][0].value + " > ")), cfg)
print(r["message"])

# B7 - reducer
from typing import Annotated
from operator import add
class P(TypedDict):
    topic: str
    points: Annotated[list[str], add]
    summary: str
def pros(s): return {"points": [f"pro {i}" for i in range(3)]}
def cons(s): return {"points": [f"con {i}" for i in range(3)]}
def summarise(s): return {"summary": f"{len(s['points'])} points"}
b = StateGraph(P)
for n, f in [("pros", pros), ("cons", cons), ("summarise", summarise)]: b.add_node(n, f)
b.add_edge(START, "pros"); b.add_edge(START, "cons")
b.add_edge(["pros", "cons"], "summarise"); b.add_edge("summarise", END)
print(b.compile().invoke({"topic": "remote work", "points": [], "summary": ""})["summary"])  # 6 points
```

**B4 expected:** same thread → it remembers Tokyo; new thread → it doesn't know where you're going.

### Part D: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | d | 6 | c | 11 | b |
| 2 | a | 7 | a | 12 | c |
| 3 | b | 8 | d | 13 | d |
| 4 | c | 9 | a | 14 | b |
| 5 | b | 10 | d | 15 | a |

**16.** LangChain provides standard components (chat models, tools, loaders, splitters, vector stores) and a ready-made agent (`create_agent`). LangGraph is the lower-level orchestration framework for building custom workflows and agents as stateful graphs with persistence and human-in-the-loop. LangChain's agents run on LangGraph.

**17.** State: a typed dict shared across steps. Nodes: functions that read state and return partial updates. Edges: fixed transitions. Conditional edges: functions choosing the next node from state. START/END: entry and exit. Cycles allow loops.

**18.** Compile with a checkpointer → invoke with a thread_id → a node calls `interrupt(payload)` → the run stops and returns `__interrupt__` with the payload; state is saved → your app shows it to a human → later, `invoke(Command(resume=answer), same config)` continues and `interrupt` returns the answer.

**19.** For: many ready integrations; built-in state/persistence/interrupts/streaming/tracing; easy provider swapping. Against: extra dependency and abstraction; fast-moving APIs; may lag new provider features; overkill for one or two calls.

**20.** Check the installed versions and whether the tutorial uses pre-1.0 APIs (e.g. `initialize_agent`, `AgentExecutor`, `LLMChain`, `langgraph.prebuilt.create_react_agent`); find the 1.x equivalent in current docs, or install `langchain-classic` for legacy code; make sure the integration package (e.g. `langchain-anthropic`) is installed.

**Scoring:** out of 25. ≥ 21 move on.
