# 09 · Embeddings & Vector Databases

*Month 2, Week 7. Reading time: about 70 minutes. Assumes Lessons 02 (NumPy), 06 and 08.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Vectors: a quick refresher
- What an embedding is
- Visualising meaning space
- Measuring similarity
- Embedding models: which ones?
- Creating embeddings in Python
- Brute-force search: the simple way
- Why vector databases exist: approximate search at scale
- What a vector database stores
- Metadata filtering
- Keyword search still matters: hybrid search
- Re-ranking
- Chunking (preview)
- Choosing a vector database (2026)
- Evaluating retrieval

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init embed_lab && cd embed_lab
uv add sentence-transformers chromadb numpy pandas matplotlib scikit-learn rank-bm25
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [08 · LLM APIs](../08_LLM_APIs/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [10 · RAG Applications](../10_RAG_Applications/README.md) ➡️
