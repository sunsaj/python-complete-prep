from lib import P

# ============================================================ LINKED LIST
P(id="ll-count", topic="linked-list", level="Warm-up", title="Count and Sum a Linked List",
statement="""
A **linked list** is a chain of `ListNode`s. Each node has a `.val` and a `.next`, which points to the next node (`None` at the end). Given the `head`, return `(count, total)`: the number of nodes and the sum of their values.

The helpers `ListNode`, `to_ll([...])` and `from_ll(head)` are already available.
""",
examples="""
```text
count_and_sum(to_ll([3, 1, 4]))  → (3, 8)
count_and_sum(None)              → (0, 0)    (an empty list)
```
""",
eli10="""
A linked list is a **treasure hunt**. You hold the first clue (the head). Each clue has a value written on it and tells you where the next clue is. To visit everything, you keep following "next" until there's no next clue (`None`).

Unlike a Python list, you **can't jump to position 5**. You have to walk there one clue at a time.
""",
approach="""
```python
node = head
while node is not None:
    ...use node.val...
    node = node.next      # follow the arrow
```
This walking loop is the base of every linked list problem.
""",
hints=["Use a variable `node` that starts at head and moves to node.next each step."],
starter=r'''def count_and_sum(head):
    pass
''',
solution=r'''def count_and_sum(head):
    count = total = 0
    node = head
    while node is not None:
        count += 1
        total += node.val
        node = node.next          # move to the next clue
    return (count, total)
''',
complexity="**Time O(n)**, **Space O(1)**.",
tests=r'''
T("three nodes", lambda: count_and_sum(to_ll([3, 1, 4])), (3, 8))
T("empty", lambda: count_and_sum(None), (0, 0))
T("one node", lambda: count_and_sum(to_ll([-5])), (1, -5))
''')

P(id="reverse-linked-list", topic="linked-list", level="Easy", blind=True, lc=206, title="Reverse Linked List",
statement="""
Reverse a singly linked list and return the **new head**.
""",
examples="""
```text
1 -> 2 -> 3 -> 4 -> 5   becomes   5 -> 4 -> 3 -> 2 -> 1
from_ll(reverse_list(to_ll([1, 2, 3, 4, 5])))  → [5, 4, 3, 2, 1]
```
""",
eli10="""
**What it's really asking:** "Make every arrow point backwards."

**Real-life picture:** kids stand in a line, each pointing at the kid **in front** of them. You walk down the line and tell each kid: _"Turn around and point at the kid **behind** you instead."_ The danger: once a kid turns around, you lose track of who was in front. So **before** turning them, remember the next kid.

You need three hands:
- `prev`: the kid behind (the new direction to point at),
- `curr`: the kid you're turning now,
- `nxt`: the kid in front (saved before turning, so you don't lose the rest of the line).
""",
approach="""
```text
prev = None, curr = head
repeat while curr:
    nxt = curr.next      # 1. remember the rest of the line
    curr.next = prev     # 2. turn the arrow around
    prev = curr          # 3. step forward: prev moves up
    curr = nxt           #    and curr moves up
return prev              # the old tail is the new head
```

### Walk-through on 1 → 2 → 3
| step | prev | curr | what changes |
|---|---|---|---|
| start | None | 1 | |
| 1 | 1 | 2 | 1 now points to None |
| 2 | 2 | 3 | 2 now points to 1 |
| 3 | 3 | None | 3 now points to 2 → done, the head is 3 |
""",
hints=["You need to remember the next node before changing curr.next.", "Use three variables: prev, curr, nxt.", "At the end, prev is the new head."],
starter=r'''def reverse_list(head):
    pass
''',
solution=r'''def reverse_list(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next       # save the rest of the list
        curr.next = prev      # flip the arrow
        prev, curr = curr, nxt
    return prev               # the old last node is the new head
''',
complexity="**Time O(n)**, **Space O(1)**. (The recursive version is O(n) space because of the call stack.)",
mistakes="- Writing `curr.next = prev` before saving `curr.next`. You lose the rest of the list.\n- Returning `head`, which is now the **last** node.",
tests=r'''
T("five nodes", lambda: from_ll(reverse_list(to_ll([1, 2, 3, 4, 5]))), [5, 4, 3, 2, 1])
T("two nodes", lambda: from_ll(reverse_list(to_ll([1, 2]))), [2, 1])
T("empty", lambda: from_ll(reverse_list(None)), [])
T("long", lambda: from_ll(reverse_list(to_ll(range(5000)))), list(range(4999, -1, -1)))
''')

P(id="merge-two-lists", topic="linked-list", level="Easy", blind=True, lc=21, title="Merge Two Sorted Lists",
statement="""
Merge two **sorted** linked lists into one sorted list (by re-linking the nodes) and return its head.
""",
examples="""
```text
merge_two_lists(to_ll([1, 2, 4]), to_ll([1, 3, 4]))  → 1 -> 1 -> 2 -> 3 -> 4 -> 4
```
""",
eli10="""
**Real-life picture:** two queues of students, each already sorted by height. You form one new sorted queue. At each step, look at the **front** student of both queues, and send the **shorter** one to the new queue. When one queue is empty, the whole other queue just joins at the end (it's already sorted).

**The "dummy node" trick:** starting the new queue is awkward (who is first?). So put a **fake student** at the front (a dummy). Build after it, and at the end return `dummy.next`. This removes all the special cases.
""",
approach="""
1. `dummy = tail = ListNode()`.
2. While both lists have nodes: attach the smaller front node to `tail.next`, advance that list, and advance `tail`.
3. Attach whichever list remains: `tail.next = l1 or l2`.
4. Return `dummy.next`.
""",
hints=["Compare the two front nodes and take the smaller one.", "A dummy starting node avoids special-casing the head.", "When one list runs out, attach the rest of the other."],
starter=r'''def merge_two_lists(l1, l2):
    pass
''',
solution=r'''def merge_two_lists(l1, l2):
    dummy = tail = ListNode()          # fake head: we return dummy.next
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 or l2               # the leftover is already sorted
    return dummy.next
''',
complexity="**Time O(n + m)**, **Space O(1)**: we only re-link existing nodes.",
tests=r'''
T("example", lambda: from_ll(merge_two_lists(to_ll([1, 2, 4]), to_ll([1, 3, 4]))), [1, 1, 2, 3, 4, 4])
T("both empty", lambda: from_ll(merge_two_lists(None, None)), [])
T("one empty", lambda: from_ll(merge_two_lists(None, to_ll([0]))), [0])
T("disjoint", lambda: from_ll(merge_two_lists(to_ll([5, 6]), to_ll([1, 2]))), [1, 2, 5, 6])
''')

