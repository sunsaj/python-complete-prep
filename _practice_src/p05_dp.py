from lib import P

# ============================================================ 1-D DP
P(id="fib-memo", topic="dp-1d", level="Warm-up", title="Fibonacci, Fast (Memoization)",
statement="""
Return the n-th Fibonacci number: `fib(0) = 0`, `fib(1) = 1`, and `fib(n) = fib(n-1) + fib(n-2)`. It must handle `n = 300` instantly.
""",
examples="""
```text
fib(10) → 55        fib(50) → 12586269025
```
""",
eli10="""
**This warm-up is the key to ALL dynamic programming. Read it slowly.**

The plain recursive version `fib(n-1) + fib(n-2)` is **horribly slow**, because it recomputes the same things again and again. fib(5) calls fib(3) twice and fib(2) three times. For fib(50) that's billions of calls.

**Real-life picture:** your teacher asks "what is 7 × 8?" 20 times. The first time you work it out. Then you **write the answer on the board** and just read it the other 19 times. That's **memoization**: remember answers you've already computed.

**Dynamic programming = break a big problem into smaller versions of itself + remember the answers to those smaller versions.**

Two styles:
- **Top-down (memo):** the normal recursion plus a cache (`@functools.cache`).
- **Bottom-up (table):** start from the smallest cases, fib(0) and fib(1), and build upward in a loop. You often only need the **last two** values.
""",
approach="""
```python
# bottom-up, O(1) memory
a, b = 0, 1            # fib(0), fib(1)
for _ in range(n):
    a, b = b, a + b    # slide forward one step
return a
```
""",
hints=["Plain recursion repeats work: cache results or build from the bottom up.", "You only need the previous two values."],
starter=r'''def fib(n):
    pass
''',
solution=r'''def fib(n):
    a, b = 0, 1                 # fib(0), fib(1)
    for _ in range(n):
        a, b = b, a + b         # move one step up the sequence
    return a
''',
complexity="**Time O(n)** instead of O(2ⁿ). **Space O(1)**.",
tests=r'''
T("fib 10", lambda: fib(10), 55)
T("fib 0", lambda: fib(0), 0)
T("fib 1", lambda: fib(1), 1)
T("fib 300 (must be fast)", lambda: fib(300), 222232244629420445529739893461909967206666939096499764990979600)
''')

P(id="climbing-stairs", topic="dp-1d", level="Easy", blind=True, lc=70, title="Climbing Stairs",
statement="""
You climb a staircase of `n` steps, taking **1 or 2 steps** at a time. How many **different ways** can you reach the top?
""",
examples="""
```text
climb_stairs(2) → 2   (1+1, 2)
climb_stairs(3) → 3   (1+1+1, 1+2, 2+1)
climb_stairs(5) → 8
```
""",
eli10="""
**What it's really asking:** "Count the different step patterns."

**The magic question of DP:** _"What was my **last** move?"_ To stand on step n, your last move was either:
- a **1-step** from step n−1, or
- a **2-step** from step n−2.

So: **ways(n) = ways(n−1) + ways(n−2)**. That's exactly Fibonacci!

Check it: ways(1) = 1, ways(2) = 2, ways(3) = 2 + 1 = 3, ways(4) = 3 + 2 = 5, ways(5) = 5 + 3 = 8 ✓

The DP recipe you'll reuse for every problem:
1. **Define** what a sub-answer means: `ways[i]` = number of ways to reach step i.
2. **Recurrence:** how a sub-answer is built from smaller ones.
3. **Base cases:** the smallest answers you know directly.
4. **Order:** compute from small to big.
""",
approach="""
```text
one, two = 1, 1          # ways(1) = 1, and "ways(0)" = 1 (stand still)
repeat n-1 times: one, two = one + two, one
return one
```
""",
hints=["Think about the LAST step you took to reach step n.", "ways(n) = ways(n-1) + ways(n-2)."],
starter=r'''def climb_stairs(n):
    pass
''',
solution=r'''def climb_stairs(n):
    prev, curr = 1, 1              # ways to reach step 0 and step 1
    for _ in range(n - 1):
        prev, curr = curr, prev + curr   # ways(i) = ways(i-1) + ways(i-2)
    return curr
''',
complexity="**Time O(n)**, **Space O(1)**.",
tests=r'''
T("n = 2", lambda: climb_stairs(2), 2)
T("n = 3", lambda: climb_stairs(3), 3)
T("n = 5", lambda: climb_stairs(5), 8)
T("n = 1", lambda: climb_stairs(1), 1)
T("n = 45", lambda: climb_stairs(45), 1836311903)
''')

