# Practice & Test 03: APIs, JSON & Git/GitHub

> **🛠️ Before you start:** you need Git, a GitHub account, `gh` logged in; requests, python-dotenv, pydantic, pandas. Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> git --version && gh auth status
> ```

**Setup:**

```bash
uv init api_practice && cd api_practice
uv add requests python-dotenv pydantic pandas
git init
```

Free, no-key APIs used below:

| API | URL | Returns |
|---|---|---|
| Open-Meteo | `https://api.open-meteo.com/v1/forecast` | Weather |
| Random User | `https://randomuser.me/api/?results=5` | Fake people |
| JSONPlaceholder | `https://jsonplaceholder.typicode.com/posts` | Fake blog posts (supports POST for practice) |
| REST Countries | `https://restcountries.com/v3.1/name/india` | Country info |

---

## Part A: JSON warm-ups

**A1.** Which of these are **valid JSON**? Why or why not?

```
1) {"name": "Asha", "age": 21}
2) {'name': 'Asha'}
3) {"active": True}
4) [1, 2, 3,]
5) {"tags": [], "note": null}
```

**A2.** Given:

```python
data = {"user": {"name": "Asha", "langs": ["python", "sql"], "address": {"city": "Pune"}}}
```

Write the expressions to get: (a) `"sql"`, (b) `"Pune"`, (c) the number of languages, (d) the user's phone or `"n/a"` if missing.

**A3.** Convert this Python dict to a pretty JSON string, save it to `user.json`, read it back, and confirm the round-trip equals the original.

---

## Part B: API exercises

**B1. GET basics.** Fetch `https://randomuser.me/api/?results=5`. Print the status code, then each person's full name, country and email.

**B2. Query parameters.** Call Open-Meteo for 3 cities of your choice (find their latitude/longitude online). Print a table sorted by current temperature.

**B3. Status codes.** Request `https://jsonplaceholder.typicode.com/posts/99999`. What status code do you get? Write code that prints a friendly message for 404 instead of crashing.

**B4. POST.** Send `{"title": "My first post", "body": "Learning APIs", "userId": 1}` to `https://jsonplaceholder.typicode.com/posts`. Print the status code (expect 201) and the returned JSON.

**B5. Retry.** Write `get_with_retry(url, params, tries=3)` with exponential backoff. Test it on a bad host like `https://this-does-not-exist.example` to see the retries happen.

**B6. Pydantic.** Define a `Person` model (`first: str`, `last: str`, `email: str`, `age: int`) and convert each Random User result into a `Person`. Then deliberately pass `age="old"` and read the error.

**B7. Secrets.** Create a `.env` with `MY_SECRET=hello123`. Load it with `python-dotenv` and print it. Add `.env` to `.gitignore` and confirm with `git status` that it's not listed.

**B8. API → Pandas.** Fetch 50 users, put them in a DataFrame (`pd.json_normalize(data["results"])` flattens nested JSON into columns!), and count users per country.

---

## Part C: Git exercises (do in order, in a fresh folder)

