from lib import P

P(id="largest-number", topic="arrays", level="Warm-up", title="Find the Largest Number",
statement="""
Given a non-empty list of numbers `nums`, return the largest one. **Don't use the built-in `max()`.** The point is to practise walking through a list yourself.
""",
examples="""
```text
largest([3, 9, 2, 7])   → 9
largest([-5, -2, -8])   → -2
largest([4])            → 4
```
""",
eli10="""
Imagine a pile of exam papers. You want the top score. You pick up the first paper and say "this is the best so far". Then you look at each next paper: if it's higher, it becomes the new "best so far". When the pile is finished, the "best so far" is the answer.
""",
approach="""
1. Start with `best = nums[0]` (not 0! The list may contain only negative numbers).
2. Loop through every number `x`.
3. If `x > best`, update `best = x`.
4. Return `best`.

This "keep a running best" idea appears in many harder problems (Best Time to Buy and Sell Stock, Maximum Subarray), so learn it well.
""",
hints=["Keep a variable for the 'best so far'.", "Start it at the first element, not at 0."],
starter=r'''def largest(nums):
    # walk through the list and remember the best value seen so far
    pass
''',
solution=r'''def largest(nums):
    best = nums[0]          # start with the first number, so negatives work too
    for x in nums:
        if x > best:
            best = x        # found a bigger one, so remember it
    return best
''',
complexity="**Time O(n)**: we look at each number once. **Space O(1)**: just one variable.",
mistakes="- Starting with `best = 0`. Then `[-5, -2]` wrongly returns 0.",
tests=r'''
T("example 1", lambda: largest([3, 9, 2, 7]), 9)
T("all negative", lambda: largest([-5, -2, -8]), -2)
T("single item", lambda: largest([4]), 4)
T("max at the end", lambda: largest([1, 2, 3, 100]), 100)
''')

P(id="count-items", topic="arrays", level="Warm-up", title="Count Each Item (Frequency Map)",
statement="""
Given a list `items`, return a **dictionary** mapping each distinct item to how many times it appears.
""",
examples="""
```text
count_items(["a", "b", "a", "c", "a"])  → {"a": 3, "b": 1, "c": 1}
count_items([])                          → {}
```
""",
eli10="""
Think of counting votes in a class election. You have a sheet of paper. For each vote, you find the candidate's name on the sheet and add a tally mark. If the name isn't there yet, you write it down with one mark.

A Python **dictionary** is exactly that sheet: names (keys) next to counts (values). Finding a name in a dictionary is super fast (it doesn't search the whole sheet), which is why dictionaries power so many interview answers.
""",
approach="""
1. Make an empty dict `counts = {}`.
2. For each item: `counts[item] = counts.get(item, 0) + 1`. `.get(item, 0)` means "the current count, or 0 if it isn't there yet".
3. Return `counts`.

In real code you'd write `collections.Counter(items)`, but build it by hand once so you understand it.
""",
hints=["Use `dict.get(key, 0)` to read a count that may not exist yet."],
starter=r'''def count_items(items):
    counts = {}
    # add 1 to the count of each item
    return counts
''',
solution=r'''def count_items(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1   # 0 if we haven't seen it yet
    return counts
''',
complexity="**Time O(n)**: each dict update is O(1) on average. **Space O(k)**, where k is the number of distinct items.",
tests=r'''
T("example", lambda: count_items(["a", "b", "a", "c", "a"]), {"a": 3, "b": 1, "c": 1})
T("empty", lambda: count_items([]), {})
T("numbers", lambda: count_items([1, 1, 1]), {1: 3})
''')