P(id="house-robber", topic="dp-1d", level="Medium", blind=True, lc=198, title="House Robber",
statement="""
Houses in a row hold `nums[i]` money. You can't rob **two adjacent houses** (the alarm goes off). Return the maximum money you can take.
""",
examples="""
```text
rob([1, 2, 3, 1])     → 4    (houses 0 and 2: 1 + 3)
rob([2, 7, 9, 3, 1])  → 12   (2 + 9 + 1)
```
""",
eli10="""
**What it's really asking:** "Pick numbers from a list, never two neighbours, to make the biggest total."

**Real-life picture:** you're walking down the street deciding at each house. At house i there are only **two choices**:
- **Rob it:** you get `nums[i]` + the best you could do up to house **i−2** (you had to skip i−1).
- **Skip it:** you keep the best you could do up to house **i−1**.

`best[i] = max(best[i−1], best[i−2] + nums[i])`

Like stairs, you only need the last two values.
""",
approach="""
### Walk-through on [2, 7, 9, 3, 1]
| house | money | skip (best up to i−1) | rob (best up to i−2 + money) | best |
|---|---|---|---|---|
| 0 | 2 | 0 | 0 + 2 | 2 |
| 1 | 7 | 2 | 0 + 7 | 7 |
| 2 | 9 | 7 | 2 + 9 | 11 |
| 3 | 3 | 11 | 7 + 3 | 11 |
| 4 | 1 | 11 | 11 + 1 | **12** |
""",
hints=["At each house: rob it (plus the best from two houses back) or skip it (keep the best from one house back).", "Keep just two running values."],
starter=r'''def rob(nums):
    pass
''',
solution=r'''def rob(nums):
    two_back, one_back = 0, 0           # best totals up to house i-2 and house i-1
    for money in nums:
        two_back, one_back = one_back, max(one_back, two_back + money)   # skip vs rob
    return one_back
''',
complexity="**Time O(n)**, **Space O(1)**.",
mistakes="- Greedily taking every other house (all even or all odd positions). Example: [2, 1, 1, 2] → the best is 4 (houses 0 and 3).",
tests=r'''
T("example 1", lambda: rob([1, 2, 3, 1]), 4)
T("example 2", lambda: rob([2, 7, 9, 3, 1]), 12)
T("not alternating", lambda: rob([2, 1, 1, 2]), 4)
T("empty", lambda: rob([]), 0)
T("one", lambda: rob([5]), 5)
''')

P(id="house-robber-ii", topic="dp-1d", level="Medium", blind=True, lc=213, title="House Robber II",
statement="""
Same as House Robber, but the houses are arranged in a **circle**: the first and last houses are neighbours.
""",
examples="""
```text
rob_circle([2, 3, 2])     → 3    (can't take both 2s; they're neighbours now)
rob_circle([1, 2, 3, 1])  → 4
rob_circle([1, 2, 3])     → 3
```
""",
eli10="""
**What changed:** house 0 and house n−1 can't **both** be robbed.

**The trick: split it into two normal (straight) streets.**
- Street A: houses 0 … n−2 (we **ignore the last** house).
- Street B: houses 1 … n−1 (we **ignore the first** house).

Every valid plan avoids at least one of the two end houses, so it fits in A or in B. Answer = max(rob(A), rob(B)), reusing House Robber!

Edge case: a single house, which is just that house.
""",
approach="`return max(nums[0], rob(nums[:-1]), rob(nums[1:]))`, where `rob` is the straight-line version. Include `nums[0]` for the one-house case.",
hints=["The first and last can't both be robbed.", "Solve the straight-line problem twice: without the first house, and without the last."],
starter=r'''def rob_circle(nums):
    pass
''',
solution=r'''def rob_circle(nums):
    def rob_line(houses):
        two_back = one_back = 0
        for money in houses:
            two_back, one_back = one_back, max(one_back, two_back + money)
        return one_back
    if len(nums) == 1:
        return nums[0]
    return max(rob_line(nums[:-1]), rob_line(nums[1:]))   # skip the last, or skip the first
''',
complexity="**Time O(n)**, **Space O(n)** for the slices (O(1) if you pass index ranges).",
tests=r'''
T("example 1", lambda: rob_circle([2, 3, 2]), 3)
T("example 2", lambda: rob_circle([1, 2, 3, 1]), 4)
T("three", lambda: rob_circle([1, 2, 3]), 3)
T("single", lambda: rob_circle([7]), 7)
T("two", lambda: rob_circle([1, 5]), 5)
''')

