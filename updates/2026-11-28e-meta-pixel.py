# Idempotent patch (28 Nov 2026): Meta pixel 643888871619620 on every page; Contact event on WhatsApp/call clicks, custom ClickBook on booking-page links
import pathlib, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "public")
MARK = "<!-- Meta Pixel 643888871619620 -->"
PIXEL = MARK + """<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','643888871619620');fbq('track','PageView');document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';if(h.indexOf('tel:')===0)fbq('track','Contact',{method:'call'});else if(/wa\\.me|whatsapp/i.test(h))fbq('track','Contact',{method:'whatsapp'});else if(/book\\.html/.test(h))fbq('trackCustom','ClickBook');},true);</script><noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=643888871619620&ev=PageView&noscript=1"/></noscript>"""
n = 0
for p in root.rglob("*.html"):
    s = p.read_text(encoding="utf-8")
    if MARK in s or "</head>" not in s:
        continue
    p.write_text(s.replace("</head>", PIXEL + "</head>", 1), encoding="utf-8")
    n += 1
print("meta pixel added to", n, "pages")
