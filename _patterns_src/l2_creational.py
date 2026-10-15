from core import L, X

L(id="singleton", part="creational", title="Singleton", tagline="Only one principal for the whole school",
body="""
### The story
A school has **exactly one principal**. Whoever asks "who's the principal?" (teachers, students, parents) gets the **same person**. You'd never want two principals giving different orders!

**Singleton: make sure a class has only one object, and give everyone a single way to reach it.** Used for things like app settings, a logger, or a connection pool.

### Classic version (override `__new__`)
```python
class Principal:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:                 # first time only
            cls._instance = super().__new__(cls)
        return cls._instance                      # always the same object

a = Principal(); b = Principal()
print(a is b)        # True: the same object
```
(`__new__` creates the object; `__init__` fills it. Remember from OOP chapter 11: `__init__` still runs on every `Principal()` call, so don't reset data there.)

### Thread-safe version (when several threads may create it at once)
```python
import threading
class Config:
    _instance, _lock = None, threading.Lock()
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:                       # only one thread at a time
                if cls._instance is None:         # check again inside the lock
                    cls._instance = super().__new__(cls)
                    cls._instance.settings = {}
        return cls._instance
```
### 🐍 The Pythonic shortcut: just use a module!
A Python module is imported **only once**, so any object created inside it is automatically a singleton:
```python
# config.py
settings = {"theme": "dark"}
# anywhere else:
from config import settings     # everyone gets the SAME dict
```
### ⚠ When NOT to use it
Singletons are **global variables in disguise**. They make testing hard (tests share state) and hide dependencies. Often the better choice is to create **one object** in `main()` and **pass it in** (dependency injection, from the DIP lesson).
""",
quiz=[
    ("Why does `__init__` need care in a `__new__`-based singleton?", "`__init__` runs on every `Class()` call even though the same object comes back, so it could reset the data. Initialize once inside `__new__`, or guard `__init__`."),
    ("What's the simplest singleton in Python?", "A module-level object. Modules are imported once and cached in `sys.modules`."),
],
exercises=[
    X("singleton-counter", "A visitor counter that exists only once",
      """
Make `VisitorCounter` a singleton. Every `VisitorCounter()` call returns the **same** object. It has `visit()`, which increases `count` by 1, and the `count` attribute **must not reset** when `VisitorCounter()` is called again.
""",
      r'''class VisitorCounter:
    def __init__(self):
        self.count = 0          # careful: this would reset every time!
    def visit(self):
        self.count += 1
''',
      r'''class VisitorCounter:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.count = 0           # initialize ONCE, here
        return cls._instance
    def visit(self):
        self.count += 1
''',
      r'''
VisitorCounter._instance = None if hasattr(VisitorCounter, "_instance") else None
C("same object every time", lambda: VisitorCounter() is VisitorCounter())
def _count():
    a = VisitorCounter(); start = a.count
    a.visit(); VisitorCounter().visit(); VisitorCounter().visit()
    return VisitorCounter().count - start
T("count doesn't reset", _count, 3)
''',
      ["Override __new__ and store the single object in a class attribute.", "Set count = 0 inside __new__ (only the first time), not in __init__."]),
])

