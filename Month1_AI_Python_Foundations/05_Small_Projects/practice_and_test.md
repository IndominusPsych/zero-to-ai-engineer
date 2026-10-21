# Practice & Test 05: Small Projects

> **🛠️ Before you start:** you need pandas, matplotlib, pytest, ruff; Project B adds requests + streamlit; Project C adds scikit-learn + joblib + streamlit; Git/GitHub for publishing. Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run pytest && uv run ruff check .
> ```

This file has: the full specs for Projects B and C (A is walked through in the lesson), extra project ideas, a universal project checklist, and a short quiz.

---

## Project A: Personal Expense Analyzer (finish it)

Follow Lesson 05 Section 3. Then add **two** nice-to-haves of your choice:

- [ ] Keyword auto-categorisation (with tests)
- [ ] Budget limits from a `budgets.json` file with warnings
- [ ] Streamlit version (`app.py`) with file upload and charts
- [ ] Month-over-month change ("Food spending up 23% vs last month")
- [ ] Use your real bank export (remove personal data before committing! Commit only `sample.csv`)

---

## Project B: Live Data Dashboard (API → Pandas → Streamlit)

**Goal:** a web dashboard that fetches live data from a free API, cleans it with Pandas, and shows charts.

**Pick one data source:**

| Idea | API (free, no key unless noted) |
|---|---|
| Weather comparison across cities | Open-Meteo `api.open-meteo.com` |
| Country statistics explorer | REST Countries `restcountries.com` |
| Crypto price tracker | CoinGecko `api.coingecko.com/api/v3` (free tier, may need demo key) |
| Earthquake monitor | USGS `earthquake.usgs.gov/fdsnws/event/1/query?format=geojson` |
| GitHub profile analyser | GitHub REST API `api.github.com/users/{name}/repos` |

### Milestones

| # | Milestone | Done when |
|---|---|---|
| 1 | Requirements + skeleton | README draft with must-have list; `uv init --package`; `.gitignore`; first commit |
| 2 | `client.py` | Function fetches data with `timeout`, `raise_for_status`, retry on 429/5xx |
| 3 | `models.py` | Pydantic models validate the fields you use |
| 4 | `transform.py` | Converts validated data to a clean DataFrame; ≥ 3 pytest tests using a saved sample JSON (no network in tests!) |
| 5 | `app.py` | Streamlit page: inputs (city/country/date), a metric row (`st.metric`), a table (`st.dataframe`), 2 charts |
| 6 | Caching | `@st.cache_data(ttl=600)` on the fetch function so you don't hammer the API |
| 7 | Errors | Friendly message if the API is down (`st.error`) |
| 8 | Ship | README with screenshot/GIF, run instructions, "What I learned"; pushed |

**Tip for tests:** save one real API response to `tests/fixtures/sample.json` and test your transform on it. Tests should never depend on the internet.

### Starter skeleton

```python
# src/dashboard/client.py
import time, requests

def get_json(url: str, params: dict | None = None, tries: int = 3) -> dict:
    for attempt in range(tries):
        try:
            r = requests.get(url, params=params, timeout=10)
            if r.status_code in (429, 500, 502, 503):
                raise requests.HTTPError(f"retryable {r.status_code}")
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if attempt == tries - 1:
                raise
            time.sleep(2 ** attempt)
```

```python
# app.py
import streamlit as st
from dashboard.client import get_json
from dashboard.transform import to_dataframe

st.set_page_config(page_title="Earthquake Monitor", layout="wide")
st.title("🌍 Earthquakes in the last 7 days")

@st.cache_data(ttl=600)
def load(min_mag: float):
    raw = get_json("https://earthquake.usgs.gov/fdsnws/event/1/query",
                   {"format": "geojson", "starttime": "NOW-7days", "minmagnitude": min_mag})
    return to_dataframe(raw)

min_mag = st.slider("Minimum magnitude", 2.5, 7.0, 4.5, 0.5)
try:
    df = load(min_mag)
except Exception as e:
    st.error(f"Couldn't load data: {e}")
    st.stop()

c1, c2 = st.columns(2)
c1.metric("Quakes", len(df)); c2.metric("Strongest", f"{df['mag'].max():.1f}")
st.map(df[["lat", "lon"]])
st.bar_chart(df.groupby(df["time"].dt.date).size())
st.dataframe(df.sort_values("mag", ascending=False))
```

(Note: `starttime=NOW-7days` is a USGS convenience; if it errors, compute the date with `datetime` and pass `YYYY-MM-DD`.)

### Rubric

| Criterion | Points |
|---|---|
| Robust API client (timeout, status, retry) | 2 |
| Pydantic validation | 2 |
| Clean transform with ≥ 3 offline tests | 3 |
| Streamlit UI with inputs, metrics, 2 charts | 3 |
| Caching + friendly errors | 2 |
| README with screenshot + run steps | 2 |
| Clean git history (≥ 8 meaningful commits) | 1 |
| **Total** | **15** (≥ 12 = portfolio-ready) |

---

## Project C: ML Predictor App

**Goal:** train a classification or regression model, evaluate it honestly, and let people try it in a Streamlit app.

**Pick a dataset:**

| Idea | Source |
|---|---|
| Titanic survival | Search "titanic.csv" (Kaggle or GitHub mirrors) |
| Wine quality | UCI Machine Learning Repository |
| Heart disease risk | UCI / Kaggle |
| Student performance | UCI |
| Your own generated data (as in Lesson 04) | Yourself |

### Milestones

| # | Milestone | Done when |
|---|---|---|
| 1 | `notebooks/explore.ipynb` | 5 bullet findings, 3 charts, missing-value summary |
| 2 | Problem statement | Task type, label, metric chosen *with a reason*, baseline score |
| 3 | `train.py` | Split → pipeline (impute/encode/scale) → compare ≥ 3 models with 5-fold CV → print a results table |
| 4 | Evaluation | Final test score once; confusion matrix or residual plot; train-vs-test check |
| 5 | Save | `models/model.joblib` + `models/metrics.json` |
| 6 | `app.py` | Streamlit form with inputs for each feature → prediction (+ probability for classifiers) |
| 7 | Honesty section in README | Limitations: dataset size, possible bias, when not to trust the model |
| 8 | Ship | README with results table, screenshot, run steps |

### Starter for the app

```python
# app.py
import joblib, pandas as pd, streamlit as st

