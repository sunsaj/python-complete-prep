from lib import P

# ============================================================ TWO POINTERS
P(id="reverse-in-place", topic="two-pointers", level="Warm-up", title="Reverse a List In Place",
statement="""
Reverse the list `nums` **in place**: change the list itself, don't create a new one, and don't use `.reverse()` or `[::-1]`. Return nothing.
""",
examples="""
```text
nums = [1, 2, 3, 4, 5]; reverse_in_place(nums)  → nums becomes [5, 4, 3, 2, 1]
```
""",
eli10="""
Picture kids standing in a line who need to reverse their order. The first and last kids swap places. Then the second and second-last swap. Keep going inward until you meet in the middle.

That's the **two pointers** idea: one finger at the left end (`left`), one at the right end (`right`), both walking toward each other.
""",
approach="""
1. `left = 0`, `right = len(nums) - 1`.
2. While `left < right`: swap `nums[left]` and `nums[right]`, then `left += 1`, `right -= 1`.

Python's swap trick: `a, b = b, a`.
""",
hints=["Start one index at each end.", "Swap, then move both inward. Stop when they meet."],
starter=r'''def reverse_in_place(nums):
    # change nums itself; don't return anything
    pass
''',
solution=r'''def reverse_in_place(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]   # swap the two ends
        left += 1
        right -= 1
''',
complexity="**Time O(n)**: n/2 swaps. **Space O(1)**: no new list.",
tests=r'''
def _rev(xs):
    reverse_in_place(xs); return xs
T("odd length", lambda: _rev([1, 2, 3, 4, 5]), [5, 4, 3, 2, 1])
T("even length", lambda: _rev([1, 2, 3, 4]), [4, 3, 2, 1])
T("empty", lambda: _rev([]), [])
C("really in place", lambda: (lambda xs: (reverse_in_place(xs), xs)[1] is xs)([1, 2]))
''')

P(id="valid-palindrome", topic="two-pointers", level="Easy", blind=True, lc=125, title="Valid Palindrome",
statement="""
A phrase is a **palindrome** if, after lowercasing it and **removing everything that isn't a letter or digit**, it reads the same forwards and backwards. Return `True` or `False`.
""",
examples="""
```text
is_palindrome("A man, a plan, a canal: Panama")  → True   ("amanaplanacanalpanama")
is_palindrome("race a car")                      → False
is_palindrome(" ")                               → True   (empty after cleaning)
```
""",
eli10="""
**What it's really asking:** "Ignoring spaces, punctuation and capital letters, is this the same backwards?"

**Real-life picture:** two friends read the sentence at the same time. One starts at the first letter, the other at the last letter, and they walk toward each other. Each friend **skips** anything that isn't a letter or number. At every step they compare letters (lowercased). If they ever differ, it's not a palindrome. If they meet in the middle without a mismatch, it is.
""",
approach="""
### Easy version (uses extra memory)
`clean = [c.lower() for c in s if c.isalnum()]`, then `return clean == clean[::-1]`. This is fine in an interview if you mention that it uses O(n) memory.

### Two pointers (O(1) memory)
1. `left = 0`, `right = len(s) - 1`.
2. While `left < right`:
   - Move `left` forward while `s[left]` isn't alphanumeric.
   - Move `right` backward while `s[right]` isn't alphanumeric.
   - If `s[left].lower() != s[right].lower()`, return False.
   - Move both inward.
3. Return True.
""",
hints=["`ch.isalnum()` tells you whether a character is a letter or digit.", "Use two pointers that skip junk characters, and compare lowercase letters."],
starter=r'''def is_palindrome(s):
    pass
''',
solution=r'''def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1                      # skip junk on the left
        elif not s[right].isalnum():
            right -= 1                     # skip junk on the right
        elif s[left].lower() != s[right].lower():
            return False                   # mismatch, so not a palindrome
        else:
            left += 1                      # matched, so move both inward
            right -= 1
    return True
''',
complexity="**Time O(n)**. **Space O(1)**.",
mistakes="- Forgetting to lowercase. 'A' and 'a' must match.\n- Skipping junk with `if` instead of looping, and then comparing a junk character.",
tests=r'''
T("example 1", lambda: is_palindrome("A man, a plan, a canal: Panama"), True)
T("example 2", lambda: is_palindrome("race a car"), False)
T("only spaces", lambda: is_palindrome(" "), True)
T("digits count", lambda: is_palindrome("0P"), False)
T("punctuation only", lambda: is_palindrome(".,"), True)
''')