L(id="factory", part="creational", title="Factory (Simple Factory & Factory Method)", tagline="Order by name; the factory builds it",
body="""
### The story
At a pizza shop you just say **"one Margherita"**. You don't go into the kitchen and decide how to knead the dough. The **kitchen (the factory)** knows how to make each pizza. If the shop adds a new pizza, **your way of ordering doesn't change**.

**Factory: put the "which class do I create, and how?" decision in one place**, so the rest of the code just asks for what it wants.

### The messy code
```python
# scattered all over the app:
if kind == "email": n = EmailNotifier(smtp_host, port)
elif kind == "sms": n = SmsNotifier(api_key)
```
Every place that creates notifiers repeats this logic. Adding "push notifications" means hunting down every copy.

### Simple factory (the version you'll use most)
```python
class EmailNotifier:
    def send(self, msg): return f"email: {msg}"
class SmsNotifier:
    def send(self, msg): return f"sms: {msg}"

class NotifierFactory:
    _registry = {"email": EmailNotifier, "sms": SmsNotifier}

    @classmethod
    def register(cls, name):                    # new kinds plug themselves in (OCP!)
        def deco(klass):
            cls._registry[name] = klass
            return klass
        return deco

    @classmethod
    def create(cls, name):
        if name not in cls._registry:
            raise ValueError(f"unknown notifier: {name}")
        return cls._registry[name]()

@NotifierFactory.register("push")
class PushNotifier:
    def send(self, msg): return f"push: {msg}"

NotifierFactory.create("push").send("hi")      # 'push: hi'
```
### Factory **Method** (the GoF version)
A parent class defines the steps but lets **subclasses decide which object to create**:
```python
class Dialog:
    def render(self):
        button = self.create_button()          # the "factory method"
        return f"[{button.draw()}]"
    def create_button(self):                   # subclasses override this
        raise NotImplementedError

class WindowsDialog(Dialog):
    def create_button(self): return WindowsButton()
class WebDialog(Dialog):
    def create_button(self): return HtmlButton()
```
### 🐍 Pythonic shortcuts
- **Classes are objects** in Python, so a plain dict `{"email": EmailNotifier}` is already a factory.
- `@classmethod` **alternative constructors** are tiny factories: `date.fromisoformat("2026-01-01")`, `dict.fromkeys(...)`.
""",
quiz=[
    ("What problem does a factory solve?", "Creation logic (which class, which arguments) lives in one place, so callers don't repeat or know it, and adding a new type touches only the factory."),
    ("Name a factory method in Python's standard library.", "`datetime.fromtimestamp()`, `date.fromisoformat()`, `int.from_bytes()`, `dict.fromkeys()`. These are classmethod alternative constructors."),
],
exercises=[
    X("factory-shapes", "A shape factory with registration",
      """
Build `ShapeFactory` with:
- `ShapeFactory.register(name)`, a **decorator** that adds a class to the registry,
- `ShapeFactory.create(name, *args)`, which returns an instance, or raises `ValueError` for unknown names.

Register `Square(side)` as `"square"` (area = side²) and `Rect(w, h)` as `"rect"` (area = w·h), using the decorator.
""",
      r'''class ShapeFactory:
    _registry = {}

    @classmethod
    def register(cls, name):
        pass

    @classmethod
    def create(cls, name, *args):
        pass

# use @ShapeFactory.register("square") on these:
class Square:
    def __init__(self, side): self.side = side
    def area(self): return self.side ** 2

class Rect:
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h
''',
      r'''class ShapeFactory:
    _registry = {}

    @classmethod
    def register(cls, name):
        def deco(klass):
            cls._registry[name] = klass
            return klass                 # return the class unchanged
        return deco

    @classmethod
    def create(cls, name, *args):
        if name not in cls._registry:
            raise ValueError(f"unknown shape: {name}")
        return cls._registry[name](*args)

@ShapeFactory.register("square")
class Square:
    def __init__(self, side): self.side = side
    def area(self): return self.side ** 2

@ShapeFactory.register("rect")
class Rect:
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h
''',
      r'''
T("square", lambda: ShapeFactory.create("square", 3).area(), 9)
T("rect", lambda: ShapeFactory.create("rect", 2, 5).area(), 10)
C("returns real instances", lambda: isinstance(ShapeFactory.create("square", 1), Square))
def _unknown():
    try:
        ShapeFactory.create("hexagon"); return False
    except ValueError:
        return True
C("unknown name raises ValueError", _unknown)
def _later():
    @ShapeFactory.register("tri")
    class Tri:
        def __init__(self, b, h): self.b, self.h = b, h
        def area(self): return self.b * self.h / 2
    return ShapeFactory.create("tri", 4, 3).area()
T("new shapes plug in later", _later, 6.0)
''',
      ["register returns a decorator function: def deco(klass): ...; return klass.", "create looks the class up in the dict and calls it with *args."]),
])

