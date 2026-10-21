# 06 · LLM Fundamentals

*Month 2, Week 5. Reading time: about 75 minutes. Assumes Month 1 (especially Lesson 04).*

| Step | File | What to do |
|---|---|---|
| 1 | 📖 [**lesson.md**](lesson.md) | Read the beginner explanation (7 sections, with tables, diagrams and a worked example). Start with its 🛠️ setup box. |
| 2 | ✍️ [**practice_and_test.md**](practice_and_test.md) | Do the exercises and mini-project, then take the quiz. Cover the answer key until you've tried. |

## What you'll learn

- Tokens: how LLMs see text
- Next-token prediction
- Parameters: the model's learned knowledge
- Embeddings: turning tokens into meaning-numbers
- The transformer and attention
- How LLMs are trained: three stages
- Knowledge cutoff
- The context window: the model's working memory
- Generation settings: temperature and friends
- Hallucinations
- Reasoning ("thinking") models
- Multimodal models
- Open vs closed models
- Cost and speed
- What LLMs are good and bad at

## Quick setup

```bash
cd ~/ai-engineer-projects
uv init llm_basics && cd llm_basics
uv add tiktoken numpy
```

Full details, a "check it works" command and fixes for common problems are at the top of [lesson.md](lesson.md) and in the [Setup Guide](../../00_SETUP_Install_Guide.md).

---

⬅️ Previous: [05 · Build 2–3 Small Projects](../../Month1_AI_Python_Foundations/05_Small_Projects/README.md)  ·  ⬆️ [Month overview](../README.md) · [Course home](../../README.md)  ·  Next: [07 · Prompt Engineering](../07_Prompt_Engineering/README.md) ➡️
