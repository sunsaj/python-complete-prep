from lib import P

# ============================================================ INTERVALS
P(id="intervals-overlap", topic="intervals", level="Warm-up", title="Do Two Intervals Overlap?",
statement="""
Intervals are `[start, end]`. Return `True` if `a` and `b` overlap. Touching at one point counts as overlapping: [1, 3] and [3, 5] overlap.
""",
examples="""
```text
overlaps([1, 3], [2, 6]) → True     overlaps([1, 2], [3, 4]) → False     overlaps([1, 3], [3, 5]) → True
```
""",
eli10="""
Two school periods overlap unless one **finishes before the other starts**. So they **don't** overlap if `a ends before b starts` or `b ends before a starts`. Flip that around:

**overlap ⇔ a.start ≤ b.end and b.start ≤ a.end**

Draw two bars on a number line to convince yourself. This one-line check is the base of every interval problem.
""",
approach="`return a[0] <= b[1] and b[0] <= a[1]`",
hints=["When do they NOT overlap? Negate that."],
starter=r'''def overlaps(a, b):
    pass
''',
solution=r'''def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]     # each one starts before the other ends
''',
complexity="**O(1)**.",
tests=r'''
T("overlap", lambda: overlaps([1, 3], [2, 6]), True)
T("apart", lambda: overlaps([1, 2], [3, 4]), False)
T("touching", lambda: overlaps([1, 3], [3, 5]), True)
T("inside", lambda: overlaps([1, 10], [4, 5]), True)
T("reversed order", lambda: overlaps([5, 6], [1, 2]), False)
''')

P(id="meeting-rooms", topic="intervals", level="Easy", blind=True, lc=252, title="Meeting Rooms",
statement="""
Given meeting times `[start, end]`, return `True` if one person can attend **all** of them, meaning no two meetings overlap. A meeting ending at 10 and another starting at 10 is fine.
""",
examples="""
```text
can_attend_all([[0, 30], [5, 10], [15, 20]])  → False
can_attend_all([[7, 10], [2, 4]])             → True
```
""",
eli10="""
**Real-life picture:** you look at your calendar for clashes. The easy way is to **sort the meetings by start time**. Then a clash can only happen between **neighbours**: if a meeting starts before the previous one ended, there's a clash. You don't need to compare every pair.

This "sort by start, then look at neighbours" move solves most interval problems.
""",
approach="Sort by start. For each consecutive pair: if `next.start < prev.end`, return False. Otherwise return True.",
hints=["Sort by start time.", "Only adjacent meetings (after sorting) can overlap first."],
starter=r'''def can_attend_all(intervals):
    pass
''',
solution=r'''def can_attend_all(intervals):
    intervals = sorted(intervals)                 # sort by start time
    for prev, nxt in zip(intervals, intervals[1:]):
        if nxt[0] < prev[1]:
            return False                          # next starts before the previous one ends
    return True
''',
complexity="**Time O(n log n)** for sorting. **Space O(n)** for the sorted copy.",
tests=r'''
T("clash", lambda: can_attend_all([[0, 30], [5, 10], [15, 20]]), False)
T("fine", lambda: can_attend_all([[7, 10], [2, 4]]), True)
T("back to back", lambda: can_attend_all([[1, 5], [5, 10]]), True)
T("empty", lambda: can_attend_all([]), True)
''')

