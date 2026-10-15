"""Build tooling for practice.html: problem schema, tiny markdown, and the shared Python test harness."""
import html
import re

PROBLEMS: list[dict] = []

TOPICS = [
    # id, title, short blurb
    ("arrays", "Arrays & Hashing", "Lists and dictionaries: the two tools behind most interview answers."),
    ("two-pointers", "Two Pointers", "Two fingers walking through a list, from both ends or at different speeds."),
    ("sliding-window", "Sliding Window", "A window that grows and shrinks as it slides over a list or string."),
    ("stack", "Stack", "A pile of plates: the last one you put on is the first one you take off."),
    ("binary-search", "Binary Search", "Guess the middle, throw away half, repeat."),
    ("linked-list", "Linked List", "A treasure hunt: each clue points to the next one."),
    ("trees", "Trees", "A family tree: each node has children, and recursion is the natural tool."),
    ("heap", "Heap / Priority Queue", "A magic box that always hands you the smallest (or largest) item first."),
    ("backtracking", "Backtracking", "Try a choice, explore, undo it, and try the next one."),
    ("tries", "Tries", "A tree of letters that makes prefix search instant."),
    ("graphs", "Graphs", "Cities and roads: BFS, DFS, and topological order."),
    ("dp-1d", "1-D Dynamic Programming", "Solve small versions first, write the answers down, build up."),
    ("dp-2d", "2-D Dynamic Programming", "The same idea in a grid: each cell built from its neighbours."),
    ("greedy", "Greedy", "Take the best-looking choice right now, when you can prove it's safe."),
    ("intervals", "Intervals", "Meetings on a calendar: sort by start, then merge or count."),
    ("matrix", "Matrix", "Grids of numbers: rotate, spiral, and mark rows and columns."),
    ("bits", "Bit Manipulation", "Numbers as rows of light switches (0 and 1)."),
]
LEVELS = ["Warm-up", "Easy", "Medium", "Hard"]


def P(**kw):
    required = ["id", "topic", "level", "title", "statement", "starter", "solution", "tests"]
    for r in required:
        assert r in kw, f"{kw.get('id')}: missing {r}"
    assert kw["level"] in LEVELS, kw["id"]
    assert kw["topic"] in {t[0] for t in TOPICS}, kw["id"]
    kw.setdefault("blind", False)
    kw.setdefault("lc", None)
    kw.setdefault("hints", [])
    for k in ["examples", "eli10", "approach", "complexity", "mistakes"]:
        kw.setdefault(k, "")
    PROBLEMS.append(kw)


# ---------------------------------------------------------------- markdown (tiny, predictable)
def _inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])_(.+?)_(?![\w*])", r"<i>\1</i>", t)
    return t