P(id="three-sum", topic="two-pointers", level="Medium", blind=True, lc=15, title="3Sum",
statement="""
Given a list `nums`, return **all unique triplets** `[a, b, c]` with `a + b + c == 0`. Each triplet should be listed once (no duplicate triplets). Any order is accepted.
""",
examples="""
```text
three_sum([-1, 0, 1, 2, -1, -4])  → [[-1, -1, 2], [-1, 0, 1]]
three_sum([0, 1, 1])              → []
three_sum([0, 0, 0])              → [[0, 0, 0]]
```
""",
eli10="""
**What it's really asking:** "Find every group of 3 numbers that add up to zero, without repeating a group."

**Real-life picture:** you have weights, some negative (balloons) and some positive (stones). You want groups of three that balance exactly at 0.

**The trick:** **sort** the numbers first. Then **fix one number** (the first of the three), and the problem shrinks to _"find two numbers that add up to −first"_ in the sorted part to its right. In a sorted list that's easy with two pointers: if the sum is too small, move the left pointer right (bigger numbers). If it's too big, move the right pointer left (smaller numbers).
""",
approach="""
1. Sort `nums`.
2. For each index `i` (the first number):
   - If `nums[i] > 0`, stop: three numbers ≥ a positive can't sum to 0.
   - If `nums[i] == nums[i-1]`, skip it (we already tried this first number, so this avoids duplicate triplets).
   - Set `left = i + 1`, `right = end`. While `left < right`:
     - `total = nums[i] + nums[left] + nums[right]`
     - total < 0 → `left += 1`. total > 0 → `right -= 1`.
     - total == 0 → record the triplet, move both pointers, and **skip repeated values** on the left.

### Walk-through: sorted = [-4, -1, -1, 0, 1, 2]
- i=0 (−4): need two numbers summing to 4. The largest pair is 1+2=3, so no.
- i=1 (−1): left at −1, right at 2 → −1−1+2 = 0 ✓ record [−1,−1,2]. Move → left at 0, right at 1 → −1+0+1 = 0 ✓ record [−1,0,1].
- i=2 (−1): same as the previous value, so skip.
- i=3 (0): left at 1, right at 2 → 3 > 0 … no more.
""",
hints=["Sorting helps a lot. Why?", "Fix the first number, then solve Two Sum on the rest with two pointers.", "Skip equal neighbours to avoid duplicate triplets."],
starter=r'''def three_sum(nums):
    pass
''',
solution=r'''def three_sum(nums):
    nums = sorted(nums)
    result = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break                              # all remaining numbers are positive
        if i > 0 and nums[i] == nums[i - 1]:
            continue                           # same first number as before, so skip duplicates
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1                      # need a bigger sum
            elif total > 0:
                right -= 1                     # need a smaller sum
            else:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1                  # skip repeats of the second number
    return result
''',
complexity="**Time O(n²)**: sorting is O(n log n), then n × a two-pointer scan. **Space O(1)** extra besides the output (and the sorted copy).",
mistakes="- Producing duplicates like two copies of [−1, 0, 1]. You need both skip rules.\n- Using a set of tuples to dedupe works, but it's slower and interviewers want the pointer logic.",
tests=r'''
T("example 1", lambda: three_sum([-1, 0, 1, 2, -1, -4]), [[-1, -1, 2], [-1, 0, 1]], same_groups)
T("none", lambda: three_sum([0, 1, 1]), [], same_groups)
T("all zeros", lambda: three_sum([0, 0, 0, 0]), [[0, 0, 0]], same_groups)
T("many duplicates", lambda: three_sum([-2, 0, 0, 2, 2]), [[-2, 0, 2]], same_groups)
T("mixed", lambda: three_sum([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]),
  [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]], same_groups)
''')

P(id="container-most-water", topic="two-pointers", level="Medium", blind=True, lc=11, title="Container With Most Water",
statement="""
`height[i]` is the height of a vertical line at position `i`. Choose two lines that, together with the x-axis, form a container. Return the **maximum amount of water** a container can hold: `width × the shorter height`.
""",
examples="""
```text
max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])  → 49   (lines at 1 and 8: width 7 × min(8, 7) = 49)
max_area([1, 1])                        → 1
```
""",
eli10="""
**What it's really asking:** "Pick two walls so the water between them is as much as possible."

**Real-life picture:** water between two walls can only rise to the **shorter** wall, or it spills over. So the amount = distance between the walls × the shorter wall.

**The clever move:** start with the two **outermost** walls (the widest possible container). Now we have to move one wall inward, and the width shrinks. Which wall should move? **Always the shorter one.** The shorter wall is the one limiting the water. Moving the taller wall inward can only make things worse (the width shrinks and the height is still limited by the same short wall). Moving the short wall at least gives a chance of finding a taller wall.
""",
approach="""
1. `left = 0`, `right = n - 1`, `best = 0`.
2. While `left < right`:
   - `area = (right - left) * min(height[left], height[right])`, and `best = max(best, area)`.
   - If `height[left] < height[right]`: `left += 1`, else `right -= 1`.
3. Return `best`.

### Walk-through on [1, 8, 6, 2, 5, 4, 8, 3, 7]
| left | right | heights | area | move |
|---|---|---|---|---|
| 0 | 8 | 1, 7 | 8×1 = 8 | left (1 is shorter) |
| 1 | 8 | 8, 7 | 7×7 = **49** | right |
| 1 | 7 | 8, 3 | 6×3 = 18 | right |
| … | … | … | never beats 49 | … |
""",
hints=["Start with the widest container (both ends).", "The water level is limited by the shorter wall.", "Move the pointer at the shorter wall inward."],
starter=r'''def max_area(height):
    pass
''',
solution=r'''def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        width = right - left
        best = max(best, width * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1          # the shorter wall limits us, so try to find a taller one
        else:
            right -= 1
    return best
''',
complexity="**Time O(n)**: the pointers meet after n steps. **Space O(1)**.",
mistakes="- Trying every pair, which is O(n²) and times out.\n- Moving the taller wall, which skips the optimal answer.",
tests=r'''
T("example 1", lambda: max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)
T("two lines", lambda: max_area([1, 1]), 1)
T("increasing", lambda: max_area([1, 2, 3, 4, 5]), 6)
T("big input", lambda: max_area(list(range(1, 100001))), 2500000000)
''')

