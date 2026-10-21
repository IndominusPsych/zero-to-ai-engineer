# Lesson 09: Embeddings & Vector Databases

*Month 2, Week 7. Reading time: about 70 minutes. Assumes Lessons 02 (NumPy), 06 and 08.*

---

## 🛠️ Setup for this lesson

| You need | Why | How to get it |
|---|---|---|
| **sentence-transformers** | Free embedding models that run on your laptop (installs PyTorch, ~1 GB) | `uv add` (below) |
| **chromadb** (1.x) | The vector database used in this lesson | `uv add` (below) |
| **numpy**, **pandas**, **matplotlib**, **scikit-learn**, **rank-bm25** | Maths, results tables, plots, keyword search (practice) | `uv add` (below) |
| ~2 GB free disk + internet | The first run downloads the `all-MiniLM-L6-v2` model (~90 MB) | Setup Guide Step 9 |
| Optional: **Voyage AI** key | Hosted embeddings (Section 2) | dash.voyageai.com → `VOYAGE_API_KEY` in `.env`; `uv add voyageai` |

**Install:**

```bash
cd ~/ai-engineer-projects
uv init embed_lab && cd embed_lab
uv add sentence-transformers chromadb numpy pandas matplotlib scikit-learn rank-bm25
```

**Check it works:**

```bash
uv run python -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('all-MiniLM-L6-v2'); print(m.encode('hello').shape)"   # (384,)
uv run python -c "import chromadb; print('chroma', chromadb.__version__)"   # 1.x
```

No GPU needed. The first check takes a minute while the model downloads; after that it's cached.

Stuck? See the step-by-step instructions and the troubleshooting table in [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md).

---

## 1. The big picture

### What is this, in simple words?

Imagine your company has 5,000 help articles. A customer asks: *"My parcel never showed up."* The right article is titled **"What to do if your order hasn't arrived."** Notice: the customer's question and the title share **no important words**. "Parcel" ≠ "order", "never showed up" ≠ "hasn't arrived". A normal keyword search (like Ctrl+F) would miss it.

**Embeddings** solve this. An embedding turns a piece of text into a list of numbers that captures its **meaning**. Texts with similar meanings get similar numbers, even if they use completely different words. So you can search by **meaning** instead of by exact words. This is called **semantic search**.

A **vector database** is a database built to store millions of these number-lists and quickly find the ones closest to a query.

Analogy: think of a giant library map where every book is placed by *topic*, not alphabetically. Cookbooks cluster in one corner, space books in another, Italian cookbooks near (but not on top of) French cookbooks. To find books like yours, you just look at what's nearby on the map. Embeddings are the map coordinates. The vector database is the librarian who can instantly find the nearest neighbours.

### Which field does it belong to?

Embeddings come from **machine learning / NLP** (Lesson 06 showed every LLM starts by turning tokens into embeddings). Vector databases belong to **information retrieval**: the field of finding relevant information, which also includes search engines. Together they're a core part of **AI engineering**.

### Why does it matter?

Embeddings are the engine behind:

| Use | Example |
|---|---|
| **Semantic search** | Help centre search that understands "parcel never showed up" |
| **RAG** (Lesson 10) | Finding the right documents to give an LLM so it answers from your data |
| **Recommendations** | "Customers who liked this article also read…" |
| **Clustering & classification** | Grouping 10,000 support tickets into themes automatically |
| **Duplicate detection** | Spotting the same question asked in different words |
| **Agent memory** (Month 3) | Letting an agent recall relevant past information |

LLMs have a knowledge cutoff and don't know your private data (Lesson 06). Embeddings + vector databases are how you **find** the relevant private data to hand them.

> **In simple words:** Embeddings turn text into "meaning coordinates," so similar meanings sit close together. A vector database stores these coordinates and finds the nearest ones fast. That lets you search by meaning, which powers RAG, recommendations and more.

---

## 2. Core concepts

### 2.1 Vectors: a quick refresher

From Lesson 02: a **vector** is a 1-D list (array) of numbers, like `[0.2, -1.3, 0.8]`. Each number is one **dimension**. A vector with 3 numbers can be drawn as a point in 3-D space. Embedding vectors have hundreds or thousands of dimensions (common sizes: 384, 768, 1024, 1536, 3072). We can't picture 1,024 dimensions, but the maths works exactly the same as in 2-D or 3-D.

