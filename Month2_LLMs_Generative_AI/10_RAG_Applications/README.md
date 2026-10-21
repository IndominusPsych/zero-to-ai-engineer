# 10 · RAG Applications

*Month 2, Weeks 7–8. Reading time: about 75 minutes. Assumes Lessons 06–09.*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- The two halves of every RAG system
- Loading documents
- Chunking: the most important design choice
- Retrieval: getting the right chunks
- Augmentation: building the prompt
- Generation and citations
- Grounding and faithfulness
- Conversational RAG
- RAG vs long context vs fine-tuning
- Evaluating RAG
- Common failure modes (and fixes)
- Beyond basic RAG (names to know)

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init rag_lab && cd rag_lab
uv add anthropic python-dotenv pypdf sentence-transformers chromadb pydantic rank-bm25
echo "ANTHROPIC_API_KEY=sk-ant-...your key..." > .env
printf ".env\n.venv/\n__pycache__/\n" >> .gitignore   # never commit your key
mkdir docs              # put your .md / .pdf files here
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [09 · Embeddings & Vector Databases](../09_Embeddings_Vector_Databases/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [11 · Build an AI-Powered Project](../11_AI_Powered_Project/README.md) ➡️
