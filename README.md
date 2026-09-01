# New Nest

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
  accessibility.html, privacy.html, robots.txt, sitemap.xml

scripts/            → source of truth + generators (not deployed)
  data.py            → all checklist content lives here
  generate_pdfs.py    → builds site/downloads/*.pdf with reportlab
  generate_site.py    → builds site/index.html + site/checklists/*.html
```

`site/` is fully pre-built and committed to the repo. Netlify does **not**
run a build step (see `netlify.toml` — `command = ""`), it just serves the
`site` folder directly. That means deploys don't burn Netlify build
minutes/credits — regenerate locally, commit the output, push.

## Editing content

1. Edit `scripts/data.py` (add a species, a category, or tweak checklist items).
2. Regenerate:
   ```bash
   pip install -r requirements.txt
   cd scripts
   python3 generate_pdfs.py
   python3 generate_site.py
   ```
3. Commit the regenerated files under `site/` along with your `data.py` change.

Adding a new species or category is just adding an entry to `SPECIES` /
`CATEGORIES` and filling in the matching `CHECKLISTS[(species, category)]`
content in `data.py` — everything else (PDFs, worksheet pages, homepage
listings, sitemap) is generated from that.

## Deploying to Netlify

1. Push this repo to GitHub.
2. In Netlify: **Add new site → Import an existing project → GitHub** → pick this repo.
3. Build settings:
   - Build command: *(leave empty)*
   - Publish directory: `site`
4. Deploy. Since there's no build command, this deploy (and every future one)
   just uploads static files — it won't consume build-minute credits the way
   a framework build would.

## License

Content and code in this repo: MIT (see `LICENSE`). Swap this out if you'd
rather use something else.
