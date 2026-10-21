# Practice & Test 04: Machine Learning Basics

> **🛠️ Before you start:** you need scikit-learn, pandas, numpy, matplotlib, joblib (datasets are built in). Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run python -c "import sklearn; print(sklearn.__version__)"
> ```

**Setup:**

```bash
uv init ml_practice && cd ml_practice
uv add scikit-learn pandas numpy matplotlib joblib
```

All datasets used here are built into scikit-learn, so no downloads are needed.

---

## Part A: Concept warm-ups (no code)

**A1.** For each, say **regression**, **classification** (binary or multi-class) or **unsupervised clustering**:
1. Predict tomorrow's temperature.
2. Decide if a transaction is fraud.
3. Group news articles into topics without any labels.
4. Recognise which of 10 digits (0–9) is in an image.
5. Predict how many minutes a delivery will take.
6. Decide if a review is positive, negative or neutral.

**A2.** Identify the features and the label: *"A bank wants to predict whether a loan applicant will default, using their income, age, existing debt, and employment years."*

**A3.** A model scores 99% on training data and 62% on test data. What's happening? Name three fixes.

**A4.** Compute by hand from this confusion matrix (positive = "has disease"):

|  | Pred: disease | Pred: healthy |
|---|---|---|
| **Actually disease** | 40 | 10 |
| **Actually healthy** | 20 | 930 |

Accuracy, precision, recall. Which matters more here, and is this a good model?

**A5.** Spot the data leakage: *"I scaled all 10,000 rows with StandardScaler, then split into train and test."*

**A6.** A model predicting house prices has MAE = 50,000. The baseline (always predict average) has MAE = 48,000. What do you conclude?

---

## Part B: Hands-on exercises

**B1. Your first classifier (Iris).**

```python
from sklearn.datasets import load_iris
X, y = load_iris(return_X_y=True, as_frame=True)
```

Split 80/20 (`random_state=42`, `stratify=y`), train a `DecisionTreeClassifier`, print accuracy and `classification_report`. (*`stratify=y` keeps class proportions equal in train and test.*)

**B2. Compare models.** On the same split, try `LogisticRegression(max_iter=1000)`, `KNeighborsClassifier()`, `RandomForestClassifier()`. Print a small table of test accuracies.

**B3. Overfitting experiment.** Using the breast cancer dataset (`load_breast_cancer`), train `DecisionTreeClassifier(max_depth=d)` for d = 1…15. Record train and test accuracy for each and plot both lines. Where does overfitting start?

**B4. Metrics for imbalance.** On breast cancer data, compute the confusion matrix, precision and recall for a logistic regression pipeline (with `StandardScaler`). In this dataset, `0` = malignant. Which mistake (FP or FN) would worry a doctor more?

**B5. Pipeline with mixed data.** Build this small DataFrame and a full pipeline (impute + scale numbers, one-hot encode city) to predict `bought` (0/1):

```python
import pandas as pd, numpy as np
rng = np.random.default_rng(0)
n = 500
df = pd.DataFrame({
    "age": rng.integers(18, 70, n).astype(float),
    "income": rng.normal(50_000, 15_000, n).round(),
    "city": rng.choice(["Pune", "Delhi", "Mumbai"], n),
    "visits": rng.integers(0, 20, n),
})
df["bought"] = ((df["visits"] > 8) & (df["income"] > 45_000)).astype(int)
df.loc[rng.choice(n, 25, replace=False), "age"] = np.nan
```

Report accuracy, F1 and 5-fold cross-validation score.

**B6. Regression.** Use `load_diabetes` (predict disease progression). Compare a baseline (mean), `LinearRegression`, and `RandomForestRegressor` by MAE and R².

**B7. Clustering.** Use `KMeans(n_clusters=3)` on the Iris features *without* the labels. Compare the clusters to the true species with `pd.crosstab`. How well did it find the species unsupervised?

**B8. Save & load.** Save your best B5 pipeline with `joblib`, load it in a new script, and predict for one new customer.

---

## Part C: Mini-project: "Will they pass?" predictor (90 min)

Build a model that predicts whether a student passes (final score ≥ 60) from study hours, attendance %, previous score, sleep hours and whether they have a tutor.

1. Generate 1,000 rows of realistic data (as in Lesson 04 Step 0) with sensible relationships plus noise, and some missing values.
2. Define the problem, metric and baseline in a markdown cell.
3. Explore with 2 charts.
4. Build a pipeline; compare at least 3 models with cross-validation.
5. Check overfitting (train vs test).
6. Report the confusion matrix and explain precision/recall in plain words for a teacher.
7. Save the model; write a `predict.py` that asks for inputs and prints "likely pass / at risk".
8. Commit to GitHub with a README including your results table.

| Rubric | ✓ |
|---|---|
| Split before preprocessing (no leakage) | |
| Baseline reported | |
| ≥ 3 models compared via cross-validation | |
| Train vs test comparison | |
| Confusion matrix explained in plain words | |
| Saved model + working predict script | |
| README with results | |

---

## Part D: Quiz (25 minutes)

1. What's the key difference between ML and traditional programming?
   a) ML is faster b) ML doesn't use data c) ML needs no code d) In ML the computer learns rules from examples

2. Which is correct?
   a) AI ⊃ ML ⊃ deep learning b) ML ⊃ AI c) LLMs ⊃ AI d) Deep learning ⊃ ML

3. Predicting the number of bikes rented tomorrow is:
   a) Clustering b) Regression c) Reinforcement learning d) Classification

4. A "label" is:
   a) A row number b) An input column c) The answer to predict d) A model name

5. Gradient descent is best described as:
   a) Splitting data b) Randomly guessing parameters c) Sorting data d) Taking small steps that reduce the loss

6. A learning rate that is too large may:
   a) Always be better b) Prevent overfitting c) Make training overshoot and fail to settle d) Reduce data size

7. Why keep a test set aside?
   a) To measure performance on unseen data b) To train faster c) It's optional decoration d) To store labels

8. Training score high, test score much lower means:
   a) Underfitting b) Overfitting c) Data is missing d) Perfect model

9. One-hot encoding is used to:
   a) Scale numbers b) Turn categories into 0/1 columns c) Split data d) Fill missing values

10. Data leakage is:
    a) Missing values b) A slow model c) Test/future information sneaking into training d) Losing data

11. With 1% fraud, a model that always predicts "not fraud" has accuracy:
    a) 99% b) 0% c) 1% d) 50%

12. Recall answers:
    a) Overall correctness b) Of predicted positives, how many are right? c) Error size d) Of actual positives, how many did we catch?

13. Random forest is:
    a) A single tree b) A clustering method c) A neural network d) Many trees voting

14. In scikit-learn, training a model is done with:
    a) `.fit()` b) `.learn()` c) `.train()` d) `.run()`

15. What does a scikit-learn Pipeline help prevent?
    a) Slow imports b) Data leakage and inconsistent preprocessing c) Missing labels d) Overfitting always

**Short answer.**

16. Explain overfitting with an everyday analogy, and how you'd detect it.
17. Why might accuracy be a misleading metric? Give an example.
18. Describe the 10-step ML workflow from memory.
19. What is a baseline and why must you always compute one?
20. How does what you learned here relate to LLMs like Claude or ChatGPT?

---

## Answer Key

### Part A

**A1.** 1 regression · 2 binary classification · 3 clustering (unsupervised) · 4 multi-class classification · 5 regression · 6 multi-class classification.

**A2.** Features: income, age, existing debt, employment years. Label: default (yes/no). Binary classification.

**A3.** Overfitting. Fixes: simpler model (e.g. limit tree depth), regularisation, more training data, fewer/better features, cross-validation to tune.

**A4.** Accuracy = (40 + 930) / 1000 = **97%**. Precision = 40 / (40 + 20) = **66.7%**. Recall = 40 / (40 + 10) = **80%**. For disease detection **recall** matters most: missing 10 sick people (FN) is dangerous. 97% accuracy sounds great but the baseline "everyone healthy" is 95%, so the real value comes from the 80% recall; it could still be improved.

**A5.** The scaler computed the mean and standard deviation using test rows too, so the training process "saw" test information. Split first, fit the scaler on training data only (pipelines do this).

**A6.** The model is worse than guessing the average; it hasn't learned anything useful. Check features, bugs, leakage, or preprocessing.

### Part B: reference solutions

```python
import numpy as np, pandas as pd, matplotlib.pyplot as plt, joblib
from sklearn.datasets import load_iris, load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             precision_score, recall_score, f1_score,
                             mean_absolute_error, r2_score)