P(id="linked-list-cycle", topic="linked-list", level="Easy", blind=True, lc=141, title="Linked List Cycle",
statement="""
Return `True` if the linked list has a **cycle** (some node's `next` points back to an earlier node), else `False`. Try for O(1) memory.
""",
examples="""
```text
3 -> 2 -> 0 -> -4 --+
     ^--------------+     → True
1 -> 2 -> None           → False
```
""",
eli10="""
**Real-life picture:** two runners on a track: a **tortoise** (1 step at a time) and a **hare** (2 steps at a time).
- If the track is a straight road with an end, the hare reaches the end and we know there's no loop.
- If the track is a **circular loop**, the hare keeps lapping around and eventually **catches up with the tortoise** from behind.

So: move slow by 1 and fast by 2. If they ever land on the same node, there's a cycle. This is **Floyd's cycle detection** ("tortoise and hare").

Easy alternative: keep a set of visited nodes. If you see one again, it's a cycle. That uses O(n) memory.
""",
approach="""
```text
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast: return True
return False
```
Why must they meet? Inside the loop, the gap between them shrinks by 1 every step, so it must reach 0.
""",
hints=["Two pointers at different speeds.", "If the fast pointer reaches None, there's no cycle.", "Compare nodes with `is`, not by value."],
starter=r'''def has_cycle(head):
    pass
''',
solution=r'''def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next             # 1 step
        fast = fast.next.next        # 2 steps
        if slow is fast:             # the hare lapped the tortoise
            return True
    return False                     # the hare reached the end of the road
''',
complexity="**Time O(n)**, **Space O(1)**.",
mistakes="- Comparing `slow.val == fast.val`. Different nodes can hold equal values, so compare the node objects with `is`.",
tests=r'''
def _cyc(vals, pos):
    head = to_ll(vals)
    if pos >= 0:
        tail = head; target = head
        for _ in range(pos): target = target.next
        while tail.next: tail = tail.next
        tail.next = target
    return head
T("cycle", lambda: has_cycle(_cyc([3, 2, 0, -4], 1)), True)
T("two-node cycle", lambda: has_cycle(_cyc([1, 2], 0)), True)
T("no cycle", lambda: has_cycle(_cyc([1, 2, 3], -1)), False)
T("empty", lambda: has_cycle(None), False)
T("equal values, no cycle", lambda: has_cycle(to_ll([1, 1, 1, 1])), False)
''')

P(id="remove-nth-from-end", topic="linked-list", level="Medium", blind=True, lc=19, title="Remove Nth Node From End of List",
statement="""
Remove the **n-th node from the end** of the list (n=1 means the last node) and return the head. Try to do it in **one pass**.
""",
examples="""
```text
remove_nth_from_end(to_ll([1, 2, 3, 4, 5]), 2)  → 1 -> 2 -> 3 -> 5
remove_nth_from_end(to_ll([1]), 1)              → empty
```
""",
eli10="""
**Real-life picture:** two people walk down a corridor holding a **rope of length n** between them. The front person starts n steps ahead. They walk together at the same speed. When the **front person hits the wall** (the end), the back person is **exactly n steps from the end**, standing just before the node to delete.

A **dummy** node before the head handles the case where we must delete the head itself.
""",
approach="""
1. `dummy.next = head`, `fast = slow = dummy`.
2. Move `fast` **n + 1** steps ahead (so `slow` stops one node **before** the target).
3. Move both until `fast` is None.
4. `slow.next = slow.next.next` (skip the target).
5. Return `dummy.next`.
""",
hints=["Use two pointers with a gap of n between them.", "A dummy node handles removing the first node.", "Stop slow one node before the node to remove."],
starter=r'''def remove_nth_from_end(head, n):
    pass
''',
solution=r'''def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next               # open a gap of n + 1
    while fast:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next         # skip the n-th node from the end
    return dummy.next
''',
complexity="**Time O(length)**, one pass. **Space O(1)**.",
tests=r'''
T("example", lambda: from_ll(remove_nth_from_end(to_ll([1, 2, 3, 4, 5]), 2)), [1, 2, 3, 5])
T("only node", lambda: from_ll(remove_nth_from_end(to_ll([1]), 1)), [])
T("remove head", lambda: from_ll(remove_nth_from_end(to_ll([1, 2]), 2)), [2])
T("remove tail", lambda: from_ll(remove_nth_from_end(to_ll([1, 2]), 1)), [1])
''')

P(id="reorder-list", topic="linked-list", level="Medium", blind=True, lc=143, title="Reorder List",
statement="""
Reorder `L0 → L1 → … → Ln` into `L0 → Ln → L1 → Ln-1 → L2 → …` **in place** (change the links, return nothing).
""",
examples="""
```text
1 -> 2 -> 3 -> 4        becomes  1 -> 4 -> 2 -> 3
1 -> 2 -> 3 -> 4 -> 5   becomes  1 -> 5 -> 2 -> 4 -> 3
```
""",
eli10="""
**What it's really asking:** "Alternate between taking from the front and the back."

**Real-life picture:** a deck of cards numbered 1 to 5. Cut it in **half**: [1 2 3] and [4 5]. Turn the second half **upside down**: [5 4]. Now **shuffle them together**, one from each pile: 1, 5, 2, 4, 3.

That's three problems you already know:
1. **Find the middle** (slow/fast pointers, like the cycle problem).
2. **Reverse** the second half (Reverse Linked List).
3. **Merge alternately** (like Merge Two Lists, but alternating).
""",
approach="""
1. Middle: `slow, fast = head, head.next`, and while `fast and fast.next`: slow +1, fast +2. `slow` ends at the end of the first half.
2. `second = slow.next`, `slow.next = None` (cut), then reverse `second`.
3. Weave: `first, second = head, reversed`. While `second`: save both nexts, link `first → second → first's old next`, and advance.
""",
hints=["Break it into: find the middle, reverse the second half, merge alternately.", "Don't forget to cut the list in the middle (set next to None)."],
starter=r'''def reorder_list(head):
    # modify the list in place; return nothing
    pass
''',
solution=r'''def reorder_list(head):
    if not head or not head.next:
        return
    slow, fast = head, head.next          # 1. find the middle
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None                      # cut into two halves
    prev = None                           # 2. reverse the second half
    while second:
        second.next, prev, second = prev, second, second.next
    first, second = head, prev            # 3. weave them together
    while second:
        f_next, s_next = first.next, second.next
        first.next = second
        second.next = f_next
        first, second = f_next, s_next
''',
complexity="**Time O(n)**, **Space O(1)**.",
mistakes="- Forgetting to cut the first half (`slow.next = None`), which creates a cycle.",
tests=r'''
def _ro(vals):
    h = to_ll(vals); reorder_list(h); return from_ll(h, 100)
T("even", lambda: _ro([1, 2, 3, 4]), [1, 4, 2, 3])
T("odd", lambda: _ro([1, 2, 3, 4, 5]), [1, 5, 2, 4, 3])
T("one", lambda: _ro([1]), [1])
T("two", lambda: _ro([1, 2]), [1, 2])
''')