P(id="longest-palindromic-substring", topic="dp-1d", level="Medium", blind=True, lc=5, title="Longest Palindromic Substring",
statement="""
Return the **longest substring** of `s` that is a palindrome. If several have the same length, any of them is accepted.
""",
examples="""
```text
longest_palindrome("babad")  → "bab"  (or "aba")
longest_palindrome("cbbd")   → "bb"
```
""",
eli10="""
**What it's really asking:** "What's the longest piece of the string that reads the same backwards?"

**Real-life picture:** drop a stone in a pond and the ripples spread **outward equally** from the centre. Every palindrome has a **centre**, and it's symmetric around it. So try **every possible centre** and **expand outward** while the left and right letters match.

There are two kinds of centres:
- **One letter** (odd-length palindromes like "aba", centred on b),
- **Between two letters** (even-length palindromes like "abba", centred between the two b's).

With 2n−1 centres, each expanding at most n steps, this takes O(n²) time but only O(1) memory. It's simpler than the DP table, and interviewers love it.
""",
approach="""
```text
expand(l, r): while l >= 0 and r < n and s[l] == s[r]: l -= 1; r += 1
              return the palindrome s[l+1 : r]
for i in range(n):
    try expand(i, i)       (odd)
    try expand(i, i + 1)   (even)
    keep the longest
```
""",
hints=["Every palindrome mirrors around its centre.", "Try each index as a centre, and also each gap between two letters.", "Expand while the characters on both sides match."],
starter=r'''def longest_palindrome(s):
    pass
''',
solution=r'''def longest_palindrome(s):
    best = ""
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1                       # ripple outward while it's still symmetric
            r += 1
        return s[l + 1:r]
    for i in range(len(s)):
        for cand in (expand(i, i), expand(i, i + 1)):   # odd centre, even centre
            if len(cand) > len(best):
                best = cand
    return best
''',
complexity="**Time O(n²)**, **Space O(1)**. (Manacher's algorithm does O(n), which is rarely expected.)",
tests=r'''
_is_pal = lambda got, exp: got == got[::-1] and len(got) == len(exp)
T("babad", lambda: longest_palindrome("babad"), "bab", lambda g, e: _is_pal(g, e) and g in "babad")
T("cbbd", lambda: longest_palindrome("cbbd"), "bb")
T("single", lambda: longest_palindrome("a"), "a")
T("whole", lambda: longest_palindrome("racecar"), "racecar")
T("long", lambda: longest_palindrome("abc" * 300 + "x" * 9), "x" * 9)
''')

P(id="palindromic-substrings", topic="dp-1d", level="Medium", blind=True, lc=647, title="Palindromic Substrings",
statement="""
Count **how many substrings** of `s` are palindromes. Substrings at different positions count separately, even if they're the same text.
""",
examples="""
```text
count_substrings("abc")  → 3    ("a", "b", "c")
count_substrings("aaa")  → 6    ("a" ×3, "aa" ×2, "aaa")
```
""",
eli10="""
It's the same **expand-around-centre** idea as the previous problem, but instead of keeping the longest palindrome, **count every successful expansion step**. Each time the ripple grows and still matches, that's one more palindrome.

For "aaa" with centre at the middle 'a': "a" ✓ (count 1), expand to "aaa" ✓ (count 2). Do that for every centre, odd and even.
""",
approach="For each of the 2n−1 centres: while the characters match, count += 1 and expand.",
hints=["Reuse expand-around-centre.", "Each successful expansion is one palindrome."],
starter=r'''def count_substrings(s):
    pass
''',
solution=r'''def count_substrings(s):
    count = 0
    for centre in range(2 * len(s) - 1):     # n letter centres + (n-1) gap centres
        l = centre // 2
        r = l + centre % 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1                        # s[l..r] is a palindrome
            l -= 1
            r += 1
    return count
''',
complexity="**Time O(n²)**, **Space O(1)**.",
tests=r'''
T("abc", lambda: count_substrings("abc"), 3)
T("aaa", lambda: count_substrings("aaa"), 6)
T("single", lambda: count_substrings("z"), 1)
T("abba", lambda: count_substrings("abba"), 6)
''')

