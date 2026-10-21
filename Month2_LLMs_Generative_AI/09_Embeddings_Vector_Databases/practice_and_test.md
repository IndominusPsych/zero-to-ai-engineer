# Practice & Test 09: Embeddings & Vector Databases

> **🛠️ Before you start:** you need sentence-transformers, chromadb, numpy, pandas, matplotlib, scikit-learn, rank-bm25 (~2 GB disk). Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run python -c "import chromadb, sentence_transformers; print('ok')"
> ```

**Setup:**

```bash
uv init embed_lab && cd embed_lab
uv add sentence-transformers chromadb numpy pandas matplotlib scikit-learn
```

The first run downloads the embedding model (~90 MB for `all-MiniLM-L6-v2`).

---

## Part A: Concept checks (no code)

**A1.** Two sentences: "The bank raised interest rates" and "We sat on the river bank." Would a *word-level* lookup treat "bank" the same in both? Would a good *sentence* embedding model? Why?

**A2.** Cosine similarity values: (a) 0.92 (b) 0.05 (c) −0.4. Describe what each means in plain words.

**A3.** A database reports cosine **distance** 0.15 for result A and 0.40 for result B. Which is more similar to the query?

**A4.** You indexed 10,000 documents with model X. A colleague queries with model Y. What happens and why?

**A5.** Which search type is better for each: (a) "error code E-4021", (b) "app freezes when I open photos", (c) "invoice INV-2026-0042", (d) "how do I get my money back"? What's the solution that handles all four?

**A6.** Your retrieval test set has 10 queries. The correct doc appears at ranks: 1, 2, 1, none, 3, 1, 1, none, 2, 1 (top-3 search). Compute Recall@3 and MRR.

---

## Part B: Hands-on

**B1. Similarity matrix.** Embed these 8 sentences and print an 8×8 cosine similarity table as a Pandas DataFrame (rounded to 2 decimals). Which pairs score highest? Any surprises?

```python
sents = ["I love my dog", "Puppies are adorable", "The stock market crashed",
         "Shares fell sharply today", "How to bake sourdough", "Bread recipe for beginners",
         "My cat sleeps all day", "Investors are worried"]
```

Optional: make a heatmap with `plt.imshow(sim, cmap="viridis"); plt.colorbar()`.

**B2. Brute-force search.** Write `search(query, docs, doc_vecs, k=3)` with NumPy only (no database). Test on B1's sentences with queries "kitten", "finance news", "baking".

**B3. Visualise meaning space.** Embed 30 sentences from 3 topics (sports, cooking, technology: write 10 each). Reduce to 2-D with `sklearn.decomposition.PCA(n_components=2)` and scatter-plot coloured by topic. Do they cluster? (**PCA**, Principal Component Analysis, squashes many dimensions into a few while keeping as much of the spread as possible. It's just for visualising.)

**B4. Chroma basics.** Store B3's 30 sentences in a Chroma collection with metadata `{"topic": ...}`. Query "a new smartphone launch" with and without `where={"topic": "technology"}`.

**B5. Compare embedding models.** Build the FAQ index from the lesson twice: with `all-MiniLM-L6-v2` and with `BAAI/bge-small-en-v1.5`. Run the lesson's 8 test queries plus 8 of your own on both. Report Recall@1, Recall@3, MRR in a table. Which wins?

**B6. What to embed.** Using the better model from B5, compare embedding (a) question only, (b) answer only, (c) question + answer. Which gives the best MRR?

**B7. Hybrid search.** `uv add rank-bm25`. Implement BM25 keyword search over the FAQs (`from rank_bm25 import BM25Okapi`; tokenise with `.lower().split()`). Implement RRF to merge BM25 and vector rankings: `score(doc) = Σ 1 / (60 + rank_in_list)`. Add a test query containing an exact code that only appears in one FAQ (add one, e.g. "Use promo code READ2026 at checkout") and show hybrid finds it when pure vector search doesn't rank it first.

**B8. Re-ranking.** Use `from sentence_transformers import CrossEncoder; ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")`. Retrieve the top 6 FAQ candidates by vector search, then re-rank with `ce.predict([(query, doc) for doc in candidates])`. Does MRR improve?