# ============================================================ SLIDING WINDOW
P(id="max-sum-k", topic="sliding-window", level="Warm-up", title="Maximum Sum of K Consecutive Numbers",
statement="""
Given a list `nums` and an integer `k` (1 ≤ k ≤ len(nums)), return the largest sum of any **k consecutive** numbers.
""",
examples="""
```text
max_sum_k([2, 1, 5, 1, 3, 2], 3)  → 9    (5 + 1 + 3)
max_sum_k([4, -1, 2], 1)           → 4
```
""",
eli10="""
Imagine a train window that shows exactly k seats at a time. As the train moves one seat forward, **one seat enters** the window on the right and **one seat leaves** on the left. You don't need to re-add all k seats every time. Just do `sum + new − old`.

That's the **sliding window** idea: reuse the previous work instead of starting over.
""",
approach="""
1. `window = sum(nums[:k])`, the first window. `best = window`.
2. For `i` from `k` to the end: `window += nums[i] - nums[i - k]` (add the new one, remove the one that left), then update `best`.
""",
hints=["Compute the first window's sum.", "Slide: add the entering element, subtract the leaving one."],
starter=r'''def max_sum_k(nums, k):
    pass
''',
solution=r'''def max_sum_k(nums, k):
    window = sum(nums[:k])          # first window
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]   # one in, one out
        best = max(best, window)
    return best
''',
complexity="**Time O(n)** instead of O(n·k). **Space O(1)**.",
tests=r'''
T("example 1", lambda: max_sum_k([2, 1, 5, 1, 3, 2], 3), 9)
T("k = 1", lambda: max_sum_k([4, -1, 2], 1), 4)
T("whole list", lambda: max_sum_k([1, 2, 3], 3), 6)
T("negatives", lambda: max_sum_k([-3, -1, -2], 2), -3)
''')

P(id="best-time-stock", topic="sliding-window", level="Easy", blind=True, lc=121, title="Best Time to Buy and Sell Stock",
statement="""
`prices[i]` is a stock's price on day `i`. Choose **one day to buy** and a **later day to sell**. Return the maximum profit, or `0` if no profit is possible.
""",
examples="""
```text
max_profit([7, 1, 5, 3, 6, 4])  → 5    (buy at 1, sell at 6)
max_profit([7, 6, 4, 3, 1])     → 0    (prices only fall)
```
""",
eli10="""
**What it's really asking:** "What's the biggest jump from a low price to a **later** high price?"

**Real-life picture:** you're looking back at a month of mango prices at the market. For each day, ask: _"If I sold today, what's the cheapest day **before** today I could have bought?"_ Just remember **the lowest price seen so far** as you walk through the days. Today's profit = today's price − lowest so far. Keep the best profit.

It's the "best so far" warm-up again, applied twice: track the minimum price and the maximum profit.
""",
approach="""
1. `lowest = infinity`, `best = 0`.
2. For each `price`:
   - `lowest = min(lowest, price)`, the cheapest buying day up to now.
   - `best = max(best, price - lowest)`, the profit if we sell today.
3. Return `best`.

### Walk-through on [7, 1, 5, 3, 6, 4]
| price | lowest so far | profit today | best |
|---|---|---|---|
| 7 | 7 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 5 | 1 | 4 | 4 |
| 3 | 1 | 2 | 4 |
| 6 | 1 | **5** | 5 |
| 4 | 1 | 3 | 5 |

Why is it called sliding window? The "buy day" is the left edge and the "sell day" is the right edge. The left edge jumps forward whenever we find a cheaper price.
""",
hints=["You must buy before you sell.", "Track the minimum price seen so far.", "At each day, the profit if you sold today = price − minimum so far."],
starter=r'''def max_profit(prices):
    pass
''',
solution=r'''def max_profit(prices):
    lowest = float("inf")
    best = 0
    for price in prices:
        lowest = min(lowest, price)          # best day to have bought, up to today
        best = max(best, price - lowest)     # profit if we sell today
    return best
''',
complexity="**Time O(n)**: one pass. **Space O(1)**.",
mistakes="- `max(prices) - min(prices)` is wrong when the maximum comes before the minimum (you can't sell before buying).",
tests=r'''
T("example 1", lambda: max_profit([7, 1, 5, 3, 6, 4]), 5)
T("falling prices", lambda: max_profit([7, 6, 4, 3, 1]), 0)
T("max before min trap", lambda: max_profit([2, 4, 1]), 2)
T("one day", lambda: max_profit([5]), 0)
''')

