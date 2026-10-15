from core import L, X

# ------------------------------------------------------------------ the project code, built in 7 steps
S1 = r'''# ===== Step 1: Menu (Composite + Iterator) =====
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, replace
from typing import Protocol

@dataclass(frozen=True)
class MenuItem:                       # a LEAF of the menu tree (frozen = can't change by accident)
    id: str
    name: str
    price: float
    veg: bool = True
    def __iter__(self):               # a leaf "iterates" over just itself
        yield self

class Category:                       # a COMPOSITE: holds items AND other categories
    def __init__(self, name):
        self.name, self.children = name, []
    def add(self, *things):
        self.children.extend(things)
        return self
    def __iter__(self):               # ITERATOR: every MenuItem inside, however deep
        for child in self.children:
            yield from child
    def find(self, item_id):
        return next((i for i in self if i.id == item_id), None)
    def veg_only(self):
        return [i for i in self if i.veg]

def sample_menu():
    return Category("QuickBite").add(
        Category("Snacks").add(MenuItem("samosa", "Samosa", 20), MenuItem("fries", "French Fries", 80)),
        Category("Meals").add(
            MenuItem("thali", "Veg Thali", 150),
            MenuItem("biryani", "Chicken Biryani", 220, veg=False),
            Category("Combos").add(MenuItem("burger-combo", "Burger Combo", 199)),
        ),
        Category("Drinks").add(MenuItem("chai", "Masala Chai", 25), MenuItem("lassi", "Sweet Lassi", 60)),
    )
'''

S2 = r'''
# ===== Step 2: Pricing (Decorator for add-ons + Strategy for discounts) =====
class Priced(Protocol):
    def price(self) -> float: ...
    def label(self) -> str: ...

class Plain:                                   # turns a MenuItem into a Priced thing
    def __init__(self, item):
        self.item = item
    def price(self): return self.item.price
    def label(self): return self.item.name

class AddOn:                                   # DECORATOR base: wraps any Priced
    extra, text = 0, ""
    def __init__(self, inner):
        self.inner = inner
    def price(self): return self.inner.price() + self.extra
    def label(self): return f"{self.inner.label()} + {self.text}"

class ExtraCheese(AddOn): extra, text = 30, "extra cheese"
class ExtraSauce(AddOn): extra, text = 10, "extra sauce"
class Jumbo(AddOn): extra, text = 50, "jumbo size"

ADDONS = {"cheese": ExtraCheese, "sauce": ExtraSauce, "jumbo": Jumbo}

def make_priced(item, addons=()):
    priced = Plain(item)
    for name in addons:
        priced = ADDONS[name](priced)          # stack decorators
    return priced

class Discount(ABC):                           # STRATEGY interface
    @abstractmethod
    def apply(self, subtotal): ...

class NoDiscount(Discount):
    def apply(self, subtotal): return subtotal

class PercentOff(Discount):
    def __init__(self, percent): self.percent = percent
    def apply(self, subtotal): return subtotal * (1 - self.percent / 100)

class FlatOff(Discount):
    def __init__(self, amount, min_total=0): self.amount, self.min_total = amount, min_total
    def apply(self, subtotal): return subtotal - self.amount if subtotal >= self.min_total else subtotal

class Cart:
    def __init__(self):
        self.lines = []                        # list of (priced, qty) tuples
    def add(self, priced, qty=1):
        if qty <= 0:
            raise ValueError("qty must be positive")
        line = (priced, qty)
        self.lines.append(line)
        return line
    def remove(self, line):
        self.lines.remove(line)
    def subtotal(self):
        return sum(p.price() * q for p, q in self.lines)
    def total(self, discount=None):
        return round(max(0, (discount or NoDiscount()).apply(self.subtotal())), 2)
'''

S3 = r'''
# ===== Step 3: Orders (Builder + Prototype) =====
@dataclass(frozen=True)
class OrderLine:
    label: str
    unit_price: float
    qty: int

@dataclass(frozen=True)
class Order:
    id: str
    customer: str
    address: str
    lines: tuple
    total: float
    def reorder(self, new_id):                 # PROTOTYPE: a copy of this order with a new id
        return replace(self, id=new_id)

class OrderBuilder:                            # BUILDER: step by step, validated in build()
    def __init__(self):
        self._customer = self._address = None
        self._cart, self._discount = Cart(), NoDiscount()
    def for_customer(self, name):
        self._customer = name
        return self
    def deliver_to(self, address):
        self._address = address
        return self
    def add(self, priced, qty=1):
        self._cart.add(priced, qty)
        return self
    def from_cart(self, cart):
        self._cart = cart
        return self
    def with_discount(self, discount):
        self._discount = discount
        return self
    def build(self, order_id):
        if not self._customer:
            raise ValueError("customer is required")
        if not self._address:
            raise ValueError("address is required")
        if not self._cart.lines:
            raise ValueError("order is empty")
        lines = tuple(OrderLine(p.label(), p.price(), q) for p, q in self._cart.lines)
        return Order(order_id, self._customer, self._address, lines, self._cart.total(self._discount))
'''