P(id="merge-k-lists", topic="linked-list", level="Hard", blind=True, lc=23, title="Merge K Sorted Lists",
statement="""
Given a list of `k` sorted linked lists, merge them into one sorted linked list and return its head.
""",
examples="""
```text
merge_k_lists([to_ll([1, 4, 5]), to_ll([1, 3, 4]), to_ll([2, 6])])  → 1 1 2 3 4 4 5 6
merge_k_lists([])  → empty
```
""",
eli10="""
**Real-life picture:** k sorted queues of students at k doors, and you need one sorted queue. At each step you want **the shortest student among all the k fronts**. Looking at all k fronts every time is slow (k checks per student).

Use a **min-heap** (a "magic box" that always gives you the smallest item fast, in O(log k)). Put the front student of each queue in the box. Take out the smallest, add it to the result, and put **that queue's next student** into the box. Repeat until the box is empty.

(Divide and conquer also works: merge the lists in pairs, like a tournament, using Merge Two Lists. That's also O(N log k).)
""",
approach="""
1. Push `(node.val, i, node)` for each non-empty list. The index `i` breaks ties, because Python can't compare two ListNodes.
2. `dummy = tail = ListNode()`.
3. While the heap isn't empty: pop the smallest `(val, i, node)`, attach it, and if `node.next` exists, push `(node.next.val, i, node.next)`.
4. Return `dummy.next`.
""",
hints=["You need the smallest of k front nodes repeatedly. Which data structure does that fast?", "Python's heapq is a min-heap. Store (value, tie_breaker, node)."],
starter=r'''import heapq

def merge_k_lists(lists):
    pass
''',
solution=r'''import heapq

def merge_k_lists(lists):
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)                         # the k front nodes
    dummy = tail = ListNode()
    while heap:
        val, i, node = heapq.heappop(heap)      # the smallest front of all lists
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))   # replace it with its successor
    return dummy.next
''',
complexity="**Time O(N log k)**: N total nodes, each push/pop is log k. **Space O(k)** for the heap.",
mistakes="- Pushing `(val, node)` without a tie-breaker → `TypeError: '<' not supported between ListNode` when values are equal.\n- Collecting all values, sorting, and rebuilding is O(N log N). It works, but it's not what interviewers want.",
tests=r'''
T("example", lambda: from_ll(merge_k_lists([to_ll([1, 4, 5]), to_ll([1, 3, 4]), to_ll([2, 6])])), [1, 1, 2, 3, 4, 4, 5, 6])
T("no lists", lambda: from_ll(merge_k_lists([])), [])
T("empty lists", lambda: from_ll(merge_k_lists([None, None])), [])
T("many equal values", lambda: from_ll(merge_k_lists([to_ll([1, 1]), to_ll([1]), to_ll([1, 1])])), [1, 1, 1, 1, 1])
''')

# ============================================================ TREES
P(id="tree-sum", topic="trees", level="Warm-up", title="Sum and Count the Nodes of a Tree",
statement="""
A binary tree node (`TreeNode`) has `.val`, `.left` and `.right`. Return the **sum of all values** in the tree. (The helper `to_tree([...])` builds a tree from a level-order list.)
""",
examples="""
```text
        5
       / \\
      3   8       tree_sum(to_tree([5, 3, 8, 1])) → 17
     /
    1
```
""",
eli10="""
A tree is like a **family tree** or folders inside folders. The magic tool for trees is **recursion**: a function that calls itself on smaller pieces.

To sum a tree, ask: _"What's the sum of my tree?"_ It's **my value + the sum of my left subtree + the sum of my right subtree**. Each subtree is just a smaller tree, so the same function handles it. An empty tree (`None`) has sum 0. That's the **base case** that stops the recursion.

Almost every tree problem follows this shape:
```python
def solve(node):
    if node is None: return <answer for empty>
    left = solve(node.left)
    right = solve(node.right)
    return <combine node.val, left, right>
```
""",
approach="`return 0 if not node else node.val + tree_sum(node.left) + tree_sum(node.right)`",
hints=["Base case: an empty tree has sum 0.", "Sum = value + sum(left) + sum(right)."],
starter=r'''def tree_sum(root):
    pass
''',
solution=r'''def tree_sum(root):
    if root is None:
        return 0                                   # empty tree
    return root.val + tree_sum(root.left) + tree_sum(root.right)
''',
complexity="**Time O(n)**. **Space O(h)** for the recursion, where h is the tree height.",
tests=r'''
T("example", lambda: tree_sum(to_tree([5, 3, 8, 1])), 17)
T("empty", lambda: tree_sum(None), 0)
T("negatives", lambda: tree_sum(to_tree([-1, -2, None, -3])), -6)
''')