P(id="longest-substring-no-repeat", topic="sliding-window", level="Medium", blind=True, lc=3, title="Longest Substring Without Repeating Characters",
statement="""
Given a string `s`, return the length of the longest **substring** (a contiguous piece) with **no repeated characters**.
""",
examples="""
```text
length_of_longest_substring("abcabcbb")  → 3   ("abc")
length_of_longest_substring("bbbbb")     → 1   ("b")
length_of_longest_substring("pwwkew")    → 3   ("wke")
```
""",
eli10="""
**What it's really asking:** "What's the longest stretch of letters where no letter repeats?"

**Real-life picture:** you're making a necklace by sliding along a string of coloured beads, and you're not allowed two beads of the same colour. Your necklace is a **window** `[left … right]`. You add the next bead on the right. If that colour is **already in your necklace**, you drop beads from the left until the old bead of that colour is gone. Then continue. Track the longest necklace you ever had.
""",
approach="""
### Window with a "last seen" dictionary
- `last[ch]` = the most recent index where `ch` appeared.
- `left` = the start of the current window.

For each `right, ch`:
1. If `ch` was seen **inside the current window** (`last[ch] >= left`), jump `left = last[ch] + 1` (drop everything up to the old copy).
2. `last[ch] = right`.
3. `best = max(best, right - left + 1)`.

### Walk-through on "abcabcbb"
| right | ch | left after | window | best |
|---|---|---|---|---|
| 0 | a | 0 | a | 1 |
| 1 | b | 0 | ab | 2 |
| 2 | c | 0 | abc | 3 |
| 3 | a | 1 | bca | 3 |
| 4 | b | 2 | cab | 3 |
| … | … | … | … | 3 |
""",
hints=["Use a window [left, right] that never contains a repeat.", "When the new character is already in the window, move left past its previous position.", "A dict of 'last index seen' makes the jump instant."],
starter=r'''def length_of_longest_substring(s):
    pass
''',
solution=r'''def length_of_longest_substring(s):
    last = {}                  # char -> last index we saw it
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1          # drop everything up to the old copy
        last[ch] = right
        best = max(best, right - left + 1)
    return best
''',
complexity="**Time O(n)**: each character is visited once. **Space O(k)** for the dict (k distinct characters).",
mistakes="- Forgetting the `last[ch] >= left` check. An old occurrence **outside** the window must not move `left` backwards (\"abba\" is the classic trap).",
tests=r'''
T("example 1", lambda: length_of_longest_substring("abcabcbb"), 3)
T("example 2", lambda: length_of_longest_substring("bbbbb"), 1)
T("example 3", lambda: length_of_longest_substring("pwwkew"), 3)
T("abba trap", lambda: length_of_longest_substring("abba"), 2)
T("empty", lambda: length_of_longest_substring(""), 0)
T("spaces count", lambda: length_of_longest_substring("a b c"), 3)
''')

P(id="char-replacement", topic="sliding-window", level="Medium", blind=True, lc=424, title="Longest Repeating Character Replacement",
statement="""
Given an uppercase string `s` and an integer `k`, you may change **at most k characters** to any other uppercase letter. Return the length of the longest substring that can be made of **one repeated letter**.
""",
examples="""
```text
character_replacement("ABAB", 2)     → 4   (change both B's → "AAAA")
character_replacement("AABABBA", 1)  → 4   ("AABA" → "AAAA")
```
""",
eli10="""
**What it's really asking:** "Find the longest stretch I can make all one letter by repainting at most k letters."

**Real-life picture:** a fence of coloured planks, and you have k cans of paint. In any section of fence, the smart move is to keep the **most common colour** and repaint the others. A section is fixable if `(section length) − (count of its most common colour) ≤ k`, because that's how many planks you'd repaint.

So slide a window. If it becomes unfixable, shrink it from the left.
""",
approach="""
1. Keep `count` = letter counts inside the window, and `top` = the highest count seen.
2. For each `right`:
   - Add `s[right]` to `count`, and update `top = max(top, count[s[right]])`.
   - If `window length - top > k`, the window needs too many repaints, so remove `s[left]` from count and `left += 1`.
   - `best = max(best, window length)`.

### Why `top` never needs to decrease (the subtle part)
We only care about finding a **longer** valid window. A longer window needs a bigger `top`. So keeping an old, too-high `top` can't create a wrong bigger answer. It just stops the window shrinking more than needed. This keeps the solution O(n).
""",
hints=["A window is valid if length − (most frequent letter count) ≤ k.", "Grow on the right. When invalid, shrink from the left by one.", "Track letter counts in a dict or a 26-length list."],
starter=r'''def character_replacement(s, k):
    pass
''',
solution=r'''def character_replacement(s, k):
    count = {}
    left = top = best = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        top = max(top, count[ch])                 # most common letter in the window
        while (right - left + 1) - top > k:       # too many letters to repaint
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
''',
complexity="**Time O(n)**. **Space O(1)**: at most 26 letters.",
mistakes="- Recomputing `max(count.values())` every step is fine (26 letters), but you should still be able to explain why the `top` trick works.",
tests=r'''
T("example 1", lambda: character_replacement("ABAB", 2), 4)
T("example 2", lambda: character_replacement("AABABBA", 1), 4)
T("k = 0", lambda: character_replacement("AABBB", 0), 3)
T("all same", lambda: character_replacement("AAAA", 2), 4)
T("single", lambda: character_replacement("A", 0), 1)
''')

