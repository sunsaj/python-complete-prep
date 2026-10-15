from lib import P

# ============================================================ BACKTRACKING
P(id="binary-strings", topic="backtracking", level="Warm-up", title="All Binary Strings of Length n",
statement="""
Return all strings of length `n` made of `0` and `1`, in increasing order.
""",
examples="""
```text
binary_strings(2)  → ["00", "01", "10", "11"]
```
""",
eli10="""
Think of filling `n` empty boxes. For the first box you **choose** 0 or 1. For each choice you go on and fill the next box, and so on. When all boxes are filled, write the string down. Then **go back** (undo) and try the other choice.

That's **backtracking**: _choose → explore → un-choose_. It's like exploring every path in a maze, stepping back when you reach the end.
""",
approach="""
```text
def go(path):
    if len(path) == n: result.append("".join(path)); return
    for bit in "01":
        path.append(bit)     # choose
        go(path)             # explore
        path.pop()           # un-choose (backtrack)
```
""",
hints=["Recursion: at each position, try '0' then '1'.", "Append, recurse, then pop to undo."],
starter=r'''def binary_strings(n):
    pass
''',
solution=r'''def binary_strings(n):
    result, path = [], []
    def go():
        if len(path) == n:
            result.append("".join(path))
            return
        for bit in "01":
            path.append(bit)       # choose
            go()                   # explore
            path.pop()             # undo the choice
    go()
    return result
''',
complexity="**Time O(2ⁿ · n)**: there are 2ⁿ strings. **Space O(n)** for the recursion (plus the output).",
tests=r'''
T("n = 2", lambda: binary_strings(2), ["00", "01", "10", "11"])
T("n = 1", lambda: binary_strings(1), ["0", "1"])
T("n = 3 count", lambda: len(binary_strings(3)), 8)
''')

P(id="subsets", topic="backtracking", level="Medium", lc=78, title="Subsets (DSA extra)",
statement="""
Given distinct integers `nums`, return **all subsets** (the power set), in any order.
""",
examples="""
```text
subsets([1, 2, 3]) → [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
```
""",
eli10="""
For each number, you make a yes/no decision: **take it** or **leave it**. With 3 numbers there are 2×2×2 = 8 decision combinations, so 8 subsets. It's the same as binary strings, where 1 means "take" and 0 means "leave"!
""",
approach="""
`go(i)`: decide for `nums[i]`.
- If `i == len(nums)`: record a copy of `path`.
- Leave it: `go(i + 1)`.
- Take it: append, `go(i + 1)`, pop.
""",
hints=["Each element is either in or out.", "Record `path[:]` (a copy!), not `path` itself."],
starter=r'''def subsets(nums):
    pass
''',
solution=r'''def subsets(nums):
    result, path = [], []
    def go(i):
        if i == len(nums):
            result.append(path[:])          # a copy: path keeps changing
            return
        go(i + 1)                           # leave nums[i]
        path.append(nums[i])                # take nums[i]
        go(i + 1)
        path.pop()
    go(0)
    return result
''',
complexity="**Time O(2ⁿ · n)**, **Space O(n)** for the recursion.",
mistakes="- `result.append(path)` without copying. Every entry then points to the same list, which is empty at the end.",
tests=r'''
T("three", lambda: subsets([1, 2, 3]), [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]], same_groups)
T("one", lambda: subsets([0]), [[], [0]], same_groups)
T("count", lambda: len(subsets(list(range(10)))), 1024)
''')

P(id="combination-sum", topic="backtracking", level="Medium", lc=39, title="Combination Sum (DSA extra)",
statement="""
Given distinct positive `candidates` and a `target`, return all **unique combinations** that sum to target. You may reuse a number **unlimited times**. Combinations are unordered: [2,2,3] is the same as [3,2,2].
""",
examples="""
```text
combination_sum([2, 3, 6, 7], 7)  → [[2, 2, 3], [7]]
combination_sum([2, 3, 5], 8)     → [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
```
""",
eli10="""
**Real-life picture:** you need to pay exactly ₹7 using coins of ₹2, ₹3, ₹6 and ₹7, as many of each as you like. List every different way.

To avoid counting [2,3,2] and [3,2,2] as different, always pick coins in **non-decreasing order**: once you move past the ₹2 coin, never go back to it. In code, pass a `start` index and only choose from `candidates[start:]`.
""",
approach="""
`go(start, remaining)`:
- `remaining == 0` → record the path.
- For `i` from `start`: let c = candidates[i]. If `c > remaining`, stop (when sorted). Otherwise choose c and call `go(i, remaining - c)`. Pass **i**, not i+1, because reuse is allowed. Then undo.
""",
hints=["Pass a start index to avoid duplicate orderings.", "Recurse with the same index i because numbers can be reused.", "Stop when remaining becomes negative (sort candidates to prune early)."],
starter=r'''def combination_sum(candidates, target):
    pass
''',
solution=r'''def combination_sum(candidates, target):
    candidates = sorted(candidates)
    result, path = [], []
    def go(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remaining:
                break                        # sorted, so every later coin is too big as well
            path.append(c)
            go(i, remaining - c)             # i (not i+1): the same coin can be reused
            path.pop()
    go(0, target)
    return result
''',
complexity="Exponential in the worst case. Roughly **O(n^(target/min))**. Pruning helps a lot in practice.",
tests=r'''
T("example 1", lambda: combination_sum([2, 3, 6, 7], 7), [[2, 2, 3], [7]], same_groups)
T("example 2", lambda: combination_sum([2, 3, 5], 8), [[2, 2, 2, 2], [2, 3, 3], [3, 5]], same_groups)
T("impossible", lambda: combination_sum([2], 1), [], same_groups)
''')