P(id="merge-intervals", topic="intervals", level="Medium", blind=True, lc=56, title="Merge Intervals",
statement="""
Merge all overlapping intervals and return the result sorted by start. Touching intervals merge: [1, 4] + [4, 5] → [1, 5].
""",
examples="""
```text
merge([[1, 3], [2, 6], [8, 10], [15, 18]])  → [[1, 6], [8, 10], [15, 18]]
merge([[1, 4], [4, 5]])                     → [[1, 5]]
```
""",
eli10="""
**Real-life picture:** you're painting stripes on a wall, and some stripes overlap. You want to describe the painted parts as **solid blocks**.

Sort the stripes by where they start. Walk through them, keeping the **current block**:
- If the next stripe **starts before (or exactly where) the current block ends**, it overlaps, so **stretch** the block's end to `max(block end, stripe end)`.
- Otherwise there's a gap. Close the current block and start a new one.
""",
approach="""
### Walk-through on [[1,3], [2,6], [8,10], [15,18]]
| interval | current block | action |
|---|---|---|
| [1, 3] | — | start [1, 3] |
| [2, 6] | [1, 3] | 2 ≤ 3 → stretch to [1, 6] |
| [8, 10] | [1, 6] | 8 > 6 → new block [8, 10] |
| [15, 18] | [8, 10] | new block [15, 18] |
""",
hints=["Sort by start.", "Compare each interval with the last merged one: overlap → extend its end, else append."],
starter=r'''def merge(intervals):
    pass
''',
solution=r'''def merge(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)    # overlaps, so stretch the current block
        else:
            merged.append([start, end])                # a gap, so start a new block
    return merged
''',
complexity="**Time O(n log n)**, **Space O(n)**.",
mistakes="- Setting the end to `end` instead of `max(...)`. [1, 10] + [2, 3] must stay [1, 10].",
tests=r'''
T("example", lambda: merge([[1, 3], [2, 6], [8, 10], [15, 18]]), [[1, 6], [8, 10], [15, 18]])
T("touching", lambda: merge([[1, 4], [4, 5]]), [[1, 5]])
T("contained", lambda: merge([[1, 10], [2, 3]]), [[1, 10]])
T("unsorted", lambda: merge([[4, 7], [1, 4]]), [[1, 7]])
''')

P(id="insert-interval", topic="intervals", level="Medium", blind=True, lc=57, title="Insert Interval",
statement="""
`intervals` is sorted by start and has no overlaps. Insert `new` and merge where necessary. Return the result, still sorted and non-overlapping.
""",
examples="""
```text
insert([[1, 3], [6, 9]], [2, 5])                         → [[1, 5], [6, 9]]
insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8])  → [[1, 2], [3, 10], [12, 16]]
```
""",
eli10="""
**Real-life picture:** a sorted calendar, and a new meeting arrives. The existing meetings fall into three groups:
1. Meetings that **end before** the new one starts: copy them unchanged.
2. Meetings that **overlap** the new one: **absorb** them into the new meeting (stretch its start and end).
3. Meetings that **start after** the new one ends: copy them unchanged.

Because the list is already sorted, one left-to-right pass handles all three groups, which is O(n). No sorting needed.
""",
approach="""
```text
i = 0
while i < n and intervals[i].end < new.start: add intervals[i]; i++          (group 1)
while i < n and intervals[i].start <= new.end:                                (group 2)
    new = [min(starts), max(ends)]; i++
add new
add the rest                                                                    (group 3)
```
""",
hints=["Three phases: before, overlapping, after.", "While overlapping, grow the new interval with min/max."],
starter=r'''def insert(intervals, new):
    pass
''',
solution=r'''def insert(intervals, new):
    result, i, n = [], 0, len(intervals)
    start, end = new
    while i < n and intervals[i][1] < start:          # 1. completely before
        result.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= end:           # 2. overlapping, so absorb
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])
    result.extend(intervals[i:])                      # 3. completely after
    return result
''',
complexity="**Time O(n)**, **Space O(n)**.",
tests=r'''
T("example 1", lambda: insert([[1, 3], [6, 9]], [2, 5]), [[1, 5], [6, 9]])
T("example 2", lambda: insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]), [[1, 2], [3, 10], [12, 16]])
T("into empty", lambda: insert([], [5, 7]), [[5, 7]])
T("at the end", lambda: insert([[1, 5]], [6, 8]), [[1, 5], [6, 8]])
T("at the start", lambda: insert([[3, 5]], [1, 2]), [[1, 2], [3, 5]])
''')

