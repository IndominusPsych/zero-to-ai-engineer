# Lesson 02: NumPy, Pandas & Data Handling

*Month 1, Week 2. Reading time: about 60–75 minutes. Assumes Lesson 01.*

---

## 🛠️ Setup for this lesson

| You need | Why | How to get it |
|---|---|---|
| Everything from Lesson 01 | VS Code, uv, Python 3.14 | Setup Guide Steps 1–4 |
| **numpy**, **pandas 3.x**, **matplotlib** | Fast arrays, tables, charts | `uv add` (below) |
| *Jupyter* VS Code extension + `ipykernel` | Notebooks: run code in cells and see tables/charts inline | Setup Guide Step 5 |

**Install:**

```bash
cd ~/ai-engineer-projects
uv init data_practice && cd data_practice
uv add numpy pandas matplotlib
uv add --dev ipykernel        # lets VS Code run notebooks with this project's packages
```

**Check it works:**

```bash
uv run python -c "import numpy, pandas, matplotlib; print('numpy', numpy.__version__, '| pandas', pandas.__version__)"
# pandas must start with 3. If it shows 2.x, run: uv add "pandas>=3"
```

In VS Code, create `explore.ipynb`, click **Select Kernel** → **Python Environments** → pick the `.venv` inside `data_practice`.

Stuck? See the step-by-step instructions and the troubleshooting table in [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md).

---

## 1. The big picture

### What is this, in simple words?

In Lesson 01 you added up four expenses with a loop. Now imagine four **million** expenses. A Python loop would be slow and the code would get messy. **NumPy** and **Pandas** are two Python packages that handle large amounts of data quickly and with very little code.

- **NumPy** ("Numerical Python") is for **fast maths on big grids of numbers**.
- **Pandas** is for **tables**: rows and columns, like a spreadsheet, but controlled by code.

Analogy: Python lists are like doing sums on paper. NumPy is a calculator that does a million sums at once. Pandas is Excel that you drive with commands instead of a mouse, and that never gets tired.

### Which field does it belong to?

These tools belong to **data science** and **data analysis**: the work of collecting, cleaning, exploring and understanding data. They're also the foundation of **machine learning** (Lesson 04), because machine learning *is* learning patterns from data.

### Why does it matter?

There's a saying: **"AI is 80% data work."** Before any model can learn, someone has to load the data, fix mistakes, fill gaps, and reshape it. Even in Month 2 when you work with large language models, you'll be loading documents, cleaning text and tracking results in tables.

| Without these tools | With them |
|---|---|
| Loops over every row | One line operates on a whole column |
| Slow for big data | Very fast (written in C underneath) |
| You write your own CSV reader | `pd.read_csv("file.csv")` |
| Hard to spot patterns | Group, sort, filter, chart in seconds |

> **In simple words:** NumPy does fast maths on lots of numbers; Pandas handles tables. Together they're the toolkit for preparing data, which is most of the work in AI.

---

## 2. Core concepts

### 2.1 Installing and importing

```bash
uv add numpy pandas matplotlib
```

```python
import numpy as np
import pandas as pd
```

`as np` gives the package a short nickname. Everyone in the world uses `np` and `pd`, so stick with them.

**Matplotlib** is a package for drawing charts. You'll use it a little at the end.

**Jupyter notebooks** are worth knowing about now. A notebook is a document where you write code in small boxes called **cells**, run each one, and see results (tables, charts) right underneath. Data people love them for exploring. VS Code opens `.ipynb` notebook files directly. Install with `uv add --dev ipykernel`.

### 2.2 NumPy arrays

The central NumPy idea is the **array**: a grid of numbers, all of the same type.

```python
a = np.array([1, 2, 3, 4])
print(a * 10)          # [10 20 30 40]
```

Notice: no loop! The multiplication applied to **every element at once**. This is called **vectorisation**: doing an operation on a whole array instead of one item at a time. Compare:

```python
# Plain Python list
nums = [1, 2, 3, 4]
result = [n * 10 for n in nums]

# NumPy
result = np.array(nums) * 10
```

For 10 million numbers, the NumPy version is typically 50–100× faster.

**Dimensions and shape.** Arrays can have more than one direction:

| Name | Dimensions | Picture | Example |
|---|---|---|---|
| Vector (1-D) | 1 | a row | `[1, 2, 3]` |
| Matrix (2-D) | 2 | a table/grid | `[[1, 2], [3, 4]]` |
| Tensor (3-D+) | 3 or more | a stack of grids | a colour photo: height × width × 3 colours |

The **shape** tells you the size in each direction:

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])
print(m.shape)      # (2, 3) → 2 rows, 3 columns
print(m.ndim)       # 2 dimensions
print(m.dtype)      # int64 → the type of every element
```

These words matter: in Month 2, an "embedding" is just a vector (a 1-D array) of numbers, and AI models are giant collections of matrices.

**Creating arrays quickly:**

```python
np.zeros(5)              # [0. 0. 0. 0. 0.]
np.ones((2, 3))          # 2×3 grid of 1s
np.arange(0, 10, 2)      # [0 2 4 6 8]  (like range)
np.linspace(0, 1, 5)     # 5 evenly spaced numbers from 0 to 1
np.random.default_rng(42).random(3)   # 3 random numbers (42 = "seed", makes it repeatable)
```

A **random seed** is a starting number for the random generator. Same seed → same "random" numbers every time. This makes experiments repeatable, which matters a lot in ML.

**Indexing and slicing** work like lists, with a comma between dimensions:

```python
m[0, 1]     # row 0, column 1 → 2
m[:, 0]     # all rows, column 0 → [1 4]
m[1]        # row 1 → [4 5 6]
```

**Boolean masks: filtering by condition.** Ask a question of every element; you get a True/False array, which you can use to pick items:

```python
scores = np.array([45, 82, 67, 91, 38])
passed = scores >= 50        # [False True True True False]
print(scores[passed])        # [82 67 91]
```

**Aggregations** summarise many numbers into one:

```python
scores.mean()   # average: 64.6
scores.max()    # 91
scores.sum()
scores.std()    # standard deviation: how spread out the values are
```

With 2-D arrays, `axis` says which direction to summarise: `axis=0` goes down columns, `axis=1` goes across rows.

**Broadcasting** lets NumPy combine arrays of different shapes sensibly:

```python
prices = np.array([[10, 20], [30, 40]])
prices * np.array([1, 0.5])      # multiplies column 1 by 1 and column 2 by 0.5
```

Analogy: one small stencil stretched across a bigger wall.

**Dot product** (you'll need this in Month 2): multiply matching elements and add them up.

```python
a = np.array([1, 2, 3]); b = np.array([4, 5, 6])
np.dot(a, b)     # 1*4 + 2*5 + 3*6 = 32
```

The dot product is how AI measures how similar two embeddings are. Keep it in mind.

### 2.3 Pandas: Series and DataFrames

Pandas has two main objects:

- A **Series**: one column of data with labels.
- A **DataFrame**: a whole table made of Series side by side. **This is the one you'll use 95% of the time.** Everyone calls it `df`.

```python
df = pd.DataFrame({
    "name":  ["Asha", "Ravi", "Meera", "John"],
    "age":   [21, 25, 23, 30],
    "city":  ["Pune", "Delhi", "Pune", "Mumbai"],
    "score": [88, 65, 95, None],
})
print(df)
```

```
    name  age    city  score
0   Asha   21    Pune   88.0
1   Ravi   25   Delhi   65.0
2  Meera   23    Pune   95.0
3   John   30  Mumbai    NaN
```

The numbers on the left (0, 1, 2, 3) are the **index**: the row labels. `NaN` ("Not a Number") is how Pandas shows a **missing value**.

```
          columns ─────────────────────▶
        ┌────────┬──────┬────────┬───────┐
 index  │  name  │ age  │  city  │ score │
   │  0 │  Asha  │  21  │  Pune  │  88.0 │ ◀── a row
   │  1 │  Ravi  │  25  │ Delhi  │  65.0 │
   ▼  2 │ Meera  │  23  │  Pune  │  95.0 │
      3 │  John  │  30  │ Mumbai │  NaN  │
        └────────┴──────┴────────┴───────┘
                    ▲ each column is a Series