**B9. Duplicate finder.** Given 20 support questions (write some that are rephrasings of each other), find all pairs with similarity > 0.8. This is how companies merge duplicate tickets.

---

## Part C: Mini-project: "Semantic search for my notes" (2 hours)

Build a CLI that indexes a folder of your own `.md` or `.txt` files (use your lesson notes from this course!) and lets you search by meaning.

1. `index.py <folder>`: read every file, split each into paragraphs (split on blank lines; skip very short ones), embed, and upsert into Chroma with metadata `{"file": name, "paragraph": n}`. Use stable IDs like `f"{file}:{n}"` so re-indexing updates instead of duplicating.
2. `search.py "<query>" [--file name] [-k 5]`: prints top results with score, file and a 200-character preview.
3. Re-indexing only re-embeds files whose modification time changed (store `mtime` in metadata; `os.path.getmtime`).
4. Create 15 test queries with known answers; report Recall@5 and MRR in the README.
5. **Stretch:** add hybrid search (BM25 + vector with RRF) and report whether it improves your metrics.

**Rubric (15):** correct indexing with stable IDs (3), search with filters (2), incremental re-index (3), evaluation with ≥ 15 queries (4), README with results (3).

---

## Part D: Quiz (20 minutes)

1. An embedding is:
   a) A vector of numbers representing meaning b) A database row c) A compressed image d) A token ID

2. Semantic search can match "parcel never showed up" with "order hasn't arrived" because:
   a) Of SQL b) They share keywords c) Of spelling correction d) Their embeddings are close in meaning space

3. Cosine similarity of 1 means:
   a) An error b) Pointing in the same direction: very similar c) Opposite meaning d) Unrelated

4. If vectors are normalised, cosine similarity equals:
   a) Zero b) The norm c) The dot product d) Euclidean distance

5. Why must documents and queries use the same embedding model?
   a) It doesn't matter b) Licensing c) Different models produce incompatible vector spaces d) Speed only

6. An embedding model differs from a chat LLM because it:
   a) Outputs vectors, not text b) Needs no training c) Can't run on CPUs d) Generates longer text

7. ANN search is:
   a) Always exact b) A keyword method c) A type of chunking d) Approximate but much faster at scale

8. HNSW is best described as:
   a) A SQL command b) A layered graph index for fast nearest-neighbour search c) An embedding model d) A compression format

9. Metadata filtering lets you:
   a) Change embeddings b) Delete vectors c) Train the model d) Restrict results by conditions like category or user permissions

10. Which query type most benefits from BM25 keyword search?
    a) "cheap holidays" b) "SKU-48213" c) "I feel the app is slow lately" d) "help me relax"

11. A cross-encoder re-ranker:
    a) Scores query and document together for more accurate ordering b) Embeds documents in advance c) Is a vector database d) Replaces the LLM

12. Recall@3 measures:
    a) Speed b) Storage size c) Whether the correct document appears in the top 3 d) Number of dimensions

13. MRR rewards:
    a) Longer documents b) More results c) Correct results appearing higher in the ranking d) Lower cost

14. For learning with a few thousand documents, a good choice is:
    a) A sharded cluster b) No search c) Training your own embedding model d) NumPy brute force or Chroma

15. "Upsert" means:
    a) Insert, or update if the ID exists b) Sort results c) Search upwards d) Delete then crash

**Short answer.**

16. Explain embeddings to a friend using an analogy.
17. Describe the difference between keyword search and semantic search, with one example where each wins.
18. Why do we chunk long documents before embedding?
19. List the four fields typically stored per record in a vector database, and why each matters.
20. Describe how you'd evaluate and improve a retrieval system.

---

## Answer Key

### Part A

**A1.** A fixed word-level lookup gives "bank" one vector in both. A sentence embedding model reads the whole sentence, so the two sentences land in different places (finance vs river), because context changes meaning.

