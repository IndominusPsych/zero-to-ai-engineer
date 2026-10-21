# Lesson 01: Python Fundamentals

*Month 1, Week 1. Reading time: about 60–75 minutes. Then type every example yourself.*

---

## 🛠️ Setup for this lesson

| You need | Why | How to get it |
|---|---|---|
| **VS Code** + the *Python* extension | Where you write and run code | code.visualstudio.com (Setup Guide Step 1) |
| **uv** | Installs Python and packages, makes project folders (explained in Section 2.2) | Setup Guide Step 2 |
| **Python 3.14** (3.13 is fine too) | The language itself | `uv python install 3.14` (Step 3) |
| A terminal | Where you type commands | Terminal (Mac), PowerShell (Windows): Step 0 |

**Install:**

```bash
# 1. Install uv (pick your system)
curl -LsSf https://astral.sh/uv/install.sh | sh                                   # macOS / Linux
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"   # Windows
# 2. Close the terminal, open a new one, then:
uv python install 3.14
# 3. Make your course folder and this lesson's project
mkdir -p ~/ai-engineer-projects && cd ~/ai-engineer-projects
uv init python_practice && cd python_practice
code .
```

**Check it works:**

```bash
uv --version          # uv 0.12 or newer
uv run python --version  # Python 3.14.x (or 3.13.x)
echo 'print("Hello, I am ready!")' > hello.py
uv run hello.py       # prints: Hello, I am ready!
```

Don't worry if words like *package* or *environment* are new: Section 2.2 explains them. For now just follow the steps. No accounts or API keys are needed this month except a free GitHub account in Lesson 03. **On Windows:** create `hello.py` in VS Code (File → New File) instead of using `echo`; see Setup Guide Step 0.

Stuck? See the step-by-step instructions and the troubleshooting table in [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md).

---

## 1. The big picture

### What is this, in simple words?

A computer is extremely fast and extremely obedient, but it doesn't understand English. It only does exactly what it's told, one tiny step at a time. To tell it what to do, we write instructions in a **programming language**: a language with strict rules that both humans and computers can read.

**Python** is one of those languages. It was designed to read almost like English. Here is a full Python program:

```python
print("Hello, I am learning Python!")
```

When you run it, the computer shows: `Hello, I am learning Python!`

That's it. One line. In many older languages, the same thing takes five or ten lines of strange symbols.

### Which field does it belong to?

Python belongs to **software development** (making programs). But it has become *the* language of **data science** and **artificial intelligence (AI)**. AI simply means computer systems that do things we'd normally call "intelligent": understanding language, recognising pictures, making predictions.

### Why does it matter for you?

Almost every AI tool you'll use in this course (data tools, machine-learning libraries, large language models, AI agents) is used *through* Python. Think of Python as the steering wheel. The AI models are the engine. You need the steering wheel first.

| Reason Python dominates AI | What it means for you |
|---|---|
| Easy to read | You learn faster and make fewer mistakes |
| Huge collection of free add-ons | Someone has already written most of the hard parts |
| Every AI company supports it first | Tutorials, examples and help are everywhere |

> **In simple words:** Python is a beginner-friendly language for giving instructions to a computer. It's the main language of AI, so it's the first thing you learn.

---

## 2. Core concepts

We'll learn the ideas one at a time. Each one uses only ideas already explained.

### 2.1 Programs, running, and the interpreter

A **program** is a text file full of instructions. Python programs end with `.py`, like `hello.py`.

To **run** a program means to ask the computer to carry out the instructions. A program called the **Python interpreter** does this. It reads your file from top to bottom, line by line, and does what each line says.

Analogy: your `.py` file is a recipe. The interpreter is the cook who reads it and actually cooks.

