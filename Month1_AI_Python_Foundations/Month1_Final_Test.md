# Month 1 Final Test: AI + Python Foundations

> **🛠️ Setup for Part 2:** you need uv, Python 3.14, Git + GitHub, and one project with numpy, pandas, matplotlib, scikit-learn, pydantic, requests, pytest. Create the project before the timer starts:
>
> ```bash
> uv init month1-final && cd month1-final
> uv add numpy pandas matplotlib scikit-learn joblib requests pydantic
> uv add --dev pytest ruff
> ```
>
> Help: [`00_SETUP_Install_Guide.md`](../00_SETUP_Install_Guide.md).

**Covers:** Lessons 01–05. **Time:** 2 hours (Part 1: 40 min, Part 2: 80 min). Closed book for Part 1; open docs (but no AI assistant) for Part 2.

**Pass mark:** 75% overall. Below that, revisit the lessons tied to the questions you missed (the lesson number is shown in brackets).

---

## Part 1: Theory (40 points)

### Section A: Multiple choice (20 × 1 point)

1. [01] What does `print(type(3 / 1))` show?
   a) int b) error c) str d) float

2. [01] Which creates a dictionary?
   a) `{1, 2}` b) `(1, 2)` c) `{"a": 1}` d) `[1, 2]`

3. [01] What is printed?
   ```python
   def f(x, y=2): return x ** y
   print(f(3), f(2, 3))
   ```
   a) `9 8` b) `9 6` c) `6 6` d) `8 9`

4. [01] Which error does `[1, 2, 3][5]` raise?
   a) TypeError b) IndexError c) ValueError d) KeyError

5. [01] Why use a virtual environment?
   a) Faster Python b) Hides code c) Keep each project's packages separate d) Required for loops

6. [02] `np.array([[1, 2], [3, 4]]).sum(axis=0)` is:
   a) `10` b) `[3 7]` c) `[1 2 3 4]` d) `[4 6]`

7. [02] Which correctly filters rows where `age > 30` AND `city == "Pune"`?
   a) `df[df["age"] > 30][df["city"] == "Pune"] = True` b) `df[(df["age"] > 30) & (df["city"] == "Pune")]` c) `df.filter(age>30, city="Pune")` d) `df[df.age > 30 and df.city == "Pune"]`

8. [02] In pandas 3.0, which line changes the original DataFrame?
   a) `df.loc[df["x"] > 0, "y"] = 1` b) `df.head()["y"] = 1` c) `df.query("x > 0").y = 1` d) `df[df.x > 0]["y"] = 1`

9. [02] "Split–apply–combine" describes:
   a) read_csv b) merge c) groupby d) concat

10. [02] `pd.to_numeric(s, errors="coerce")` does what with "abc"?
    a) Returns NaN b) Returns 0 c) Raises d) Keeps "abc"

11. [03] Status code 404 means:
    a) Success b) Not found c) Rate limited d) Unauthorized

12. [03] Which HTTP method sends data to create something?
    a) GET b) DELETE c) OPTIONS d) POST

13. [03] JSON `true` becomes in Python:
    a) `1` b) `"true"` c) `True` d) `None`

14. [03] Correct order:
    a) `git init` → `git push` → `git add` b) `git push` → `git commit` c) `git commit` → `git add` → `git push` d) `git add` → `git commit` → `git push`

15. [03] Your API key was pushed to a public repo. First thing to do?
    a) Revoke/rotate the key b) Nothing c) Make a new commit removing it d) Delete the repo

16. [04] Predicting whether an email is spam is:
    a) Clustering b) Binary classification c) Regression d) Reinforcement learning

17. [04] Train accuracy 98%, test accuracy 70%:
    a) Overfitting b) Data is perfect c) Underfitting d) Need a larger learning rate

18. [04] Precision is:
    a) (TP + TN) / all b) TP / (TP + FP) c) FP / all d) TP / (TP + FN)

19. [04] Which avoids data leakage?
    a) Use the test set to choose features b) Scale all data, then split c) Train on the test set d) Split, then fit preprocessing only on training data

20. [05] The best first version of a project is:
    a) Only the README b) Feature-complete c) An MVP that works end to end d) Only tests

### Section B: Short answers (10 × 2 points)

21. [01] Explain the difference between a parameter and an argument.
22. [01] What does `if __name__ == "__main__":` do?
23. [02] Name four problems you might fix during data cleaning, and one Pandas method for each.
24. [02] What's the difference between an `inner` and a `left` merge?
25. [03] What are headers in an HTTP request? Give two examples.
26. [03] Why should you set a `timeout` and use retries with exponential backoff?
27. [03] What goes in `.gitignore`, and why?
28. [04] Explain gradient descent using an analogy.
29. [04] Why can 99% accuracy be a bad model? What should you report instead?
30. [05] What makes a README good? List at least five elements.

---

## Part 2: Practical (60 points)

Create a new repo `month1-final` and do all tasks there. Commit after each task.