S4 = r'''
# ===== Step 4: Payments (Factory + Adapter) =====
class QuickPaySDK:                     # pretend third-party UPI library (we can't edit it)
    def charge_paise(self, paise):
        return {"ok": True, "txn": f"UPI{paise}"}

class CardCoClient:                    # pretend third-party card library (we can't edit it)
    def authorize(self, amount_str):
        return f"CARD-{amount_str}"

class PaymentFactory:                  # FACTORY with self-registration
    _methods = {}
    @classmethod
    def register(cls, name):
        def deco(klass):
            cls._methods[name] = klass
            return klass
        return deco
    @classmethod
    def create(cls, name):
        if name not in cls._methods:
            raise ValueError(f"unknown payment method: {name}")
        return cls._methods[name]()

@PaymentFactory.register("upi")
class UpiPayment:                      # ADAPTER: QuickPaySDK -> our pay(amount) interface
    def __init__(self, sdk=None):
        self.sdk = sdk or QuickPaySDK()
    def pay(self, amount):
        return self.sdk.charge_paise(round(amount * 100))["txn"]

@PaymentFactory.register("card")
class CardPayment:                     # ADAPTER: CardCoClient -> pay(amount)
    def __init__(self, client=None):
        self.client = client or CardCoClient()
    def pay(self, amount):
        return self.client.authorize(f"{amount:.2f}")

@PaymentFactory.register("cash")
class CashOnDelivery:
    def pay(self, amount):
        return f"COD-{amount:.2f}"
'''

S5 = r'''
# ===== Step 5: Order lifecycle (State table + Observer) =====
TRANSITIONS = {
    "PLACED": {"PAID", "CANCELLED"},
    "PAID": {"PREPARING", "CANCELLED"},
    "PREPARING": {"OUT_FOR_DELIVERY"},
    "OUT_FOR_DELIVERY": {"DELIVERED"},
    "DELIVERED": set(),
    "CANCELLED": set(),
}

class EventBus:                        # OBSERVER: publish/subscribe
    def __init__(self):
        self._subs = defaultdict(list)
    def subscribe(self, event, fn):
        self._subs[event].append(fn)
    def publish(self, event, **data):
        for fn in list(self._subs[event]):
            try:
                fn(**data)
            except Exception:
                pass                   # one broken subscriber must not break the app

class InvalidTransition(Exception):
    pass

class OrderTracker:                    # STATE (transition-table version)
    def __init__(self, bus):
        self.bus, self.status = bus, {}
    def start(self, order_id):
        self.status[order_id] = "PLACED"
        self.bus.publish("status_changed", order_id=order_id, old=None, new="PLACED")
    def move(self, order_id, new):
        old = self.status[order_id]
        if new not in TRANSITIONS[old]:
            raise InvalidTransition(f"{old} -> {new} is not allowed")
        self.status[order_id] = new
        self.bus.publish("status_changed", order_id=order_id, old=old, new=new)
'''

S6 = r'''
# ===== Step 6: Cart undo (Command) + checkout checks (Chain of Responsibility) =====
class AddToCart:                       # COMMAND
    def __init__(self, cart, priced, qty=1):
        self.cart, self.priced, self.qty, self.line = cart, priced, qty, None
    def execute(self):
        self.line = self.cart.add(self.priced, self.qty)
    def undo(self):
        self.cart.remove(self.line)

class CartHistory:
    def __init__(self):
        self.done, self.undone = [], []
    def run(self, cmd):
        cmd.execute(); self.done.append(cmd); self.undone.clear()
    def undo(self):
        if self.done:
            cmd = self.done.pop(); cmd.undo(); self.undone.append(cmd)
    def redo(self):
        if self.undone:
            cmd = self.undone.pop(); cmd.execute(); self.done.append(cmd)

class ValidationError(Exception):
    pass

class Check:                           # CHAIN OF RESPONSIBILITY base
    def __init__(self, nxt=None):
        self.next = nxt
    def validate(self, ctx):
        if self.next:
            self.next.validate(ctx)

class NotEmpty(Check):
    def validate(self, ctx):
        if not ctx["cart"].lines:
            raise ValidationError("cart is empty")
        super().validate(ctx)

class MinimumOrder(Check):
    def __init__(self, minimum, nxt=None):
        super().__init__(nxt)
        self.minimum = minimum
    def validate(self, ctx):
        if ctx["cart"].subtotal() < self.minimum:
            raise ValidationError(f"minimum order is {self.minimum}")
        super().validate(ctx)

class DeliveryArea(Check):
    def __init__(self, cities, nxt=None):
        super().__init__(nxt)
        self.cities = cities
    def validate(self, ctx):
        if ctx["city"] not in self.cities:
            raise ValidationError(f"we don't deliver to {ctx['city']}")
        super().validate(ctx)
'''

