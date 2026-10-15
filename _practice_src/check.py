"""Validate every problem: solution passes all tests, starter loads, ids unique, Blind 75 count."""
import glob, importlib, os, sys, time

sys.path.insert(0, os.path.dirname(__file__))
import lib

for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "p*.py"))):
    importlib.import_module(os.path.basename(f)[:-3])

ids, bad = set(), 0
for p in lib.PROBLEMS:
    assert p["id"] not in ids, "duplicate id " + p["id"]
    ids.add(p["id"])
    t0 = time.perf_counter()
    r = lib.run_local(p["solution"], p["tests"])
    dt = time.perf_counter() - t0
    fails = [x for x in r["results"] if not x["ok"]]
    if r["setup"] or fails or len(r["results"]) < 3:
        bad += 1
        print(f"FAIL {p['id']}: setup={r['setup']} n={len(r['results'])}")
        for x in fails: print("    ", x)
    if dt > 2: print(f"SLOW {p['id']} {dt:.1f}s")
    s = lib.run_local(p["starter"], p["tests"])
    if s["setup"]:
        bad += 1; print(f"STARTER BROKEN {p['id']}: {s['setup']}")
blind = [p for p in lib.PROBLEMS if p["blind"]]
print(f"{len(lib.PROBLEMS)} problems, {len(blind)} Blind 75, {bad} problems with issues")
sys.exit(1 if bad else 0)