P(id="non-overlapping", topic="intervals", level="Medium", blind=True, lc=435, title="Non-overlapping Intervals",
statement="""
Return the **minimum number of intervals to remove** so the rest don't overlap. Touching ([1,2] and [2,3]) is fine.
""",
examples="""
```text
erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]])  → 1    (remove [1, 3])
erase_overlap_intervals([[1, 2], [1, 2], [1, 2]])          → 2
```
""",
eli10="""
**Flip the question:** removing the fewest is the same as **keeping the most** non-clashing meetings.

**Real-life picture:** you want to attend as many events at a fair as possible. The smart greedy rule: **always pick the event that ends earliest**. It leaves the most time for everything else. Sort by **end time**, keep an event if it starts at or after the last kept event's end, and skip it otherwise (that's a removal).

Why "ends earliest" and not "starts earliest" or "shortest"? A long event that starts early could block many others. Choosing the earliest finish can never hurt.
""",
approach="Sort by end. `last_end = -inf`, `removed = 0`. For each: if `start >= last_end`, keep it (last_end = end), else `removed += 1`.",
hints=["Maximise the intervals you keep instead.", "Greedy: sort by END time and keep each interval that doesn't clash."],
starter=r'''def erase_overlap_intervals(intervals):
    pass
''',
solution=r'''def erase_overlap_intervals(intervals):
    removed, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):   # earliest finish first
        if start >= last_end:
            last_end = end            # keep it
        else:
            removed += 1              # it clashes with a kept one, so remove it
    return removed
''',
complexity="**Time O(n log n)**, **Space O(n)** for the sort.",
tests=r'''
T("example 1", lambda: erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]), 1)
T("all same", lambda: erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]), 2)
T("none", lambda: erase_overlap_intervals([[1, 2], [2, 3]]), 0)
T("long blocker", lambda: erase_overlap_intervals([[1, 100], [11, 22], [1, 11], [2, 12]]), 2)
''')

P(id="meeting-rooms-ii", topic="intervals", level="Medium", blind=True, lc=253, title="Meeting Rooms II",
statement="""
Return the **minimum number of rooms** needed to hold all the meetings. A room freed at time 10 can host a meeting starting at 10.
""",
examples="""
```text
min_meeting_rooms([[0, 30], [5, 10], [15, 20]])  → 2
min_meeting_rooms([[7, 10], [2, 4]])             → 1
```
""",
eli10="""
**Real-life picture:** you manage rooms at an office. Go through the meetings **in order of start time**. When a meeting starts, check: _"Has any room become free?"_ Specifically, look at the room that frees up **earliest**. If its meeting ended at or before now, reuse that room. If not, open a new room.

"The room that frees up earliest" means a **min-heap of end times**. The heap's size at the end = the number of rooms used.

(Alternative: the "sweep line". Sort all starts and all ends separately and walk through time: +1 at each start, −1 at each end, and track the maximum.)
""",
approach="""
1. Sort by start. `ends = []` (a min-heap).
2. For each meeting: if `ends` isn't empty and `ends[0] <= start`, `heappop` (reuse that room). Then `heappush(ends, end)`.
3. Return `len(ends)`.
""",
hints=["Process meetings by start time.", "Keep a min-heap of end times of rooms in use; reuse the earliest-ending room if it's free."],
starter=r'''import heapq

def min_meeting_rooms(intervals):
    pass
''',
solution=r'''import heapq

def min_meeting_rooms(intervals):
    ends = []                                   # end times of the rooms in use (min-heap)
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heappop(ends)                 # the earliest room is free again, so reuse it
        heapq.heappush(ends, end)
    return len(ends)
''',
complexity="**Time O(n log n)**, **Space O(n)**.",
tests=r'''
T("example 1", lambda: min_meeting_rooms([[0, 30], [5, 10], [15, 20]]), 2)
T("example 2", lambda: min_meeting_rooms([[7, 10], [2, 4]]), 1)
T("all overlap", lambda: min_meeting_rooms([[1, 5], [2, 6], [3, 7]]), 3)
T("back to back", lambda: min_meeting_rooms([[1, 5], [5, 10], [10, 15]]), 1)
T("empty", lambda: min_meeting_rooms([]), 0)
''')

# ============================================================ MATRIX
P(id="transpose", topic="matrix", level="Warm-up", title="Transpose a Matrix",
statement="""
Return the **transpose**: rows become columns. `result[j][i] = m[i][j]`. The matrix may be rectangular.
""",
examples="""
```text
transpose([[1, 2, 3], [4, 5, 6]])  → [[1, 4], [2, 5], [3, 6]]
```
""",
eli10="""
Imagine a class seating chart. The transpose turns the chart on its diagonal: the first **row** of students becomes the first **column**.

Python trick: `zip(*m)` takes the first item of every row, then the second item of every row, and so on. That's exactly the columns!
""",
approach="`return [list(col) for col in zip(*m)]`, or two nested loops.",
hints=["result has len(m[0]) rows and len(m) columns.", "zip(*matrix) groups the columns."],
starter=r'''def transpose(m):
    pass
''',
solution=r'''def transpose(m):
    return [list(col) for col in zip(*m)]     # each column of m becomes a row
''',
complexity="**Time O(r·c)**, **Space O(r·c)**.",
tests=r'''
T("rect", lambda: transpose([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])
T("square", lambda: transpose([[1, 2], [3, 4]]), [[1, 3], [2, 4]])
T("single row", lambda: transpose([[1, 2]]), [[1], [2]])
''')