S7 = r'''
# ===== Step 7: The app (Facade + Proxy + Singleton + Template Method) =====
class Settings:                        # SINGLETON: one shared settings object
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.min_order = 50
            cls._instance.cities = {"Pune", "Mumbai"}
        return cls._instance

class MenuService:                     # pretend this is a slow database
    def __init__(self, menu):
        self.menu, self.lookups = menu, 0
    def get(self, item_id):
        self.lookups += 1
        item = self.menu.find(item_id)
        if item is None:
            raise KeyError(f"no such item: {item_id}")
        return item

class CachedMenu:                      # PROXY: same get(), but cached
    def __init__(self, service):
        self.service, self.cache = service, {}
    def get(self, item_id):
        if item_id not in self.cache:
            self.cache[item_id] = self.service.get(item_id)
        return self.cache[item_id]

class Receipt(ABC):                    # TEMPLATE METHOD: fixed layout, variable pieces
    def render(self, order):
        return "\n".join([self.header(order), *(self.line(l) for l in order.lines), self.footer(order)])
    def header(self, order): return f"QuickBite order {order.id}"
    def footer(self, order): return f"TOTAL {order.total:.2f}"
    @abstractmethod
    def line(self, l): ...

class TextReceipt(Receipt):
    def line(self, l): return f"{l.qty} x {l.label} @ {l.unit_price:.2f}"

class SmsReceipt(Receipt):
    def header(self, order): return f"QB {order.id}"
    def line(self, l): return f"{l.qty}x {l.label}"

class QuickBite:                       # FACADE: one simple entry point for the whole system
    def __init__(self, menu, bus=None):
        self.settings = Settings()
        self.menu = CachedMenu(MenuService(menu))
        self.bus = bus or EventBus()
        self.tracker = OrderTracker(self.bus)
        self.checks = NotEmpty(MinimumOrder(self.settings.min_order, DeliveryArea(self.settings.cities)))
        self.orders, self._next = {}, 1

    def _new_id(self):
        order_id = f"QB{self._next:04d}"
        self._next += 1
        return order_id

    def place_order(self, customer, city, address, items, payment="upi", discount=None):
        cart = Cart()
        for item_id, qty, *rest in items:                      # items: (id, qty) or (id, qty, addons)
            cart.add(make_priced(self.menu.get(item_id), rest[0] if rest else ()), qty)
        self.checks.validate({"cart": cart, "city": city})     # chain of checks
        order = (OrderBuilder().for_customer(customer).deliver_to(f"{address}, {city}")
                 .from_cart(cart).with_discount(discount or NoDiscount()).build(self._new_id()))
        self.tracker.start(order.id)
        receipt = PaymentFactory.create(payment).pay(order.total)
        self.tracker.move(order.id, "PAID")
        self.orders[order.id] = order
        self.bus.publish("order_paid", order=order, receipt=receipt)
        return order

    def advance(self, order_id, new_status):
        self.tracker.move(order_id, new_status)

    def status(self, order_id):
        return self.tracker.status[order_id]

    def reorder(self, order_id, payment="upi"):
        order = self.orders[order_id].reorder(self._new_id())  # prototype
        self.tracker.start(order.id)
        receipt = PaymentFactory.create(payment).pay(order.total)
        self.tracker.move(order.id, "PAID")
        self.orders[order.id] = order
        self.bus.publish("order_paid", order=order, receipt=receipt)
        return order
'''

FULL = S1 + S2 + S3 + S4 + S5 + S6 + S7
code = lambda s: "```python\n" + s.strip("\n") + "\n```"

# ------------------------------------------------------------------ lessons
L(id="qb-overview", part="project", title="QuickBite: The Plan", tagline="We'll build a real food-ordering app, step by step",
body="""
### What we're building
**QuickBite** is the backend of a food-ordering app (like a mini Swiggy or Zomato for your school canteen). By the end, this works:
```python
app = QuickBite(sample_menu())
order = app.place_order("Asha", "Pune", "12 MG Road",
                        [("thali", 1), ("burger-combo", 2, ["cheese", "jumbo"])],
                        payment="upi", discount=PercentOff(10))
app.advance(order.id, "PREPARING")
print(TextReceipt().render(order))
```
### Requirements (what the "client" asked for)
1. A **menu** with categories inside categories (Snacks, Meals → Combos…).
2. **Add-ons** (extra cheese, jumbo size) that change the price, in any combination.
3. **Discounts** that change every festival.
4. Orders that are **validated** (customer, address, at least one item) and can be **re-ordered**.
5. **Several payment providers**, each with its own weird third-party API.
6. An order **lifecycle** (placed → paid → preparing → out for delivery → delivered) with **notifications**.
7. **Undo** in the cart, plus **checkout rules** (minimum order, delivery cities).
8. **One simple entry point** for the mobile app, cached menu lookups, shared settings, and receipts in different formats.

### Which pattern solves which requirement
| requirement | pattern(s) | step |
|---|---|---|
| nested menu, "loop over every item" | **Composite**, **Iterator** | 1 |
| add-ons in any combination | **Decorator** | 2 |
| changing discounts | **Strategy** | 2 |
| safe order creation, reorder | **Builder**, **Prototype** | 3 |
| many payment SDKs | **Factory**, **Adapter** | 4 |
| lifecycle + notifications | **State**, **Observer** | 5 |
| cart undo, checkout rules | **Command**, **Chain of Responsibility** | 6 |
| simple entry, caching, settings, receipts | **Facade**, **Proxy**, **Singleton**, **Template Method** | 7 |

> **We deliberately don't use** Visitor, Mediator, Memento, Bridge, Flyweight or Abstract Factory here. Good designers **don't force patterns** where there's no problem for them to solve. A pattern without a problem is just extra complexity. (Ideas for where they *could* fit come in the final lesson.)

### The class picture
```text
          QuickBite  (Facade)
   ┌──────────┼─────────────┬───────────────┬──────────────┐
CachedMenu  Checks chain  OrderBuilder   PaymentFactory  OrderTracker ──► EventBus ──► subscribers
 (Proxy)    (Chain)       (Builder)       (Factory)       (State)          (Observer)
   │                         │               │
MenuService ──► Category/MenuItem          UpiPayment/CardPayment (Adapters) ──► 3rd-party SDKs
               (Composite + Iterator)
Cart ◄── Plain/AddOn (Decorator)   Discount (Strategy)   AddToCart/CartHistory (Command)
```
### SOLID in this project
- **S:** each class has one job (Cart adds up totals, OrderBuilder validates and builds, OrderTracker handles status).
- **O:** new add-ons, discounts, payment methods and checks are **new classes**, with no edits.
- **L:** every `Discount` and every payment method can replace another.
- **I:** small interfaces: `Priced` has just `price()` and `label()`; a payment needs only `pay()`.
- **D:** the facade depends on abstractions (any Discount, any payment from the factory, any bus).

Each of the next lessons builds one step. The exercise gives you all the **previous steps' code ready-made**, and you write the new step.
""")