### 2.2 What an embedding is

An **embedding** is a vector produced by an **embedding model** (a neural network trained for this job) that represents the meaning of a piece of input: a word, sentence, paragraph, image, or even code.

```
"How do I reset my password?"     → [0.12, -0.48, 0.33, ..., 0.07]   (e.g. 384 numbers)
"I forgot my login credentials"   → [0.10, -0.45, 0.30, ..., 0.09]   ← very similar!
"Best pizza toppings"             → [-0.71, 0.22, -0.05, ..., 0.64]  ← very different
```

How do embedding models learn this? During training they're shown huge numbers of text pairs that mean similar things (a question and its answer, a title and its article) and pairs that don't. The model is rewarded for placing similar pairs close together and different ones far apart. This is called **contrastive learning**.

An embedding model is **not** a chat LLM. It doesn't generate text; it only outputs vectors. It's usually much smaller, faster and cheaper.

### 2.3 Visualising meaning space

If we squash embeddings down to 2-D for a picture, related ideas cluster:

```
          ▲
          │   • "refund policy"
          │ • "money back"      • "return an item"
          │        • "cancel my order"
          │
          │                              • "pizza recipe"
          │                           • "how to bake bread"
          │
          │   • "reset password"
          │ • "can't log in"   • "forgot username"
          └────────────────────────────────────────────▶
```

Directions in this space can even carry meaning. The famous example: `vector("king") − vector("man") + vector("woman") ≈ vector("queen")`.

### 2.4 Measuring similarity

To find "nearby" vectors we need a way to measure closeness. Three common measures:

| Measure | Idea | Range | Use |
|---|---|---|---|
| **Cosine similarity** | The angle between two vectors (do they point the same way?), ignoring length | −1 to 1 (1 = same direction) | Most common for text |
| **Dot product** | Multiply matching numbers and add (Lesson 02!) | Any number | Fast; equals cosine when vectors are normalised |
| **Euclidean (L2) distance** | Straight-line distance between points | 0 = identical, bigger = farther | Also common |

Cosine similarity formula (you coded it in Practice 02!):

```
cos(a, b) = (a · b) / (|a| × |b|)
```

`|a|` is the vector's length (its **norm**). **Normalising** a vector means scaling it to length 1. Many embedding models output normalised vectors, so cosine similarity = dot product, which is very fast to compute.

Note: some databases report **cosine distance** = 1 − cosine similarity. Then *smaller* is better. Always check which one you're reading.

Tiny worked example (2-D):

```python
import numpy as np
a = np.array([1.0, 1.0])     # "dogs"
b = np.array([1.0, 0.9])     # "puppies"
c = np.array([-1.0, 0.2])    # "taxes"

def cos(x, y): return x @ y / (np.linalg.norm(x) * np.linalg.norm(y))
print(cos(a, b))   # 0.998 → very similar
print(cos(a, c))   # -0.55 → unrelated/opposite
```

(`x @ y` is NumPy shorthand for the dot product.)

### 2.5 Embedding models: which ones?

| Option | Examples (2026) | Pros | Cons |
|---|---|---|---|
| **Run locally (free, open)** | `sentence-transformers` models like `all-MiniLM-L6-v2` (384 dims, tiny), BGE, E5, GTE, Nomic | Free, private, works offline | Lower quality than the best APIs (but often good enough); uses your CPU/GPU |
| **API models** | **Voyage AI** (Anthropic's recommended embeddings partner; Anthropic doesn't offer its own embedding model), OpenAI `text-embedding-3-small/large`, Google Gemini embeddings, Cohere Embed | High quality, multilingual, nothing to host | Costs per token (but cheap); data leaves your machine |

How to choose: check the public **MTEB leaderboard** (Massive Text Embedding Benchmark), which ranks models on many retrieval tasks, then *test on your own data*. Consider language support, maximum input length, vector size (bigger = more storage), price and privacy.

**Critical rule:** the vectors from different models live in different "maps." **You must use the same embedding model for your documents and your queries.** If you switch models, re-embed everything.

Some models want different **input types** for documents vs queries (e.g. a prefix like `"query: "` or an `input_type="query"` parameter). Read the model card.

### 2.6 Creating embeddings in Python

Local and free with `sentence-transformers` (downloads the model the first time):