P(id="word-search", topic="backtracking", level="Medium", blind=True, lc=79, title="Word Search",
statement="""
Given a 2-D grid of letters `board` and a `word`, return `True` if the word can be traced by moving **up, down, left, or right** through adjacent cells, **without reusing a cell**.
""",
examples="""
```text
board = [["A","B","C","E"],
         ["S","F","C","S"],
         ["A","D","E","E"]]
exist(board, "ABCCED") → True     exist(board, "SEE") → True     exist(board, "ABCB") → False
```
""",
eli10="""
**What it's really asking:** "Can I spell the word by walking across a letter grid, one step at a time, never stepping on the same tile twice?"

**Real-life picture:** a crossword-style maze. Start on every tile that matches the **first letter**. From there, try all 4 directions for the next letter. If a direction fails, **step back** and try another (that's backtracking). While you're standing on a path, **mark the tiles you're using** (as if you put a coin on them) so you don't reuse them, and remove the coin when you step back.
""",
approach="""
`dfs(r, c, i)` asks: "Can I match `word[i:]` starting at cell (r, c)?"
1. If `i == len(word)`: True (everything matched).
2. If (r, c) is outside the grid, or `board[r][c] != word[i]`: False.
3. Mark it: `tmp = board[r][c]`, `board[r][c] = "#"`.
4. Try the 4 neighbours with `i + 1`.
5. Unmark: `board[r][c] = tmp`. Return whether any neighbour succeeded.

Try `dfs(r, c, 0)` from every cell.

**Speed-up:** if the board doesn't have enough of each letter the word needs (check with Counter), return False immediately.
""",
hints=["Start a search from every cell matching word[0].", "DFS to the 4 neighbours, matching the next letter.", "Temporarily mark the cell as used, and restore it after exploring (backtrack)."],
starter=r'''def exist(board, word):
    pass
''',
solution=r'''from collections import Counter

def exist(board, word):
    rows, cols = len(board), len(board[0])
    have = Counter(ch for row in board for ch in row)
    if any(have[ch] < n for ch, n in Counter(word).items()):
        return False                                   # not enough letters at all

    def dfs(r, c, i):
        if i == len(word):
            return True
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[i]:
            return False
        tmp, board[r][c] = board[r][c], "#"            # mark as used on the current path
        found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
                 dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
        board[r][c] = tmp                              # backtrack: un-mark
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
''',
complexity="**Time O(R · C · 4^L)** in the worst case (L = word length). **Space O(L)** recursion depth.",
mistakes="- Forgetting to restore the cell, which breaks later searches.\n- Using a global visited set that's never cleaned up after backtracking.",
tests=r'''
def _b(): return [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
T("ABCCED", lambda: exist(_b(), "ABCCED"), True)
T("SEE", lambda: exist(_b(), "SEE"), True)
T("ABCB (reuse)", lambda: exist(_b(), "ABCB"), False)
T("single cell", lambda: exist([["a"]], "a"), True)
T("missing letters", lambda: exist([["a", "b"]], "abc"), False)
''')