L(id="qb-step1", part="project", title="Step 1: The Menu (Composite + Iterator)", tagline="Categories inside categories",
body="""
### The problem
The menu has **categories inside categories**: Meals → Combos → Burger Combo. We need to:
- loop over **every** dish, however deeply nested (for search, or a "veg only" filter),
- find a dish by its id,

without writing special code for "is this a category or a dish?" everywhere.

### The design
- `MenuItem` (a **leaf**) is a frozen dataclass. Its `__iter__` yields just itself.
- `Category` (a **composite**) holds children, and its `__iter__` does `yield from child` for each child.

Because **both** are iterable in the same way, the category doesn't care whether a child is a dish or another category. That's the **Composite** pattern with Python's built-in **Iterator** protocol.
""" + code(S1) + """
### Things to notice
- `frozen=True` means nobody can accidentally change a dish's price in one order and affect everyone.
- `find` is just a generator expression over the whole tree.
- Adding a new sub-category needs **no code changes** at all.
""",
quiz=[("Why does MenuItem have an `__iter__` that yields itself?", "So that leaves and categories can be treated the same way: `yield from child` works whether the child is a dish or a category, with no isinstance checks.")],
exercises=[X("qb1", "Build the menu tree",
"""
Write `MenuItem` (frozen dataclass: `id`, `name`, `price`, `veg=True`, plus an `__iter__` that yields itself) and `Category(name)` with `add(*things)` (chainable), `__iter__`, `find(item_id)` (None if missing) and `veg_only()`. `sample_menu()` is provided at the bottom of the starter and must work with your classes.
""",
S1.split("@dataclass(frozen=True)")[0] + r'''@dataclass(frozen=True)
class MenuItem:
    id: str
    name: str
    price: float
    veg: bool = True
    # TODO: add __iter__ that yields self

class Category:
    def __init__(self, name):
        self.name, self.children = name, []
    # TODO: add(), __iter__(), find(), veg_only()

''' + "def sample_menu" + S1.split("def sample_menu")[1],
S1,
r'''
T("counts every dish", lambda: len(list(sample_menu())), 7)
T("finds nested combo", lambda: sample_menu().find("burger-combo").price, 199)
T("missing item", lambda: sample_menu().find("pizza"), None)
T("veg only", lambda: [i.id for i in sample_menu().veg_only()], ["samosa", "fries", "thali", "burger-combo", "chai", "lassi"])
def _frozen():
    try:
        sample_menu().find("chai").price = 1; return False
    except Exception:
        return True
C("menu items are frozen", _frozen)
''', ["MenuItem.__iter__: `yield self`.", "Category.__iter__: `for child in self.children: yield from child`."])])

L(id="qb-step2", part="project", title="Step 2: Add-ons & Discounts (Decorator + Strategy)", tagline="Extra cheese, jumbo size, festival offers",
body="""
### Add-ons: the Decorator pattern
A burger can be **plain**, **+cheese**, **+cheese +jumbo**, **+sauce +cheese**… Making one class per combination would explode. Instead:
- `Plain(item)` wraps a menu item and gives `price()` and `label()`,
- every add-on is a **decorator** that wraps any `Priced` thing and adds its extra price and text.

`ExtraCheese(Jumbo(Plain(burger)))` costs 199 + 50 + 30 = 279.

### Discounts: the Strategy pattern
Discounts change every festival, so each discount is a class with `apply(subtotal)`. The cart doesn't know which one it got. That's Strategy, and adding "Diwali 25% off" later means adding one new class.
""" + code(S2) + """
### Things to notice
- `class ExtraCheese(AddOn): extra, text = 30, "extra cheese"` puts the class body on one line. It's allowed because it's a simple assignment, and it reads nicely for tiny subclasses.
- `make_priced(item, ["cheese", "jumbo"])` turns a list of add-on names into stacked decorators. The `ADDONS` dict is a mini **factory**.
- `Cart.total()` never goes below 0, whatever discount you pass.
""",
quiz=[("Why not a `with_cheese` boolean on MenuItem?", "Then every new add-on would mean editing MenuItem (breaking open/closed), and combinations would need ever more flags. Decorators stack freely.")],
exercises=[X("qb2", "Add-ons, discounts and the cart",
"""
Using the given Step 1 code, write Step 2: `Plain`, `AddOn` (with `ExtraCheese` +30, `ExtraSauce` +10, `Jumbo` +50), `ADDONS`, `make_priced(item, addons)`, the discounts (`NoDiscount`, `PercentOff(p)`, `FlatOff(amount, min_total=0)`), and `Cart` with `add` (returns the line tuple; qty must be > 0), `remove(line)`, `subtotal()` and `total(discount=None)` (rounded to 2 decimals, never below 0).
""",
S1 + r'''
# ===== Step 2: YOUR CODE =====
class Plain:
    pass

class AddOn:
    pass

ADDONS = {}

def make_priced(item, addons=()):
    pass

class NoDiscount:
    pass

class Cart:
    pass
''',
S1 + S2,
r'''
_m = sample_menu()
_burger = lambda *a: make_priced(_m.find("burger-combo"), a)
T("plain price", lambda: _burger().price(), 199)
T("stacked add-ons", lambda: (_burger("jumbo", "cheese").price(), _burger("jumbo", "cheese").label()), (279, "Burger Combo + jumbo size + extra cheese"))
def _cart():
    c = Cart(); c.add(make_priced(_m.find("thali")), 2); c.add(_burger("cheese")); return c
T("subtotal", lambda: _cart().subtotal(), 529)
T("percent off", lambda: _cart().total(PercentOff(10)), 476.1)
T("flat off needs minimum", lambda: (_cart().total(FlatOff(100, 600)), _cart().total(FlatOff(100, 500))), (529, 429))
T("never negative", lambda: _cart().total(FlatOff(10_000)), 0)
def _remove():
    c = Cart(); line = c.add(make_priced(_m.find("chai"))); c.remove(line); return c.lines
T("remove a line", _remove, [])
def _badqty():
    try:
        Cart().add(make_priced(_m.find("chai")), 0); return False
    except ValueError:
        return True
C("qty must be positive", _badqty)
''', ["AddOn.price() = inner.price() + extra; AddOn.label() appends ' + text'.", "make_priced wraps Plain(item) in each add-on in order.", "Cart.total: round(max(0, discount.apply(subtotal)), 2)."])])