P(id="invert-tree", topic="trees", level="Easy", blind=True, lc=226, title="Invert Binary Tree",
statement="""
Mirror the tree: swap the left and right children of **every** node. Return the root.
""",
examples="""
```text
     4                4
   /   \\            /   \\
  2     7    →     7     2
 / \\   / \\        / \\   / \\
1   3 6   9      9   6 3   1
```
""",
eli10="""
**Real-life picture:** hold a family-tree poster up to a **mirror**. Everything on the left appears on the right.

With recursion: _"To mirror my tree: swap my two children, then mirror each child's tree."_ An empty tree is already mirrored.
""",
approach="""
```text
invert(node):
    if node is None: return None
    node.left, node.right = invert(node.right), invert(node.left)
    return node
```
You can also do it with a queue (BFS), swapping the children of each node you visit.
""",
hints=["At each node, swap left and right.", "Do the same for both subtrees (recursion)."],
starter=r'''def invert_tree(root):
    pass
''',
solution=r'''def invert_tree(root):
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)   # swap the mirrored subtrees
    return root
''',
complexity="**Time O(n)**, **Space O(h)**.",
tests=r'''
T("example", lambda: from_tree(invert_tree(to_tree([4, 2, 7, 1, 3, 6, 9]))), [4, 7, 2, 9, 6, 3, 1])
T("small", lambda: from_tree(invert_tree(to_tree([2, 1, 3]))), [2, 3, 1])
T("empty", lambda: from_tree(invert_tree(None)), [])
T("one-sided", lambda: from_tree(invert_tree(to_tree([1, 2]))), [1, None, 2])
''')

P(id="max-depth", topic="trees", level="Easy", blind=True, lc=104, title="Maximum Depth of Binary Tree",
statement="""
Return the tree's **maximum depth**: the number of nodes on the longest path from the root down to a leaf.
""",
examples="""
```text
max_depth(to_tree([3, 9, 20, None, None, 15, 7]))  → 3
max_depth(None)                                    → 0
```
""",
eli10="""
**Real-life picture:** how many generations does a family tree have? A person's tree is **1 (themselves) + the deeper of their children's trees**.

`depth(node) = 1 + max(depth(left), depth(right))`, and the depth of nothing is 0.
""",
approach="Recursion: `return 0 if not node else 1 + max(max_depth(node.left), max_depth(node.right))`. The BFS alternative counts levels with a queue.",
hints=["Depth of an empty tree = 0.", "Depth = 1 + max(depth of left, depth of right)."],
starter=r'''def max_depth(root):
    pass
''',
solution=r'''def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
''',
complexity="**Time O(n)**, **Space O(h)**.",
tests=r'''
T("example", lambda: max_depth(to_tree([3, 9, 20, None, None, 15, 7])), 3)
T("empty", lambda: max_depth(None), 0)
T("chain", lambda: max_depth(to_tree([1, None, 2])), 2)
''')

P(id="same-tree", topic="trees", level="Easy", blind=True, lc=100, title="Same Tree",
statement="""
Return `True` if two binary trees are **identical**: the same shape and the same values.
""",
examples="""
```text
is_same_tree(to_tree([1, 2, 3]), to_tree([1, 2, 3]))   → True
is_same_tree(to_tree([1, 2]), to_tree([1, None, 2]))   → False
```
""",
eli10="""
**Real-life picture:** two people compare their family trees branch by branch. Two trees are the same if **the roots match**, the **left family trees match**, and the **right family trees match**.

Base cases: both empty → same. Exactly one empty, or different values → not the same.
""",
approach="""
```text
same(p, q):
    if not p and not q: return True
    if not p or not q or p.val != q.val: return False
    return same(p.left, q.left) and same(p.right, q.right)
```
""",
hints=["Handle the 'both None' and 'one None' cases first.", "Then compare values and recurse on both sides."],
starter=r'''def is_same_tree(p, q):
    pass
''',
solution=r'''def is_same_tree(p, q):
    if p is None and q is None:
        return True                  # both empty
    if p is None or q is None or p.val != q.val:
        return False                 # shape or value differs
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
''',
complexity="**Time O(n)**, **Space O(h)**.",
tests=r'''
T("same", lambda: is_same_tree(to_tree([1, 2, 3]), to_tree([1, 2, 3])), True)
T("different shape", lambda: is_same_tree(to_tree([1, 2]), to_tree([1, None, 2])), False)
T("different values", lambda: is_same_tree(to_tree([1, 2, 1]), to_tree([1, 1, 2])), False)
T("both empty", lambda: is_same_tree(None, None), True)
''')

P(id="subtree", topic="trees", level="Easy", blind=True, lc=572, title="Subtree of Another Tree",
statement="""
Return `True` if `sub` appears **inside** `root` as a subtree: some node of `root` together with **all** of its descendants must equal `sub` exactly.
""",
examples="""
```text
root = [3, 4, 5, 1, 2], sub = [4, 1, 2]                      → True
root = [3, 4, 5, 1, 2, None, None, None, None, 0], sub = [4, 1, 2]  → False  (the 4 there has an extra child 0)
```
""",
eli10="""
**Real-life picture:** "Is this small family tree (sub) a complete branch somewhere in the big family tree?"

Walk to **every node** of the big tree and ask: _"Starting here, is the tree exactly the same as `sub`?"_ You already wrote that check: it's **Same Tree**! So this problem is "Same Tree, tried at every node".
""",
approach="""
```text
is_subtree(root, sub):
    if root is None: return False        (ran out of places to try)
    if is_same(root, sub): return True
    return is_subtree(root.left, sub) or is_subtree(root.right, sub)
```
""",
hints=["Reuse the Same Tree function.", "Try every node of root as the starting point."],
starter=r'''def is_subtree(root, sub):
    pass
''',
solution=r'''def is_subtree(root, sub):
    def same(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return same(a.left, b.left) and same(a.right, b.right)

    if root is None:
        return sub is None
    if same(root, sub):
        return True                       # a match starting here
    return is_subtree(root.left, sub) or is_subtree(root.right, sub)
''',
complexity="**Time O(n · m)** in the worst case (n nodes, m nodes in sub). **Space O(h)**. (A hashing or serialization trick gives O(n + m).)",
tests=r'''
T("yes", lambda: is_subtree(to_tree([3, 4, 5, 1, 2]), to_tree([4, 1, 2])), True)
T("extra child", lambda: is_subtree(to_tree([3, 4, 5, 1, 2, None, None, None, None, 0]), to_tree([4, 1, 2])), False)
T("whole tree", lambda: is_subtree(to_tree([1, 2]), to_tree([1, 2])), True)
T("leaf", lambda: is_subtree(to_tree([1, 2, 3]), to_tree([3])), True)
''')