You run a file by typing this in the **terminal** (a text window where you type commands to your computer; on Mac it's the "Terminal" app):

```bash
python hello.py
```

(On some computers it's `python3` instead of `python`.)

### 2.2 Setting up a project the modern way: virtual environments and uv

Soon you'll install **packages**: ready-made bundles of Python code that other people wrote, like NumPy or Pandas (Lesson 02). Different projects may need different versions of the same package. If you install everything into one place, things clash.

A **virtual environment** solves this. It's a private box of packages for one project only. Analogy: each project gets its own toolbox, so borrowing a hammer for one job never breaks another.

**uv** is a popular modern tool that creates these boxes and installs packages, very fast. In 2026 it's the common recommendation for new projects. (The older way, `python -m venv` plus `pip install`, still works and you'll see it in lots of tutorials.)

```bash
# one-time: install uv (see docs.astral.sh/uv for your system)
uv init my_first_project     # make a new project folder
cd my_first_project
uv add requests              # install a package into this project's private box
uv run hello.py              # run a file using this project's box
```

| Old way | uv way | What it does |
|---|---|---|
| `python -m venv .venv` | `uv init` / `uv venv` | Create the private box |
| `pip install requests` | `uv add requests` | Install a package |
| `python file.py` (after activating) | `uv run file.py` | Run using the box |

### 2.3 Values and data types

Everything a program works with is a **value**: a piece of data. Every value has a **type**, which tells Python what kind of thing it is and what you can do with it.

| Type | Python name | Examples | Think of it as |
|---|---|---|---|
| Whole number | `int` (integer) | `7`, `-3`, `2026` | Counting things |
| Decimal number | `float` | `3.14`, `0.5`, `-2.0` | Measuring things |
| Text | `str` (string) | `"hello"`, `'AI'` | Words in quotes |
| True/False | `bool` (boolean) | `True`, `False` | A light switch |
| Nothing | `NoneType` | `None` | An empty box |

A **string** is text inside quotes. It's called a "string" because it's a string of characters (letters, digits, symbols) lined up like beads.

You can ask Python for a value's type:

```python
print(type(42))        # <class 'int'>
print(type("42"))      # <class 'str'>   ← quotes make it text!
```

That last line matters: `42` is a number, but `"42"` is text that happens to look like a number. You can do maths with the first, not the second.

### 2.4 Variables

A **variable** is a name that points to a value. Analogy: a label stuck on a box. The box holds the value; the label lets you find it later.

```python
name = "Asha"
age = 21
height_m = 1.65
is_student = True

print(name, "is", age)     # Asha is 21
```

The `=` sign here does **not** mean "equals" like in maths. It means **"put the value on the right into the box named on the left."** That's why this works:

```python
score = 10
score = score + 5    # take current score (10), add 5, store back → 15
```

Naming rules: use letters, digits and underscores, don't start with a digit, no spaces. Python style is `snake_case` (lowercase words joined by underscores): `user_name`, not `UserName`.

### 2.5 Operators: doing things with values

**Operators** are symbols that combine values.

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | add (or join text) | `3 + 2` / `"AI" + "!"` | `5` / `"AI!"` |
| `-` | subtract | `10 - 4` | `6` |
| `*` | multiply | `3 * 4` | `12` |
| `/` | divide (always gives a float) | `7 / 2` | `3.5` |
| `//` | whole-number divide | `7 // 2` | `3` |
| `%` | remainder ("modulo") | `7 % 2` | `1` |
| `**` | power | `2 ** 3` | `8` |

**Comparison operators** ask a question and answer with `True` or `False`:

| Operator | Question | Example | Result |
|---|---|---|---|
| `==` | equal? (note: two `=`) | `5 == 5` | `True` |
| `!=` | not equal? | `5 != 3` | `True` |
| `>` `<` | bigger / smaller? | `3 > 10` | `False` |
| `>=` `<=` | bigger-or-equal / smaller-or-equal? | `5 >= 5` | `True` |

**Logical operators** combine True/False answers: `and` (both must be true), `or` (at least one), `not` (flip it).

```python
age = 20
has_ticket = True
print(age >= 18 and has_ticket)   # True
```

### 2.6 Input, output and f-strings

`print()` shows things. `input()` asks the user to type something, and always gives back a **string**.

```python
name = input("What's your name? ")
print(f"Nice to meet you, {name}!")
```

That `f"..."` is an **f-string** (formatted string). Anything inside `{ }` gets replaced by its value. It's the cleanest way to build text from variables.

Because `input()` gives text, convert it if you need a number. This is called **type conversion**:

```python
age_text = input("Age? ")     # e.g. "21" (text)
age = int(age_text)           # 21 (number)
print(f"Next year you'll be {age + 1}")
```

Converters: `int()`, `float()`, `str()`, `bool()`.

### 2.7 Comments

A **comment** is a note for humans. Python ignores everything after `#` on a line.

```python
# Calculate the total price including 18% tax
total = price * 1.18
```

### 2.8 Making decisions: if / elif / else

Programs often need to choose. An **if statement** runs some code only when a condition is True.

```python
temperature = 31

if temperature > 30:
    print("Hot! Drink water.")
elif temperature > 15:
    print("Nice weather.")
else:
    print("Bring a jacket.")
```

Two crucial rules:

1. The line ends with a colon `:`.
2. The code that "belongs" to the if is **indented** (pushed right by 4 spaces). In Python, **indentation is not decoration, it's meaning.** It's how Python knows which lines are inside the if.

`elif` means "else if": check another condition. `else` catches everything left.

### 2.9 Collections: holding many values

One variable usually holds one value. **Collections** hold many. There are four main ones.

**Lists:** an ordered, changeable row of items, in square brackets.

```python
fruits = ["apple", "banana", "mango"]
print(fruits[0])        # apple   ← counting starts at 0!
print(fruits[-1])       # mango   ← negative counts from the end
fruits.append("kiwi")   # add to the end
print(len(fruits))      # 4       ← len() = how many items
```

The position number is called the **index**. Python starts counting at **0**. This trips up every beginner exactly once.

**Slicing** takes a piece of a list (or string): `fruits[1:3]` gives items at index 1 and 2 (the end number is *not* included).

**Dictionaries ("dicts"):** a collection of **key → value** pairs, in curly braces. Analogy: a real dictionary, where you look up a word (the key) to get its meaning (the value).

```python
student = {"name": "Asha", "age": 21, "course": "AI"}
print(student["name"])           # Asha
student["age"] = 22              # change a value
student["city"] = "Pune"         # add a new pair
print(student.get("phone", "unknown"))   # safe lookup with a default
```

Dicts are everywhere in AI work. When we talk to AI services in Lesson 03 and Month 2, the data comes back shaped exactly like dicts.

**Tuples:** like lists but can't be changed after creation. Round brackets: `point = (3, 4)`. Use them for things that belong together and shouldn't change.

**Sets:** an unordered bag of *unique* items: `{"red", "blue", "red"}` becomes `{"red", "blue"}`. Great for removing duplicates.

| Collection | Brackets | Ordered? | Changeable? | Duplicates? | Typical use |
|---|---|---|---|---|---|
| list | `[ ]` | Yes | Yes | Yes | A row of things |
| dict | `{k: v}` | Yes (keeps insert order) | Yes | Keys unique | Look things up by name |
| tuple | `( )` | Yes | **No** | Yes | Fixed groups, like (x, y) |
| set | `{ }` | No | Yes | **No** | Unique items |

### 2.10 Loops: repeating work

A **loop** repeats code. The **for loop** goes through each item in a collection:

```python
for fruit in fruits:
    print(f"I like {fruit}")
```

Read it as: "for each `fruit` in `fruits`, do the indented lines."

`range(n)` produces the numbers 0 up to (not including) n, handy for counting:

```python
for i in range(3):
    print(i)       # 0, 1, 2
```

Looping over a dict:

```python
for key, value in student.items():
    print(key, "→", value)
```

The **while loop** repeats *as long as* a condition is True:

```python
count = 3
while count > 0:
    print(count)
    count = count - 1
print("Lift off!")
```

Be careful: if the condition never becomes False, the loop runs forever (an **infinite loop**). Press `Ctrl + C` in the terminal to stop it.

`break` exits a loop early; `continue` skips to the next round.

### 2.11 List comprehensions (a shortcut)

A very common pattern is "make a new list by transforming another list." Python has a one-line shortcut called a **list comprehension**:

```python
numbers = [1, 2, 3, 4, 5]
squares = [n * n for n in numbers]              # [1, 4, 9, 16, 25]
evens   = [n for n in numbers if n % 2 == 0]    # [2, 4]
```

Read it as: "give me `n * n` for each `n` in `numbers`."

### 2.12 Functions: reusable recipes

A **function** is a named block of code you can run whenever you want. You've already used some built-in functions: `print()`, `len()`, `type()`. Now you'll make your own.

```python
def greet(name):
    return f"Hello, {name}!"

message = greet("Asha")
print(message)     # Hello, Asha!
```

Parts:

- `def` = "define a function".
- `greet` = its name.
- `name` = a **parameter**: a placeholder for the input.
- `"Asha"` = the **argument**: the actual value you pass in when you **call** (use) the function.
- `return` = hand a result back to whoever called it.

Analogy: a function is a vending machine. You put something in (arguments), it does work inside, and something comes out (the return value).

**Default values** and **keyword arguments**:

```python
def price_with_tax(price, tax_rate=0.18):
    return price * (1 + tax_rate)

price_with_tax(100)                 # 118.0 (uses default 0.18)
price_with_tax(100, tax_rate=0.05)  # 105.0 (keyword argument)
```

**Type hints** are optional labels saying what types a function expects and returns. Python doesn't enforce them, but they make code easier to read, and AI libraries use them heavily (you'll see this with tool calling in Month 3):

