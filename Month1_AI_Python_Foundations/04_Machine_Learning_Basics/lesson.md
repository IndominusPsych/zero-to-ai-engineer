# Lesson 04: Machine Learning Basics

*Month 1, Weeks 3–4. Reading time: about 75 minutes. Assumes Lessons 01–03.*

---

## 🛠️ Setup for this lesson

| You need | Why | How to get it |
|---|---|---|
| Everything from Lessons 01–02 | uv, Python, VS Code + Jupyter | Setup Guide Steps 1–5 |
| **scikit-learn**, **pandas**, **numpy**, **matplotlib**, **joblib** | Train and evaluate models, plot results, save models | `uv add` (below) |
| No datasets to download | The lesson builds its own data; the practice uses datasets built into scikit-learn | - |

**Install:**

```bash
cd ~/ai-engineer-projects
uv init ml_practice && cd ml_practice
uv add scikit-learn pandas numpy matplotlib joblib
uv add --dev ipykernel      # optional, for notebooks
```

**Check it works:**

```bash
uv run python -c "import sklearn; from sklearn.datasets import load_iris; print('scikit-learn', sklearn.__version__, '| iris rows:', len(load_iris().data))"
```

Stuck? See the step-by-step instructions and the troubleshooting table in [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md).

---

## 1. The big picture

### What is this, in simple words?

Normally, to make a computer do something, a programmer writes the rules:

```python
if "free money" in email: label = "spam"
```

But some tasks have too many rules to write. What makes a photo a "cat"? What makes a house worth $300,000? You can't list every rule.

**Machine learning (ML)** flips this around. Instead of writing the rules, you **show the computer lots of examples with the answers**, and it **figures out the rules itself**.

```
 TRADITIONAL PROGRAMMING              MACHINE LEARNING

 rules  ─┐                           data    ─┐
         ├──▶ computer ──▶ answers             ├──▶ computer ──▶ RULES (a "model")
 data   ─┘                           answers ─┘
```

Analogy: teaching a child what a dog is. You don't give them a definition ("four legs, fur, barks"). You point at many dogs and say "dog," and at cats and say "not a dog." Eventually they recognise dogs they've never seen. That's machine learning.

### Which field does it belong to?

ML is a branch of **artificial intelligence**. Here's how the big words relate:

