# Practice & Test 01: Python Fundamentals

> **🛠️ Before you start:** you need uv and Python 3.14 (no extra packages). Install them with the commands in the **🛠️ Setup for this lesson** box at the top of [`lesson.md`](lesson.md) (full help: [`00_SETUP_Install_Guide.md`](../../00_SETUP_Install_Guide.md)). Quick check:
>
> ```bash
> uv run python --version
> ```

**How to use this file:** Do Parts A–C with your editor open. Then take the Quiz (Part D) with the lesson closed. Only then check the Answer Key at the bottom.

Setup once:

```bash
uv init python_practice && cd python_practice
# create files like ex1.py and run with: uv run ex1.py
```

---

## Part A: Warm-up: predict the output (no computer!)

Write down what each prints *before* running it. Then run to check.

```python
# A1
x = 7
x = x * 2
print(x)

# A2
print(type("3.5"))

# A3
print(10 / 4, 10 // 4, 10 % 4)

# A4
fruits = ["apple", "banana", "cherry", "date"]
print(fruits[1], fruits[-1], fruits[1:3])

# A5
d = {"a": 1, "b": 2}
d["c"] = d["a"] + d["b"]
print(d)

# A6
total = 0
for i in range(1, 5):
    total += i
print(total)

# A7
print([n * 10 for n in range(4) if n != 2])

# A8
def f(a, b=3):
    return a * b
print(f(2), f(2, 5))

# A9
print("AI" * 3)

# A10
print(len({"red", "blue", "red", "green"}))
```

---

## Part B: Hands-on exercises (increasing difficulty)

**B1. Greeting.** Ask the user for their name and birth year. Print `Hi <name>, you are about <age> years old.` (use 2026).

**B2. Even or odd.** Write a function `is_even(n: int) -> bool`. Then print whether each number from 1 to 10 is even or odd.

**B3. FizzBuzz** (the classic interview question). Print numbers 1–30, but print `Fizz` for multiples of 3, `Buzz` for multiples of 5, and `FizzBuzz` for multiples of both.

**B4. Word counter.** Write `count_words(text: str) -> dict[str, int]` that returns how many times each word appears (lowercase, ignore punctuation `.,!?`). Test it on: `"The cat sat. The cat ran! A dog sat?"`

**B5. Safe number input.** Keep asking the user for a number until they type a valid one (use `while True`, `try/except ValueError`, and `break`).

**B6. Grade book.** Given:

```python
students = [
    {"name": "Asha",  "scores": [88, 92, 79]},
    {"name": "Ravi",  "scores": [65, 70, 58]},
    {"name": "Meera", "scores": [95, 98, 100]},
]
```

Write functions to (a) compute each student's average, (b) give a letter grade (A ≥ 90, B ≥ 75, C ≥ 60, else F), (c) print a neat report, (d) find the top student.

**B7. Files.** Write the grade report from B6 into `report.txt`, then read it back and print how many lines it has.

**B8. Class.** Create a class `TodoList` with methods `add(task)`, `complete(task)`, `pending() -> list[str]`, and `save(path)` that writes pending tasks to a file.

---

## Part C: Mini-project: Number-guessing game (45–60 min)

Requirements:

1. The computer picks a random integer 1–100 (`import random`, `random.randint(1, 100)`).
2. The user guesses; the program says "Too high" / "Too low".
3. Invalid input (like `abc`) must not crash the game.
4. Count attempts; at the end print `You got it in N tries!`.
5. Ask "Play again? (y/n)".
6. **Stretch:** keep a best score in `best_score.txt` across runs.

**Self-check rubric:**

| Criterion | ✓ |
|---|---|
| Uses at least 2 functions | |
| Handles bad input with try/except | |
| Uses a while loop correctly (no infinite loop bug) | |
| Uses f-strings for output | |
| Has comments/docstrings | |
| Runs start to finish without errors | |

---

## Part D: Quiz (lesson closed, 25 minutes)

**Multiple choice: pick one.**