```python
def price_with_tax(price: float, tax_rate: float = 0.18) -> float:
    return price * (1 + tax_rate)
```

**Docstrings** are a description string as the first line of a function:

```python
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b
```

**Scope:** a variable made *inside* a function only exists inside it. Think of the function as a room. What's made in the room stays in the room.

### 2.13 Errors and exceptions

When something goes wrong while running, Python stops and shows an **error** (formally, an **exception**). The message looks scary but is actually helpful. **Read the last line first.**

```
Traceback (most recent call last):
  File "app.py", line 3, in <module>
    print(10 / 0)
ZeroDivisionError: division by zero
```

The **traceback** is the trail showing where it happened. The last line says *what*: dividing by zero.

| Common error | What it usually means |
|---|---|
| `SyntaxError` | You broke a grammar rule: missing `:`, bracket or quote |
| `IndentationError` | Spaces at the start of a line are wrong |
| `NameError` | You used a variable name that doesn't exist (often a typo) |
| `TypeError` | Wrong type, e.g. `"5" + 3` |
| `ValueError` | Right type, bad value, e.g. `int("hello")` |
| `KeyError` | Dict key doesn't exist |
| `IndexError` | List position doesn't exist |
| `FileNotFoundError` | The file path is wrong |

You can **catch** expected errors with `try / except`, so the program doesn't crash:

```python
try:
    age = int(input("Age? "))
except ValueError:
    print("Please type a number.")
```

### 2.14 Files

Programs often read and write files. The safe pattern uses `with`, which automatically closes the file when done:

```python
# write
with open("notes.txt", "w") as f:
    f.write("Learn Python\n")

# read
with open("notes.txt", "r") as f:
    content = f.read()
print(content)
```

Modes: `"r"` read, `"w"` write (erases old content!), `"a"` append (add to the end).

### 2.15 Modules and imports

A **module** is a `.py` file of code you can reuse. `import` brings it in. Python comes with a big **standard library** of modules built in:

```python
import math
print(math.sqrt(16))          # 4.0

from datetime import date
print(date.today())

import random
print(random.choice(["rock", "paper", "scissors"]))
```

Packages you install (with `uv add`) are imported the same way. A **library** is a general word for a collection of reusable code (one or many packages).

### 2.16 Classes and objects (a gentle first look)

So far, data (variables) and actions (functions) have been separate. A **class** bundles them together. It's a blueprint. An **object** is one thing built from that blueprint.

Analogy: "Car" is a blueprint (class). *Your* red car is one object. Every car has data (colour, fuel) and actions (drive, refuel).

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner          # data stored on the object = "attribute"
        self.balance = balance

    def deposit(self, amount: float):   # function inside a class = "method"
        self.balance += amount

