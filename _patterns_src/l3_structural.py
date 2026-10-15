from core import L, X

L(id="adapter", part="structural", title="Adapter", tagline="A travel plug adapter for code",
body="""
### The story
You travel to the UK with your Indian phone charger. The UK sockets have a **different shape**! You don't rebuild your charger or the wall. You buy a small **travel adapter** that fits both.

**Adapter: wrap an object with an incompatible interface so it looks like the interface your code expects.** It's very common when using **third-party libraries** or **old code** you can't change.

### Example: two payment companies with different APIs
```python
from typing import Protocol

class PaymentGateway(Protocol):            # what OUR app expects
    def pay(self, amount_rupees: float) -> str: ...

class PayFastSDK:                          # third-party library 1 (can't change it)
    def make_payment(self, paise: int) -> dict:
        return {"status": "ok", "ref": f"PF-{paise}"}

class OldBankAPI:                          # third-party library 2 (completely different)
    def transfer(self, amount, currency="INR") -> str:
        return f"BANK-{amount}-{currency}"

class PayFastAdapter:                      # makes PayFast look like PaymentGateway
    def __init__(self, sdk: PayFastSDK):
        self.sdk = sdk
    def pay(self, amount_rupees):
        result = self.sdk.make_payment(int(amount_rupees * 100))   # convert rupees to paise
        return result["ref"]

class OldBankAdapter:
    def __init__(self, api: OldBankAPI):
        self.api = api
    def pay(self, amount_rupees):
        return self.api.transfer(amount_rupees)

def checkout(gateway: PaymentGateway, total):
    return gateway.pay(total)               # works with either; it never sees the SDKs

checkout(PayFastAdapter(PayFastSDK()), 99.5)     # 'PF-9950'
```
```text
 Your code ──calls──► pay()  [Adapter]  ──translates──► make_payment(paise)  [3rd-party SDK]
```
### Why it's great
- Your app depends on **your own interface**, not on the library's (DIP again!).
- Switching providers means writing **one new adapter**.
- In tests, you can use a fake gateway.
""",
quiz=[
    ("You switch from one SMS provider to another with a different API. What changes if you used an Adapter?", "Only the adapter class (write a new one). The rest of the app keeps calling your own `send()` interface."),
    ("Adapter vs Decorator?", "An Adapter **changes the interface** to fit. A Decorator **keeps the same interface** and adds behaviour."),
],
exercises=[
    X("adapter-temps", "Adapt a Fahrenheit sensor",
      """
Your weather app expects sensors with `celsius()` (returning a float rounded to 1 decimal place). A company gives you `FahrenheitSensor` with a `read_f()` method, which you **can't** modify. Write `FahrenheitAdapter(sensor)` so it works with `average_temp(sensors)`, which is already written.

C = (F − 32) × 5 / 9.
""",
      r'''class CelsiusSensor:
    def __init__(self, c): self.c = c
    def celsius(self): return self.c

class FahrenheitSensor:          # third-party: don't change
    def __init__(self, f): self.f = f
    def read_f(self): return self.f

def average_temp(sensors):
    return round(sum(s.celsius() for s in sensors) / len(sensors), 1)

class FahrenheitAdapter:
    pass
''',
      r'''class CelsiusSensor:
    def __init__(self, c): self.c = c
    def celsius(self): return self.c

class FahrenheitSensor:
    def __init__(self, f): self.f = f
    def read_f(self): return self.f

def average_temp(sensors):
    return round(sum(s.celsius() for s in sensors) / len(sensors), 1)

class FahrenheitAdapter:
    def __init__(self, sensor):
        self.sensor = sensor                  # wrap the incompatible object
    def celsius(self):
        return round((self.sensor.read_f() - 32) * 5 / 9, 1)   # translate
''',
      r'''
T("boiling point", lambda: FahrenheitAdapter(FahrenheitSensor(212)).celsius(), 100.0)
T("mixed sensors", lambda: average_temp([CelsiusSensor(20), FahrenheitAdapter(FahrenheitSensor(86))]), 25.0)
C("FahrenheitSensor not modified", lambda: not hasattr(FahrenheitSensor, "celsius"), "don't add celsius() to the third-party class")
''',
      ["Store the wrapped sensor in __init__.", "celsius() calls sensor.read_f() and converts the result."]),
])