# ============================================================ TRIES
P(id="implement-trie", topic="tries", level="Medium", blind=True, lc=208, title="Implement Trie (Prefix Tree)",
statement="""
Implement a `Trie` with `insert(word)`, `search(word)` (is this exact word stored?) and `starts_with(prefix)` (does any stored word start with this prefix?).
""",
examples="""
```text
t = Trie(); t.insert("apple")
t.search("apple") → True;  t.search("app") → False;  t.starts_with("app") → True
t.insert("app");  t.search("app") → True
```
""",
eli10="""
**What is a trie?** A tree where **each step down is one letter**. Words that share a beginning share the same path, like a dictionary's index tabs: A → P → P → (L → E).

**Real-life picture:** the autocomplete on your phone keyboard. You type "ap", it walks down a → p, and everything below that point is a suggestion.

Each node has:
- `children`: a dict from letter to the next node,
- `end`: True if a word **ends** here. That's how "app" can be a word while "ap" is not.
""",
approach="""
- **insert:** start at the root. For each letter, create the child if it's missing and move down. At the end, set `end = True`.
- **search:** walk the letters. If one is missing, return False. At the end, return `node.end`.
- **starts_with:** the same walk, but at the end return True (you don't need `end`).

Each operation is O(length of the word), no matter how many words are stored!
""",
hints=["Each node: a dict of children plus an 'is end of word' flag.", "search and starts_with share the same walk; they differ only at the end."],
starter=r'''class Trie:
    def __init__(self):
        pass
    def insert(self, word):
        pass
    def search(self, word):
        pass
    def starts_with(self, prefix):
        pass
''',
solution=r'''class TrieNode:
    def __init__(self):
        self.children = {}      # letter -> TrieNode
        self.end = False        # does a word end here?

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())   # create the path if needed
        node.end = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None     # the path breaks
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.end

    def starts_with(self, prefix):
        return self._walk(prefix) is not None
''',
complexity="**O(L)** per operation (L = word length). **Space O(total letters inserted)**.",
tests=r'''
def _run():
    t = Trie(); t.insert("apple")
    out = [t.search("apple"), t.search("app"), t.starts_with("app")]
    t.insert("app"); out.append(t.search("app"))
    return out
T("example", _run, [True, False, True, True])
def _run2():
    t = Trie(); t.insert("a")
    return [t.search("a"), t.starts_with("b"), t.search(""), t.starts_with("")]
T("edge cases", _run2, [True, False, False, True])
def _run3():
    t = Trie()
    for w in ["car", "card", "care"]: t.insert(w)
    return [t.search("car"), t.search("ca"), t.starts_with("card"), t.search("cards")]
T("shared prefixes", _run3, [True, False, True, False])
''')

P(id="word-dictionary", topic="tries", level="Medium", blind=True, lc=211, title="Design Add and Search Words",
statement="""
Design `WordDictionary` with `add_word(word)` and `search(word)`, where the search pattern may contain `.`, which matches **any one letter**.
""",
examples="""
```text
d.add_word("bad"); d.add_word("dad"); d.add_word("mad")
d.search("pad") → False;  d.search("bad") → True;  d.search(".ad") → True;  d.search("b..") → True
```
""",
eli10="""
It's the Trie from the previous problem, plus **wildcards**. When the pattern has a normal letter, walk down that one branch. When it has a `.`, you don't know which branch, so **try every child** (that's a small DFS/backtracking). If any branch reaches the end of the pattern at a node where a word ends, it's a match.
""",
approach="""
`dfs(node, i)`:
- If `i == len(word)`: return `node.end`.
- `ch = word[i]`. If `ch == "."`: return True if `dfs(child, i+1)` is True for **any** child.
- Otherwise: go to `children[ch]` if it exists, else return False.
""",
hints=["Build on the Trie.", "On '.', recursively try all children."],
starter=r'''class WordDictionary:
    def __init__(self):
        pass
    def add_word(self, word):
        pass
    def search(self, word):
        pass
''',
solution=r'''class WordDictionary:
    def __init__(self):
        self.root = {}                      # dict-based trie: letter -> child dict; "$" marks a word end

    def add_word(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)
''',
complexity="add: **O(L)**. search: O(L) without dots, worst case **O(26^dots · L)**.",
tests=r'''
def _run():
    d = WordDictionary()
    for w in ["bad", "dad", "mad"]: d.add_word(w)
    return [d.search("pad"), d.search("bad"), d.search(".ad"), d.search("b.."), d.search("...."), d.search("..")]
T("example", _run, [False, True, True, True, False, False])
def _run2():
    d = WordDictionary(); d.add_word("a"); d.add_word("ab")
    return [d.search("."), d.search("a."), d.search(".b"), d.search("b")]
T("short words", _run2, [True, True, True, False])
def _run3():
    d = WordDictionary(); return d.search("a")
T("empty dict", _run3, False)
''')