```

### 2.4 Loading and looking at data

Usually you load a file instead of typing data:

```python
df = pd.read_csv("sales.csv")       # also: read_excel, read_json, read_parquet
```

First things to do with *any* new dataset (memorise this ritual):

```python
df.head()        # first 5 rows
df.shape         # (rows, columns)
df.info()        # columns, types, how many non-missing values
df.describe()    # stats: mean, min, max, etc. for number columns
df.columns       # list of column names
df["city"].value_counts()   # how often each value appears
```

### 2.5 Data types in Pandas (and what changed in pandas 3.0)

Each column has a **dtype** (data type): `int64`, `float64`, `bool`, `datetime64`, and for text, `str`.

**Recent change:** pandas **3.0** came out in January 2026. Two changes matter for beginners:

1. **Text columns now get a proper `str` dtype.** Older tutorials show text columns as `object`. If a tutorial checks `dtype == object`, that check may now fail.
2. **Copy-on-Write is always on.** Any time you pick out part of a table, Pandas treats it as a separate copy. This removes a famous confusing warning (`SettingWithCopyWarning`), but it means one old style no longer works (shown in 2.7).

### 2.6 Selecting data

```python
df["name"]                 # one column → Series
df[["name", "score"]]      # several columns → DataFrame (note double brackets)
df[df["age"] > 22]         # rows where age > 22 (a boolean mask, like NumPy!)
df[(df["city"] == "Pune") & (df["score"] > 90)]   # combine with & (and), | (or)
```

Use `&` and `|` (not `and`/`or`) and wrap each condition in brackets.

**`.loc` and `.iloc`** are precise selectors:

| Selector | Selects by | Example |
|---|---|---|
| `.loc[rows, cols]` | **labels** (names) | `df.loc[df["age"] > 22, "name"]` |
| `.iloc[rows, cols]` | **positions** (numbers) | `df.iloc[0:2, 0:2]` (first 2 rows, first 2 columns) |

### 2.7 Changing data

**Add or change a column:**

```python
df["age_next_year"] = df["age"] + 1          # vectorised, like NumPy
df["passed"] = df["score"] >= 70
```

**Change only some rows (do it in one step with `.loc`):**

```python
df.loc[df["city"] == "Pune", "region"] = "West"     # ✅ correct
```

```python
df[df["city"] == "Pune"]["region"] = "West"        # ❌ "chained assignment" - does nothing in pandas 3.0
```

The second line picks a copy of some rows, then changes the copy, which is thrown away. Pandas 3.0 makes this rule strict. Always use a single `.loc[...] = ...`.

**Apply your own function** to each value:

```python
df["name_upper"] = df["name"].apply(lambda n: n.upper())
# or better, built-in string methods:
df["name_upper"] = df["name"].str.upper()
```

A **lambda** is a tiny one-line function without a name: `lambda n: n.upper()` means "given n, return n.upper()".

**Rename, drop, sort:**

```python
df = df.rename(columns={"score": "exam_score"})
df = df.drop(columns=["name_upper"])
df = df.sort_values("age", ascending=False)
```

Most Pandas methods **return a new DataFrame** rather than changing the old one, so you write `df = df.something()`.

### 2.8 Cleaning data

Real data is messy. **Data cleaning** means fixing it before use. The common problems:

| Problem | Detect | Fix |
|---|---|---|
| Missing values | `df.isna().sum()` | `df.dropna()` (remove rows) or `df["score"].fillna(df["score"].mean())` (fill) |
| Duplicates | `df.duplicated().sum()` | `df.drop_duplicates()` |
| Wrong type (numbers stored as text) | `df.info()` | `pd.to_numeric(df["price"], errors="coerce")` |
| Messy text (" pune", "PUNE") | `df["city"].unique()` | `df["city"].str.strip().str.title()` |
| Dates as text | `df.info()` | `pd.to_datetime(df["date"])` |
| Outliers (crazy values like age 999) | `df.describe()`, charts | Filter them out or cap them |

`errors="coerce"` means "if something can't be converted, make it missing (NaN) instead of crashing."

### 2.9 Grouping and summarising

The single most powerful Pandas idea is **groupby**: split rows into groups, calculate something for each group, combine the results. This is called **split–apply–combine**.

```python
df.groupby("city")["score"].mean()
```

```
city
Delhi     65.0
Mumbai     NaN
Pune      91.5
```

```
      SPLIT by city          APPLY mean()       COMBINE
  ┌─ Pune:  88, 95  ──────▶    91.5    ─┐
  ├─ Delhi: 65      ──────▶    65.0    ─┼──▶  a small table
  └─ Mumbai: NaN    ──────▶    NaN     ─┘