L(id="decorator", part="structural", title="Decorator", tagline="Toppings on a pizza",
body="""
### The story
Start with a **plain pizza** (₹200). Add cheese (+₹40), then olives (+₹30), then jalapeños (+₹25). Each topping **wraps** the pizza and adds a little to the price and the description. It's still "a pizza" at every step, so you can keep adding.

**Decorator: wrap an object in another object with the same interface, adding behaviour before or after delegating to the inner one.** You can stack wrappers in any combination, so you don't need a class for every combination (`CheeseOlivePizza`, `CheeseJalapenoPizza`… would explode!).

### The object decorator (GoF style)
```python
class Pizza:
    def cost(self): return 200
    def name(self): return "pizza"

class Topping:                                # base decorator: same interface as Pizza
    def __init__(self, inner):
        self.inner = inner
    def cost(self): return self.inner.cost()
    def name(self): return self.inner.name()

class Cheese(Topping):
    def cost(self): return self.inner.cost() + 40
    def name(self): return self.inner.name() + " + cheese"

class Olives(Topping):
    def cost(self): return self.inner.cost() + 30
    def name(self): return self.inner.name() + " + olives"

order = Olives(Cheese(Pizza()))
print(order.name(), order.cost())             # pizza + cheese + olives 270
```
```text
 Olives ──wraps──► Cheese ──wraps──► Pizza
 cost() = 30 +    ( 40 +            200 )
```
### Python's `@decorator` syntax: the same idea for functions
```python
import functools, time

def timed(func):
    @functools.wraps(func)                 # keep the original name and docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)     # call the wrapped function
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timed                                     # same as: slow_add = timed(slow_add)
def slow_add(a, b):
    return a + b
```
Real-world uses: logging, caching (`@functools.cache`), retries, auth checks (`@login_required` in Django), web routes (`@app.get("/")`).
""",
quiz=[
    ("Why are decorators better than subclasses for pizza toppings?", "Subclasses would need one class per **combination** (which explodes quickly). Decorators combine freely at runtime: `Olives(Cheese(Pizza()))`."),
    ("What does `@functools.wraps` do?", "It copies the wrapped function's name, docstring and other metadata to the wrapper, so debugging and documentation still show the real function."),
],
exercises=[
    X("decorator-coffee", "Coffee with add-ons",
      """
`Coffee` has `cost()` = 50 and `describe()` = `"coffee"`. Write decorators:
- `Milk` (+10, `" + milk"`), `Sugar` (+5, `" + sugar"`), `ExtraShot` (+25, `" + extra shot"`),

so that `Sugar(Milk(Coffee()))` gives cost 65 and describes as `"coffee + milk + sugar"`. Decorators must stack in **any** order and **any** number of times.
""",
      r'''class Coffee:
    def cost(self): return 50
    def describe(self): return "coffee"

class AddOn:
    pass
''',
      r'''class Coffee:
    def cost(self): return 50
    def describe(self): return "coffee"

class AddOn:                                 # base decorator: wraps any beverage
    price, label = 0, ""
    def __init__(self, inner):
        self.inner = inner
    def cost(self):
        return self.inner.cost() + self.price
    def describe(self):
        return f"{self.inner.describe()} + {self.label}"

class Milk(AddOn):
    price, label = 10, "milk"
class Sugar(AddOn):
    price, label = 5, "sugar"
class ExtraShot(AddOn):
    price, label = 25, "extra shot"
''',
      r'''
T("milk + sugar", lambda: (Sugar(Milk(Coffee())).cost(), Sugar(Milk(Coffee())).describe()), (65, "coffee + milk + sugar"))
T("double shot", lambda: ExtraShot(ExtraShot(Coffee())).cost(), 100)
T("order matters for description", lambda: Milk(Sugar(Coffee())).describe(), "coffee + sugar + milk")
T("plain", lambda: Coffee().cost(), 50)
''',
      ["A base AddOn stores `inner` and delegates to it.", "Each add-on adds its price to inner.cost() and its label to inner.describe()."]),
    X("decorator-retry", "Function decorator: @count_calls",
      """
Write a function decorator `count_calls` that counts how many times the decorated function is called, stored as an attribute `calls` on the wrapper. It must preserve the function's `__name__` (use `functools.wraps`) and pass all arguments through.
""",
      r'''import functools

def count_calls(func):
    pass

@count_calls
def greet(name, punctuation="!"):
    return f"hi {name}{punctuation}"
''',
      r'''import functools

def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def greet(name, punctuation="!"):
    return f"hi {name}{punctuation}"
''',
      r'''
def _run():
    greet.calls = 0
    a = greet("asha"); b = greet("ravi", punctuation="?")
    return [a, b, greet.calls]
T("counts and passes args", _run, ["hi asha!", "hi ravi?", 2])
T("keeps the name", lambda: greet.__name__, "greet")
''',
      ["Define wrapper(*args, **kwargs) inside, and increment wrapper.calls.", "Set wrapper.calls = 0 before returning wrapper."]),
])