P(id="lca-bst", topic="trees", level="Medium", blind=True, lc=235, title="Lowest Common Ancestor of a BST",
statement="""
In a **Binary Search Tree** (every left descendant < node < every right descendant), find the **lowest common ancestor** of nodes with values `p` and `q`: the deepest node that has both in its subtree (a node counts as its own descendant). Return that node's **value**.
""",
examples="""
```text
        6
      /   \\
     2     8
    / \\   / \\
   0   4 7   9
      / \\
     3   5
lca_bst(root, 2, 8) → 6     lca_bst(root, 2, 4) → 2     lca_bst(root, 3, 5) → 4
```
""",
eli10="""
**What's a BST?** A tree where **smaller values go left, bigger go right**, everywhere. Like a sorted list arranged as a tree.

**What it's really asking:** "Where do the paths to p and q split apart?"

**Real-life picture:** you're giving directions from the root. At each node:
- If **both** p and q are **smaller**, they're both in the left subtree, so go left.
- If **both** are **bigger**, go right.
- Otherwise they're on **different sides** (or one of them is this node). This node is where the paths split, so it's the answer!
""",
approach="""
```text
node = root
while node:
    if p < node.val and q < node.val: node = node.left
    elif p > node.val and q > node.val: node = node.right
    else: return node.val
```
No recursion is needed. Each step goes one level down: O(h).
""",
hints=["Use the BST ordering: compare p and q with the current node.", "If both are on the same side, go that way; otherwise you've found the split point."],
starter=r'''def lca_bst(root, p, q):
    # p and q are values; return the value of the LCA node
    pass
''',
solution=r'''def lca_bst(root, p, q):
    node = root
    while node:
        if p < node.val and q < node.val:
            node = node.left           # both are in the left subtree
        elif p > node.val and q > node.val:
            node = node.right          # both are in the right subtree
        else:
            return node.val            # they split here (or one of them IS this node)
''',
complexity="**Time O(h)**: O(log n) if balanced. **Space O(1)**.",
tests=r'''
_t = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
T("split at root", lambda: lca_bst(to_tree(_t), 2, 8), 6)
T("ancestor is p", lambda: lca_bst(to_tree(_t), 2, 4), 2)
T("deep", lambda: lca_bst(to_tree(_t), 3, 5), 4)
T("two nodes", lambda: lca_bst(to_tree([2, 1]), 2, 1), 2)
''')

P(id="level-order", topic="trees", level="Medium", blind=True, lc=102, title="Binary Tree Level Order Traversal",
statement="""
Return the node values **level by level**, left to right, as a list of lists.
""",
examples="""
```text
level_order(to_tree([3, 9, 20, None, None, 15, 7]))  → [[3], [9, 20], [15, 7]]
```
""",
eli10="""
**Real-life picture:** a family photo taken **generation by generation**: grandparents first, then parents, then kids.

Use a **queue** (first in, first out, like a ticket counter line). Start with the root in the queue. For each level: count how many people are in the queue right now (that's the whole current generation). Take them out one by one, write down their values, and add **their children** to the back of the queue. This is **BFS (Breadth-First Search)**.
""",
approach="""
```text
queue = deque([root])
while queue:
    level = []
    for _ in range(len(queue)):        # exactly the nodes of this level
        node = queue.popleft()
        level.append(node.val)
        add node.left / node.right if they exist
    result.append(level)
```
""",
hints=["Use a queue (collections.deque).", "Process exactly len(queue) nodes per level."],
starter=r'''from collections import deque

def level_order(root):
    pass
''',
solution=r'''from collections import deque

def level_order(root):
    if root is None:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):           # only the nodes already waiting = this level
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
''',
complexity="**Time O(n)**. **Space O(w)**, where w is the maximum width of a level.",
mistakes="- Using `list.pop(0)` as the queue, which is O(n) per pop. Use `deque.popleft()`.",
tests=r'''
T("example", lambda: level_order(to_tree([3, 9, 20, None, None, 15, 7])), [[3], [9, 20], [15, 7]])
T("one node", lambda: level_order(to_tree([1])), [[1]])
T("empty", lambda: level_order(None), [])
T("left chain", lambda: level_order(to_tree([1, 2, None, 3])), [[1], [2], [3]])
''')

P(id="validate-bst", topic="trees", level="Medium", blind=True, lc=98, title="Validate Binary Search Tree",
statement="""
Return `True` if the tree is a valid BST: for **every** node, all values in its left subtree are **strictly smaller** and all values in its right subtree are **strictly larger**.
""",
examples="""
```text
is_valid_bst(to_tree([2, 1, 3]))                    → True
is_valid_bst(to_tree([5, 1, 4, None, None, 3, 6]))  → False   (4 is in 5's right subtree but 4 < 5)
is_valid_bst(to_tree([5, 4, 6, None, None, 3, 7]))  → False   (3 is in 5's right subtree)
```
""",
eli10="""
**The trap:** checking only "left child < node < right child" is **not enough**. A node deep in the right subtree must still be bigger than the root, as in the third example.

**Real-life picture:** each node is given an **allowed range** of values by its ancestors. The root may be anything: (−∞, +∞). Going **left** means "you must be smaller than me", so the upper limit becomes my value. Going **right** means "you must be bigger than me", so the lower limit becomes my value. Every node must fit inside its range.
""",
approach="""
```text
valid(node, low, high):
    if node is None: return True
    if not (low < node.val < high): return False
    return valid(node.left, low, node.val) and valid(node.right, node.val, high)
start: valid(root, -inf, +inf)
```
Alternative: an **in-order traversal** (left, node, right) of a BST gives a strictly increasing sequence, so check that.
""",
hints=["Comparing only with the direct children is not enough.", "Pass down an allowed (low, high) range for each node."],
starter=r'''def is_valid_bst(root):
    pass
''',
solution=r'''def is_valid_bst(root):
    def valid(node, low, high):
        if node is None:
            return True
        if not (low < node.val < high):
            return False                        # outside the range the ancestors allow
        return valid(node.left, low, node.val) and valid(node.right, node.val, high)
    return valid(root, float("-inf"), float("inf"))
''',
complexity="**Time O(n)**, **Space O(h)**.",
tests=r'''
T("valid", lambda: is_valid_bst(to_tree([2, 1, 3])), True)
T("child violation", lambda: is_valid_bst(to_tree([5, 1, 4, None, None, 3, 6])), False)
T("deep violation", lambda: is_valid_bst(to_tree([5, 4, 6, None, None, 3, 7])), False)
T("duplicates invalid", lambda: is_valid_bst(to_tree([2, 2, 2])), False)
T("single", lambda: is_valid_bst(to_tree([1])), True)
''')