```
┌──────────────────────────────────────────────────────────┐
│ ARTIFICIAL INTELLIGENCE: machines doing "smart" tasks    │
│  ┌────────────────────────────────────────────────────┐  │
│  │ MACHINE LEARNING: learning patterns from data      │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │ DEEP LEARNING: ML using large "neural nets"  │  │  │
│  │  │  ┌────────────────────────────────────────┐  │  │  │
│  │  │  │ GENERATIVE AI / LLMs (Month 2):        │  │  │  │
│  │  │  │ deep learning that creates text/images │  │  │  │
│  │  │  └────────────────────────────────────────┘  │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Why does it matter?

ML powers spam filters, Netflix recommendations, fraud detection, maps' arrival times, face unlock, and, at the innermost circle, ChatGPT and Claude. Even if you'll mostly *use* large AI models rather than train them, understanding the basics (training, testing, overfitting, evaluation) lets you reason about why AI succeeds and fails. Those ideas come back constantly in Months 2 and 3.

> **In simple words:** Machine learning means giving a computer examples with answers so it learns the rules itself. It's the part of AI that all modern systems, including LLMs, are built on.

---

## 2. Core concepts

### 2.1 Data, features and labels

ML data is usually a table (a DataFrame!). Each row is one **example** (also called a **sample** or **observation**).

- **Features** are the input columns: the information you know. (Also called inputs, predictors, or "X".)
- The **label** is the column you want to predict: the answer. (Also called the target, or "y".)

| size_sqm | bedrooms | age_years | distance_km | **price** |
|---|---|---|---|---|
| 80 | 2 | 10 | 5 | **210,000** |
| 120 | 3 | 2 | 12 | **340,000** |
| 60 | 1 | 30 | 2 | **180,000** |
| ← features (X) → | | | | ← label (y) |

### 2.2 The model

A **model** is the "rule-maker" that learns how features relate to the label. At heart, it's a mathematical function with adjustable knobs called **parameters** (or **weights**).

The simplest example: a straight line.

```
price = w1 × size + w2 × bedrooms + ... + b
```

The `w`s and `b` are parameters. **Training** means finding the parameter values that make the model's guesses closest to the real answers.

Analogy: tuning a radio. The knobs are parameters. You twist them until the station comes in clearly (the predictions match reality).

### 2.3 Training and prediction

- **Training (fitting):** show the model examples with answers; it adjusts its parameters.
- **Prediction (inference):** give the trained model new features *without* answers; it guesses the label.

In Month 2, when you send a question to an LLM, you're doing **inference** on a model someone else trained.

### 2.4 Types of machine learning

| Type | You give it | It learns to | Example |
|---|---|---|---|
| **Supervised learning** | Examples **with** labels | Predict the label for new examples | Price from house features; spam or not |
| **Unsupervised learning** | Examples **without** labels | Find structure/groups by itself | Group customers into types |
| **Reinforcement learning** | A goal and rewards | Choose actions that earn the most reward | Game-playing AI; also used to fine-tune LLMs to be helpful |

Supervised learning has two flavours, depending on the label:

| Flavour | Label is… | Example question | Example answer |
|---|---|---|---|
| **Regression** | A number | "What price?" | 312,500 |
| **Classification** | A category | "Spam or not?" | "spam" |

Classification with two choices is **binary**; with more, it's **multi-class**.

### 2.5 Loss: how wrong is the model?

To improve, the model needs a score for how wrong it is. That's the **loss** (or **error**). Lower is better.

For regression, a common loss is **Mean Squared Error (MSE)**: for each example, take (prediction − truth), square it so negatives don't cancel positives, then average.

| Real | Predicted | Error | Squared |
|---|---|---|---|
| 200 | 210 | 10 | 100 |
| 300 | 280 | −20 | 400 |
| | | **MSE** | **250** |

### 2.6 Gradient descent: how models learn

How does the model find good parameters? The most common method is **gradient descent**.

Analogy: you're on a foggy hill at night and want to reach the lowest valley (the lowest loss). You can't see far, but you can feel which way the ground slopes under your feet. So you take a small step downhill. Repeat. Eventually you reach the bottom.

- The **gradient** is the direction of steepest slope.
- The **learning rate** is how big each step is. Too big: you leap over the valley. Too small: it takes forever.
- One pass through all the training data is an **epoch**.

```
 loss
  │ \
  │  \  ●  step
  │   \   ●  step
  │    \    ●
  │     \__   ●__●   ← bottom = best parameters
  └─────────────────── parameter value
```

You won't code gradient descent by hand; libraries do it. But this is *exactly* how the giant models in Month 2 were trained too, just with billions of parameters.

### 2.7 Train / test split: honest evaluation

If you test a student with the exact questions they studied, a perfect score proves nothing; they may have memorised. ML is the same.

So we **split** the data:

- **Training set** (~80%): the model learns from this.
- **Test set** (~20%): hidden until the end, used once to measure real performance on unseen data.

Often there's a third, the **validation set**: used during development to compare options, so the test set stays truly untouched.

```
 all data ───┬── 70% TRAIN       (learn)
             ├── 15% VALIDATION  (tune & choose)
             └── 15% TEST        (final exam, look once)