```bash
uv add sentence-transformers
```

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = ["How do I reset my password?", "I forgot my login", "Best pizza toppings"]
vectors = model.encode(sentences, normalize_embeddings=True)
print(vectors.shape)                    # (3, 384)
print(vectors @ vectors.T)              # 3×3 grid of cosine similarities
```

The last line computes every pair's similarity at once (matrix maths from Lesson 02): you'll see passwords ↔ login ≈ 0.6+, and both ↔ pizza ≈ 0.0.

With an API (example: Voyage AI; others look very similar):

```python
# uv add voyageai ; VOYAGE_API_KEY in .env
import voyageai
vo = voyageai.Client()
doc_vecs = vo.embed(documents, model="voyage-3.5", input_type="document").embeddings
q_vec = vo.embed(["parcel never arrived"], model="voyage-3.5", input_type="query").embeddings[0]
```

(Model names change; check the provider's current list.)

### 2.7 Brute-force search: the simple way

With a few thousand documents, you don't need a special database. Store vectors in a NumPy array and compare the query to all of them:

```python
doc_vecs = model.encode(docs, normalize_embeddings=True)     # shape (N, 384)
q = model.encode(["parcel never showed up"], normalize_embeddings=True)[0]
scores = doc_vecs @ q                                        # N similarity scores
top = scores.argsort()[::-1][:3]                             # indexes of the 3 best
for i in top:
    print(round(float(scores[i]), 3), docs[i])
```

`argsort()` returns positions that would sort the array; `[::-1]` reverses it (highest first). This is **exact nearest-neighbour search**, or **k-NN** (k-Nearest Neighbours, which you met in Lesson 04!). It's perfectly fine up to roughly 100,000 vectors.

### 2.8 Why vector databases exist: approximate search at scale

Comparing a query to 100 million vectors one by one is too slow. Vector databases use **ANN** (**Approximate Nearest Neighbour**) algorithms that find *almost* the best matches, extremely fast, by organising vectors cleverly in advance. The organised structure is called an **index**.

The most popular ANN index is **HNSW** (Hierarchical Navigable Small World). Analogy: finding a house in a new country. You don't check every house. You take a flight to the right region (top layer, few long-range links), a train to the right town (middle layer), then walk the streets (bottom layer, many short links). Each layer narrows the search.

```
 Layer 2:  •───────────────────────•              (few points, long jumps)
 Layer 1:  •──────•────────•───────•──────•
 Layer 0:  •─•─•─•─•─•─•─•─•─•─•─•─•─•─•─•─•─•    (all points, short hops)
```

"Approximate" means it might occasionally miss the true #1 match, but the **recall** (fraction of true nearest neighbours found) is typically 95–99%, at a tiny fraction of the time. Other index types include IVF (cluster the vectors, only search nearby clusters) and quantisation (compress vectors to save memory).

### 2.9 What a vector database stores

Each item (often called a **record** or **point**) has:

| Field | Example | Why |
|---|---|---|
| **ID** | `"faq-017"` | To update or delete it later |
| **Vector** | `[0.12, -0.48, ...]` | For similarity search |
| **Document / text** | "Orders not delivered after 14 days can be…" | To show or give to an LLM |
| **Metadata** | `{"category": "delivery", "updated": "2026-09-01", "lang": "en"}` | For filtering, sorting, citing sources |

Most databases are organised into **collections** (like tables): one collection per kind of data.

### 2.10 Metadata filtering

Often you want "most similar, **but only** among X": only English articles, only documents this user may see, only policies updated after 2025. **Metadata filtering** combines similarity with normal conditions:

```python
results = collection.query(query_embeddings=[q], n_results=5,
                           where={"category": "delivery"})
```

This is also how you enforce **access control**: never return documents a user isn't allowed to see.

### 2.11 Keyword search still matters: hybrid search

Embeddings are great at meaning, but weaker at **exact** things: product codes ("SKU-48213"), names, rare technical terms, error codes. Classic **keyword search** handles these well. The standard keyword-ranking algorithm is **BM25**: it scores documents by how often the query's words appear, giving more weight to rare words.

**Hybrid search** runs both and merges the results (a common merging method is **Reciprocal Rank Fusion, RRF**: documents ranked highly by either method rise to the top).

| Query | Keyword (BM25) | Semantic (embeddings) |
|---|---|---|
| "error E-4021" | ✅ exact match | ❌ might return generic error docs |
| "my parcel never showed up" | ❌ no shared words | ✅ finds "order hasn't arrived" |

### 2.12 Re-ranking

A two-stage trick for better quality:

1. **Retrieve** the top 50 candidates quickly with vector (or hybrid) search.
2. **Re-rank** them with a slower, more accurate **re-ranker** (a **cross-encoder**: a model that reads the query and each document *together* and scores relevance), then keep the top 5.

```
 query ─▶ fast vector search (top 50) ─▶ re-ranker (careful scoring) ─▶ best 5
