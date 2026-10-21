# Practice & Test 02: NumPy, Pandas & Data Handling

> **🛠️ Before you start:** you need numpy, pandas 3.x, matplotlib (+ ipykernel for notebooks). Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run python -c "import pandas; print(pandas.__version__)"   # 3.x
> ```

**Setup:**

```bash
uv init data_practice && cd data_practice
uv add numpy pandas matplotlib
```

Create this file as `students.csv` for the exercises:

```
id,name,gender,city,math,science,english,joined
1,Asha,F,Pune,88,92,79,2025-06-01
2,ravi ,M,delhi,65,,58,2025-07-15
3,Meera,F,Pune,95,98,100,2025-06-20
4,John,M,Mumbai,72,68,,2025-08-03
5,Asha,F,Pune,88,92,79,2025-06-01
6,Kiran,M,Delhi,abc,75,81,2025-09-10
7,Zara,F,Mumbai,55,61,70,2025-09-28
8,Leo,M,pune,91,85,88,2025-10-05
```

---

## Part A: NumPy warm-ups (predict, then run)

```python
import numpy as np
a = np.array([2, 4, 6, 8])
m = np.array([[1, 2, 3], [4, 5, 6]])

# A1
print(a + 1)
# A2
print(a[a > 4])
# A3
print(m.shape, m.ndim)
# A4
print(m[:, 1])
# A5
print(m.sum(axis=0), m.sum(axis=1))
# A6
print(np.dot(np.array([1, 0, 2]), np.array([3, 5, 1])))
# A7
print(np.arange(0, 1, 0.25))
# A8
print(m * np.array([10, 100, 1000]))
```

## Part B: NumPy exercises

**B1.** Create a 5×5 array of random integers 1–100 with seed 0 (`np.random.default_rng(0).integers(1, 101, size=(5, 5))`). Print its max, min, mean, and the mean of each column.

**B2.** Normalise an array: transform `x = np.array([10, 20, 30, 40, 50])` so the smallest becomes 0 and largest becomes 1, using `(x - x.min()) / (x.max() - x.min())`. (This is called **min-max scaling**; you'll use it in Lesson 04.)

**B3.** Write `cosine_similarity(a, b)` = `dot(a, b) / (norm(a) * norm(b))` where `norm` is `np.linalg.norm`. Test: `[1, 2, 3]` vs `[2, 4, 6]` (should be 1.0) and `[1, 0]` vs `[0, 1]` (should be 0.0). *You will reuse this exact function in Lesson 09 on embeddings.*

**B4.** Time it: compare summing 10 million numbers using a Python loop vs `np.sum`. Use `import time; t = time.perf_counter()`.

## Part C: Pandas exercises (use `students.csv`)

**C1. Inspect.** Load the file and run the five-step inspection ritual. List every data problem you can find.

**C2. Clean.**
- Remove exact duplicates.
- Fix `name` and `city` whitespace/capitalisation.
- Convert `math` to numbers (bad values → NaN).
- Convert `joined` to datetime.
- Fill missing subject scores with that subject's median.

**C3. Features.** Add `average` (mean of the three subjects, use `df[["math","science","english"]].mean(axis=1)`) and `grade` (A ≥ 90, B ≥ 75, C ≥ 60, else F). Hint: `pd.cut(df["average"], bins=[0, 60, 75, 90, 101], labels=["F", "C", "B", "A"], right=False)`.

**C4. Questions.**
1. Average score per city?
2. How many students per gender?
3. Who is the top student in each city? (Hint: `df.loc[df.groupby("city")["average"].idxmax()]`)
4. How many students joined each month?

**C5. Merge.** Create `clubs = pd.DataFrame({"id": [1, 3, 4, 9], "club": ["Robotics", "Chess", "Music", "Art"]})`. Do a left merge and an inner merge with the students. Explain the different row counts.

**C6. Chart & save.** Make a bar chart of average score per city, save to `city_scores.png`, and save the clean data to `students_clean.csv` without the index.

**C7. Copy-on-Write check.** Run this and explain why `df` doesn't change. Then fix it:

```python
df[df["city"] == "Pune"]["math"] = 100
```

---

## Part D: Mini-project: explore a real dataset (60–90 min)

Pick one free public dataset (search "Titanic CSV", "Kaggle Netflix titles CSV", or download any CSV from data.gov / data.gov.in). In a Jupyter notebook:

1. Load and inspect it. Write 3 bullet points describing the data.
2. Clean at least 3 kinds of problems. Write down *why* you chose each fix.
3. Answer 3 questions using `groupby`.
4. Make 2 charts.
5. Write a 5-sentence "findings" summary at the top of the notebook.

Save it. In Lesson 03 you'll put it on GitHub.

---

## Part E: Quiz (25 minutes, lesson closed)

1. What is the main advantage of NumPy arrays over Python lists for maths?
   a) They are easier to print b) They can be any length c) They hold mixed types d) Vectorised operations are much faster

2. `np.array([[1,2],[3,4],[5,6]]).shape` is:
   a) (2, 3) b) 6 c) (3, 2) d) (6,)

3. What does `arr[arr > 0]` do?
   a) Sets negative values to 0 b) Returns only the positive elements c) Counts positives d) Errors

4. A random seed is used to:
   a) Make results repeatable b) Remove randomness completely forever c) Make code faster d) Encrypt data

5. The dot product of `[1, 2]` and `[3, 4]` is:
   a) 11 b) 7 c) [3, 8] d) 10

6. In Pandas, a single column is a:
   a) DataFrame b) Array c) Index d) Series

7. Which shows column types and non-missing counts?
   a) `df.describe()` b) `df.info()` c) `df.head()` d) `df.shape`

8. Which correctly sets `bonus` to 10 for rows where `sales > 100` in pandas 3.0?
   a) `df[df.sales > 100]["bonus"] = 10` b) `df.bonus[df.sales > 100] == 10` c) `df.loc[df["sales"] > 100, "bonus"] = 10` d) `df.set(bonus=10)`

9. How do you combine two filter conditions?
   a) `,` b) `and` c) `+` d) `&` with brackets around each

10. `pd.to_numeric(col, errors="coerce")` turns unconvertible values into:
    a) Empty strings b) An error c) NaN d) 0

11. Why is median sometimes better than mean for filling gaps?
    a) It isn't pulled by extreme values b) It's always bigger c) It's faster d) Pandas requires it

12. `df.groupby("city")["sales"].sum()` follows which pattern?
    a) filter–drop–fill b) split–apply–combine c) load–clean–save d) map-reduce-sort

13. A `how="inner"` merge keeps:
    a) all left rows b) only rows matching in both c) all rows from both d) only unmatched rows

14. In pandas 3.0, text columns default to which dtype?
    a) category b) object c) str d) char

15. Why write `df.to_csv("x.csv", index=False)`?
    a) Avoids saving row numbers as an extra column b) Faster c) Required for Excel d) Compresses the file

**Short answer.**

16. Explain vectorisation using an everyday analogy.
17. You load a file and `price` shows as `str` dtype. What are two possible causes and how do you fix it?
18. Describe the six-stage data pipeline from the lesson.
19. When would you drop rows with missing values, and when would you fill them?
20. What's the difference between `.loc` and `.iloc`?

---

## Answer Key

### Part A

| # | Output |
|---|---|
| A1 | `[3 5 7 9]` |
| A2 | `[6 8]` |
| A3 | `(2, 3) 2` |
| A4 | `[2 5]` |
| A5 | `[5 7 9] [ 6 15]` |
| A6 | `5` (1·3 + 0·5 + 2·1) |
| A7 | `[0.   0.25 0.5  0.75]` |
| A8 | `[[  10  200 3000] [  40  500 6000]]` |

### Part B

```python
import numpy as np, time