```

Several summaries at once with `.agg`:

```python
df.groupby("city").agg(
    people=("name", "count"),
    avg_score=("score", "mean"),
    oldest=("age", "max"),
)
```

A **pivot table** is a groupby shaped like a grid (just like Excel pivot tables):

```python
sales.pivot_table(index="region", columns="month", values="revenue", aggfunc="sum")
```

### 2.10 Combining tables

Data often lives in several tables. **Merging** (also called **joining**) combines them using a shared column, the **key**:

```python
orders    = pd.DataFrame({"customer_id": [1, 2, 1], "amount": [50, 30, 20]})
customers = pd.DataFrame({"customer_id": [1, 2], "name": ["Asha", "Ravi"]})

merged = orders.merge(customers, on="customer_id", how="left")
```

| `how=` | Keeps |
|---|---|
| `"inner"` | Only rows with a match in both tables |
| `"left"` | All rows from the left table, matches from the right |
| `"right"` | All rows from the right table |
| `"outer"` | Everything from both |

`pd.concat([df1, df2])` stacks tables on top of each other (same columns).

### 2.11 Time and dates

```python
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month
df["weekday"] = df["date"].dt.day_name()
monthly = df.set_index("date").resample("ME")["revenue"].sum()   # total per month
```

`.dt` gives date tools, just as `.str` gives text tools. `resample` regroups by time periods ("ME" = month end, "W" = week, "D" = day).

### 2.12 Charts and saving

```python
import matplotlib.pyplot as plt

df.groupby("city")["score"].mean().plot(kind="bar", title="Average score by city")
plt.tight_layout()
plt.savefig("scores.png")
plt.show()
```

Saving results:

```python
df.to_csv("clean_data.csv", index=False)     # index=False: don't save row numbers as a column
df.to_parquet("clean_data.parquet")           # faster, smaller format for big data
```

**Parquet** is a file format for tables that is compressed and keeps column types. It's common in real data teams.

> **In simple words:** NumPy gives you arrays: fast grids of numbers you can do maths on all at once. Pandas gives you DataFrames: tables you can load, inspect, select from, clean, group, merge and chart in a few lines. In pandas 3.0, change rows with a single `.loc[...] = ...`.

---

## 3. How it works: a real analysis, start to finish

**Scenario:** You run a small online shop. You have a messy file `orders.csv`. Your boss asks: *"Which product category makes the most money, and how are sales trending by month?"*

### The data

```
order_id,date,customer,category,price,quantity
1001,2026-01-03,asha,Books,12.5,2
1002,2026-01-05,Ravi ,electronics,250,1
1003,2026-01-05,Meera,Books,,1
1004,2026-02-11,john,Clothing,40,3
1004,2026-02-11,john,Clothing,40,3
1005,2026-02-15,Asha,Electronics,abc,1
1006,2026-03-02,ravi,books,8,5
1007,2026-03-20,Meera,Clothing,25,2
```

Can you spot the problems? Messy names and categories (`" Ravi "`, `"books"` vs `"Books"`), a missing price, a duplicate row (1004), and a price that's text (`"abc"`).

### Step 1: Load and inspect

```python
import pandas as pd
df = pd.read_csv("orders.csv")
print(df.shape)       # (8, 6)
df.info()
```

`info()` reveals `price` is a `str` column (because of `"abc"`), not a number. That's the first clue something is wrong.

### Step 2: Remove duplicates

```python
print(df.duplicated().sum())     # 1
df = df.drop_duplicates()
```

### Step 3: Fix text

```python
df["customer"] = df["customer"].str.strip().str.title()     # " Ravi " → "Ravi"
df["category"] = df["category"].str.strip().str.title()     # "books" → "Books"
```

### Step 4: Fix types

```python
df["price"] = pd.to_numeric(df["price"], errors="coerce")   # "abc" → NaN
df["date"] = pd.to_datetime(df["date"])
print(df.isna().sum())      # price: 2 missing
```

### Step 5: Handle missing values

Two prices are missing. Options: delete those rows, or fill with something sensible. A reasonable choice is the median price **of the same category** (the **median** is the middle value when sorted; it isn't thrown off by extreme values the way the average is).

```python
df["price"] = df["price"].fillna(
    df.groupby("category")["price"].transform("median")
)
```

`transform` returns a value for every row (the group's median, lined up with each row), so it fits back into the column.

### Step 6: Create the measure we need

```python
df["revenue"] = df["price"] * df["quantity"]
```

### Step 7: Answer question 1, best category

```python
by_cat = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
print(by_cat)
```

```
category
Electronics    500.0
Clothing       170.0
Books           75.25
```

### Step 8: Answer question 2, monthly trend

```python
monthly = df.set_index("date").resample("ME")["revenue"].sum()
monthly.plot(kind="line", marker="o", title="Monthly revenue")
```

### Step 9: Save the clean data

```python
df.to_csv("orders_clean.csv", index=False)
```

### The whole flow

```
 orders.csv (messy)
      │ read_csv
      ▼
 inspect (shape, info, isna) ──▶ find problems
      │
      ▼
 clean: drop_duplicates → str.strip/title → to_numeric/to_datetime → fillna
      │
      ▼
 feature: revenue = price × quantity
      │
      ├──▶ groupby(category).sum()  → "Electronics earns most"
      └──▶ resample(month).sum()    → trend chart
      │
      ▼
 orders_clean.csv