model = joblib.load("models/model.joblib")
st.title("🚢 Would you survive the Titanic?")
pclass = st.selectbox("Ticket class", [1, 2, 3])
sex = st.radio("Sex", ["male", "female"])
age = st.slider("Age", 0, 80, 30)
fare = st.number_input("Fare", 0.0, 500.0, 30.0)

if st.button("Predict"):
    row = pd.DataFrame([{"Pclass": pclass, "Sex": sex, "Age": age, "Fare": fare}])
    p = model.predict_proba(row)[0, 1]
    st.metric("Survival probability", f"{p:.0%}")
```

### Rubric

| Criterion | Points |
|---|---|
| Clear problem + metric + baseline | 2 |
| Pipeline without leakage | 3 |
| ≥ 3 models compared with CV | 2 |
| Honest final evaluation (test once, overfitting check) | 3 |
| Working app | 2 |
| Limitations section | 1 |
| README + results table | 2 |
| **Total** | **15** (≥ 12 = portfolio-ready) |

---

## Extra project ideas (if you want variety)

| Project | Main skills |
|---|---|
| Habit tracker CLI with JSON storage and weekly stats | Python, files, JSON, CLI |
| Movie watchlist using the OMDb API (free key) | APIs, `.env` secrets, Pandas |
| Job-posting analyser: scrape/collect 100 postings into CSV, find top skills | Pandas, text cleaning, `value_counts` |
| Spam classifier on the SMS Spam Collection dataset | ML classification, text features (`TfidfVectorizer`), precision/recall |
| Customer segmentation with k-means | Unsupervised ML, scaling, charts |

---

## Universal "ready to ship" checklist

Run this on every project before calling it done:

- [ ] Fresh-clone test: `git clone <url> /tmp/test && cd /tmp/test && uv sync && <run command>` works
- [ ] README: title, one-liner, screenshot, features, install/run, how it works, learned, next steps
- [ ] `.gitignore` covers `.env`, `.venv/`, `__pycache__/`, big data
- [ ] `.env.example` if any keys are needed
- [ ] `uv run pytest` passes
- [ ] `uv run ruff check .` is clean
- [ ] No hard-coded personal paths
- [ ] Sample data included (small, no personal info)
- [ ] I can explain every line

---

## Quiz (15 minutes)

1. What is an MVP?
   a) A testing tool b) The final polished product c) Most Valuable Player d) The smallest version that works and is useful

2. Which is the best first-project scope?
   a) A CLI that summarises your expenses b) A full social network c) A stock-trading AI d) A self-driving car simulator

3. Separation of concerns means:
   a) Separate computers b) Each file/function has one job c) Keep worries away d) Separate Git branches

4. Where do uv projects list their dependencies?
   a) .env b) README.md c) pyproject.toml d) .gitignore

5. A pytest test function must:
   a) Print "pass" b) Use input() c) Start with `test_` and use `assert` d) Be in main.py

6. Why save a sample API response for tests?
   a) Tests run offline and give the same result every time b) It's faster to write c) To hide the API d) Required by GitHub

7. What does `@st.cache_data(ttl=600)` do?
   a) Logs errors b) Remembers results for 10 minutes to avoid repeat calls c) Deletes data d) Encrypts the app

8. The "fresh clone test" checks:
   a) The code is formatted b) Git is installed c) The repo is public d) Someone else can download and run your project with the documented steps

9. What should `.env.example` contain?
   a) Nothing b) The names of needed variables with placeholder values c) Your password hint d) Real secrets

10. Best use of an AI assistant while learning?
    a) Generate the whole project b) Copy without testing c) Never use them d) Explain errors and give hints, then you write the code

**Short answer.**

11. Describe the build loop in your own words.
12. List 5 things a good README contains.
13. Why are friendly error messages better than raw tracebacks for users?
14. Pick one of your projects and write its must-have and nice-to-have lists.
15. What would an interviewer likely ask about Project C, and how would you answer?

### Answers

| Q | A | Q | A |
|---|---|---|---|
| 1 | d | 6 | a |
| 2 | a | 7 | b |
| 3 | b | 8 | d |
| 4 | c | 9 | b |
| 5 | c | 10 | d |

**11.** Choose the next smallest requirement → write a little code → run it → fix errors → add a test if useful → commit → repeat.

**12.** Any five of: title + one-liner, screenshot/output, features, install & run commands, how it works, what I learned/challenges, next steps, limitations.

**13.** Users aren't programmers and don't know what a traceback means. A message saying what went wrong and how to fix it ("File not found, check --file") gets them unstuck without reading code.

**14.** (Your own answer. Check that must-haves are few and testable.)

**15.** "Why that metric?", "How did you avoid leakage?", "What's your baseline?", "Did it overfit?", "What are its limitations/bias?" Answer with your problem statement, pipeline explanation, CV table, train vs test numbers, and README limitations section.

**Scoring:** 10 MCQ + 5 short × 2 = 20. ≥ 16 move on.

➡️ Now take `../Month1_Final_Test.md`.
