#!/usr/bin/env python3
"""Inject the Welcome Home monetization funnel into prebuilt pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
HEALTH = "https://yourpetshealthlog.netlify.app/"
PACK = "https://buymeacoffee.com/divclass016/extras"
CANON = "https://welcomehomepet.netlify.app"

HANDOFF = f'''  <section class="handoff" id="next">
    <div class="wrap">
      <p class="eyebrow">After the first week</p>
      <h2>The checklists get them home. The health log keeps the record.</h2>
      <p>Singles stay free. When you want the first-week sheets and the matching trackers in one pack, that is the only thing for sale.</p>
      <div class="hero-actions">
        <a class="btn" href="{HEALTH}">Open the health log</a>
        <a class="btn btn-ghost" href="{PACK}" target="_blank" rel="noopener">Species starter pack</a>
      </div>
    </div>
  </section>

'''

TERMS = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Terms | Welcome Home</title>
<meta name="description" content="Terms for Welcome Home free pet checklists, the optional starter pack, and future supply links.">
<link rel="canonical" href="{CANON}/terms.html">
<meta name="theme-color" content="#c1694f">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header"><div class="wrap"><a class="brand" href="/"><span class="tag-mark" aria-hidden="true"></span>Welcome Home</a></div></header>
<main id="main"><section class="simple-page">
<h1>Terms</h1>
<p>Welcome Home checklists are organizational aids. They do not diagnose, prescribe, or replace a veterinarian.</p>
<h2>Free pages</h2>
<p>Every checklist and worksheet on this site is free. No account and no email are required.</p>
<h2>Starter pack</h2>
<p>The species starter pack is optional. Buying it is not required to download any checklist on this site.</p>
<h2>Supply links</h2>
<p>Shopping lists may later include affiliate links. If they do, Welcome Home may earn a commission, and the price you pay does not change. Those links are not veterinary recommendations.</p>
<p><a href="/privacy.html">Privacy</a></p>
</section></main>
</body>
</html>
'''

FOOTER_EXTRA = (
    f'<a href="/terms.html">Terms</a>'
    f'<a href="{HEALTH}">Health log</a>'
    f'<a href="{PACK}" target="_blank" rel="noopener">Starter pack</a>'
)


def main() -> None:
    (SITE / "terms.html").write_text(TERMS, encoding="utf-8")
    for page in SITE.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        if "/terms.html" not in html and "footer-links" in html:
            html = html.replace(
                '<a href="/privacy.html">Privacy</a>',
                '<a href="/privacy.html">Privacy</a>' + FOOTER_EXTRA,
                1,
            )
        if page.name == "index.html" and 'id="next"' not in html:
            html = html.replace('<section class="safety"', HANDOFF + '<section class="safety"', 1)
        page.write_text(html, encoding="utf-8")
    sitemap = SITE / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    loc = f"<url><loc>{CANON}/terms.html</loc></url>"
    if loc not in text:
        text = text.replace("</urlset>", f"  {loc}\n</urlset>")
        sitemap.write_text(text, encoding="utf-8")
    print("funnel applied")


if __name__ == "__main__":
    main()