P(id="kth-smallest-bst", topic="trees", level="Medium", blind=True, lc=230, title="Kth Smallest Element in a BST",
statement="""
Return the **k-th smallest** value (1-indexed) in a BST.
""",
examples="""
```text
kth_smallest(to_tree([3, 1, 4, None, 2]), 1)            → 1
kth_smallest(to_tree([5, 3, 6, 2, 4, None, None, 1]), 3) → 3
```
""",
eli10="""
**Key fact:** visiting a BST **in-order** (left subtree, then the node, then the right subtree) gives the values **in sorted order**. It's like reading a sorted list that has been folded into a tree.

So just walk in-order and **stop at the k-th node** you visit. Use a stack to walk iteratively: keep going left as far as possible (stacking the nodes), pop one (that's the next smallest), then go to its right child.
""",
approach="""
```text
stack, node = [], root
while True:
    while node: stack.append(node); node = node.left      # go as far left as possible
    node = stack.pop()                                     # the next smallest
    k -= 1
    if k == 0: return node.val
    node = node.right
```
""",
hints=["In-order traversal of a BST visits values in sorted order.", "Count nodes as you visit them and stop at k."],
starter=r'''def kth_smallest(root, k):
    pass
''',
solution=r'''def kth_smallest(root, k):
    stack, node = [], root
    while True:
        while node:                 # dive left: smaller values first
            stack.append(node)
            node = node.left
        node = stack.pop()          # the next value in sorted order
        k -= 1
        if k == 0:
            return node.val
        node = node.right           # then the bigger values of this subtree
''',
complexity="**Time O(h + k)**, **Space O(h)**.",
tests=r'''
T("k = 1", lambda: kth_smallest(to_tree([3, 1, 4, None, 2]), 1), 1)
T("k = 3", lambda: kth_smallest(to_tree([5, 3, 6, 2, 4, None, None, 1]), 3), 3)
T("largest", lambda: kth_smallest(to_tree([2, 1, 3]), 3), 3)
''')

P(id="build-tree-pre-in", topic="trees", level="Medium", blind=True, lc=105, title="Construct Binary Tree from Preorder and Inorder",
statement="""
Given the `preorder` (node, left, right) and `inorder` (left, node, right) traversals of a tree with **unique** values, rebuild the tree and return its root.
""",
examples="""
```text
preorder = [3, 9, 20, 15, 7], inorder = [9, 3, 15, 20, 7]
→ tree [3, 9, 20, None, None, 15, 7]
```
""",
eli10="""
**Two clues:**
- **Preorder** always lists the **root first**. So `preorder[0] = 3` is the root.
- **Inorder** lists **everything left of the root, then the root, then everything right**. Find 3 in inorder: `[9] 3 [15, 20, 7]`. Now you know the **left subtree has 1 node** (9) and the **right subtree has 3 nodes**.

Then repeat the same trick on each side with the matching slices. It's like a detective puzzle: the preorder says "who is the boss", and the inorder says "who sits on the boss's left or right".
""",
approach="""
1. Build `index = {value: position in inorder}` for O(1) lookups.
2. Keep a pointer `pre_i` into preorder (the next root to use).
3. `build(lo, hi)` builds the subtree whose inorder range is `[lo, hi]`:
   - If `lo > hi`, return None.
   - `root_val = preorder[pre_i]`, then `pre_i += 1`.
   - `mid = index[root_val]`.
   - `root.left = build(lo, mid - 1)`, then `root.right = build(mid + 1, hi)`. **Left first**, because preorder lists the left subtree before the right.
""",
hints=["preorder[0] is always the root.", "The root's position in inorder splits the left and right subtrees.", "Use a dict for value → inorder index, and consume preorder left to right."],
starter=r'''def build_tree(preorder, inorder):
    pass
''',
solution=r'''def build_tree(preorder, inorder):
    index = {v: i for i, v in enumerate(inorder)}
    pre_i = 0

    def build(lo, hi):                    # build from inorder[lo..hi]
        nonlocal pre_i
        if lo > hi:
            return None
        root = TreeNode(preorder[pre_i])  # the next preorder value is this subtree's root
        pre_i += 1
        mid = index[root.val]
        root.left = build(lo, mid - 1)    # left first: preorder visits left before right
        root.right = build(mid + 1, hi)
        return root

    return build(0, len(inorder) - 1)
''',
complexity="**Time O(n)** with the index dict. **Space O(n)**.",
tests=r'''
T("example", lambda: from_tree(build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])), [3, 9, 20, None, None, 15, 7])
T("single", lambda: from_tree(build_tree([-1], [-1])), [-1])
T("left chain", lambda: from_tree(build_tree([3, 2, 1], [1, 2, 3])), [3, 2, None, 1])
T("right chain", lambda: from_tree(build_tree([1, 2, 3], [1, 2, 3])), [1, None, 2, None, 3])
''')