# B1
X, y = load_iris(return_X_y=True, as_frame=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
tree = DecisionTreeClassifier(random_state=42).fit(X_tr, y_tr)
print(accuracy_score(y_te, tree.predict(X_te)))          # ~0.93-1.0
print(classification_report(y_te, tree.predict(X_te)))

# B2
models = {"tree": DecisionTreeClassifier(random_state=42),
          "logreg": LogisticRegression(max_iter=1000),
          "knn": KNeighborsClassifier(),
          "forest": RandomForestClassifier(random_state=42)}
print(pd.Series({n: accuracy_score(y_te, m.fit(X_tr, y_tr).predict(X_te)) for n, m in models.items()}))

# B3
Xb, yb = load_breast_cancer(return_X_y=True)
Xb_tr, Xb_te, yb_tr, yb_te = train_test_split(Xb, yb, test_size=0.25, random_state=0, stratify=yb)
rows = []
for d in range(1, 16):
    m = DecisionTreeClassifier(max_depth=d, random_state=0).fit(Xb_tr, yb_tr)
    rows.append({"depth": d, "train": m.score(Xb_tr, yb_tr), "test": m.score(Xb_te, yb_te)})
res = pd.DataFrame(rows).set_index("depth"); res.plot(marker="o"); plt.show()
# Train accuracy climbs to 1.0; test peaks around depth 3-5 then flattens/drops → overfitting beyond that.

# B4
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xb_tr, yb_tr)
p = pipe.predict(Xb_te)
print(confusion_matrix(yb_te, p))
print("precision (malignant):", precision_score(yb_te, p, pos_label=0))
print("recall    (malignant):", recall_score(yb_te, p, pos_label=0))
# A doctor worries most about missing a malignant tumour (predicting benign when it's malignant).
# With malignant as the class of interest, that's a false negative → prioritise recall for class 0.