P(id="rotate-image", topic="matrix", level="Medium", blind=True, lc=48, title="Rotate Image",
statement="""
Rotate an `n × n` matrix **90° clockwise, in place** (modify it, return nothing).
""",
examples="""
```text
[[1,2,3],        [[7,4,1],
 [4,5,6],   →     [8,5,2],
 [7,8,9]]         [9,6,3]]
```
""",
eli10="""
**Real-life picture:** turn a photo on your phone by 90°. Doing it in place sounds hard, but there's a neat two-step trick:
1. **Transpose** (flip over the diagonal from top-left to bottom-right): rows become columns.
2. **Reverse each row** (a mirror flip left to right).

Try it on paper with the 3×3 example. After the transpose you get [[1,4,7],[2,5,8],[3,6,9]], and reversing each row gives [[7,4,1],[8,5,2],[9,6,3]] ✓

(For counter-clockwise: transpose, then reverse the **order of the rows** instead.)
""",
approach="""
1. For i < j: swap `m[i][j]` and `m[j][i]` (an in-place transpose, upper triangle only, so each pair is swapped once).
2. For each row: `row.reverse()`.
""",
hints=["90° clockwise = transpose + reverse each row.", "In the transpose, only swap pairs with j > i (otherwise you swap twice and undo it)."],
starter=r'''def rotate(m):
    # modify m in place
    pass
''',
solution=r'''def rotate(m):
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):                  # upper triangle only
            m[i][j], m[j][i] = m[j][i], m[i][j]    # transpose
    for row in m:
        row.reverse()                              # mirror left to right
''',
complexity="**Time O(n²)**, **Space O(1)**.",
tests=r'''
def _r(m): rotate(m); return m
T("3x3", lambda: _r([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), [[7, 4, 1], [8, 5, 2], [9, 6, 3]])
T("4x4", lambda: _r([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]),
  [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]])
T("1x1", lambda: _r([[1]]), [[1]])
''')

P(id="spiral-matrix", topic="matrix", level="Medium", blind=True, lc=54, title="Spiral Matrix",
statement="""
Return all elements of an `m × n` matrix in **spiral order**: clockwise, from the outside in.
""",
examples="""
```text
spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]])            → [1, 2, 3, 6, 9, 8, 7, 4, 5]
spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])  → [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
```
""",
eli10="""
**Real-life picture:** peeling an onion, or walking around a running track lane by lane, moving one lane inward each lap.

Keep four **walls**: `top`, `bottom`, `left`, `right`. Each lap:
1. Walk **right** along the top row, then move the top wall down.
2. Walk **down** the right column, then move the right wall left.
3. Walk **left** along the bottom row (if a row is still left), then move the bottom wall up.
4. Walk **up** the left column (if a column is still left), then move the left wall right.

Stop when the walls cross. The "if still left" checks matter for non-square matrices. Without them you'd walk the same middle row twice.
""",
approach="Use the four boundaries and the four loops above, with checks `top <= bottom` and `left <= right` before steps 3 and 4.",
hints=["Track four boundaries.", "After each side, shrink the corresponding boundary.", "Check the boundaries before walking the bottom row and the left column."],
starter=r'''def spiral_order(m):
    pass
''',
solution=r'''def spiral_order(m):
    out = []
    top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1): out.append(m[top][c])        # → along the top
        top += 1
        for r in range(top, bottom + 1): out.append(m[r][right])      # ↓ down the right
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1): out.append(m[bottom][c])   # ← along the bottom
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1): out.append(m[r][left])     # ↑ up the left
            left += 1
    return out
''',
complexity="**Time O(m·n)**, **Space O(1)** besides the output.",
tests=r'''
T("3x3", lambda: spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), [1, 2, 3, 6, 9, 8, 7, 4, 5])
T("3x4", lambda: spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]), [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])
T("single row", lambda: spiral_order([[1, 2, 3]]), [1, 2, 3])
T("single column", lambda: spiral_order([[1], [2], [3]]), [1, 2, 3])
''')