P(id="min-window-substring", topic="sliding-window", level="Hard", blind=True, lc=76, title="Minimum Window Substring",
statement="""
Given strings `s` and `t`, return the **shortest substring of `s`** that contains **every character of `t`**, counting duplicates. If none exists, return `""`.
""",
examples="""
```text
min_window("ADOBECODEBANC", "ABC")  → "BANC"
min_window("a", "a")                → "a"
min_window("a", "aa")               → ""    (need two a's)
```
""",
eli10="""
**What it's really asking:** "What's the smallest piece of `s` that has all the letters on my shopping list `t`?"

**Real-life picture:** you're walking down a market street (`s`) with a shopping list (`t`). You **expand** your walk to the right until your bag has everything on the list. Then you try to **shrink from the left**: can you skip the first few shops and still have everything? Shrink as long as the bag stays complete, recording the shortest stretch. When removing a shop breaks the bag, expand right again. Repeat.

That's the "expand until valid, shrink while valid" pattern, the most important sliding window template.
""",
approach="""
1. `need = Counter(t)`, how many of each letter we need. `missing = len(t)`, how many letters are still missing in total.
2. Move `right` across `s`:
   - If `need[ch] > 0`, this letter was useful, so `missing -= 1`.
   - `need[ch] -= 1`. It can go negative, which means we have extra copies.
   - While `missing == 0` (the window is valid):
     - Record the window if it's the shortest so far.
     - Remove `s[left]`: `need[s[left]] += 1`. If it becomes > 0, we just lost a needed letter, so `missing += 1`.
     - `left += 1`.
3. Return the best window.

### Mini walk-through, "ADOBECODEBANC" / "ABC"
- Expand until "ADOBEC" has A, B, C. Valid, length 6.
- Shrink: dropping A breaks it. Expand… eventually "CODEBA", "BANC".
- The shortest valid window seen is **"BANC"** (length 4).
""",
hints=["Count what you need from t.", "Expand right until every needed letter is covered (track a 'missing' counter).", "While covered, record the window and shrink from the left."],
starter=r'''def min_window(s, t):
    pass
''',
solution=r'''from collections import Counter

def min_window(s, t):
    if not t or not s:
        return ""
    need = Counter(t)          # how many more of each letter we still need
    missing = len(t)           # total letters still missing
    left = 0
    best = (float("inf"), 0, 0)    # (length, start, end)
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1       # this letter fills a real need
        need[ch] -= 1          # negative = extra copies in the window
        while missing == 0:    # window has everything, so try to shrink it
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right + 1)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1   # we just dropped a needed letter
            left += 1
    return "" if best[0] == float("inf") else s[best[1]:best[2]]
''',
complexity="**Time O(|s| + |t|)**: each index enters and leaves the window once. **Space O(k)** for the counts.",
mistakes="- Comparing whole Counters at every step (O(26) each). That's fine, but the `missing` counter is the clean O(1) way.\n- Forgetting duplicate letters in `t` (\"aa\" needs two a's).",
tests=r'''
T("example 1", lambda: min_window("ADOBECODEBANC", "ABC"), "BANC")
T("exact", lambda: min_window("a", "a"), "a")
T("impossible", lambda: min_window("a", "aa"), "")
T("duplicates needed", lambda: min_window("aaflslflsldkalskaaa", "aaa"), "aaa")
T("whole string", lambda: min_window("ab", "ba"), "ab")
''')

# ============================================================ STACK
P(id="reverse-with-stack", topic="stack", level="Warm-up", title="Reverse a String Using a Stack",
statement="""
Reverse the string `s` using a **stack** (a Python list with `append` and `pop`). Don't use slicing.
""",
examples="""
```text
reverse_with_stack("hello")  → "olleh"
```
""",
eli10="""
A **stack** is a pile of plates: you can only put a plate on **top** (`append`) or take the **top** plate off (`pop`). The last plate in is the first plate out ("LIFO").

Put each letter on the pile, then take them all off. They come out in reverse order!
""",
approach="1. Push every character: `stack.append(ch)`.\n2. Pop until empty, adding each popped letter to the result.",
hints=["`list.append` pushes, and `list.pop()` removes the last item."],
starter=r'''def reverse_with_stack(s):
    stack = []
    pass
''',
solution=r'''def reverse_with_stack(s):
    stack = []
    for ch in s:
        stack.append(ch)            # push
    out = []
    while stack:
        out.append(stack.pop())     # pop gives the last pushed letter first
    return "".join(out)
''',
complexity="**Time O(n)**, **Space O(n)**.",
tests=r'''
T("hello", lambda: reverse_with_stack("hello"), "olleh")
T("empty", lambda: reverse_with_stack(""), "")
T("one", lambda: reverse_with_stack("x"), "x")
''')