L(id="qb-step3", part="project", title="Step 3: Building Orders (Builder + Prototype)", tagline="A safe way to make orders, and 'order again' in one tap",
body="""
### Builder
An order needs a customer, an address and at least one line, plus an optional discount. The `OrderBuilder` collects these **step by step** (`for_customer(...).deliver_to(...).from_cart(...)`) and checks everything **once** in `build()`. The finished `Order` is a **frozen dataclass**: once placed, it can't be edited by accident.

Each `OrderLine` stores the label and unit price **at the time of ordering**. If the menu price changes tomorrow, old orders still show what the customer really paid.

### Prototype
"Order again" copies a past order with a new id: `order.reorder(new_id)` uses `dataclasses.replace`, which is Python's built-in "clone with changes".
""" + code(S3),
quiz=[("Why store the label and price inside OrderLine instead of a reference to MenuItem?", "Orders are historical records. If the menu changes later, the order must still show what was actually bought and paid.")],
exercises=[X("qb3", "OrderBuilder and reorder",
"""
Write Step 3: frozen dataclasses `OrderLine(label, unit_price, qty)` and `Order(id, customer, address, lines, total)` with `reorder(new_id)`, plus an `OrderBuilder` with chainable `for_customer`, `deliver_to`, `add(priced, qty=1)`, `from_cart(cart)`, `with_discount(discount)` and `build(order_id)`.

`build` raises `ValueError` if the customer, the address or the items are missing. `lines` must be a **tuple** of OrderLine, and `total` uses the cart total with the discount.
""",
S1 + S2 + r'''
# ===== Step 3: YOUR CODE =====
@dataclass(frozen=True)
class OrderLine:
    pass

@dataclass(frozen=True)
class Order:
    pass

class OrderBuilder:
    pass
''',
S1 + S2 + S3,
r'''
_m = sample_menu()
def _order():
    return (OrderBuilder().for_customer("Asha").deliver_to("MG Road")
            .add(make_priced(_m.find("thali")), 2).add(make_priced(_m.find("chai"), ["jumbo"]))
            .with_discount(PercentOff(10)).build("QB0001"))
T("lines", lambda: _order().lines, (OrderLine("Veg Thali", 150, 2), OrderLine("Masala Chai + jumbo size", 75, 1)))
T("total with discount", lambda: _order().total, 337.5)
T("reorder keeps everything but the id", lambda: (_order().reorder("QB0009").id, _order().reorder("QB0009").total), ("QB0009", 337.5))
def _missing(step):
    b = OrderBuilder().for_customer("A").deliver_to("X").add(make_priced(_m.find("chai")))
    if step == "customer": b = OrderBuilder().deliver_to("X").add(make_priced(_m.find("chai")))
    if step == "address": b = OrderBuilder().for_customer("A").add(make_priced(_m.find("chai")))
    if step == "items": b = OrderBuilder().for_customer("A").deliver_to("X")
    try:
        b.build("x"); return False
    except ValueError:
        return True
C("validates customer, address, items", lambda: all(_missing(s) for s in ("customer", "address", "items")))
def _frozen():
    try:
        _order().total = 0; return False
    except Exception:
        return True
C("orders are frozen", _frozen)
''', ["Each builder method stores a value and returns self.", "build(): check the three requirements, then make a tuple of OrderLine from the cart lines."])])

L(id="qb-step4", part="project", title="Step 4: Payments (Factory + Adapter)", tagline="UPI, card, cash: and tomorrow, something new",
body="""
### The problem
Each payment company gives us a library with a **different API**: `QuickPaySDK.charge_paise(paise)` returns a dict, and `CardCoClient.authorize("199.00")` returns a string. We can't edit their code, and the app shouldn't care which one is used.

### The design
- **Adapter:** `UpiPayment` and `CardPayment` wrap the SDKs and expose **our** interface, `pay(amount) -> receipt id`. Unit conversion (rupees to paise) lives inside the adapter.
- **Factory:** `PaymentFactory.create("upi")` returns the right object. New methods **register themselves** with a decorator, so the factory never needs editing (open/closed).
- The adapters accept the SDK in `__init__` (`sdk=None` means "use the real one"), which is dependency injection, so tests can pass fakes.
""" + code(S4),
quiz=[("Where does the rupees-to-paise conversion belong, and why?", "Inside the UPI adapter. It's a detail of that SDK; the rest of the app always speaks rupees.")],
exercises=[X("qb4", "Payment factory and adapters",
"""
Write Step 4: `PaymentFactory` with `register(name)` (a decorator) and `create(name)` (`ValueError` if unknown), plus three registered methods:
- `"upi"` → `UpiPayment`, adapting `QuickPaySDK` (pay ₹12.5 → `"UPI1250"`),
- `"card"` → `CardPayment`, adapting `CardCoClient` (pay 199 → `"CARD-199.00"`),
- `"cash"` → `CashOnDelivery` (pay 50 → `"COD-50.00"`).

The two SDK classes are given. Don't modify them.
""",
S1 + S2 + S3 + r'''
# ===== Step 4 =====
class QuickPaySDK:                     # third-party: don't edit
    def charge_paise(self, paise):
        return {"ok": True, "txn": f"UPI{paise}"}

class CardCoClient:                    # third-party: don't edit
    def authorize(self, amount_str):
        return f"CARD-{amount_str}"

# YOUR CODE: PaymentFactory, UpiPayment, CardPayment, CashOnDelivery
''',
S1 + S2 + S3 + S4,
r'''
T("upi", lambda: PaymentFactory.create("upi").pay(12.5), "UPI1250")
T("card", lambda: PaymentFactory.create("card").pay(199), "CARD-199.00")
T("cash", lambda: PaymentFactory.create("cash").pay(50), "COD-50.00")
def _unknown():
    try:
        PaymentFactory.create("bitcoin"); return False
    except ValueError:
        return True
C("unknown method raises ValueError", _unknown)
def _fake():
    class FakeSDK:
        def charge_paise(self, paise): return {"txn": f"FAKE{paise}"}
    return UpiPayment(FakeSDK()).pay(1)
T("adapter accepts an injected SDK (for tests)", _fake, "FAKE100")
''', ["register returns a decorator that stores the class in a dict and returns it.", "UpiPayment.pay: return self.sdk.charge_paise(round(amount * 100))['txn']."])])