P(id="set-matrix-zeroes", topic="matrix", level="Medium", blind=True, lc=73, title="Set Matrix Zeroes",
statement="""
If a cell is 0, set its **entire row and column** to 0. Do it **in place**. Bonus: O(1) extra space.
""",
examples="""
```text
[[1,1,1],        [[1,0,1],
 [1,0,1],   →     [0,0,0],
 [1,1,1]]         [1,0,1]]
```
""",
eli10="""
**The trap:** if you start zeroing immediately, the new zeros make you zero out even more rows and columns that you shouldn't touch. You must first **find out** which rows and columns to clear, and only **then** clear them.

**Simple version (O(m + n) memory):** first pass, write down `zero_rows` and `zero_cols` (two sets). Second pass, set a cell to 0 if its row or column is in a set.

**O(1) trick:** use the **first row and first column as the notebook** (mark `m[i][0] = 0` and `m[0][j] = 0`). The first row and column need their own two boolean flags, because they're being used as storage.
""",
approach="""
Simple, safe version:
1. Collect `rows = {i}` and `cols = {j}` wherever `m[i][j] == 0`.
2. For every cell: if `i in rows or j in cols`, set it to 0.
""",
hints=["Don't zero while scanning; first record which rows and columns to clear.", "For O(1) space, store the markers in the first row and column (plus two flags)."],
starter=r'''def set_zeroes(m):
    # modify m in place
    pass
''',
solution=r'''def set_zeroes(m):
    rows, cols = len(m), len(m[0])
    first_row_zero = any(m[0][j] == 0 for j in range(cols))
    first_col_zero = any(m[i][0] == 0 for i in range(rows))
    for i in range(1, rows):                       # use row 0 and column 0 as markers
        for j in range(1, cols):
            if m[i][j] == 0:
                m[i][0] = m[0][j] = 0
    for i in range(1, rows):                       # clear using the markers
        for j in range(1, cols):
            if m[i][0] == 0 or m[0][j] == 0:
                m[i][j] = 0
    if first_row_zero:
        for j in range(cols): m[0][j] = 0
    if first_col_zero:
        for i in range(rows): m[i][0] = 0
''',
complexity="**Time O(m·n)**, **Space O(1)**.",
tests=r'''
def _z(m): set_zeroes(m); return m
T("centre", lambda: _z([[1, 1, 1], [1, 0, 1], [1, 1, 1]]), [[1, 0, 1], [0, 0, 0], [1, 0, 1]])
T("corners", lambda: _z([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]), [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]])
T("no zeros", lambda: _z([[1, 2], [3, 4]]), [[1, 2], [3, 4]])
T("first column", lambda: _z([[1, 2], [0, 4]]), [[0, 2], [0, 0]])
''')

# ============================================================ BITS
P(id="is-even-bit", topic="bits", level="Warm-up", title="Even or Odd with a Bit",
statement="""
Return `True` if `n` is even, using a **bitwise** operator (no `%`).
""",
examples="""
```text
is_even(4) → True      is_even(7) → False      is_even(0) → True
```
""",
eli10="""
Computers store numbers in **binary**: rows of light switches, each 0 or 1. 6 = `110`, 7 = `111`.

The **rightmost switch** says whether there's an extra 1, i.e. whether the number is odd. `n & 1` (AND with 1) **keeps only that rightmost switch**. If it's 0, the number is even.

Bit operators to know:
- `&` AND: 1 only if both bits are 1.
- `|` OR: 1 if either bit is 1.
- `^` XOR: 1 if the bits **differ**. Note that `x ^ x = 0` and `x ^ 0 = x`!
- `<<` and `>>` shift left and right (×2 and ÷2).
""",
approach="`return n & 1 == 0`. Watch the precedence: write `(n & 1) == 0`.",
hints=["The lowest bit of an odd number is 1."],
starter=r'''def is_even(n):
    pass
''',
solution=r'''def is_even(n):
    return (n & 1) == 0          # the lowest bit is 0 for even numbers
''',
complexity="**O(1)**.",
tests=r'''
T("4", lambda: is_even(4), True)
T("7", lambda: is_even(7), False)
T("0", lambda: is_even(0), True)
T("negative", lambda: is_even(-3), False)
''')