# B5  (df from the exercise)
X5, y5 = df.drop(columns="bought"), df["bought"]
X5_tr, X5_te, y5_tr, y5_te = train_test_split(X5, y5, test_size=0.2, random_state=0, stratify=y5)
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), ["age", "income", "visits"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),
])
clf = Pipeline([("prep", prep), ("model", RandomForestClassifier(random_state=0))]).fit(X5_tr, y5_tr)
pred = clf.predict(X5_te)
print(accuracy_score(y5_te, pred), f1_score(y5_te, pred))
print(cross_val_score(clf, X5_tr, y5_tr, cv=5).mean())

# B6
Xd, yd = load_diabetes(return_X_y=True)
Xd_tr, Xd_te, yd_tr, yd_te = train_test_split(Xd, yd, test_size=0.2, random_state=0)
print("baseline MAE", mean_absolute_error(yd_te, np.full(len(yd_te), yd_tr.mean())))
for name, m in [("linear", LinearRegression()), ("forest", RandomForestRegressor(random_state=0))]:
    m.fit(Xd_tr, yd_tr); pr = m.predict(Xd_te)
    print(name, mean_absolute_error(yd_te, pr), r2_score(yd_te, pr))
# Linear and forest both clearly beat the baseline; R² around 0.4-0.5: a hard problem.

# B7
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
print(pd.crosstab(km.labels_, y))
# One species is perfectly separated; the other two overlap a bit (~90% agreement overall).

# B8
joblib.dump(clf, "buyer_model.joblib")
loaded = joblib.load("buyer_model.joblib")
print(loaded.predict(pd.DataFrame([{"age": 30, "income": 60_000, "city": "Pune", "visits": 12}])))  # [1]
```

### Part D: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | d | 6 | c | 11 | a |
| 2 | a | 7 | a | 12 | d |
| 3 | b | 8 | b | 13 | d |
| 4 | c | 9 | b | 14 | a |
| 5 | d | 10 | c | 15 | b |

**16.** Like a student memorising past exam answers instead of learning the subject: perfect on old papers, poor on new questions. Detect it by comparing training and test (or validation) scores; a large gap means overfitting.

**17.** When classes are imbalanced, always predicting the common class scores high accuracy while being useless. E.g. 99% of emails aren't phishing, so "never phishing" = 99% accurate but catches none. Use precision, recall, F1, confusion matrix.

**18.** Define problem & metric → get & explore data → split → baseline → preprocess + model (pipeline) → try alternatives → check over/underfitting → cross-validate & tune → final test once → save, deploy, monitor.

**19.** The score of a trivially simple strategy (mean prediction, most common class). It tells you whether your model has actually learned something; without it, a number like "80% accuracy" has no meaning.

**20.** LLMs are giant neural networks (deep learning, inside ML) trained with the same ideas: features and targets (predict the next word), a loss, gradient descent, held-out evaluation, and risks like overfitting and biased data. When you use them via API you're doing inference.

**Scoring:** out of 25. ≥ 21 move on.
