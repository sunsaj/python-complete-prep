from core import L, X

# ============================================================ PART 0
L(id="why-design", part="start", title="Why Do We Even Need Design?", tagline="Messy code is like a messy school bag",
body="""
### The messy school bag
Imagine your school bag with **no compartments**. Books, tiffin, pencils, sports shoes, all thrown in together. On day 1 it's fine. By month 3, your tiffin has leaked onto your maths notebook, and finding a pencil takes 5 minutes.

Code is the same. A small program can be messy and still work. But real programs **grow**: new features every week, many people editing them. Without organisation:
- changing one thing **breaks** something unrelated,
- nobody can **find** where anything is,
- **adding** a feature means editing 20 places,
- **testing** is impossible because everything is glued together.

**Software design** is about putting compartments in your bag: deciding which piece of code is responsible for what, and how the pieces talk to each other.

### Two big ideas in this tutorial
1. **SOLID principles**: 5 rules of thumb for good classes. Think of them as "good habits", like "keep your tiffin in its own box".
2. **Design patterns**: 22 famous **ready-made solutions** to problems that keep coming up. Think of them as "recipes". You don't invent a new recipe for tea every morning, you use one that works.

> Patterns were collected in a famous 1994 book by four authors (the "Gang of Four", GoF). They wrote for C++/Java. **Python makes many patterns simpler**, sometimes just a function. You'll see the "Pythonic shortcut" in every lesson.

### Words you need (2-minute refresher)
| word | meaning | school example |
|---|---|---|
| **class** | a blueprint | the "Student" form design |
| **object** | a thing made from the blueprint | Asha's filled-in form |
| **method** | something an object can do | `student.submit_homework()` |
| **inheritance** ("is a") | a child class reuses a parent | a `ClassMonitor` **is a** `Student` |
| **composition** ("has a") | an object contains another | a `School` **has** `Classrooms` |
| **interface** | a promise: "I have these methods" | anything with `.charge()` can be a charger |

If any of these feel shaky, read **chapters 08–10 (OOP from Zero)** in the main guide first.

### Interfaces in Python: ABC and Protocol
Many patterns rely on an **interface**, a "socket" that different objects can plug into:
```python
from abc import ABC, abstractmethod
from typing import Protocol

class Shape(ABC):                  # ABC: children MUST implement area()
    @abstractmethod
    def area(self) -> float: ...

class Drawable(Protocol):          # Protocol: anything with draw() fits, no inheritance needed
    def draw(self) -> str: ...
```
### How to study each lesson
Every lesson follows the same path: **story → messy code (the problem) → the pattern (the fix) → picture → when NOT to use it → Python shortcut → quick check → practice**. Do the practice. Reading about swimming won't teach you to swim!
""",
quiz=[
    ("What's the difference between a class and an object?", "A class is the **blueprint** (the form design). An object is **one actual thing** made from it (one filled-in form). One class, many objects."),
    ("'Is a' or 'has a'? A Car and its Engine.", "**Has a**: a car *has* an engine, so that's composition. A car is not a kind of engine."),
    ("Why does a pattern from a Java book often look simpler in Python?", "Python has first-class functions, duck typing, modules, decorators and dataclasses built in. Some patterns that need several classes in Java are just a function or a module in Python."),
],
exercises=[
    X("warmup-shape", "Warm-up: your first interface",
      """
Create an abstract class `Shape` with an abstract method `area()`. Then make two shapes:
- `Rectangle(w, h)` with area `w * h`,
- `Circle(r)` with area `3.14 * r * r` (use 3.14).

Finally, write `total_area(shapes)`, which adds up the areas of any list of shapes.
""",
      r'''from abc import ABC, abstractmethod

class Shape(ABC):
    pass   # add an abstract method area()

class Rectangle(Shape):
    pass

class Circle(Shape):
    pass

def total_area(shapes):
    pass
''',
      r'''from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14 * self.r * self.r

def total_area(shapes):
    return sum(s.area() for s in shapes)     # works for ANY shape: that's polymorphism
''',
      r'''
T("rectangle", lambda: Rectangle(3, 4).area(), 12)
T("circle", lambda: Circle(1).area(), 3.14)
T("total", lambda: round(total_area([Rectangle(2, 5), Circle(2)]), 2), 22.56)
def _abstract():
    try:
        Shape(); return False
    except TypeError:
        return True
C("Shape can't be created directly (it's abstract)", _abstract, "Shape() should raise TypeError: add @abstractmethod")
C("Rectangle is a Shape", lambda: issubclass(Rectangle, Shape) and issubclass(Circle, Shape))
''',
      ["Use `@abstractmethod` above `def area(self)` inside Shape.", "`total_area` can use `sum(s.area() for s in shapes)`."]),
])