```

Re-rankers are available locally (e.g. via sentence-transformers' `CrossEncoder`) or as APIs (Voyage, Cohere).

### 2.13 Chunking (preview)

Embedding a whole 50-page document into one vector blurs all its topics together. Instead, split documents into **chunks** (e.g. a few paragraphs each) and embed each chunk. Chunking is so important for RAG that Lesson 10 covers it in depth.

### 2.14 Choosing a vector database (2026)

| Option | Type | Best for | Notes |
|---|---|---|---|
| **NumPy array** | In memory | Learning, < ~100k vectors | Zero setup |
| **FAISS** | Library (by Meta) | Fast local search, research | Not a full database (no metadata storage built in) |
| **Chroma** | Open-source, embedded or server | Prototypes, Python-first projects, this course | Runs inside your Python program with file storage |
| **pgvector** | PostgreSQL extension | Apps already using Postgres; most projects under ~10M vectors | One database for everything; SQL + vectors |
| **Qdrant** | Open-source server / cloud | Production with strong filtering and hybrid search | Self-host or managed |
| **Weaviate, Milvus** | Open-source server / cloud | Large-scale production | Rich features |
| **Pinecone** | Fully managed cloud (SaaS) | Zero-ops production | Easy, but costs grow with scale; data hosted by them |

A sensible path: **NumPy → Chroma for learning → pgvector or Qdrant for production.** Pick based on your existing stack more than benchmarks.

### 2.15 Evaluating retrieval

How do you know your search is good? Make a small **test set**: 20–50 realistic queries, each with the ID(s) of the correct document(s). Then measure:

| Metric | Question |
|---|---|
| **Recall@k** (hit rate) | Is the correct document in the top k results? |
| **MRR** (Mean Reciprocal Rank) | How high up is the first correct result? (1st = 1.0, 2nd = 0.5, 3rd = 0.33…) |
| **Precision@k** | What fraction of the top k are relevant? |

Change one thing (embedding model, chunk size, hybrid on/off, re-ranker) and re-measure, exactly like the prompt evals in Lesson 07.

> **In simple words:** An embedding model turns text into a vector; similar meanings → nearby vectors, measured by cosine similarity. Use the same model for documents and queries. For small data, NumPy brute force works; for large data, vector databases use ANN indexes like HNSW. Store ID + vector + text + metadata, filter by metadata, add keyword search for exact terms (hybrid), re-rank for precision, and measure retrieval with recall@k and MRR.

---

## 3. How it works: semantic FAQ search, start to finish

**Scenario:** PageTurner Books (our bookshop from Lessons 07–08) has 12 FAQ entries. Customers type questions in their own words; we want the best-matching FAQ answers, fast, with filtering by category.

### Step 1: Setup

```bash
uv init faq_search && cd faq_search
uv add sentence-transformers chromadb pandas
```

### Step 2: The data

```python
# faqs.py
FAQS = [
    {"id": "f01", "category": "delivery", "q": "How long does shipping take?",
     "a": "Standard shipping takes 3–5 business days. Express takes 1–2 days."},
    {"id": "f02", "category": "delivery", "q": "What if my order hasn't arrived?",
     "a": "Orders can take up to 14 days in busy periods. After 14 days we reship for free or refund in full."},
    {"id": "f03", "category": "delivery", "q": "Do you ship internationally?",
     "a": "Yes, we ship to 40 countries. International delivery takes 7–21 days."},
    {"id": "f04", "category": "refund", "q": "What is your return policy?",
     "a": "You can return unread books within 30 days for a full refund."},
    {"id": "f05", "category": "refund", "q": "How long do refunds take?",
     "a": "Refunds reach your account 5–7 business days after we receive the return."},
    {"id": "f06", "category": "damaged", "q": "My book arrived damaged. What now?",
     "a": "Send us a photo within 7 days and we'll replace it free of charge."},
    {"id": "f07", "category": "account", "q": "How do I reset my password?",
     "a": "Click 'Forgot password' on the login page and follow the email link."},
    {"id": "f08", "category": "account", "q": "How do I delete my account?",
     "a": "Go to Settings → Privacy → Delete account. This can't be undone."},
    {"id": "f09", "category": "payment", "q": "Which payment methods do you accept?",
     "a": "We accept cards, UPI, PayPal and gift cards."},
    {"id": "f10", "category": "payment", "q": "Why was I charged twice?",
     "a": "A temporary hold may appear; it disappears in 3 days. If not, contact us with your order ID."},
    {"id": "f11", "category": "other", "q": "Do you sell ebooks?",
     "a": "Yes, ebooks are available in EPUB format and download instantly after purchase."},
    {"id": "f12", "category": "other", "q": "Can I buy a gift card?",
     "a": "Yes, digital gift cards from $10 to $200 are available on the Gift page."},
]
```

### Step 3: Decide what to embed

We embed **question + answer together**, so a query can match either the question wording or details in the answer:

```python
texts = [f"Q: {f['q']}\nA: {f['a']}" for f in FAQS]
```

### Step 4: Embed and store in Chroma

```python
# build_index.py
import chromadb
from sentence_transformers import SentenceTransformer
from faqs import FAQS

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")      # saved to a folder on disk
collection = client.get_or_create_collection(
    name="faqs", configuration={"hnsw": {"space": "cosine"}}  # HNSW index using cosine distance
)

