# Idempotent patch (27 Nov 2026): treatment images -> treatment-specific photos (Unsplash licence stock + clinic's own kids photo with parental consent)
import pathlib, sys, json, re, shutil, html
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "public")
src = pathlib.Path(__file__).resolve().parent
dst = root / "assets" / "img"; dst.mkdir(parents=True, exist_ok=True)
for f in src.glob("*.jpg"):
    shutil.copyfile(f, dst / f.name)
# Stock photos (Unsplash licence: free for commercial use), downloaded at deploy time, cropped 4:5 by Unsplash's image service
import urllib.request
STOCK = {'dental-implant-model.jpg': 'photo-1593022356769-11f762e25ed9', 'braces-brackets-smile.jpg': 'photo-1656514894252-fb336a3ad6a6', 'clear-aligner-fitting.jpg': 'photo-1777793636393-a0fec488f3fb', 'root-canal-tooth-model.jpg': 'photo-1777793389944-f7165259a05c', 'wisdom-teeth-xray.jpg': 'photo-1777445374290-eedda5be8e5b', 'teeth-scaling-cleaning.jpg': 'photo-1606811971618-4486d14f3f99', 'emergency-toothache-cold-compress.jpg': 'photo-1602932213623-cc17e9541bb4'}
for name, pid in STOCK.items():
    if (dst / name).exists(): continue
    try:
        req = urllib.request.Request("https://images.unsplash.com/%s?w=800&h=1000&fit=crop&crop=entropy&fm=jpg&q=76" % pid, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        if data[:3] == b"\xff\xd8\xff" and len(data) > 20000: (dst / name).write_bytes(data)
    except Exception as e:
        print("download failed", name, e)
RULES = json.loads('[["tx-implants", "Dental Implants", "dental-implant-model", "Dental implant model: titanium implant post with a crown between natural teeth", "Illustrative stock photo"], ["tx-implants", "زراعة الأسنان", "dental-implant-model", "مجسم زراعة أسنان: زرعة تيتانيوم عليها طربوش بين أسنان طبيعية", "صورة توضيحية"], ["tx-root-canal", "Root Canal Treatment", "root-canal-tooth-model", "Tooth cross-section model showing decay reaching the pulp and root canals", "Illustrative stock photo"], ["tx-root-canal", "حشو العصب", "root-canal-tooth-model", "مجسم مقطع سنة بيوضح تسوس واصل للعصب وقنوات الجذور", "صورة توضيحية"], ["tx-scaling", "Scaling & Polishing", "teeth-scaling-cleaning", "Teeth being cleaned with a dental mirror and scaler", "Illustrative stock photo"], ["tx-scaling", "تنظيف الجير", "teeth-scaling-cleaning", "تنظيف الأسنان بمراية وأداة إزالة الجير", "صورة توضيحية"], ["tx-extractions", "Extractions & Wisdom Teeth", "wisdom-teeth-xray", "Panoramic dental X-ray showing the wisdom teeth", "Illustrative stock photo"], ["tx-extractions", "خلع الأسنان وضروس العقل", "wisdom-teeth-xray", "أشعة بانوراما للأسنان بتوضح ضروس العقل", "صورة توضيحية"], ["tx-kids", "Children\'s Dentistry", "kids-dentist-dr-fatma-hesham", "Dr. Fatma Hesham, pediatric dentist, with two young patients at Enhanced Dental Clinic", "Dr. Fatma Hesham with two of our young patients"], ["tx-kids", "أسنان الأطفال", "kids-dentist-dr-fatma-hesham", "د. فاطمة هشام، طبيبة أسنان الأطفال، مع طفلتين في عيادة إنهانسد", "د. فاطمة هشام مع اتنين من مرضانا الصغيرين"], ["clinic-treatment", "Orthodontics (Braces)", "braces-brackets-smile", "Close-up of teeth with metal braces: brackets and archwire", "Illustrative stock photo"], ["clinic-treatment", "تقويم الأسنان", "braces-brackets-smile", "أسنان عليها تقويم معدني: براكتس وسلك", "صورة توضيحية"], ["clinic-treatment", "Emergency Dental Care", "emergency-toothache-cold-compress", "Person holding a cold compress to the cheek for toothache", "Illustrative stock photo"], ["clinic-treatment", "طوارئ الأسنان", "emergency-toothache-cold-compress", "شخص حاطط كمادة باردة على خده من ألم الضرس", "صورة توضيحية"], ["clinic-lounge", "Clear Aligners & Invisalign", "clear-aligner-fitting", "Patient fitting a clear aligner onto the upper teeth", "Illustrative stock photo"], ["clinic-lounge", "التقويم الشفاف وإنفزلاين", "clear-aligner-fitting", "مريضة بتركّب تقويم شفاف على الأسنان العلوية", "صورة توضيحية"]]')
def esc(s): return html.escape(s, quote=True)
n = 0
for p in root.rglob("*.html"):
    s = p.read_text(encoding="utf-8"); t = s
    for old, title, new, alt, cap in RULES:
        if not (dst / (new + ".jpg")).exists(): continue
        pat = re.compile(r'srcset="([^"]*?)assets/img/' + re.escape(old) + r'\.webp"><img src="([^"]*?)assets/img/' + re.escape(old) + r'\.jpg" alt="' + re.escape(esc(title)) + '" ')
        t = pat.sub(lambda m: 'srcset="%sassets/img/%s.webp"><img src="%sassets/img/%s.jpg" alt="%s" width="800" height="1000" ' % (m.group(1), new, m.group(2), new, esc(alt)), t)
        a = '<aside class="aside rv"><div class="frame outlined"><picture>'
        i = t.find(a)
        if i >= 0:
            j = t.find("</picture></div>", i)
            seg = t[i:j]
            if ("assets/img/%s.jpg" % new) in seg and not t[j+16:].startswith('<p class="muted"'):
                t = t[:j+16] + '<p class="muted" style="font-size:.8rem;margin:8px 2px 0">%s</p>' % esc(cap) + t[j+16:]
    if t != s:
        p.write_text(t, encoding="utf-8"); n += 1
print("copied", len(list(src.glob("*.jpg"))), "images; patched", n, "files")