P(id="contains-duplicate", topic="arrays", level="Easy", blind=True, lc=217, title="Contains Duplicate",
statement="""
Given a list of integers `nums`, return `True` if **any value appears at least twice**, and `False` if every element is different.
""",
examples="""
```text
contains_duplicate([1, 2, 3, 1])   → True    (1 appears twice)
contains_duplicate([1, 2, 3, 4])   → False
contains_duplicate([])             → False
```
""",
eli10="""
**What it's really asking:** "Is anything repeated?"

**Real-life picture:** you're the teacher taking attendance, and you suspect someone signed the sheet twice. One slow way: for every name, read the *whole* sheet again looking for the same name. A fast way: keep a **notebook of names you've already seen**. For each new name, check the notebook. If it's there, you've caught a duplicate. If not, write it in.

Checking a Python **set** is like flipping straight to the right page, not reading every page. That's why the set version is fast.
""",
approach="""
### Slow way first (brute force)
Compare every pair: element 0 with 1, 2, 3…, element 1 with 2, 3… That's about n×n/2 comparisons. With 100,000 numbers, that's 5 billion checks. Too slow.

### The clever idea: remember what you've seen
1. Make an empty set `seen`.
2. For each number `x`:
   - If `x` is already in `seen`, return `True` (duplicate found!).
   - Otherwise add it: `seen.add(x)`.
3. If the loop ends, there are no duplicates, so return `False`.

### Walk-through on `[1, 2, 3, 1]`
| x | seen before | in seen? | action |
|---|---|---|---|
| 1 | {} | no | add → {1} |
| 2 | {1} | no | add → {1, 2} |
| 3 | {1, 2} | no | add → {1, 2, 3} |
| 1 | {1, 2, 3} | **yes** | return True |

**One-liner** (good to mention): `return len(set(nums)) != len(nums)`. A set drops duplicates, so if it shrank, something was repeated. It's simpler, but it can't stop early.
""",
hints=["What data structure answers 'have I seen this before?' instantly?", "A set. Check before you add."],
starter=r'''def contains_duplicate(nums):
    pass
''',
solution=r'''def contains_duplicate(nums):
    seen = set()                 # numbers we've met so far
    for x in nums:
        if x in seen:            # O(1) average lookup
            return True          # caught a repeat, so stop early
        seen.add(x)
    return False
''',
complexity="**Time O(n)**: one pass, and each set check is O(1) on average. **Space O(n)**: in the worst case the set holds every number.",
mistakes="""
- Using a **list** for `seen`. `x in list` scans the whole list, which brings back O(n²).
- Sorting first works (duplicates become neighbours) but costs O(n log n). Mention it as an option if memory is tight.
""",
tests=r'''
T("example 1", lambda: contains_duplicate([1, 2, 3, 1]), True)
T("example 2", lambda: contains_duplicate([1, 2, 3, 4]), False)
T("empty list", lambda: contains_duplicate([]), False)
T("many repeats", lambda: contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]), True)
T("big, all different", lambda: contains_duplicate(list(range(100000))), False)
''')

P(id="valid-anagram", topic="arrays", level="Easy", blind=True, lc=242, title="Valid Anagram",
statement="""
Given two strings `s` and `t`, return `True` if `t` is an **anagram** of `s`: it uses exactly the same letters, the same number of times, possibly in a different order.
""",
examples="""
```text
is_anagram("anagram", "nagaram")  → True
is_anagram("rat", "car")          → False
is_anagram("aab", "abb")          → False   (counts differ)
```
""",
eli10="""
**What it's really asking:** "Can I rearrange the letters of one word to make the other?"

**Real-life picture:** two Scrabble players each have a bag of letter tiles. Are the bags identical? Tip each bag out and **count each letter**: 3 A's, 1 N, 1 G… If every count matches, the bags are the same. The order of the tiles doesn't matter, only the counts.
""",
approach="""
### Idea: compare letter counts
1. If the lengths differ, return `False` immediately.
2. Count the letters of `s` in a dict (the frequency map from the warm-up!).
3. Count the letters of `t` the same way.
4. Return whether the two dicts are equal.

### Walk-through: "rat" vs "car"
- counts("rat") = {r:1, a:1, t:1}
- counts("car") = {c:1, a:1, r:1}
- t ≠ c, so they're not equal. Return **False**.

### Alternatives
- `sorted(s) == sorted(t)`: simplest, O(n log n).
- `Counter(s) == Counter(t)`: the Pythonic one-liner, O(n).
""",
hints=["Anagram means same letters with the same counts.", "Count with a dict (or Counter) and compare."],
starter=r'''def is_anagram(s, t):
    pass
''',
solution=r'''def is_anagram(s, t):
    if len(s) != len(t):
        return False                    # different sizes can't be anagrams
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1     # add letters from s
    for ch in t:
        if counts.get(ch, 0) == 0:
            return False                # t uses a letter s doesn't have (enough of)
        counts[ch] -= 1                 # use up one tile
    return True                         # equal lengths + nothing ran out = same bags
''',
complexity="**Time O(n)**. **Space O(1)** for lowercase English letters (at most 26 keys), O(k) in general.",
mistakes="- Comparing `set(s) == set(t)`. Sets forget counts, so \"aab\" and \"abb\" would wrongly match.",
tests=r'''
T("example 1", lambda: is_anagram("anagram", "nagaram"), True)
T("example 2", lambda: is_anagram("rat", "car"), False)
T("counts differ", lambda: is_anagram("aab", "abb"), False)
T("different lengths", lambda: is_anagram("a", "ab"), False)
T("empty strings", lambda: is_anagram("", ""), True)
''')