L(id="facade", part="structural", title="Facade", tagline="One reception desk instead of ten offices",
body="""
### The story
To get admission in a school you'd normally need the accounts office, the library card office, the uniform shop, the transport desk… Instead, a friendly **reception desk** says: _"Give me the form, I'll handle everything."_ The offices still exist, but you only talk to **one desk**.

**Facade: a simple front door to a complicated system.** It doesn't hide the subsystems from experts; it just gives normal users an easy path.

```python
class Inventory:
    def reserve(self, item): return f"reserved {item}"
class Payment:
    def charge(self, amount): return f"charged {amount}"
class Shipping:
    def schedule(self, item, address): return f"shipping {item} to {address}"
class Email:
    def send(self, to, text): return f"emailed {to}"

class ShopFacade:                                   # the reception desk
    def __init__(self):
        self.inventory, self.payment = Inventory(), Payment()
        self.shipping, self.email = Shipping(), Email()

    def buy(self, item, amount, address, email):
        return [
            self.inventory.reserve(item),
            self.payment.charge(amount),
            self.shipping.schedule(item, address),
            self.email.send(email, "order placed"),
        ]

ShopFacade().buy("book", 299, "Pune", "asha@x.com")   # one call does it all
```
### Real-world facades in Python
- `requests.get(url)` is a facade over sockets, TLS, HTTP parsing, connection pools…
- `shutil.copytree` is a facade over many low-level file operations.
- A "service layer" class in a web app (`OrderService.place_order(...)`) is usually a facade.

> **Facade vs Adapter:** an Adapter makes **one** interface fit another. A Facade makes **many** things simple behind **one new** interface.
""",
quiz=[("Does a Facade prevent using the subsystems directly?", "No. It's a convenience entry point. Advanced code can still use the subsystems when needed.")],
exercises=[
    X("facade-movie", "Home theatre facade",
      """
Subsystems are given. Write `HomeTheater(projector, sound, lights)` with:
- `watch(movie)`: dims the lights to 10, turns on the projector, sets the sound volume to 20, and returns `"Playing <movie>"`,
- `end()`: turns off the projector, sets the lights to 100, and returns `"Goodbye"`.
""",
      r'''class Projector:
    def __init__(self): self.on = False
    def power(self, on): self.on = on
class Sound:
    def __init__(self): self.volume = 0
    def set_volume(self, v): self.volume = v
class Lights:
    def __init__(self): self.level = 100
    def dim(self, level): self.level = level

class HomeTheater:
    pass
''',
      r'''class Projector:
    def __init__(self): self.on = False
    def power(self, on): self.on = on
class Sound:
    def __init__(self): self.volume = 0
    def set_volume(self, v): self.volume = v
class Lights:
    def __init__(self): self.level = 100
    def dim(self, level): self.level = level

class HomeTheater:
    def __init__(self, projector, sound, lights):
        self.projector, self.sound, self.lights = projector, sound, lights
    def watch(self, movie):
        self.lights.dim(10)
        self.projector.power(True)
        self.sound.set_volume(20)
        return f"Playing {movie}"
    def end(self):
        self.projector.power(False)
        self.lights.dim(100)
        return "Goodbye"
''',
      r'''
def _run():
    p, s, l = Projector(), Sound(), Lights()
    ht = HomeTheater(p, s, l)
    a = ht.watch("Inception"); mid = (p.on, s.volume, l.level)
    b = ht.end(); end = (p.on, l.level)
    return [a, mid, b, end]
T("one call controls everything", _run, ["Playing Inception", (True, 20, 10), "Goodbye", (False, 100)])
C("HomeTheater uses the given subsystems", lambda: (lambda l: (HomeTheater(Projector(), Sound(), l).watch("x"), l.level)[1] == 10)(Lights()))
''',
      ["Store the three subsystems, then call their methods in order inside watch() and end()."]),
])