# ============================================================ SOLID
L(id="srp", part="solid", title="S: Single Responsibility Principle", tagline="One class, one job",
body="""
### The story
In your school, the **canteen uncle** makes food, the **librarian** issues books, and the **PE teacher** runs sports. Imagine one person doing all three. When the library rules change, the cook has to learn them. When he's sick, there's no food, no books and no sports!

**SRP: a class should have only one reason to change.** In simple words, **one class, one job**.

### The messy code
```python
class ReportCard:
    def __init__(self, student, marks):
        self.student, self.marks = student, marks
    def average(self):                         # job 1: calculate
        return sum(self.marks) / len(self.marks)
    def to_html(self):                         # job 2: format for display
        return f"<h1>{self.student}</h1><p>{self.average():.1f}</p>"
    def save(self, path):                      # job 3: store in a file
        with open(path, "w") as f:
            f.write(self.to_html())
    def email_parents(self, address):          # job 4: send email
        ...
```
This class changes if the **grading rule** changes, if the **design** changes, if we move from **files to a database**, or if the **email provider** changes. That's four reasons to change, so it's fragile.

### The fix: one job each
```python
class ReportCard:                      # job: the data + grade calculations
    def __init__(self, student, marks):
        self.student, self.marks = student, marks
    def average(self):
        return sum(self.marks) / len(self.marks)

class HtmlFormatter:                   # job: how it looks
    def format(self, card):
        return f"<h1>{card.student}</h1><p>{card.average():.1f}</p>"

class FileSaver:                       # job: where it's stored
    def save(self, text, path):
        with open(path, "w") as f:
            f.write(text)
```
Now changing the design only touches `HtmlFormatter`. Switching to a database means replacing `FileSaver`. Each piece is also easy to **test** on its own.

### The "and" test
Describe your class in one sentence. If you need the word **"and"** ("it calculates marks **and** formats HTML **and** saves files"), it probably has too many jobs.

> **Don't overdo it:** SRP doesn't mean "one method per class". `ReportCard` can have `average()`, `highest()` and `grade()`. Those are all the same job (the maths of marks).
""",
quiz=[
    ("A `User` class validates passwords, saves to the DB, and sends welcome emails. Which SRP smell is it?", "Three reasons to change: security rules, storage, and email. Split it into `PasswordPolicy`, `UserRepository` and `WelcomeMailer`, and keep `User` as the data."),
    ("Does SRP mean every class must have one method?", "No. One **job** (one reason to change), which can involve many related methods."),
],
exercises=[
    X("srp-split", "Split the god class",
      """
`Invoice` below does three jobs. Refactor it into:
- `Invoice(items)`, which stores `items` (a list of `(name, price)` tuples) and has `total()`,
- `InvoicePrinter`, with `render(invoice)` returning exactly the same text as the old `print_text()`,
- `TaxCalculator(rate)`, with `tax(invoice)` returning `round(invoice.total() * rate, 2)`.

`Invoice` must **not** have `print_text` or `tax` methods anymore.
""",
      r'''# OLD messy version, refactor it:
class Invoice:
    def __init__(self, items, tax_rate):
        self.items, self.tax_rate = items, tax_rate
    def total(self):
        return sum(price for _, price in self.items)
    def tax(self):
        return round(self.total() * self.tax_rate, 2)
    def print_text(self):
        lines = [f"{name}: {price}" for name, price in self.items]
        return "\n".join(lines + [f"TOTAL: {self.total()}"])
''',
      r'''class Invoice:                          # job: the invoice data + its total
    def __init__(self, items):
        self.items = items
    def total(self):
        return sum(price for _, price in self.items)

class InvoicePrinter:                   # job: presentation
    def render(self, invoice):
        lines = [f"{name}: {price}" for name, price in invoice.items]
        return "\n".join(lines + [f"TOTAL: {invoice.total()}"])

class TaxCalculator:                    # job: tax rules
    def __init__(self, rate):
        self.rate = rate
    def tax(self, invoice):
        return round(invoice.total() * self.rate, 2)
''',
      r'''
_inv = lambda: Invoice([("pen", 10), ("book", 90)])
T("total", lambda: _inv().total(), 100)
T("printer", lambda: InvoicePrinter().render(_inv()), "pen: 10\nbook: 90\nTOTAL: 100")
T("tax", lambda: TaxCalculator(0.18).tax(_inv()), 18.0)
C("Invoice no longer prints or taxes", lambda: not hasattr(Invoice, "print_text") and not hasattr(Invoice, "tax"),
  "remove print_text and tax from Invoice")
''',
      ["Invoice keeps only items + total().", "Move printing into InvoicePrinter.render(invoice), which reads invoice.items."]),
])