P(id="two-sum", topic="arrays", level="Easy", blind=True, lc=1, title="Two Sum",
statement="""
Given a list of integers `nums` and an integer `target`, return the **indices** `[i, j]` (with i < j) of the two numbers that add up to `target`. Exactly one answer exists, and you may not use the same element twice.
""",
examples="""
```text
two_sum([2, 7, 11, 15], 9)  → [0, 1]    (2 + 7 = 9)
two_sum([3, 2, 4], 6)       → [1, 2]    (2 + 4 = 6)
two_sum([3, 3], 6)          → [0, 1]
```
""",
eli10="""
**What it's really asking:** "Which two numbers make the target, and where are they?"

**Real-life picture:** you have ₹9 and want to buy exactly two items from a shelf. You walk along the shelf. At each item (say it costs ₹2) you think: _"I'd need a partner costing ₹9 − ₹2 = ₹7. Have I already passed a ₹7 item?"_ If you kept a **notebook of prices you've seen and where they were**, you can answer instantly.

The trick is to stop asking "which pair works?" and ask "**what partner do I need, and have I seen it?**"
""",
approach="""
### Slow way: try every pair
Two loops: i from 0, j from i+1, check `nums[i] + nums[j] == target`. That's O(n²). It works, but it's too slow for big inputs.

### Clever way: one pass with a dict
1. `seen = {}` maps a **value** to its **index**.
2. For each index `i` with value `x`:
   - `need = target - x`
   - If `need` is in `seen`, return `[seen[need], i]`.
   - Otherwise store `seen[x] = i`.

Check **before** storing, so you don't pair a number with itself.

### Walk-through: nums = [2, 7, 11, 15], target = 9
| i | x | need | seen before | found? |
|---|---|---|---|---|
| 0 | 2 | 7 | {} | no → seen = {2: 0} |
| 1 | 7 | 2 | {2: 0} | **yes** → return [0, 1] |
""",
hints=["For each number x, which number do you need to reach the target?", "Store numbers you've seen in a dict: value → index.", "Check for the partner before adding the current number."],
starter=r'''def two_sum(nums, target):
    pass
''',
solution=r'''def two_sum(nums, target):
    seen = {}                          # value -> index where we saw it
    for i, x in enumerate(nums):
        need = target - x              # the partner that would complete the pair
        if need in seen:
            return [seen[need], i]     # partner was earlier, so its index is smaller
        seen[x] = i                    # remember x for future numbers
    return []                          # (the problem promises we never get here)
''',
complexity="**Time O(n)**: one pass with O(1) dict lookups. **Space O(n)** for the dict.",
mistakes="""
- Storing before checking: with `[3, 3]` and target 6 you might match index 0 with itself.
- Sorting the list first loses the original indices (two pointers works only if you keep track of them).
""",
tests=r'''
T("example 1", lambda: two_sum([2, 7, 11, 15], 9), [0, 1])
T("example 2", lambda: two_sum([3, 2, 4], 6), [1, 2])
T("duplicates", lambda: two_sum([3, 3], 6), [0, 1])
T("negatives", lambda: two_sum([-1, -2, -3, -4, -5], -8), [2, 4])
T("big input", lambda: two_sum(list(range(100000)), 199997), [99998, 99999])
''')

