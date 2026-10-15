"""Build ../practice.html: validate every solution first, then embed all problems as JSON.

Run:  python build.py        (from this folder)
"""
import glob, importlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

if subprocess.call([sys.executable, os.path.join(HERE, "check.py")]) != 0:
    sys.exit("Validation failed: practice.html NOT written.")

import lib
from primers import PRIMERS, INTRO
for f in sorted(glob.glob(os.path.join(HERE, "p*.py"))):
    if os.path.basename(f) != "primers.py":
        importlib.import_module(os.path.basename(f)[:-3])

topic_order = [t[0] for t in lib.TOPICS]
problems = sorted(lib.PROBLEMS, key=lambda p: (topic_order.index(p["topic"]), lib.LEVELS.index(p["level"])))  # stable: keeps authored order within a level

data = {
    "intro": lib.md(INTRO),
    "topics": [{"id": tid, "title": title, "blurb": blurb, "primer": lib.md(PRIMERS[tid])} for tid, title, blurb in lib.TOPICS],
    "problems": [{
        "id": p["id"], "topic": p["topic"], "level": p["level"], "title": p["title"], "blind": p["blind"], "lc": p["lc"],
        "statement": lib.md(p["statement"]), "examples": lib.md(p["examples"]), "eli10": lib.md(p["eli10"]),
        "approach": lib.md(p["approach"]), "hints": [lib._inline(h) for h in p["hints"]],
        "starter": p["starter"].strip("\n") + "\n", "solution": p["solution"].strip("\n") + "\n",
        "complexity": lib.md(p["complexity"]), "mistakes": lib.md(p["mistakes"]), "tests": p["tests"],
    } for p in problems],
    "python": {"prelude": lib.PRELUDE, "harness": lib.HARNESS, "runner": lib.RUNNER},
}
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = open(os.path.join(HERE, "template.html"), encoding="utf-8").read().replace("/*__DATA__*/", payload)
out = os.path.join(HERE, "..", "practice.html")
open(out, "w", encoding="utf-8").write(html)
print(f"wrote practice.html: {len(problems)} problems, {sum(p['blind'] for p in problems)} Blind 75, {len(html) // 1024} KB")