texts = [f"Q: {f['q']}\nA: {f['a']}" for f in FAQS]
vectors = model.encode(texts, normalize_embeddings=True).tolist()

collection.upsert(                       # "upsert" = insert, or update if the ID exists
    ids=[f["id"] for f in FAQS],
    embeddings=vectors,
    documents=texts,
    metadatas=[{"category": f["category"]} for f in FAQS],
)
print("Indexed", collection.count(), "FAQs")
```

Note `.tolist()`: Chroma accepts plain Python lists of numbers.

### Step 5: Search

```python
# search.py
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")      # SAME model as indexing!
collection = chromadb.PersistentClient(path="./chroma_db").get_collection("faqs")

def search(query: str, k: int = 3, category: str | None = None):
    q_vec = model.encode([query], normalize_embeddings=True).tolist()
    res = collection.query(
        query_embeddings=q_vec,
        n_results=k,
        where={"category": category} if category else None,
        include=["documents", "metadatas", "distances"],
    )
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        print(f"{1 - dist:.2f}  [{meta['category']}]  {doc.splitlines()[0]}")

search("my parcel never showed up")
search("can I get my money back?")
search("I can't log in anymore")
search("send books abroad", category="delivery")
```

**Actual output** from a test run (your numbers may differ slightly):

```
0.42  [delivery]  Q: What if my order hasn't arrived?
0.37  [payment]   Q: Why was I charged twice?
0.31  [delivery]  Q: How long does shipping take?

0.42  [refund]    Q: How long do refunds take?
0.39  [refund]    Q: What is your return policy?
0.29  [payment]   Q: Why was I charged twice?

0.44  [account]   Q: How do I reset my password?
0.33  [account]   Q: How do I delete my account?
0.17  [payment]   Q: Why was I charged twice?

0.42  [delivery]  Q: Do you ship internationally?
0.23  [delivery]  Q: What if my order hasn't arrived?
0.22  [delivery]  Q: How long does shipping take?
```

Notice the scores look "low" (0.4). That's normal for this small model: what matters is the **ranking**, not the absolute number. And notice "can I get my money back" put *refund timing* slightly above *return policy*: close, but arguably not the best order. That's exactly the kind of thing evaluation and re-ranking catch.

"Parcel never showed up" found "order hasn't arrived" with **zero** shared keywords. That's semantic search. (We print `1 - dist` because Chroma returns cosine *distance*.)

### Step 6: Evaluate retrieval

```python
# eval_search.py  (reuses `model` and `collection` from search.py)
TESTS = [
    ("my parcel never showed up", "f02"),
    ("can I get my money back", "f04"),
    ("forgot my login details", "f07"),
    ("charged two times on my card", "f10"),
    ("the cover was torn when it came", "f06"),
    ("do you have digital books", "f11"),
    ("how many days until my refund", "f05"),
    ("deliver to Canada?", "f03"),
]

