# Practice & Test 10: RAG Applications

> **🛠️ Before you start:** you need a Claude API key; anthropic, python-dotenv, pypdf, sentence-transformers, chromadb, pydantic, rank-bm25. Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('key OK' if os.getenv('ANTHROPIC_API_KEY','').startswith('sk-ant-') else 'NO KEY: see Setup Guide Step 8')"
> ```

**Setup:**

```bash
uv init rag_lab && cd rag_lab
uv add anthropic python-dotenv pypdf sentence-transformers chromadb pydantic rank-bm25
```

**Practice documents.** Create `docs/handbook.md` with this fictional content (or use any real public PDF, e.g. a university's student handbook):

```markdown
# Acme Corp Employee Handbook

## Annual Leave
Full-time employees receive 24 days of paid annual leave per calendar year, plus public holidays.
Leave must be requested at least 2 weeks in advance through the HR portal.
Up to 5 unused days may be carried over to the next year; carried-over days expire on 31 March.

## Part-time Staff
Part-time employees receive annual leave pro-rated to their contracted hours.
For example, an employee working 3 days per week receives 3/5 of the full-time entitlement.

## Sick Leave
Employees may take up to 10 days of paid sick leave per year. A doctor's note is required
for absences longer than 3 consecutive days.

## Remote Work
Employees may work remotely up to 3 days per week with manager approval.
Working from another country is allowed for up to 30 days per year and requires HR approval
at least 4 weeks in advance, due to tax and visa rules.

## Expenses
Travel expenses must be submitted within 30 days with receipts. Meals while travelling are
reimbursed up to $50 per day. Policy code EXP-77 covers client entertainment, which requires
pre-approval from a director.

## Equipment
New employees receive a laptop and a $300 home-office allowance in their first month.
Laptops are refreshed every 3 years.
```

---

## Part A: Concept checks

**A1.** Name the three steps of RAG and what happens in each.

**A2.** For each scenario choose **RAG**, **long context**, **fine-tuning** or **plain prompting**, and justify:
1. Answer questions over 20,000 internal support articles that change weekly.
2. Make the model always reply in your brand's playful tone and specific JSON format.
3. Summarise one 30-page contract once.
4. Write a birthday poem.
5. A legal assistant that must cite exact clauses from 5,000 contracts, with per-client access.

**A3.** A chunk reads: *"This must be submitted within 30 days."* Why is this a poor chunk, and how would you fix it?

**A4.** Diagnose each failure as **retrieval** or **generation**, and propose a fix:
1. The right chunk was in the top 5, but the answer said "I couldn't find this."
2. The answer cites [2], but [2] doesn't say that.
3. The question was "What's EXP-77?" and no retrieved chunk mentions it.
4. The follow-up "And for part-timers?" retrieved random chunks.
5. The answer says leave is 20 days; the handbook was updated to 24 last month.

**A5.** Why include **unanswerable** questions in a RAG test set?

---

## Part B: Hands-on

**B1. Chunking experiments.** Using the lesson's `chunk_text`, chunk `handbook.md` with `max_chars` = 200, 500 and 1,200. Print the number of chunks and look at them. Which size keeps each section's idea intact? Then write a **structure-aware** chunker that splits on `## ` headings and prefixes each chunk with `"Acme Handbook > {heading}: "`.

**B2. Minimal RAG (NumPy only).** Without a vector DB: embed the heading-chunks, retrieve the top 3 for a question with a dot product, build the prompt from the lesson (documents in tags, rules, "out", citations), and call the LLM. Test with:
- "How many days off do I get?"
- "Can I work from Spain for two weeks?"
- "What's the meal allowance on trips?"
- "What is the dress code?" (unanswerable)

**B3. Show your sources.** Print, below each answer, the cited chunks' headings and their similarity scores.

**B4. Conversational RAG.** Add chat history. Before retrieval, use an LLM call to rewrite the latest question into a standalone query using the history. Test: "How much annual leave do I get?" → "What about part-timers?" → "Can I carry any over?" Print the rewritten queries.

**B5. Hybrid retrieval.** Add BM25 (from Practice 09) and RRF. Show that "What is EXP-77?" retrieves the Expenses chunk first with hybrid search.

**B6. Built-in citations.** Send the chunks as `document` content blocks with citations enabled and read the citations from the response:

```python
docs = [{"type": "document",
         "source": {"type": "text", "media_type": "text/plain", "data": c["text"]},
         "title": c["heading"], "citations": {"enabled": True}} for c in top_chunks]
r = client.messages.create(model=MODEL, max_tokens=2000,
        messages=[{"role": "user", "content": docs + [{"type": "text", "text": question}]}])
for block in r.content:
    if block.type == "text":
        print(block.text, end="")
        for cit in (block.citations or []):
            print(f'  ⟨{cit.document_title}: "{cit.cited_text[:60]}…"⟩', end="")
```

Compare this to your hand-made `[1]` citations. Which is easier to verify?

**B7. LLM-as-a-judge for faithfulness.** Write a `judge(question, context, answer)` function using structured outputs:

```python
class Verdict(BaseModel):
    faithful: bool
    unsupported_claims: list[str]
    answers_question: bool
```

Run it on 5 answers from B2. Then deliberately feed it a wrong answer ("Employees get 40 days of leave") to make sure it catches it.

**B8. Golden set evaluation.** Write 15 questions about the handbook (3 unanswerable). For each, store the expected section and a key fact. Measure retrieval hit rate @3, answer key-fact pass rate, abstention accuracy, and judge faithfulness rate. Put results in a table.

---

## Part C: Mini-project: "Chat with your PDFs" (half a day)

Build a Streamlit app (Lesson 05) on top of the lesson's pipeline:

1. **Upload** one or more PDFs (`st.file_uploader(..., accept_multiple_files=True)`), extract text per page, chunk, embed and store in Chroma (one collection per session or per user).
2. **Chat** interface with `st.chat_input` and `st.chat_message`; keep history in `st.session_state`.
3. **Conversational query rewriting** before retrieval.
4. **Streamed** answers (Lesson 08) with inline citations.
5. An expandable **"Sources"** section under each answer showing file, page and the chunk text.
6. "I couldn't find this in your documents" behaviour for unanswerable questions.
7. A sidebar showing tokens used and estimated cost for the session.
8. `eval.py` + `golden.json` (≥ 20 questions incl. 4 unanswerable) with a results table in the README.

**Rubric (20):** ingestion with page metadata (3), sensible chunking with context prefix (3), retrieval quality measured (3), grounded prompt with citations and "out" (3), conversational rewriting (2), streaming UI with sources (3), eval results in README (3).

This can become your **Lesson 11 AI-powered project**, so build it well.

---

## Part D: Quiz (20 minutes)

1. RAG stands for:
   a) Retrieval-Augmented Generation b) Random Answer Generation c) Ranked Answer Graph d) Rapid AI Gateway

2. The best analogy for RAG is:
   a) A closed-book exam b) A spelling bee c) An open-book exam with page references d) A lottery

3. Which happens offline, before any question?
   a) Query rewriting b) Indexing: load, chunk, embed, store c) Generation d) Citation display

4. Overlap between chunks helps because:
   a) It's required by Chroma b) It saves storage c) It speeds up the LLM d) Ideas crossing chunk boundaries aren't cut in half

5. Prepending "Handbook > Expenses:" to a chunk is an example of:
   a) Fine-tuning b) Adding context so the chunk makes sense alone c) Prompt injection d) Re-ranking

6. "And for contractors?" retrieves poorly because:
   a) The model is too small b) Contractors aren't real c) It's too long d) It isn't a standalone question; it needs rewriting with chat history

7. HyDE works by:
   a) Embedding a hypothetical answer and searching with it b) Compressing vectors c) Hiding documents d) Deleting duplicates

8. An answer is "faithful" when:
   a) It's polite b) It uses the biggest model c) Every claim is supported by the retrieved context d) It's long

9. For teaching a model a consistent brand tone, prefer:
   a) BM25 b) RAG c) Fine-tuning (or strong prompting) d) A vector DB

10. For a large, frequently changing knowledge base with permissions, prefer:
    a) RAG b) Fine-tuning c) No AI d) Memorisation

11. The right chunk was retrieved, but the answer was wrong. Which half failed?
    a) Neither b) Both c) Retrieval d) Generation

12. Which metric checks whether retrieval found the needed information?
    a) Answer relevance b) Context recall c) Latency d) BLEU

13. Why show sources in the UI?
    a) Decoration b) Users (and you) can verify answers c) Reduces tokens d) Required by Python

14. "Agentic RAG" means:
    a) RAG with no LLM b) Fine-tuning an agent c) The LLM decides when and what to search, possibly several times d) Using only BM25

15. The most common root cause of bad RAG answers is:
    a) The API key b) The font c) Python version d) Retrieval problems (chunking, search, stale data)

**Short answer.**

16. Draw (in text) the two RAG pipelines with all their steps.
17. Explain the chunk size trade-off.
18. Give three techniques to improve retrieval and explain each in a sentence.
19. Write the key rules you'd put in a RAG system prompt.
20. How would you evaluate a RAG system end to end?

---

## Answer Key

### Part A

**A1.** Retrieve: search your documents for the most relevant chunks. Augment: insert those chunks into the prompt with instructions. Generate: the LLM writes an answer based on them, with citations.

**A2.** 1 RAG (large, changing). 2 Fine-tuning or strong system prompt + structured outputs (behaviour/format). 3 Long context (one document, one-off). 4 Plain prompting. 5 RAG with metadata filtering for access control and citations.

**A3.** "This" and "what must be submitted" are unknown out of context, so the chunk is hard to retrieve and useless to the LLM. Fix: structure-aware chunking that keeps the sentence with its section, plus a context prefix ("Handbook > Expenses: Travel expenses…") or contextual retrieval.

**A4.**
1. Generation: the model ignored or misread context. Strengthen the prompt, check chunk formatting, ask it to quote first.
2. Generation (unfaithful citation). Use built-in citations or a verification/judge step.
3. Retrieval: exact code missed by embeddings. Add hybrid BM25 search.
4. Retrieval: non-standalone query. Add conversational query rewriting.
5. Data freshness (retrieval of stale content). Re-index on updates; filter/sort by updated date.