P(id="word-search-ii", topic="tries", level="Hard", blind=True, lc=212, title="Word Search II",
statement="""
Given a letter grid `board` and a list of `words`, return **all words** that can be traced on the board (adjacent moves, no cell reused within a word). Any order.
""",
examples="""
```text
board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
find_words(board, ["oath", "pea", "eat", "rain"])  → ["eat", "oath"]
```
""",
eli10="""
**What it's really asking:** Word Search, but for **many words at once**.

Running Word Search separately for every word would repeat a lot of walking (words like "oath" and "oat" share most of their path). Instead, put **all the words in a Trie**, then do **one** DFS from each cell. As you walk the grid, you also walk down the trie. If the trie has no child for the next letter, **stop immediately**, because no word continues this way. When you reach a trie node where a word ends, you found one!

It's like walking through the maze with the whole dictionary in your hand, checking "does any word start like this?" at every step.
""",
approach="""
1. Build a trie, storing the complete word at its end node (`node["$"] = word`).
2. For each cell, run `dfs(r, c, trie_root)`:
   - `ch = board[r][c]`. If ch isn't a child of the node, return.
   - Move to `nxt = node[ch]`. If `"$"` is in nxt, record the word and **delete the marker** (so it's not found twice).
   - Mark the cell, recurse into the 4 neighbours, then unmark.
   - **Pruning:** if `nxt` becomes empty, remove it from its parent so dead branches are never searched again.
""",
hints=["Insert all words into a trie first.", "DFS the board while walking the trie at the same time.", "Stop when the trie has no matching child; remove found words to avoid duplicates."],
starter=r'''def find_words(board, words):
    pass
''',
solution=r'''def find_words(board, words):
    root = {}
    for w in words:                           # 1. build the trie
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w                         # store the full word at its end

    rows, cols, found = len(board), len(board[0]), []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.get(ch)
        if node is None:
            return                            # no word continues this way
        if "$" in node:
            found.append(node.pop("$"))       # found it; pop so it's reported only once
        board[r][c] = "#"                     # mark as used
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, node)
        board[r][c] = ch                      # un-mark
        if not node:
            parent.pop(ch)                    # prune an empty branch

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    return found
''',
complexity="Roughly **O(R · C · 4 · 3^(L−1))** in the worst case, but the trie pruning makes it much faster in practice. **Space O(total letters in words)**.",
tests=r'''
_b = lambda: [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
T("example", lambda: find_words(_b(), ["oath", "pea", "eat", "rain"]), ["eat", "oath"], same_items)
T("none", lambda: find_words([["a","b"],["c","d"]], ["abcb"]), [], same_items)
T("duplicate paths reported once", lambda: find_words([["a","a"]], ["aa", "a"]), ["a", "aa"], same_items)
T("shared prefix", lambda: find_words([["o","a","b","n"],["o","t","a","e"],["a","h","k","r"],["a","f","l","v"]], ["oa", "oaa"]), ["oa", "oaa"], same_items)
''')

# ============================================================ GRAPHS
P(id="flood-fill", topic="graphs", level="Easy", lc=733, title="Flood Fill (warm-up for grids)",
statement="""
Given a grid `image`, a start cell `(sr, sc)` and a `color`, recolour the start cell **and every cell connected to it** (up/down/left/right) that has the **same original colour**. Return the image.
""",
examples="""
```text
flood_fill([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2) → [[2,2,2],[2,2,0],[2,0,1]]
```
""",
eli10="""
This is the **paint bucket tool** in MS Paint! Click a spot and the colour spreads to every touching pixel of the same colour.

A grid is a **graph**: each cell is a node connected to its 4 neighbours. "Spread to all connected cells" is a **DFS** (go as deep as you can) or a **BFS** (spread in rings). This tiny pattern unlocks Number of Islands, Pacific Atlantic, and many more.
""",
approach="""
1. `old = image[sr][sc]`. If `old == color`, return immediately (otherwise you'd loop forever).
2. `dfs(r, c)`: if the cell is out of bounds or not `old`, stop. Otherwise paint it and dfs into the 4 neighbours.
""",
hints=["Remember the original colour first.", "If the new colour equals the old one, do nothing.", "DFS into the 4 neighbours that still have the old colour."],
starter=r'''def flood_fill(image, sr, sc, color):
    pass
''',
solution=r'''def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image                        # nothing to do (and avoids infinite recursion)
    rows, cols = len(image), len(image[0])
    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or image[r][c] != old:
            return
        image[r][c] = color                 # paint it (this also marks it visited)
        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)
    dfs(sr, sc)
    return image
''',
complexity="**Time O(R·C)**, **Space O(R·C)** recursion in the worst case.",
tests=r'''
T("example", lambda: flood_fill([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2), [[2,2,2],[2,2,0],[2,0,1]])
T("same colour", lambda: flood_fill([[0,0,0],[0,0,0]], 0, 0, 0), [[0,0,0],[0,0,0]])
T("single", lambda: flood_fill([[5]], 0, 0, 7), [[7]])
''')