P(id="decode-ways", topic="dp-1d", level="Medium", blind=True, lc=91, title="Decode Ways",
statement="""
Letters are encoded as numbers: A=1, B=2, … Z=26. Given a digit string `s`, return **how many ways** it can be decoded. A `0` can't stand alone, and "06" isn't valid.
""",
examples="""
```text
num_decodings("12")   → 2    ("AB" = 1,2   or  "L" = 12)
num_decodings("226")  → 3    (2,2,6 / 22,6 / 2,26)
num_decodings("06")   → 0
```
""",
eli10="""
**What it's really asking:** "In how many ways can I cut this digit string into pieces of 1 or 2 digits, where each piece is a valid letter (1–26)?"

It's **Climbing Stairs with rules**! At each position you can take a **1-digit step** (valid if that digit isn't '0') or a **2-digit step** (valid if the two digits form 10–26).

`ways[i]` = number of ways to decode the first i digits.
- If `s[i-1]` (one digit) is 1–9: `ways[i] += ways[i-1]`
- If `s[i-2:i]` (two digits) is 10–26: `ways[i] += ways[i-2]`
""",
approach="""
### Walk-through on "226"
| i | 1-digit piece | ok? | 2-digit piece | ok? | ways[i] |
|---|---|---|---|---|---|
| 0 | — | | — | | 1 (empty string) |
| 1 | "2" | ✓ | — | | 1 |
| 2 | "2" | ✓ +1 | "22" | ✓ +1 | 2 |
| 3 | "6" | ✓ +2 | "26" | ✓ +1 | **3** |
""",
hints=["Like climbing stairs: steps of 1 or 2 digits.", "A 1-digit step is valid if the digit ≠ '0'. A 2-digit step is valid if the value is 10..26.", "ways[i] = (valid 1-step ? ways[i-1] : 0) + (valid 2-step ? ways[i-2] : 0)."],
starter=r'''def num_decodings(s):
    pass
''',
solution=r'''def num_decodings(s):
    prev2, prev1 = 1, 1 if s and s[0] != "0" else 0    # ways for "" and for the first digit
    if not s:
        return 0
    for i in range(2, len(s) + 1):
        curr = 0
        if s[i - 1] != "0":
            curr += prev1                  # take one digit as a letter
        if 10 <= int(s[i - 2:i]) <= 26:
            curr += prev2                  # take two digits as a letter
        prev2, prev1 = prev1, curr
    return prev1
''',
complexity="**Time O(n)**, **Space O(1)**.",
mistakes="- Treating '0' as a letter.\n- Accepting \"06\" as a 2-digit letter (the value must be ≥ 10).",
tests=r'''
T("12", lambda: num_decodings("12"), 2)
T("226", lambda: num_decodings("226"), 3)
T("leading zero", lambda: num_decodings("06"), 0)
T("10", lambda: num_decodings("10"), 1)
T("100", lambda: num_decodings("100"), 0)
T("11106", lambda: num_decodings("11106"), 2)
''')

P(id="coin-change", topic="dp-1d", level="Medium", blind=True, lc=322, title="Coin Change",
statement="""
Given coin values `coins` (unlimited supply) and an `amount`, return the **fewest coins** needed to make exactly that amount, or `-1` if it's impossible.
""",
examples="""
```text
coin_change([1, 2, 5], 11)  → 3    (5 + 5 + 1)
coin_change([2], 3)         → -1
coin_change([1], 0)         → 0
```
""",
eli10="""
**What it's really asking:** "What's the smallest number of coins that adds up to the amount?"

**Why not greedy?** "Always take the biggest coin" fails. With coins [1, 3, 4] and amount 6, greedy gives 4+1+1 = 3 coins, but 3+3 = **2 coins** is better.

**DP thinking:** `best[a]` = the fewest coins to make amount a. Ask the magic question, _"What was the **last coin** I added?"_ If the last coin was c, the rest is amount a−c, made in `best[a−c]` coins. Try every coin and take the minimum:

`best[a] = 1 + min(best[a − c] for each coin c ≤ a)`

`best[0] = 0` (zero coins make zero). Build the table from 1 up to the amount.
""",
approach="""
### Walk-through: coins [1, 2, 5], first few amounts
| a | try coin 1 | try coin 2 | try coin 5 | best[a] |
|---|---|---|---|---|
| 0 | | | | 0 |
| 1 | best[0]+1 = 1 | — | — | 1 |
| 2 | best[1]+1 = 2 | best[0]+1 = 1 | — | 1 |
| 3 | best[2]+1 = 2 | best[1]+1 = 2 | — | 2 |
| 5 | 3 | 3 | best[0]+1 = 1 | 1 |
| 11 | best[10]+1 = 3 | best[9]+1 = 4 | best[6]+1 = 3 | **3** |
""",
hints=["Greedy (biggest coin first) can fail.", "best[a] = 1 + min over coins of best[a - coin].", "Use infinity for 'impossible' and convert it to -1 at the end."],
starter=r'''def coin_change(coins, amount):
    pass
''',
solution=r'''def coin_change(coins, amount):
    INF = float("inf")
    best = [0] + [INF] * amount               # best[a] = fewest coins to make a
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1      # use coin c as the last coin
    return best[amount] if best[amount] != INF else -1
''',
complexity="**Time O(amount × number of coins)**, **Space O(amount)**.",
tests=r'''
T("example", lambda: coin_change([1, 2, 5], 11), 3)
T("impossible", lambda: coin_change([2], 3), -1)
T("zero", lambda: coin_change([1], 0), 0)
T("greedy fails", lambda: coin_change([1, 3, 4], 6), 2)
T("bigger", lambda: coin_change([186, 419, 83, 408], 6249), 20)
''')