```

**Cross-validation** is a smarter version: split the training data into, say, 5 parts ("folds"), train on 4 and check on 1, rotate 5 times, and average the scores. More reliable, especially with small data.

### 2.8 Overfitting and underfitting

The most important idea in ML.

- **Underfitting:** the model is too simple to capture the pattern. Bad on training data *and* test data. (A student who didn't study.)
- **Overfitting:** the model memorised the training data, including its noise and quirks. Great on training, bad on test. (A student who memorised the answer key but can't solve new problems.)
- **Good fit:** learned the real pattern. Good on both.

| | Training score | Test score | Fix |
|---|---|---|---|
| Underfitting | Low | Low | More complex model, better features |
| Good fit | High | High (close to training) | 🎉 |
| Overfitting | Very high | Much lower | Simpler model, more data, **regularisation** |

**Regularisation** means adding a penalty that discourages the model from becoming too complex: a "keep it simple" rule.

This idea links to the **bias–variance trade-off**: simple models have high **bias** (consistently wrong in the same way); complex models have high **variance** (change wildly with small data changes). The goal is the sweet spot.

### 2.9 Feature engineering and preprocessing

Models only see numbers. **Preprocessing** converts raw data into model-ready numbers:

| Step | Why | How (scikit-learn) |
|---|---|---|
| Fill missing values (**imputation**) | Models can't handle NaN | `SimpleImputer(strategy="median")` |
| Encode categories | "Pune"/"Delhi" aren't numbers | **One-hot encoding**: a 0/1 column per category, `OneHotEncoder` |
| **Scale** numbers | Some models get confused when one feature is 0–1 and another is 0–1,000,000 | `StandardScaler` (mean 0, std 1) or min-max scaling |

**Feature engineering** means creating more useful features from existing ones, e.g. `price_per_sqm`, `house_age = 2026 − year_built`, `is_weekend` from a date. Good features often matter more than the choice of model.

**Data leakage** is a sneaky bug: when information from the test set (or from the future) accidentally gets into training. Example: scaling using the average of *all* data before splitting. The test score looks amazing, then the model fails in real life. Fix: split **first**, then fit preprocessing on training data only. Scikit-learn **pipelines** (below) do this automatically.

### 2.10 A tour of common algorithms

An **algorithm** is the method a model uses to learn. You don't need the maths yet, just the intuition:

| Algorithm | Task | Intuition |
|---|---|---|
| **Linear regression** | Regression | Fit the best straight line (or flat surface) through the points. |
| **Logistic regression** | Classification | Despite the name, it classifies: outputs a probability (0–1) using an S-shaped curve. |
| **Decision tree** | Both | A flowchart of yes/no questions: "size > 100? → bedrooms > 2? → …" Easy to explain; overfits easily. |
| **Random forest** | Both | Hundreds of decision trees, each slightly different, voting together. Robust, a great default. |
| **Gradient boosting** (XGBoost, LightGBM) | Both | Trees built one after another, each fixing the previous ones' mistakes. Often the top performer on tables. |
| **k-Nearest Neighbours (kNN)** | Both | Find the k most similar known examples and copy their answer. (Similarity search returns in Lesson 09!) |
| **k-Means** | Clustering (unsupervised) | Group points into k clusters around centre points. |
| **Neural networks** | Both | Layers of simple maths units loosely inspired by brain neurons. With many layers = **deep learning**, the basis of LLMs. |

### 2.11 Neural networks in one minute

A **neuron** (in ML) takes several numbers in, multiplies each by a weight, adds them up, and passes the result through a simple function (an **activation function**) that decides how strongly it "fires." Stack many neurons into **layers**, connect layers in sequence, and you get a **neural network**.

```
 inputs        hidden layer(s)      output
  size  ─┐      ○ ○ ○ ○
  beds  ─┼────▶ ○ ○ ○ ○  ────▶    price
  age   ─┘      ○ ○ ○ ○