P(id="number-of-islands", topic="graphs", level="Medium", blind=True, lc=200, title="Number of Islands",
statement="""
Given a grid of `"1"` (land) and `"0"` (water), count the **islands**: groups of land cells connected up/down/left/right.
""",
examples="""
```text
grid = [["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]]          → 3
```
""",
eli10="""
**Real-life picture:** you're flying over the sea with a map. Every time you spot land you **haven't visited yet**, that's a **new island**: count it! Then use the paint bucket (flood fill) to "sink" or colour the **whole island**, so you won't count it again. Keep scanning.

Number of islands = number of times you had to start a new flood fill.
""",
approach="""
1. `count = 0`.
2. For every cell: if it's `"1"`: `count += 1`, then `sink(r, c)`. Sink is a flood fill that turns all connected `"1"`s into `"0"`.
3. Return count.

### Walk-through on the example
- (0,0) is land, so count = 1, and sinking clears the 2×2 block at the top-left.
- (2,2) is land, so count = 2, and it sinks.
- (3,3) is land, so count = 3, and sinking clears (3,3) and (3,4).
""",
hints=["Scan every cell.", "When you find unvisited land, count it and flood-fill the whole island so it isn't counted again."],
starter=r'''def num_islands(grid):
    pass
''',
solution=r'''from collections import deque

def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            count += 1                          # a new island
            grid[r][c] = "0"
            queue = deque([(r, c)])             # BFS: sink the whole island
            while queue:
                x, y = queue.popleft()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1":
                        grid[nx][ny] = "0"      # mark it when queued, so it's never added twice
                        queue.append((nx, ny))
    return count
''',
complexity="**Time O(R·C)**: each cell is visited a constant number of times. **Space O(R·C)** in the worst case for the queue.",
mistakes="- Counting each land cell instead of each island.\n- Marking cells as visited only when **popped**, not when **pushed**. The same cell then gets queued many times.",
tests=r'''
T("example", lambda: num_islands([["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]), 3)
T("one big", lambda: num_islands([["1","1","1"],["0","1","0"],["1","1","1"]]), 1)
T("all water", lambda: num_islands([["0","0"],["0","0"]]), 0)
T("diagonal doesn't connect", lambda: num_islands([["1","0"],["0","1"]]), 2)
T("big grid", lambda: num_islands([["1"] * 300 for _ in range(300)]), 1)
''')

P(id="clone-graph", topic="graphs", level="Medium", blind=True, lc=133, title="Clone Graph",
statement="""
Given a node of a connected undirected graph (each `Node` has `.val` and `.neighbors`), return a **deep copy**: brand-new nodes with the same structure. (Tests build graphs with `build_graph(adjacency)`.)
""",
examples="""
```text
adjacency [[2, 4], [1, 3], [2, 4], [1, 3]]   (1-2-3-4-1, a square)
clone_graph(build_graph(...)) → a new square with the same connections, made of NEW Node objects
```
""",
eli10="""
**What it's really asking:** "Photocopy a network of friends, where every friend in the copy is a **new person** with the same friendships."

**The danger:** friendships go both ways and form loops (1 is friends with 2, and 2 with 1). A naive copy would go 1 → 2 → 1 → 2… forever, or make two copies of the same person.

**The fix:** keep a **register** (a dict) `old node → its copy`. Before copying someone, check the register: _"Did I already make a copy of this person?"_ If yes, reuse it.
""",
approach="""
```text
copies = {}
clone(node):
    if node in copies: return copies[node]       # already copied
    copy = Node(node.val)
    copies[node] = copy                          # register BEFORE copying neighbours (handles loops)
    copy.neighbors = [clone(n) for n in node.neighbors]
    return copy
```
""",
hints=["Use a dict mapping original node → clone.", "Register the clone before visiting neighbours, so cycles stop."],
starter=r'''def clone_graph(node):
    pass
''',
solution=r'''def clone_graph(node):
    if node is None:
        return None
    copies = {}                                  # original -> clone
    def clone(n):
        if n in copies:
            return copies[n]                     # reuse: handles cycles and shared friends
        c = Node(n.val)
        copies[n] = c                            # register first!
        c.neighbors = [clone(m) for m in n.neighbors]
        return c
    return clone(node)
''',
complexity="**Time O(V + E)**, **Space O(V)**.",
tests=r'''
_sq = [[2, 4], [1, 3], [2, 4], [1, 3]]
T("square structure", lambda: graph_to_adj(clone_graph(build_graph(_sq))), _sq)
C("all nodes are new", lambda: not (graph_node_ids(clone_graph(build_graph(_sq))) & graph_node_ids(build_graph(_sq))))
def _deep():
    g = build_graph(_sq); c = clone_graph(g)
    return not (graph_node_ids(c) & graph_node_ids(g)) and graph_to_adj(c) == _sq
C("deep copy (no shared nodes with input)", _deep)
T("single node", lambda: graph_to_adj(clone_graph(build_graph([[]]))), [[]])
T("empty", lambda: clone_graph(None), None)
''')