P(id="number-of-1-bits", topic="bits", level="Easy", blind=True, lc=191, title="Number of 1 Bits",
statement="""
Return how many `1` bits a non-negative integer has (its "Hamming weight").
""",
examples="""
```text
hamming_weight(11)  → 3     (1011)
hamming_weight(128) → 1     (10000000)
```
""",
eli10="""
**Simple way:** look at the last switch (`n & 1`), add it to the count, then shift everything right (`n >>= 1`). Repeat until n is 0.

**Brian Kernighan's trick:** `n & (n - 1)` **turns off the lowest 1 bit**. Example: 12 = `1100`, 11 = `1011`, and 12 & 11 = `1000`. So count how many times you can do that before n becomes 0. It loops only as many times as there are 1s!
""",
approach="`while n: n &= n - 1; count += 1`",
hints=["Check the last bit and shift right, repeatedly.", "Faster: n & (n-1) removes the lowest set bit."],
starter=r'''def hamming_weight(n):
    pass
''',
solution=r'''def hamming_weight(n):
    count = 0
    while n:
        n &= n - 1        # switch off the lowest 1 bit
        count += 1
    return count
''',
complexity="**O(number of 1 bits)** ≤ O(32). **Space O(1)**.",
tests=r'''
T("11", lambda: hamming_weight(11), 3)
T("128", lambda: hamming_weight(128), 1)
T("0", lambda: hamming_weight(0), 0)
T("all ones", lambda: hamming_weight(2**31 - 1), 31)
''')

P(id="counting-bits", topic="bits", level="Easy", blind=True, lc=338, title="Counting Bits",
statement="""
Return a list `ans` of length `n + 1` where `ans[i]` is the number of 1 bits in i. Aim for O(n).
""",
examples="""
```text
count_bits(5) → [0, 1, 1, 2, 1, 2]
```
""",
eli10="""
**DP + bits!** Shifting i right by one (`i >> 1`, which halves it) removes the last bit. So:

`bits(i) = bits(i >> 1) + (i & 1)`

"The 1s in i = the 1s in half of i, plus 1 if i is odd." Half of i is smaller, so we've already computed it. For example, 5 = `101`, half is 2 = `10` (1 one), and 5 is odd, so 1 + 1 = 2 ✓
""",
approach="`ans = [0] * (n + 1)`, then for i in 1..n: `ans[i] = ans[i >> 1] + (i & 1)`.",
hints=["Reuse the answer for i // 2.", "Add 1 if i is odd."],
starter=r'''def count_bits(n):
    pass
''',
solution=r'''def count_bits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)    # bits of half of i, plus the last bit
    return ans
''',
complexity="**Time O(n)**, **Space O(n)** for the output.",
tests=r'''
T("n = 5", lambda: count_bits(5), [0, 1, 1, 2, 1, 2])
T("n = 0", lambda: count_bits(0), [0])
T("n = 2", lambda: count_bits(2), [0, 1, 1])
''')

P(id="reverse-bits", topic="bits", level="Easy", blind=True, lc=190, title="Reverse Bits",
statement="""
Reverse the bits of a **32-bit** unsigned integer and return the result as an integer.
""",
examples="""
```text
reverse_bits(43261596)   → 964176192
(00000010100101000001111010011100 → 00111001011110000010100101000000)
reverse_bits(1)          → 2147483648   (the last bit moves to the first position)
```
""",
eli10="""
**Real-life picture:** 32 people in a row hold cards with 0 or 1. Make them stand in the opposite order.

Build the answer one bit at a time. 32 times:
1. Shift the answer left (make room on the right): `result <<= 1`.
2. Copy n's **last** bit onto it: `result |= n & 1`.
3. Drop n's last bit: `n >>= 1`.

The bit that was last in n gets pushed further left with every round, so after 32 rounds it ends up first.
""",
approach="Loop exactly **32 times**, even if n becomes 0 early. The leading zeros have to move to the end!",
hints=["Take n's lowest bit and push it onto the result, 32 times.", "result = (result << 1) | (n & 1); n >>= 1."],
starter=r'''def reverse_bits(n):
    pass
''',
solution=r'''def reverse_bits(n):
    result = 0
    for _ in range(32):                  # always 32 bits, including leading zeros
        result = (result << 1) | (n & 1) # make room, then copy n's last bit
        n >>= 1
    return result
''',
complexity="**O(32) = O(1)**.",
tests=r'''
T("example", lambda: reverse_bits(43261596), 964176192)
T("1", lambda: reverse_bits(1), 2147483648)
T("all ones", lambda: reverse_bits(4294967293), 3221225471)
T("0", lambda: reverse_bits(0), 0)
''')