```

Each connection has a weight. Training (gradient descent, via a method called **backpropagation**) adjusts millions or billions of weights. Libraries like **PyTorch** are used to build these. LLMs are enormous neural networks of a special design called the **transformer** (Lesson 06).

### 2.12 Evaluation metrics

How do we score a model? It depends on the task.

**Regression metrics:**

| Metric | Meaning | Good value |
|---|---|---|
| **MAE** (Mean Absolute Error) | Average size of the error, in the label's units | Lower; "off by $15k on average" |
| **RMSE** (Root MSE) | Like MAE but punishes big errors more | Lower |
| **R²** (R-squared) | How much of the variation the model explains, 0 to 1 | Closer to 1 |

**Classification metrics.** First, the **confusion matrix**, a table of right and wrong predictions:

|  | Predicted: spam | Predicted: not spam |
|---|---|---|
| **Actually spam** | ✅ True Positive (TP) | ❌ False Negative (FN): missed spam |
| **Actually not spam** | ❌ False Positive (FP): good email flagged | ✅ True Negative (TN) |

From it:

| Metric | Formula | Question it answers |
|---|---|---|
| **Accuracy** | (TP + TN) / all | How often am I right overall? |
| **Precision** | TP / (TP + FP) | When I say "spam," how often am I right? |
| **Recall** | TP / (TP + FN) | Of all real spam, how much did I catch? |
| **F1 score** | balance of precision and recall | One number when you care about both |

**Why accuracy can lie:** if 99% of transactions are not fraud, a model that always says "not fraud" is 99% accurate and completely useless. With **imbalanced data** (one class is rare), look at precision and recall.

Precision vs recall is a trade-off you choose based on cost: for cancer screening, **recall** matters most (don't miss cases). For a spam filter, **precision** matters (don't hide important emails).

A **baseline** is the score of a dumb strategy (always predict the average, or the most common class). Your model must beat it, or it's not learning anything.

### 2.13 scikit-learn: the toolbox

**scikit-learn** (imported as `sklearn`) is the standard Python library for classic ML. Every model follows the same pattern:

```python
model = SomeModel()             # 1. choose
model.fit(X_train, y_train)     # 2. learn
preds = model.predict(X_test)   # 3. predict
```

That consistency means once you can use one model, you can use them all.

> **In simple words:** Features go in, a label comes out. A model has parameters; training tunes them to lower the loss (via gradient descent). Split data so you test on unseen examples. Watch for overfitting and data leakage. Preprocess (impute, encode, scale), try a few algorithms, and score them with the right metric against a baseline.

---

## 3. How it works: predicting house prices, start to finish

**Scenario:** A real-estate startup wants to estimate house prices instantly from a few details. You have a table of past sales.

### Step 0: Setup and data

```bash
uv add scikit-learn pandas numpy matplotlib
```

We'll generate realistic fake data so you can run this anywhere:

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1000
df = pd.DataFrame({
    "size_sqm":    rng.integers(40, 250, n),
    "bedrooms":    rng.integers(1, 6, n),
    "age_years":   rng.integers(0, 60, n),
    "distance_km": rng.uniform(0.5, 30, n).round(1),
    "city":        rng.choice(["Pune", "Mumbai", "Delhi"], n),
})
city_bonus = df["city"].map({"Pune": 0, "Mumbai": 120_000, "Delhi": 60_000})
df["price"] = (
    2_500 * df["size_sqm"] + 15_000 * df["bedrooms"] - 1_200 * df["age_years"]
    - 3_000 * df["distance_km"] + city_bonus + rng.normal(0, 25_000, n)
).round(-3)
df.loc[rng.choice(n, 30, replace=False), "age_years"] = np.nan    # some missing values
```

### Step 1: Define the problem

- Task type: **supervised regression** (the label is a number).
- Features (X): size, bedrooms, age, distance, city. Label (y): price.
- Metric: **MAE**, because "off by ₹X on average" is easy for the business to understand.

### Step 2: Explore

```python
df.info()
df.describe()
df.groupby("city")["price"].mean()
df.plot.scatter(x="size_sqm", y="price")    # bigger → pricier? yes, roughly a line
```

### Step 3: Split first (avoid leakage!)

```python
from sklearn.model_selection import train_test_split

X = df.drop(columns="price")
y = df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### Step 4: Baseline

```python
from sklearn.metrics import mean_absolute_error

baseline_pred = np.full(len(y_test), y_train.mean())   # always guess the average
print("Baseline MAE:", mean_absolute_error(y_test, baseline_pred))
# roughly 140,000: our model must beat this
```

### Step 5: Preprocessing + model in one pipeline

A **pipeline** chains preprocessing and a model into one object, so the same steps apply to training and new data, and preprocessing only learns from training data.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression

numeric = ["size_sqm", "bedrooms", "age_years", "distance_km"]
categorical = ["city"]

preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])

linear = Pipeline([("prep", preprocess), ("model", LinearRegression())])
linear.fit(X_train, y_train)
print("Linear MAE:", mean_absolute_error(y_test, linear.predict(X_test)))
# around 20,000: far better than the baseline
```

### Step 6: Try another model

```python
from sklearn.ensemble import RandomForestRegressor

forest = Pipeline([("prep", preprocess),
                   ("model", RandomForestRegressor(n_estimators=200, random_state=42))])
forest.fit(X_train, y_train)
print("Forest MAE:", mean_absolute_error(y_test, forest.predict(X_test)))
```

On this data the linear model often wins, because we *created* the data with a straight-line formula. On real, messy data, forests usually win. **That's why you always try a few.**

### Step 7: Check for overfitting

```python
from sklearn.metrics import r2_score
for name, m in [("linear", linear), ("forest", forest)]:
    print(name,
          "train R²:", round(r2_score(y_train, m.predict(X_train)), 3),
          "test R²:",  round(r2_score(y_test,  m.predict(X_test)), 3))
```

If the forest scores ~0.99 on train but notably lower on test, it's overfitting a bit. Fixes: limit tree depth (`max_depth=10`), more data.