L(id="proxy", part="structural", title="Proxy", tagline="A stand-in that controls access",
body="""
### The story
A celebrity has a **manager**. You don't call the celebrity directly; the manager answers. The manager can **check** whether you're allowed (protection), **remember** common answers so the celebrity isn't disturbed (caching), or only call the celebrity when **really needed** (lazy loading). To you it feels like talking to the celebrity.

**Proxy: an object with the same interface as the real object that controls access to it.**

### Three common proxies
```python
class RealImage:
    def __init__(self, path):
        print(f"loading {path} from disk…")     # slow!
        self.path = path
    def show(self):
        return f"showing {self.path}"

class LazyImage:                                 # 1) VIRTUAL proxy: create only when first needed
    def __init__(self, path):
        self.path, self._real = path, None
    def show(self):
        if self._real is None:
            self._real = RealImage(self.path)    # loaded on first use
        return self._real.show()

class CachedWeather:                             # 2) CACHING proxy
    def __init__(self, api):
        self.api, self.cache = api, {}
    def today(self, city):
        if city not in self.cache:
            self.cache[city] = self.api.today(city)   # call the slow API only once per city
        return self.cache[city]

class ProtectedDocs:                             # 3) PROTECTION proxy
    def __init__(self, docs, user_role):
        self.docs, self.role = docs, user_role
    def read(self, name):
        if self.role != "teacher":
            raise PermissionError("teachers only")
        return self.docs.read(name)
```
**Proxy vs Decorator:** they're built the same way (both wrap). The difference is intent. A **proxy controls access** (when, whether, how often); a **decorator adds features**.

🐍 Python has a built-in caching proxy for functions: `@functools.cache`.
""",
quiz=[("Name the three proxy types from the lesson.", "Virtual (lazy creation), caching, and protection (permission checks). Remote proxies (an object standing in for one on another computer) are a fourth.")],
exercises=[
    X("proxy-cache", "A caching proxy with counters",
      """
`SlowDictionary.lookup(word)` is slow (pretend it calls the internet). Write `CachedDictionary(real)` with the same `lookup(word)` that calls the real one **only the first time** for each word. Also keep two counters: `hits` (answered from the cache) and `misses` (had to ask the real one).
""",
      r'''class SlowDictionary:
    def __init__(self):
        self.calls = 0
    def lookup(self, word):
        self.calls += 1
        return f"meaning of {word}"

class CachedDictionary:
    pass
''',
      r'''class SlowDictionary:
    def __init__(self):
        self.calls = 0
    def lookup(self, word):
        self.calls += 1
        return f"meaning of {word}"

class CachedDictionary:
    def __init__(self, real):
        self.real, self.cache = real, {}
        self.hits = self.misses = 0
    def lookup(self, word):
        if word in self.cache:
            self.hits += 1
        else:
            self.misses += 1
            self.cache[word] = self.real.lookup(word)    # only on a cache miss
        return self.cache[word]
''',
      r'''
def _run():
    real = SlowDictionary(); d = CachedDictionary(real)
    out = [d.lookup("cat"), d.lookup("dog"), d.lookup("cat"), d.lookup("cat")]
    return [out[2], real.calls, d.hits, d.misses]
T("cache works", _run, ["meaning of cat", 2, 2, 2])
T("same answer as the real one", lambda: CachedDictionary(SlowDictionary()).lookup("sun"), "meaning of sun")
''',
      ["Keep a dict cache; check it before calling the real object."]),
])