P(id="valid-parentheses", topic="stack", level="Easy", blind=True, lc=20, title="Valid Parentheses",
statement="""
Given a string containing only `()[]{}`, return `True` if the brackets are **valid**: every opener is closed by the **same type**, in the **correct order**.
""",
examples="""
```text
is_valid("()[]{}")  → True
is_valid("(]")      → False
is_valid("([)]")    → False   (closed in the wrong order)
is_valid("{[]}")    → True
```
""",
eli10="""
**What it's really asking:** "Does every bracket close properly, like nested boxes?"

**Real-life picture:** you're stacking boxes inside boxes. Each `(`, `[`, `{` opens a new box **on top of the pile**. A closing bracket must close **the most recently opened box**, the one on top. If the top box is a `[` but you see `)`, that's wrong. At the end the pile must be empty (every box closed).

"Most recent first" is exactly what a **stack** gives you.
""",
approach="""
1. `pairs = {")": "(", "]": "[", "}": "{"}`.
2. For each character:
   - An opener: push it.
   - A closer: if the stack is empty, or its top isn't the matching opener, return False. Otherwise pop.
3. At the end, return `not stack` (everything was closed).

### Walk-through on "([)]"
| ch | stack before | action |
|---|---|---|
| ( | [] | push → [(] |
| [ | [(] | push → [(, [] |
| ) | [(, [] | top is [ but we need ( → **False** |
""",
hints=["The most recently opened bracket must be closed first.", "Push openers onto a stack, and for closers check the top."],
starter=r'''def is_valid(s):
    pass
''',
solution=r'''def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:                                  # a closing bracket
            if not stack or stack[-1] != pairs[ch]:
                return False                             # nothing to close, or the wrong type
            stack.pop()
        else:
            stack.append(ch)                             # an opening bracket
    return not stack                                     # leftover openers = invalid
''',
complexity="**Time O(n)**, **Space O(n)**.",
mistakes="- Only counting brackets. \"([)]\" has balanced counts but is invalid.\n- Forgetting the final empty check (\"((\" must be False).",
tests=r'''
T("simple", lambda: is_valid("()[]{}"), True)
T("wrong type", lambda: is_valid("(]"), False)
T("wrong order", lambda: is_valid("([)]"), False)
T("nested", lambda: is_valid("{[]}"), True)
T("unclosed", lambda: is_valid("(("), False)
T("closer first", lambda: is_valid("]"), False)
''')

P(id="min-stack", topic="stack", level="Medium", lc=155, title="Min Stack (DSA extra)",
statement="""
Design a class `MinStack` with `push(x)`, `pop()`, `top()` and `get_min()`, where **every operation is O(1)**. `get_min()` returns the smallest element currently in the stack.
""",
examples="""
```text
s = MinStack(); s.push(-2); s.push(0); s.push(-3)
s.get_min() → -3;  s.pop();  s.top() → 0;  s.get_min() → -2
```
""",
eli10="""
The difficulty: after you pop the smallest element, what's the new minimum? Searching the whole stack would be slow.

Trick: next to each plate, write down **"the minimum of everything at or below this plate"**. When you pop a plate, the plate under it already knows the minimum for the stack that remains!
""",
approach="Store pairs `(value, min_so_far)`. On push: `min_so_far = min(x, current_min)`. `get_min()` just reads the top pair's second value.",
hints=["Store the current minimum alongside each element."],
starter=r'''class MinStack:
    def __init__(self):
        pass
    def push(self, x):
        pass
    def pop(self):
        pass
    def top(self):
        pass
    def get_min(self):
        pass
''',
solution=r'''class MinStack:
    def __init__(self):
        self.items = []                     # pairs: (value, min of this and everything below)
    def push(self, x):
        current_min = min(x, self.items[-1][1]) if self.items else x
        self.items.append((x, current_min))
    def pop(self):
        self.items.pop()
    def top(self):
        return self.items[-1][0]
    def get_min(self):
        return self.items[-1][1]
''',
complexity="**All operations O(1)**. **Space O(n)**.",
tests=r'''
def _run():
    s = MinStack(); s.push(-2); s.push(0); s.push(-3)
    out = [s.get_min()]; s.pop(); out += [s.top(), s.get_min()]
    return out
T("example", _run, [-3, 0, -2])
def _run2():
    s = MinStack(); s.push(5); s.push(5); s.pop(); return s.get_min()
T("equal values", _run2, 5)
def _run3():
    s = MinStack()
    for x in [3, 1, 4, 1, 5]: s.push(x)
    mins = []
    for _ in range(5): mins.append(s.get_min()); s.pop()
    return mins
T("pop sequence", _run3, [1, 1, 1, 1, 3])
''')

