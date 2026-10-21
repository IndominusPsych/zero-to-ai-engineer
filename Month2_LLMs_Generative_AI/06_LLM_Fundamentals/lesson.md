# Lesson 06: LLM Fundamentals

*Month 2, Week 5. Reading time: about 75 minutes. Assumes Month 1 (especially Lesson 04).*

---

## 🛠️ Setup for this lesson

| You need | Why | How to get it |
|---|---|---|
| A free chat assistant account | Experiments with tokens, context and hallucination | claude.ai, chatgpt.com or gemini.google.com (Setup Guide Step 7) |
| **tiktoken**, **numpy** (practice only) | Count tokens and play with probabilities in Python | `uv add` (below) |
| No API key yet | You'll create one in Lesson 08 | - |

**Install:**

```bash
cd ~/ai-engineer-projects
uv init llm_basics && cd llm_basics
uv add tiktoken numpy
```

**Check it works:**

```bash
uv run python -c "import tiktoken; e = tiktoken.get_encoding('o200k_base'); print(len(e.encode('Hello, how are you today?')), 'tokens')"
# The first run downloads a small token list, so you need internet.
```

`tiktoken` is OpenAI's tokenizer. Claude uses a different one, but the counts are close enough to build intuition. Lesson 08 shows how to count Claude tokens exactly.

Stuck? See the step-by-step instructions and the troubleshooting table in [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md).

---

## 1. The big picture

### What is this, in simple words?

An **LLM** (Large Language Model) is a computer program that has read a gigantic amount of text and learned to **predict what text comes next**. That one simple skill, done extremely well, turns out to let it answer questions, write essays and code, translate, summarise, and hold a conversation.

ChatGPT, Claude, Gemini, Llama and DeepSeek are all built on LLMs.

Analogy: your phone keyboard suggests the next word as you type. An LLM is that idea scaled up enormously. It has read a large fraction of the public internet plus many books, and it holds billions of learned settings instead of a few thousand, so its "next word" guesses are good enough to write a whole, sensible essay one piece at a time.

### Which field does it belong to?

Remember the nested circles from Lesson 04:

```
AI ⊃ Machine learning ⊃ Deep learning ⊃ Generative AI ⊃ LLMs
```

- **Generative AI** means models that *create* new content (text, images, audio, video, code) rather than just labelling or predicting a number.
- **LLMs** are the text-generating branch. Many are now **multimodal**: they can also take in images, audio or documents.

The field of making computers handle human language is called **NLP** (Natural Language Processing). LLMs have taken over most of it.

### Why does it matter?

Before LLMs, every language task needed its own specially trained model: one for translation, one for spam, one for summaries. Now **one general model** does all of them, just by being *asked* in plain English. That's why "AI engineering" exploded: you can build powerful products without training models yourself, by calling an LLM through an API (Lesson 08) and connecting it to data (Lessons 09–10) and tools (Month 3).

| Before LLMs | With LLMs |
|---|---|
| Collect thousands of labelled examples per task | Describe the task in words ("prompting") |
| Train a separate model for each task | One model, many tasks |
| Weeks of ML work | Minutes to a first prototype |

> **In simple words:** An LLM is a huge neural network trained to predict the next piece of text. That simple skill makes it a general-purpose language engine you can use for almost any text task just by asking.

---

## 2. Core concepts

### 2.1 Tokens: how LLMs see text

LLMs don't read letters or whole words. They read **tokens**: chunks of text, often a word or part of a word.

```
"Unbelievable results!"  →  ["Un", "believ", "able", " results", "!"]
```

A **tokenizer** is the tool that splits text into tokens and gives each one an ID number. The model only ever sees those numbers.

Rough rules of thumb for English:

| | ≈ |
|---|---|
| 1 token | ¾ of a word, or ~4 characters |
| 100 tokens | ~75 words |
| 1 page of text | ~500–700 tokens |

Why care? Because **everything about LLMs is measured in tokens**: how much you can send, how much it costs, how fast it is. Languages other than English, and code, often use more tokens per word.