### Step 8: Cross-validate to be sure

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(linear, X_train, y_train, cv=5, scoring="neg_mean_absolute_error")
print("CV MAE:", -scores.mean())
```

(Scikit-learn makes errors negative so "higher is better" for every score. The minus sign flips it back.)

### Step 9: Use it and save it

```python
new_house = pd.DataFrame([{"size_sqm": 110, "bedrooms": 3, "age_years": 5,
                           "distance_km": 8, "city": "Mumbai"}])
print("Estimated price:", round(linear.predict(new_house)[0], -3))

import joblib
joblib.dump(linear, "house_model.joblib")       # save the trained model to a file
model = joblib.load("house_model.joblib")       # load it later, e.g. inside an API
```

In Lesson 16 you'll put a model like this behind a web API so anyone can use it.

### The ML workflow (memorise this)

```
 1 Define problem & metric ─▶ 2 Get & explore data ─▶ 3 Split (train/test)
        ▼
 4 Baseline ─▶ 5 Preprocess + model (pipeline) ─▶ 6 Try alternatives
        ▼
 7 Check over/underfitting ─▶ 8 Cross-validate & tune ─▶ 9 Final test once ─▶ 10 Save & deploy
                                                                       │
                                     monitor in real life ◀────────────┘ (and retrain when data changes)
