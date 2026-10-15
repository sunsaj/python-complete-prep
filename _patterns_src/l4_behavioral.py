from core import L, X

L(id="strategy", part="behavioral", title="Strategy", tagline="Choose how to get to school today",
body="""
### The story
You can get to school by **walking**, **cycling** or **bus**. The goal is the same (reach school); only the **way** changes. Each morning you pick a strategy based on the weather and time.

**Strategy: put each way of doing a job in its own class (or function) behind one interface, and choose which one to use at runtime.**

### The messy code
```python
def travel_time(mode, km):
    if mode == "walk": return km * 12
    elif mode == "cycle": return km * 4
    elif mode == "bus": return km * 2 + 10      # waiting time
```
### The pattern
```python
from typing import Protocol

class Route(Protocol):
    def minutes(self, km: float) -> float: ...

class Walk:
    def minutes(self, km): return km * 12
class Cycle:
    def minutes(self, km): return km * 4
class Bus:
    def minutes(self, km): return km * 2 + 10

class Navigator:
    def __init__(self, route: Route):
        self.route = route                 # the strategy can be swapped any time
    def eta(self, km):
        return self.route.minutes(km)

nav = Navigator(Walk()); nav.eta(2)        # 24
nav.route = Bus();       nav.eta(2)        # 14
```
### 🐍 Pythonic shortcut: functions are strategies
```python
STRATEGIES = {"walk": lambda km: km * 12, "bus": lambda km: km * 2 + 10}
def eta(km, how=STRATEGIES["walk"]):
    return how(km)
sorted(students, key=lambda s: s.marks)    # `key=` is a strategy!
```
**Where you see it:** sorting keys, payment methods, discount rules, compression algorithms, route planners, ML model selection.
""",
quiz=[("How is Strategy related to the Open/Closed principle?", "New behaviours are new strategy classes or functions; the code that uses the strategy never changes."),
      ("What is `sorted(..., key=len)` an example of?", "The Strategy pattern using a plain function: the comparison strategy is passed in.")],
exercises=[
    X("strategy-discount", "Discount strategies",
      """
Write discount strategies, each with `apply(total)`:
- `NoDiscount`: the total unchanged,
- `Percent(p)`: p% off,
- `Flat(amount)`: minus the amount, but never below 0,
- `BuyOverGetOff(threshold, off)`: if total ≥ threshold, subtract `off`.

`Checkout(strategy)` has `pay(total)`, which returns `round(strategy.apply(total), 2)`, and the strategy can be changed later by assigning `checkout.strategy = ...`.
""",
      r'''class NoDiscount:
    pass

class Checkout:
    pass
''',
      r'''class NoDiscount:
    def apply(self, total): return total

class Percent:
    def __init__(self, p): self.p = p
    def apply(self, total): return total * (1 - self.p / 100)

class Flat:
    def __init__(self, amount): self.amount = amount
    def apply(self, total): return max(0, total - self.amount)

class BuyOverGetOff:
    def __init__(self, threshold, off): self.threshold, self.off = threshold, off
    def apply(self, total): return total - self.off if total >= self.threshold else total

class Checkout:
    def __init__(self, strategy):
        self.strategy = strategy
    def pay(self, total):
        return round(self.strategy.apply(total), 2)
''',
      r'''
T("no discount", lambda: Checkout(NoDiscount()).pay(500), 500)
T("20 percent", lambda: Checkout(Percent(20)).pay(500), 400.0)
T("flat never negative", lambda: Checkout(Flat(100)).pay(60), 0)
T("threshold met", lambda: Checkout(BuyOverGetOff(1000, 150)).pay(1200), 1050)
T("threshold not met", lambda: Checkout(BuyOverGetOff(1000, 150)).pay(900), 900)
def _swap():
    c = Checkout(NoDiscount()); a = c.pay(100); c.strategy = Percent(50); return [a, c.pay(100)]
T("swap strategy at runtime", _swap, [100, 50.0])
''',
      ["Each strategy is a tiny class with apply(total).", "Checkout stores self.strategy and calls it in pay()."]),
])