# B1
r = np.random.default_rng(0).integers(1, 101, size=(5, 5))
print(r.max(), r.min(), r.mean(), r.mean(axis=0))

# B2
x = np.array([10, 20, 30, 40, 50])
print((x - x.min()) / (x.max() - x.min()))   # [0.   0.25 0.5  0.75 1.  ]

# B3
def cosine_similarity(a, b) -> float:
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

print(cosine_similarity([1, 2, 3], [2, 4, 6]))   # 1.0 (same direction)
print(cosine_similarity([1, 0], [0, 1]))         # 0.0 (unrelated)

# B4
nums = np.arange(10_000_000)
t = time.perf_counter(); s = 0
for n in nums.tolist(): s += n
print("loop:", time.perf_counter() - t)
t = time.perf_counter(); np.sum(nums)
print("numpy:", time.perf_counter() - t)    # typically 50-100x faster
```

### Part C

```python
import pandas as pd
import matplotlib.pyplot as plt

# C1
df = pd.read_csv("students.csv")
df.head(); df.shape; df.info(); df.describe(); df.isna().sum()
# Problems: duplicate row (id 5 = Asha again, but different id! see note),
# "ravi " whitespace/lowercase, "delhi"/"pune" lowercase, "abc" in math (so math is str),
# missing science (Ravi) and english (John), joined is text.
```

> **Note on C1:** Row 5 has the same data as row 1 but a different `id`, so `drop_duplicates()` will **not** remove it. Real cleaning needs judgement: use `df.drop_duplicates(subset=["name", "gender", "city", "math", "science", "english", "joined"])`. Spotting this is part of the test.

```python
# C2
subset = [c for c in df.columns if c != "id"]
df = df.drop_duplicates(subset=subset)
df["name"] = df["name"].str.strip().str.title()
df["city"] = df["city"].str.strip().str.title()
df["math"] = pd.to_numeric(df["math"], errors="coerce")
df["joined"] = pd.to_datetime(df["joined"])
for col in ["math", "science", "english"]:
    df[col] = df[col].fillna(df[col].median())