L(id="abstract-factory", part="creational", title="Abstract Factory", tagline="A matching uniform set: never mix and match by accident",
body="""
### The story
Your school has a **summer uniform set** (half shirt, shorts, cap) and a **winter uniform set** (full shirt, trousers, sweater). You'd look silly mixing a sweater with shorts. The uniform shop gives you a **whole matching set** at once.

**Abstract Factory: an interface for creating *families* of related objects that belong together**, without naming their exact classes.

### Example: light and dark themes
```python
from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def draw(self): ...
class Checkbox(ABC):
    @abstractmethod
    def draw(self): ...

class LightButton(Button):
    def draw(self): return "⬜ button"
class DarkButton(Button):
    def draw(self): return "⬛ button"
class LightCheckbox(Checkbox):
    def draw(self): return "☐ light"
class DarkCheckbox(Checkbox):
    def draw(self): return "☑ dark"

class ThemeFactory(ABC):                 # the abstract factory
    @abstractmethod
    def button(self) -> Button: ...
    @abstractmethod
    def checkbox(self) -> Checkbox: ...

class LightTheme(ThemeFactory):
    def button(self): return LightButton()
    def checkbox(self): return LightCheckbox()

class DarkTheme(ThemeFactory):
    def button(self): return DarkButton()
    def checkbox(self): return DarkCheckbox()

def build_settings_page(theme: ThemeFactory):
    return [theme.button().draw(), theme.checkbox().draw()]   # always a matching pair
```

### Factory vs Abstract Factory
| | Factory | Abstract Factory |
|---|---|---|
| creates | **one** product | a **family** of products |
| example | "give me a notifier" | "give me a whole matching UI theme" |

Real-world uses: UI themes, database drivers (connection + cursor + dialect), cloud providers (AWS storage + AWS queue vs GCP storage + GCP queue).
""",
quiz=[
    ("When do you need an Abstract Factory instead of a simple factory?", "When several created objects **must match each other** (a family): theme widgets, or provider-specific clients that must come from the same provider."),
],
exercises=[
    X("af-furniture", "Furniture families",
      """
A furniture shop sells **Modern** and **Victorian** sets. Create:
- products `ModernChair`, `ModernTable`, `VictorianChair`, `VictorianTable`, each with `describe()` returning `"modern chair"`, `"modern table"`, `"victorian chair"`, `"victorian table"`,
- an abstract `FurnitureFactory` with `make_chair()` and `make_table()`,
- `ModernFactory` and `VictorianFactory`.

`furnish_room(factory)` returns `[chair.describe(), table.describe()]`.
""",
      r'''from abc import ABC, abstractmethod

class FurnitureFactory(ABC):
    pass

def furnish_room(factory):
    pass
''',
      r'''from abc import ABC, abstractmethod

class ModernChair:
    def describe(self): return "modern chair"
class ModernTable:
    def describe(self): return "modern table"
class VictorianChair:
    def describe(self): return "victorian chair"
class VictorianTable:
    def describe(self): return "victorian table"

class FurnitureFactory(ABC):
    @abstractmethod
    def make_chair(self): ...
    @abstractmethod
    def make_table(self): ...

class ModernFactory(FurnitureFactory):
    def make_chair(self): return ModernChair()
    def make_table(self): return ModernTable()

class VictorianFactory(FurnitureFactory):
    def make_chair(self): return VictorianChair()
    def make_table(self): return VictorianTable()

def furnish_room(factory):
    return [factory.make_chair().describe(), factory.make_table().describe()]
''',
      r'''
T("modern set", lambda: furnish_room(ModernFactory()), ["modern chair", "modern table"])
T("victorian set", lambda: furnish_room(VictorianFactory()), ["victorian chair", "victorian table"])
C("factories share the abstract base", lambda: issubclass(ModernFactory, FurnitureFactory) and issubclass(VictorianFactory, FurnitureFactory))
def _abstract():
    try:
        FurnitureFactory(); return False
    except TypeError:
        return True
C("FurnitureFactory is abstract", _abstract)
''',
      ["Write the 4 product classes first.", "Each concrete factory returns its own family's chair and table."]),
])