L(id="observer", part="behavioral", title="Observer", tagline="Subscribe to a YouTube channel",
body="""
### The story
When you **subscribe** to a YouTube channel, you get notified of every new video. The channel doesn't know or care who you are. It just tells **all subscribers**. You can **unsubscribe** any time.

**Observer: an object (the subject) keeps a list of subscribers (observers) and notifies all of them when something happens.** The subject and the observers stay loosely connected.

```python
class Channel:                                   # the SUBJECT
    def __init__(self, name):
        self.name, self._subscribers = name, []
    def subscribe(self, fn):
        self._subscribers.append(fn)
    def unsubscribe(self, fn):
        self._subscribers.remove(fn)
    def upload(self, title):
        for notify in list(self._subscribers):    # copy, in case someone unsubscribes mid-loop
            notify(self.name, title)

def phone(channel, title): print(f"📱 {channel}: {title}")
def email(channel, title): print(f"📧 {channel} posted {title}")

c = Channel("MathsWithFun")
c.subscribe(phone); c.subscribe(email)
c.upload("Fractions made easy")                  # both get notified
```
### An event bus: Observer for a whole app
```python
from collections import defaultdict
class EventBus:
    def __init__(self): self.handlers = defaultdict(list)
    def on(self, event, fn): self.handlers[event].append(fn)
    def emit(self, event, **data):
        for fn in self.handlers[event]:
            fn(**data)

bus = EventBus()
bus.on("order_paid", lambda order_id: print("send receipt", order_id))
bus.on("order_paid", lambda order_id: print("tell kitchen", order_id))
bus.emit("order_paid", order_id=42)
```
**Where you see it:** button clicks in GUIs, Django signals, spreadsheet cells updating, stock price alerts, message brokers (Kafka) at large scale.

> ⚠ **Gotchas:** one failing subscriber shouldn't break the rest (wrap each call in try/except), and remember to unsubscribe, or the subject keeps old objects alive forever (a memory leak).
""",
quiz=[("Why does the subject loop over a *copy* of the subscriber list?", "A subscriber might unsubscribe while being notified, and changing a list while looping over it skips items or errors."),
      ("Observer vs simply calling functions directly?", "With Observer, the subject doesn't know its subscribers. New reactions are added without changing the subject (open/closed).")],
exercises=[
    X("observer-stock", "Stock price alerts",
      """
Write `Stock(symbol, price)` with `subscribe(fn)`, `unsubscribe(fn)` and a `set_price(new)` method that updates the price and calls every subscriber as `fn(symbol, old, new)`, **but only if the price actually changed**. Subscribers are called in the order they subscribed, and an exception raised by one subscriber must **not** stop the others (catch it and move on).
""",
      r'''class Stock:
    def __init__(self, symbol, price):
        self.symbol, self.price = symbol, price
''',
      r'''class Stock:
    def __init__(self, symbol, price):
        self.symbol, self.price = symbol, price
        self._subs = []
    def subscribe(self, fn):
        self._subs.append(fn)
    def unsubscribe(self, fn):
        self._subs.remove(fn)
    def set_price(self, new):
        old = self.price
        if new == old:
            return                                  # nothing changed, so no notification
        self.price = new
        for fn in list(self._subs):
            try:
                fn(self.symbol, old, new)
            except Exception:
                pass                                # one bad subscriber can't break the rest
''',
      r'''
def _run():
    log = []
    s = Stock("TCS", 100)
    a = lambda sym, o, n: log.append(("a", sym, o, n))
    def broken(sym, o, n): raise RuntimeError("boom")
    b = lambda sym, o, n: log.append(("b", n))
    s.subscribe(a); s.subscribe(broken); s.subscribe(b)
    s.set_price(110); s.set_price(110); s.unsubscribe(a); s.set_price(90)
    return log
T("notifications", _run, [("a", "TCS", 100, 110), ("b", 110), ("b", 90)])
def _price():
    s = Stock("X", 5); s.set_price(7); return s.price
T("price updates even with no subscribers", _price, 7)
''',
      ["Keep a list of subscriber functions.", "In set_price, return early if nothing changed; wrap each call in try/except."]),
])