L(id="composite", part="structural", title="Composite", tagline="Boxes inside boxes",
body="""
### The story
Your computer has **files** and **folders**. A folder can contain files **and other folders**. When you ask "how big is this folder?", it adds up its files **and** asks each sub-folder the same question. To you, a file and a folder both answer `size()`.

**Composite: treat single objects and groups of objects the same way, using a tree.**

```python
from abc import ABC, abstractmethod

class Item(ABC):                        # the common interface
    @abstractmethod
    def size(self) -> int: ...

class File(Item):                       # a LEAF: no children
    def __init__(self, name, kb):
        self.name, self.kb = name, kb
    def size(self):
        return self.kb

class Folder(Item):                     # a COMPOSITE: contains Items (files or folders!)
    def __init__(self, name):
        self.name, self.children = name, []
    def add(self, item):
        self.children.append(item)
        return self
    def size(self):
        return sum(child.size() for child in self.children)   # recursion does the magic

root = Folder("school").add(File("notes.txt", 5)).add(Folder("photos").add(File("trip.jpg", 300)))
root.size()      # 305
```
```text
 school/            size = 5 + 300
 ├── notes.txt  5
 └── photos/        size = 300
     └── trip.jpg 300
```
**Where you see it:** folders, menus with sub-menus, company org charts, UI layouts (panels containing buttons and panels), maths expressions (`(2 + 3) * 4` is a tree).
""",
quiz=[("What makes Composite work so neatly?", "Leaves and groups share **one interface**, and groups delegate to their children recursively, so client code never needs to check 'is this a file or a folder?'.")],
exercises=[
    X("composite-menu", "Restaurant menu with sub-menus",
      """
Build a menu tree:
- `Dish(name, price)` with `total()` = price and `count()` = 1,
- `Menu(name)` with `add(item)` (returns self for chaining), `total()` = the sum of the children's totals, and `count()` = the total number of **dishes** inside, however deeply nested.

Also write `cheapest(menu)`, returning the name of the cheapest `Dish` anywhere in the tree.
""",
      r'''class Dish:
    pass

class Menu:
    pass

def cheapest(menu):
    pass
''',
      r'''class Dish:
    def __init__(self, name, price):
        self.name, self.price = name, price
    def total(self): return self.price
    def count(self): return 1
    def dishes(self): return [self]

class Menu:
    def __init__(self, name):
        self.name, self.children = name, []
    def add(self, item):
        self.children.append(item)
        return self
    def total(self): return sum(c.total() for c in self.children)
    def count(self): return sum(c.count() for c in self.children)
    def dishes(self): return [d for c in self.children for d in c.dishes()]

def cheapest(menu):
    return min(menu.dishes(), key=lambda d: d.price).name
''',
      r'''
def _m():
    drinks = Menu("drinks").add(Dish("tea", 20)).add(Dish("juice", 60))
    snacks = Menu("snacks").add(Dish("samosa", 15)).add(Menu("combos").add(Dish("thali", 150)))
    return Menu("main").add(drinks).add(snacks).add(Dish("dosa", 80))
T("total", lambda: _m().total(), 325)
T("count", lambda: _m().count(), 5)
T("cheapest", lambda: cheapest(_m()), "samosa")
T("empty menu", lambda: (Menu("x").total(), Menu("x").count()), (0, 0))
''',
      ["Both classes need total() and count(); Menu sums its children's.", "For cheapest, add a method that lists all dishes recursively."]),
])