L(id="ocp", part="solid", title="O: Open/Closed Principle", tagline="Add new things without editing old things",
body="""
### The story
Think of a **power strip** (extension board). When you buy a new gadget, you **plug it in**. You don't open the strip and rewire it! The strip is **closed** for changes but **open** for new plugs.

**OCP: code should be open for extension, closed for modification.** Add new behaviour by **adding new code**, not by editing code that already works (and is already tested).

### The messy code
```python
def calculate_fee(student_type, base):
    if student_type == "regular":
        return base
    elif student_type == "scholarship":
        return base * 0.5
    elif student_type == "staff_child":
        return base * 0.3
    # every new type = edit this function again (and risk breaking the others)
```
### The fix: a "socket" (interface) plus one class per type
```python
from abc import ABC, abstractmethod

class FeePolicy(ABC):
    @abstractmethod
    def fee(self, base): ...

class Regular(FeePolicy):
    def fee(self, base): return base

class Scholarship(FeePolicy):
    def fee(self, base): return base * 0.5

class StaffChild(FeePolicy):
    def fee(self, base): return base * 0.3

def calculate_fee(policy: FeePolicy, base):
    return policy.fee(base)          # never changes again!

# New type next year? Just ADD a class:
class SportsQuota(FeePolicy):
    def fee(self, base): return base * 0.6
```
### Python shortcut: a registry dictionary
```python
FEE_RULES = {"regular": lambda b: b, "scholarship": lambda b: b * 0.5}
FEE_RULES["sports"] = lambda b: b * 0.6        # extend without touching existing code
```
> **Spot it:** long `if/elif` chains on a "type" string, repeated in several places, are the classic OCP smell. The fix is usually **polymorphism** or a **registry**.
""",
quiz=[
    ("What does 'closed for modification' protect you from?", "Breaking code that already works and is tested. New features go into **new** code, so old features keep working."),
    ("What's the usual fix for a long if/elif chain on a type?", "Polymorphism (a class per type behind a common interface), or a dictionary registry of functions or classes."),
],
exercises=[
    X("ocp-shipping", "Make shipping costs extensible",
      """
Replace the `if/elif` with classes. Create an abstract `Shipping` with `cost(weight)`, plus:
- `Standard`: `weight * 10`
- `Express`: `weight * 20 + 50`
- `Free`: always `0`

Then `shipping_cost(method, weight)` must just call `method.cost(weight)`. Finally, **add a new** `Drone` class (`weight * 15 + 100`) **without editing** `shipping_cost`.
""",
      r'''# messy version:
# def shipping_cost(kind, weight):
#     if kind == "standard": return weight * 10
#     elif kind == "express": return weight * 20 + 50
#     elif kind == "free": return 0

from abc import ABC, abstractmethod

class Shipping(ABC):
    pass

def shipping_cost(method, weight):
    pass
''',
      r'''from abc import ABC, abstractmethod

class Shipping(ABC):
    @abstractmethod
    def cost(self, weight): ...

class Standard(Shipping):
    def cost(self, weight): return weight * 10

class Express(Shipping):
    def cost(self, weight): return weight * 20 + 50

class Free(Shipping):
    def cost(self, weight): return 0

class Drone(Shipping):                       # added later: no edits anywhere else
    def cost(self, weight): return weight * 15 + 100

def shipping_cost(method, weight):
    return method.cost(weight)
''',
      r'''
T("standard", lambda: shipping_cost(Standard(), 2), 20)
T("express", lambda: shipping_cost(Express(), 2), 90)
T("free", lambda: shipping_cost(Free(), 99), 0)
T("drone (the extension)", lambda: shipping_cost(Drone(), 2), 130)
C("all are Shipping", lambda: all(issubclass(c, Shipping) for c in (Standard, Express, Free, Drone)))
''',
      ["Each class implements cost(self, weight).", "shipping_cost is one line: return method.cost(weight)."]),
])

