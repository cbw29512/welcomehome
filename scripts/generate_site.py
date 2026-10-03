# -*- coding: utf-8 -*-
"""Generate the Welcome Home static site (index + worksheet pages + utility pages)."""
import datetime
import json
import os
from data import SITE, SPECIES, CATEGORIES, CHECKLISTS, FAQ

SITE_DIR = os.path.join(os.path.dirname(__file__), "..", "site")
CHECKLISTS_DIR = os.path.join(SITE_DIR, "checklists")
os.makedirs(CHECKLISTS_DIR, exist_ok=True)

SPECIES_SORTED = sorted(SPECIES.items(), key=lambda kv: kv[1]["sort"])
CATEGORIES_SORTED = sorted(CATEGORIES.items(), key=lambda kv: kv[1]["sort"])

INDEX_ROBOTS = "index, follow, max-image-preview:large"


def website_node():
    return {
        "@type": "WebSite",
        "name": SITE["name"],
        "url": SITE["url"] + "/",
        "description": SITE["description"],
    }


def breadcrumb_node(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": pos, "name": name, "item": url}
            for pos, (name, url) in enumerate(trail, start=1)
        ],
    }


def page_node(title, description, canonical_path, extra=None):
    node = {
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": SITE["url"] + canonical_path,
        "isPartOf": website_node(),
    }
    node.update(extra or {})
    return node


def base_head(title, description, canonical_path, schema, robots=INDEX_ROBOTS):
    payload = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE['url']}{canonical_path}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="{SITE['color']}">
<link rel="icon" href="/favicon.ico" sizes="any">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE['url']}{canonical_path}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{payload}</script>
</head>
"""


def header_html(active=""):
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/"><span class="tag-mark" aria-hidden="true"></span>{SITE['name']}</a>
    <nav class="site-nav" aria-label="Primary">
      <a href="/#finder">Checklists</a>
      <a href="{SITE['health_log_url']}">Health log</a>
      <a href="/#safety">Care &amp; safety</a>
    </nav>
    <a class="support-link" href="{SITE['coffee_url']}" target="_blank" rel="noopener">Buy me a coffee</a>
  </div>
</header>
"""


def footer_html():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <p>{SITE['name']} — free checklists for the first days with a new pet.</p>
    <div class="footer-links">
      <a href="{SITE['health_log_url']}">Health log</a>
      <a href="/accessibility.html">Accessibility</a>
      <a href="/privacy.html">Privacy</a>
      <a href="/terms.html">Terms</a>
      <a href="{SITE['coffee_url']}" target="_blank" rel="noopener">Buy me a coffee (optional)</a>
    </div>
  </div>
</footer>
"""


def health_log_section():
    return f"""  <section class="handoff" id="next">
    <div class="wrap">
      <div class="handoff-card">
        <p class="eyebrow">After the first week</p>
        <h2>The checklists get them home. The health log keeps the record.</h2>
        <p>Your Pet's Health Log is the free companion site for everything that comes next — weights, vet visits, medications, and what you want to ask at the next appointment. Same deal as here: no account, no email.</p>
        <p class="handoff-action"><a class="btn btn-ghost" href="{SITE['health_log_url']}">Open the free health log</a></p>
        <p class="fine-print">Goes to yourpetshealthlog.netlify.app. Free, nothing to buy.</p>
      </div>
    </div>
  </section>