L(id="command", part="behavioral", title="Command", tagline="Write the order on a slip of paper",
body="""
### The story
In a restaurant, the waiter writes your order on a **slip of paper** and pins it in the kitchen. The slip **is** the request. It can wait in a queue, be done later, be cancelled, or be kept as a record. And the waiter doesn't need to know how to cook!

**Command: turn a request (an action) into an object.** Then you can **queue** it, **log** it, **undo** it, or **replay** it.

### Undo/redo for a drawing app
```python
class AddShape:
    def __init__(self, canvas, shape):
        self.canvas, self.shape = canvas, shape
    def execute(self):
        self.canvas.append(self.shape)
    def undo(self):
        self.canvas.remove(self.shape)

class Editor:
    def __init__(self):
        self.canvas, self.done, self.undone = [], [], []
    def run(self, cmd):
        cmd.execute()
        self.done.append(cmd)
        self.undone.clear()              # a new action wipes the redo history
    def undo(self):
        if self.done:
            cmd = self.done.pop(); cmd.undo(); self.undone.append(cmd)
    def redo(self):
        if self.undone:
            cmd = self.undone.pop(); cmd.execute(); self.done.append(cmd)

ed = Editor()
ed.run(AddShape(ed.canvas, "circle")); ed.run(AddShape(ed.canvas, "square"))
ed.undo()       # canvas = ['circle']
ed.redo()       # canvas = ['circle', 'square']
```
```text
  done stack:   [add circle, add square]   ← undo pops from here
  undone stack: []                          ← redo pops from here
```
**Where you see it:** undo/redo in editors, task queues (Celery jobs are commands), remote-control buttons, database migrations (`upgrade` / `downgrade`), transaction logs.

🐍 A simple command can be just a function or a `functools.partial`. A class is needed when you want `undo()` too.
""",
quiz=[("Why does doing a new action clear the redo stack?", "Redo history only makes sense along the same timeline. After a new action, the 'future' you undid is no longer reachable."),
      ("Name two things Command lets you do with actions besides running them.", "Undo/redo, queueing or scheduling, logging or auditing, and replaying.")],
exercises=[
    X("command-text", "Undo/redo text editor",
      """
Write commands on a `Doc` (it has a `text` attribute):
- `Append(doc, s)`: adds s at the end; undo removes it,
- `Delete(doc, n)`: removes the last n characters; undo puts them back (remember what you deleted!).

Write `History` with `run(cmd)`, `undo()` and `redo()`, using the two-stack approach (a new `run` clears redo). Undo or redo with nothing to do should simply do nothing.
""",
      r'''class Doc:
    def __init__(self): self.text = ""

class Append:
    pass

class Delete:
    pass

class History:
    pass
''',
      r'''class Doc:
    def __init__(self): self.text = ""

class Append:
    def __init__(self, doc, s): self.doc, self.s = doc, s
    def execute(self): self.doc.text += self.s
    def undo(self): self.doc.text = self.doc.text[:-len(self.s)] if self.s else self.doc.text

class Delete:
    def __init__(self, doc, n): self.doc, self.n, self.removed = doc, n, ""
    def execute(self):
        self.removed = self.doc.text[-self.n:] if self.n else ""     # remember for undo
        self.doc.text = self.doc.text[:len(self.doc.text) - len(self.removed)]
    def undo(self): self.doc.text += self.removed

class History:
    def __init__(self): self.done, self.undone = [], []
    def run(self, cmd):
        cmd.execute(); self.done.append(cmd); self.undone.clear()
    def undo(self):
        if self.done:
            cmd = self.done.pop(); cmd.undo(); self.undone.append(cmd)
    def redo(self):
        if self.undone:
            cmd = self.undone.pop(); cmd.execute(); self.done.append(cmd)
''',
      r'''
def _run():
    d, h = Doc(), History(); seen = []
    h.run(Append(d, "Hello")); h.run(Append(d, " World")); seen.append(d.text)
    h.run(Delete(d, 5)); seen.append(d.text)
    h.undo(); seen.append(d.text)
    h.undo(); seen.append(d.text)
    h.redo(); seen.append(d.text)
    h.run(Append(d, "!")); h.redo(); seen.append(d.text)
    h.undo(); h.undo(); h.undo(); h.undo(); seen.append(d.text)
    return seen
T("full undo/redo story", _run, ["Hello World", "Hello ", "Hello World", "Hello", "Hello World", "Hello World!", ""])
def _empty():
    d, h = Doc(), History(); h.undo(); h.redo(); return d.text
T("undo/redo on empty history do nothing", _empty, "")
''',
      ["Delete must store the removed text inside execute(), so undo can restore it.", "History.run clears the redo stack."]),
])

