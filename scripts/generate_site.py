# -*- coding: utf-8 -*-
"""Generate the Welcome Home static site (index + worksheet pages + utility pages)."""
import os
from data import SITE, SPECIES, CATEGORIES, CHECKLISTS

SITE_DIR = os.path.join(os.path.dirname(__file__), "..", "site")
CHECKLISTS_DIR = os.path.join(SITE_DIR, "checklists")
os.makedirs(CHECKLISTS_DIR, exist_ok=True)

SPECIES_SORTED = sorted(SPECIES.items(), key=lambda kv: kv[1]["sort"])
CATEGORIES_SORTED = sorted(CATEGORIES.items(), key=lambda kv: kv[1]["sort"])


def base_head(title, description, canonical_path):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE['url']}{canonical_path}">
<meta name="theme-color" content="{SITE['color']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE['url']}{canonical_path}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="/assets/style.css">
</head>
"""


def header_html(active=""):
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/"><span class="tag-mark" aria-hidden="true"></span>{SITE['name']}</a>
    <nav class="site-nav" aria-label="Primary">
      <a href="/#finder">Find a checklist</a>
      <a href="/#how">How it helps</a>
      <a href="/#safety">Care &amp; safety</a>
    </nav>
  </div>
</header>
"""


def footer_html():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <p>{SITE['name']} — free checklists for the first days with a new pet.</p>
    <div class="footer-links">
      <a href="/accessibility.html">Accessibility</a>
      <a href="/privacy.html">Privacy</a>
    </div>
  </div>
</footer>
"""


# ---------------------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------------------

def build_species_tabs():
    buttons = ['<li><button type="button" data-species="all" aria-pressed="true">All pets</button></li>']
    for key, sp in SPECIES_SORTED:
        buttons.append(
            f'<li><button type="button" data-species="{key}" aria-pressed="false">'
            f'<span class="em" aria-hidden="true">{sp["emoji"]}</span>{sp["label"]}</button></li>'
        )
    return "\n      ".join(buttons)


def build_category_blocks():
    blocks = []
    for cat_key, cat in CATEGORIES_SORTED:
        rows = []
        for sp_key, sp in SPECIES_SORTED:
            pdf_href = f"/downloads/{sp_key}-{cat_key}-checklist.pdf"
            worksheet_href = f"/checklists/{sp_key}-{cat_key}.html"
            first_items = [it for _, items in CHECKLISTS[(sp_key, cat_key)] for it in items][:2]
            preview = "; ".join(first_items).rstrip(".")
            rows.append(f"""      <div class="checklist-row" data-species="{sp_key}">
        <div>
          <p class="who"><span aria-hidden="true">{sp['emoji']}</span> {sp['label']}</p>
          <p class="what">{preview}, and more.</p>
        </div>
        <div class="checklist-links">
          <a class="pdf" href="{pdf_href}">Printable PDF</a>
          <a class="web" href="{worksheet_href}">Web worksheet</a>
        </div>
      </div>""")
        blocks.append(f"""  <div class="category-block" id="{cat_key}">
    <h3>{cat['title']}</h3>
    <p class="cat-desc">{cat['desc']}</p>
{chr(10).join(rows)}
  </div>""")
    return "\n\n".join(blocks)


def build_index():
    title = f"{SITE['name']} — Free New Pet Checklists (Printable)"
    desc = SITE["description"]
    html = base_head(title, desc, "/") + f"""<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header_html()}
