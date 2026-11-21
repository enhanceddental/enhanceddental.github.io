# Adds the clinic's Facebook page next to Instagram/TikTok on every page (idempotent).
import glob, sys
FB = "https://www.facebook.com/61573322218797"
root = sys.argv[1]
n = 0
for f in glob.glob(root + "/**/*.html", recursive=True):
    s = open(f, encoding="utf-8").read()
    if FB in s:
        continue
    t = s.replace('>Instagram</a> · <a href="https://www.tiktok.com/@enhanced_clinic"',
                  '>Instagram</a> · <a href="%s" target="_blank" rel="noopener">Facebook</a> · <a href="https://www.tiktok.com/@enhanced_clinic"' % FB)
    t = t.replace('>Instagram @enhancedclinic</a><br><a href="https://www.tiktok.com/@enhanced_clinic"',
                  '>Instagram @enhancedclinic</a><br><a href="%s" target="_blank" rel="noopener">Facebook · Enhanced Dental Clinic</a><br><a href="https://www.tiktok.com/@enhanced_clinic"' % FB)
    t = t.replace('"sameAs": ["https://www.instagram.com/enhancedclinic/", "https://www.tiktok.com/@enhanced_clinic"',
                  '"sameAs": ["https://www.instagram.com/enhancedclinic/", "%s", "https://www.tiktok.com/@enhanced_clinic"' % FB)
    if t != s:
        open(f, "w", encoding="utf-8").write(t); n += 1
print("facebook link added to", n, "pages")