P(id="group-anagrams", topic="arrays", level="Medium", blind=True, lc=49, title="Group Anagrams",
statement="""
Given a list of strings `words`, group the anagrams together. Return a list of groups. Any order of groups, and of words within a group, is accepted.
""",
examples="""
```text
group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
→ [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
group_anagrams([""])   → [[""]]
```
""",
eli10="""
**What it's really asking:** "Put words made of the same letters into the same box."

**Real-life picture:** you're sorting letters (mail) into pigeonholes. Each pigeonhole needs a **label** so that all anagrams get the same label. A good label: **the word's letters sorted alphabetically**. "eat" → "aet", "tea" → "aet", "ate" → "aet". Same label, same pigeonhole!

So the problem becomes: _compute a label for each word, then group the words by label_. Grouping by a label is exactly what a dictionary of lists does.
""",
approach="""
1. `groups = defaultdict(list)` maps a label to a list of words.
2. For each word: `label = "".join(sorted(word))`, then `groups[label].append(word)`.
3. Return `list(groups.values())`.

### Walk-through
| word | label | groups after |
|---|---|---|
| eat | aet | {aet: [eat]} |
| tea | aet | {aet: [eat, tea]} |
| tan | ant | {…, ant: [tan]} |
| ate | aet | {aet: [eat, tea, ate], …} |
| nat | ant | {…, ant: [tan, nat]} |
| bat | abt | {…, abt: [bat]} |

### Faster label (bonus)
Sorting costs O(k log k) per word. Instead count the 26 letters and use the counts tuple as the label: `tuple(count)`. That's O(k). Tuples work as dict keys because they're **hashable**; lists aren't.
""",
hints=["Anagrams share something when you sort their letters.", "Use that sorted string as a dict key.", "`defaultdict(list)` saves you from 'if key not in dict' checks."],
starter=r'''def group_anagrams(words):
    pass
''',
solution=r'''from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)            # label -> words with that label
    for w in words:
        label = "".join(sorted(w))        # "tea" -> "aet": same for all anagrams
        groups[label].append(w)
    return list(groups.values())
''',
complexity="**Time O(n · k log k)**, where n is the number of words and k the word length (sorting each word). The counting-label version is O(n · k). **Space O(n · k)**.",
mistakes="- Using a list as a dict key → `TypeError: unhashable type: 'list'`. Convert it to a tuple or string first.",
tests=r'''
T("example", lambda: group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]),
  [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]], same_groups)
T("empty word", lambda: group_anagrams([""]), [[""]], same_groups)
T("single", lambda: group_anagrams(["a"]), [["a"]], same_groups)
T("no anagrams", lambda: group_anagrams(["abc", "def"]), [["abc"], ["def"]], same_groups)
''')