def hit_rank(query, expected, k=3):
    q = model.encode([query], normalize_embeddings=True).tolist()
    ids = collection.query(query_embeddings=q, n_results=k)["ids"][0]
    return ids.index(expected) + 1 if expected in ids else None

ranks = [hit_rank(q, e) for q, e in TESTS]
recall_at_3 = sum(r is not None for r in ranks) / len(ranks)
mrr = sum(1 / r for r in ranks if r) / len(ranks)
print(f"Recall@3 = {recall_at_3:.0%}   MRR = {mrr:.2f}")
```

In a test run this gave **Recall@3 = 100% and MRR = 0.94**: every answer was in the top 3, and usually first. On real data (thousands of docs, messier questions) expect lower numbers. Now experiment: try a stronger embedding model (e.g. `BAAI/bge-small-en-v1.5`) or embed questions only, re-run, compare. Data beats opinion.

### Step 7: Updating

When an FAQ changes, `upsert` the same ID with its new text and vector. To remove one: `collection.delete(ids=["f08"])`. No full rebuild needed.

### What you built

```
 FAQS ─▶ "Q + A" text ─▶ embedding model ─▶ vectors ─┐
                                                     ▼
                              Chroma collection (HNSW index, cosine) + metadata
                                                     ▲
 user query ─▶ SAME embedding model ─▶ query vector ─┘ ─▶ top-k nearest (+ category filter)
                                                                   │
                                                 eval: Recall@3, MRR on test queries
