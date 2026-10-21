# Lesson 10: RAG Applications

*Month 2, Weeks 7–8. Reading time: about 75 minutes. Assumes Lessons 06–09.*

---

## 🛠️ Setup for this lesson

| You need | Why | How to get it |
|---|---|---|
| Everything from Lessons 08–09 | API key, embeddings, Chroma | Setup Guide Steps 8–9 |
| Claude API key in `.env` | Your code calls the model | Setup Guide Step 8 (set a spending limit first!) |
| **pypdf** | Read text out of PDF files | `uv add` (below) |
| **anthropic**, **python-dotenv**, **sentence-transformers**, **chromadb**, **pydantic**, **rank-bm25** | Generation, retrieval, structured outputs, hybrid search | `uv add` (below) |
| A document or two to ask questions about | Your knowledge base | The practice file gives you one; any public PDF works too |

**Install:**

```bash
cd ~/ai-engineer-projects
uv init rag_lab && cd rag_lab
uv add anthropic python-dotenv pypdf sentence-transformers chromadb pydantic rank-bm25
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
mkdir docs              # put your .md / .pdf files here
```

**Check it works:**

```bash
uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('key OK' if os.getenv('ANTHROPIC_API_KEY','').startswith('sk-ant-') else 'NO KEY: see Setup Guide Step 8')"
uv run python -c "import pypdf, chromadb, sentence_transformers; print('RAG stack OK')"
```

Stuck? See the step-by-step instructions and the troubleshooting table in [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md).

---

## 1. The big picture

### What is this, in simple words?

**RAG** stands for **Retrieval-Augmented Generation**. It's a simple but powerful idea:

1. **Retrieve:** when a user asks a question, *search* your own documents for the most relevant passages (Lesson 09).
2. **Augment:** paste those passages into the prompt (Lesson 07).
3. **Generate:** ask the LLM to answer **using those passages** (Lesson 08).