P(id="daily-temperatures", topic="stack", level="Medium", lc=739, title="Daily Temperatures (DSA extra: monotonic stack)",
statement="""
Given daily `temps`, return a list `answer` where `answer[i]` is **how many days you wait after day i for a warmer temperature**, or 0 if that never happens.
""",
examples="""
```text
daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) → [1, 1, 4, 2, 1, 1, 0, 0]
```
""",
eli10="""
Picture people in a queue, each holding a temperature card and waiting for someone warmer to arrive. Keep a **stack of people still waiting**. When a new, warmer day comes, everyone waiting with a colder card gets their answer: the day difference. They leave the stack.

The stack always holds temperatures in **decreasing** order from bottom to top. That's called a **monotonic stack**, a pattern used in many "next greater element" problems.
""",
approach="""
1. `stack` holds the **indices** of days still waiting.
2. For each day `i`: while the stack isn't empty and `temps[i] > temps[stack[-1]]`, pop `j` and set `answer[j] = i - j`.
3. Push `i`.
""",
hints=["Keep the indices of days still waiting for a warmer day.", "A warmer day resolves everyone colder on top of the stack."],
starter=r'''def daily_temperatures(temps):
    pass
''',
solution=r'''def daily_temperatures(temps):
    answer = [0] * len(temps)
    stack = []                                   # indices still waiting (decreasing temperatures)
    for i, t in enumerate(temps):
        while stack and t > temps[stack[-1]]:
            j = stack.pop()
            answer[j] = i - j                    # day j waited i - j days
        stack.append(i)
    return answer
''',
complexity="**Time O(n)**: each index is pushed and popped at most once. **Space O(n)**.",
tests=r'''
T("example", lambda: daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]), [1, 1, 4, 2, 1, 1, 0, 0])
T("increasing", lambda: daily_temperatures([30, 40, 50, 60]), [1, 1, 1, 0])
T("decreasing", lambda: daily_temperatures([60, 50, 40]), [0, 0, 0])
''')

# ============================================================ BINARY SEARCH
P(id="binary-search", topic="binary-search", level="Easy", lc=704, title="Classic Binary Search",
statement="""
Given a **sorted** list `nums` and a `target`, return the index of `target`, or `-1` if it isn't there. Must be **O(log n)**.
""",
examples="""
```text
search([-1, 0, 3, 5, 9, 12], 9)  → 4
search([-1, 0, 3, 5, 9, 12], 2)  → -1
```
""",
eli10="""
The "guess my number between 1 and 100" game: you guess 50. "Higher!" Now you know it's 51–100, so you threw away half the possibilities with one guess. Guess the middle again (75), and so on. With 100 numbers you need at most 7 guesses. With a million, about 20!

That's why binary search is **O(log n)**: each step halves the search space.
""",
approach="""
1. `lo = 0`, `hi = len(nums) - 1`.
2. While `lo <= hi`: `mid = (lo + hi) // 2`.
   - Found → return `mid`.
   - `nums[mid] < target` → the answer is to the right: `lo = mid + 1`.
   - Otherwise → `hi = mid - 1`.
3. Return -1.
""",
hints=["Look at the middle element and decide which half to keep.", "Use `while lo <= hi` and move lo or hi past mid."],
starter=r'''def search(nums, target):
    pass
''',
solution=r'''def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1           # target is in the right half
        else:
            hi = mid - 1           # target is in the left half
    return -1
''',
complexity="**Time O(log n)**. **Space O(1)**.",
mistakes="- `lo = mid` instead of `mid + 1` → infinite loop.\n- `while lo < hi` → misses the last remaining element.",
tests=r'''
T("found", lambda: search([-1, 0, 3, 5, 9, 12], 9), 4)
T("missing", lambda: search([-1, 0, 3, 5, 9, 12], 2), -1)
T("single found", lambda: search([5], 5), 0)
T("first", lambda: search([1, 2, 3], 1), 0)
T("big", lambda: search(list(range(0, 2000000, 2)), 1999998), 999999)
''')