1. What does the Python interpreter do?
   a) Stores your files online b) Translates Python to English c) Installs packages d) Reads and executes your code line by line

2. What is a virtual environment?
   a) A video game b) A type of loop c) A private set of packages for one project d) A cloud computer

3. What is the type of `"42"`?
   a) str b) int c) bool d) float

4. `x = 5` means:
   a) error b) store the value 5 under the name x c) check if x is 5 d) x equals 5 forever

5. What does `7 // 2` give?
   a) 3 b) 4 c) 1 d) 3.5

6. Which compares two values for equality?
   a) `===` b) `:=` c) `==` d) `=`

7. `colors = ["red", "green", "blue"]`. What is `colors[-1]`?
   a) red b) blue c) IndexError d) green

8. What does `input()` always return?
   a) bool b) int c) whatever the user typed, auto-converted d) str

9. Which collection is best for looking up a phone number by name?
   a) set b) dict c) tuple d) list

10. What is wrong with this code?
    ```python
    if age > 18
        print("adult")
    ```
    a) Nothing b) `print` needs no brackets c) Should use `==` d) Missing colon

11. In `def greet(name):` what is `name`?
    a) A module b) An argument c) A parameter d) A return value

12. Which error do you get from `int("hello")`?
    a) ValueError b) TypeError c) KeyError d) NameError

13. Why use `with open(...) as f:`?
    a) It's required for CSV only b) It's faster c) It encrypts the file d) It automatically closes the file

14. What does `[x * 2 for x in [1, 2, 3]]` produce?
    a) 12 b) [2, 4, 6] c) [1, 2, 3, 1, 2, 3] d) Error

15. In a class, what is `self`?
    a) The current object b) A global variable c) The class name d) A keyword for loops

**Short answer (2–3 sentences each).**

16. Explain the difference between a list and a dictionary, with an example of when you'd use each.
17. You see `KeyError: 'email'`. What happened and give two ways to fix it.
18. Why does Python care about indentation when most languages don't?
19. What does `if __name__ == "__main__":` do and why is it useful?
20. Explain to a friend why `"5" + 3` fails but `int("5") + 3` works.

---

## Answer Key

### Part A

| # | Output | Why |
|---|---|---|
| A1 | `14` | 7 × 2 stored back in x |
| A2 | `<class 'str'>` | Quotes make text |
| A3 | `2.5 2 2` | true divide, whole divide, remainder |
| A4 | `banana date ['banana', 'cherry']` | index 1, last, slice 1 to 3 (3 excluded) |
| A5 | `{'a': 1, 'b': 2, 'c': 3}` | new key added |
| A6 | `10` | 1+2+3+4 (range stops before 5) |
| A7 | `[0, 10, 30]` | n = 0,1,3 (2 skipped) |
| A8 | `6 10` | default b=3, then b=5 |
| A9 | `AIAIAI` | string repetition |
| A10 | `3` | sets drop the duplicate "red" |

### Part B: model solutions

```python
# B1
name = input("Name? ")
year = int(input("Birth year? "))
print(f"Hi {name}, you are about {2026 - year} years old.")

# B2
def is_even(n: int) -> bool:
    return n % 2 == 0

for n in range(1, 11):
    print(n, "even" if is_even(n) else "odd")

# B3
for n in range(1, 31):
    if n % 15 == 0:          # check "both" FIRST
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)

# B4
def count_words(text: str) -> dict[str, int]:
    for ch in ".,!?":
        text = text.replace(ch, "")
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts

print(count_words("The cat sat. The cat ran! A dog sat?"))
# {'the': 2, 'cat': 2, 'sat': 2, 'ran': 1, 'a': 1, 'dog': 1}

# B5
while True:
    try:
        num = float(input("Enter a number: "))
        break
    except ValueError:
        print("That's not a number, try again.")
print(f"Thanks! You entered {num}")

# B6
def average(scores: list[float]) -> float:
    return sum(scores) / len(scores)

def letter(avg: float) -> str:
    if avg >= 90: return "A"
    if avg >= 75: return "B"
    if avg >= 60: return "C"
    return "F"

def report(students: list[dict]) -> list[str]:
    lines = []
    for s in students:
        avg = average(s["scores"])
        lines.append(f"{s['name']:<6} avg {avg:5.1f}  grade {letter(avg)}")
    return lines

for line in report(students):
    print(line)

top = max(students, key=lambda s: average(s["scores"]))
print("Top student:", top["name"])      # Meera
```