P(id="max-product-subarray", topic="dp-1d", level="Medium", blind=True, lc=152, title="Maximum Product Subarray",
statement="""
Return the largest **product** of a contiguous, non-empty subarray of `nums`. The numbers can be negative or zero.
""",
examples="""
```text
max_product([2, 3, -2, 4])  → 6    ([2, 3])
max_product([-2, 0, -1])    → 0
max_product([-2, 3, -4])    → 24   (all three: two negatives make a positive!)
```
""",
eli10="""
**The twist:** a **negative × negative = positive**. So a very **negative** product so far can become the **biggest** after multiplying by another negative number.

**Real-life picture:** think of your score in a game where cards multiply it, and some cards are "−". Keep track of **two** running scores ending at the current card:
- `hi`: the **largest** product ending here,
- `lo`: the **smallest** (most negative) product ending here.

At each new number x, the new hi and lo come from three candidates: `x` (start fresh here), `hi × x`, and `lo × x`. If x is negative, the old lo times x might become the new hi!
""",
approach="""
```text
hi = lo = best = nums[0]
for x in nums[1:]:
    candidates = (x, hi * x, lo * x)
    hi, lo = max(candidates), min(candidates)
    best = max(best, hi)
```
### Walk-through on [-2, 3, -4]
| x | hi | lo | best |
|---|---|---|---|
| −2 | −2 | −2 | −2 |
| 3 | max(3, −6, −6) = 3 | min(...) = −6 | 3 |
| −4 | max(−4, −12, **24**) = 24 | −12 | **24** |
""",
hints=["A negative number flips the biggest and smallest products.", "Track both the max and the min product ending at each position."],
starter=r'''def max_product(nums):
    pass
''',
solution=r'''def max_product(nums):
    hi = lo = best = nums[0]
    for x in nums[1:]:
        candidates = (x, hi * x, lo * x)        # start fresh, extend the max, or extend the min
        hi, lo = max(candidates), min(candidates)
        best = max(best, hi)
    return best
''',
complexity="**Time O(n)**, **Space O(1)**.",
tests=r'''
T("example", lambda: max_product([2, 3, -2, 4]), 6)
T("zero", lambda: max_product([-2, 0, -1]), 0)
T("two negatives", lambda: max_product([-2, 3, -4]), 24)
T("single negative", lambda: max_product([-3]), -3)
T("zeros split", lambda: max_product([0, 2, -3, 0, 4, 5]), 20)
''')

P(id="word-break", topic="dp-1d", level="Medium", blind=True, lc=139, title="Word Break",
statement="""
Return `True` if string `s` can be split into a sequence of words from `words` (words can be reused).
""",
examples="""
```text
word_break("leetcode", ["leet", "code"])                  → True
word_break("applepenapple", ["apple", "pen"])             → True
word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])  → False
```
""",
eli10="""
**What it's really asking:** "Can I chop this long string into dictionary words with no letters left over?"

**DP thinking:** `ok[i]` = "the first i letters can be split into words". Magic question: _"What's the **last word** of the split?"_ For position i, try every possible last word that ends at i: if `s[j:i]` is a dictionary word **and** `ok[j]` is True (the part before it was splittable), then `ok[i]` is True.

`ok[0] = True`: the empty prefix is trivially fine.

Like dominoes: you can place a word-domino ending at position i only if a domino chain already reaches its start j.
""",
approach="""
```text
ok = [True] + [False] * n
for i in 1..n:
    for each word w in words:
        if i >= len(w) and ok[i - len(w)] and s[i - len(w):i] == w: ok[i] = True; break
return ok[n]
```
### Walk-through: "leetcode"
- ok[0] = True
- ok[4]: "leet" ends at 4 and ok[0] is True → **True**
- ok[8]: "code" ends at 8 and ok[4] is True → **True** ✓
""",
hints=["ok[i] = can the first i characters be split?", "ok[i] is True if some word w ends at i and ok[i - len(w)] is True."],
starter=r'''def word_break(s, words):
    pass
''',
solution=r'''def word_break(s, words):
    ok = [True] + [False] * len(s)          # ok[i]: s[:i] can be split into words
    for i in range(1, len(s) + 1):
        for w in words:
            j = i - len(w)
            if j >= 0 and ok[j] and s[j:i] == w:
                ok[i] = True                 # a word ends exactly at i
                break
    return ok[len(s)]
''',
complexity="**Time O(n × number of words × word length)**, **Space O(n)**.",
mistakes="- Greedy matching (taking the first word that fits) fails: \"catsandog\" with \"cats\" vs \"cat\". DP tries all the options.",
tests=r'''
T("leetcode", lambda: word_break("leetcode", ["leet", "code"]), True)
T("reuse", lambda: word_break("applepenapple", ["apple", "pen"]), True)
T("catsandog", lambda: word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]), False)
T("must be fast", lambda: word_break("a" * 300 + "b", ["a", "aa", "aaa", "aaaa"]), False)
''')