L(id="lsp", part="solid", title="L: Liskov Substitution Principle", tagline="A child must keep the parent's promises",
body="""
### The story
Your teacher says: _"Any student can be sent to fetch chalk from the staff room."_ If one "student" is actually a **toddler visiting for the day** who can't walk there alone, the teacher's rule breaks. If you call something a Student, it must be able to do what students do.

**LSP: if `B` is a child of `A`, you must be able to use a `B` anywhere an `A` is expected, without surprises.** (Named after computer scientist Barbara Liskov.)

### The famous broken example
```python
class Bird:
    def fly(self):
        return "flap flap"

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly!")   # breaks Bird's promise

def migrate(birds):
    for b in birds:
        b.fly()          # crashes when a Penguin is in the list
```
`Penguin` **is** a bird in biology, but **not** in this code, because this code's `Bird` promises "I can fly".

### The fix: make promises honest
```python
class Bird:
    def eat(self): return "nom"

class FlyingBird(Bird):
    def fly(self): return "flap flap"

class Sparrow(FlyingBird): ...
class Penguin(Bird):                   # a Bird, but NOT a FlyingBird
    def swim(self): return "splash"

def migrate(birds: list[FlyingBird]):  # only accepts birds that really fly
    return [b.fly() for b in birds]
```
### LSP warning signs
- A child method that **raises** "not supported" or does nothing.
- A child that **demands more** (stricter inputs) or **gives less** (weaker outputs) than the parent.
- Code that checks `if isinstance(x, Penguin):` before calling a method. That's a sign the hierarchy is lying.

> The classic interview example: is a `Square` a `Rectangle`? If a rectangle lets you set width and height separately, a square can't keep that promise. Make them separate classes, or immutable.
""",
quiz=[
    ("Your `ReadOnlyList(list)` raises an error in `append`. Is that LSP-safe?", "No. Code expecting a list will call `append` and crash. Don't inherit from `list`; make a separate class (or use a tuple)."),
    ("How can `isinstance` checks before method calls hint at an LSP problem?", "If callers must special-case a subclass, that subclass doesn't really behave like its parent, so the hierarchy is wrong."),
],
exercises=[
    X("lsp-accounts", "Fix the savings account",
      """
A `FixedDeposit` currently inherits from `Account` but **raises** on `withdraw`, which breaks LSP. Redesign it:
- `Account(balance)` with `deposit(x)` and a `balance` attribute (no withdraw!),
- `WithdrawableAccount(Account)` adds `withdraw(x)` (raise `ValueError` if x > balance),
- `Savings(WithdrawableAccount)` is a normal account,
- `FixedDeposit(Account)` can only deposit.

`pay_rent(account, amount)` takes a **WithdrawableAccount** and withdraws. It must never be possible to pass a FixedDeposit as a withdrawable account.
""",
      r'''class Account:
    def __init__(self, balance=0):
        self.balance = balance
    def deposit(self, x):
        self.balance += x
    def withdraw(self, x):
        self.balance -= x

class FixedDeposit(Account):
    def withdraw(self, x):
        raise Exception("locked!")     # LSP violation, fix the design

def pay_rent(account, amount):
    account.withdraw(amount)
''',
      r'''class Account:
    def __init__(self, balance=0):
        self.balance = balance
    def deposit(self, x):
        self.balance += x

class WithdrawableAccount(Account):
    def withdraw(self, x):
        if x > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= x

class Savings(WithdrawableAccount):
    pass

class FixedDeposit(Account):            # honest: it never promised withdraw
    pass

def pay_rent(account: WithdrawableAccount, amount):
    account.withdraw(amount)
''',
      r'''
def _rent():
    s = Savings(1000); pay_rent(s, 300); return s.balance
T("rent from savings", _rent, 700)
def _fd():
    f = FixedDeposit(500); f.deposit(100); return f.balance
T("fixed deposit can deposit", _fd, 600)
C("FixedDeposit has no withdraw", lambda: not hasattr(FixedDeposit(), "withdraw"), "FixedDeposit must not inherit withdraw")
C("FixedDeposit is NOT withdrawable", lambda: not issubclass(FixedDeposit, WithdrawableAccount))
def _over():
    try:
        Savings(10).withdraw(50); return False
    except ValueError:
        return True
C("overdraw raises ValueError", _over)
''',
      ["Move withdraw out of Account into a new subclass.", "FixedDeposit should inherit from Account only."]),
])

