PRIMERS = {
"arrays": """
**Lists** keep things in order and let you jump to any position instantly (`nums[5]`). **Dictionaries and sets** answer _"have I seen this?"_ or _"what's stored under this key?"_ instantly, without searching everything.

> The #1 interview trick: when your solution has a loop inside a loop (O(n²)), ask "**can a dict or set remember what I've already seen?**". That usually turns it into one loop (O(n)).

**Signals:** "duplicate", "count", "pair that sums to", "group by", "seen before".

```python
seen = set()            # membership in O(1)
count = {}              # frequency map
count[x] = count.get(x, 0) + 1
from collections import Counter, defaultdict
```
""",
"two-pointers": """
Put **two fingers** on a list and move them according to a rule, instead of trying every pair.
- **From both ends toward the middle:** palindromes, reversing, pair sums in a **sorted** list.
- **Both from the left at different speeds:** linked list middles and cycles (you'll see this later).

> Two pointers usually needs **sorted** data or a symmetric structure. Sorting first costs O(n log n) but often unlocks an O(n) scan.

```python
left, right = 0, len(nums) - 1
while left < right:
    if condition: left += 1
    else: right -= 1
```
""",
"sliding-window": """
A **window** is a contiguous piece of a list or string `[left … right]`. Instead of re-checking every piece from scratch, **slide** the window: grow it on the right, shrink it on the left, and update a running summary (a sum, counts, "last seen" positions).

**Signals:** "longest/shortest **substring/subarray** such that…", "at most k…", "contains all of…".

```python
left = 0
for right, x in enumerate(items):
    add x to the window
    while window is invalid:
        remove items[left]; left += 1
    best = max(best, right - left + 1)
```
""",
"stack": """
A **stack** is a pile of plates: **Last In, First Out**. In Python, use a list: `append` to push, `pop()` to pop, `stack[-1]` to peek.

**Signals:** matching brackets, "most recent", undo, nested structures, "next greater/smaller element" (a **monotonic stack**: keep the stack sorted by popping anything that breaks the order).
""",
"binary-search": """
**Guess the middle, throw away half.** Each step halves the search space, so a million items take only ~20 steps: **O(log n)**.

It needs something **sorted**, or more generally a **yes/no condition that flips once** (false, false, false, true, true). Binary search finds where it flips.

```python
lo, hi = 0, len(nums) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if nums[mid] == target: return mid
    if nums[mid] < target: lo = mid + 1
    else: hi = mid - 1
```
> Most bugs are off-by-one errors: `lo <= hi` vs `lo < hi`, and `hi = mid` vs `mid - 1`. Trace a 2-element example by hand.
""",
"linked-list": """
A chain of nodes: each has a `val` and a `next` arrow. You can't jump to the middle, only **walk**. The tricks:
- **Dummy head node:** avoids special cases when the head changes.
- **Fast & slow pointers:** find the middle, detect cycles, find the k-th from the end.
- **Reverse in place** with prev/curr/next.

> Draw boxes and arrows on paper! Linked list bugs are almost always "I lost the pointer to the rest of the list".

The helpers `to_ll([1,2,3])` and `from_ll(head)` let you test easily.
""",
"trees": """
A **binary tree**: each node has up to two children, left and right. Trees are naturally **recursive**: every child is the root of a smaller tree.

**The recursion recipe:**
1. **Base case:** what's the answer for an empty tree (`None`)?
2. **Trust the recursion:** assume `solve(left)` and `solve(right)` already work.
3. **Combine** them with the current node.

**BST (Binary Search Tree):** left < node < right everywhere. An **in-order** walk (left, node, right) visits the values in sorted order.

**BFS** (a queue, level by level) vs **DFS** (recursion or a stack, go deep first).

Helpers: `to_tree([3, 9, 20, None, None, 15, 7])` builds from level order, and `from_tree(root)` converts back.
""",
"heap": """
A **heap** gives you the **smallest** item in O(1) and lets you add or remove items in O(log n). Python: `import heapq`. It's a **min-heap** on a normal list.

- **Max-heap:** push negative numbers (`-x`).
- **Top-k largest:** keep a min-heap of size k and pop when it grows bigger.
- **Ties:** push tuples like `(priority, counter, item)`.

**Signals:** "k largest/smallest", "merge k sorted", "median of a stream", "schedule the earliest/cheapest next".
""",
"backtracking": """
**Try every possibility, but undo as you go.** Explore a "decision tree": at each step, make a choice, recurse, then **undo the choice** and try the next one.

```python
def go(state):
    if done(state): record a COPY; return
    for choice in options(state):
        make(choice)
        go(state)
        undo(choice)
```
**Signals:** "all combinations / permutations / subsets", "can you place / spell / arrange". It's often exponential, so **prune** branches that can't work.
""",
"tries": """
A **trie** (say "try") is a tree of letters. Each path from the root spells a prefix, and words with the same beginning share a path. Looking up a word of length L takes O(L), no matter how many words are stored.

**Signals:** "prefix", "autocomplete", "starts with", "search many words at once", "wildcard search".

```python
root = {}
node = root
for ch in word: node = node.setdefault(ch, {})
node["$"] = True      # end of word
```
""",
"graphs": """
**Nodes** (things) connected by **edges** (relationships): cities and roads, people and friendships, courses and prerequisites. A grid is a graph too: each cell connects to its 4 neighbours.

- **DFS** (go deep): flood fill, connectivity, path existence.
- **BFS** (spread in rings): the **shortest path** in steps.
- **Topological sort** (Kahn: repeatedly take nodes with no incoming edges): ordering with dependencies, cycle detection in **directed** graphs.
- **Union-Find:** "are these connected?", counting groups, cycle detection in **undirected** graphs.

> Always keep a **visited** set, or you'll loop forever on cycles.
""",
"dp-1d": """
**Dynamic programming = solve smaller versions of the problem first, write the answers down, and build up.** It's just recursion plus memory.

**The 4-step recipe:**
1. **Define the state:** `dp[i]` means _what exactly?_ ("ways to reach step i", "best total up to house i").
2. **Recurrence:** ask "what was the **last** choice?" and build `dp[i]` from smaller `dp[...]`.
3. **Base cases:** the smallest answers you know without thinking.
4. **Order:** fill from small to big. Often you only need the last one or two values.

**Signals:** "number of ways", "minimum/maximum", "can you reach/make", plus choices that overlap. If brute-force recursion repeats the same sub-questions, it's DP.
""",
"dp-2d": """
The same DP recipe, but the state needs **two numbers**: `dp[i][j]`, like "the first i letters of a and the first j letters of b" or "row i, column j of a grid". Each cell is built from neighbours already computed (above, left, diagonal).

> Draw the table on paper for a small example and fill it in by hand. That's how you find the recurrence. Then notice that you often only need the previous row, which saves memory.

Beware the Python trap `[[0] * n] * m`, which creates m references to **the same row**. Use `[[0] * n for _ in range(m)]`.
""",
"greedy": """
**Greedy = make the best-looking choice right now and never look back.** It's fast and simple, but it's **only correct when you can argue why the local choice can't hurt**. Otherwise you need DP.

Classic greedy rules: "reset when the running sum goes negative" (Kadane), "track the farthest reach", "pick whatever ends earliest" (intervals).

> In interviews, explain **why** greedy is safe, or show a counterexample that proves it isn't (like coin change with coins [1, 3, 4]).
""",
"intervals": """
Intervals are `[start, end]` pairs: meetings, bookings, ranges. Almost every interval problem starts with **sorting**:
- by **start** → merge, insert, detect clashes,
- by **end** → keep the most non-overlapping ones (greedy).

Overlap test: `a.start <= b.end and b.start <= a.end`.
"How many at the same time?" → a min-heap of end times, or a sweep line of +1/−1 events.
""",
"matrix": """
A matrix is a list of rows: `m[row][col]`. Common tools:
- `zip(*m)` gives the columns (transpose).
- Boundaries `top, bottom, left, right` for spirals.
- Rotation = transpose + reverse.
- Using the matrix itself as storage, to get O(1) extra space.

Grids where you move between neighbours are really **graphs** (see the Graphs topic).
""",
"bits": """
Numbers are stored in binary, as rows of 0/1 switches. The bit operators:

- `a & b` (AND): 1 where **both** are 1 → 6 & 3 = 2 (110 & 011 = 010)
- `a ^ b` (XOR): 1 where they **differ** → 6 ^ 3 = 5, and x ^ x = 0
- OR (the vertical-bar operator): 1 where **either** is 1 → 6 OR 3 = 7
- `<<` / `>>` (shift): 1 << 3 = 8, and 8 >> 1 = 4

Tricks: `n & 1` (odd?), `n & (n - 1)` (turn off the lowest 1), XOR to cancel out pairs.
> Python ints never overflow, so problems that assume 32 bits need a mask: `& 0xFFFFFFFF`.
""",
}