P(id="lis", topic="dp-1d", level="Medium", blind=True, lc=300, title="Longest Increasing Subsequence",
statement="""
Return the length of the longest **strictly increasing subsequence** of `nums`. A subsequence keeps the original order but may skip elements.
""",
examples="""
```text
length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])  → 4    (2, 3, 7, 18)
length_of_lis([0, 1, 0, 3, 2, 3])            → 4
length_of_lis([7, 7, 7])                     → 1
```
""",
eli10="""
**What it's really asking:** "Pick numbers left to right, each bigger than the last. What's the most you can pick?"

### Way 1: DP, O(n²) (understand this one first)
`lis[i]` = the length of the longest increasing subsequence **ending at i**. To end at i, the previous chosen number must be some earlier `nums[j] < nums[i]`, so:
`lis[i] = 1 + max(lis[j] for j < i if nums[j] < nums[i])`, or 1 if there's none.

### Way 2: "patience piles", O(n log n) (the impressive one)
**Real-life picture:** a card game. Deal the cards left to right onto piles. Each card goes on the **leftmost pile whose top card is ≥ it**. If there's no such pile, start a new pile on the right. **The number of piles = the LIS length.**
In code, keep a list `tails` where `tails[k]` is the smallest possible last number of an increasing subsequence of length k+1. Use **binary search** (`bisect_left`) to find where each number goes.
""",
approach="""
### Patience walk-through on [10, 9, 2, 5, 3, 7, 101, 18]
| x | tails after | why |
|---|---|---|
| 10 | [10] | new pile |
| 9 | [9] | replace 10 (a smaller tail is better) |
| 2 | [2] | replace 9 |
| 5 | [2, 5] | bigger than every tail → new pile |
| 3 | [2, 3] | replace 5 |
| 7 | [2, 3, 7] | new pile |
| 101 | [2, 3, 7, 101] | new pile |
| 18 | [2, 3, 7, 18] | replace 101 |
Length **4**. (`tails` isn't necessarily a real subsequence, but its length is correct.)
""",
hints=["DP: lis[i] = longest increasing subsequence that ends at index i.", "Faster: keep the smallest possible tail for each length, and binary-search where each number goes."],
starter=r'''def length_of_lis(nums):
    pass
''',
solution=r'''import bisect

def length_of_lis(nums):
    tails = []                                   # tails[k] = smallest tail of an increasing subseq of length k+1
    for x in nums:
        i = bisect.bisect_left(tails, x)         # the first tail >= x
        if i == len(tails):
            tails.append(x)                      # x extends the longest subsequence
        else:
            tails[i] = x                         # x is a better (smaller) tail for length i+1
    return len(tails)
''',
complexity="**Time O(n log n)** (the DP version is O(n²)). **Space O(n)**.",
mistakes="- Using `bisect_right`, which allows equal numbers and breaks *strictly* increasing.",
tests=r'''
T("example 1", lambda: length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)
T("example 2", lambda: length_of_lis([0, 1, 0, 3, 2, 3]), 4)
T("all equal", lambda: length_of_lis([7, 7, 7]), 1)
T("increasing", lambda: length_of_lis(list(range(2000))), 2000)
''')