P(id="max-path-sum", topic="trees", level="Hard", blind=True, lc=124, title="Binary Tree Maximum Path Sum",
statement="""
A **path** is any sequence of connected nodes (each used at most once). It doesn't have to pass through the root, and it can go up then down. Return the **maximum sum** of any non-empty path. Values can be negative.
""",
examples="""
```text
max_path_sum(to_tree([1, 2, 3]))                          → 6    (2 - 1 - 3)
max_path_sum(to_tree([-10, 9, 20, None, None, 15, 7]))    → 42   (15 - 20 - 7)
max_path_sum(to_tree([-3]))                               → -3
```
""",
eli10="""
**Real-life picture:** each node is a town with a toll (positive = you earn money, negative = you pay). You want the most profitable road trip that never visits a town twice. A trip looks like an **upside-down V**: it climbs up from one side to a "peak" town, then goes down the other side.

For each town, ask two questions:
1. **"Best trip with me as the peak?"** = my value + the best downward path on my left (if it's positive) + the best downward path on my right (if positive). Update the global best.
2. **"Best path going *down* from me, to give to my parent?"** = my value + the better **one** of my left/right downward paths. A parent can only continue through **one** side, because a path can't split.

Negative branches are ignored by taking `max(0, branch)`: "don't go there at all".
""",
approach="""
```text
best = -infinity
gain(node):                       # best downward path starting at node
    if not node: return 0
    left = max(0, gain(node.left))
    right = max(0, gain(node.right))
    best = max(best, node.val + left + right)    # node as the peak
    return node.val + max(left, right)           # one side only, for the parent
```
""",
hints=["For each node, consider it as the 'top' of the path.", "The recursive function returns the best ONE-sided downward path.", "Ignore negative branches with max(0, ...)."],
starter=r'''def max_path_sum(root):
    pass
''',
solution=r'''def max_path_sum(root):
    best = float("-inf")

    def gain(node):
        nonlocal best
        if node is None:
            return 0
        left = max(0, gain(node.left))           # skip losing branches
        right = max(0, gain(node.right))
        best = max(best, node.val + left + right)    # path that peaks at this node
        return node.val + max(left, right)           # the parent can use only one side

    gain(root)
    return best
''',
complexity="**Time O(n)**, **Space O(h)**.",
mistakes="- Returning `node.val + left + right` to the parent. A path can't branch both ways and continue upward.\n- Starting `best = 0`. An all-negative tree must return its largest single value.",
tests=r'''
T("small", lambda: max_path_sum(to_tree([1, 2, 3])), 6)
T("classic", lambda: max_path_sum(to_tree([-10, 9, 20, None, None, 15, 7])), 42)
T("single negative", lambda: max_path_sum(to_tree([-3])), -3)
T("all negative", lambda: max_path_sum(to_tree([-2, -1])), -1)
T("go through", lambda: max_path_sum(to_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])), 48)
''')

P(id="serialize-tree", topic="trees", level="Hard", blind=True, lc=297, title="Serialize and Deserialize Binary Tree",
statement="""
Write `serialize(root)`, which turns a tree into a **string**, and `deserialize(data)`, which rebuilds the **same** tree from it. Any format is fine, as long as the round trip works.
""",
examples="""
```text
deserialize(serialize(to_tree([1, 2, 3, None, None, 4, 5])))  → the same tree
```
""",
eli10="""
**Real-life picture:** you want to send a tree by SMS, which only allows text. Write down a **preorder walk** (node, then left, then right), and write a special mark like `#` for every **empty spot**. The empty spots are important: they tell the receiver where a branch stops, which captures the **shape**.

`1,2,#,#,3,4,#,#,5,#,#`

To rebuild, read the values in the same order: the first value is the root, then rebuild its left subtree (consuming values), then its right subtree. Each `#` means "nothing here".
""",
approach="""
### serialize (preorder with markers)
`walk(node)`: if None, write "#". Otherwise write node.val, then walk(left), then walk(right). Join with commas.

### deserialize
Split on commas into an iterator. `build()`: take the next token. If it's "#", return None. Otherwise make a node, with `node.left = build()` and `node.right = build()`.
""",
hints=["Preorder + a marker for None captures the shape completely.", "Deserialize by consuming tokens in the same order with recursion."],
starter=r'''def serialize(root):
    pass

def deserialize(data):
    pass
''',
solution=r'''def serialize(root):
    out = []
    def walk(node):
        if node is None:
            out.append("#")              # mark the empty spot so the shape is kept
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)
    walk(root)
    return ",".join(out)

def deserialize(data):
    tokens = iter(data.split(","))
    def build():
        tok = next(tokens)
        if tok == "#":
            return None
        node = TreeNode(int(tok))
        node.left = build()              # same order as serialize: left first
        node.right = build()
        return node
    return build()
''',
complexity="**Time O(n)** both ways. **Space O(n)**.",
tests=r'''
def _rt(vals): return from_tree(deserialize(serialize(to_tree(vals))))
T("example", lambda: _rt([1, 2, 3, None, None, 4, 5]), [1, 2, 3, None, None, 4, 5])
T("empty", lambda: _rt([]), [])
T("negatives", lambda: _rt([-1, -2, None, -30]), [-1, -2, None, -30])
C("serialize returns str", lambda: isinstance(serialize(to_tree([1])), str))
''')

# ============================================================ HEAP
P(id="k-smallest", topic="heap", level="Warm-up", title="K Smallest Numbers with heapq",
statement="""
Return the `k` smallest numbers of `nums` in increasing order, using **`heapq`** (not `sorted`).
""",
examples="""
```text
k_smallest([5, 1, 9, 3, 7], 3)  → [1, 3, 5]
```
""",
eli10="""
A **heap** is a "magic box": you can throw numbers in, and you can always take out the **smallest** one quickly (O(log n)). Python's `heapq` turns a normal list into such a box.

- `heapq.heapify(lst)` turns a list into a heap in O(n).
- `heapq.heappop(h)` removes and returns the smallest.
- `heapq.heappush(h, x)` adds x.
""",
approach="Heapify a copy, then pop k times.",
hints=["heapify, then heappop k times."],
starter=r'''import heapq

def k_smallest(nums, k):
    pass
''',
solution=r'''import heapq

def k_smallest(nums, k):
    h = list(nums)
    heapq.heapify(h)                                   # O(n)
    return [heapq.heappop(h) for _ in range(k)]        # k pops, each O(log n)
''',
complexity="**Time O(n + k log n)**. **Space O(n)**.",
tests=r'''
T("example", lambda: k_smallest([5, 1, 9, 3, 7], 3), [1, 3, 5])
T("k = 0", lambda: k_smallest([2, 1], 0), [])
T("duplicates", lambda: k_smallest([2, 2, 1], 2), [1, 2])
''')

P(id="kth-largest", topic="heap", level="Medium", lc=215, title="Kth Largest Element (DSA extra)",
statement="""
Return the k-th **largest** element of `nums` (k=1 means the maximum). Try O(n log k).
""",
examples="""
```text
kth_largest([3, 2, 1, 5, 6, 4], 2)  → 5
```
""",
eli10="""
Keep a small **min-heap of size k**, the "top k club". Every new number tries to join. If the club has more than k members, kick out the **smallest**. At the end the club holds the k largest numbers, and the **smallest member of the club** is the k-th largest overall.
""",
approach="Push each number, and pop when `len(heap) > k`. Return `heap[0]`.",
hints=["A min-heap of size k keeps the k largest numbers seen so far.", "Its top (heap[0]) is the k-th largest."],
starter=r'''import heapq

def kth_largest(nums, k):
    pass
''',
solution=r'''import heapq

def kth_largest(nums, k):
    club = []
    for x in nums:
        heapq.heappush(club, x)
        if len(club) > k:
            heapq.heappop(club)        # drop the smallest; keep only the top k
    return club[0]                     # the smallest of the top k
''',
complexity="**Time O(n log k)**, **Space O(k)**.",
tests=r'''
T("example", lambda: kth_largest([3, 2, 1, 5, 6, 4], 2), 5)
T("duplicates", lambda: kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4)
T("k = 1", lambda: kth_largest([1], 1), 1)
''')