L(id="state", part="behavioral", title="State", tagline="A traffic light that knows what it is",
body="""
### The story
A **traffic light** behaves differently depending on its current colour. Pressing "next" on red gives green; on green it gives yellow; on yellow, red. Instead of one giant `if colour == …` everywhere, **each colour knows what comes next and how it behaves**.

**State: an object changes its behaviour when its internal state changes, by delegating to a state object.** It looks as if the object changed its class.

### The messy code
```python
class Order:
    def __init__(self): self.status = "new"
    def pay(self):
        if self.status == "new": self.status = "paid"
        elif self.status == "paid": raise Exception("already paid")
        elif self.status == "shipped": raise Exception("too late")
    def ship(self):
        if self.status == "paid": self.status = "shipped"
        else: raise Exception("can't ship")
    # every new status = edit EVERY method 😵
```
### The pattern: one class per state
```python
class OrderState:
    def pay(self, order):  raise ValueError(f"can't pay when {self.name}")
    def ship(self, order): raise ValueError(f"can't ship when {self.name}")

class New(OrderState):
    name = "new"
    def pay(self, order): order.state = Paid()

class Paid(OrderState):
    name = "paid"
    def ship(self, order): order.state = Shipped()

class Shipped(OrderState):
    name = "shipped"

class Order:
    def __init__(self): self.state = New()
    def pay(self): self.state.pay(self)          # delegate to the current state
    def ship(self): self.state.ship(self)
```
### 🐍 The lighter version: a transition table
When states differ only in **which moves are allowed** (not in big behaviour differences), a dictionary is cleaner:
```python
ALLOWED = {"new": {"paid", "cancelled"}, "paid": {"shipped"}, "shipped": set()}
def move(order, new):
    if new not in ALLOWED[order.status]:
        raise ValueError(f"{order.status} → {new} not allowed")
    order.status = new
```
**State vs Strategy:** they look alike. With Strategy, *you* pick the algorithm from outside. With State, the object **switches states itself** as things happen.
""",
quiz=[("When should you prefer a transition table over state classes?", "When states only differ in which transitions are allowed. Use classes when each state has substantially different behaviour."),
      ("State vs Strategy?", "Strategy is chosen by the client and doesn't change itself. State objects trigger transitions to other states as events happen.")],
exercises=[
    X("state-vending", "Vending machine states",
      """
A vending machine (one product, price 20) has three states: `Idle`, `HasCoin` and `SoldOut`. Implement `VendingMachine(stock)` with:
- `insert(amount)`: in Idle, store the credit and move to HasCoin; in HasCoin, add to the credit; in SoldOut, return `"sold out, returning <amount>"`.
- `press()`: in HasCoin with credit ≥ 20, dispense, give change, reduce stock, and return `"enjoy! change <credit-20>"`. Then move to Idle, or to SoldOut if the stock is 0. With too little credit, return `"need <20-credit> more"`. In Idle, return `"insert coin first"`.
- `state_name()`: `"idle"`, `"has_coin"` or `"sold_out"`.

A machine created with stock 0 starts in SoldOut. Use state classes (not if/elif on strings inside VendingMachine).
""",
      r'''class VendingMachine:
    PRICE = 20
    def __init__(self, stock):
        self.stock, self.credit = stock, 0
''',
      r'''class State:
    name = "?"
    def insert(self, m, amount): raise NotImplementedError
    def press(self, m): raise NotImplementedError

class Idle(State):
    name = "idle"
    def insert(self, m, amount):
        m.credit = amount
        m.state = HasCoin()
        return f"credit {m.credit}"
    def press(self, m):
        return "insert coin first"

class HasCoin(State):
    name = "has_coin"
    def insert(self, m, amount):
        m.credit += amount
        return f"credit {m.credit}"
    def press(self, m):
        if m.credit < m.PRICE:
            return f"need {m.PRICE - m.credit} more"
        change, m.credit = m.credit - m.PRICE, 0
        m.stock -= 1
        m.state = SoldOut() if m.stock == 0 else Idle()
        return f"enjoy! change {change}"

class SoldOut(State):
    name = "sold_out"
    def insert(self, m, amount):
        return f"sold out, returning {amount}"
    def press(self, m):
        return "sold out"

class VendingMachine:
    PRICE = 20
    def __init__(self, stock):
        self.stock, self.credit = stock, 0
        self.state = Idle() if stock > 0 else SoldOut()
    def insert(self, amount): return self.state.insert(self, amount)
    def press(self): return self.state.press(self)
    def state_name(self): return self.state.name
''',
      r'''
def _run():
    m = VendingMachine(1); out = [m.state_name(), m.press()]
    m.insert(10); out.append(m.press()); out.append(m.state_name())
    m.insert(15); out.append(m.press()); out.append(m.state_name())
    out.append(m.insert(5))
    return out
T("story", _run, ["idle", "insert coin first", "need 10 more", "has_coin", "enjoy! change 5", "sold_out", "sold out, returning 5"])
T("starts sold out", lambda: VendingMachine(0).state_name(), "sold_out")
def _two():
    m = VendingMachine(2); m.insert(20); a = m.press(); return [a, m.state_name(), m.stock]
T("back to idle when stock remains", _two, ["enjoy! change 0", "idle", 1])
''',
      ["Create Idle, HasCoin and SoldOut classes, each with insert(m, amount) and press(m).", "VendingMachine just delegates: return self.state.press(self)."]),
])

L(id="template-method", part="behavioral", title="Template Method", tagline="Same recipe steps, different ingredients",
body="""
### The story
Making **tea** and making **coffee** follow the same recipe: _boil water → brew → pour into a cup → add extras_. Only the **brew** and **extras** steps differ (tea leaves + lemon vs coffee powder + milk). Write the recipe **once** and let each drink fill in its own steps.

**Template Method: a parent class defines the skeleton of an algorithm (the order of steps); subclasses fill in some steps** without changing the order.

```python
from abc import ABC, abstractmethod

class HotDrink(ABC):
    def make(self):                          # the TEMPLATE method: a fixed order
        steps = [self.boil(), self.brew(), self.pour()]
        if self.wants_extras():              # a "hook": optional, with a default
            steps.append(self.extras())
        return steps

    def boil(self): return "boil water"      # shared steps
    def pour(self): return "pour in cup"
    def wants_extras(self): return True      # hook with a default

    @abstractmethod
    def brew(self): ...                      # subclasses MUST fill these in
    @abstractmethod
    def extras(self): ...

class Tea(HotDrink):
    def brew(self): return "steep tea"
    def extras(self): return "add lemon"

class BlackCoffee(HotDrink):
    def brew(self): return "drip coffee"
    def extras(self): return "add milk"
    def wants_extras(self): return False     # override the hook
```
**Where you see it:** `unittest.TestCase` (setUp → test → tearDown), Django class-based views (`get_queryset`, `get_context_data`), game loops, data exporters (fetch → transform → write).

> **Template Method vs Strategy:** Template Method uses **inheritance** (override steps). Strategy uses **composition** (pass in a step). Prefer Strategy when the steps vary independently or need to change at runtime.
""",
quiz=[("What's a 'hook' in the Template Method?", "An optional step with a default implementation that subclasses *may* override (like `wants_extras`)."),
      ("Where does Python's unittest use it?", "`TestCase.run()` is the template: setUp(), your test method, then tearDown(), which you override.")],
exercises=[
    X("template-report", "Report exporters",
      """
Write an abstract `Exporter` with the template method `export(rows)`, which returns `header() + body + footer()`:
- the body is `"".join(self.row(r) for r in rows)`,
- `header()` and `footer()` default to `""` (hooks),
- `row(r)` is abstract.

Then:
- `CsvExporter`: header `"name,marks\\n"`, rows like `"Asha,90\\n"`,
- `HtmlExporter`: header `"<table>"`, footer `"</table>"`, rows `"<tr><td>Asha</td><td>90</td></tr>"`.

Each `r` is a tuple `(name, marks)`.
""",
      r'''from abc import ABC, abstractmethod

class Exporter(ABC):
    pass
''',
      r'''from abc import ABC, abstractmethod

class Exporter(ABC):
    def export(self, rows):                         # the template: fixed order
        return self.header() + "".join(self.row(r) for r in rows) + self.footer()
    def header(self): return ""                     # hooks
    def footer(self): return ""
    @abstractmethod
    def row(self, r): ...

class CsvExporter(Exporter):
    def header(self): return "name,marks\n"
    def row(self, r): return f"{r[0]},{r[1]}\n"

class HtmlExporter(Exporter):
    def header(self): return "<table>"
    def footer(self): return "</table>"
    def row(self, r): return f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
''',
      r'''
_rows = [("Asha", 90), ("Ravi", 75)]
T("csv", lambda: CsvExporter().export(_rows), "name,marks\nAsha,90\nRavi,75\n")
T("html", lambda: HtmlExporter().export(_rows), "<table><tr><td>Asha</td><td>90</td></tr><tr><td>Ravi</td><td>75</td></tr></table>")
T("empty", lambda: HtmlExporter().export([]), "<table></table>")
def _abstract():
    try:
        Exporter(); return False
    except TypeError:
        return True
C("Exporter is abstract", _abstract)
''',
      ["export() calls header(), row() for each row, then footer().", "Mark row() with @abstractmethod."]),
])