```

In Lesson 10, you'll take these top results and hand them to an LLM, so it writes a natural answer grounded in your FAQs. That's RAG.

> **In simple words:** Decide what text to embed, embed it with one model, store vectors + text + metadata in a collection, embed the query with the same model, fetch the nearest results (optionally filtered), and measure retrieval quality with a small test set.

---

## 4. Key terms (in order)

| Term | Plain meaning |
|---|---|
| **Keyword search** | Finding documents that contain the query's exact words. |
| **Embedding** | A vector of numbers representing the meaning of an input. |
| **Semantic search** | Searching by meaning instead of exact words. |
| **Vector database** | A database that stores vectors and finds the nearest ones fast. |
| **Information retrieval** | The field of finding relevant information (search). |
| **Dimension** | One number in a vector; embeddings have hundreds to thousands. |
| **Embedding model** | A neural network that outputs embeddings (not a chat model). |
| **Contrastive learning** | Training that pulls similar pairs together and pushes different ones apart. |
| **Cosine similarity** | Similarity based on the angle between vectors (1 = same direction). |
| **Dot product** | Multiply matching numbers and sum; equals cosine for normalised vectors. |
| **Euclidean (L2) distance** | Straight-line distance between vectors. |
| **Norm / normalising** | A vector's length / scaling it to length 1. |
| **Cosine distance** | 1 − cosine similarity; smaller = more similar. |
| **MTEB** | A public leaderboard comparing embedding models. |
| **Input type (query/document)** | Some models embed queries and documents slightly differently. |
| **sentence-transformers** | Python library for running open embedding models locally. |
| **k-NN / exact search** | Comparing the query to every vector to find the k nearest. |
| **ANN** | Approximate nearest neighbour: much faster, nearly as accurate. |
| **Index** | A pre-organised structure that makes search fast. |
| **HNSW** | A popular layered-graph ANN index. |
| **Recall (in ANN)** | Fraction of true nearest neighbours the index finds. |
| **Record / point** | One stored item: ID + vector + text + metadata. |
| **Metadata** | Extra fields (category, date, source) attached to a record. |
| **Collection** | A named group of records, like a table. |
| **Metadata filtering** | Restricting search with conditions like `category = delivery`. |
| **Access control** | Ensuring users only retrieve documents they're allowed to see. |
| **BM25** | Classic keyword-ranking algorithm. |
| **Hybrid search / RRF** | Combining keyword and semantic results / a method to merge rankings. |
| **Re-ranker / cross-encoder** | A slower model that scores query–document pairs together for better ordering. |
| **Chunk** | A piece of a longer document, embedded separately. |
| **FAISS, Chroma, pgvector, Qdrant, Pinecone…** | Popular vector search tools and databases. |
| **Upsert** | Insert a record, or update it if the ID already exists. |
| **Recall@k / MRR / Precision@k** | Retrieval quality metrics. |

> **In simple words:** Embedding, cosine similarity, ANN/HNSW, metadata, hybrid, re-rank, recall@k. That's the vocabulary of modern search.

---

## 5. The people involved

| Who | What they do | Day to day |
|---|---|---|
| **AI engineers** | Build search, RAG and recommendation features | Choose embedding models, design what to embed, tune retrieval, run evals. |
| **Search / relevance engineers** | Specialise in ranking quality | Hybrid search, re-rankers, query understanding, A/B tests. |
| **Data engineers** | Keep the index fed | Pipelines that embed new or changed documents and remove deleted ones. |
| **Database / platform teams** | Run the vector database | Scaling, backups, latency, cost of storage and memory. |
| **Embedding-model providers** (Voyage AI, OpenAI, Google, Cohere, open-source labs) | Train embedding models | Release new, better, cheaper, multilingual models. |
| **Security / compliance** | Protect data | Make sure filters enforce permissions; sensitive data handled properly. |
| **End users** | Search and ask questions | Experience "it just understood what I meant." |

> **In simple words:** AI and search engineers make retrieval good, data and platform teams keep it running, providers improve models, and users feel the difference.

---

## 6. Common misconceptions and beginner mistakes

| Mistake / myth | Reality / fix |
|---|---|
| Using different models for documents and queries | Always the same model (and correct input types). Re-embed everything if you switch. |
| "Vector databases are magic AI." | They're nearest-neighbour search over numbers. Quality comes from the embedding model, chunking and data. |
| "I need a vector database from day one." | NumPy or Chroma is fine for small data. Scale up when needed. |
| Embedding whole long documents as one vector | Chunk them (Lesson 10). |
| Ignoring metadata | Store source, date, category, permissions; you'll need them for filtering and citations. |
| Reading cosine distance as similarity | Check: distance smaller = better; similarity bigger = better. |
| Expecting embeddings to handle exact codes/names well | Add keyword (BM25) search: hybrid. |
| No retrieval eval | Build 20–50 test queries with known answers; measure recall@k and MRR. |
| Forgetting updates and deletes | Re-embed changed docs, delete removed ones; stale indexes give wrong answers. |
| Assuming a high similarity score means "correct" | Scores are relative. A top result can still be irrelevant if nothing good exists; consider a minimum score threshold. |
| Leaking private documents via search | Filter by user permissions at query time. |

> **In simple words:** Same model both sides, chunk long docs, keep metadata, add keyword search for exact terms, measure retrieval, and keep the index fresh and permission-aware.

---

## 7. One-page recap

### The 10 things to remember

1. **Embeddings = meaning as numbers.** Similar meaning → nearby vectors.
2. **Semantic search** finds matches without shared keywords.
3. **Cosine similarity** is the standard measure; normalised vectors make it a dot product.
4. **Same embedding model** for documents and queries. Always.
5. **Small data: NumPy brute force. Big data: a vector DB with an ANN index (HNSW).**
6. **Each record = ID + vector + text + metadata.**
7. **Metadata filters** for categories, dates and permissions.
8. **Hybrid search** (BM25 + embeddings) for exact terms; **re-rankers** for precision.
9. **Measure retrieval** with recall@k and MRR on a test set.
10. **Chroma for learning; pgvector/Qdrant/Pinecone for production,** chosen by your stack.

### Cheat sheet

```python
model = SentenceTransformer("all-MiniLM-L6-v2")
vecs = model.encode(texts, normalize_embeddings=True)       # (N, dims)
scores = vecs @ model.encode([query], normalize_embeddings=True)[0]
col = chromadb.PersistentClient(path="db").get_or_create_collection(
          "name", configuration={"hnsw": {"space": "cosine"}})
col.upsert(ids=..., embeddings=vecs.tolist(), documents=texts, metadatas=[...])
col.query(query_embeddings=[q], n_results=5, where={"category": "x"})
```

### What to learn next

➡️ **Lesson 10: RAG Applications.** You can now *find* the right information. Next you'll give it to an LLM so it writes accurate, cited answers from your own documents: Retrieval-Augmented Generation.