P(id="top-k-frequent", topic="heap", level="Medium", blind=True, lc=347, title="Top K Frequent Elements",
statement="""
Return the `k` most frequent elements of `nums`, in any order. The answer is unique.
""",
examples="""
```text
top_k_frequent([1, 1, 1, 2, 2, 3], 2)  → [1, 2]
top_k_frequent([1], 1)                 → [1]
```
""",
eli10="""
**What it's really asking:** "Which k things appear the most?"

**Real-life picture:** the most popular songs in your class. First **count the votes** for each song (a frequency dict). Then find the k songs with the most votes.

Two good ways:
1. **Heap:** keep a top-k club ordered by count, like the Kth Largest problem. O(n log k).
2. **Bucket sort (the clever O(n) trick):** a count can be at most n. Make buckets numbered 0…n. Put each number into the bucket matching its count ("songs with 3 votes" go in bucket 3). Then walk the buckets from the **highest** down, collecting numbers until you have k.
""",
approach="""
### Bucket version
1. `count = Counter(nums)`.
2. `buckets = [[] for _ in range(len(nums) + 1)]`, and for each `num, c`: `buckets[c].append(num)`.
3. Walk `c` from len(nums) down to 1, extending the result, and stop when you have k.

### Walk-through: [1,1,1,2,2,3], k=2
- counts: {1:3, 2:2, 3:1}
- buckets[3] = [1], buckets[2] = [2], buckets[1] = [3]
- From the top: take 1 (from bucket 3), then 2 (from bucket 2) → [1, 2] ✓
""",
hints=["Count frequencies first.", "Then you need the k largest counts: use a heap, or buckets indexed by count."],
starter=r'''from collections import Counter

def top_k_frequent(nums, k):
    pass
''',
solution=r'''from collections import Counter

def top_k_frequent(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]   # buckets[c] = numbers seen exactly c times
    for num, c in count.items():
        buckets[c].append(num)
    result = []
    for c in range(len(buckets) - 1, 0, -1):       # most frequent first
        for num in buckets[c]:
            result.append(num)
            if len(result) == k:
                return result
    return result
''',
complexity="**Time O(n)** with buckets (a heap gives O(n log k)). **Space O(n)**.",
mistakes="- Sorting the counts gives O(n log n). It's acceptable, but mention the faster options.",
tests=r'''
T("example", lambda: top_k_frequent([1, 1, 1, 2, 2, 3], 2), [1, 2], same_items)
T("single", lambda: top_k_frequent([1], 1), [1], same_items)
T("negatives", lambda: top_k_frequent([4, -1, -1, 4, 4, 2], 2), [4, -1], same_items)
T("all", lambda: top_k_frequent([1, 2], 2), [1, 2], same_items)
''')

P(id="median-stream", topic="heap", level="Hard", blind=True, lc=295, title="Find Median from Data Stream",
statement="""
Design `MedianFinder` with `add_num(x)` and `find_median()`. Numbers arrive one at a time, and `find_median()` returns the current median (the average of the two middle values when the count is even).
""",
examples="""
```text
m = MedianFinder(); m.add_num(1); m.add_num(2); m.find_median() → 1.5
m.add_num(3); m.find_median() → 2
```
""",
eli10="""
**What it's really asking:** "Keep track of the middle value as numbers keep arriving."

**Real-life picture:** students enter a hall one by one and you must always know the middle height. Split the students into two groups:
- **Short group** (the smaller half): you need quick access to its **tallest** member.
- **Tall group** (the bigger half): you need quick access to its **shortest** member.

Keep the groups **equal in size** (or the short group has one extra). Then the median is either the tallest short student, or the average of the tallest short and the shortest tall.

"Quick access to the biggest/smallest" means **heaps**: a **max-heap** for the short half and a **min-heap** for the tall half. Python only has min-heaps, so store **negative numbers** to fake a max-heap.
""",
approach="""
`add_num(x)`:
1. Push x into `low` (as −x).
2. Move low's largest into `high` (this keeps every low ≤ every high).
3. If `high` is now bigger than `low`, move high's smallest back to `low`.

`find_median()`:
- If `low` has more elements: return `-low[0]`.
- Else: return `(-low[0] + high[0]) / 2`.

Each add is O(log n), and find_median is O(1).
""",
hints=["Split the numbers into a lower half and an upper half.", "Max-heap for the lower half (store negatives), min-heap for the upper half.", "Rebalance so the sizes differ by at most 1."],
starter=r'''import heapq

class MedianFinder:
    def __init__(self):
        pass
    def add_num(self, x):
        pass
    def find_median(self):
        pass
''',
solution=r'''import heapq

class MedianFinder:
    def __init__(self):
        self.low = []     # max-heap (stored as negatives): the smaller half
        self.high = []    # min-heap: the larger half

    def add_num(self, x):
        heapq.heappush(self.low, -x)
        heapq.heappush(self.high, -heapq.heappop(self.low))      # the biggest of low goes to high
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))  # keep low the same size or 1 bigger

    def find_median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2
''',
complexity="**add_num O(log n)**, **find_median O(1)**, **Space O(n)**.",
mistakes="- Sorting the whole list on every query is O(n log n) per call, which is too slow for a stream.",
tests=r'''
def _run(ops):
    m = MedianFinder(); out = []
    for x in ops:
        if x == "?": out.append(m.find_median())
        else: m.add_num(x)
    return out
T("example", lambda: _run([1, 2, "?", 3, "?"]), [1.5, 2])
T("negatives", lambda: _run([-1, "?", -2, "?", -3, "?"]), [-1, -1.5, -2])
T("unsorted stream", lambda: _run([5, 15, 1, 3, "?", 8, "?"]), [4.0, 5])
''')