"""


def support_section():
    return f"""  <section class="support" id="support">
    <div class="wrap">
      <p>Every checklist here stays free. If one of them saved you a second trip to the pet store, you can <a href="{SITE['coffee_url']}" target="_blank" rel="noopener">buy me a coffee</a> — completely optional, and it never unlocks anything, because nothing here is locked.</p>
    </div>
  </section>
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
          <a class="web" href="{worksheet_href}" aria-label="Open the {sp['label']} {cat['heading']}">Open checklist</a>
          <a class="pdf" href="{pdf_href}" aria-label="Download the printable {sp['label']} {cat['heading']} PDF">Printable PDF</a>
        </div>
      </div>""")
        blocks.append(f"""  <div class="category-block" id="{cat_key}">
    <h3>{cat['title']}</h3>
    <p class="cat-desc">{cat['desc']}</p>
{chr(10).join(rows)}
  </div>""")
    return "\n\n".join(blocks)


def build_faq_blocks():
    blocks = []
    for entry in FAQ:
        answer = entry["a"]
        if entry.get("link") == "health_log":
            answer = answer.replace(
                "Your Pet's Health Log",
                f'<a href="{SITE["health_log_url"]}">Your Pet\'s Health Log</a>',
                1,
            )
        blocks.append(f"""        <div class="faq-item">
          <h3>{entry['q']}</h3>
          <p>{answer}</p>
        </div>""")
    return "\n".join(blocks)


def index_schema(title, desc):
    return {
        "@context": "https://schema.org",
        "@graph": [
            website_node(),
            {
                "@type": "CollectionPage",
                "name": title,
                "description": desc,
                "url": SITE["url"] + "/",
                "isPartOf": website_node(),
                "about": [
                    {"@type": "Thing", "name": f"{sp['label']} care checklists"}
                    for _, sp in SPECIES_SORTED
                ],
                "hasPart": [
                    {
                        "@type": "ItemList",
                        "name": cat["title"],
                        "description": cat["desc"],
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": pos,
                                "name": f"{sp['label']} {cat['heading']}",
                                "url": f"{SITE['url']}/checklists/{sp_key}-{cat_key}.html",
                            }
                            for pos, (sp_key, sp) in enumerate(SPECIES_SORTED, start=1)
                        ],
                    }
                    for cat_key, cat in CATEGORIES_SORTED
                ],
            },
            {
                "@type": "FAQPage",
                "url": SITE["url"] + "/#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": entry["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": entry["a"]},
                    }
                    for entry in FAQ
                ],
            },
        ],
    }


def build_index():
    title = f"Free New Pet Checklists (Printable PDF) | {SITE['name']}"
    desc = SITE["description"]
    html = base_head(title, desc, "/", index_schema(title, desc)) + f"""<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header_html()}
<main id="main">

  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">Printable PDFs and phone worksheets</p>
      <h1>Free new pet checklists for the first week home.</h1>
      <p class="lede">Bring them home ready, not scrambling — whether it's a dog, cat, rabbit, guinea pig, or bird.</p>
      <div class="hero-actions">
        <a class="btn btn-lg" href="#finder">Get your free checklist</a>
        <p class="fine-print">Free. No account. No email.</p>
      </div>
      <p class="hero-aside">Already settled in? <a href="{SITE['health_log_url']}">Open the free health log</a> to track weights, vet visits, and meds.</p>
    </div>
  </section>

  <section class="finder" id="finder">
    <div class="wrap">
      <h2>Pick your pet, grab your checklist</h2>
      <p>Tap a pet to narrow it down. Every checklist opens as a tappable worksheet on your phone, or a printable PDF.</p>
      <ul class="species-tabs">
      {build_species_tabs()}
      </ul>

{build_category_blocks()}
    </div>
  </section>

{health_log_section()}
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
          <p>Check items off on your phone as you go, or print it for the fridge. Either way, less scrambling on day one.</p>
        </li>
      </ol>
    </div>
  </section>

  <section class="faq" id="faq">
    <div class="wrap">
      <h2>Common questions</h2>
      <div class="faq-list">
{build_faq_blocks()}
      </div>
    </div>
  </section>

  <section class="safety" id="safety">
    <div class="wrap">
      <h2>Before you print: a quick note</h2>
      <p>These checklists are meant to help you get organized and ask better questions — they're general starting points, not species-specific medical or husbandry guidance for every situation. A vet who works with your pet's species is the right source for anything about diet amounts, medication, or a health concern.</p>
      <p>If something feels urgent — your new pet won't eat, seems in pain, or is acting very differently than usual — contact a vet promptly rather than waiting to work through a checklist.</p>
    </div>
  </section>

{support_section()}
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