> `lambda s: ...` is a tiny one-line unnamed function. `max(..., key=...)` uses it to decide what to compare. You'll see `lambda` often in Pandas.

```python
# B7
with open("report.txt", "w") as f:
    for line in report(students):
        f.write(line + "\n")

with open("report.txt") as f:
    print(len(f.readlines()), "lines")   # 3 lines

# B8
class TodoList:
    def __init__(self):
        self.tasks: dict[str, bool] = {}     # task -> done?

    def add(self, task: str):
        self.tasks[task] = False

    def complete(self, task: str):
        if task in self.tasks:
            self.tasks[task] = True

    def pending(self) -> list[str]:
        return [t for t, done in self.tasks.items() if not done]

    def save(self, path: str):
        with open(path, "w") as f:
            f.write("\n".join(self.pending()))

todo = TodoList()
todo.add("learn loops"); todo.add("learn dicts")
todo.complete("learn loops")
print(todo.pending())     # ['learn dicts']
```

### Part C: reference solution

```python
import random

BEST_FILE = "best_score.txt"

def get_guess() -> int:
    while True:
        try:
            return int(input("Your guess (1-100): "))
        except ValueError:
            print("Please type a whole number.")

def load_best() -> int | None:
    try:
        with open(BEST_FILE) as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return None

def save_best(score: int):
    with open(BEST_FILE, "w") as f:
        f.write(str(score))

def play_round() -> int:
    """Play one game and return the number of attempts."""
    secret = random.randint(1, 100)
    attempts = 0
    while True:
        guess = get_guess()
        attempts += 1
        if guess > secret:
            print("Too high")
        elif guess < secret:
            print("Too low")
        else:
            print(f"You got it in {attempts} tries!")
            return attempts

def main():
    while True:
        tries = play_round()
        best = load_best()
        if best is None or tries < best:
            save_best(tries)
            print("🏆 New best score!")
        if input("Play again? (y/n) ").lower() != "y":
            break

if __name__ == "__main__":
    main()
```

### Part D: Quiz answers

| Q | Answer | Q | Answer | Q | Answer |
|---|---|---|---|---|---|
| 1 | d | 6 | c | 11 | c |
| 2 | c | 7 | b | 12 | a |
| 3 | a | 8 | d | 13 | d |
| 4 | b | 9 | b | 14 | b |
| 5 | a | 10 | d | 15 | a |

**16.** A list is an ordered row you access by position (e.g. a playlist of songs, `songs[0]`). A dict maps keys to values and you access by name (e.g. a contact book, `phones["Asha"]`). Use a list when order/position matters, a dict when you look things up by a label.

**17.** You asked a dict for the key `'email'` but it doesn't exist. Fixes: check first with `if "email" in d:`, or use `d.get("email", "default")`, or catch `KeyError` with try/except.

**18.** Python uses indentation *instead of* curly braces to show which lines belong to a block (an if, loop or function). That forces code to look the way it works, which makes it very readable, but it means wrong spaces change the meaning or cause an IndentationError.

**19.** It runs the code inside it only when the file is run directly (`python file.py`), not when another file imports it. That lets you reuse the file's functions elsewhere without accidentally running the whole program.

**20.** `"5"` is text and `3` is a number; Python won't guess whether you want to join text or add numbers, so it raises a TypeError. `int("5")` converts the text into the number 5, so adding 3 works and gives 8.

**Scoring:** 15 MCQs × 1 point + 5 short answers × 2 points = 25. **≥ 21 = move on.** 18–20 = review missed sections. < 18 = redo Section 2 and Part B.