Analogy: an **open-book exam**. A student who answers from memory may forget or make things up (that's an LLM hallucinating). A student allowed to look things up in the textbook, and required to point to the page, gives accurate, checkable answers. RAG turns the LLM into the open-book student, and your documents are the textbook.

```
 user question ──▶ RETRIEVE relevant chunks ──▶ AUGMENT the prompt with them ──▶ GENERATE a grounded, cited answer
                  (vector / hybrid search)       (<documents> + question)         (LLM API)
```

### Which field does it belong to?

RAG sits at the meeting point of **information retrieval** (search) and **generative AI** (LLMs). It's the most widely deployed pattern in **AI engineering**: probably the first thing a company builds with LLMs.

### Why does it matter?

From Lesson 06, LLMs have three big limits. RAG addresses all three:

| LLM limit | How RAG helps |
|---|---|
| **Knowledge cutoff:** doesn't know recent info | Retrieve today's documents |
| **No private knowledge:** never saw your company's files | Retrieve from your own data |
| **Hallucination:** invents plausible answers | Answer only from retrieved text, with citations you can check |

Plus practical benefits:

- **Update knowledge instantly:** change a document and re-index it; no model retraining.
- **Access control:** only retrieve what each user may see.
- **Cheaper than stuffing everything into the context window:** send 5 relevant chunks, not 500 pages.

**Real examples:** "chat with your docs" tools, customer-support assistants, internal HR/IT helpdesks, legal and medical research assistants, coding assistants that search your codebase.

> **In simple words:** RAG = search your documents, paste the best passages into the prompt, and have the LLM answer from them with citations. It gives LLMs fresh, private, checkable knowledge.

---

## 2. Core concepts

### 2.1 The two halves of every RAG system

A RAG system has two separate pipelines:

```
 ┌─────────────── INDEXING (offline, done ahead of time) ────────────────┐
 │ load documents → clean → split into chunks → embed → store in vector DB │
 └──────────────────────────────────────────────────────────────────────────┘

 ┌─────────────── QUERYING (online, every question) ─────────────────────────────┐
 │ question → (rewrite) → embed → retrieve top-k → (re-rank) → build prompt → LLM → answer + citations │
 └───────────────────────────────────────────────────────────────────────────────────┘
```

Indexing is also called **ingestion**. It runs once, then again whenever documents change.

### 2.2 Loading documents

Your knowledge lives in many formats: PDFs, Word files, web pages, Markdown, Notion, Google Drive, databases, support tickets. A **document loader** reads a format and extracts plain text plus metadata.

| Format | Python tool |
|---|---|
| PDF | `pypdf` (simple), `pymupdf` (faster, better layout), or services that handle scanned PDFs with **OCR** (Optical Character Recognition: reading text from images) |
| Word (.docx) | `python-docx` |
| HTML / web pages | `requests` + `beautifulsoup4`, or `trafilatura` (extracts the main article text) |
| Many formats at once | `unstructured`, `docling`, or framework loaders (LangChain/LlamaIndex) |

Always keep **metadata**: source file, page number, section title, URL, last-updated date, access permissions. You need these for citations, filtering and freshness.

**Cleaning** removes junk: repeated headers/footers, page numbers, cookie banners, navigation menus, broken line breaks. Garbage in your chunks means garbage in the answers.

### 2.3 Chunking: the most important design choice

**Chunking** means splitting documents into smaller pieces (**chunks**) before embedding. Why (recap of Lesson 09): one vector per long document blurs its topics; small focused chunks match specific questions; and you only want to send relevant text to the LLM.

**Chunk size trade-off:**

| Too small (e.g. 1 sentence) | Just right | Too large (e.g. 10 pages) |
|---|---|---|
| Loses context ("it" refers to what?) | A coherent idea with its context | Blurry embedding, irrelevant text sent to LLM |
| Many fragments to retrieve | Typically ~200–800 tokens | Fewer chunks fit in the prompt |

**Overlap** repeats a little text between neighbouring chunks (e.g. 10–20%) so ideas that cross a boundary aren't cut in half.

```
 Document: [=========================================================]
 Chunk 1:  [==========]
 Chunk 2:          [==========]        ← overlap region shared with chunk 1
 Chunk 3:                  [==========]
```

**Chunking strategies:**

| Strategy | How | When |
|---|---|---|
| **Fixed-size** | Every N tokens/characters, with overlap | Simple baseline |
| **Recursive** | Split by paragraphs; if too big, by sentences; if still too big, by words | A great default for prose |
| **Structure-aware** | Split on headings, sections, list items, table rows, code functions | Manuals, policies, docs, code: best when structure exists |
| **Semantic** | Start a new chunk where the topic changes (embedding similarity drops) | Long unstructured text |

**Add context to each chunk.** A chunk saying *"The limit is 30 days"* is useless alone: limit of what? Two fixes:

- Prepend the document title and section heading: `"Employee Handbook > Leave Policy > Annual leave: The limit is 30 days…"`
- **Contextual retrieval** (a technique Anthropic published in 2024): use an LLM to write a one-sentence description of where each chunk fits in the whole document, and prepend it before embedding. It noticeably reduces retrieval failures, at the cost of one cheap LLM call per chunk at indexing time (prompt caching makes this affordable).

### 2.4 Retrieval: getting the right chunks

All of Lesson 09 applies: embed the question with the **same** model, search the vector database, filter by metadata, use **hybrid search** (BM25 + vectors) for exact terms, and **re-rank** for precision.

**How many chunks (top-k)?** Common: retrieve 20–50 candidates, re-rank, keep 3–10 for the prompt. Too few → the answer may be missing. Too many → noise, cost, "lost in the middle" (Lesson 06).

**Query transformation** improves retrieval when questions are vague or conversational:

| Technique | Idea | Example |
|---|---|---|
| **Query rewriting** | An LLM rewrites the question into a clear search query, using chat history | "What about for part-timers?" → "Annual leave entitlement for part-time employees" |
| **Multi-query** | Generate 3–5 differently-worded queries, search all, merge | Catches different phrasings |
| **Decomposition** | Split a complex question into sub-questions | "Compare leave for UK and India offices" → two searches |
| **HyDE** (Hypothetical Document Embeddings) | Ask an LLM to write a *fake* answer, embed that, and search with it | Fake answers often look more like real documents than questions do |

### 2.5 Augmentation: building the prompt

Use Lesson 07's principles: documents first, in tags with metadata, question last, clear rules, an "out", and a demand for citations.

```
You answer employee questions using ONLY the documents provided.

<documents>
<document id="1" source="handbook.pdf" page="12" section="Annual Leave">
Full-time employees receive 24 days of paid annual leave per calendar year...
</document>
<document id="2" source="handbook.pdf" page="13" section="Part-time staff">
Part-time employees receive leave pro-rated to their contracted hours...
</document>
</documents>

Rules:
- Base every statement on the documents. Cite sources like [1] or [2] after each claim.
- If the documents don't contain the answer, say: "I couldn't find this in the handbook.
  Please contact HR." Do not guess.
- If documents conflict, say so and cite both.

<question>
How much annual leave do part-timers get?
</question>
```

### 2.6 Generation and citations

The LLM writes the answer from the provided chunks. To make answers **verifiable**:

- **Inline citations** like `[1]`, mapped by your code back to source + page for display.
- **Quotes:** ask the model to quote the exact supporting sentence (easy to check).
- **Built-in citation features:** some APIs (including Claude's) can return citations automatically, pointing to the exact passages of documents you sent. You pass documents as special `document` content blocks with citations enabled, and the response comes back with `citations` attached to each part of the text.

Show sources in your user interface. Users trust answers they can check.

### 2.7 Grounding and faithfulness

An answer is **grounded** (or **faithful**) if every claim is supported by the retrieved context. RAG reduces hallucination but **doesn't eliminate it**: the model can still misread, over-generalise, or mix in its own knowledge. Defences:

- Strict prompt rules + the "out" (Lesson 07).
- Citations and quotes.
- A **verification step**: a second LLM call checks each claim against the sources (prompt chaining, Lesson 07).
- Evaluations that measure faithfulness (2.10).

### 2.8 Conversational RAG

In a chat, follow-ups like *"And for contractors?"* make no sense on their own. Before retrieving, **rewrite the follow-up into a standalone question** using the chat history ("Annual leave entitlement for contractors"), then retrieve with that. Send the conversation plus the newly retrieved documents to the LLM.

### 2.9 RAG vs long context vs fine-tuning

With 1M-token context windows, why not just paste everything? And when should you fine-tune instead?

| Approach | What it is | Best when | Downsides |
|---|---|---|---|
| **Long context** ("stuff it all in") | Put entire documents in the prompt | Small knowledge base (fits comfortably, e.g. < a few hundred pages); one-off analysis of a document | Cost and latency on every request; quality can drop with huge inputs; doesn't scale to large libraries |
| **RAG** | Retrieve relevant chunks per question | Large or changing knowledge; need citations and permissions | Retrieval can miss; more moving parts |
| **Fine-tuning** | Further-train a model on your examples | Teaching a *style, format or behaviour*, not facts | Expensive; facts get stale; still hallucinates; no citations |

Rule of thumb: **RAG for knowledge, fine-tuning for behaviour, long context for small or one-off material.** They can be combined: prompt caching (Lesson 08) makes long context cheaper for repeated questions about the same documents.

### 2.10 Evaluating RAG

A RAG system can fail in two places, so evaluate both:

```
            RETRIEVAL                                   GENERATION
 question ─▶ did we find the right chunks? ─────────▶ did the answer use them correctly?
            (context recall / precision, recall@k, MRR)  (faithfulness, answer relevance, correctness)
```

| Metric | Question | How to measure |
|---|---|---|
| **Context recall** | Did retrieval find the chunks needed to answer? | Test set with known source chunks (Lesson 09 metrics) |
| **Context precision** | Were the retrieved chunks mostly relevant? | Label or LLM-judge each chunk |
| **Faithfulness / groundedness** | Is every claim in the answer supported by the context? | LLM-as-a-judge with a rubric; spot checks |
| **Answer relevance** | Does it actually address the question? | LLM-as-a-judge |
| **Correctness** | Does it match the reference answer? | Compare to expert-written answers |
| **Abstention** | Does it say "I don't know" when the answer isn't in the documents? | Include unanswerable questions in the test set |

Build a **golden dataset**: 30–100 realistic questions with reference answers and the source passages, including tricky and unanswerable ones. Libraries such as **RAGAS** and **DeepEval** automate many of these metrics.

### 2.11 Common failure modes (and fixes)

| Symptom | Likely cause | Fix |
|---|---|---|
| "I couldn't find it" but the info exists | Retrieval miss: bad chunking, wrong embedding model, vague query | Better chunking, contextual retrieval, hybrid search, query rewriting, bigger k |
| Answer mixes up two policies | Chunks lack context; similar text from different documents | Prepend titles/sections; metadata filters; re-ranking |
| Confident wrong answer | Model ignored or over-generalised the context | Stricter rules, citations, verification step, lower-effort-but-strict prompt |
| Outdated answer | Stale index | Re-index on change; store and filter by "updated" date |
| Tables/numbers garbled | PDF extraction broke the layout | Better parser; keep tables as Markdown; structure-aware chunking |
| Leaks confidential info | No access control | Filter retrieval by user permissions |
| Slow or expensive | Too many/too large chunks; big model | Smaller k after re-ranking; cache; right-size model |

### 2.12 Beyond basic RAG (names to know)

- **Agentic RAG:** the LLM decides *when* and *what* to search, can search several times, and refines queries, using search as a **tool** (Month 3).
- **GraphRAG:** builds a **knowledge graph** (entities and their relationships) from documents, to answer questions that connect many facts ("Which suppliers do all our delayed projects have in common?").
- **Multimodal RAG:** retrieving images, charts and slides as well as text.

> **In simple words:** RAG has an indexing pipeline (load → clean → chunk → embed → store) and a query pipeline (rewrite → retrieve → re-rank → prompt → generate with citations). Chunking and context-rich chunks matter most. Ground answers with strict rules, citations and an "out". Use RAG for knowledge, fine-tuning for behaviour, long context for small or one-off material. Evaluate retrieval and generation separately with a golden dataset.

---

## 3. How it works: an Employee Handbook assistant, start to finish

**Scenario:** a company has a 40-page employee handbook (PDF) plus a few policy Markdown files. Employees keep asking HR the same questions. You'll build an assistant that answers from these documents with citations, and says so when it can't.

### Step 1: Setup

```bash
uv init handbook_rag && cd handbook_rag
uv add anthropic python-dotenv pypdf sentence-transformers chromadb pydantic
```

```
handbook_rag/
├── docs/              handbook.pdf, remote_work.md, expenses.md
├── ingest.py          indexing pipeline
├── rag.py             query pipeline
├── eval.py            golden-set evaluation
└── golden.json        test questions
```

### Step 2: Load documents, keeping page metadata

```python
# ingest.py (part 1)
from pathlib import Path
from pypdf import PdfReader

def load_docs(folder: str) -> list[dict]:
    """Return a list of {text, source, page} 'pages' from PDFs and Markdown files."""
    pages = []
    for path in Path(folder).iterdir():
        if path.suffix == ".pdf":
            for i, page in enumerate(PdfReader(path).pages, start=1):
                text = page.extract_text() or ""
                pages.append({"text": text, "source": path.name, "page": i})
        elif path.suffix in {".md", ".txt"}:
            pages.append({"text": path.read_text(), "source": path.name, "page": 1})
    return pages
```

### Step 3: Clean and chunk (recursive, with overlap and headings)

```python
# ingest.py (part 2)
import re

def clean(text: str) -> str:
    text = re.sub(r"Page \d+ of \d+", "", text)        # remove page footers
    text = re.sub(r"[ \t]+", " ", text)                # collapse spaces
    return re.sub(r"\n{3,}", "\n\n", text).strip()     # collapse blank lines

def split_long(p: str, max_chars: int) -> list[str]:
    """Break a paragraph longer than max_chars into sentence-sized pieces."""
    if len(p) <= max_chars:
        return [p]
    pieces, current = [], ""
    for sentence in re.split(r"(?<=[.!?])\s+", p):
        if current and len(current) + len(sentence) + 1 > max_chars:
            pieces.append(current)
            current = ""
        current = f"{current} {sentence}".strip()
    if current:
        pieces.append(current)
    return pieces

def chunk_text(text: str, max_chars: int = 1200, overlap: int = 200) -> list[str]:
    """Pack paragraphs into chunks of up to ~max_chars; each new chunk starts with
    the last `overlap` characters of the previous one."""
    paras = [piece for p in text.split("\n\n") if p.strip()
             for piece in split_long(p.strip(), max_chars - overlap)]
    chunks, current = [], ""
    for p in paras:
        if current and len(current) + len(p) + 2 > max_chars:
            chunks.append(current)
            current = current[-overlap:]          # carry the overlap into the next chunk
        current = f"{current}\n\n{p}" if current else p
    if current:
        chunks.append(current)
    return chunks

def find_heading(text: str) -> str:
    """Use the first short line as a section heading (good enough for many handbooks)."""
    for line in text.splitlines():
        if 3 < len(line) < 80 and not line.endswith("."):
            return line.strip()
    return ""
```

(1,200 characters is roughly 250–300 tokens. Real projects often use a token-based splitter from a library; the idea is identical.)

### Step 4: Embed and store, with context prepended

```python
# ingest.py (part 3)
import chromadb
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "BAAI/bge-small-en-v1.5"

def main():
    model = SentenceTransformer(EMBED_MODEL)
    col = chromadb.PersistentClient(path="./db").get_or_create_collection(
        "handbook", configuration={"hnsw": {"space": "cosine"}})

    ids, docs, metas = [], [], []
    for page in load_docs("docs"):
        heading = find_heading(page["text"])
        for n, chunk in enumerate(chunk_text(clean(page["text"]))):
            ids.append(f"{page['source']}:p{page['page']}:c{n}")
            docs.append(f"[{page['source']} > {heading}]\n{chunk}")    # context prefix
            metas.append({"source": page["source"], "page": page["page"], "section": heading})

    vecs = model.encode(docs, normalize_embeddings=True, show_progress_bar=True).tolist()
    col.upsert(ids=ids, embeddings=vecs, documents=docs, metadatas=metas)
    print(f"Indexed {len(ids)} chunks")

if __name__ == "__main__":
    main()
```

Run `uv run ingest.py` once (and again whenever documents change).

### Step 5: Retrieve

```python
# rag.py (part 1)
import chromadb, anthropic
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "claude-opus-5-5"

embedder = SentenceTransformer(EMBED_MODEL)
col = chromadb.PersistentClient(path="./db").get_collection("handbook")
client = anthropic.Anthropic()

def retrieve(question: str, k: int = 5) -> list[dict]:
    q = embedder.encode([question], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=q, n_results=k, include=["documents", "metadatas", "distances"])
    return [{"text": d, **m, "score": round(1 - dist, 3)}
            for d, m, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])]
```

### Step 6: Augment and generate with citations

```python
# rag.py (part 2)
SYSTEM = """You are the company's HR handbook assistant.
Answer ONLY from the documents provided. After each claim, cite the document number like [2].
If the documents don't contain the answer, reply exactly:
"I couldn't find this in the handbook. Please contact HR at hr@example.com."
If documents conflict, point it out and cite both. Keep answers under 150 words."""

def build_prompt(question: str, chunks: list[dict]) -> str:
    docs = "\n".join(
        f'<document id="{i}" source="{c["source"]}" page="{c["page"]}">\n{c["text"]}\n</document>'
        for i, c in enumerate(chunks, start=1)
    )
    return f"<documents>\n{docs}\n</documents>\n\n<question>\n{question}\n</question>"

def answer(question: str) -> dict:
    chunks = retrieve(question)
    response = client.messages.create(
        model=LLM_MODEL,
        max_tokens=2000,
        system=SYSTEM,
        output_config={"effort": "low"},
        messages=[{"role": "user", "content": build_prompt(question, chunks)}],
    )
    text = next((b.text for b in response.content if b.type == "text"), "")
    return {"answer": text,
            "sources": [f'[{i}] {c["source"]} p.{c["page"]} (score {c["score"]})'
                        for i, c in enumerate(chunks, start=1)]}

if __name__ == "__main__":
    while (q := input("\nAsk the handbook (blank to quit): ").strip()):
        result = answer(q)
        print("\n" + result["answer"] + "\n\nSources:\n" + "\n".join(result["sources"]))
```

(`while (q := input(...))` uses the **walrus operator** `:=`, which assigns and tests in one step: keep looping while the input isn't blank.)

**Example session:**

```
Ask the handbook: how much leave do part-timers get?

Part-time employees receive annual leave pro-rated to their contracted hours [2].
For example, someone working 3 days a week gets 3/5 of the full-time entitlement
of 24 days, which is 14.4 days [1][2].

Sources:
[1] handbook.pdf p.12 (score 0.71)
[2] handbook.pdf p.13 (score 0.69)
...

Ask the handbook: what's the CEO's salary?

I couldn't find this in the handbook. Please contact HR at hr@example.com.
```

### Step 7: Evaluate with a golden set

```json
// golden.json  (a few of ~30)
[
  {"q": "How many days of annual leave do full-timers get?", "expected_source": "handbook.pdf", "expected_page": 12, "answer_contains": "24"},
  {"q": "Can I work from another country?", "expected_source": "remote_work.md", "expected_page": 1, "answer_contains": "30 days"},
  {"q": "What's the CEO's salary?", "expected_source": null, "expected_page": null, "answer_contains": "couldn't find"}
]
```

```python
# eval.py
import json
from rag import retrieve, answer

golden = json.load(open("golden.json"))
hits = correct = 0
for case in golden:
    chunks = retrieve(case["q"])
    if case["expected_source"] is None or any(
            c["source"] == case["expected_source"] and c["page"] == case["expected_page"] for c in chunks):
        hits += 1
    if case["answer_contains"].lower() in answer(case["q"])["answer"].lower():
        correct += 1
print(f"Retrieval hit rate @5: {hits / len(golden):.0%}")
print(f"Answer check pass rate: {correct / len(golden):.0%}")
```

"Answer contains" is a crude but useful first check. Add an **LLM-as-a-judge** step for faithfulness: give a second model the context, the answer and a rubric ("Is every claim supported by the documents? yes/no + which claim isn't"), and use structured outputs (Lesson 08) for its verdict.

### Step 8: Improve, measuring each change

| Version | Change | Retrieval @5 | Answer pass |
|---|---|---|---|
| v1 | 1,200-char chunks, no prefix | 78% | 72% |
| v2 | + section-heading prefix | 86% | 80% |
| v3 | + hybrid search (BM25) for policy codes | 91% | 84% |
| v4 | + query rewriting for follow-ups, re-ranker | 95% | 90% |

(Your numbers will differ; the point is the method.)

### The whole system

```
 INDEXING:  docs/*.pdf,*.md ─▶ load (pages + metadata) ─▶ clean ─▶ chunk (overlap) ─▶ "[source > section]" prefix
                                                                                             │
                                                                         embed (bge-small) ─▶ Chroma
 QUERY:     question ─▶ embed (same model) ─▶ top-5 chunks ─▶ <documents> prompt + rules ─▶ Claude ─▶ answer [1][2]
                                                                                                   + sources
 EVAL:      golden.json ─▶ retrieval hit rate + answer checks (+ LLM judge) ─▶ change one thing ─▶ re-run
```

> **In simple words:** Load documents with page metadata, clean and chunk them with overlap and heading prefixes, embed and store; at question time retrieve the top chunks, put them in a tagged prompt with strict citation rules and an "out", generate the answer, show sources, and measure everything with a golden set.

---

## 4. Key terms (in order)

| Term | Plain meaning |
|---|---|
| **RAG** | Retrieval-Augmented Generation: search docs, add them to the prompt, generate a grounded answer. |
| **Retrieve / augment / generate** | Find relevant chunks / paste into prompt / LLM writes the answer. |
| **Indexing / ingestion** | Offline pipeline: load, clean, chunk, embed, store. |
| **Document loader** | Code that reads a file format into text + metadata. |
| **OCR** | Reading text from images or scanned pages. |
| **Cleaning** | Removing junk like headers, footers and menus. |
| **Chunking / chunk** | Splitting documents into pieces / one piece. |
| **Chunk size / overlap** | How big each piece is / text repeated between neighbours. |
| **Recursive / structure-aware / semantic chunking** | Split by paragraphs then smaller / by headings and sections / by topic changes. |
| **Contextual retrieval** | Prepending an LLM-written description of each chunk's place in its document before embedding. |
| **Top-k** | How many chunks to retrieve. |
| **Query rewriting / multi-query / decomposition / HyDE** | Ways to transform a question so retrieval works better. |
| **Citation** | A pointer from a claim to its source passage. |
| **Grounded / faithful** | Every claim is supported by the provided context. |
| **Verification step** | A second LLM check of claims against sources. |
| **Conversational RAG** | RAG in chat, rewriting follow-ups into standalone questions. |
| **Long context** | Putting whole documents in the prompt instead of retrieving. |
| **Fine-tuning** | Further training a model on your examples (for behaviour, not facts). |
| **Context recall / precision** | Did we retrieve what's needed / was what we retrieved relevant? |
| **Answer relevance / correctness / abstention** | On-topic / matches the reference / says "I don't know" correctly. |
| **Golden dataset** | Test questions with reference answers and sources. |
| **RAGAS / DeepEval** | Libraries that automate RAG evaluation metrics. |
| **Agentic RAG** | The LLM decides when and what to search, using search as a tool. |
| **GraphRAG / knowledge graph** | RAG over a network of entities and their relationships. |
| **Walrus operator `:=`** | Python: assign a value inside an expression. |

> **In simple words:** Ingest, chunk, embed, retrieve, augment, generate, cite, evaluate. That's RAG.

---

## 5. The people involved

| Who | What they do | RAG day to day |
|---|---|---|
| **AI engineers** | Build the RAG pipelines | Chunking, retrieval tuning, prompts, citations, evals, cost. |
| **Data engineers** | Feed the index | Connectors to Drive/Confluence/SharePoint/databases; keep it fresh; handle deletions. |
| **Content owners** (HR, legal, support leads) | Own the documents | Keep documents accurate and current. RAG is only as good as its sources! They also write golden answers. |
| **Security & compliance** | Protect data | Permissions-aware retrieval, audit logs, data retention, PII handling. |
| **Product / UX designers** | Shape the experience | How citations are shown, how "I don't know" is phrased, feedback buttons (👍/👎). |
| **End users** (employees, customers) | Ask questions | Need fast, correct, cited answers and a path to a human. |
| **Vendors** (vector DBs, embedding providers, frameworks like LangChain and LlamaIndex) | Supply components | Release features like hybrid search, re-rankers, loaders. |

> **In simple words:** Engineers build it, content owners keep the knowledge right, security keeps it safe, designers make it trustworthy, users rely on it.

---

## 6. Common misconceptions and beginner mistakes

| Myth / mistake | Reality / fix |
|---|---|
| "RAG eliminates hallucinations." | It reduces them. Add strict rules, citations, an "out", verification and evals. |
| "Just use bigger chunks to be safe." | Big chunks blur retrieval and waste tokens. Test sizes; add context prefixes. |
| Throwing away page/section metadata | You need it for citations, filters and debugging. |
| Never looking at retrieved chunks | Print them! Most RAG bugs are retrieval bugs, visible immediately. |
| Only evaluating final answers | Evaluate retrieval separately, so you know which half to fix. |
| No unanswerable questions in the test set | Include them to test abstention. |
| "Long context makes RAG obsolete." | For large, changing, permissioned knowledge, RAG is still cheaper, faster and auditable. Use long context when material is small. |
| "Fine-tune to teach it our documents." | Fine-tuning is for behaviour/style; facts go stale and can't be cited. Use RAG for knowledge. |
| Ignoring PDF extraction quality | Tables and columns often break. Check extracted text; use better parsers. |
| Stale index | Re-index on document changes; track "last updated". |
| Retrieving documents users shouldn't see | Filter by permissions at retrieval time. |
| Building on a framework before understanding the steps | Build it by hand once (this lesson); then frameworks make sense (Lesson 14). |

> **In simple words:** RAG problems are usually retrieval problems. Look at the chunks, keep metadata, test with tricky and unanswerable questions, and keep the index fresh and permission-aware.

---

## 7. One-page recap

### The 10 things to remember

1. **RAG = retrieve → augment → generate:** an open-book exam for LLMs.
2. **Two pipelines:** offline indexing, online querying.
3. **Keep metadata** (source, page, section, date, permissions) from the start.
4. **Chunking is the biggest lever:** coherent ~200–800-token chunks with overlap and context prefixes.
5. **Retrieval = Lesson 09:** same embedding model, hybrid search, filters, re-ranking.
6. **Rewrite conversational follow-ups** into standalone queries.
7. **Prompt:** documents first in tags, rules, an "out", citations, question last.
8. **Ground and verify:** citations, quotes, optional verification pass.
9. **RAG for knowledge, fine-tuning for behaviour, long context for small or one-off material.**
10. **Evaluate both halves** with a golden set (retrieval hit rate; faithfulness, correctness, abstention).

### What to learn next

➡️ **Lesson 11: Build an AI-Powered Project.** You now have every Month 2 skill. Next you'll combine them into one polished, portfolio-ready AI application with a UI, evals and a README.