P(id="pacific-atlantic", topic="graphs", level="Medium", blind=True, lc=417, title="Pacific Atlantic Water Flow",
statement="""
`heights` is an island's height map. The **Pacific** touches the top and left edges, and the **Atlantic** touches the bottom and right edges. Rain flows from a cell to a neighbour (4 directions) with **equal or lower** height. Return all cells `[r, c]` from which water can reach **both** oceans (any order).
""",
examples="""
```text
heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
→ [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
```
""",
eli10="""
**What it's really asking:** "From which hills can rainwater roll down into both oceans?"

**The clever reversal:** checking every cell by "letting water flow down" repeats lots of work. Instead, **think backwards**: start **from the oceans** and **climb uphill**. Every cell you can climb to from the Pacific shore can drain into the Pacific.
1. Flood "uphill" from all Pacific edge cells. Mark everything reachable.
2. Flood "uphill" from all Atlantic edge cells. Mark everything reachable.
3. The answer is the cells marked by **both** floods.

Uphill means: from a cell you may move to a neighbour that is **higher or equal**.
""",
approach="""
1. `pac`, `atl` = sets of reachable cells.
2. `dfs(r, c, seen)`: add (r, c), then visit each in-bounds neighbour not in `seen` with `heights[n] >= heights[r][c]`.
3. Start a dfs from every top-row and left-column cell (Pacific), and every bottom-row and right-column cell (Atlantic).
4. Return `pac & atl`.
""",
hints=["Reverse the flow: start from each ocean's border and move to higher-or-equal neighbours.", "Do two searches and intersect the results."],
starter=r'''def pacific_atlantic(heights):
    pass
''',
solution=r'''def pacific_atlantic(heights):
    rows, cols = len(heights), len(heights[0])
    pac, atl = set(), set()

    def climb(starts, seen):                  # iterative DFS, uphill from the shore
        stack = list(starts)
        seen.update(starts)
        while stack:
            r, c = stack.pop()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if (0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen
                        and heights[nr][nc] >= heights[r][c]):
                    seen.add((nr, nc))
                    stack.append((nr, nc))

    climb([(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)], pac)
    climb([(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows)], atl)
    return [list(cell) for cell in pac & atl]
''',
complexity="**Time O(R·C)**: each cell is visited at most twice. **Space O(R·C)**.",
tests=r'''
_h = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
T("example", lambda: pacific_atlantic(_h), [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]], same_items)
T("single cell", lambda: pacific_atlantic([[1]]), [[0, 0]], same_items)
T("flat", lambda: pacific_atlantic([[1, 1], [1, 1]]), [[0, 0], [0, 1], [1, 0], [1, 1]], same_items)
''')

P(id="course-schedule", topic="graphs", level="Medium", blind=True, lc=207, title="Course Schedule",
statement="""
There are `n` courses (0…n−1). `prerequisites[i] = [a, b]` means you must take `b` **before** `a`. Return `True` if you can finish all the courses, which is possible only when there's **no cycle** of prerequisites.
""",
examples="""
```text
can_finish(2, [[1, 0]])          → True    (take 0, then 1)
can_finish(2, [[1, 0], [0, 1]])  → False   (each needs the other first: a cycle)
```
""",
eli10="""
**What it's really asking:** "Is there a circular dependency?"

**Real-life picture:** college courses. Maths-2 needs Maths-1. If Maths-1 needed Maths-2, you'd be stuck forever, which is a cycle.

**Kahn's method (peeling the onion):**
1. For each course, count how many prerequisites it still has (its **in-degree**).
2. Courses with **0** remaining prerequisites can be taken **now**. Put them in a queue.
3. "Take" a course: every course that depended on it has one fewer prerequisite. If one drops to 0, it joins the queue.
4. If you managed to take **all n** courses, there's no cycle. If some are left over, they're stuck in a cycle.

This is **topological sort**: an order in which every task comes after its requirements.
""",
approach="""
1. Build `graph[b] = [courses that need b]` and `indeg[a] += 1`.
2. `queue` = all courses with indeg 0.
3. Pop a course, `taken += 1`, and decrement its dependents' in-degrees, enqueuing the ones that reach 0.
4. Return `taken == n`.
""",
hints=["Model courses as a directed graph: b → a.", "Repeatedly take courses with no remaining prerequisites (in-degree 0).", "If you can't take all of them, there's a cycle."],
starter=r'''from collections import deque

def can_finish(n, prerequisites):
    pass
''',
solution=r'''from collections import deque

def can_finish(n, prerequisites):
    graph = [[] for _ in range(n)]
    indeg = [0] * n                           # how many prerequisites each course still needs
    for course, pre in prerequisites:
        graph[pre].append(course)
        indeg[course] += 1
    queue = deque(i for i in range(n) if indeg[i] == 0)
    taken = 0
    while queue:
        c = queue.popleft()
        taken += 1
        for nxt in graph[c]:
            indeg[nxt] -= 1                   # one requirement satisfied
            if indeg[nxt] == 0:
                queue.append(nxt)
    return taken == n                         # leftovers are stuck in a cycle
''',
complexity="**Time O(V + E)**, **Space O(V + E)**.",
mistakes="- Getting the edge direction backwards. It still detects cycles, but be clear about which way the edges point when you explain it.",
tests=r'''
T("possible", lambda: can_finish(2, [[1, 0]]), True)
T("cycle", lambda: can_finish(2, [[1, 0], [0, 1]]), False)
T("no prereqs", lambda: can_finish(3, []), True)
T("long chain", lambda: can_finish(5, [[1, 0], [2, 1], [3, 2], [4, 3]]), True)
T("cycle deep inside", lambda: can_finish(4, [[1, 0], [2, 1], [3, 2], [1, 3]]), False)
''')