L(id="iterator", part="behavioral", title="Iterator", tagline="Next song, please",
body="""
### The story
A music player has a **"next"** button. You don't need to know whether the songs are stored in a list, a folder, or come from the internet. You just press "next" until there are no more.

**Iterator: give a way to go through the elements of a collection one by one, without exposing how it's stored inside.**

### Python has this pattern **built into the language**
`for x in thing:` works on anything that follows the **iterator protocol**:
- `__iter__()` returns an iterator,
- the iterator's `__next__()` returns the next item, or raises `StopIteration` at the end.

```python
class Countdown:
    def __init__(self, start): self.start = start
    def __iter__(self):                  # easiest way: make __iter__ a generator
        n = self.start
        while n > 0:
            yield n                      # pause here and hand out one value
            n -= 1

for x in Countdown(3):
    print(x)        # 3, 2, 1
```
### Custom traversal orders
The same collection can offer different iterators:
```python
class Playlist:
    def __init__(self, songs): self.songs = songs
    def __iter__(self): return iter(self.songs)                # normal order
    def reversed_order(self): return reversed(self.songs)      # another iterator
    def shuffled(self, seed=0):
        import random
        order = self.songs[:]
        random.Random(seed).shuffle(order)
        yield from order
```
**Generators** (functions with `yield`) are Python's superpower here: lazy, memory-friendly, and only a few lines. See chapter 07 of the main guide for how they work inside.
""",
quiz=[("What two methods make up Python's iterator protocol?", "`__iter__` (return an iterator) and `__next__` (return the next item or raise `StopIteration`)."),
      ("Why are generators memory-friendly?", "They produce one item at a time on demand instead of building a whole list in memory.")],
exercises=[
    X("iterator-tree", "Iterate a family tree",
      """
`Person(name, children=None)` forms a family tree. Make `Person` **iterable**, so that `for p in grandpa` yields every **name** in **depth-first pre-order** (a person first, then each child's subtree in order). Also add `by_generation()`, a generator that yields lists of names level by level (breadth-first).
""",
      r'''class Person:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []
''',
      r'''from collections import deque

class Person:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def __iter__(self):                         # depth-first pre-order, as a generator
        yield self.name
        for child in self.children:
            yield from child                    # delegate to the child's own iterator

    def by_generation(self):                    # breadth-first, level by level
        level = [self]
        while level:
            yield [p.name for p in level]
            level = [c for p in level for c in p.children]
''',
      r'''
def _fam():
    return Person("Dada", [Person("Papa", [Person("Asha"), Person("Ravi")]), Person("Chacha", [Person("Mini")])])
T("depth-first", lambda: list(_fam()), ["Dada", "Papa", "Asha", "Ravi", "Chacha", "Mini"])
T("by generation", lambda: list(_fam().by_generation()), [["Dada"], ["Papa", "Chacha"], ["Asha", "Ravi", "Mini"]])
T("works with `in`", lambda: "Mini" in _fam(), True)
''',
      ["Write __iter__ as a generator: yield self.name, then `yield from child` for each child.", "by_generation: keep a list for the current level and build the next level from the children."]),
])