def md(src: str) -> str:
    src = src.strip("\n")
    if not src.strip():
        return ""
    lines = src.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang = line[3:].strip()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = ' class="plain"' if lang in ("text", "plain") else ""
            code = html.escape("\n".join(buf), quote=False)
            out.append(f"<pre{cls}><code>{code}</code></pre>" if not cls else f"<pre{cls}>{code}</pre>")
            continue
        if not line.strip():
            i += 1
            continue
        if re.match(r"^\s*[-*] ", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                item = re.sub(r"^\s*[-*] ", "", lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^\s*[-*] ", lines[i]):
                    item += " " + lines[i].strip()
                    i += 1
                items.append(f"<li>{_inline(item)}</li>")
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if re.match(r"^\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                item = re.sub(r"^\d+\. ", "", lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("   ") and lines[i].strip():
                    item += " " + lines[i].strip()
                    i += 1
                items.append(f"<li>{_inline(item)}</li>")
            out.append("<ol>" + "".join(items) + "</ol>")
            continue
        if line.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:])
                i += 1
            out.append(f'<div class="note">{_inline(" ".join(buf))}</div>')
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            head, *body = rows
            t = "<table><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in head) + "</tr>"
            t += "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(t + "</table>")
            continue
        if line.startswith("### "):
            out.append(f"<h4>{_inline(line[4:])}</h4>")
            i += 1
            continue
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(```|\s*[-*] |\d+\. |> |\||### )", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append(f"<p>{_inline(' '.join(buf))}</p>")
    return "\n".join(out)


# ---------------------------------------------------------------- Python side (shared by CPython build check + Pyodide)
PRELUDE = r'''
from typing import List, Optional
from collections import Counter, defaultdict, deque, OrderedDict
import heapq, bisect, math, itertools, functools, string, re

class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next
    def __repr__(self):
        return "ListNode(" + " -> ".join(map(str, from_ll(self, 50))) + ")"

def to_ll(values):
    """Python list -> linked list. to_ll([1, 2, 3]) gives 1 -> 2 -> 3"""
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def from_ll(head, limit=100000):
    """linked list -> Python list (stops after `limit` nodes, in case of a cycle)"""
    out = []
    while head is not None and len(out) < limit:
        out.append(head.val)
        head = head.next
    return out

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right
    def __repr__(self):
        return f"TreeNode({from_tree(self)})"

def to_tree(values):
    """Level-order list (None = missing child) -> binary tree. to_tree([2, 1, 3])"""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q, i = deque([root]), 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); q.append(node.right)
        i += 1
    return root

def from_tree(root):
    """binary tree -> level-order list (trailing None removed)"""
    out, q = [], deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append(None)
        else:
            out.append(n.val); q.append(n.left); q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out

def find_node(root, val):
    """find the node holding `val` (used by tests that need node references)"""
    stack = [root]
    while stack:
        n = stack.pop()
        if n is None: continue
        if n.val == val: return n
        stack += [n.left, n.right]
    return None

class Node:
    """graph node for Clone Graph"""
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
    def __repr__(self):
        return f"Node({self.val})"

def build_graph(adj):
    """adj[i] = list of neighbour values of node i+1 (values start at 1)"""
    if not adj:
        return None
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nbrs in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nbrs]
    return nodes[0]

def graph_to_adj(node):
    if node is None:
        return []
    seen, q = {node.val: node}, deque([node])
    while q:
        n = q.popleft()
        for m in n.neighbors:
            if m.val not in seen:
                seen[m.val] = m; q.append(m)
    return [[m.val for m in seen[v].neighbors] for v in sorted(seen)]

def graph_node_ids(node):
    seen, q = {}, deque([node] if node else [])
    while q:
        n = q.popleft()
        if id(n) in seen: continue
        seen[id(n)] = n
        q.extend(n.neighbors)
    return set(seen)
'''

HARNESS = r'''
import json as _json, traceback as _tb, sys as _sys, linecache as _lc
_results = []

def _short(x):
    r = repr(x)
    return r if len(r) <= 400 else r[:400] + " ..."

def _err():
    et, ev, tb = _sys.exc_info()
    frames = [f for f in _tb.extract_tb(tb) if f.filename == "solution.py"]
    where = "".join(f"  line {f.lineno}, in {f.name}:  {(f.line or '').strip()}\n" for f in frames[-3:])
    return where + "".join(_tb.format_exception_only(et, ev)).strip()

def T(name, call, expected, cmp=None):
    """one test: call() must equal expected (or satisfy cmp(got, expected))"""
    try:
        got = call()
    except Exception:
        _results.append({"name": name, "ok": False, "got": None, "exp": _short(expected), "err": _err()})
        return
    try:
        ok = bool(cmp(got, expected)) if cmp else got == expected
    except Exception:
        ok = False
    _results.append({"name": name, "ok": ok, "got": _short(got), "exp": _short(expected), "err": None})

def C(name, check, describe=""):
    """one test: check() must return True"""
    try:
        ok, err = bool(check()), None
    except Exception:
        ok, err = False, _err()
    _results.append({"name": name, "ok": ok, "got": describe if not ok else "", "exp": "", "err": err})

def same_items(a, b):        # order doesn't matter
    return sorted(map(repr, a)) == sorted(map(repr, b))

def same_groups(a, b):       # list of lists, order doesn't matter anywhere
    return sorted(sorted(map(repr, g)) for g in a) == sorted(sorted(map(repr, g)) for g in b)
'''

RUNNER = r'''
_lc.cache["solution.py"] = (len(USER_SRC), None, USER_SRC.splitlines(True), "solution.py")
_setup = None
try:
    exec(compile(USER_SRC, "solution.py", "exec"), globals())
except BaseException:
    _setup = _err()
if _setup is None:
    try:
        exec(compile(TEST_SRC, "tests.py", "exec"), globals())
    except BaseException:
        _results.append({"name": "tests stopped early: a class/function they need is missing or incomplete",
                         "ok": False, "got": None, "exp": "", "err": _err()})
RESULT = _json.dumps({"setup": _setup, "results": _results})
'''


def run_local(user_src: str, test_src: str) -> dict:
    import json
    ns = {"USER_SRC": user_src, "TEST_SRC": test_src, "__name__": "__main__"}
    exec(PRELUDE, ns)
    exec(HARNESS, ns)
    exec(RUNNER, ns)
    return json.loads(ns["RESULT"])