INTRO = """
### How to use this page
1. Go through the topics **in order**. Each one starts with an easy warm-up and gets harder: **Warm-up → Easy → Medium → Hard**.
2. For each problem: read it, then read **"Understand it like a 10th grader"**. Try to code it in the editor before looking at the approach.
3. Stuck? Reveal the **hints one at a time**. Still stuck after 25 minutes? Read the approach, then **close it and code it yourself**.
4. Press **Run tests** (or Ctrl + Enter). Python really runs in your browser. Every problem is marked ✓ when all its tests pass.
5. Re-solve the problems you needed the solution for **3 days later**, from a blank editor. That's what makes it stick.

### Big-O, explained like you're in 10th standard
Big-O answers **"how much slower does my code get when the input gets bigger?"**

| Big-O | name | 1,000 items → steps | picture |
|---|---|---|---|
| O(1) | constant | 1 | grab the top plate |
| O(log n) | logarithmic | ~10 | guess-the-number by halving |
| O(n) | linear | 1,000 | read every page once |
| O(n log n) | sorting | ~10,000 | sorting a deck of cards smartly |
| O(n²) | quadratic | 1,000,000 | everyone shakes hands with everyone |
| O(2ⁿ) | exponential | way too many | trying every combination |

> A computer does about **100 million simple steps per second** in Python (much less, honestly about 10–50 million). If n = 100,000, O(n²) is 10 billion steps, which is too slow. That's why interviewers push you from O(n²) to O(n) or O(n log n).

### Python tools you'll use all the time
```python
from collections import Counter, defaultdict, deque
import heapq, bisect
seen = set();  freq = Counter(words);  groups = defaultdict(list)
q = deque([start]); q.popleft()          # queue for BFS
heapq.heappush(h, x); heapq.heappop(h)   # min-heap
i = bisect.bisect_left(sorted_list, x)   # binary search
```
"""