```

This **load → inspect → clean → transform → analyse → save** pipeline is what data people do every day. In Lesson 04 you'll add one more step at the end: *train a model.*

> **In simple words:** Real analysis follows a fixed rhythm: load, inspect, clean (duplicates, text, types, missing values), create new columns, group to answer questions, chart, save.

---

## 4. Key terms (in order)

| Term | Plain meaning |
|---|---|
| **NumPy** | Package for fast maths on arrays of numbers. |
| **Pandas** | Package for working with tables (DataFrames). |
| **Data science / analysis** | Collecting, cleaning and studying data to find answers. |
| **Matplotlib** | Package for drawing charts. |
| **Jupyter notebook** | Document of runnable code cells with results shown underneath. |
| **Array** | A grid of same-type numbers (NumPy's main object). |
| **Vectorisation** | Doing an operation on a whole array at once, without a loop. |
| **Vector / matrix / tensor** | 1-D / 2-D / 3-D-or-more arrays. |
| **Shape** | Size in each direction, e.g. `(2, 3)`. |
| **dtype** | The data type of the values in an array or column. |
| **Random seed** | Starting number that makes "random" results repeatable. |
| **Boolean mask** | A True/False array used to filter items. |
| **Aggregation** | Summarising many values into one (sum, mean, max…). |
| **Axis** | The direction of an operation: 0 = down columns, 1 = across rows. |
| **Standard deviation** | How spread out values are around the average. |
| **Broadcasting** | Stretching a smaller array to combine with a bigger one. |
| **Dot product** | Multiply matching elements and sum; used to measure similarity. |
| **Series** | A single labelled column. |
| **DataFrame** | A table of rows and columns. |
| **Index** | Row labels of a DataFrame. |
| **NaN** | Pandas' marker for a missing value. |
| **Copy-on-Write** | pandas 3.0 rule: selections act as copies; change data in one `.loc` step. |
| **Chained assignment** | `df[a][b] = x`: the old style that no longer works. |
| **`.loc` / `.iloc`** | Select by labels / by positions. |
| **Lambda** | A tiny one-line function without a name. |
| **Data cleaning** | Fixing errors, gaps and inconsistencies in data. |
| **Outlier** | A value far outside the normal range. |
| **Median** | The middle value when sorted. |
| **groupby / split–apply–combine** | Split rows into groups, calculate per group, combine results. |
| **Pivot table** | A groupby summary shaped as a grid. |
| **Merge / join / key** | Combine tables by matching a shared column (the key). |
| **resample** | Regroup time data into periods (days, months). |
| **Parquet** | A fast, compressed file format for tables. |

> **In simple words:** Arrays and DataFrames are the two containers; masks, groupby and merge are the three superpowers; NaN, dtype and Copy-on-Write are the three things that bite beginners.

---

## 5. The people involved

| Who | What they do | Day to day with NumPy/Pandas |
|---|---|---|
| **Data analyst** | Answers business questions | Loads CSVs and database exports, cleans, groups, charts, reports. |
| **Data scientist** | Finds patterns, builds models | Explores data in notebooks; prepares features for ML. |
| **Data engineer** | Builds the pipelines that move and store data | Writes cleaning jobs that run automatically; cares about speed (may also use tools like Polars, a newer, faster DataFrame library, or SQL). |
| **ML engineer** | Trains and deploys models | Turns DataFrames into NumPy arrays that models consume. |
| **AI engineer** | Builds LLM apps | Uses Pandas to load documents, log experiments, and evaluate AI answers in tables. |
| **Business stakeholders** (managers, clients) | Ask the questions | Never touch the code, but rely on its answers being correct, so cleaning really matters. |
| **NumPy and Pandas maintainers** | Open-source volunteers and funded developers | Ship releases like pandas 3.0 (Jan 2026). |

> **In simple words:** Analysts, scientists, engineers and AI builders all live in Pandas daily; managers depend on the answers; open-source maintainers keep the tools improving.

---

## 6. Common misconceptions and beginner mistakes

| Mistake | Fix |
|---|---|
| Looping over DataFrame rows with `for` | Use vectorised column maths: `df["a"] * df["b"]`. Loops are 100× slower. |
| `df[df.a > 1]["b"] = 0` (chained assignment) | `df.loc[df["a"] > 1, "b"] = 0`. |
| Using `and` / `or` in filters | Use `&` / `|` with brackets: `(df.a > 1) & (df.b < 5)`. |
| Forgetting methods return new objects | `df = df.dropna()`, not just `df.dropna()`. |
| Not looking at the data first | Always run `head()`, `info()`, `describe()`, `isna().sum()`. |
| Dropping all rows with any missing value | You might delete most of your data. Check how much is missing and think first. |
| Filling missing values with 0 without thinking | Zero can be a real value (e.g. price). Mean/median/"unknown" are often better. |
| Expecting text columns to be `object` | In pandas 3.0 they're `str`. Old tutorials differ. |
| Saving with the index | Use `to_csv(..., index=False)` or you get an extra "Unnamed: 0" column. |
| Thinking NumPy and Pandas compete | Pandas is built *on* NumPy; you use both. `df.to_numpy()` converts. |
| "Clean data is someone else's job." | In real projects it's 60–80% of the work. Embrace it. |

> **In simple words:** Avoid loops and chained assignment, look before you clean, think before you drop or fill, and remember most methods return a new table.

---

## 7. One-page recap

### The 10 things to remember

1. **NumPy = fast number grids; Pandas = tables.** Import as `np` and `pd`.
2. **Vectorise:** operate on whole arrays/columns, never loop over rows.
3. **Shape** tells you the size; vectors (1-D) and matrices (2-D) are the language of AI.
4. **Boolean masks filter:** `arr[arr > 5]`, `df[df["age"] > 20]`.
5. **The inspection ritual:** `head()`, `shape`, `info()`, `describe()`, `isna().sum()`.
6. **Cleaning checklist:** duplicates, messy text, wrong types, missing values, outliers.
7. **Change rows with one `.loc[mask, col] = value`** (Copy-on-Write in pandas 3.0).
8. **groupby = split–apply–combine.** It answers most business questions.
9. **merge** joins tables on a key; **concat** stacks them.
10. **The pipeline:** load → inspect → clean → transform → analyse → save.

### Cheat sheet

```python
a = np.array([1, 2, 3]); a * 2; a.mean(); a[a > 1]; np.dot(a, a)
df = pd.read_csv("f.csv"); df.head(); df.info()
df[["a", "b"]]; df[df["a"] > 1]; df.loc[df["a"] > 1, "b"] = 0
df.drop_duplicates(); df["c"].str.strip(); pd.to_numeric(df["p"], errors="coerce")
df["x"].fillna(df["x"].median())
df.groupby("cat")["rev"].sum(); df.merge(other, on="id", how="left")
df.to_csv("out.csv", index=False)
```

### What to learn next

➡️ **Lesson 03: APIs, JSON & Git/GitHub.** So far your data came from files. Next you'll pull live data from the internet through APIs, understand JSON (the format AI services speak), and start saving your work properly with Git.
