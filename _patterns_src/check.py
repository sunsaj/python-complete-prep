"""Validate every lesson exercise: the solution passes all tests and the starter loads."""
import glob, importlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core
from core import lib

for f in sorted(glob.glob(os.path.join(HERE, "l*.py"))):
    importlib.import_module(os.path.basename(f)[:-3])

ids, bad, n_ex = set(), 0, 0
for les in core.LESSONS:
    assert les["id"] not in ids, "duplicate lesson " + les["id"]
    ids.add(les["id"])
    for ex in les["exercises"]:
        n_ex += 1
        assert ex["id"] not in ids, "duplicate id " + ex["id"]
        ids.add(ex["id"])
        r = lib.run_local(ex["solution"], ex["tests"])
        fails = [x for x in r["results"] if not x["ok"]]
        if r["setup"] or fails or len(r["results"]) < 2:
            bad += 1
            print(f"FAIL {les['id']}/{ex['id']}: setup={r['setup']} n={len(r['results'])}")
            for x in fails: print("    ", x)
        s = lib.run_local(ex["starter"], ex["tests"])
        if s["setup"]:
            bad += 1; print(f"STARTER BROKEN {ex['id']}: {s['setup']}")
        if all(x["ok"] for x in s["results"]) and s["results"]:
            print(f"WARNING starter already passes {ex['id']}")
import re
n_snip = 0
for les in core.LESSONS:                      # every ```python example in the lesson text must at least compile
    for lang, code in re.findall(r"```(\w*)\n(.*?)```", les["body"], re.S):
        if lang in ("text", "plain"):
            continue
        n_snip += 1
        try:
            compile(code, les["id"], "exec")
        except SyntaxError as e:
            bad += 1; print(f"SNIPPET SYNTAX {les['id']}: line {e.lineno}: {e.msg}\n    {e.text}")
print(f"{len(core.LESSONS)} lessons, {n_ex} exercises, {n_snip} lesson snippets, {bad} with issues")
sys.exit(1 if bad else 0)