L(id="qb-step5", part="project", title="Step 5: Order Lifecycle (State + Observer)", tagline="Placed → Paid → Preparing → Out for delivery → Delivered",
body="""
### State
An order moves through statuses, and **only some moves are allowed**: you can't deliver an order that wasn't paid, and you can't cancel once it's out for delivery. The rules live in **one table**, `TRANSITIONS`. Here each status only differs in which moves are allowed, so the **light (table) version** of the State pattern is the right choice (see the State lesson).

### Observer
When the status changes, many parts of the app care: the customer's app, the kitchen screen, the delivery partner, analytics. The tracker doesn't know any of them. It just **publishes** `"status_changed"` on the `EventBus`, and anyone can **subscribe**.
""" + code(S5) + """
### Try it in your head
```python
bus = EventBus()
bus.subscribe("status_changed", lambda order_id, old, new: print(f"📱 {order_id}: {new}"))
t = OrderTracker(bus)
t.start("QB1")             # 📱 QB1: PLACED
t.move("QB1", "PAID")      # 📱 QB1: PAID
t.move("QB1", "DELIVERED") # InvalidTransition: PAID -> DELIVERED is not allowed
```
""",
quiz=[("Why does EventBus catch exceptions from subscribers?", "So one broken subscriber (say, the SMS service is down) doesn't stop the others or crash order processing.")],
exercises=[X("qb5", "Tracker and event bus",
"""
Write Step 5: the `TRANSITIONS` table (as in the lesson), an `EventBus` (`subscribe(event, fn)`, and `publish(event, **data)`, which calls the subscribers in order and ignores their exceptions), `InvalidTransition`, and `OrderTracker(bus)` with `start(order_id)` and `move(order_id, new)`. Both publish `"status_changed"` with `order_id`, `old` and `new` (old is `None` for start).
""",
S1 + S2 + S3 + S4 + r'''
# ===== Step 5: YOUR CODE =====
TRANSITIONS = {}

class EventBus:
    pass

class InvalidTransition(Exception):
    pass

class OrderTracker:
    pass
''',
S1 + S2 + S3 + S4 + S5,
r'''
def _run():
    bus, log = EventBus(), []
    bus.subscribe("status_changed", lambda order_id, old, new: log.append((order_id, old, new)))
    def broken(**kw): raise RuntimeError("sms down")
    bus.subscribe("status_changed", broken)
    t = OrderTracker(bus)
    t.start("A"); t.move("A", "PAID"); t.move("A", "PREPARING")
    return log
T("events in order", _run, [("A", None, "PLACED"), ("A", "PLACED", "PAID"), ("A", "PAID", "PREPARING")])
def _invalid():
    t = OrderTracker(EventBus()); t.start("B"); t.move("B", "PAID")
    try:
        t.move("B", "DELIVERED"); return False
    except InvalidTransition:
        return t.status["B"] == "PAID"
C("illegal move raises InvalidTransition and keeps the status", _invalid)
def _cancel():
    t = OrderTracker(EventBus()); t.start("C"); t.move("C", "CANCELLED")
    try:
        t.move("C", "PAID"); return False
    except InvalidTransition:
        return True
C("cancelled is final", _cancel)
''', ["TRANSITIONS maps each status to a set of allowed next statuses.", "move(): look up the old status, check `new in TRANSITIONS[old]`, update, publish."])])