L(id="chain", part="behavioral", title="Chain of Responsibility", tagline="Ask the class monitor, then the teacher, then the principal",
body="""
### The story
You have a problem at school. You ask the **class monitor**. If they can't handle it, they pass it to the **class teacher**. If it's still too big, the teacher passes it to the **principal**. Each person either **handles it** or **passes it along** the chain.

**Chain of Responsibility: pass a request along a chain of handlers; each one decides whether to handle it or forward it to the next.**

```python
class Handler:
    def __init__(self, next_handler=None):
        self.next = next_handler
    def handle(self, problem):
        if self.next:
            return self.next.handle(problem)
        return "nobody could help"

class Monitor(Handler):
    def handle(self, problem):
        if problem == "lost pencil":
            return "monitor: borrow mine"
        return super().handle(problem)         # pass it along

class Teacher(Handler):
    def handle(self, problem):
        if problem in ("homework doubt", "seat change"):
            return "teacher: sorted"
        return super().handle(problem)

class Principal(Handler):
    def handle(self, problem):
        return f"principal: will look into '{problem}'"

chain = Monitor(Teacher(Principal()))
chain.handle("lost pencil")      # monitor handles it
chain.handle("bus late")         # goes all the way to the principal
```
### A pipeline where every step runs (middleware)
Often each handler does its part and then **always** passes the request on, like web middleware: authentication → rate limit → logging → the actual view. Any step can stop the chain by raising an error or returning early.

**Where you see it:** web framework middleware (Django, FastAPI/Starlette), Python's `logging` (loggers pass records up to their parents' handlers), customer-support escalation, event bubbling in browsers.
""",
quiz=[("What's the benefit of Chain of Responsibility over one big if/elif?", "Each handler is small and independent, and handlers can be added, removed or reordered without touching the others.")],
exercises=[
    X("chain-approval", "Expense approval chain",
      """
Expenses need approval based on the amount:
- `TeamLead` approves up to 1,000,
- `Manager` up to 10,000,
- `Director` up to 100,000,
- anything bigger returns `"rejected: too large"`.

Each handler returns `"<role> approved <amount>"` (roles: `team lead`, `manager`, `director`) or passes the request to its next handler. Build the chain with `make_chain()`.
""",
      r'''class Approver:
    def __init__(self, next_approver=None):
        self.next = next_approver

def make_chain():
    pass
''',
      r'''class Approver:
    limit, role = 0, ""
    def __init__(self, next_approver=None):
        self.next = next_approver
    def approve(self, amount):
        if amount <= self.limit:
            return f"{self.role} approved {amount}"
        if self.next:
            return self.next.approve(amount)        # pass it up the chain
        return "rejected: too large"

class TeamLead(Approver):
    limit, role = 1_000, "team lead"
class Manager(Approver):
    limit, role = 10_000, "manager"
class Director(Approver):
    limit, role = 100_000, "director"

def make_chain():
    return TeamLead(Manager(Director()))
''',
      r'''
T("small", lambda: make_chain().approve(500), "team lead approved 500")
T("boundary", lambda: make_chain().approve(1000), "team lead approved 1000")
T("medium", lambda: make_chain().approve(5000), "manager approved 5000")
T("big", lambda: make_chain().approve(99999), "director approved 99999")
T("too big", lambda: make_chain().approve(10**6), "rejected: too large")
''',
      ["Give each class a limit and a role; the base class does the compare-or-forward logic.", "make_chain returns TeamLead(Manager(Director()))."]),
])

L(id="mediator", part="behavioral", title="Mediator", tagline="The air-traffic controller",
body="""
### The story
Planes at an airport **don't talk to every other plane** ("are you landing? I'm taking off!"). That would be chaos with 50 planes. Instead, everyone talks only to the **control tower**, which coordinates them all.

**Mediator: objects communicate through one central coordinator instead of referring to each other directly.** This turns a messy web of connections into a tidy star.

```text
 without a mediator: everyone knows everyone      with a mediator: a star
   A ── B                                          A   B
   │ ╲╱ │                                           ╲ ╱
   │ ╱╲ │                                         [ Tower ]
   C ── D                                           ╱ ╲
                                                   C   D
```
### A class chat room
```python
class ChatRoom:                                   # the MEDIATOR
    def __init__(self):
        self.members = {}
    def join(self, user):
        self.members[user.name] = user
        user.room = self
    def send(self, sender, text, to=None):
        targets = [self.members[to]] if to else [u for u in self.members.values() if u is not sender]
        for u in targets:
            u.inbox.append(f"{sender.name}: {text}")

class Student:
    def __init__(self, name):
        self.name, self.inbox, self.room = name, [], None
    def say(self, text, to=None):
        self.room.send(self, text, to)            # talks only to the mediator

room = ChatRoom()
asha, ravi = Student("Asha"), Student("Ravi")
room.join(asha); room.join(ravi)
asha.say("hi all")                                # Ravi gets it
```
**Where you see it:** chat rooms, GUI dialogs (a form controller coordinating text boxes and buttons), air-traffic control, game lobbies.

> **Mediator vs Observer:** Observer broadcasts "something happened" to anyone listening. A Mediator actively **coordinates** who talks to whom, often with rules.
""",
quiz=[("What problem does a Mediator solve?", "Too many direct connections between objects (N×N). Each object only knows the mediator, so the objects stay simple and reusable.")],
exercises=[
    X("mediator-tower", "Airport control tower",
      """
Write `Tower` with `request_landing(plane)`, which allows **one plane on the runway at a time**:
- if the runway is free, give it to the plane and return `"<id> cleared to land"`,
- otherwise, add the plane to a waiting queue and return `"<id> hold"`.

`runway_free()` is called when the current plane leaves. It clears the runway, and if a plane is waiting, the **first one in the queue** gets the runway; return `"<id> cleared to land"` for it (or `"runway empty"`).

`Plane(id, tower)` has `land()`, which calls the tower. Planes never talk to each other.
""",
      r'''from collections import deque

class Tower:
    pass

class Plane:
    def __init__(self, id, tower):
        self.id, self.tower = id, tower
    def land(self):
        return self.tower.request_landing(self)
''',
      r'''from collections import deque

class Tower:
    def __init__(self):
        self.on_runway = None
        self.waiting = deque()
    def request_landing(self, plane):
        if self.on_runway is None:
            self.on_runway = plane
            return f"{plane.id} cleared to land"
        self.waiting.append(plane)
        return f"{plane.id} hold"
    def runway_free(self):
        self.on_runway = None
        if self.waiting:
            self.on_runway = self.waiting.popleft()
            return f"{self.on_runway.id} cleared to land"
        return "runway empty"

class Plane:
    def __init__(self, id, tower):
        self.id, self.tower = id, tower
    def land(self):
        return self.tower.request_landing(self)
''',
      r'''
def _run():
    t = Tower(); a, b, c = Plane("AI101", t), Plane("6E202", t), Plane("UK303", t)
    return [a.land(), b.land(), c.land(), t.runway_free(), t.runway_free(), t.runway_free()]
T("one at a time, in order", _run, ["AI101 cleared to land", "6E202 hold", "UK303 hold", "6E202 cleared to land", "UK303 cleared to land", "runway empty"])
def _again():
    t = Tower(); p = Plane("A", t); p.land(); t.runway_free(); return Plane("B", t).land()
T("free runway is reused", _again, "B cleared to land")
''',
      ["The tower stores the plane on the runway plus a deque of waiting planes.", "runway_free pops from the left of the queue."]),
])