<main id="main">

  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">Free printable checklists for new pet parents</p>
      <h1>Bring them home ready, not scrambling.</h1>
      <p class="lede">Whatever's joining your family — dog, cat, rabbit, guinea pig, or bird — get the first week, the shopping list, the first vet visit, and the home safety walk-through in one place.</p>
      <div class="hero-actions">
        <a class="btn" href="#finder">Find your checklist</a>
        <p class="fine-print">Free. No account. No email.</p>
      </div>
    </div>
  </section>

  <section class="steps" id="how">
    <div class="wrap">
      <h2>How it helps</h2>
      <ol class="step-list">
        <li>
          <p class="step-num">1</p>
          <h3>Choose your pet</h3>
          <p>Checklists are written for how that species actually settles in — a cat's first week looks nothing like a puppy's.</p>
        </li>
        <li>
          <p class="step-num">2</p>
          <h3>Pick what you need</h3>
          <p>First week plan, supply list, vet visit prep, or a home safety pass — grab one or all four.</p>
        </li>
        <li>
          <p class="step-num">3</p>
          <h3>Walk in ready</h3>
          <p>Print it, or check items off on your phone as you go. Either way, less scrambling on day one.</p>
        </li>
      </ol>
    </div>
  </section>

  <section class="finder" id="finder">
    <div class="wrap">
      <h2>Find a checklist</h2>
      <p>Filter by pet, or browse everything below. Every checklist comes as a printable PDF and an accessible web worksheet.</p>
      <ul class="species-tabs">
      {build_species_tabs()}
      </ul>

{build_category_blocks()}
    </div>
  </section>

  <section class="safety" id="safety">
    <div class="wrap">
      <h2>Before you print: a quick note</h2>
      <p>These checklists are meant to help you get organized and ask better questions — they're general starting points, not species-specific medical or husbandry guidance for every situation. A vet who works with your pet's species is the right source for anything about diet amounts, medication, or a health concern.</p>
      <p>If something feels urgent — your new pet won't eat, seems in pain, or is acting very differently than usual — contact a vet promptly rather than waiting to work through a checklist.</p>
    </div>
  </section>

</main>
{footer_html()}
<script src="/assets/site.js"></script>
</body>
</html>
"""
    with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
        f.write(html)


# ---------------------------------------------------------------------------
# Worksheet pages
# ---------------------------------------------------------------------------

def build_worksheet(sp_key, cat_key):
    sp = SPECIES[sp_key]
    cat = CATEGORIES[cat_key]
    sections = CHECKLISTS[(sp_key, cat_key)]
    slug = f"{sp_key}-{cat_key}"
    pdf_href = f"/downloads/{slug}-checklist.pdf"
    title = f"{cat['title']} for {sp['label']} | {SITE['name']}"
    desc = f"Free accessible web worksheet: {cat['desc']} Built for {sp['label'].lower()}. Also available as a printable PDF."

    total_items = sum(len(items) for _, items in sections)

    section_blocks = []
    idx = 0
    for heading, items in sections:
        lis = []
        for item in items:
            idx += 1
            cid = f"{slug}-i{idx}"
            lis.append(f"""      <li>
        <input type="checkbox" id="{cid}">
        <label for="{cid}">{item}</label>
      </li>""")
        section_blocks.append(f"""    <div class="section-block">
      <h2>{heading}</h2>
      <ul class="check-list">
{chr(10).join(lis)}
      </ul>
    </div>""")

    html = base_head(title, desc, f"/checklists/{slug}.html") + f"""<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header_html()}
<main id="main">
  <div class="worksheet-header">
    <div class="wrap">
      <p class="crumb"><a href="/#{cat_key}">{SITE['name']}</a> / {cat['short']} / {sp['label']}</p>
      <h1>{cat['title']}</h1>
      <p class="sub">For {sp['label']}. {cat['desc']}</p>
      <div class="worksheet-actions">
        <a class="btn" href="{pdf_href}">Download printable PDF</a>
        <a class="btn btn-ghost" href="/#finder">See other checklists</a>
      </div>
      <div class="pet-fields">
        <div>
          <label for="pet-name">Pet's name (stays on your device)</label>
          <input type="text" id="pet-name" autocomplete="off">
        </div>
        <div>
          <label for="date-home">Date home</label>
          <input type="date" id="date-home">
        </div>
      </div>
    </div>
  </div>

  <div class="worksheet-body">
    <div class="wrap" data-worksheet-id="{slug}">
      <p class="progress-note"><strong data-progress>0 of {total_items} done</strong> — checked items are saved on this device only.</p>

