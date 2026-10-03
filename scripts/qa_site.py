#!/usr/bin/env python3
"""Static QA checks for the prebuilt Welcome Home site."""
from __future__ import annotations

import json
import logging
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE_URL = "https://welcomehomepet.netlify.app"
HEALTH_LOG = "https://yourpetshealthlog.netlify.app/"
LOG = logging.getLogger("welcomehome.qa")

# Search-result limits: longer than this and Google rewrites or truncates it.
TITLE_MAX = 65
DESC_MIN = 70
DESC_MAX = 165

# The paid binder is not ready, so no checkout of any kind may ship. Buy Me a
# Coffee is allowed only as the bare profile link, never a product/extras page.
FORBIDDEN_LINKS = (
    re.compile(r"gumroad\.com", re.I),
    re.compile(r"buymeacoffee\.com/[\w.-]+/\S", re.I),
    re.compile(r"\b(add to cart|checkout now|buy now)\b", re.I),
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_depth = 0
        self.title = ""
        self.lang = ""
        self.h1_count = 0
        self.ids: list[str] = []
        self.links: list[tuple[str, str, str]] = []
        self.labels: set[str] = set()
        self.controls: list[tuple[str, str]] = []
        self.description = ""
        self.canonical = ""
        self.robots = ""
        self.headings: list[str] = []
        self.h1_depth = 0
        self.h1_text = ""
        self.jsonld_depth = 0
        self.jsonld: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.lang = data.get("lang", "")
        elif tag == "title":
            self.title_depth += 1
        elif tag == "h1":
            self.h1_count += 1
            self.h1_depth += 1
        elif tag == "meta" and data.get("name", "").lower() == "description":
            self.description = data.get("content", "").strip()
        elif tag == "meta" and data.get("name", "").lower() == "robots":
            self.robots = data.get("content", "").strip()
        elif tag == "link" and data.get("rel", "").lower() == "canonical":
            self.canonical = data.get("href", "").strip()
        elif tag == "script" and data.get("type", "").lower() == "application/ld+json":
            self.jsonld_depth += 1
            self.jsonld.append("")

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings.append(tag)
        elif tag == "label" and data.get("for"):
            self.labels.add(data["for"])
        elif tag in {"input", "select", "textarea"}:
            control_type = data.get("type", "text").lower()
            if control_type not in {"hidden", "submit", "button"}:
                self.controls.append((tag, data.get("id", "")))

        if data.get("id"):
            self.ids.append(data["id"])
        for attr in ("href", "src"):
            if data.get(attr):
                self.links.append((tag, attr, data[attr]))
        if data.get("target") == "_blank":
            rel = set(data.get("rel", "").lower().split())
            if "noopener" not in rel:
                self.links.append((tag, "unsafe_blank", data.get("href", "")))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1
        elif tag == "script" and self.jsonld_depth:
            self.jsonld_depth -= 1
        elif tag == "h1" and self.h1_depth:
            self.h1_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title += data
        if self.h1_depth:
            self.h1_text += data
        if self.jsonld_depth and self.jsonld:
            self.jsonld[-1] += data


def local_target(page: Path, raw_url: str) -> Path | None:
    parsed = urlsplit(raw_url)
    if parsed.scheme or parsed.netloc or raw_url.startswith(("mailto:", "tel:", "data:")):
        return None
    path = parsed.path
    if not path or path == "/":
        return SITE / "index.html"
    if path.startswith("/"):
        target = SITE / path.lstrip("/")
    else:
        target = page.parent / path
    if target.is_dir():
        target /= "index.html"
    return target.resolve()


def expected_canonical(page: Path) -> str:
    rel = page.relative_to(SITE).as_posix()
    return BASE_URL + ("/" if rel == "index.html" else f"/{rel}")


def check_page(page: Path) -> tuple[list[str], PageParser | None]:
    errors: list[str] = []
    try:
        text = page.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(text)
    except (OSError, UnicodeError) as exc:
        return [f"cannot read/parse page: {exc}"], None

    title = parser.title.strip()
    if parser.lang.lower() != "en":
        errors.append("missing or unexpected <html lang=\"en\">")
    if not title:
        errors.append("missing non-empty <title>")
    elif len(title) > TITLE_MAX:
        errors.append(f"title is {len(title)} chars, over the {TITLE_MAX}-char search limit")
    if not parser.description:
        errors.append("missing meta description")
    elif not DESC_MIN <= len(parser.description) <= DESC_MAX:
        errors.append(
            f"meta description is {len(parser.description)} chars, "
            f"outside the {DESC_MIN}-{DESC_MAX} range"
        )
    if not parser.canonical.startswith("https://"):
        errors.append("missing HTTPS canonical URL")
    elif parser.canonical != expected_canonical(page):
        errors.append(
            f"canonical {parser.canonical} does not match page path "
            f"(expected {expected_canonical(page)})"
        )
    if not parser.robots:
        errors.append("missing meta robots")
    if parser.h1_count != 1:
        errors.append(f"expected exactly one h1, found {parser.h1_count}")
    if parser.headings and parser.headings[0] != "h1":
        errors.append(f"first heading on the page is <{parser.headings[0]}>, not <h1>")
    if not parser.jsonld:
        errors.append("missing JSON-LD structured data")
    for payload in parser.jsonld:
        try:
            json.loads(payload)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON-LD structured data: {exc}")
    for pattern in FORBIDDEN_LINKS:
        found = pattern.search(text)
        if found:
            errors.append(f"checkout/paid-product reference is not allowed yet: {found.group(0)!r}")
    if len(parser.ids) != len(set(parser.ids)):
        errors.append("duplicate element id found")

    for tag, control_id in parser.controls:
        if not control_id:
            errors.append(f"{tag} control missing id")
        elif control_id not in parser.labels:
            errors.append(f"control #{control_id} missing matching label")

    for _tag, attr, raw_url in parser.links:
        if attr == "unsafe_blank":
            errors.append(f"target=_blank link missing rel=noopener: {raw_url}")
            continue
        target = local_target(page, raw_url)
        if target is not None and not target.exists():
            errors.append(f"broken local {attr}: {raw_url}")
    return errors, parser


def check_site(parsed: dict[Path, PageParser]) -> list[str]:
    """Site-wide rules: unique search metadata and the free health-log handoff."""
    errors: list[str] = []
    fields = {
        "title": lambda parser: parser.title.strip(),
        "meta description": lambda parser: parser.description,
        "h1": lambda parser: " ".join(parser.h1_text.split()),
    }
    for label, getter in fields.items():
        seen: dict[str, Path] = {}
        for page, parser in parsed.items():
            value = getter(parser)
            if not value:
                continue
            if value in seen:
                errors.append(
                    f"duplicate {label} shared by {seen[value].relative_to(ROOT)} "
                    f"and {page.relative_to(ROOT)}: {value!r}"
                )
            else:
                seen[value] = page

    for page, parser in parsed.items():
        rel = page.relative_to(SITE).as_posix()
        if rel != "index.html" and not rel.startswith("checklists/"):
            continue
        hrefs = [url for _tag, attr, url in parser.links if attr == "href"]
        if not any(url.startswith(HEALTH_LOG) for url in hrefs):
            errors.append(f"{rel} is missing an internal link to the free health log")
    return errors


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        pages = sorted(SITE.rglob("*.html"))
        if not pages:
            raise RuntimeError("no HTML pages found under site/")
        failures = 0
        parsed: dict[Path, PageParser] = {}
        for page in pages:
            issues, parser = check_page(page)
            if parser is not None:
                parsed[page] = parser
            if issues:
                failures += len(issues)
                for issue in issues:
                    LOG.error("%s: %s", page.relative_to(ROOT), issue)
        for issue in check_site(parsed):
            failures += 1
            LOG.error("site: %s", issue)
        for required in (SITE / "robots.txt", SITE / "sitemap.xml"):
            if not required.is_file():
                failures += 1
                LOG.error("missing required SEO file: %s", required.relative_to(ROOT))
        sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
        indexable = [
            p for p in pages
            if p.relative_to(SITE).as_posix() != "404.html"
        ]
        for page in indexable:
            if expected_canonical(page) not in sitemap:
                failures += 1
                LOG.error("sitemap.xml is missing %s", expected_canonical(page))
        if failures:
            LOG.error("QA failed with %d issue(s) across %d HTML pages", failures, len(pages))
            return 1
        LOG.info(
            "QA passed: %d HTML pages — links, labels, unique search metadata, "
            "structured data, health-log links and SEO files",
            len(pages),
        )
        return 0
    except Exception as exc:  # Final guard: CI should fail loudly, never silently.
        LOG.exception("QA crashed: %s", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
