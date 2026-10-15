"""Build ../patterns.html. Validates every exercise first; reuses the look + Python runner of practice.html.

Run:  python build.py        (from this folder)
"""
import glob, importlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
if subprocess.call([sys.executable, os.path.join(HERE, "check.py")]) != 0:
    sys.exit("Validation failed: patterns.html NOT written.")

import core
from core import lib
for f in sorted(glob.glob(os.path.join(HERE, "l*.py"))):
    importlib.import_module(os.path.basename(f)[:-3])

# shared look + editor + Python runner, taken from the practice page template (single source of truth)
practice = open(os.path.join(HERE, "..", "_practice_src", "template.html"), encoding="utf-8").read()
css = practice[practice.index("<style>") + 7:practice.index("</style>")]
script = practice[practice.index("<script>\n(function") + 8:practice.rindex("</script>")]
def block(start, end):
    i = script.index(start)
    return script[i:script.index(end, i)]
shared = (block("  /* ---------- syntax highlighting", "  /* ---------- data helpers")
          + block("  /* ---------- tiny code editor", "  /* ---------- Python runner")
          + block("  /* ---------- Python runner", "  function runTests"))
# adapt the single-editor bits to many editors per page
shared = shared.replace('$("#runBtn").click()', 'ta.dispatchEvent(new Event("run"))')
shared = re.sub(r"function updateStatus\(\) \{.*?\n  \}\n", '''function updateStatus() {
    const txt = { idle: "", loading: "⏳ Loading Python in your browser… (first time ~10 MB, then cached)", ready: "🟢 Python ready", running: "⚙️ Running…", error: "🔴 Python failed to load" }[py.state] || "";
    $$(".pystatus").forEach(el => el.textContent = txt);
    $$(".runBtn").forEach(b => b.disabled = py.state === "running");
  }
''', shared, flags=re.S)
assert "pystatus" in shared and 'new Event("run")' in shared, "shared JS adaptation failed"

data = {
    "parts": core.PARTS,
    "lessons": [{
        "id": l["id"], "part": l["part"], "title": l["title"], "tagline": l["tagline"], "body": lib.md(l["body"]),
        "quiz": [[lib._inline(q), lib.md(a)] for q, a in l["quiz"]],
        "exercises": [{"id": x["id"], "title": x["title"], "statement": lib.md(x["statement"]),
                       "starter": x["starter"].strip("\n") + "\n", "solution": x["solution"].strip("\n") + "\n",
                       "tests": x["tests"], "hints": [lib._inline(h) for h in x["hints"]]} for x in l["exercises"]],
    } for l in core.LESSONS],
    "python": {"prelude": lib.PRELUDE, "harness": lib.HARNESS, "runner": lib.RUNNER},
}
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
html = (tpl.replace("/*__CSS__*/", css).replace("/*__SHARED_JS__*/", shared)
           .replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
open(os.path.join(HERE, "..", "patterns.html"), "w", encoding="utf-8").write(html)
print(f"wrote patterns.html: {len(core.LESSONS)} lessons, {sum(len(l['exercises']) for l in core.LESSONS)} exercises, {len(html) // 1024} KB")