{chr(10).join(section_blocks)}

      <p class="reset-row"><button type="button" data-reset>Clear this worksheet</button></p>
    </div>
  </div>
</main>
{footer_html()}
<script src="/assets/site.js"></script>
</body>
</html>
"""
    with open(os.path.join(CHECKLISTS_DIR, f"{slug}.html"), "w") as f:
        f.write(html)


# ---------------------------------------------------------------------------
# Utility pages
# ---------------------------------------------------------------------------

def build_accessibility():
    title = f"Accessibility | {SITE['name']}"
    desc = "Accessibility statement for Welcome Home's free pet checklist printables and web worksheets."
    html = base_head(title, desc, "/accessibility.html") + f"""<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header_html()}
<main id="main">
  <section class="simple-page">
    <h1>Accessibility</h1>
    <p>{SITE['name']} is built so every checklist works without an account, without JavaScript, and without a mouse.</p>
    <h2>What that looks like in practice</h2>
    <ul>
      <li>Every printable checklist has a matching web worksheet built from real HTML checkboxes and labels, readable by screen readers and operable by keyboard.</li>
      <li>Color is never the only signal — checked items also get a line-through and a status count.</li>
      <li>Text and interactive elements meet WCAG AA contrast against the page background.</li>
      <li>The site works, and every PDF can still be downloaded, with JavaScript turned off. JavaScript only adds checkbox-saving and the pet-species filter.</li>
      <li>Layout is responsive from small phones up to wide desktop screens.</li>
    </ul>
    <h2>Something not working for you?</h2>
    <p>If you run into an accessibility barrier anywhere on this site, please open an issue on the project's GitHub repository so it can get fixed.</p>
  </section>
</main>
{footer_html()}
</body>
</html>
"""
    with open(os.path.join(SITE_DIR, "accessibility.html"), "w") as f:
        f.write(html)


def build_privacy():
    title = f"Privacy | {SITE['name']}"
    desc = "Privacy information for Welcome Home's free pet checklist printables."
    html = base_head(title, desc, "/privacy.html") + f"""<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header_html()}
<main id="main">
  <section class="simple-page">
    <h1>Privacy</h1>
    <p>{SITE['name']} does not ask for an account or an email address, and does not run visitor tracking or advertising scripts.</p>
    <h2>What's stored, and where</h2>
    <p>When you check off items on a web worksheet, or type your pet's name and the date they came home, that's saved using your browser's local storage — on your device only. It is never sent to a server, and clearing your browser data will remove it.</p>
    <h2>Hosting</h2>
    <p>This site is static and hosted on Netlify. Netlify may log basic, aggregate technical request data (like any web host) to keep the service running; Welcome Home itself does not add any additional analytics.</p>
  </section>
</main>
{footer_html()}
</body>
</html>
"""
    with open(os.path.join(SITE_DIR, "privacy.html"), "w") as f:
        f.write(html)


def build_robots_and_sitemap():
    with open(os.path.join(SITE_DIR, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")

    urls = ["/", "/accessibility.html", "/privacy.html"]
    for sp_key in SPECIES:
        for cat_key in CATEGORIES:
            urls.append(f"/checklists/{sp_key}-{cat_key}.html")

    items = "\n".join(f"  <url><loc>{SITE['url']}{u}</loc></url>" for u in urls)
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
"""
    with open(os.path.join(SITE_DIR, "sitemap.xml"), "w") as f:
        f.write(sitemap)


def main():
    build_index()
    for sp_key in SPECIES:
        for cat_key in CATEGORIES:
            build_worksheet(sp_key, cat_key)
    build_accessibility()
    build_privacy()
    build_robots_and_sitemap()
    print("Site generated in", SITE_DIR)


if __name__ == "__main__":
    main()