L(id="bridge", part="structural", title="Bridge", tagline="Separate the remote from the TV",
body="""
### The story
A **TV remote** and a **TV** are separate things. Any remote (basic or fancy with voice) can control any TV brand (Sony or Samsung). If they were glued together you'd need a class for every combination: `BasicSonyRemote`, `VoiceSamsungRemote`… With 3 remotes × 4 TVs, that's **12 classes**. Separate them and you need **3 + 4 = 7**.

**Bridge: split something that varies in two independent directions into two hierarchies, and connect them with composition** (the remote *has a* device).

```python
class Device:                                # implementation side
    def __init__(self): self.volume, self.on = 10, False
    def toggle(self): self.on = not self.on
class Sony(Device):
    brand = "Sony"
class Samsung(Device):
    brand = "Samsung"

class Remote:                                # abstraction side, which HAS a device (the bridge)
    def __init__(self, device: Device):
        self.device = device
    def power(self):
        self.device.toggle()
    def volume_up(self):
        self.device.volume += 1

class VoiceRemote(Remote):                   # extend the remotes freely…
    def say(self, command):
        if command == "louder":
            for _ in range(5):
                self.volume_up()

VoiceRemote(Samsung()).say("louder")         # …and combine with any device
```
**Where you see it:** notifications (Urgent / Normal) × channels (Email / SMS), shapes × renderers (screen / printer), database query layer × drivers.

> Bridge is "composition over inheritance" applied on purpose, when you can see **two independent axes of change**.
""",
quiz=[("You have 4 shapes and 3 renderers. How many classes with inheritance only? With Bridge?", "Inheritance only: 4 × 3 = 12 combination classes. Bridge: 4 + 3 = 7 classes, with a shape *having* a renderer.")],
exercises=[
    X("bridge-notify", "Messages × channels",
      """
Messages come in two kinds and can go through two channels:
- **Channels:** `EmailChannel` and `SmsChannel`, each with `deliver(text)` returning `"EMAIL: <text>"` or `"SMS: <text>"`.
- **Messages:** `Message(channel)` with `send(text)` that delivers `text` unchanged, and `UrgentMessage(Message)` that delivers `"URGENT! " + text.upper()`.

Any message must work with any channel, so there must be **no** classes like `UrgentSms`.
""",
      r'''class EmailChannel:
    pass

class SmsChannel:
    pass

class Message:
    pass

class UrgentMessage(Message):
    pass
''',
      r'''class EmailChannel:
    def deliver(self, text): return f"EMAIL: {text}"

class SmsChannel:
    def deliver(self, text): return f"SMS: {text}"

class Message:
    def __init__(self, channel):
        self.channel = channel                  # the bridge: a message HAS a channel
    def format(self, text):
        return text
    def send(self, text):
        return self.channel.deliver(self.format(text))

class UrgentMessage(Message):
    def format(self, text):
        return "URGENT! " + text.upper()
''',
      r'''
T("normal email", lambda: Message(EmailChannel()).send("hi"), "EMAIL: hi")
T("urgent sms", lambda: UrgentMessage(SmsChannel()).send("fire drill"), "SMS: URGENT! FIRE DRILL")
T("urgent email", lambda: UrgentMessage(EmailChannel()).send("x"), "EMAIL: URGENT! X")
C("UrgentMessage is a Message", lambda: issubclass(UrgentMessage, Message))
''',
      ["Message stores a channel and calls channel.deliver(...).", "UrgentMessage only changes how the text is formatted."]),
])