P(id="find-min-rotated", topic="binary-search", level="Medium", blind=True, lc=153, title="Find Minimum in Rotated Sorted Array",
statement="""
A sorted list of **distinct** numbers was **rotated**: some prefix was moved to the end, e.g. `[0,1,2,4,5,6,7]` → `[4,5,6,7,0,1,2]`. Return the **minimum** in O(log n).
""",
examples="""
```text
find_min([3, 4, 5, 1, 2])         → 1
find_min([4, 5, 6, 7, 0, 1, 2])   → 0
find_min([11, 13, 15, 17])        → 11   (rotated 0 times)
```
""",
eli10="""
**What it's really asking:** "Where is the 'drop' in a sorted list that got cut and re-glued?"

**Real-life picture:** the list looks like a hill that goes up, then **falls off a cliff**, then goes up again: `4 5 6 7 | 0 1 2`. The minimum is right after the cliff.

Look at the **middle** and compare it with the **last** element:
- If middle > last, the cliff is somewhere to the **right** of the middle (we're still on the first, high part).
- If middle < last, everything from the middle to the end is a nice sorted climb, so the cliff (the minimum) is at the middle or to its **left**.

Each comparison throws away half, which is binary search!
""",
approach="""
1. `lo = 0`, `hi = n - 1`.
2. While `lo < hi`:
   - `mid = (lo + hi) // 2`
   - If `nums[mid] > nums[hi]`: the minimum is right of mid → `lo = mid + 1`.
   - Else: the minimum is at mid or left → `hi = mid` (keep mid, it might be the answer!).
3. Return `nums[lo]`.

### Walk-through on [4, 5, 6, 7, 0, 1, 2]
| lo | hi | mid | nums[mid] vs nums[hi] | move |
|---|---|---|---|---|
| 0 | 6 | 3 | 7 > 2 | lo = 4 |
| 4 | 6 | 5 | 1 < 2 | hi = 5 |
| 4 | 5 | 4 | 0 < 1 | hi = 4 |
| 4 | 4 | — | stop | answer nums[4] = **0** |
""",
hints=["Compare the middle element with the last element.", "If middle > last, the minimum is to the right.", "Otherwise the minimum is at mid or to its left (don't exclude mid)."],
starter=r'''def find_min(nums):
    pass
''',
solution=r'''def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1          # the cliff is to the right of mid
        else:
            hi = mid              # mid could be the minimum, so keep it
    return nums[lo]
''',
complexity="**Time O(log n)**. **Space O(1)**.",
mistakes="- Writing `hi = mid - 1`, which can jump past the minimum.\n- Comparing with `nums[lo]` instead of `nums[hi]`, which gets the non-rotated case wrong.",
tests=r'''
T("example 1", lambda: find_min([3, 4, 5, 1, 2]), 1)
T("example 2", lambda: find_min([4, 5, 6, 7, 0, 1, 2]), 0)
T("not rotated", lambda: find_min([11, 13, 15, 17]), 11)
T("two items", lambda: find_min([2, 1]), 1)
T("single", lambda: find_min([7]), 7)
''')

P(id="search-rotated", topic="binary-search", level="Medium", blind=True, lc=33, title="Search in Rotated Sorted Array",
statement="""
A sorted list of distinct numbers was rotated (like the previous problem). Return the index of `target`, or -1. Must be O(log n).
""",
examples="""
```text
search_rotated([4, 5, 6, 7, 0, 1, 2], 0)  → 4
search_rotated([4, 5, 6, 7, 0, 1, 2], 3)  → -1
```
""",
eli10="""
**What it's really asking:** binary search, but the list is "broken" in one place.

**The key insight:** cut a rotated list at **any** middle, and **at least one half is perfectly sorted**. Check which half is sorted (compare its ends). Then ask the easy question: _"Is the target inside the sorted half's range?"_
- Yes → search there.
- No → it must be in the other half.

Example: `[4 5 6 7 | 0 1 2]`, mid = 7. The left half 4…7 is sorted. Is 0 between 4 and 7? No, so go right.
""",
approach="""
While `lo <= hi`:
1. `mid`. If `nums[mid] == target` → return mid.
2. If `nums[lo] <= nums[mid]` (the **left half is sorted**):
   - If `nums[lo] <= target < nums[mid]` → `hi = mid - 1`, else `lo = mid + 1`.
3. Else (the **right half is sorted**):
   - If `nums[mid] < target <= nums[hi]` → `lo = mid + 1`, else `hi = mid - 1`.
""",
hints=["One of the two halves around mid is always sorted.", "Figure out which half is sorted by comparing nums[lo] and nums[mid].", "Check whether the target lies within that sorted half's range."],
starter=r'''def search_rotated(nums, target):
    pass
''',
solution=r'''def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                    # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                         # target is inside the sorted left half
            else:
                lo = mid + 1
        else:                                        # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1                         # target is inside the sorted right half
            else:
                hi = mid - 1
    return -1
''',
complexity="**Time O(log n)**. **Space O(1)**.",
mistakes="- Using `<` instead of `<=` in `nums[lo] <= nums[mid]`. When lo == mid, the left 'half' is a single element and counts as sorted.",
tests=r'''
T("example 1", lambda: search_rotated([4, 5, 6, 7, 0, 1, 2], 0), 4)
T("missing", lambda: search_rotated([4, 5, 6, 7, 0, 1, 2], 3), -1)
T("single missing", lambda: search_rotated([1], 0), -1)
T("two items", lambda: search_rotated([3, 1], 1), 1)
T("in left part", lambda: search_rotated([5, 1, 3], 5), 0)
T("not rotated", lambda: search_rotated([1, 2, 3, 4, 5], 4), 3)
''')