L(id="builder", part="creational", title="Builder", tagline="Build a burger step by step",
body="""
### The story
At a burger counter, you build your order **step by step**: bun → patty → cheese? → onions? → sauce. Some steps are optional, and the order is checked at the end ("you can't have a burger with no patty!"). Then they hand you the **finished** burger.

**Builder: construct a complex object step by step, then produce the final (often immutable) result with `build()`**, which validates everything once.

### The problem: the "telescoping constructor"
```python
Burger("sesame", "veg", True, False, True, "mayo", 2, False)   # what does True mean?? 😵
```
### The builder
```python
from dataclasses import dataclass

@dataclass(frozen=True)                  # the finished product can't be changed
class Burger:
    bun: str
    patty: str
    toppings: tuple
    sauce: str

class BurgerBuilder:
    def __init__(self):
        self._bun, self._patty, self._toppings, self._sauce = "plain", None, [], "none"
    def bun(self, kind):
        self._bun = kind
        return self                      # returning self allows chaining
    def patty(self, kind):
        self._patty = kind
        return self
    def add(self, topping):
        self._toppings.append(topping)
        return self
    def sauce(self, kind):
        self._sauce = kind
        return self
    def build(self):
        if self._patty is None:
            raise ValueError("a burger needs a patty!")   # validation in ONE place
        return Burger(self._bun, self._patty, tuple(self._toppings), self._sauce)

burger = BurgerBuilder().bun("sesame").patty("veg").add("cheese").add("onion").sauce("mayo").build()
```
This style of chaining calls is called a **fluent interface** (SQLAlchemy queries and pandas method chains work this way).

### 🐍 Pythonic shortcut
Python has **keyword arguments with defaults**, which solve most telescoping problems on their own:
```python
Burger(bun="sesame", patty="veg", toppings=("cheese",), sauce="mayo")
```
Use a real Builder when: construction happens **in steps over time**, **validation spans several fields**, or the same steps can produce **different results** (an SQL string vs a MongoDB query).
""",
quiz=[
    ("Why does each builder method `return self`?", "So calls can be chained: `b.bun(...).patty(...).build()`, a fluent interface."),
    ("When are plain keyword arguments enough?", "When the object is created in one go and validation is simple. Python's kwargs already fix 'what does True mean?'."),
],
exercises=[
    X("builder-query", "An SQL query builder",
      """
Write `QueryBuilder(table)` with chainable methods:
- `select(*cols)` (default `*` if never called),
- `where(condition)` (can be called several times; conditions are joined with ` AND `),
- `order_by(col)`,
- `limit(n)`,

and `build()` returning a string like:
`SELECT name, age FROM students WHERE age > 10 AND class = 5 ORDER BY name LIMIT 3`
Leave out the parts that weren't set. `limit` must raise `ValueError` if n ≤ 0.
""",
      r'''class QueryBuilder:
    def __init__(self, table):
        self.table = table

    def build(self):
        pass
''',
      r'''class QueryBuilder:
    def __init__(self, table):
        self.table = table
        self._cols, self._where, self._order, self._limit = ["*"], [], None, None

    def select(self, *cols):
        self._cols = list(cols)
        return self

    def where(self, condition):
        self._where.append(condition)
        return self

    def order_by(self, col):
        self._order = col
        return self

    def limit(self, n):
        if n <= 0:
            raise ValueError("limit must be positive")
        self._limit = n
        return self

    def build(self):
        parts = [f"SELECT {', '.join(self._cols)} FROM {self.table}"]
        if self._where:
            parts.append("WHERE " + " AND ".join(self._where))
        if self._order:
            parts.append(f"ORDER BY {self._order}")
        if self._limit:
            parts.append(f"LIMIT {self._limit}")
        return " ".join(parts)
''',
      r'''
T("full query", lambda: QueryBuilder("students").select("name", "age").where("age > 10").where("class = 5").order_by("name").limit(3).build(),
  "SELECT name, age FROM students WHERE age > 10 AND class = 5 ORDER BY name LIMIT 3")
T("defaults", lambda: QueryBuilder("books").build(), "SELECT * FROM books")
T("only where", lambda: QueryBuilder("t").where("x = 1").build(), "SELECT * FROM t WHERE x = 1")
def _bad():
    try:
        QueryBuilder("t").limit(0); return False
    except ValueError:
        return True
C("limit(0) raises ValueError", _bad)
C("methods chain (return self)", lambda: isinstance(QueryBuilder("t").select("a").where("b"), QueryBuilder))
''',
      ["Store each part in an attribute; every method returns self.", "In build(), add each part to a list only if it was set, then join with spaces."]),
])