def worksheet_meta(sp_key, cat_key):
    """Title, H1 and meta description for one checklist page, species named first."""
    sp = SPECIES[sp_key]
    cat = CATEGORIES[cat_key]
    heading = f"{sp['label']} {cat['heading']}"
    title = f"Free {sp['label']} {cat['seo']} | {SITE['name']}"
    desc = (
        f"Free {sp['search']} {cat['seo'].lower()}: {cat['meta']}. "
        f"Tick it off on your phone or print the PDF."
    )
    return title, heading, desc


def build_sibling_links(sp_key, cat_key):
    sp = SPECIES[sp_key]
    links = []
    for other_key, other in CATEGORIES_SORTED:
        if other_key == cat_key:
            continue
        links.append(
            f'        <li><a href="/checklists/{sp_key}-{other_key}.html">'
            f"{sp['label']} {other['heading']}</a></li>"
        )
    return f"""      <nav class="sibling-links" aria-label="More {sp['label']} checklists">
        <h2>More free {sp['label'].lower()} checklists</h2>
        <ul>
{chr(10).join(links)}
        </ul>
      </nav>"""


def worksheet_schema(sp_key, cat_key, title, desc, canonical_path, items):
    sp = SPECIES[sp_key]
    cat = CATEGORIES[cat_key]
    return {
        "@context": "https://schema.org",
        "@graph": [
            page_node(
                title,
                desc,
                canonical_path,
                {
                    "breadcrumb": breadcrumb_node(
                        [
                            (SITE["name"], SITE["url"] + "/"),
                            (cat["title"], f"{SITE['url']}/#{cat_key}"),
                            (f"{sp['label']} {cat['heading']}", SITE["url"] + canonical_path),
                        ]
                    ),
                    "mainEntity": {
                        "@type": "ItemList",
                        "name": f"{sp['label']} {cat['heading']}",
                        "numberOfItems": len(items),
                        "itemListElement": [
                            {"@type": "ListItem", "position": pos, "name": item}
                            for pos, item in enumerate(items, start=1)
                        ],
                    },
                },
            ),
        ],
    }


def build_worksheet(sp_key, cat_key):
    sp = SPECIES[sp_key]
    cat = CATEGORIES[cat_key]
    sections = CHECKLISTS[(sp_key, cat_key)]
    slug = f"{sp_key}-{cat_key}"
    pdf_href = f"/downloads/{slug}-checklist.pdf"
    canonical_path = f"/checklists/{slug}.html"
    title, heading, desc = worksheet_meta(sp_key, cat_key)
    all_items = [item for _, items in sections for item in items]

    total_items = sum(len(items) for _, items in sections)

    section_blocks = []
    idx = 0
    for section_heading, items in sections:
        lis = []
        for item in items:
            idx += 1
            cid = f"{slug}-i{idx}"
            lis.append(f"""      <li>
        <input type="checkbox" id="{cid}">
        <label for="{cid}">{item}</label>
      </li>""")
        section_blocks.append(f"""    <div class="section-block">
      <h2>{section_heading}</h2>
      <ul class="check-list">
{chr(10).join(lis)}
      </ul>
    </div>""")

    schema = worksheet_schema(sp_key, cat_key, title, desc, canonical_path, all_items)
    html = base_head(title, desc, canonical_path, schema) + f"""<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header_html()}
<main id="main">
  <div class="worksheet-header">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="/">{SITE['name']}</a> / <a href="/#{cat_key}">{cat['short']}</a> / {sp['label']}
      </nav>
      <h1>{heading}</h1>
      <p class="sub">{cat['desc']} Written for {sp['search']} owners, free to print or use on your phone.</p>
      <p class="worksheet-hint">Tap an item to check it off — progress saves on this device.</p>
      <div class="worksheet-actions">
        <a class="btn btn-ghost" href="{pdf_href}">Download printable PDF</a>
        <a class="text-link" href="/#finder">See other checklists</a>
      </div>
      <div class="pet-fields">
        <div>
          <label for="pet-name">Pet's name</label>
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

      <div class="worksheet-next">
        <h2>Once the first week is behind you</h2>
        <p>Weights, vet visits, medications, and questions for the next appointment all live in <a href="{SITE['health_log_url']}">Your Pet's Health Log</a> — the free companion site, no account needed.</p>
        <p><a class="btn btn-ghost" href="{SITE['health_log_url']}">Open the free health log</a></p>
      </div>

{build_sibling_links(sp_key, cat_key)}
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
    desc = ("Accessibility statement for Welcome Home: every free pet checklist works "
            "with a screen reader, a keyboard, JavaScript off, and on a phone.")
    html = base_head(title, desc, "/accessibility.html",
                     page_node(title, desc, "/accessibility.html")) + f"""<body>
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
    desc = ("How Welcome Home handles your data: no account, no email, no tracking "
            "scripts, and checked checklist items stay in your own browser.")
    html = base_head(title, desc, "/privacy.html",
                     page_node(title, desc, "/privacy.html")) + f"""<body>
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


def build_terms():
    title = f"Terms | {SITE['name']}"
    desc = ("Terms for Welcome Home: every pet checklist is free to print and use, "
            "support is optional, and nothing here replaces veterinary advice.")
    html = base_head(title, desc, "/terms.html",
                     page_node(title, desc, "/terms.html")) + f"""<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header_html()}
