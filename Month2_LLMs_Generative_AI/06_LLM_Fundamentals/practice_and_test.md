# Practice & Test 06: LLM Fundamentals

> **🛠️ Before you start:** you need a free chat assistant account; tiktoken and numpy for Part C (no API key). Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run python -c "import tiktoken; print('ok')"
> ```

This lesson is mostly conceptual, so the practice mixes thinking exercises, small experiments in a chat app (Claude.ai, ChatGPT, Gemini, any of them), and a little Python.

---

## Part A: Thinking exercises

**A1. Tokens.** Estimate tokens for: (a) a 300-word email, (b) a 10-page report (~5,000 words), (c) a 200-page book (~60,000 words). Use 1 token ≈ 0.75 words.

**A2. Context budget.** A model has a 200,000-token context window. Your system prompt is 1,500 tokens, the chat history so far is 40,000, you attach a document of 120,000 tokens, and you want up to 8,000 tokens of answer. Does it fit? How much room is left?

**A3. Cost.** Imagine a model priced at $3 per million input tokens and $15 per million output tokens. Your app handles 2,000 requests per day, each with 1,500 input tokens and 400 output tokens. What's the daily and monthly (30-day) cost? What if you switched to a model at $1 / $5?

**A4. Memory.** A user says, "The chatbot remembered my name from earlier in the conversation, so the model must be learning." Explain what's really happening.

**A5. Temperature.** Pick a temperature (low ~0.2 / high ~0.9) for each: (a) extract invoice totals into JSON, (b) brainstorm 20 startup names, (c) answer a medical FAQ from provided text, (d) write a children's bedtime story, (e) generate SQL from a question.

**A6. Hallucination.** For each scenario, name the most likely cause and one fix:
1. The model cites a research paper that doesn't exist.
2. It says the latest version of a library is one from two years ago.
3. It counts 2 "r"s in "strawberry."
4. It invents a company policy when answering an employee's question.

**A7. Training stages.** Match each to pre-training, instruction fine-tuning, or preference training:
1. Learning that Paris is the capital of France.
2. Learning to answer in a helpful Q&A format.
3. Learning to prefer a polite, accurate answer over a rude one.
4. Learning to refuse instructions for making weapons.

---

## Part B: Experiments (chat app)

Write down what you observe for each.

**B1. Knowledge cutoff.** Ask: "What is your knowledge cutoff, and what's the most recent event you know about?" Then ask about something that happened last week. Does it know? Does it admit not knowing?

**B2. Counting weakness.** Ask: "How many letter e's are in 'excellence experience'?" Then ask it to "spell it out letter by letter, then count." Compare. Why does the second approach work better?

**B3. Non-determinism.** Ask the same creative question 3 times in new chats: "Give me a one-sentence slogan for a coffee shop on Mars." Compare the answers.

**B4. Reasoning.** Ask a logic puzzle with and without "think step by step" (or with a thinking/reasoning mode on vs off if your app has one): *"A bat and ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much is the ball?"* (Correct: $0.05.)

**B5. Grounding.** Paste a short paragraph about a fictional company ("Zentrix Ltd was founded in 2019 in Nairobi and makes solar bike lights…"). Ask a question that *is* answered in it and one that *isn't*. Then add: "If the answer isn't in the text, say 'Not in the text.'" Does it hallucinate less?

**B6. Multimodal.** Upload a photo of a receipt or a chart and ask for a structured summary.

---

## Part C: Python: see tokens yourself

Install a tokenizer library and explore. (`tiktoken` is OpenAI's tokenizer; other models use different tokenizers, but the idea is the same.)

```bash
uv init token_lab && cd token_lab
uv add tiktoken
```

```python
import tiktoken

enc = tiktoken.get_encoding("o200k_base")

for text in ["Hello world", "Unbelievable results!", "def add(a, b): return a + b",
             "नमस्ते दुनिया", "strawberry", "   lots   of   spaces   "]:
    ids = enc.encode(text)
    pieces = [enc.decode([i]) for i in ids]
    print(f"{len(ids):>3} tokens | {pieces}")