L(id="flyweight", part="structural", title="Flyweight", tagline="Share what's the same, store only what's different",
body="""
### The story
A forest in a video game has **1 million trees**, but only **3 kinds** of tree (oak, pine, palm). Each kind's 3D model and texture is **huge**. Storing a copy in every tree would crash your computer. Instead, store each kind **once** and let each tree remember only its **own small details**: its position.

**Flyweight: share the common heavy part (intrinsic state) between many objects; keep the unique light part (extrinsic state) per object.**

```python
class TreeType:                          # the shared, heavy part (the flyweight)
    def __init__(self, name, texture):
        self.name, self.texture = name, texture

class TreeFactory:
    _types = {}
    @classmethod
    def get(cls, name, texture):
        key = (name, texture)
        if key not in cls._types:
            cls._types[key] = TreeType(name, texture)   # created only once per kind
        return cls._types[key]

class Tree:                              # the light part: just position + a reference
    __slots__ = ("x", "y", "kind")       # __slots__ makes each tree even smaller
    def __init__(self, x, y, kind):
        self.x, self.y, self.kind = x, y, kind

forest = [Tree(i, i * 2, TreeFactory.get("oak", "oak.png")) for i in range(1_000_000)]
len(TreeFactory._types)   # 1: only one TreeType object exists
```
### Python already does this for you!
- **Small integers** (−5 to 256) and many short **strings** are shared ("interned") by CPython. `a = 7; b = 7; a is b` gives True.
- `sys.intern(s)` lets you intern strings yourself.
- `@functools.cache` on a factory function is an easy flyweight factory.
""",
quiz=[("Intrinsic vs extrinsic state?", "Intrinsic = shared, doesn't change, stored in the flyweight (the tree model). Extrinsic = unique per use, passed in or stored per object (the tree's position).")],
exercises=[
    X("flyweight-chars", "Character styles in a text editor",
      """
A document has thousands of characters, but only a few **styles** (font, size, bold). Write:
- `Style(font, size, bold)`,
- `StyleFactory.get(font, size, bold)`, which returns the **same** Style object for the same combination; `StyleFactory.count()` returns how many distinct styles exist,
- `Char(symbol, style)`.

Build `make_text(text, style_args)` returning a list of `Char`s that all share one style.
""",
      r'''class Style:
    pass

class StyleFactory:
    pass

class Char:
    pass

def make_text(text, style_args):
    pass
''',
      r'''class Style:
    def __init__(self, font, size, bold):
        self.font, self.size, self.bold = font, size, bold

class StyleFactory:
    _cache = {}
    @classmethod
    def get(cls, font, size, bold):
        key = (font, size, bold)
        if key not in cls._cache:
            cls._cache[key] = Style(font, size, bold)
        return cls._cache[key]
    @classmethod
    def count(cls):
        return len(cls._cache)

class Char:
    __slots__ = ("symbol", "style")
    def __init__(self, symbol, style):
        self.symbol, self.style = symbol, style

def make_text(text, style_args):
    style = StyleFactory.get(*style_args)
    return [Char(ch, style) for ch in text]
''',
      r'''
StyleFactory._cache = {} if hasattr(StyleFactory, "_cache") else None
def _run():
    a = make_text("hello world" * 100, ("Arial", 12, False))
    b = make_text("bold!", ("Arial", 12, True))
    c = make_text("again", ("Arial", 12, False))
    return [len(a), StyleFactory.count(), a[0].style is c[3].style, a[0].style is b[0].style]
T("styles are shared", _run, [1100, 2, True, False])
C("same args, same object", lambda: StyleFactory.get("Mono", 10, True) is StyleFactory.get("Mono", 10, True))
''',
      ["Cache Style objects in a dict keyed by (font, size, bold).", "Every Char keeps a reference to the shared Style."]),
])