P(id="combination-sum-iv", topic="dp-1d", level="Medium", blind=True, lc=377, title="Combination Sum IV",
statement="""
Given distinct positive `nums` and a `target`, return the number of **ordered** sequences (different orders count as different) of numbers from `nums` that add up to `target`. Numbers can be reused.
""",
examples="""
```text
combination_sum4([1, 2, 3], 4) → 7
(1,1,1,1) (1,1,2) (1,2,1) (2,1,1) (2,2) (1,3) (3,1)
```
""",
eli10="""
This is **Climbing Stairs where the allowed step sizes are `nums`**! "How many ways to climb to `target`, using steps of 1, 2 or 3?" Order matters (1+2 differs from 2+1), exactly like different step patterns on stairs.

`ways[t]` = the number of sequences summing to t. The last number could be any n in nums: `ways[t] = sum(ways[t − n] for n in nums if n ≤ t)`, with `ways[0] = 1`.

(If order **didn't** matter, it'd be the "coin change ways" problem, where the loops are swapped: coins on the outside.)
""",
approach="Build `ways` from 1 to target. The outer loop is over the target and the inner loop over nums, which counts orderings.",
hints=["Same as climbing stairs with custom step sizes.", "ways[t] = Σ ways[t - n]; ways[0] = 1."],
starter=r'''def combination_sum4(nums, target):
    pass
''',
solution=r'''def combination_sum4(nums, target):
    ways = [1] + [0] * target              # ways[0] = 1: the empty sequence
    for t in range(1, target + 1):
        for n in nums:
            if n <= t:
                ways[t] += ways[t - n]     # the last number used was n
    return ways[target]
''',
complexity="**Time O(target × len(nums))**, **Space O(target)**.",
tests=r'''
T("example", lambda: combination_sum4([1, 2, 3], 4), 7)
T("impossible", lambda: combination_sum4([9], 3), 0)
T("stairs", lambda: combination_sum4([1, 2], 10), 89)
''')

# ============================================================ 2-D DP
P(id="unique-paths", topic="dp-2d", level="Medium", blind=True, lc=62, title="Unique Paths",
statement="""
A robot starts at the top-left of an `m × n` grid and can move only **right** or **down**. How many different paths reach the bottom-right?
""",
examples="""
```text
unique_paths(3, 7) → 28        unique_paths(3, 2) → 3
```
""",
eli10="""
**What it's really asking:** "Count the different routes through a city grid going only east or south."

**DP in 2-D:** how many ways reach cell (r, c)? The robot's **last move** came either from the cell **above** or from the cell to the **left**. So:
`paths[r][c] = paths[r−1][c] + paths[r][c−1]`

The whole top row and the whole left column have exactly **1** path each (just keep going straight).

```text
1  1  1  1
1  2  3  4
1  3  6  10      ← each cell = the one above + the one to the left
```
You can keep only one row and update it in place: `row[c] += row[c-1]`.

(Bonus maths answer: you make (m−1) down moves and (n−1) right moves in some order, which is `C(m+n−2, m−1)`.)
""",
approach="`row = [1] * n`. Repeat m−1 times: for c in 1..n−1: `row[c] += row[c-1]`. Return `row[-1]`.",
hints=["paths to a cell = paths from above + paths from the left.", "The first row and the first column are all 1."],
starter=r'''def unique_paths(m, n):
    pass
''',
solution=r'''def unique_paths(m, n):
    row = [1] * n                       # top row: only one way to reach each cell
    for _ in range(m - 1):
        for c in range(1, n):
            row[c] += row[c - 1]        # from above (old row[c]) + from the left (row[c-1])
    return row[-1]
''',
complexity="**Time O(m·n)**, **Space O(n)**.",
tests=r'''
T("3 x 7", lambda: unique_paths(3, 7), 28)
T("3 x 2", lambda: unique_paths(3, 2), 3)
T("1 x 1", lambda: unique_paths(1, 1), 1)
T("big", lambda: unique_paths(23, 12), 193536720)
''')

P(id="lcs", topic="dp-2d", level="Medium", blind=True, lc=1143, title="Longest Common Subsequence",
statement="""
Return the length of the longest **subsequence** common to both strings `a` and `b` (the characters are in order but don't need to be adjacent).
""",
examples="""
```text
lcs("abcde", "ace")  → 3    ("ace")
lcs("abc", "abc")    → 3
lcs("abc", "def")    → 0
```
""",
eli10="""
**What it's really asking:** "What's the longest list of letters that appears, in order, in both words?" (It's used in `git diff` and in DNA comparison!)

**Fill in a table:** `dp[i][j]` = the LCS of the **first i letters of a** and the **first j letters of b**. Look at the last letters, `a[i-1]` and `b[j-1]`:
- If they're **equal**, use that letter! `dp[i][j] = dp[i-1][j-1] + 1`.
- If they're **different**, one of them isn't in the answer, so drop either one: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.

The first row and column are 0 (an empty string has nothing in common with anything).
""",
approach="""
### Table for "abcde" (rows) vs "ace" (columns)
```text
      ""  a  c  e
  ""   0  0  0  0
  a    0  1  1  1
  b    0  1  1  1
  c    0  1  2  2
  d    0  1  2  2
  e    0  1  2  3   ← answer 3
```
""",
hints=["dp[i][j] = LCS of a[:i] and b[:j].", "If the last chars match: dp[i-1][j-1] + 1. Else: max(dp[i-1][j], dp[i][j-1])."],
starter=r'''def lcs(a, b):
    pass
''',
solution=r'''def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1          # the letters match: use them
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])   # drop one letter
    return dp[m][n]
''',
complexity="**Time O(m·n)**, **Space O(m·n)** (O(min(m, n)) with two rows).",
mistakes="- `[[0] * (n+1)] * (m+1)` creates the SAME row repeated (see the Python object model chapter!). Use a comprehension.",
tests=r'''
T("ace", lambda: lcs("abcde", "ace"), 3)
T("same", lambda: lcs("abc", "abc"), 3)
T("none", lambda: lcs("abc", "def"), 0)
T("longer", lambda: lcs("oxcpqrsvwf", "shmtulqrypy"), 2)
''')