L(id="prototype", part="creational", title="Prototype", tagline="Photocopy instead of starting from scratch",
body="""
### The story
Your teacher makes **one perfect worksheet** and then **photocopies** it for 40 students, instead of writing 40 by hand. Each student can then fill in their own copy without affecting the others.

**Prototype: create new objects by copying (cloning) an existing, already-set-up object.** It's useful when setting an object up is expensive or complicated (loading settings, a big configuration, a game character with many stats).

### In Python: the `copy` module
```python
import copy

class Character:
    def __init__(self, name, level, skills):
        self.name, self.level, self.skills = name, level, skills
    def clone(self, **changes):
        new = copy.deepcopy(self)        # a full independent copy (inner lists copied too)
        new.__dict__.update(changes)     # tweak a few fields
        return new

warrior = Character("Template", 10, ["sword", "shield"])
asha = warrior.clone(name="Asha")
asha.skills.append("bow")                # doesn't affect warrior: deep copy!
```
### ⚠ Shallow vs deep copy (the classic bug)
```python
shallow = copy.copy(warrior)      # NEW object, but the SAME skills list inside
shallow.skills.append("magic")    # oops, warrior.skills changed too!
```
- `copy.copy` (shallow): copies the outer object; inner lists and dicts are **shared**.
- `copy.deepcopy`: copies everything, all the way down.

### A prototype registry
Keep ready-made templates in a dict and clone them on request:
```python
TEMPLATES = {"warrior": warrior, "mage": Character("Template", 8, ["fireball"])}
hero = TEMPLATES["mage"].clone(name="Ravi")
```
🐍 For dataclasses, `dataclasses.replace(obj, name="Ravi")` (or `copy.replace` in 3.13) is a built-in shallow "clone with changes".
""",
quiz=[
    ("Shallow copy of an object containing a list, then you append to the copy's list. What happens to the original?", "The original's list changes too, because a shallow copy shares inner objects. Use `copy.deepcopy`."),
],
exercises=[
    X("prototype-docs", "Document templates",
      """
Write `Document(title, sections)` (sections is a list of strings) with `clone(**changes)`, which returns a **deep** copy with optional field changes.

Then write a `TemplateRegistry` with `add(name, doc)` and `create(name, **changes)`, which returns a fresh clone of the stored template. Raise `KeyError` for unknown names. Changing a clone must **never** change the template.
""",
      r'''import copy

class Document:
    def __init__(self, title, sections):
        self.title, self.sections = title, sections
    def clone(self, **changes):
        pass

class TemplateRegistry:
    pass
''',
      r'''import copy

class Document:
    def __init__(self, title, sections):
        self.title, self.sections = title, sections
    def clone(self, **changes):
        new = copy.deepcopy(self)
        new.__dict__.update(changes)
        return new

class TemplateRegistry:
    def __init__(self):
        self._templates = {}
    def add(self, name, doc):
        self._templates[name] = doc
    def create(self, name, **changes):
        return self._templates[name].clone(**changes)     # KeyError if unknown
''',
      r'''
def _run():
    reg = TemplateRegistry()
    reg.add("report", Document("Report", ["Intro", "Results"]))
    a = reg.create("report", title="Science Report")
    a.sections.append("Conclusion")
    b = reg.create("report")
    return [a.title, a.sections, b.title, b.sections]
T("clones are independent", _run, ["Science Report", ["Intro", "Results", "Conclusion"], "Report", ["Intro", "Results"]])
def _missing():
    try:
        TemplateRegistry().create("nope"); return False
    except KeyError:
        return True
C("unknown template raises KeyError", _missing)
def _deep():
    d = Document("x", [["nested"]]); c = d.clone(); c.sections[0].append("y"); return d.sections == [["nested"]]
C("deep copy (nested lists too)", _deep)
''',
      ["Use copy.deepcopy(self), then update __dict__ with the changes.", "The registry stores templates in a dict and calls .clone(**changes)."]),
])