P(id="connected-components", topic="graphs", level="Medium", blind=True, lc=323, title="Number of Connected Components in an Undirected Graph",
statement="""
Given `n` nodes (0…n−1) and a list of undirected `edges`, return the number of **connected components** (separate groups).
""",
examples="""
```text
count_components(5, [[0, 1], [1, 2], [3, 4]])          → 2
count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]])  → 1
```
""",
eli10="""
**Real-life picture:** people at a party holding hands. How many separate **circles of friends** are there?

**Union-Find (Disjoint Set Union):** every person starts as their own group's **leader**. Each edge (a handshake) says "these two groups are now one", so make one leader follow the other. Every successful merge reduces the group count by 1. Start with n groups and subtract one per real merge.

Two speed tricks:
- **Path compression:** when you look up someone's leader, make them point directly at the top leader next time.
- **Union by size:** attach the smaller group under the bigger one.

(BFS/DFS from each unvisited node also works, like counting islands.)
""",
approach="""
```text
parent = list(range(n))
find(x): while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]; return x
for a, b in edges:
    ra, rb = find(a), find(b)
    if ra != rb: parent[ra] = rb; groups -= 1
```
""",
hints=["Start with n separate groups.", "Each edge that joins two different groups reduces the count by 1.", "Union-Find makes the 'are they already in the same group?' check fast."],
starter=r'''def count_components(n, edges):
    pass
''',
solution=r'''def count_components(n, edges):
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]     # path compression (halving)
            x = parent[x]
        return x

    groups = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:                          # two different groups join
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra                   # the smaller group goes under the bigger one
            size[ra] += size[rb]
            groups -= 1
    return groups
''',
complexity="**Time O(E · α(n))**, which is practically O(E). **Space O(n)**.",
tests=r'''
T("two groups", lambda: count_components(5, [[0, 1], [1, 2], [3, 4]]), 2)
T("one group", lambda: count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]), 1)
T("no edges", lambda: count_components(4, []), 4)
T("redundant edges", lambda: count_components(3, [[0, 1], [1, 0], [0, 1]]), 2)
''')

P(id="graph-valid-tree", topic="graphs", level="Medium", blind=True, lc=261, title="Graph Valid Tree",
statement="""
Given `n` nodes and undirected `edges`, return `True` if the edges form a valid **tree**: everything is connected, and there are **no cycles**.
""",
examples="""
```text
valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]])          → True
valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]])  → False   (1-2-3 is a cycle)
```
""",
eli10="""
**A tree has two properties at once:** it's **connected** (one piece) and has **no loops**.

**Neat fact:** a tree with n nodes has **exactly n − 1 edges**. More edges than that must create a loop. Fewer means it can't be connected.

So:
1. If `len(edges) != n - 1`, return False.
2. With exactly n−1 edges, it's a tree **if and only if** there's no cycle. Equivalently, if and only if it's connected. Check with Union-Find: if an edge connects two nodes that are **already in the same group**, it closes a loop, so return False.
""",
approach="Check the edge count, then Union-Find: return False on the first edge whose endpoints already share a leader.",
hints=["How many edges does a tree with n nodes have?", "An edge between two already-connected nodes creates a cycle."],
starter=r'''def valid_tree(n, edges):
    pass
''',
solution=r'''def valid_tree(n, edges):
    if len(edges) != n - 1:
        return False                    # a tree must have exactly n - 1 edges
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False                # already connected, so this edge closes a cycle
        parent[ra] = rb
    return True                         # n-1 edges + no cycle = connected tree
''',
complexity="**Time O(n · α(n))**, **Space O(n)**.",
tests=r'''
T("tree", lambda: valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]), True)
T("cycle", lambda: valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]), False)
T("disconnected", lambda: valid_tree(4, [[0, 1], [2, 3]]), False)
T("single node", lambda: valid_tree(1, []), True)
T("n-1 edges but cycle + isolated", lambda: valid_tree(4, [[0, 1], [1, 2], [2, 0]]), False)
''')