<main id="main">
  <section class="simple-page">
    <h1>Terms</h1>
    <p>{SITE['name']} checklists are organizational aids. They do not diagnose, prescribe, or replace a veterinarian.</p>
    <h2>Everything here is free</h2>
    <p>Every checklist, worksheet, and PDF on this site is free to download and use. There is no account, no email wall, and nothing to buy to get the full version — this is the full version.</p>
    <h2>Optional support</h2>
    <p>If you want to chip in for the hosting, there's a Buy Me a Coffee link in the footer. It is entirely optional and it does not unlock extra content.</p>
    <h2>Supply links</h2>
    <p>Shopping lists may later include affiliate links. If they do, {SITE['name']} may earn a commission, the price you pay does not change, and those links are not veterinary recommendations.</p>
    <p><a href="/privacy.html">Privacy</a> &middot; <a href="/accessibility.html">Accessibility</a></p>
  </section>
</main>
{footer_html()}
</body>
</html>
"""
    with open(os.path.join(SITE_DIR, "terms.html"), "w") as f:
        f.write(html)


def build_404():
    title = f"Page Not Found | {SITE['name']}"
    desc = "That Welcome Home pet checklist page could not be found. Browse the free new pet checklists instead."
    html = base_head(title, desc, "/404.html",
                     page_node(title, desc, "/404.html"),
                     robots="noindex, follow") + f"""<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header_html()}
<main id="main">
  <section class="simple-page">
    <h1>That page wandered off.</h1>
    <p>The checklist or page you tried to open is not here.</p>
    <p><a class="btn" href="/#finder">Browse all pet checklists</a></p>
  </section>
</main>
{footer_html()}
</body>
</html>
"""
    with open(os.path.join(SITE_DIR, "404.html"), "w") as f:
        f.write(html)


def build_robots_and_sitemap():
    with open(os.path.join(SITE_DIR, "robots.txt"), "w") as f:
        f.write(
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /404.html\n"
            f"Sitemap: {SITE['url']}/sitemap.xml\n"
        )

    today = datetime.date.today().isoformat()
    # Checklist pages are the pages meant to rank, so they lead the sitemap.
    urls = [("/", "1.0")]
    for sp_key, _ in SPECIES_SORTED:
        for cat_key, _ in CATEGORIES_SORTED:
            urls.append((f"/checklists/{sp_key}-{cat_key}.html", "0.8"))
    urls += [("/accessibility.html", "0.3"), ("/privacy.html", "0.3"), ("/terms.html", "0.3")]

    items = "\n".join(
        f"  <url><loc>{SITE['url']}{path}</loc>"
        f"<lastmod>{today}</lastmod><priority>{priority}</priority></url>"
        for path, priority in urls
    )
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
    build_terms()
    build_404()
    build_robots_and_sitemap()
    print("Site generated in", SITE_DIR)


if __name__ == "__main__":
    main()