acct = BankAccount("Asha", 100)
acct.deposit(50)
print(acct.balance)     # 150
```

- `__init__` runs automatically when you create an object. It sets up the starting data.
- `self` means "this particular object."
- `+=` is shorthand: `a += 5` is the same as `a = a + 5`.

You don't need to master classes now. But you'll *use* objects constantly: a Pandas table, an AI client, an agent: all are objects with methods you call using a dot, like `acct.deposit(50)`.

> **In simple words:** A program is a recipe the interpreter follows. You store values (numbers, text, True/False) in named variables, group them in lists and dicts, make decisions with `if`, repeat with loops, package reusable steps as functions, handle problems with `try/except`, read files with `with open`, borrow code with `import`, and bundle data plus actions in classes.

---

## 3. How it works: one real example, start to finish

Let's build something real: an **expense tracker**. You'll see how all the concepts click together. We'll grow it step by step, the way real programmers work.

**The goal:** read a list of expenses from a file, total them by category, and warn if you've overspent.

### Step 1: Decide what the data looks like

Each expense has a description, a category, and an amount. A dict fits perfectly. Many expenses → a list of dicts.

```python
expenses = [
    {"item": "coffee",     "category": "food",      "amount": 3.50},
    {"item": "bus ticket", "category": "transport", "amount": 2.00},
    {"item": "lunch",      "category": "food",      "amount": 8.25},
    {"item": "book",       "category": "education", "amount": 15.00},
]
```

This "list of dicts" shape is the single most common data shape you'll see in AI work.

### Step 2: Total everything with a loop

```python
total = 0
for e in expenses:
    total += e["amount"]
print(f"Total spent: ${total:.2f}")     # Total spent: $28.75
```

`:.2f` inside the f-string means "show 2 decimal places."

### Step 3: Group by category using a dict

```python
by_category = {}
for e in expenses:
    cat = e["category"]
    by_category[cat] = by_category.get(cat, 0) + e["amount"]

print(by_category)
# {'food': 11.75, 'transport': 2.0, 'education': 15.0}
```

The trick: `.get(cat, 0)` returns the current total, or 0 if this category is new.

### Step 4: Wrap the logic in functions

Functions make code reusable and testable.

```python
def total_spent(expenses: list[dict]) -> float:
    """Return the sum of all expense amounts."""
    return sum(e["amount"] for e in expenses)

def totals_by_category(expenses: list[dict]) -> dict[str, float]:
    """Return a dict of category -> total amount."""
    result = {}
    for e in expenses:
        result[e["category"]] = result.get(e["category"], 0) + e["amount"]
    return result
```

### Step 5: Add a decision

```python
BUDGET = {"food": 10, "transport": 20, "education": 50}

def check_budget(totals: dict[str, float]) -> None:
    for cat, spent in totals.items():
        limit = BUDGET.get(cat)
        if limit is None:
            print(f"⚠️  No budget set for {cat}")
        elif spent > limit:
            print(f"🔴 {cat}: spent ${spent:.2f}, over the ${limit} budget!")
        else:
            print(f"🟢 {cat}: ${spent:.2f} of ${limit}")
```

(Writing a variable name in ALL CAPS, like `BUDGET`, is a convention meaning "this is a fixed setting; don't change it.")

### Step 6: Read the data from a file, safely

Real data lives in files. Create `expenses.csv`. **CSV** means "comma-separated values": a plain text table where each line is a row and commas separate the columns.

```
item,category,amount
coffee,food,3.50
bus ticket,transport,2.00
lunch,food,8.25
book,education,15.00
```

Read it with the standard library's `csv` module:

```python
import csv

def load_expenses(path: str) -> list[dict]:
    expenses = []
    try:
        with open(path) as f:
            for row in csv.DictReader(f):       # each row becomes a dict
                row["amount"] = float(row["amount"])   # text → number
                expenses.append(row)
    except FileNotFoundError:
        print(f"Couldn't find {path}")
    return expenses
```

### Step 7: Put it all together

```python
def main():
    expenses = load_expenses("expenses.csv")
    if not expenses:
        return
    print(f"Total: ${total_spent(expenses):.2f}")
    check_budget(totals_by_category(expenses))

if __name__ == "__main__":
    main()
```

That last `if __name__ == "__main__":` line means "only run `main()` when this file is run directly, not when another file imports it." You'll see it at the bottom of almost every Python script.

**Output:**

```
Total: $28.75
🔴 food: spent $11.75, over the $10 budget!
🟢 transport: $2.00 of $20
🟢 education: $15.00 of $50
```

### What just happened (diagram)

```
expenses.csv ──▶ load_expenses() ──▶ list of dicts ──┬──▶ total_spent() ──▶ print total
   (file)          (files, try,        (data)        │
                    loops, types)                    └──▶ totals_by_category() ──▶ check_budget()
                                                            (dict grouping)        (if/elif/else)