P(id="alien-dictionary", topic="graphs", level="Hard", blind=True, lc=269, title="Alien Dictionary",
statement="""
An alien language uses English letters in an unknown order. You get a list of `words` **sorted in the alien order**. Return a string containing every letter that appears, in a valid alien order. If the list is impossible (contradictory), return `""`. When several orders are valid, any one is accepted.
""",
examples="""
```text
alien_order(["wrt", "wrf", "er", "ett", "rftt"])  → "wertf"
alien_order(["z", "x", "z"])                      → ""      (z < x and x < z: contradiction)
alien_order(["abc", "ab"])                        → ""      (a longer word before its own prefix is invalid)
```
""",
eli10="""
**What it's really asking:** "From a sorted dictionary in an unknown alphabet, work out the alphabet."

**How do sorted words reveal letter order?** Compare **neighbouring words** and find the **first position where they differ**. In "wrt" vs "wrf", the first difference is t vs f, so **t comes before f**. That's one rule. (The letters after the first difference tell us nothing.)

Collect all such rules (t→f, w→e, r→t, e→r), and the problem becomes **Course Schedule**: find an order where every letter comes after the letters that must precede it, a **topological sort**. If there's a cycle (z before x before z), it's impossible.

**Sneaky invalid case:** "abc" listed before "ab". A word must come after its own prefix, so this input is invalid.
""",
approach="""
1. Make a node for **every letter** that appears (even letters with no rules).
2. For each neighbouring pair (w1, w2): find the first differing index and add the edge `w1[i] → w2[i]`. If there's no difference and `len(w1) > len(w2)`, return "".
3. Run Kahn's topological sort on the letters. If the output contains every letter, return it; otherwise there's a cycle, so return "".
""",
hints=["Compare adjacent words only.", "The first differing character gives one ordering rule.", "Topologically sort the letters (like Course Schedule); a cycle means invalid."],
starter=r'''from collections import deque

def alien_order(words):
    pass
''',
solution=r'''from collections import deque

def alien_order(words):
    graph = {ch: set() for w in words for ch in w}   # every letter is a node
    indeg = {ch: 0 for ch in graph}
    for w1, w2 in zip(words, words[1:]):
        for a, b in zip(w1, w2):
            if a != b:                                # first difference: a comes before b
                if b not in graph[a]:
                    graph[a].add(b)
                    indeg[b] += 1
                break
        else:                                         # no difference found in the overlap
            if len(w1) > len(w2):
                return ""                             # "abc" before "ab" is impossible
    queue = deque(ch for ch in graph if indeg[ch] == 0)
    order = []
    while queue:
        ch = queue.popleft()
        order.append(ch)
        for nxt in graph[ch]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return "".join(order) if len(order) == len(graph) else ""   # leftovers = cycle
''',
complexity="**Time O(total characters)**. **Space O(1)**: at most 26 letters and 26² edges.",
mistakes="- Comparing every pair of words instead of adjacent ones (only adjacent pairs are needed).\n- Forgetting letters that never appear in a rule.\n- Missing the prefix case.",
tests=r'''
def _valid(words):
    def check(got, _):
        letters = {c for w in words for c in w}
        if sorted(got) != sorted(letters): return False
        rank = {c: i for i, c in enumerate(got)}
        key = lambda w: [rank[c] for c in w]
        return all(key(a) <= key(b) for a, b in zip(words, words[1:]))
    return check
_w1 = ["wrt", "wrf", "er", "ett", "rftt"]
T("example", lambda: alien_order(_w1), "wertf", _valid(_w1))
T("contradiction", lambda: alien_order(["z", "x", "z"]), "")
T("prefix trap", lambda: alien_order(["abc", "ab"]), "")
_w2 = ["z", "x"]
T("two letters", lambda: alien_order(_w2), "zx", _valid(_w2))
_w3 = ["ab", "adc"]
T("letters without rules included", lambda: alien_order(_w3), "abdc", _valid(_w3))
''')