### Task 1: Python (10 points) [01]

Write `text_stats.py` with a function `analyse(text: str) -> dict` returning:
- `words`: number of words
- `unique_words`: number of unique words (lowercase, punctuation `.,!?;:` removed)
- `top_3`: list of the 3 most common words as `(word, count)` tuples
- `longest`: the longest word

Plus `main()` that reads a file path from `input()`, handles `FileNotFoundError` nicely, and prints the stats. Include docstrings and type hints.

### Task 2: Pandas (15 points) [02]

Create `sales.csv`:

```
order_id,date,region,product,units,unit_price
1,2026-07-01,North,Laptop,2,800
2,2026-07-03,south,Phone,5,300
3,2026-07-03,South ,Phone,5,300
4,2026-07-15,East,Tablet,,450
5,2026-08-02,North,Phone,3,300
6,2026-08-10,West,Laptop,1,
7,2026-08-21,East,Laptop,4,780
8,2026-09-05,West,Tablet,2,450
9,2026-09-09,North,Laptop,1,820
9,2026-09-09,North,Laptop,1,820
```

In `sales_analysis.py`:
1. Clean: fix region text, remove exact duplicates (note: rows 2 and 3 differ only by region text; after fixing text they become duplicates, so do text cleaning **before** dropping duplicates), fill missing `units` with the product's median units, fill missing `unit_price` with the product's median price.
2. Add `revenue`.
3. Print: revenue by region (sorted), revenue by month, best-selling product by units.
4. Save a bar chart `revenue_by_region.png` and `sales_clean.csv`.

### Task 3: API + JSON + Pydantic (15 points) [03]

`countries.py`:
1. Fetch data for these countries from `https://restcountries.com/v3.1/name/{name}`: India, Japan, Brazil, Kenya, Germany.
2. Validate with a Pydantic model: `name` (common name), `capital` (first capital), `population`, `region`, `area`.
3. Handle failures: timeout, retry on 5xx, skip on 404 with a warning.
4. Save as `countries.json`, load into Pandas, add `density = population / area`, print sorted by density.

### Task 4: ML (15 points) [04]

`model.py` using `sklearn.datasets.load_wine` (3-class classification):
1. Split 80/20 with stratify.
2. Compute a baseline (most common class) accuracy.
3. Build pipelines for logistic regression (with scaling) and random forest; compare with 5-fold CV on training data.
4. Evaluate the best one on the test set: accuracy + classification report + confusion matrix.
5. Print train vs test accuracy and state in a comment whether it overfits.
6. Save the model with joblib.

### Task 5: Project hygiene (5 points) [05]

- README with what each script does and how to run it
- `.gitignore`
- At least 2 pytest tests for `analyse()` from Task 1
- ≥ 6 meaningful commits; pushed to GitHub

---

## Answer Key

### Section A

| Q | A | Q | A | Q | A | Q | A |
|---|---|---|---|---|---|---|---|
| 1 | d | 6 | d | 11 | b | 16 | b |
| 2 | c | 7 | b | 12 | d | 17 | a |
| 3 | a | 8 | a | 13 | c | 18 | b |
| 4 | b | 9 | c | 14 | d | 19 | d |
| 5 | c | 10 | a | 15 | a | 20 | c |

### Section B (model answers)

21. A parameter is the placeholder name in the function definition (`def f(x)` → `x`); an argument is the actual value passed when calling (`f(5)` → `5`).
22. Runs the code inside only when the file is executed directly, not when it's imported, so functions can be reused without side effects.
23. Duplicates → `drop_duplicates()`; missing values → `fillna()`/`dropna()`; wrong types → `pd.to_numeric()`/`pd.to_datetime()`; messy text → `.str.strip().str.title()`; outliers → boolean filtering.
24. Inner keeps only rows whose key exists in both tables; left keeps all rows of the left table and fills NaN where the right has no match.
25. Extra labelled information sent with the request, e.g. `Authorization: Bearer <key>`, `Content-Type: application/json`.
26. Networks and servers fail or get overloaded; a timeout stops your program hanging forever, and backoff retries recover from temporary errors (429/5xx) without hammering the server.
27. Files that must not be tracked: secrets (`.env`), environments (`.venv/`), caches (`__pycache__/`), large/raw data. They're secret, rebuildable, or too big.
28. Like walking downhill in fog: feel the slope (gradient) and take a small step (learning rate) downward, repeating until you reach the valley (lowest loss).
29. With imbalanced classes, always predicting the majority class gives high accuracy but catches nothing. Report precision, recall, F1, the confusion matrix and a baseline.
30. Title + one-liner, screenshot/example output, features, install/run commands, how it works, what I learned, next steps/limitations.

### Part 2 reference solutions