```

Every concept from Section 2 appeared: variables, types, conversion, lists, dicts, loops, functions, type hints, `if`, files, `try/except`, `import`, f-strings. In Lesson 02 you'll do the same job in 3 lines with Pandas, and you'll appreciate *why* Pandas exists.

> **In simple words:** Real programs are built in small steps: pick a data shape, process it with loops, wrap the logic in functions, add decisions, then load real data from a file. Grow it piece by piece, running it after each step.

---

## 4. Key terms (in the order you met them)

| Term | Plain meaning |
|---|---|
| **Programming language** | A strict language for writing instructions a computer can follow. |
| **Python** | A readable, beginner-friendly programming language; the main language of AI. |
| **Artificial intelligence (AI)** | Computer systems doing tasks we'd call "intelligent", like understanding language. |
| **Program / script** | A text file (`.py`) of instructions. |
| **Interpreter** | The program that reads your Python file and carries it out, line by line. |
| **Terminal** | A text window where you type commands to the computer. |
| **Package** | A ready-made bundle of code someone else wrote that you can install. |
| **Virtual environment** | A private box of packages for one project, so projects don't clash. |
| **uv** | A fast modern tool to create projects and environments and install packages. |
| **pip** | The older, standard tool for installing packages. |
| **Value** | A single piece of data, like `5` or `"hi"`. |
| **Data type** | The kind of value: `int`, `float`, `str`, `bool`, `None`. |
| **String** | Text inside quotes. |
| **Variable** | A name (label) that points to a value. |
| **Operator** | A symbol that combines values: `+`, `==`, `and`… |
| **f-string** | Text starting with `f` where `{variable}` gets filled in. |
| **Type conversion** | Turning one type into another, e.g. `int("5")`. |
| **Comment** | A `#` note for humans; Python ignores it. |
| **Condition / if statement** | Code that runs only when something is True. |
| **Indentation** | The spaces at the start of a line; in Python it defines which block code belongs to. |
| **List** | Ordered, changeable collection: `[1, 2, 3]`. |
| **Index** | An item's position number, starting at 0. |
| **Slicing** | Taking a piece of a list or string: `x[1:3]`. |
| **Dictionary (dict)** | Key → value lookup table: `{"name": "Asha"}`. |
| **Tuple** | Like a list but unchangeable: `(3, 4)`. |
| **Set** | Unordered collection of unique items. |
| **Loop (for / while)** | Code that repeats: for each item, or while a condition holds. |
| **List comprehension** | One-line way to build a list: `[x*2 for x in nums]`. |
| **Function** | A named, reusable block of code. |
| **Parameter / argument** | Parameter = the input's placeholder name; argument = the actual value you pass. |
| **Return value** | What a function hands back. |
| **Type hint** | An optional label showing expected types: `def f(x: int) -> str`. |
| **Docstring** | A description string at the top of a function. |
| **Scope** | Where a variable exists (e.g. only inside its function). |
| **Exception / error** | A problem that stops the program, with a named type. |
| **Traceback** | The error report showing where the problem happened. |
| **try / except** | Catch an expected error and handle it gracefully. |
| **CSV** | A plain-text table: rows on lines, columns split by commas. |
| **Module / import** | A reusable `.py` file / the command to bring it in. |
| **Standard library** | The modules that come with Python for free. |
| **Library** | General word for a reusable collection of code. |
| **Class / object** | Blueprint / a thing built from the blueprint. |
| **Attribute / method** | Data stored on an object / a function belonging to an object. |

> **In simple words:** These ~40 words are the vocabulary of every Python conversation. If one feels fuzzy, go back to its section.

---

## 5. The people involved