```

**C1.** Run it. Which text uses the most tokens per character? Why might non-English text cost more?

**C2.** Write `estimate_cost(text, input_price_per_m, output_tokens, output_price_per_m)` that counts tokens with tiktoken and returns the dollar cost.

**C3.** Simulate temperature. Given these next-token scores, apply softmax with temperatures 0.2, 1.0 and 2.0 and print the probabilities. (Softmax turns scores into probabilities: `p = exp(s/T) / sum(exp(s/T))`.)

```python
import numpy as np
tokens = [" mat", " floor", " sofa", " roof", " moon"]
scores = np.array([3.0, 2.4, 2.0, 1.0, -1.0])
```

What happens to " moon" as temperature rises?

**C4. (Optional) Run a local model.** Install Ollama (ollama.com), run `ollama run llama3.2` (or any small model it lists), and chat with it. Compare its quality and speed to a frontier model.

---

## Part D: Quiz (20 minutes)

1. What does an LLM fundamentally do?
   a) Predicts the next token b) Searches a database of answers c) Runs SQL d) Copies text from the internet

2. Roughly how many words is 1,000 tokens in English?
   a) 4,000 b) 750 c) 1,000 d) 250

3. "Autoregressive" means:
   a) It trains itself b) It runs automatically c) It uses regression d) It generates one token at a time, feeding each back in

4. The transformer's key mechanism is:
   a) Decision trees b) Convolution c) Attention d) k-means

5. Which training stage teaches the model most of its world knowledge?
   a) Tokenisation b) Pre-training c) RLHF d) Prompting

6. RLHF uses:
   a) Human preference feedback to reward better answers b) Only labelled images c) A search engine d) Hard-coded rules

7. The context window is:
   a) The training data size b) The chat app's window size c) The max tokens the model considers at once d) The number of layers

8. Why can a chatbot "remember" earlier messages?
   a) It stores a database in its weights b) Weights update after each message c) It doesn't d) The app re-sends the conversation each time

9. High temperature leads to:
   a) More varied, creative, error-prone answers b) More focused, repetitive answers c) Shorter answers d) Faster responses

10. A hallucination is:
    a) A refusal b) A crash c) Confidently stated false information d) A slow answer

11. Which best reduces hallucination for questions about your company's policies?
    a) Use a bigger font b) Ask twice c) Higher temperature d) Provide the policy text and instruct it to answer only from it

12. A "knowledge cutoff" means:
    a) Max output length b) The date after which training data stops c) Token limit d) Price limit

13. Reasoning models are best for:
    a) Hard maths, logic and planning b) Simple greetings c) Image generation d) Lowest latency

14. Which is usually more expensive per token?
    a) They're always equal b) Output tokens c) Neither costs anything d) Input tokens

15. An open-weight model:
    a) Has no parameters b) Can't be downloaded c) Is always better d) Has published weights you can run yourself

**Short answer.**

16. Explain tokens and why they matter to cost and limits.
17. Describe the journey of a question through an LLM in 5 steps.
18. Why do LLMs struggle to count letters in words?
19. When would you choose a small, fast model over a large one?
20. Give three ways to reduce hallucinations.

---

## Answer Key

### Part A

**A1.** (a) ~400 tokens (b) ~6,700 tokens (c) ~80,000 tokens.

**A2.** 1,500 + 40,000 + 120,000 + 8,000 = 169,500. Fits; 30,500 tokens to spare.

**A3.** Input: 2,000 × 1,500 = 3M tokens/day × $3 = $9. Output: 2,000 × 400 = 0.8M × $15 = $12. **$21/day ≈ $630/month.** At $1/$5: $3 + $4 = $7/day ≈ $210/month, a third of the cost. (This is why model choice matters.)

**A4.** The model doesn't learn. The app sends the full conversation, including the message where the user gave their name, with every new request, so the name is in the context window.

**A5.** (a) low (b) high (c) low (d) high-ish (e) low.

**A6.**
1. Hallucination from pattern-matching what citations look like → provide sources/RAG, ask it to quote only given documents, verify.
2. Knowledge cutoff → give it docs or a web search tool.
3. Tokenisation (it sees chunks, not letters) → ask it to spell out letters first, or use a code tool.
4. Doesn't have the real policy, so it invents a plausible one → provide the actual policy text (RAG), instruct "say you don't know if not covered."

**A7.** 1 pre-training · 2 instruction fine-tuning · 3 preference training · 4 preference training (and fine-tuning on refusal examples).

### Part B: what you should notice

- B1: it states a cutoff and likely doesn't know last week's news unless the app has web search.
- B2: spelling it out turns each letter into separate tokens, so counting becomes reliable. ("excellence experience" has 8 e's.)
- B3: different slogans each time (non-deterministic sampling).
- B4: without reasoning, many models (and humans!) say $0.10; with step-by-step reasoning, $0.05.
- B5: the "Not in the text" instruction reduces invented answers.

### Part C

```python
# C2
def estimate_cost(text, input_price_per_m, output_tokens, output_price_per_m):
    n_in = len(enc.encode(text))
    return n_in / 1e6 * input_price_per_m + output_tokens / 1e6 * output_price_per_m

# C3
for T in [0.2, 1.0, 2.0]:
    e = np.exp(scores / T)
    p = e / e.sum()
    print(T, dict(zip(tokens, p.round(3))))
# At T=0.2, " mat" gets ~95%; " moon" ≈ 0.
# At T=2.0, the distribution flattens and " moon" rises to a few percent → more surprising (and wrong) choices.
```

C1: non-English scripts and unusual spacing often take more tokens per character, because the tokenizer's vocabulary was built mostly from English-heavy text.

### Part D: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | a | 6 | a | 11 | d |
| 2 | b | 7 | c | 12 | b |
| 3 | d | 8 | d | 13 | a |
| 4 | c | 9 | a | 14 | b |
| 5 | b | 10 | c | 15 | d |

**16.** Tokens are the chunks of text (~¾ word) the model reads and writes. Context limits, pricing and speed are all counted in tokens, so longer prompts and answers cost more and must fit in the context window.

**17.** App builds the full input (system prompt + history + message) → tokeniser converts to IDs → embeddings → transformer layers with attention compute next-token probabilities → sample a token, append, repeat until stop → detokenise and return.

**18.** They see tokens (chunks like "straw" + "berry"), not individual letters, so letter-level information isn't directly visible.

**19.** For simple, high-volume or latency-sensitive tasks (classification, extraction, short replies, routing) where the small model's quality is good enough. It's cheaper and faster.

**20.** Provide source material and instruct "answer only from it"; allow/encourage "I don't know"; ask for quotes/citations; give tools (search, calculator); lower temperature; verify outputs.

**Scoring:** out of 25. ≥ 21 move on.
