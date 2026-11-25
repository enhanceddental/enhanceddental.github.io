# Idempotent patch: new Facebook username + Google review count (25 Nov 2026)
import pathlib, re, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "public")
n = 0
for p in list(root.rglob("*.html")) + list(root.rglob("*.txt")) + list(root.rglob("*.xml")):
    s = p.read_text(encoding="utf-8")
    t = s.replace("https://www.facebook.com/61573322218797", "https://www.facebook.com/enhancedclinic")
    t = t.replace("<strong>292</strong>", "<strong>297</strong>")
    t = t.replace("<br>292 ", "<br>297 ")
    t = t.replace("from 292 reviews", "from 297 reviews")
    if t != s:
        p.write_text(t, encoding="utf-8"); n += 1
print("patched", n, "files")