P(id="missing-number", topic="bits", level="Easy", blind=True, lc=268, title="Missing Number",
statement="""
`nums` contains `n` distinct numbers from the range `0…n`, so exactly one number is missing. Return it, in O(n) time and O(1) space.
""",
examples="""
```text
missing_number([3, 0, 1])                       → 2
missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1])     → 8
```
""",
eli10="""
**Way 1, maths:** the sum 0 + 1 + … + n = n(n+1)/2 (the formula young Gauss used). Subtract the sum of the list, and what's left is the missing number!

**Way 2, XOR magic:** XOR has two superpowers: `x ^ x = 0` (a pair cancels out) and `x ^ 0 = x`. XOR together **every index 0…n** and **every number in the list**. Each present number appears **twice** (once as an index, once as a value) and cancels out. Only the missing number appears **once**, so it's left over.
""",
approach="`result = n`, then for each i, x: `result ^= i ^ x`. Return result.",
hints=["What should the sum of 0..n be?", "Or: XOR all indices and values; pairs cancel."],
starter=r'''def missing_number(nums):
    pass
''',
solution=r'''def missing_number(nums):
    result = len(nums)                    # n itself (indices only go up to n-1)
    for i, x in enumerate(nums):
        result ^= i ^ x                   # present numbers cancel in pairs
    return result
''',
complexity="**Time O(n)**, **Space O(1)**.",
tests=r'''
T("example 1", lambda: missing_number([3, 0, 1]), 2)
T("example 2", lambda: missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8)
T("missing n", lambda: missing_number([0, 1]), 2)
T("missing 0", lambda: missing_number([1]), 0)
''')

P(id="sum-two-integers", topic="bits", level="Medium", blind=True, lc=371, title="Sum of Two Integers",
statement="""
Return `a + b` **without using `+` or `-`**. a and b can be negative, and they fit in 32-bit signed integers.
""",
examples="""
```text
get_sum(1, 2) → 3      get_sum(-2, 3) → 1      get_sum(-5, -7) → -12
```
""",
eli10="""
**How do you add on paper?** Add the digits, and **carry** when needed. Binary addition is the same:
- `a ^ b` = the sum **without carries** (1+0 = 1, 1+1 = 0 with a carry).
- `(a & b) << 1` = the **carries**: a carry happens where both bits are 1, and it moves one place left.

Repeat "sum = a ^ b, carry = (a & b) << 1" until there's no carry left.

**The Python twist:** Python ints have **unlimited size**, so negative numbers would loop forever (the carries keep moving left without end). Fix it by keeping everything within **32 bits** with a mask `0xFFFFFFFF`, and convert back to a negative number at the end if the top (sign) bit is set.
""",
approach="""
```text
MASK = 0xFFFFFFFF
while b:
    a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
return a if a <= 0x7FFFFFFF else ~(a ^ MASK)      (convert back to a negative if bit 31 is set)
```
""",
hints=["XOR adds without carry; AND then shift-left gives the carry.", "In Python, mask to 32 bits to make negatives terminate.", "Convert back: if the result > 0x7FFFFFFF it's negative: ~(a ^ MASK)."],
starter=r'''def get_sum(a, b):
    pass
''',
solution=r'''def get_sum(a, b):
    MASK = 0xFFFFFFFF                      # keep to 32 bits (Python ints are unbounded)
    a, b = a & MASK, b & MASK
    while b:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK   # sum without carry, then the carry
    return a if a <= 0x7FFFFFFF else ~(a ^ MASK)        # turn a 32-bit two's complement back into a Python int
''',
complexity="**O(32) = O(1)** iterations.",
mistakes="- Without the mask, `get_sum(-1, 1)` loops forever in Python.",
tests=r'''
T("1 + 2", lambda: get_sum(1, 2), 3)
T("-2 + 3", lambda: get_sum(-2, 3), 1)
T("both negative", lambda: get_sum(-5, -7), -12)
T("-1 + 1", lambda: get_sum(-1, 1), 0)
T("zero", lambda: get_sum(0, 0), 0)
''')