```

> **In simple words:** Define the task and metric, explore, split, beat a baseline, use a pipeline so preprocessing can't leak, compare models, check train vs test scores, cross-validate, then save the winner.

---

## 4. Key terms (in order)

| Term | Plain meaning |
|---|---|
| **Machine learning (ML)** | Computers learning rules from examples instead of being told them. |
| **Deep learning** | ML using large multi-layer neural networks. |
| **Generative AI** | Deep learning models that create new content (text, images). |
| **Example / sample** | One row of data. |
| **Feature (X)** | An input column the model uses. |
| **Label / target (y)** | The answer column to predict. |
| **Model** | The learned function from features to label. |
| **Parameters / weights** | The adjustable knobs inside a model. |
| **Training / fitting** | Adjusting parameters using examples with answers. |
| **Prediction / inference** | Using a trained model on new data. |
| **Supervised / unsupervised / reinforcement** | With labels / without labels / learning from rewards. |
| **Regression / classification** | Predicting a number / predicting a category. |
| **Loss** | A score of how wrong the model is. |
| **MSE** | Average of squared errors. |
| **Gradient descent** | Repeatedly stepping "downhill" to reduce loss. |
| **Learning rate** | The step size in gradient descent. |
| **Epoch** | One full pass over the training data. |
| **Training / validation / test set** | Learn from / tune with / final exam data. |
| **Cross-validation** | Rotating train/check folds and averaging. |
| **Overfitting / underfitting** | Memorised noise / too simple to learn. |
| **Regularisation** | A penalty for complexity, to reduce overfitting. |
| **Bias / variance** | Consistently wrong / overly sensitive to data. |
| **Preprocessing** | Turning raw data into model-ready numbers. |
| **Imputation** | Filling in missing values. |
| **One-hot encoding** | One 0/1 column per category. |
| **Scaling** | Putting numeric features on similar ranges. |
| **Feature engineering** | Creating better features from existing data. |
| **Data leakage** | Test or future info sneaking into training. |
| **Algorithm** | The learning method (linear regression, random forest…). |
| **Decision tree / random forest / gradient boosting** | Question flowchart / many voting trees / trees fixing each other's errors. |
| **kNN / k-means** | Copy nearest neighbours / group into k clusters. |
| **Neural network / neuron / layer** | Network of simple weighted units arranged in layers. |
| **Activation function** | Decides how strongly a neuron fires. |
| **Backpropagation** | The method to compute how to adjust each weight. |
| **PyTorch** | Popular library for building neural networks. |
| **Transformer** | The neural network design behind LLMs (Lesson 06). |
| **MAE / RMSE / R²** | Regression scores. |
| **Confusion matrix** | Table of TP, FP, FN, TN. |
| **Accuracy / precision / recall / F1** | Classification scores. |
| **Imbalanced data** | One class is much rarer than others. |
| **Baseline** | Score of a dumb strategy; your model must beat it. |
| **scikit-learn** | Standard Python library for classic ML (`fit` / `predict`). |
| **Pipeline** | Chained preprocessing + model in one object. |

> **In simple words:** The core loop in words: features + labels → train (minimise loss) → evaluate on held-out data with the right metric → avoid overfitting and leakage.

---

## 5. The people involved

| Who | What they do | ML day to day |
|---|---|---|
| **Data scientist** | Explores data, builds and evaluates models | Notebooks, scikit-learn, metrics, explaining results to the business. |
| **ML engineer** | Turns models into reliable software | Pipelines, saving/serving models, monitoring, retraining. |
| **Data engineer** | Gets clean data where it's needed | Builds the data pipelines models feed on. |
| **ML researcher** | Invents new methods | Works at universities and AI labs (Anthropic, OpenAI, Google DeepMind, Meta) on new architectures and training methods. |
| **AI engineer** | Builds products using pre-trained models | Rarely trains from scratch; uses LLMs via APIs but needs ML intuition for evaluation and failure modes. |
| **Data labellers / annotators** | Create labels by hand | Tag images, rate AI answers; their work feeds supervised learning and LLM fine-tuning. |
| **Domain experts** (doctors, bankers…) | Know what the data means | Define the problem, judge whether predictions make sense. |
| **End users / the public** | Are affected by predictions | Loan approvals, medical alerts; this is why fairness and bias in data matter. |
| **Regulators** | Set rules | E.g. the EU AI Act sets duties for high-risk AI systems. |

> **In simple words:** Scientists build models, engineers ship them, labellers and experts supply knowledge, and real people live with the results, so fairness and correctness matter.

---

## 6. Common misconceptions and beginner mistakes

| Myth / mistake | Reality / fix |
|---|---|
| "ML is magic / the model understands." | It finds statistical patterns. It's only as good as its data. |
| "More complex model = better." | Start simple. Linear/logistic regression and random forests are hard to beat on tables. |
| Testing on training data | Always evaluate on held-out test data. |
| Preprocessing before splitting | Split first; use a pipeline to avoid leakage. |
| Only reporting accuracy | With imbalanced data, report precision/recall/F1 and the confusion matrix. |
| No baseline | Always compute one; a "95% accurate" model may be worse than guessing. |
| Using the test set over and over while tuning | That turns it into training data. Use validation/cross-validation; look at test once. |
| "I need a GPU and huge data to start." | Classic ML runs on a laptop with a few thousand rows. |
| Garbage in, garbage out ignored | Data quality beats algorithm choice. Lesson 02 skills matter most. |
| "Correlation means cause." | A model can use a pattern without it being a cause (ice cream sales predict drownings; both rise in summer). |
| "Once trained, done forever." | The world changes (**data drift**); models must be monitored and retrained. |
| Biased data → biased model | If past decisions were unfair, the model learns the unfairness. Check performance across groups. |

> **In simple words:** Start simple, split first, use the right metric, beat a baseline, protect your test set, and remember models only reflect their data.

---

## 7. One-page recap

### The 10 things to remember

1. **ML learns rules from examples** instead of being programmed with them.
2. **AI ⊃ ML ⊃ deep learning ⊃ generative AI/LLMs.**
3. **Features (X) → model → label (y).** Regression predicts numbers; classification predicts categories.
4. **Training minimises a loss** by gradient descent: small steps downhill.
5. **Split the data;** judge only on unseen test data.
6. **Overfitting = memorising.** Compare train vs test scores.
7. **Preprocess with pipelines:** impute, encode, scale, without leakage.
8. **Pick the metric for the cost of mistakes:** MAE for prices; precision/recall when classes are imbalanced.
9. **Always beat a baseline,** and try a few algorithms.
10. **scikit-learn's pattern is `fit` then `predict`.** Save models with `joblib`.

### Cheat sheet

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipe = Pipeline([("prep", ColumnTransformer([...])), ("model", RandomForestClassifier())])
pipe.fit(X_train, y_train); preds = pipe.predict(X_test)
mean_absolute_error / r2_score / accuracy_score / classification_report / confusion_matrix
cross_val_score(pipe, X_train, y_train, cv=5)
joblib.dump(pipe, "model.joblib")
```

### What to learn next

➡️ **Lesson 05: Build 2–3 small projects.** Time to put Lessons 01–04 together into real, portfolio-ready projects. Then in Month 2 you'll meet the biggest ML models ever built: large language models.