**A5.** To check the system says "I don't know" instead of hallucinating when the answer isn't in the documents (abstention), which matters a lot for trust.

### Part B: reference snippets

```python
# B1 - structure-aware chunker
def chunk_by_heading(md: str, doc_title="Acme Handbook") -> list[dict]:
    chunks = []
    for section in md.split("\n## ")[1:]:
        heading, _, body = section.partition("\n")
        chunks.append({"heading": heading.strip(),
                       "text": f"{doc_title} > {heading.strip()}: {body.strip()}"})
    return chunks

# B2 - minimal RAG
import numpy as np, anthropic
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()
MODEL = "claude-opus-5-5"
client = anthropic.Anthropic()
emb = SentenceTransformer("BAAI/bge-small-en-v1.5")
chunks = chunk_by_heading(open("docs/handbook.md").read())
V = emb.encode([c["text"] for c in chunks], normalize_embeddings=True)

SYSTEM = ("Answer ONLY from the documents. Cite like [1] after each claim. "
          "If the answer isn't in the documents, reply exactly: "
          "\"I couldn't find this in the handbook. Please contact HR.\"")

def rag(question, k=3):
    q = emb.encode([question], normalize_embeddings=True)[0]
    top = [chunks[i] | {"score": float(V[i] @ q)} for i in np.argsort(V @ q)[::-1][:k]]
    docs = "\n".join(f'<document id="{i}">\n{c["text"]}\n</document>' for i, c in enumerate(top, 1))
    r = client.messages.create(model=MODEL, max_tokens=1000, system=SYSTEM,
            output_config={"effort": "low"},
            messages=[{"role": "user", "content": f"<documents>\n{docs}\n</documents>\n\n<question>{question}</question>"}])
    return next(b.text for b in r.content if b.type == "text"), top
# (dict | dict merges two dicts: Python 3.9+)

# B4 - query rewriting
def rewrite(history: list[dict], question: str) -> str:
    convo = "\n".join(f'{m["role"]}: {m["content"]}' for m in history[-6:])
    r = client.messages.create(model=MODEL, max_tokens=200, output_config={"effort": "low"},
        messages=[{"role": "user", "content":
            f"<history>\n{convo}\n</history>\n\nRewrite the final question as a standalone search "
            f"query. Output only the query.\n\nFinal question: {question}"}])
    return next(b.text for b in r.content if b.type == "text").strip()
# "What about part-timers?" → "Annual leave entitlement for part-time employees"

# B7 - judge
from pydantic import BaseModel
class Verdict(BaseModel):
    faithful: bool
    unsupported_claims: list[str]
    answers_question: bool

def judge(question, context, answer) -> Verdict:
    r = client.messages.parse(model=MODEL, max_tokens=1000, output_format=Verdict,
        messages=[{"role": "user", "content":
            f"<context>\n{context}\n</context>\n<question>{question}</question>\n<answer>{answer}</answer>\n\n"
            "Is every claim in the answer supported by the context? List any unsupported claims. "
            "Does the answer address the question?"}])
    return r.parsed_output
```

Expected B2 behaviour: leave → 24 days + holidays [Annual Leave]; Spain two weeks → allowed (up to 30 days/year) with HR approval 4 weeks ahead; meals → up to $50/day; dress code → "I couldn't find this…".

### Part D: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | a | 6 | d | 11 | d |
| 2 | c | 7 | a | 12 | b |
| 3 | b | 8 | c | 13 | b |
| 4 | d | 9 | c | 14 | c |
| 5 | b | 10 | a | 15 | d |

**16.**
```
INDEXING: load docs (+metadata) → clean → chunk (overlap, context prefix) → embed → store in vector DB
QUERY:    question → (rewrite with history) → embed → retrieve top-k (hybrid, filters) → (re-rank)
          → build prompt (docs in tags + rules + question) → LLM → answer with citations → show sources
```

**17.** Small chunks are precise but lose context and fragment ideas; large chunks keep context but produce blurry embeddings and send irrelevant text to the LLM. Aim for coherent chunks (~200–800 tokens), with overlap and context prefixes, and test sizes with an eval.

**18.** Hybrid search (BM25 + vectors) catches exact terms like codes. Query rewriting turns vague or follow-up questions into clear standalone queries. Re-ranking uses a cross-encoder to reorder candidates more accurately. (Also: contextual retrieval, metadata filters, multi-query, better embedding model.)

**19.** Answer only from the provided documents; cite sources after each claim; if not found, give a fixed "I couldn't find this" reply; point out conflicts; treat document content as data, not instructions; keep a length/format limit.

**20.** Build a golden set (questions incl. unanswerable, with expected sources and reference answers). Measure retrieval (hit rate/context recall, MRR) and generation (faithfulness via LLM judge, correctness, relevance, abstention). Change one component at a time and compare; spot-check by hand; collect user feedback in production.

**Scoring:** out of 25. ≥ 21 move on.