P(id="product-except-self", topic="arrays", level="Medium", blind=True, lc=238, title="Product of Array Except Self",
statement="""
Given a list `nums`, return a list `answer` where `answer[i]` is the product of **all numbers except `nums[i]`**. You may **not use division**, and it should run in O(n).
""",
examples="""
```text
product_except_self([1, 2, 3, 4])      → [24, 12, 8, 6]
product_except_self([-1, 1, 0, -3, 3]) → [0, 0, 9, 0, 0]
```
""",
eli10="""
**What it's really asking:** for each position, multiply everything **to its left** and everything **to its right**.

**Real-life picture:** people stand in a queue. For each person, you want "the product of everyone except me". Split it into two questions: _what's the product of everyone **in front of** me?_ and _of everyone **behind** me?_ Multiply those two answers.

You can find "everyone in front" for all people in one walk from the front (keep a running product), and "everyone behind" in one walk from the back.
""",
approach="""
### Why not division?
Total product ÷ nums[i] breaks when there's a 0 (you'd divide by zero), and the problem forbids it anyway.

### Two passes
1. `answer[i]` = product of everything **left** of i. Walk left to right with `left = 1`: store `answer[i] = left`, then `left *= nums[i]`.
2. Walk right to left with `right = 1`: `answer[i] *= right`, then `right *= nums[i]`.

### Walk-through on [1, 2, 3, 4]
| i | left product (before i) | right product (after i) | answer |
|---|---|---|---|
| 0 | 1 | 2·3·4 = 24 | 24 |
| 1 | 1 | 3·4 = 12 | 12 |
| 2 | 1·2 = 2 | 4 | 8 |
| 3 | 1·2·3 = 6 | 1 | 6 |

The key trick is **storing the left products in the answer list itself**, so you only need O(1) extra space besides the output.
""",
hints=["Product except me = (product of everything to my left) × (product of everything to my right).", "Compute the left products in one pass and the right products in a second pass, backwards."],
starter=r'''def product_except_self(nums):
    pass
''',
solution=r'''def product_except_self(nums):
    n = len(nums)
    answer = [1] * n
    left = 1
    for i in range(n):              # pass 1: product of everything LEFT of i
        answer[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):  # pass 2: multiply in everything RIGHT of i
        answer[i] *= right
        right *= nums[i]
    return answer
''',
complexity="**Time O(n)**: two passes. **Space O(1)** extra (the output list doesn't count).",
mistakes="- Updating `left` **before** storing it. Then you include nums[i] in its own product.",
tests=r'''
T("example 1", lambda: product_except_self([1, 2, 3, 4]), [24, 12, 8, 6])
T("with a zero", lambda: product_except_self([-1, 1, 0, -3, 3]), [0, 0, 9, 0, 0])
T("two zeros", lambda: product_except_self([0, 4, 0]), [0, 0, 0])
T("two numbers", lambda: product_except_self([2, 3]), [3, 2])
''')

P(id="encode-decode-strings", topic="arrays", level="Medium", blind=True, lc=271, title="Encode and Decode Strings",
statement="""
Write `encode(strs)`, which turns a list of strings into **one string**, and `decode(s)`, which turns it back into the original list. The strings may contain **any** characters, including commas, `#`, digits, and empty strings.
""",
examples="""
```text
decode(encode(["hello", "world"]))   → ["hello", "world"]
decode(encode(["", "a#b", "3#x"]))   → ["", "a#b", "3#x"]
decode(encode([]))                   → []
```
""",
eli10="""
**What it's really asking:** pack many strings into one so they can be unpacked **exactly**, even if they contain your "separator" characters.

**Real-life picture:** you're sending several parcels in one big box. If you just throw them in, the receiver can't tell where one parcel ends. Gluing a comma between them fails as soon as a parcel itself contains a comma.

Solution: write the **length on each parcel's label**: "5#hello5#world". The receiver reads digits up to `#` (that's the length, 5), then takes **exactly 5 characters**, whatever they are. Even if the parcel contains `#` or digits, it doesn't matter, because the receiver counts rather than searching for separators.
""",
approach="""
### Encode
For each string `s`: write `len(s)`, then `#`, then `s`. Join them all.
`["a#b", ""]` → `"3#a#b" + "0#"` = `"3#a#b0#"`.

### Decode
Use an index `i` starting at 0:
1. Find the `#` starting from `i`: `j = s.index("#", i)`.
2. The length is `int(s[i:j])`.
3. The string is `s[j+1 : j+1+length]`.
4. Move `i = j + 1 + length` and repeat until the end.

### Why it's safe
The decoder **never looks inside** the content for separators. It jumps over exactly `length` characters. This "length-prefix" framing is how real network protocols (HTTP/2, many binary formats) work.
""",
hints=["A plain separator fails if a string contains it.", "Put the length of each string in front of it.", "While decoding, read the length first, then slice exactly that many characters."],
starter=r'''def encode(strs):
    pass

def decode(s):
    pass
''',
solution=r'''def encode(strs):
    return "".join(f"{len(s)}#{s}" for s in strs)   # "5#hello5#world"

def decode(s):
    out, i = [], 0
    while i < len(s):
        j = s.index("#", i)            # the first '#' after i ends the length digits
        length = int(s[i:j])
        start = j + 1
        out.append(s[start:start + length])   # take EXACTLY `length` characters
        i = start + length                     # jump to the next label
    return out
''',
complexity="**Time O(total characters)** for both. **Space O(total characters)** for the output.",
mistakes="- Splitting on `#` or `,`. That breaks when a string contains those characters, which is exactly what the tests check.",
tests=r'''
T("simple", lambda: decode(encode(["hello", "world"])), ["hello", "world"])
T("tricky characters", lambda: decode(encode(["", "a#b", "3#x", "##"])), ["", "a#b", "3#x", "##"])
T("empty list", lambda: decode(encode([])), [])
T("one empty string", lambda: decode(encode([""])), [""])
T("long string", lambda: decode(encode(["x" * 1234, "y"])), ["x" * 1234, "y"])
C("encode returns a string", lambda: isinstance(encode(["a"]), str), "encode must return one str")
''')

