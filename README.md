# Welcome Home

Free printable checklists for the first days with a new pet — first week
plan, supply shopping list, first vet visit prep, and a home safety
walk-through, each written specifically for dogs, cats, rabbits & guinea
pigs, or birds.

Live-ish sibling project to Steady Paws (pet health trackers). No account,
no email wall, no tracking scripts.

## Structure

```
site/              → everything Netlify serves, as-is (this is the publish dir)
  index.html
  checklists/       → 16 accessible web worksheets (one per pet × checklist type)
  downloads/         → 16 matching printable PDFs
  assets/            → style.css, site.js
  accessibility.html, privacy.html, terms.html, 404.html
  robots.txt, sitemap.xml

scripts/            → source of truth + generators (not deployed)
  data.py            → all checklist content, plus the SEO phrasing and FAQ
  generate_pdfs.py    → builds site/downloads/*.pdf with reportlab
  generate_site.py    → builds every page in site/ (plus robots + sitemap)
  seo_enhance.py      → deploy-only: injects the Search Console token if set
  qa_site.py          → audits the built site; fails the build on regressions
```

`site/` is fully pre-built and committed, so what you read in the repo is
what gets served. Netlify's build command only runs the two Python audit
steps (`seo_enhance.py`, then `qa_site.py`) — nothing bundles or compiles,
so deploys stay cheap. Regenerate locally, commit the output, push.

## Search basics (don't regress these)

Everything a crawler needs is generated, committed, and then verified:

- **Unique title, meta description, canonical, Open Graph/Twitter tags, and
  JSON-LD on every page.** Titles lead with the species keyword (`Free Dog
  First Week Checklist`), descriptions stay inside search-result length, and
  each checklist H1 names the species.
- **Structured data**: `WebSite` + `CollectionPage` + `FAQPage` on the
  homepage, and `WebPage` + `BreadcrumbList` + an `ItemList` of the actual
  checklist items on each worksheet.
- **Internal links**: the homepage and every worksheet link to the free
  [Your Pet's Health Log](https://yourpetshealthlog.netlify.app/), and each
  worksheet cross-links the other three checklists for the same species.
- **`robots.txt` + `sitemap.xml`** with the checklist pages listed first.

`qa_site.py` enforces all of it — duplicate titles/descriptions/H1s,
over-long titles, mismatched canonicals, a missing health-log link, invalid
JSON-LD, broken local links, unlabeled inputs, or a page missing from the
sitemap all fail the build. It also fails on any checkout or paid-product
link, because the paid binder isn't ready to sell.

## Editing content

1. Edit `scripts/data.py` (add a species, a category, or tweak checklist items).
2. Regenerate:
   ```bash
   pip install -r requirements.txt
   cd scripts
   python3 generate_pdfs.py
   python3 generate_site.py
   ```
3. Check it before committing:
   ```bash
   python3 scripts/qa_site.py
   ```
4. Commit the regenerated files under `site/` along with your `data.py` change.

Adding a new species or category is just adding an entry to `SPECIES` /
`CATEGORIES` and filling in the matching `CHECKLISTS[(species, category)]`
content in `data.py` — everything else (PDFs, worksheet pages, homepage
listings, titles, descriptions, structured data, sitemap) is generated from
that. `SPECIES[...]["search"]` and the `seo` / `heading` / `meta` keys on each
category are what the titles, H1s and descriptions are built from.

## Deploying to Netlify

1. Push this repo to GitHub.
2. In Netlify: **Add new site → Import an existing project → GitHub** → pick this repo.
3. Build settings:
   - Build command: `python3 scripts/seo_enhance.py && python3 scripts/qa_site.py`
     (already set in `netlify.toml`)
   - Publish directory: `site`
4. Optional: set a `GOOGLE_SITE_VERIFICATION` environment variable to have the
   Search Console token injected at deploy time.
5. Deploy. The build only runs two short Python scripts over pre-built files,
   so it won't consume build-minute credits the way a framework build would.

## License

Content and code in this repo: MIT (see `LICENSE`). Swap this out if you'd
rather use something else.
