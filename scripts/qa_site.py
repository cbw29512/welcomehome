#!/usr/bin/env python3
"""Static QA checks for the prebuilt Welcome Home site."""
from __future__ import annotations

import logging
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
LOG = logging.getLogger("welcomehome.qa")


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

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.lang = data.get("lang", "")
        elif tag == "title":
            self.title_depth += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta" and data.get("name", "").lower() == "description":
            self.description = data.get("content", "").strip()
        elif tag == "link" and data.get("rel", "").lower() == "canonical":
            self.canonical = data.get("href", "").strip()
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

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title += data


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


def check_page(page: Path) -> list[str]:
    errors: list[str] = []
    try:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        return [f"cannot read/parse page: {exc}"]

    if parser.lang.lower() != "en":
        errors.append("missing or unexpected <html lang=\"en\">")
    if not parser.title.strip():
        errors.append("missing non-empty <title>")
    if not parser.description:
        errors.append("missing meta description")
    if not parser.canonical.startswith("https://"):
        errors.append("missing HTTPS canonical URL")
    if parser.h1_count != 1:
        errors.append(f"expected exactly one h1, found {parser.h1_count}")
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
    return errors


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        pages = sorted(SITE.rglob("*.html"))
        if not pages:
            raise RuntimeError("no HTML pages found under site/")
        failures = 0
        for page in pages:
            issues = check_page(page)
            if issues:
                failures += len(issues)
                for issue in issues:
                    LOG.error("%s: %s", page.relative_to(ROOT), issue)
        for required in (SITE / "robots.txt", SITE / "sitemap.xml"):
            if not required.is_file():
                failures += 1
                LOG.error("missing required SEO file: %s", required.relative_to(ROOT))
        if failures:
            LOG.error("QA failed with %d issue(s) across %d HTML pages", failures, len(pages))
            return 1
        LOG.info("QA passed: %d HTML pages, local links, labels, metadata and SEO files", len(pages))
        return 0
    except Exception as exc:  # Final guard: CI should fail loudly, never silently.
        LOG.exception("QA crashed: %s", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