P(id="longest-consecutive", topic="arrays", level="Medium", blind=True, lc=128, title="Longest Consecutive Sequence",
statement="""
Given an **unsorted** list of integers, return the length of the longest run of consecutive numbers (like 4, 5, 6, 7). The numbers don't need to be next to each other in the list. Aim for **O(n)**, which rules out sorting.
""",
examples="""
```text
longest_consecutive([100, 4, 200, 1, 3, 2])           → 4    (1, 2, 3, 4)
longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])   → 9    (0 through 8)
longest_consecutive([])                                → 0
```
""",
eli10="""
**What it's really asking:** "What's the longest chain of numbers that follow one after another, like 1-2-3-4?"

**Real-life picture:** roll numbers are written on scattered cards on the floor. You want the longest run of roll numbers with no gaps. Smart approach: only **start counting from a card that has no card just before it** (no "n − 1"). For example, 1 is a start because 0 is missing. From each start, count upward (2? yes. 3? yes. 4? yes. 5? no), so the run is 4.

Why only start at chain beginnings? If you started counting at every card, you'd recount the same chain over and over (2→3→4, then 3→4…), which is slow.
""",
approach="""
1. Put all the numbers in a set, so "is x present?" is O(1).
2. For each number `x` in the set:
   - If `x - 1` is in the set, **skip it**, because `x` isn't the start of a chain.
   - Otherwise count up: `length = 1`, and while `x + length` is in the set, `length += 1`.
   - Keep the best length.

### Walk-through: {100, 4, 200, 1, 3, 2}
| x | x−1 present? | start? | chain | length |
|---|---|---|---|---|
| 100 | 99 no | yes | 100 | 1 |
| 4 | 3 yes | skip | — | — |
| 200 | 199 no | yes | 200 | 1 |
| 1 | 0 no | yes | 1, 2, 3, 4 | **4** |
| 3, 2 | yes | skip | — | — |

### Why it's O(n) even with a nested while loop
Each number is visited by the inner while loop **at most once** in total, because only chain starts begin counting. So the total work is about 2n.
""",
hints=["Sorting would be O(n log n). Can a set help?", "A number starts a chain only if (number − 1) is missing.", "From each chain start, count upward while the next number exists."],
starter=r'''def longest_consecutive(nums):
    pass
''',
solution=r'''def longest_consecutive(nums):
    present = set(nums)
    best = 0
    for x in present:
        if x - 1 in present:
            continue                    # not a chain start, so skip (keeps it O(n))
        length = 1
        while x + length in present:    # walk up the chain
            length += 1
        best = max(best, length)
    return best
''',
complexity="**Time O(n)**: each number is part of at most one upward walk. **Space O(n)** for the set.",
mistakes="""
- Looping over `nums` instead of the set. With many duplicates, this repeats work.
- Forgetting the chain-start check. That becomes O(n²) on input like `range(n)`.
""",
tests=r'''
T("example 1", lambda: longest_consecutive([100, 4, 200, 1, 3, 2]), 4)
T("example 2", lambda: longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), 9)
T("empty", lambda: longest_consecutive([]), 0)
T("duplicates", lambda: longest_consecutive([1, 2, 0, 1]), 3)
T("big range (must be fast)", lambda: longest_consecutive(list(range(200000, 0, -1))), 200000)
''')