# ============================================================ GREEDY
P(id="max-subarray", topic="greedy", level="Medium", blind=True, lc=53, title="Maximum Subarray (Kadane's Algorithm)",
statement="""
Return the largest **sum** of a contiguous, non-empty subarray.
""",
examples="""
```text
max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])  → 6    ([4, -1, 2, 1])
max_subarray([-3, -1, -2])                     → -1
```
""",
eli10="""
**Real-life picture:** you walk along a road picking up coins (+) and paying tolls (−). You're allowed to choose where to **start** and **stop** your walk. What's the most money you can end with?

**Kadane's insight:** keep a running total of "the best walk that **ends right here**". At each new number, ask: _"Is my running total helping me or hurting me?"_ If the running total is **negative**, throw it away and **start fresh** from here. A negative past can only make the future worse.

`current = max(x, current + x)` and `best = max(best, current)`.
""",
approach="""
### Walk-through on [-2, 1, -3, 4, -1, 2, 1, -5, 4]
| x | current (best ending here) | best |
|---|---|---|
| −2 | −2 | −2 |
| 1 | max(1, −1) = 1 | 1 |
| −3 | −2 | 1 |
| 4 | max(4, 2) = 4 (fresh start!) | 4 |
| −1 | 3 | 4 |
| 2 | 5 | 5 |
| 1 | **6** | 6 |
| −5 | 1 | 6 |
| 4 | 5 | 6 |
""",
hints=["Track the best sum of a subarray ending at the current index.", "If the running sum goes negative, starting fresh is better."],
starter=r'''def max_subarray(nums):
    pass
''',
solution=r'''def max_subarray(nums):
    current = best = nums[0]
    for x in nums[1:]:
        current = max(x, current + x)     # extend the walk, or restart here if the past is a burden
        best = max(best, current)
    return best
''',
complexity="**Time O(n)**, **Space O(1)**.",
mistakes="- Starting `best = 0`, which fails when every number is negative.",
tests=r'''
T("example", lambda: max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
T("all negative", lambda: max_subarray([-3, -1, -2]), -1)
T("single", lambda: max_subarray([1]), 1)
T("all positive", lambda: max_subarray([5, 4, -1, 7, 8]), 23)
''')

P(id="jump-game", topic="greedy", level="Medium", blind=True, lc=55, title="Jump Game",
statement="""
You start at index 0. `nums[i]` is the **maximum** jump length from index i. Return `True` if you can reach the last index.
""",
examples="""
```text
can_jump([2, 3, 1, 1, 4])  → True
can_jump([3, 2, 1, 0, 4])  → False   (every route lands on the 0 at index 3 and gets stuck)
```
""",
eli10="""
**Real-life picture:** stepping stones across a river. Each stone says how far you can leap from it.

**Greedy idea:** walk from left to right and remember the **farthest stone you could possibly reach** so far (`reach`). At each stone i:
- If `i > reach`, you can't even get to this stone. You're stuck, so return False.
- Otherwise, from here you could reach `i + nums[i]`. Update `reach`.

If `reach` gets to the last index, return True. You never need to plan the exact route; you only track how far your reach extends.
""",
approach="`reach = 0`. For each i: if i > reach → False. Set reach = max(reach, i + nums[i]). Return True.",
hints=["Track the farthest index reachable so far.", "If the current index is beyond that, you're stuck."],
starter=r'''def can_jump(nums):
    pass
''',
solution=r'''def can_jump(nums):
    reach = 0                           # the farthest index we can get to so far
    for i, jump in enumerate(nums):
        if i > reach:
            return False                # this stone is out of reach
        reach = max(reach, i + jump)
        if reach >= len(nums) - 1:
            return True
    return True
''',
complexity="**Time O(n)**, **Space O(1)**.",
tests=r'''
T("reachable", lambda: can_jump([2, 3, 1, 1, 4]), True)
T("stuck", lambda: can_jump([3, 2, 1, 0, 4]), False)
T("single", lambda: can_jump([0]), True)
T("zero at start", lambda: can_jump([0, 1]), False)
''')