The **vocabulary** is the full list of tokens a model knows, often 100,000–200,000 of them.

### 2.2 Next-token prediction

Here is the entire core job of an LLM:

> Given a sequence of tokens, output a **probability** for every possible next token.

```
Input:  "The cat sat on the"
Output: " mat" 31%  |  " floor" 18%  |  " sofa" 12%  |  " roof" 4%  | ... (100,000+ options)
```

Then one token is picked, added to the input, and the process repeats:

```
"The cat sat on the"           → " mat"
"The cat sat on the mat"       → "."
"The cat sat on the mat."      → " It"
...
```

Generating text one token at a time, each time feeding the result back in, is called **autoregressive generation**. This is why you see chatbot answers appear word by word: it's literally being produced that way.

### 2.3 Parameters: the model's learned knowledge

In Lesson 04 you learned models have **parameters** (weights): adjustable numbers tuned during training. A house-price model might have 10. LLMs have **billions** (written "B"): 8B, 70B, 400B+, and frontier models likely more (companies often don't publish exact sizes).

These parameters store everything the model "knows": grammar, facts, writing styles, coding patterns, reasoning habits. Not as a database of sentences, but as patterns spread across all the numbers.

More parameters generally means more capability, but also more cost and slower responses. That's why providers offer **model families** in sizes: e.g. Anthropic's Claude comes as Haiku (small, fast, cheap), Sonnet (balanced) and Opus (largest, most capable).

### 2.4 Embeddings: turning tokens into meaning-numbers

The first thing a model does with each token ID is look up its **embedding**: a long list of numbers (a **vector**, Lesson 02) that represents the token's meaning, e.g. 4,096 numbers per token.

The magic property: **tokens with similar meanings get similar vectors.** "king" and "queen" end up close together; "king" and "banana" far apart. You'll use this directly in Lesson 09 to search documents by meaning.

### 2.5 The transformer and attention

The design (**architecture**) of almost every LLM is the **transformer**, introduced by Google researchers in 2017 in a paper titled *"Attention Is All You Need."* (The "T" in GPT stands for Transformer.)

Its key idea is **attention**: when processing each token, the model looks at all the other tokens and decides **how much each one matters** for understanding this one.

Example: *"The trophy didn't fit in the suitcase because **it** was too big."* What does "it" mean? Attention lets the model connect "it" strongly to "trophy" (because "too big" makes sense for the trophy).

```
 "The trophy didn't fit in the suitcase because it was too big"
       ▲                         ▲            │
       └──── strong attention ───┼────────────┘
                     weak ───────┘
```

A transformer stacks dozens of **layers**. Each layer has attention (tokens share information) followed by a small neural network (each token "thinks" about what it gathered). Early layers pick up grammar; later layers capture meaning, facts and reasoning.

```
 tokens ─▶ embeddings ─▶ [attention + neural net] × N layers ─▶ probabilities for next token
```

You don't need the maths. Just remember: **tokens → vectors → many layers of attention → next-token probabilities.**

### 2.6 How LLMs are trained: three stages

| Stage | What happens | Analogy | Result |
|---|---|---|---|
| **1. Pre-training** | Predict the next token on trillions of tokens of text (web, books, code). Takes months on thousands of GPUs (graphics chips used for maths). | Reading a whole library | A **base model**: knows a lot, but just continues text; doesn't follow instructions well |
| **2. Fine-tuning / instruction tuning** (also called **SFT**, supervised fine-tuning) | Train further on examples of questions with good answers | Apprenticeship with a mentor | Follows instructions, answers like an assistant |
| **3. Preference training** (**RLHF**: Reinforcement Learning from Human Feedback; and variants using AI feedback, like Anthropic's **Constitutional AI**) | People (or AI judges following written principles) compare answers; the model is rewarded for better ones (Lesson 04's reinforcement learning!) | Getting feedback on your work | Helpful, honest, harmless; refuses dangerous requests |

Modern models also get extra training on **reasoning**: rewarded for solving maths and coding problems correctly with step-by-step thinking.

The model that results from all this is **frozen**: its parameters don't change when you chat with it. It doesn't learn from your conversation (unless the company later uses data for training, which depends on its policies and your settings).

### 2.7 Knowledge cutoff

Because training data is collected up to some date, a model doesn't know about events after its **knowledge cutoff** (training cutoff). Ask about yesterday's news and it may not know, or may make something up. Solutions: give it the information yourself (Lesson 10, RAG) or give it a web search tool (Month 3).

### 2.8 The context window: the model's working memory

The **context window** is the maximum number of tokens the model can consider at once: your instructions + the conversation so far + any documents + its own answer.

Analogy: a desk. Everything the model can use must fit on the desk right now. Anything that falls off the desk is invisible to it.

| Era | Typical context window |
|---|---|
| 2020 | ~2,000 tokens (a few pages) |
| 2023 | 8,000–100,000 |
| 2025–2026 | 200,000 to 1,000,000+ tokens (several books) for frontier models |

Important consequences:

- **LLMs have no memory between API calls.** A chatbot "remembers" earlier messages only because the app **re-sends the whole conversation every time**. (You'll build this in Lesson 08.)
- Bigger context costs more and is slower. And models can pay less attention to details buried in the middle of very long inputs, a known weakness sometimes called **"lost in the middle."**

### 2.9 Generation settings: temperature and friends

When the model has probabilities for the next token, *how* do we pick one? **Sampling settings** control this:

| Setting | What it does | Low value | High value |
|---|---|---|---|
| **Temperature** | How adventurous the choice is | Picks the most likely tokens → focused, consistent, repetitive | Picks less likely tokens more often → creative, varied, more errors |
| **Top-p** (nucleus sampling) | Only consider the smallest set of tokens whose probabilities add up to p | Very safe choices | Wider choices |
| **Max tokens** | Hard limit on output length | Short answers (may cut off mid-sentence) | Long answers allowed |
| **Stop sequences** | Text that makes generation stop | | |

Rule of thumb: **temperature 0–0.3 for facts, extraction, code; 0.7–1.0 for brainstorming and creative writing.** (Some newer reasoning models fix or restrict these settings.)

Even at temperature 0, outputs aren't guaranteed to be identical every time: LLMs are **non-deterministic** in practice. Design your apps to cope with variation.

### 2.10 Hallucinations

A **hallucination** is when an LLM states something false with full confidence: a fake citation, a wrong date, a non-existent library function.

Why it happens: the model is trained to produce *plausible-sounding* next tokens, not to check facts against a database. If it doesn't know, the most "plausible" continuation may be invented.

How to reduce it (you'll practise all of these):

| Technique | Lesson |
|---|---|
| Give it the source material and say "answer only from this" | 07, 10 (RAG) |
| Allow "I don't know" explicitly | 07 |
| Ask for quotes/citations from the provided text | 07, 10 |
| Give it tools (search, calculator, database) | 12 |
| Verify outputs with code or a second check | 08, 13 |
| Use lower temperature for factual tasks | 06 |

### 2.11 Reasoning ("thinking") models

Since late 2024, many models can **think before answering**: they generate hidden or visible step-by-step reasoning first, then the final answer. This is called **extended thinking**, **reasoning**, or **test-time compute** (spending more computation at answer time).

- Much better at maths, logic, planning, complex code.
- Slower and costs more (thinking tokens are billed).
- Usually controlled with a setting such as a "thinking budget" or "reasoning effort" (low/medium/high).

Use them for hard problems; use fast models for simple ones.

### 2.12 Multimodal models

**Multimodal** models accept (and sometimes produce) more than text: images, PDFs, audio, video. You can send a photo of a receipt and ask "what's the total?" or a chart and ask "what's the trend?" Images are converted into tokens too, so they use up context and cost.

### 2.13 Open vs closed models

| | **Closed / proprietary** | **Open-weight** |
|---|---|---|
| Examples (2026) | Anthropic Claude, OpenAI GPT, Google Gemini | Meta Llama, Mistral, DeepSeek, Alibaba Qwen, Google Gemma, OpenAI's gpt-oss |
| How you use it | Through the company's API or app | Download the weights and run yourself, or use a host |
| Pros | Usually most capable; no hardware needed | Privacy, control, can fine-tune, no per-token fee if self-hosted |
| Cons | Pay per token; data goes to provider | Need powerful hardware (GPUs) or a host; you handle safety |

**Weights** = the model's parameters, saved as files. "Open-weight" means those files are published. Tools like **Ollama** let you run small open models on a laptop.

### 2.14 Cost and speed

API pricing is **per token**, usually quoted per million tokens, with **output tokens costing more than input tokens** (often 4–5×). Two speed measures:

- **Latency / time to first token**: how long before the answer starts.
- **Throughput**: tokens per second once it's going.

Small models are cheaper and faster; large and reasoning models are slower and pricier. Choosing the *smallest model that does the job well* is a core AI-engineering skill.

### 2.15 What LLMs are good and bad at

| ✅ Strong | ⚠️ Weak / careful |
|---|---|
| Writing, rewriting, summarising, translating | Exact arithmetic on big numbers (use a calculator tool) |
| Explaining concepts, answering general questions | Facts after the knowledge cutoff |
| Writing and explaining code | Precise counting (letters in a word, words in a text), because they see tokens |
| Extracting structured data from messy text | Guaranteed consistency (non-deterministic) |
| Classifying, tagging, sentiment | Citing sources they weren't given (may hallucinate) |
| Brainstorming, role-play, tutoring | Knowing what they don't know |
| Reasoning through multi-step problems (especially reasoning models) | Very long, detailed instructions buried mid-context |

> **In simple words:** Text becomes tokens; tokens become meaning-vectors; a transformer's attention layers mix them and predict the next token, one at a time. Training = pre-training (read everything) + fine-tuning (follow instructions) + preference training (be helpful and safe). The context window is its desk; it has no memory beyond what you send. Temperature controls creativity. It can hallucinate, so ground it in sources and tools.

---

## 3. How it works: one question, start to finish

Let's follow a single request through an LLM.

**You type:** *"What's the capital of Australia? Answer in one word."*

### Step 1: The app builds the full input

The chat app doesn't send just your text. It assembles the whole context:

```
[system]  You are a helpful assistant. Today is 2026-10-20.
[user]    What's the capital of Australia? Answer in one word.
[assistant] ▌   ← the model will continue from here
```

The **system prompt** is hidden instructions from the app's developer that set behaviour (Lesson 07). The roles (`system`, `user`, `assistant`) are marked with special tokens so the model knows who said what.

### Step 2: Tokenisation

```
"What's the capital of Australia? Answer in one word."
→ ["What", "'s", " the", " capital", " of", " Australia", "?", " Answer", " in", " one", " word", "."]
→ [3923, 596, 279, 6864, 315, 8494, 30, 22559, 304, 832, 3492, 13]   (IDs are illustrative)
```

About 12 tokens, plus the system prompt and role markers: maybe ~40 input tokens total.

### Step 3: Embedding

Each ID is swapped for its vector of thousands of numbers. Now the input is a grid (a matrix: tokens × numbers).

### Step 4: Through the transformer layers

In each of dozens of layers, attention lets tokens share information:

- " capital" pays attention to " Australia" → *we need the capital city of a country*.
- " one word" shapes the answer format.
- Facts stored in the weights during pre-training ("Canberra is the capital of Australia," seen thousands of times) get activated.

### Step 5: Next-token probabilities

At the last position, the model outputs probabilities:

```
" Canberra"  92.1%
" Sydney"     5.3%    ← a common misconception it also saw in training!
" The"        1.2%
...
```

### Step 6: Sampling

With low temperature, " Canberra" is almost certainly picked. With a very high temperature, there's a small chance of " Sydney": a **hallucination caused by sampling**.

### Step 7: Repeat until done

```
"... Answer in one word. Canberra"  → next token: "."  → then a special end-of-turn token → stop
```

### Step 8: Return to you

The output tokens are converted back to text (**detokenised**) and shown: **"Canberra."** The app reports usage, e.g. 40 input tokens and 3 output tokens, which is what you're billed for.

### Step 9: Your follow-up question

You ask *"And its population?"* The model has no memory, so the app sends **everything again**: system prompt + first question + "Canberra." + new question. That's how "it" in your follow-up resolves to Canberra. And it's why long chats get slower and more expensive.

### The whole pipeline

```
 your text ─▶ app adds system prompt + history ─▶ tokenizer ─▶ token IDs ─▶ embeddings
                                                                              │
     ┌────────────────────────────────────────────────────────────────────────┘
     ▼
 transformer layers (attention + neural nets) × N ─▶ probabilities ─▶ sample (temperature)
     ▲                                                                   │
     └──────────── append token, repeat until end/max tokens ◀───────────┘
                                                                         │
                                               detokenise ─▶ answer + token usage (billing)
```

> **In simple words:** The app wraps your message with instructions and history, the tokenizer turns it into numbers, the transformer predicts the next token's probabilities, one is picked based on temperature, and the loop repeats until done. Every new message re-sends the whole conversation.

---

## 4. Key terms (in order)

| Term | Plain meaning |
|---|---|
| **LLM** | Large Language Model: a huge neural network trained to predict the next text. |
| **Generative AI** | AI that creates new content. |
| **Multimodal** | Handles more than text: images, audio, PDFs. |
| **NLP** | Natural Language Processing: computers working with human language. |
| **Token** | A chunk of text (≈ ¾ word) the model reads and writes. |
| **Tokenizer** | Splits text into tokens and IDs. |
| **Vocabulary** | All tokens a model knows. |
| **Next-token prediction** | The core task: give probabilities for what comes next. |
| **Autoregressive** | Generating one token at a time, feeding each back in. |
| **Parameters / weights** | The billions of learned numbers inside the model. |
| **Model family** | Different sizes of the same model line (e.g. Haiku / Sonnet / Opus). |
| **Embedding** | A vector of numbers representing meaning. |
| **Architecture** | The design of a neural network. |
| **Transformer** | The architecture behind LLMs (2017). |
| **Attention** | Mechanism letting each token weigh how much other tokens matter. |
| **Layer** | One processing stage; transformers stack many. |
| **Pre-training** | Learning next-token prediction on huge text collections. |
| **GPU** | Graphics chip used for the heavy maths of AI. |
| **Base model** | A pre-trained model that only continues text. |
| **Fine-tuning / SFT** | Extra training on examples to specialise or follow instructions. |
| **RLHF / Constitutional AI** | Training with human (or principle-guided AI) feedback on which answers are better. |
| **Knowledge cutoff** | The date after which the model knows nothing. |
| **Context window** | Max tokens the model can consider at once (input + output). |
| **Lost in the middle** | Tendency to overlook details in the middle of very long inputs. |
| **Sampling** | Picking the next token from the probabilities. |
| **Temperature** | Randomness of sampling; low = focused, high = creative. |
| **Top-p** | Only sample from the most likely tokens adding up to probability p. |
| **Max tokens** | Output length limit. |
| **Stop sequence** | Text that ends generation. |
| **Non-deterministic** | May give different outputs for the same input. |
| **Hallucination** | Confidently stated false information. |
| **Reasoning / extended thinking** | Model thinks step by step before answering. |
| **Test-time compute** | Spending more computation at answer time for better results. |
| **Open-weight vs closed** | Weights downloadable vs only via the company's API. |
| **Ollama** | Tool to run open models locally. |
| **Latency / throughput** | Wait before the answer starts / tokens per second. |
| **System prompt** | Hidden developer instructions that set the model's behaviour. |
| **Detokenise** | Turn token IDs back into text. |

> **In simple words:** Tokens, context window, temperature and hallucination are the four words you'll use every single day from now on.

---

## 5. The people involved

| Who | What they do | LLMs day to day |
|---|---|---|
| **AI labs / model providers** (Anthropic, OpenAI, Google DeepMind, Meta, Mistral, DeepSeek, Alibaba…) | Train foundation models | Research, massive training runs, safety testing, releasing new model versions every few months. |
| **ML researchers** | Invent new methods | Improve architectures, training, reasoning, efficiency. |
| **Safety & alignment researchers** | Make models helpful, honest and harmless | Red-teaming (trying to make models misbehave), evaluations, interpretability (understanding what's inside). |
| **Data annotators / raters** | Write and rank example answers | Provide the feedback used in fine-tuning and RLHF. |
| **Cloud and chip companies** (NVIDIA, AWS, Google Cloud, Microsoft Azure) | Provide GPUs and hosting | Many models are also offered through their platforms (e.g. Claude on AWS Bedrock and Google Vertex AI). |
| **AI engineers** (you!) | Build products on top of models | Choose models, write prompts, connect data and tools, evaluate quality, control costs. |
| **Product teams** | Decide what to build | Balance capability, cost, speed and risk. |
| **End users** | Use AI apps | Need to understand AI can be wrong; benefit from good app design. |
| **Policy makers / regulators** | Set rules | E.g. the EU AI Act's obligations for general-purpose AI models, rolling in during 2025–2027. |

> **In simple words:** Labs build the models, raters and safety teams shape their behaviour, cloud companies power them, and AI engineers like you turn them into useful products for real people.

---

## 6. Common misconceptions and beginner mistakes

| Myth / mistake | Reality |
|---|---|
| "The LLM looks things up on the internet." | Not by default. It answers from patterns in its weights. Search only happens if the app gives it a search tool. |
| "It remembers our past chats." | The model doesn't. Apps may store and re-send history or "memories" as text in the context. |
| "It learns from my conversation in real time." | Weights are frozen during use. |
| "It understands like a human." | It's a powerful pattern predictor. It can reason impressively *and* fail at things a child wouldn't. Treat it as a capable but fallible assistant. |
| "If it sounds confident, it's correct." | Confidence and correctness are unrelated. Verify important facts. |
| "Tokens = words." | ≈ ¾ word in English; more tokens for code and many other languages. |
| "Bigger model is always better." | Smaller models are cheaper, faster and often good enough. Choose per task. |
| "Temperature 0 means identical answers every time." | Usually very similar, not guaranteed identical. |
| "A huge context window means I can dump everything in." | Cost and latency grow, and details can get lost. Send what's relevant (Lesson 10). |
| "It can count letters or do big arithmetic perfectly." | Token-based models struggle with exact counting and long arithmetic; give them a code tool. |
| "Open-weight means 'free and easy'." | You pay in hardware, setup and maintenance. |
| "Model X is the best, forever." | Rankings change every few months. Build so you can swap models. |

> **In simple words:** No internet, no memory, no learning during use, no guaranteed truth. Powerful but fallible. Pick the right size, send relevant context, and verify.

---

## 7. One-page recap

### The 10 things to remember

1. **An LLM predicts the next token,** one at a time, from probabilities.
2. **Tokens ≈ ¾ of a word.** Cost, limits and speed are all measured in tokens.
3. **Transformer + attention** is the architecture: each token weighs every other token.
4. **Training = pre-training → instruction fine-tuning → preference training (RLHF/Constitutional AI).**
5. **Weights are frozen;** the model doesn't learn or remember between calls.
6. **The context window is its desk;** apps re-send history each turn.
7. **Knowledge cutoff:** no knowledge of recent events unless you provide it.
8. **Temperature:** low for facts/code, higher for creativity.
9. **Hallucinations happen:** ground answers in sources, allow "I don't know", use tools, verify.
10. **Choose models by task:** small/fast for simple jobs, large or reasoning models for hard ones; output tokens cost more.

### What to learn next

➡️ **Lesson 07: Prompt Engineering.** Now that you know how an LLM processes your input, you'll learn how to write that input so you reliably get excellent output.