L(id="isp", part="solid", title="I: Interface Segregation Principle", tagline="Don't force anyone to sign up for things they can't do",
body="""
### The story
Imagine the school forces **every** student to join cricket **and** music **and** coding club, even if they hate cricket. Half of them would "join" but do nothing. Better: **small separate clubs**, where you join only what you actually do.

**ISP: many small, specific interfaces beat one big "do-everything" interface.** A class shouldn't be forced to implement methods it doesn't need.

### The messy code
```python
from abc import ABC, abstractmethod

class Machine(ABC):
    @abstractmethod
    def print(self, doc): ...
    @abstractmethod
    def scan(self) -> str: ...
    @abstractmethod
    def fax(self, number): ...

class CheapPrinter(Machine):
    def print(self, doc): return f"printing {doc}"
    def scan(self): raise NotImplementedError     # forced to fake it
    def fax(self, number): raise NotImplementedError
```
(Notice that ISP violations often cause LSP violations too!)

### The fix: small interfaces (roles)
```python
from typing import Protocol

class Printer(Protocol):
    def print(self, doc) -> str: ...

class Scanner(Protocol):
    def scan(self) -> str: ...

class CheapPrinter:                     # implements only what it can
    def print(self, doc): return f"printing {doc}"

class OfficeMachine:                    # can do several roles
    def print(self, doc): return f"printing {doc}"
    def scan(self): return "scanned page"

def print_homework(p: Printer, doc):    # asks only for what it needs
    return p.print(doc)
```
> Python's `Protocol` is great for ISP: a class doesn't even have to inherit; it just needs the right methods (duck typing, but checked by type checkers).
""",
quiz=[
    ("A `Worker` interface has `work()` and `eat_lunch()`. A `Robot` worker must implement `eat_lunch()`. What's wrong?", "That's an ISP violation. Split it into `Workable` and `Eater`; the robot implements only `Workable`."),
    ("Why does ISP make testing easier?", "A function asking for a tiny interface (just `print()`) can be tested with a tiny fake object."),
],
exercises=[
    X("isp-devices", "Split the smart-device interface",
      """
Create three small abstract interfaces: `Switchable` (`turn_on()` / `turn_off()`), `Dimmable` (`set_brightness(level)`), and `Speaker` (`play(song)`). Then:
- `Bulb`: Switchable + Dimmable. It stores `on` (bool) and `brightness` (int, default 100). `turn_on` and `turn_off` set `on`.
- `SmartSpeaker`: Switchable + Speaker. `play(song)` returns `"playing <song>"` only if it's on, else `"off"`.
- `Fan`: Switchable only.

Write `all_off(devices)`, which turns off every Switchable device. **No class may have a method it can't really do.**
""",
      r'''from abc import ABC, abstractmethod

class Switchable(ABC):
    pass

class Dimmable(ABC):
    pass

class Speaker(ABC):
    pass

class Bulb:
    pass

class SmartSpeaker:
    pass

class Fan:
    pass

def all_off(devices):
    pass
''',
      r'''from abc import ABC, abstractmethod

class Switchable(ABC):
    @abstractmethod
    def turn_on(self): ...
    @abstractmethod
    def turn_off(self): ...

class Dimmable(ABC):
    @abstractmethod
    def set_brightness(self, level): ...

class Speaker(ABC):
    @abstractmethod
    def play(self, song): ...

class _OnOff(Switchable):                 # shared on/off behaviour
    def __init__(self):
        self.on = False
    def turn_on(self):
        self.on = True
    def turn_off(self):
        self.on = False

class Bulb(_OnOff, Dimmable):
    def __init__(self):
        super().__init__()
        self.brightness = 100
    def set_brightness(self, level):
        self.brightness = level

class SmartSpeaker(_OnOff, Speaker):
    def play(self, song):
        return f"playing {song}" if self.on else "off"

class Fan(_OnOff):
    pass

def all_off(devices):
    for d in devices:
        d.turn_off()
''',
      r'''
def _scene():
    b, s, f = Bulb(), SmartSpeaker(), Fan()
    for d in (b, s, f): d.turn_on()
    b.set_brightness(30)
    played = s.play("lofi")
    all_off([b, s, f])
    return [b.brightness, played, b.on, s.on, f.on, s.play("x")]
T("living-room scene", _scene, [30, "playing lofi", False, False, False, "off"])
C("Fan is not Dimmable and can't play", lambda: not hasattr(Fan(), "set_brightness") and not hasattr(Fan(), "play"))
C("Bulb can't play music", lambda: not hasattr(Bulb(), "play"))
C("interfaces used", lambda: issubclass(Bulb, Dimmable) and issubclass(SmartSpeaker, Speaker) and all(issubclass(c, Switchable) for c in (Bulb, SmartSpeaker, Fan)))
''',
      ["A small base class with on/off can be shared by all three devices.", "Use multiple inheritance from the small interfaces: class Bulb(Base, Dimmable)."]),
])