L(id="qb-step6", part="project", title="Step 6: Cart Undo & Checkout Rules (Command + Chain)", tagline="Oops, remove that! And: we don't deliver there.",
body="""
### Command: undo in the cart
Every "add to cart" tap becomes a **command object** (`AddToCart`) with `execute()` and `undo()`. `CartHistory` keeps two stacks, so the user can undo and redo freely. The command remembers **which line** it added, so undo removes exactly that line.

### Chain of Responsibility: checkout checks
Before placing an order, several rules must pass: **cart not empty → minimum order amount → delivery city**. Each rule is a small handler that checks one thing and passes the request to the next. Adding a rule ("no orders after 11 pm") means writing one class and adding it to the chain.
""" + code(S6),
quiz=[("Why does AddToCart store `self.line`?", "So undo removes exactly the line this command added, even if the cart has identical lines from other commands.")],
exercises=[X("qb6", "Commands and the checks chain",
"""
Write Step 6: `AddToCart(cart, priced, qty=1)` (a command), `CartHistory` (run/undo/redo with two stacks), `ValidationError`, the base `Check(nxt=None)`, and the three checks `NotEmpty`, `MinimumOrder(minimum, nxt=None)` and `DeliveryArea(cities, nxt=None)`. Each check raises `ValidationError` with the exact messages from the lesson (`"cart is empty"`, `"minimum order is <n>"`, `"we don't deliver to <city>"`), or passes to the next. The context is a dict: `{"cart": cart, "city": city}`.
""",
S1 + S2 + S3 + S4 + S5 + r'''
# ===== Step 6: YOUR CODE =====
class AddToCart:
    pass

class CartHistory:
    pass

class ValidationError(Exception):
    pass

class Check:
    pass
''',
S1 + S2 + S3 + S4 + S5 + S6,
r'''
_m = sample_menu()
def _undo():
    cart, h = Cart(), CartHistory()
    h.run(AddToCart(cart, make_priced(_m.find("thali")))); h.run(AddToCart(cart, make_priced(_m.find("chai")), 2))
    a = cart.subtotal(); h.undo(); b = cart.subtotal(); h.redo(); c = cart.subtotal(); h.undo(); h.undo(); d = cart.subtotal()
    return [a, b, c, d]
T("undo/redo cart", _undo, [200, 150, 200, 0])
def _check(cart, city):
    chain = NotEmpty(MinimumOrder(50, DeliveryArea({"Pune"})))
    try:
        chain.validate({"cart": cart, "city": city}); return "ok"
    except ValidationError as e:
        return str(e)
def _c(*ids):
    c = Cart()
    for i in ids: c.add(make_priced(_m.find(i)))
    return c
T("empty", lambda: _check(Cart(), "Pune"), "cart is empty")
T("too small", lambda: _check(_c("chai"), "Pune"), "minimum order is 50")
T("wrong city", lambda: _check(_c("thali"), "Delhi"), "we don't deliver to Delhi")
T("all good", lambda: _check(_c("thali"), "Pune"), "ok")
''', ["AddToCart.execute stores the returned line; undo calls cart.remove(self.line).", "Each check raises on failure, otherwise calls super().validate(ctx)."])])

L(id="qb-step7", part="project", title="Step 7: The App (Facade + Proxy + Singleton + Template Method)", tagline="One button for the mobile app to press",
body="""
### Facade
The mobile app shouldn't juggle carts, builders, factories and trackers. `QuickBite.place_order(...)` is **one simple call** that does everything, in order:
1. look up each item through the **cached menu** and apply its add-ons,
2. run the **checks chain**,
3. **build** the order,
4. **track** it (PLACED), **pay** through the factory, then mark it PAID,
5. **publish** `"order_paid"` for anyone who cares.

### Proxy
`MenuService` pretends to be a slow database. `CachedMenu` has the **same `get()`** but remembers results, so the "database" is asked only once per item.

### Singleton
`Settings()` always returns the same object (minimum order, delivery cities). In a bigger app you might prefer passing settings in (DIP), but it's a fair use for app-wide configuration.

### Template Method
`Receipt.render()` fixes the layout (header → lines → footer). `TextReceipt` and `SmsReceipt` fill in the pieces differently.
""" + code(S7),
quiz=[("What would the mobile app code look like without the Facade?", "It would have to create carts, builders, trackers and payment objects itself and call them in the right order, duplicating business logic in every client app.")],
exercises=[X("qb7", "Wire up the facade",
"""
All the parts from Steps 1–7 are given, **except** the body of `QuickBite.place_order`. Implement it following the 5 steps in the lesson: cached menu lookups with add-ons, the checks, `OrderBuilder` (address = `"<address>, <city>"`), start tracking, pay with `PaymentFactory`, move to `"PAID"`, store the order in `self.orders`, publish `"order_paid"` with `order=` and `receipt=`, and return the order.

Items are tuples `(item_id, qty)` or `(item_id, qty, [addons])`.
""",
S1 + S2 + S3 + S4 + S5 + S6 + S7.split("    def place_order")[0] + r'''    def place_order(self, customer, city, address, items, payment="upi", discount=None):
        # TODO: implement the 5 steps from the lesson
        pass

    def advance(self, order_id, new_status):
        self.tracker.move(order_id, new_status)

    def status(self, order_id):
        return self.tracker.status[order_id]
''',
FULL,
r'''
Settings._instance = None
def _app():
    app = QuickBite(sample_menu()); paid = []
    app.bus.subscribe("order_paid", lambda order, receipt: paid.append((order.id, receipt)))
    o = app.place_order("Asha", "Pune", "12 MG Road", [("thali", 1), ("burger-combo", 2, ["cheese", "jumbo"])],
                        payment="upi", discount=PercentOff(10))
    return app, o, paid
T("order total", lambda: _app()[1].total, 637.2)
T("address and lines", lambda: (_app()[1].address, _app()[1].lines[1]), ("12 MG Road, Pune", OrderLine("Burger Combo + extra cheese + jumbo size", 279, 2)))
T("paid + event published", lambda: (_app()[0].status("QB0001"), _app()[2]), ("PAID", [("QB0001", "UPI63720")]))
def _cache():
    app = QuickBite(sample_menu())
    app.place_order("A", "Pune", "x", [("thali", 1)]); app.place_order("B", "Pune", "y", [("thali", 2)])
    return app.menu.service.lookups
T("menu proxy caches lookups", _cache, 1)
def _rules():
    app = QuickBite(sample_menu())
    try:
        app.place_order("A", "Delhi", "x", [("thali", 1)]); return "no error"
    except ValidationError as e:
        return str(e)
T("checks are applied", _rules, "we don't deliver to Delhi")
def _flow():
    app, o, _ = _app(); app.advance(o.id, "PREPARING"); app.advance(o.id, "OUT_FOR_DELIVERY"); app.advance(o.id, "DELIVERED")
    return app.status(o.id)
T("full lifecycle", _flow, "DELIVERED")
''', ["Build a Cart, adding make_priced(self.menu.get(item_id), addons) for each item.", "Then self.checks.validate({'cart': cart, 'city': city}), then OrderBuilder()....build(self._new_id()).", "start → pay → move to PAID → store → publish → return."])])

