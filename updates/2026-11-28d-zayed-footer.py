# Adds the Sheikh Zayed page link to the footer of every page (idempotent).
import pathlib, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "public")
pairs = [
    ('<li><a href="dentist-6th-of-october.html">دكتور أسنان في 6 أكتوبر</a></li>',
     '<li><a href="dentist-sheikh-zayed.html">دكتور أسنان لأهل الشيخ زايد</a></li>'),
    ('<li><a href="dentist-6th-of-october.html">Dentist in 6th of October</a></li>',
     '<li><a href="dentist-sheikh-zayed.html">A dentist for Sheikh Zayed patients</a></li>'),
]
n = 0
for f in root.rglob("*.html"):
    s = f.read_text(encoding="utf-8")
    if 'href="dentist-sheikh-zayed.html">دكتور أسنان لأهل' in s or 'href="dentist-sheikh-zayed.html">A dentist for' in s:
        continue
    for a, b in pairs:
        if a in s:
            s = s.replace(a, a + b, 1); f.write_text(s, encoding="utf-8"); n += 1; break
print("zayed footer link added to", n, "pages")