L(id="memento", part="behavioral", title="Memento", tagline="Save game, load game",
body="""
### The story
Before fighting the big boss in a video game, you **save the game**. If you lose, you **load** the save and you're back exactly where you were. The save file is a **snapshot**. You can't edit what's inside it; you can only restore it.

**Memento: capture an object's internal state in a snapshot so it can be restored later, without exposing the object's internals.**

```python
from dataclasses import dataclass

@dataclass(frozen=True)              # frozen: a save file must not be changed
class Snapshot:
    level: int
    health: int
    items: tuple

class Game:                          # the ORIGINATOR
    def __init__(self):
        self.level, self.health, self.items = 1, 100, []
    def save(self) -> Snapshot:
        return Snapshot(self.level, self.health, tuple(self.items))   # copy the state
    def load(self, snap: Snapshot):
        self.level, self.health, self.items = snap.level, snap.health, list(snap.items)

class SaveSlots:                     # the CARETAKER: stores snapshots and never looks inside
    def __init__(self): self.slots = {}
    def store(self, name, snap): self.slots[name] = snap
    def get(self, name): return self.slots[name]

g = Game(); slots = SaveSlots()
g.level, g.items = 5, ["sword"]
slots.store("before boss", g.save())
g.health = 0                          # lost the fight 😢
g.load(slots.get("before boss"))      # back to level 5 with full health
```
**Memento vs Command for undo:** Command stores **how to reverse an action**. Memento stores **a whole snapshot**. Mementos are simpler but use more memory, so they work well for small states or periodic checkpoints.

**Where you see it:** game saves, editor "revert to saved", database transactions (savepoints), form drafts.
""",
quiz=[("Why make the snapshot immutable and copy lists into it?", "If the snapshot shared the live list, later changes to the game would silently change the 'saved' state too.")],
exercises=[
    X("memento-editor", "Drawing app checkpoints",
      """
`Canvas` has `shapes` (a list) and `color` (a string). Write:
- `Canvas.save()`, which returns an **immutable** snapshot (copy the list!),
- `Canvas.restore(snapshot)`,
- `Checkpoints` (the caretaker) with `push(snapshot)` and `pop()`, which returns the latest snapshot, or `None` if there is none.

Changing the canvas after saving must not affect saved snapshots.
""",
      r'''class Canvas:
    def __init__(self):
        self.shapes, self.color = [], "black"
    def draw(self, shape):
        self.shapes.append(shape)

class Checkpoints:
    pass
''',
      r'''from dataclasses import dataclass

@dataclass(frozen=True)
class CanvasSnapshot:
    shapes: tuple
    color: str

class Canvas:
    def __init__(self):
        self.shapes, self.color = [], "black"
    def draw(self, shape):
        self.shapes.append(shape)
    def save(self):
        return CanvasSnapshot(tuple(self.shapes), self.color)   # a frozen copy
    def restore(self, snap):
        self.shapes, self.color = list(snap.shapes), snap.color

class Checkpoints:
    def __init__(self): self._stack = []
    def push(self, snap): self._stack.append(snap)
    def pop(self): return self._stack.pop() if self._stack else None
''',
      r'''
def _run():
    c, cp = Canvas(), Checkpoints()
    c.draw("circle"); cp.push(c.save())
    c.draw("square"); c.color = "red"; cp.push(c.save())
    c.draw("star"); c.color = "blue"
    c.restore(cp.pop()); a = (list(c.shapes), c.color)
    c.restore(cp.pop()); b = (list(c.shapes), c.color)
    return [a, b, cp.pop()]
T("checkpoints restore in reverse order", _run, [(["circle", "square"], "red"), (["circle"], "black"), None])
def _immutable():
    c = Canvas(); c.draw("x"); s = c.save(); c.draw("y")
    try:
        s.color = "z"; return False
    except Exception:
        return len(s.shapes) == 1
C("snapshots are frozen copies", _immutable, "use a frozen dataclass and copy the list into a tuple")
''',
      ["A frozen dataclass makes a good snapshot.", "Copy the shapes list into a tuple when saving, and back into a list when restoring."]),
])