**A2.** (a) Very similar meaning. (b) Essentially unrelated. (c) Unrelated or somewhat opposite.

**A3.** A (smaller distance = more similar).

**A4.** Results will be essentially random/garbage: the two models' vector spaces are different "maps," so distances between them mean nothing.

**A5.** (a) keyword (b) semantic (c) keyword (d) semantic. Hybrid search handles all four.

**A6.** Found in 8 of 10 → **Recall@3 = 80%**. MRR = (1 + 0.5 + 1 + 0 + 0.333 + 1 + 1 + 0 + 0.5 + 1) / 10 = 6.333 / 10 = **0.63**.

### Part B: reference snippets

```python
import numpy as np, pandas as pd
from sentence_transformers import SentenceTransformer, CrossEncoder
model = SentenceTransformer("all-MiniLM-L6-v2")

# B1
V = model.encode(sents, normalize_embeddings=True)
sim = pd.DataFrame(V @ V.T, index=sents, columns=sents).round(2)
print(sim)
# dog↔puppies, stock crash↔shares fell↔investors, sourdough↔bread score highest.

# B2
def search(query, docs, doc_vecs, k=3):
    q = model.encode([query], normalize_embeddings=True)[0]
    scores = doc_vecs @ q
    idx = scores.argsort()[::-1][:k]
    return [(docs[i], round(float(scores[i]), 3)) for i in idx]
print(search("kitten", sents, V))

# B3
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
P = PCA(n_components=2).fit_transform(model.encode(all_sents, normalize_embeddings=True))
for topic in ["sports", "cooking", "technology"]:
    m = [t == topic for t in topics]
    plt.scatter(P[m, 0], P[m, 1], label=topic)
plt.legend(); plt.show()

# B7 - BM25 + RRF
from rank_bm25 import BM25Okapi
bm25 = BM25Okapi([t.lower().split() for t in texts])

def rrf(rankings: list[list[str]], k: int = 60) -> list[str]:
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)

def hybrid(query, ids, k=3):
    kw = [ids[i] for i in np.argsort(bm25.get_scores(query.lower().split()))[::-1][:10]]
    q = model.encode([query], normalize_embeddings=True)[0]
    vec = [ids[i] for i in np.argsort(doc_vecs @ q)[::-1][:10]]
    return rrf([kw, vec])[:k]

# B8
ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
def rerank(query, candidates):
    scores = ce.predict([(query, c) for c in candidates])
    return [c for _, c in sorted(zip(scores, candidates), reverse=True)]

# B9
Q = model.encode(questions, normalize_embeddings=True)
S = Q @ Q.T
pairs = [(questions[i], questions[j], round(float(S[i, j]), 2))
         for i in range(len(questions)) for j in range(i + 1, len(questions)) if S[i, j] > 0.8]
```

### Part D: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | a | 6 | a | 11 | a |
| 2 | d | 7 | d | 12 | c |
| 3 | b | 8 | b | 13 | c |
| 4 | c | 9 | d | 14 | d |
| 5 | c | 10 | b | 15 | a |

**16.** Like placing every sentence on a giant map by topic: sentences about the same idea are neighbours even if worded differently. An embedding is a sentence's map coordinates, so finding similar sentences = looking for nearby points.

**17.** Keyword search matches exact words (wins for "error E-4021" or a product code); semantic search matches meaning (wins for "my parcel never came" → "order hasn't arrived"). Hybrid combines both.

**18.** A single vector for a long document blends many topics into a blurry average, so specific questions match poorly; also models have input length limits, and LLMs need small, focused passages. Chunks give sharp, specific vectors.

**19.** ID (to update/delete), vector (to search), text/document (to show or give the LLM), metadata (to filter by category/date/permissions and cite sources).

**20.** Build a test set of realistic queries with known correct documents; measure Recall@k and MRR; change one thing at a time (embedding model, what to embed, chunk size, hybrid search, re-ranker, filters); re-measure and keep what helps.

**Scoring:** out of 25. ≥ 21 move on.