1. `git init` a folder called `git-practice`. Run `git status`.
2. Create `.gitignore` with `.env` and `__pycache__/`. Create `hello.py`. Commit both with a good message.
3. Edit `hello.py`. Run `git diff` and read the output. Commit.
4. Run `git log --oneline`. How many commits?
5. Create a branch `feature-greeting`, change the greeting, commit.
6. Switch back to `main`. Is your change there? (It shouldn't be.) Merge the branch: `git merge feature-greeting`.
7. **Make a conflict on purpose:** create branch `a`, change line 1, commit. Switch to `main`, change the same line differently, commit. `git merge a`. Resolve it.
8. Create a GitHub repo and push. Open it in the browser.
9. On GitHub, edit the README in the browser and commit there. Back on your computer, `git pull`.
10. Make a branch, push it, open a Pull Request on GitHub, and merge it.

---

## Part D: Mini-project: "Country Explorer" CLI (60–90 min)

Build `country.py`:

1. Ask the user for a country name.
2. Call `https://restcountries.com/v3.1/name/{name}`.
3. Validate the parts you need with Pydantic (official name, capital, population, region, currencies, languages).
4. Print a neat summary. Handle 404 (country not found) gracefully.
5. Save every lookup to `history.json` (append to a list).
6. Command `history` shows past lookups as a Pandas table.
7. Put it on GitHub with a README (what it does, how to run, example output) and a `.gitignore`. At least 5 meaningful commits.

**Rubric:**

| Criterion | ✓ |
|---|---|
| Uses `timeout` and checks status | |
| Handles not-found and network errors | |
| Validates with Pydantic | |
| Reads/writes JSON file correctly | |
| README explains how to run | |
| ≥ 5 commits with clear messages | |
| No secrets or `.venv` in the repo | |

---

## Part E: Quiz (25 minutes)

1. What is an API, most simply?
   a) A website b) A database c) A programming language d) A menu of requests one program can make to another

2. Which HTTP method is typically used to send a prompt to an AI model?
   a) DELETE b) GET c) POST d) HEAD

3. A response of **401** means:
   a) Unauthorized: missing/wrong key b) Not found c) Success d) Server crashed

4. A response of **429** means:
   a) Wrong URL b) Too many requests: slow down c) Created d) Bad JSON

5. In `https://api.x.com/v1/search?q=cats&limit=5`, what are `q` and `limit`?
   a) Query parameters b) Headers c) Endpoints d) Status codes

6. Where should your API key be stored?
   a) In the code b) In an environment variable / `.env` (git-ignored) c) In the README d) In a commit message

7. JSON `null` becomes what in Python?
   a) 0 b) False c) None d) ""

8. `json.loads` converts:
   a) A dict to a string b) A file to dict c) A dict to a file d) A JSON string to Python objects

9. What does `resp.raise_for_status()` do?
   a) Converts JSON b) Raises an error if status is 4xx/5xx c) Prints the status d) Retries

10. Exponential backoff means:
    a) Wait longer each retry (1s, 2s, 4s…) b) Give up immediately c) Retry instantly forever d) Send requests in parallel

11. What is an SDK?
    a) A key b) A status code c) A company's package that wraps its API in friendly functions d) A Git command

12. Correct order to save a change to GitHub:
    a) commit → add → push b) push → add → commit c) add → push → commit d) add → commit → push

13. What belongs in `.gitignore`?
    a) `.env` and `.venv/` b) Your main code c) pyproject.toml d) README.md

14. You accidentally pushed a real API key. Best action?
    a) Make the repo private b) Delete the line and commit c) Ignore it d) Revoke the key immediately and create a new one

15. A pull request is:
    a) A conflict b) An HTTP GET c) A request to merge a branch, usually with review d) Downloading code

**Short answer.**

16. Explain request, response, headers and body using the restaurant analogy.
17. Why does Pydantic validation matter when working with APIs?
18. What's the difference between Git and GitHub?
19. Describe what a merge conflict is and how to resolve one.
20. What are the 5 things to look for when reading new API docs?

---

## Answer Key

### Part A

**A1.** 1 ✅ valid. 2 ❌ single quotes not allowed. 3 ❌ must be lowercase `true`. 4 ❌ trailing comma not allowed. 5 ✅ valid.

**A2.**
```python
data["user"]["langs"][1]                     # "sql"
data["user"]["address"]["city"]              # "Pune"
len(data["user"]["langs"])                   # 2
data["user"].get("phone", "n/a")             # "n/a"
```

**A3.**
```python
import json
original = {"name": "Asha", "skills": ["python", "ai"], "active": True}
with open("user.json", "w") as f:
    json.dump(original, f, indent=2)
with open("user.json") as f:
    loaded = json.load(f)
print(loaded == original)    # True
```

### Part B