L(id="visitor", part="behavioral", title="Visitor", tagline="A health inspector visiting different shops",
body="""
### The story
A **health inspector** visits a bakery, a restaurant and a juice shop. Each needs a different check. Next month a **tax inspector** visits the same shops with different checks. The shops don't change; new **visitors** bring new operations.

**Visitor: add new operations to a group of classes without changing those classes.** Each operation lives in its own visitor.

### GoF style (double dispatch)
```python
class Circle:
    def __init__(self, r): self.r = r
    def accept(self, visitor): return visitor.visit_circle(self)

class Square:
    def __init__(self, s): self.s = s
    def accept(self, visitor): return visitor.visit_square(self)

class AreaVisitor:                         # operation 1
    def visit_circle(self, c): return 3.14 * c.r ** 2
    def visit_square(self, s): return s.s ** 2

class SvgVisitor:                          # operation 2, added WITHOUT touching the shapes
    def visit_circle(self, c): return f'<circle r="{c.r}"/>'
    def visit_square(self, s): return f'<rect width="{s.s}"/>'

shapes = [Circle(1), Square(2)]
[s.accept(AreaVisitor()) for s in shapes]        # [3.14, 4]
```
### 🐍 Pythonic shortcut: `functools.singledispatch`
```python
from functools import singledispatch

@singledispatch
def area(shape):
    raise TypeError(f"unknown shape {type(shape).__name__}")

@area.register
def _(shape: Circle): return 3.14 * shape.r ** 2

@area.register
def _(shape: Square): return shape.s ** 2
```
**Where you see it:** compilers and linters walking a syntax tree (Python's own `ast.NodeVisitor`!), exporting a document to PDF/HTML/Markdown, tax or pricing calculations over different item types.

> Trade-off: adding a new **operation** is easy (a new visitor), but adding a new **class** means updating every visitor.
""",
quiz=[("When is Visitor a good fit?", "When the classes are stable but you keep adding new operations over them (exports, reports, analysis)."),
      ("What Python stdlib class uses Visitor?", "`ast.NodeVisitor`: `visit_Name`, `visit_Call`, etc. are called for each node type.")],
exercises=[
    X("visitor-cart", "Cart visitors: tax and weight",
      """
Items: `Book(price)`, `Food(price, kg)` and `Gadget(price, kg)`. Each has `accept(visitor)` calling `visitor.visit_book(self)`, `visit_food` or `visit_gadget`.

Write two visitors:
- `TaxVisitor`: books 0% tax, food 5%, gadgets 18%. It returns the tax amount, rounded to 2 decimals.
- `ShippingWeightVisitor`: books weigh 0.5 kg each; food and gadgets use their `kg`.

Write `total(items, visitor)`, which returns the rounded sum of `item.accept(visitor)`.
""",
      r'''class Book:
    def __init__(self, price): self.price = price

class Food:
    def __init__(self, price, kg): self.price, self.kg = price, kg

class Gadget:
    def __init__(self, price, kg): self.price, self.kg = price, kg

def total(items, visitor):
    pass
''',
      r'''class Book:
    def __init__(self, price): self.price = price
    def accept(self, v): return v.visit_book(self)

class Food:
    def __init__(self, price, kg): self.price, self.kg = price, kg
    def accept(self, v): return v.visit_food(self)

class Gadget:
    def __init__(self, price, kg): self.price, self.kg = price, kg
    def accept(self, v): return v.visit_gadget(self)

class TaxVisitor:
    def visit_book(self, b): return 0
    def visit_food(self, f): return round(f.price * 0.05, 2)
    def visit_gadget(self, g): return round(g.price * 0.18, 2)

class ShippingWeightVisitor:
    def visit_book(self, b): return 0.5
    def visit_food(self, f): return f.kg
    def visit_gadget(self, g): return g.kg

def total(items, visitor):
    return round(sum(item.accept(visitor) for item in items), 2)
''',
      r'''
_cart = lambda: [Book(300), Food(200, 2), Gadget(1000, 1.5), Book(100)]
T("tax", lambda: total(_cart(), TaxVisitor()), 190.0)
T("weight", lambda: total(_cart(), ShippingWeightVisitor()), 4.5)
T("empty cart", lambda: total([], TaxVisitor()), 0)
''',
      ["Each item's accept calls the matching visit_* method on the visitor.", "total sums item.accept(visitor) for all items."]),
])