# C3
df["average"] = df[["math", "science", "english"]].mean(axis=1)
df["grade"] = pd.cut(df["average"], bins=[0, 60, 75, 90, 101],
                     labels=["F", "C", "B", "A"], right=False)

# C4
print(df.groupby("city")["average"].mean())
print(df["gender"].value_counts())
print(df.loc[df.groupby("city")["average"].idxmax(), ["city", "name", "average"]])
print(df.groupby(df["joined"].dt.to_period("M")).size())

# C5
clubs = pd.DataFrame({"id": [1, 3, 4, 9], "club": ["Robotics", "Chess", "Music", "Art"]})
left = df.merge(clubs, on="id", how="left")     # 7 rows: all students, club NaN if none
inner = df.merge(clubs, on="id", how="inner")   # 3 rows: only ids 1, 3, 4
# id 9 has no student, so it appears in neither.

# C6
df.groupby("city")["average"].mean().plot(kind="bar", title="Average by city")
plt.tight_layout(); plt.savefig("city_scores.png")
df.to_csv("students_clean.csv", index=False)

# C7
# df[df["city"] == "Pune"] creates a NEW (copied) DataFrame; setting ["math"] on it
# changes only that temporary copy, which is thrown away. Fix:
df.loc[df["city"] == "Pune", "math"] = 100
```

### Part E: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | d | 6 | d | 11 | a |
| 2 | c | 7 | b | 12 | b |
| 3 | b | 8 | c | 13 | b |
| 4 | a | 9 | d | 14 | c |
| 5 | a | 10 | c | 15 | a |

**16.** Like a stamp that prints on every envelope in a stack at once instead of writing the address on each envelope by hand. The operation is applied to the whole array in one go by fast code underneath.

**17.** Some values are non-numeric text (e.g. "abc", "$12", "1,200") or the file uses odd formatting. Inspect with `df["price"].unique()`, clean symbols with `.str.replace(...)`, then `pd.to_numeric(..., errors="coerce")`.

**18.** Load → inspect → clean → transform (create new columns) → analyse (group/chart) → save.

**19.** Drop when only a few rows are affected and they're not important, or when the missing value is essential (e.g. the target you want to predict). Fill when many rows are affected or the row's other data is valuable, using a sensible value (median, mode, "Unknown").

**20.** `.loc` selects by labels (index names and column names, and boolean masks); `.iloc` selects by integer position (0, 1, 2…), like list indexing.

**Scoring:** out of 25 (15 + 5×2). ≥ 21 move on.