```python
import os, time, json, requests
import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

# B1
r = requests.get("https://randomuser.me/api/", params={"results": 5}, timeout=10)
print(r.status_code)
for p in r.json()["results"]:
    print(p["name"]["first"], p["name"]["last"], "|", p["location"]["country"], "|", p["email"])

# B2
cities = {"Pune": (18.52, 73.86), "Tokyo": (35.68, 139.69), "Paris": (48.86, 2.35)}
rows = []
for c, (lat, lon) in cities.items():
    d = requests.get("https://api.open-meteo.com/v1/forecast",
                     params={"latitude": lat, "longitude": lon, "current": "temperature_2m"},
                     timeout=10).json()
    rows.append({"city": c, "temp": d["current"]["temperature_2m"]})
print(pd.DataFrame(rows).sort_values("temp", ascending=False))

# B3
r = requests.get("https://jsonplaceholder.typicode.com/posts/99999", timeout=10)
if r.status_code == 404:
    print("That post doesn't exist.")     # status is 404

# B4
r = requests.post("https://jsonplaceholder.typicode.com/posts",
                  json={"title": "My first post", "body": "Learning APIs", "userId": 1},
                  timeout=10)
print(r.status_code, r.json())          # 201 {... 'id': 101}

# B5
def get_with_retry(url, params=None, tries=3):
    for attempt in range(tries):
        try:
            r = requests.get(url, params=params, timeout=5)
            if r.status_code in (429, 500, 502, 503):
                raise requests.HTTPError(str(r.status_code))
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            if attempt == tries - 1:
                raise
            wait = 2 ** attempt
            print(f"failed ({type(e).__name__}), waiting {wait}s")
            time.sleep(wait)

# B6
class Person(BaseModel):
    first: str
    last: str
    email: str
    age: int

people = [Person(first=p["name"]["first"], last=p["name"]["last"],
                 email=p["email"], age=p["dob"]["age"])
          for p in requests.get("https://randomuser.me/api/?results=5", timeout=10).json()["results"]]
try:
    Person(first="A", last="B", email="x@y.z", age="old")
except ValidationError as e:
    print(e)     # "Input should be a valid integer"

# B7
load_dotenv()
print(os.getenv("MY_SECRET"))     # hello123

# B8
data = requests.get("https://randomuser.me/api/?results=50", timeout=10).json()
df = pd.json_normalize(data["results"])
print(df["location.country"].value_counts())
```

### Part C: notes

- Step 4: 2 commits (if you did steps 2 and 3).
- Step 6: no, branches are separate until merged.
- Step 7: open the file, find `<<<<<<< HEAD … ======= … >>>>>>> a`, keep the line you want, delete all three marker lines, `git add hello.py`, `git commit`.

### Part E: Quiz answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | d | 6 | b | 11 | c |
| 2 | c | 7 | c | 12 | d |
| 3 | a | 8 | d | 13 | a |
| 4 | b | 9 | b | 14 | d |
| 5 | a | 10 | a | 15 | c |

**16.** The request is your order to the waiter: the method/URL is *what* you want and *from which counter*, the headers are extra notes on the order slip (who you are, which format you want), and the body is the details of your order. The response is what the waiter brings back: a status (did they have it?) and the food (data, usually JSON).

**17.** APIs can change, return missing fields or unexpected types. Validation catches that immediately with a clear error at the boundary, instead of a confusing crash much later in your code. It also documents what shape you expect.

**18.** Git is the version-control tool that runs on your computer and stores your project's history. GitHub is a website (one of several) that hosts Git repositories online for backup, sharing and collaboration.

**19.** A conflict happens when two branches changed the same lines differently and Git can't decide which to keep. Open the file, choose the correct content between the `<<<<<<<`, `=======`, `>>>>>>>` markers, delete the markers, then `git add` and `git commit`.

**20.** Base URL, authentication method, endpoints and parameters, example request/response, rate limits and error codes.

**Scoring:** out of 25. ≥ 21 move on.