| Who | What they do | What Python means for them day to day |
|---|---|---|
| **You, the learner** | Learn by writing small programs | Python is your daily tool: you'll write some every single day of this course. |
| **Software engineer / developer** | Builds apps and services | Writes Python for web back-ends, scripts and automation; cares about clean, tested code. |
| **Data analyst** | Answers business questions with data | Uses Python (with Pandas, Lesson 02) instead of, or alongside, Excel. |
| **Data scientist / ML engineer** | Builds models that learn from data | Uses Python libraries like scikit-learn and PyTorch to train and test models. |
| **AI engineer** (your target role) | Builds products on top of AI models (chatbots, RAG apps, agents) | Writes Python to call AI APIs, connect data, and wire up tools. This is the job Months 2–3 prepare you for. |
| **Python core developers** | Volunteers who maintain the language itself | Release a new version every October (3.14 in Oct 2025). |
| **Package authors / open-source community** | Write the free packages everyone uses | Their work is why you rarely start from zero. |
| **The Python Software Foundation (PSF)** | Non-profit that looks after Python | Runs python.org and PyPI (the Python Package Index: the online store where packages live). |

> **In simple words:** Everyone from analysts to AI engineers uses Python daily. Volunteers and a non-profit maintain it, and a huge community shares free packages through PyPI.

---

## 6. Common misconceptions and beginner mistakes

| Mistake / myth | Reality / fix |
|---|---|
| "I must memorise everything." | No professional does. You learn the *ideas*; you look up exact names constantly. |
| "I'll learn by watching videos." | You learn by **typing and breaking** code. Watching feels like progress but isn't. |
| Copy-pasting examples | Type them by hand. Your fingers learn the grammar. |
| Mixing tabs and spaces, or wrong indentation | Use 4 spaces. VS Code does it for you. |
| `if x = 5:` | Use `==` to compare. A single `=` stores a value. |
| Forgetting `input()` returns text | Convert: `int(input(...))`. |
| Starting to count at 1 | Indexes start at 0. The last item is `[-1]` or `[len(x) - 1]`. |
| `"Age: " + 21` → TypeError | Use an f-string: `f"Age: {21}"`. |
| Fearing error messages | Errors are the computer *helping* you. Read the last line first. |
| Writing 100 lines, then running | Run after every few lines. Small steps, fast feedback. |
| Naming a file `random.py` or `pandas.py` | It hides the real module. Never name files after packages you import. |
| Installing packages globally | Use a project environment (`uv init`, `uv add`). |
| "Python is slow, so it's bad for AI." | The heavy maths runs in fast code underneath (C, CUDA). Python is the steering wheel. |
| Following a tutorial using Python 2 (`print "hi"`) | Python 2 is dead since 2020. Always use Python 3. |

> **In simple words:** Type code yourself, run it often, read errors calmly from the bottom, and watch out for `=` vs `==`, counting from 0, and `input()` giving text.

---

## 7. One-page recap

### The 10 things to remember

1. **Python is the steering wheel of AI.** You'll use it to drive every tool in this course.
2. **The interpreter reads your file top to bottom** and does each line.
3. **Use a project environment** (`uv init` / `uv add`) so packages don't clash.
4. **Every value has a type:** `int`, `float`, `str`, `bool`, `None`. `"5"` is not `5`.
5. **`=` stores, `==` compares.**
6. **Indentation is meaning.** A colon `:` starts a block; indented lines are inside it.
7. **Lists are rows (index from 0); dicts are lookups (key → value).** A list of dicts is the most common data shape in AI.
8. **Loops repeat; functions package; `return` hands back.**
9. **Errors are helpful.** Read the last line; use `try/except` for expected problems.
10. **Build in tiny steps** and run after each one.

### Cheat sheet

```python
x = 5                          # variable
name = f"Hi {x}"               # f-string
nums = [1, 2, 3]; nums[0]      # list, index 0
d = {"a": 1}; d["a"]           # dict lookup
if x > 3: ...                  # decision
for n in nums: ...             # loop
def f(a: int) -> int: return a # function
try: ... except ValueError: ...# handle errors
with open("f.txt") as fh: ...  # files
import math                    # modules
```

### What to learn next

➡️ **Lesson 02: NumPy, Pandas & data handling.** You just added up expenses with a loop. Next you'll learn the tools that do that across millions of rows in one line, which is exactly what AI work needs.

Now open `practice_and_test.md` in this folder.