L(id="dip", part="solid", title="D: Dependency Inversion Principle", tagline="Depend on the socket, not on the exact plug",
body="""
### The story
Your phone has a **USB-C port**. It doesn't care whether you plug in your charger, your friend's, or a power bank. If phones were **soldered** to one specific charger, you'd be stuck forever.

**DIP: important (high-level) code should depend on an abstraction (an interface), not on concrete details.** And the details plug into that abstraction.

### The messy code
```python
class MySQLDatabase:
    def save(self, data): ...

class AttendanceService:
    def __init__(self):
        self.db = MySQLDatabase()          # soldered to MySQL!
    def mark_present(self, student):
        self.db.save({"student": student, "present": True})
```
Problems: you can't switch to another database, and **you can't test it without a real MySQL server**.

### The fix: depend on an interface, and "inject" the concrete thing
```python
from typing import Protocol

class Storage(Protocol):                  # the abstraction (the USB-C port)
    def save(self, data) -> None: ...

class AttendanceService:
    def __init__(self, storage: Storage):  # handed in from outside = "dependency injection"
        self.storage = storage
    def mark_present(self, student):
        self.storage.save({"student": student, "present": True})

class MySQLStorage:
    def save(self, data): ...              # real one, for production

class MemoryStorage:                       # fake one, for tests
    def __init__(self): self.rows = []
    def save(self, data): self.rows.append(data)

service = AttendanceService(MemoryStorage())   # tests: no database needed!
```
### DIP vs "dependency injection"
- **Dependency Inversion** is the **principle**: depend on abstractions.
- **Dependency Injection** is the **technique**: pass dependencies in (usually through `__init__`) instead of creating them inside.

> Rule of thumb: if a class does `self.x = SomethingConcrete()` in `__init__` for something slow or external (a DB, an API, email, the clock), consider passing it in instead.
""",
quiz=[
    ("Why is `datetime.now()` inside business logic a DIP smell?", "The code depends on the real clock, so tests can't control time. Inject a `clock` function instead (e.g. `clock=datetime.now`)."),
    ("What's the difference between Dependency Inversion and Dependency Injection?", "Inversion is the principle (depend on abstractions); injection is the technique (pass dependencies in from outside)."),
],
exercises=[
    X("dip-notifier", "Inject the notifier",
      """
`ExamResults` currently creates an `SmsSender` inside itself. Fix it:
- Define a `Notifier` Protocol (or ABC) with `send(to, message)`.
- `ExamResults(notifier)` receives the notifier in `__init__`.
- `publish(student, phone, marks)` sends `"<student> scored <marks>"` to `phone` via the notifier, and returns `"PASS"` if marks ≥ 35, else `"FAIL"`.
- Write a `FakeNotifier` that records every `(to, message)` in a list attribute `sent`, so tests need no real SMS.
""",
      r'''class SmsSender:
    def send(self, to, message):
        raise RuntimeError("would send a real SMS!")

class ExamResults:
    def __init__(self):
        self.sms = SmsSender()            # hard-wired: fix this
    def publish(self, student, phone, marks):
        self.sms.send(phone, f"{student} scored {marks}")
        return "PASS" if marks >= 35 else "FAIL"

class FakeNotifier:
    pass
''',
      r'''from typing import Protocol

class Notifier(Protocol):
    def send(self, to, message) -> None: ...

class SmsSender:
    def send(self, to, message):
        raise RuntimeError("would send a real SMS!")

class ExamResults:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier              # injected from outside
    def publish(self, student, phone, marks):
        self.notifier.send(phone, f"{student} scored {marks}")
        return "PASS" if marks >= 35 else "FAIL"

class FakeNotifier:
    def __init__(self):
        self.sent = []
    def send(self, to, message):
        self.sent.append((to, message))
''',
      r'''
def _run():
    fake = FakeNotifier()
    r = ExamResults(fake)
    return [r.publish("Asha", "999", 82), r.publish("Ravi", "888", 20), fake.sent]
T("publish with a fake", _run, ["PASS", "FAIL", [("999", "Asha scored 82"), ("888", "Ravi scored 20")]])
def _no_sms():
    import inspect
    return "SmsSender()" not in inspect.getsource(ExamResults.__init__)
C("ExamResults doesn't create SmsSender itself", _no_sms, "take the notifier as an __init__ parameter")
''',
      ["Change `__init__(self)` to `__init__(self, notifier)`.", "FakeNotifier needs `self.sent = []` and a send() that appends."]),
])
