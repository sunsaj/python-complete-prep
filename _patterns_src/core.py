"""Lesson schema for patterns.html (reuses markdown + Python harness from ../_practice_src/lib.py)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_practice_src"))
import lib  # noqa: E402  (md, _inline, PRELUDE, HARNESS, RUNNER, run_local)

PARTS = [
    ("start", "Part 0 · Start Here"),
    ("solid", "Part 1 · SOLID Principles"),
    ("creational", "Part 2 · Creational Patterns (making objects)"),
    ("structural", "Part 3 · Structural Patterns (connecting objects)"),
    ("behavioral", "Part 4 · Behavioral Patterns (objects working together)"),
    ("project", "Part 5 · Project: QuickBite Food-Ordering App"),
]
LESSONS: list[dict] = []


def L(**kw):
    for r in ["id", "part", "title", "body"]:
        assert r in kw, f"{kw.get('id')}: missing {r}"
    assert kw["part"] in {p[0] for p in PARTS}, kw["id"]
    kw.setdefault("tagline", "")
    kw.setdefault("quiz", [])          # list of (question, answer-markdown)
    kw.setdefault("exercises", [])     # list of dicts made with X()
    LESSONS.append(kw)


def X(id, title, statement, starter, solution, tests, hints=()):
    return {"id": id, "title": title, "statement": statement, "starter": starter,
            "solution": solution, "tests": tests, "hints": list(hints)}