```python
# Task 1 - text_stats.py
from collections import Counter

PUNCT = ".,!?;:"

def analyse(text: str) -> dict:
    """Return word statistics for a block of text."""
    cleaned = text.lower()
    for p in PUNCT:
        cleaned = cleaned.replace(p, "")
    words = cleaned.split()
    if not words:
        return {"words": 0, "unique_words": 0, "top_3": [], "longest": ""}
    return {
        "words": len(words),
        "unique_words": len(set(words)),
        "top_3": Counter(words).most_common(3),
        "longest": max(words, key=len),
    }

def main() -> None:
    path = input("File path: ")
    try:
        with open(path) as f:
            print(analyse(f.read()))
    except FileNotFoundError:
        print(f"Couldn't find {path}")

if __name__ == "__main__":
    main()
```

(`Counter` from the standard library counts items; `.most_common(3)` gives the top 3. A dict-based count is equally fine.)

```python
# Task 2 - sales_analysis.py
import pandas as pd, matplotlib.pyplot as plt

df = pd.read_csv("sales.csv")
df["region"] = df["region"].str.strip().str.title()
df = df.drop_duplicates(subset=[c for c in df.columns if c != "order_id"])
# rows 2/3 and the two order 9 rows collapse → 8 rows remain
df["units"] = df["units"].fillna(df.groupby("product")["units"].transform("median"))
df["unit_price"] = df["unit_price"].fillna(df.groupby("product")["unit_price"].transform("median"))
df["date"] = pd.to_datetime(df["date"])
df["revenue"] = df["units"] * df["unit_price"]

by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
print(by_region)
print(df.groupby(df["date"].dt.to_period("M"))["revenue"].sum())
print(df.groupby("product")["units"].sum().idxmax())

by_region.plot(kind="bar"); plt.tight_layout(); plt.savefig("revenue_by_region.png")
df.to_csv("sales_clean.csv", index=False)
```

> Note: rows 2 and 3 have different `order_id`s, so whether they're "true duplicates" is a judgement call. Ignoring `order_id` when de-duplicating (as above) or keeping both are both acceptable **if you explain your choice in a comment**. Reasoning about data is the skill being tested.

```python
# Task 3 - countries.py
import json, time, logging, requests
import pandas as pd
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

class Country(BaseModel):
    name: str
    capital: str | None
    population: int
    region: str
    area: float

def fetch(name: str, tries: int = 3) -> dict | None:
    for attempt in range(tries):
        try:
            r = requests.get(f"https://restcountries.com/v3.1/name/{name}", timeout=10)
            if r.status_code == 404:
                logging.warning("Not found: %s", name); return None
            if r.status_code >= 500:
                raise requests.HTTPError(str(r.status_code))
            r.raise_for_status()
            return r.json()[0]
        except (requests.Timeout, requests.ConnectionError, requests.HTTPError):
            if attempt == tries - 1:
                logging.warning("Giving up on %s", name); return None
            time.sleep(2 ** attempt)

rows = []
for n in ["India", "Japan", "Brazil", "Kenya", "Germany"]:
    raw = fetch(n)
    if raw:
        rows.append(Country(name=raw["name"]["common"], capital=(raw.get("capital") or [None])[0],
                            population=raw["population"], region=raw["region"], area=raw["area"]))

with open("countries.json", "w") as f:
    json.dump([c.model_dump() for c in rows], f, indent=2)
df = pd.read_json("countries.json")
df["density"] = df["population"] / df["area"]
print(df.sort_values("density", ascending=False))
```

```python
# Task 4 - model.py
import numpy as np, joblib
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

X, y = load_wine(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("baseline:", (y_te == np.bincount(y_tr).argmax()).mean())    # ~0.40

models = {"logreg": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
          "forest": make_pipeline(RandomForestClassifier(random_state=42))}
cv = {n: cross_val_score(m, X_tr, y_tr, cv=5).mean() for n, m in models.items()}
print(cv)
best = models[max(cv, key=cv.get)].fit(X_tr, y_tr)
pred = best.predict(X_te)
print(accuracy_score(y_te, pred)); print(classification_report(y_te, pred)); print(confusion_matrix(y_te, pred))
print("train", best.score(X_tr, y_tr), "test", best.score(X_te, y_te))
# Both ~0.97-1.0 and close together → no meaningful overfitting.
joblib.dump(best, "wine_model.joblib")
```

```python
# Task 5 - tests/test_text_stats.py
from text_stats import analyse

def test_counts_words_and_unique():
    r = analyse("The cat. The dog!")
    assert r["words"] == 4 and r["unique_words"] == 3

def test_empty_text():
    assert analyse("")["words"] == 0
```

### Scoring

| Part | Points |
|---|---|
| Section A | 20 |
| Section B | 20 |
| Task 1 | 10 |
| Task 2 | 15 |
| Task 3 | 15 |
| Task 4 | 15 |
| Task 5 | 5 |
| **Total** | **100** → pass at **75** |

🎉 Passed? Start **Month 2: `../Month2_LLMs_Generative_AI/06_LLM_Fundamentals/lesson.md`**.