L(id="qb-final", part="project", title="Final: The Complete App + Your Extension Challenge", tagline="Run it, read it, then extend it without editing a single existing class",
body="""
### The complete QuickBite source
Here's everything from Steps 1–7 in one file (about 300 lines). Read it top to bottom: you now know **every** pattern in it.
""" + code(FULL) + """
### A tour of the patterns, as a demo script
```python
app = QuickBite(sample_menu())
app.bus.subscribe("status_changed", lambda order_id, old, new: print(f"📱 {order_id}: {old} -> {new}"))   # Observer
order = app.place_order("Asha", "Pune", "12 MG Road",
                        [("thali", 1), ("burger-combo", 2, ["cheese", "jumbo"])],   # Decorator add-ons
                        payment="card", discount=PercentOff(10))                    # Factory+Adapter, Strategy
print(TextReceipt().render(order))                                                  # Template Method
app.advance(order.id, "PREPARING")                                                  # State
again = app.reorder(order.id)                                                       # Prototype
```
### Where the unused patterns *could* fit (design discussion)
- **Visitor:** a `SalesReport` visitor computing tax and revenue per item type.
- **Mediator:** a `DeliveryDispatcher` coordinating restaurants, riders and customers.
- **Memento:** saving cart drafts so the user can come back tomorrow.
- **Bridge:** notifications (Order-update, Promo) × channels (SMS, Push, Email).
- **Flyweight:** sharing item images and nutrition data among millions of order lines.
- **Abstract Factory:** a "region" factory creating matching tax rules + currency + payment providers per country.

> Interview tip: when asked "what patterns did you use?", explain **the problem each one solved**. Saying "I used Strategy because discounts change every festival" beats listing pattern names.

### 🏆 Your challenge: extend without editing
Add **two features** by writing **new code only** (append it at the bottom of the editor and don't modify any existing class):
1. **Loyalty points:** a `LoyaltyProgram(bus)` class that subscribes to `"order_paid"` and gives the customer **1 point per ₹10** of the order total (`int(total // 10)`). `points(customer)` returns their points (0 if none).
2. **Wallet payment:** register a new payment method `"wallet"` with the factory. `WalletPayment` uses a shared class-level dict `balances` (customer-agnostic for simplicity: one key `"default"`), starts at ₹1000, deducts the amount, returns `"WAL-<remaining balance with 2 decimals>"`, and raises `ValueError("insufficient wallet balance")` if there isn't enough. The order must then **not** be stored or published.

This proves the design is open for extension and closed for modification. That's SOLID in action!
""",
exercises=[X("qb-ext", "Extension challenge: loyalty + wallet",
"""
The full QuickBite code is already in the editor. **Scroll to the bottom** and add `LoyaltyProgram` and `WalletPayment` as described in the lesson, without changing any existing code.
""",
FULL + r'''

# ===================== YOUR EXTENSIONS BELOW (don't edit anything above) =====================
class LoyaltyProgram:
    pass

# @PaymentFactory.register("wallet")
# class WalletPayment: ...
''',
FULL + r'''

# ===================== YOUR EXTENSIONS BELOW (don't edit anything above) =====================
class LoyaltyProgram:                          # a new OBSERVER: no existing class changed
    def __init__(self, bus):
        self._points = defaultdict(int)
        bus.subscribe("order_paid", self.on_paid)
    def on_paid(self, order, receipt):
        self._points[order.customer] += int(order.total // 10)
    def points(self, customer):
        return self._points.get(customer, 0)

@PaymentFactory.register("wallet")             # a new payment method: registered, not hard-coded
class WalletPayment:
    balances = {"default": 1000.0}
    def pay(self, amount):
        if amount > self.balances["default"]:
            raise ValueError("insufficient wallet balance")
        self.balances["default"] -= amount
        return f"WAL-{self.balances['default']:.2f}"
''',
r'''
Settings._instance = None
def _loyal():
    app = QuickBite(sample_menu()); lp = LoyaltyProgram(app.bus)
    app.place_order("Asha", "Pune", "x", [("thali", 1)])                  # 150 -> 15 points
    app.place_order("Asha", "Pune", "x", [("biryani", 1)], payment="cash") # 220 -> 22 points
    app.place_order("Ravi", "Mumbai", "y", [("fries", 1)])                  # 80 -> 8 points
    return [lp.points("Asha"), lp.points("Ravi"), lp.points("Nobody")]
T("loyalty points", _loyal, [37, 8, 0])
def _wallet():
    WalletPayment.balances["default"] = 1000.0
    app = QuickBite(sample_menu()); seen = []
    app.bus.subscribe("order_paid", lambda order, receipt: seen.append(receipt))
    app.place_order("A", "Pune", "x", [("biryani", 4)], payment="wallet")  # 880
    try:
        app.place_order("A", "Pune", "x", [("thali", 1)], payment="wallet"); err = None
    except ValueError as e:
        err = str(e)
    return [seen, err, len(app.orders)]
T("wallet pays, then runs out", _wallet, [["WAL-120.00"], "insufficient wallet balance", 1])
def _untouched():
    above = USER_SRC.split("YOUR EXTENSIONS BELOW")[0]       # everything you were told not to edit
    return "YOUR EXTENSIONS BELOW" in USER_SRC and "wallet" not in above.lower() and "loyalty" not in above.lower()
C("existing code not modified (extensions only below the marker)", _untouched, "add new classes only, below the marker line")
''', ["LoyaltyProgram.__init__ subscribes a method to 'order_paid'; that method receives order= and receipt=.",
      "Decorate WalletPayment with @PaymentFactory.register('wallet').",
      "QuickBite.place_order already stops before storing/publishing if pay() raises."])])
