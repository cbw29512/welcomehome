#!/usr/bin/env python3
"""Apply shared SEO metadata to the prebuilt Welcome Home static pages."""
from __future__ import annotations

import json
import os
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE_URL = "https://welcomehomepet.netlify.app"
VERIFY = os.getenv("GOOGLE_SITE_VERIFICATION", "").strip()


class PageInfo(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_depth = 0
        self.h1_depth = 0
        self.label_for = ""
        self.label_parts: list[str] = []
        self.title = ""
        self.h1 = ""
        self.description = ""
        self.checkbox_ids: set[str] = set()
        self.checkbox_labels: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "title":
            self.title_depth += 1
        elif tag == "h1":
            self.h1_depth += 1
        elif tag == "meta" and data.get("name", "").lower() == "description":
            self.description = data.get("content", "").strip()
        elif tag == "input" and data.get("type", "").lower() == "checkbox" and data.get("id"):
            self.checkbox_ids.add(data["id"])
        elif tag == "label" and data.get("for"):
            self.label_for = data["for"]
            self.label_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1
        elif tag == "h1" and self.h1_depth:
            self.h1_depth -= 1
        elif tag == "label" and self.label_for:
            if self.label_for in self.checkbox_ids:
                label = " ".join("".join(self.label_parts).split())
                if label:
                    self.checkbox_labels.append(label)
            self.label_for = ""
            self.label_parts = []

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title += data
        if self.h1_depth:
            self.h1 += data
        if self.label_for:
            self.label_parts.append(data)


def canonical_url(page: Path) -> str:
    rel = page.relative_to(SITE).as_posix()
    return BASE_URL + ("/" if rel == "index.html" else f"/{rel}")


def schema_for(page: Path, info: PageInfo) -> dict:
    url = canonical_url(page)
    rel = page.relative_to(SITE).as_posix()
    common = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": info.title.strip(),
        "description": info.description,
        "url": url,
        "isPartOf": {"@type": "WebSite", "name": "Welcome Home", "url": BASE_URL + "/"},
    }
    if rel == "index.html":
        return {
            "@context": "https://schema.org",
            "@graph": [
                {"@type": "WebSite", "name": "Welcome Home", "url": BASE_URL + "/"},
                {
                    "@type": "CollectionPage",
                    "name": info.title.strip(),
                    "description": info.description,
                    "url": url,
                    "about": [
                        {"@type": "Thing", "name": "New pet checklists"},
                        {"@type": "Thing", "name": "Pet preparation"},
                    ],
                },
            ],
        }
    if rel.startswith("checklists/") and info.checkbox_labels:
        common["mainEntity"] = {
            "@type": "ItemList",
            "numberOfItems": len(info.checkbox_labels),
            "itemListElement": [
                {"@type": "ListItem", "position": pos, "name": label}
                for pos, label in enumerate(info.checkbox_labels, start=1)
            ],
        }
    return common


def enhance(page: Path) -> bool:
    text = page.read_text(encoding="utf-8")
    info = PageInfo()
    info.feed(text)
    additions: list[str] = []
    rel = page.relative_to(SITE).as_posix()

    if 'name="robots"' not in text:
        robots = "noindex, follow" if rel == "404.html" else "index, follow, max-image-preview:large"
        additions.append(f'<meta name="robots" content="{robots}">')
    if 'rel="icon"' not in text:
        additions.append('<link rel="icon" href="/favicon.ico" sizes="any">')
    if 'property="og:site_name"' not in text:
        additions.append('<meta property="og:site_name" content="Welcome Home">')
    if 'property="og:locale"' not in text:
        additions.append('<meta property="og:locale" content="en_US">')
    if 'name="twitter:title"' not in text:
        additions.append(f'<meta name="twitter:title" content="{info.title.strip()}">')
    if 'name="twitter:description"' not in text:
        additions.append(f'<meta name="twitter:description" content="{info.description}">')
    if VERIFY and 'name="google-site-verification"' not in text:
        additions.append(f'<meta name="google-site-verification" content="{VERIFY}">')
    if 'type="application/ld+json"' not in text:
        payload = json.dumps(schema_for(page, info), ensure_ascii=False, separators=(",", ":"))
        additions.append(f'<script type="application/ld+json">{payload}</script>')

    if not additions:
        return False
    if "</head>" not in text:
        raise RuntimeError(f"missing </head> in {page}")
    text = text.replace("</head>", "\n" + "\n".join(additions) + "\n</head>", 1)
    page.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    pages = sorted(SITE.rglob("*.html"))
    if not pages:
        raise RuntimeError("no HTML pages found under site/")
    changed = sum(1 for page in pages if enhance(page))
    print(f"SEO enhancement complete: {changed}/{len(pages)} pages updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
