# Paul Ohm's Personal Website — CLAUDE.md

Hugo-based academic website for Paul Ohm, Professor of Law at Georgetown University Law Center. Theme: `monopriv` (custom, lives in `themes/monopriv/`). Deployed via GitHub Pages.

## Publication Pipeline

Publications are maintained in one BibTeX file and imported into Hugo via a Python script. **Never hand-edit files in `content/pub/` — regenerate them from the bib file instead.**

### Workflow

1. Edit `bib/mypubs.bib` to add or update entries.
2. Run the import script from the repo root:
   ```
   python scripts/import_pubs.py bib/mypubs.bib
   ```
   Use `--overwrite` to regenerate existing entries (e.g., to add a URL):
   ```
   python scripts/import_pubs.py bib/mypubs.bib --overwrite
   ```
3. Commit both the updated `.bib` file and any changed `content/pub/` files.

**Dependency:** `pip install "bibtexparser<2"` (must use v1, not v2).

### How `import_pubs.py` works

- Reads `@Article` and `@Book` entries from the `.bib` file.
- Converts the BibTeX key to a hyphenated slug: `DataAnalysisRules` → `data-analysis-rules`, `VanBuren` → `van-buren`.
- Creates `content/pub/<slug>/index.md` with Hugo front matter.
- Writes `pubtype: article` or `pubtype: book` based on the BibTeX entry type.
- Strips `Paul Ohm` from the author list; remaining authors become the `coauthors` list.
- By default, skips slugs whose directories already exist (safe re-run). Pass `--overwrite` to update them.

### Front matter fields generated

**All entries:**

| Field | Source | Notes |
|---|---|---|
| `title` | `title` field | Quoted if it contains special chars |
| `date` | `year` field | Set to `<year>-01-01` |
| `pubtype` | BibTeX entry type | `article` or `book` |
| `year` | `year` field | Stored separately for display |
| `yearadorn` | `yearadorn` field | Custom adornment before the year (e.g., "forthcoming") |
| `link` | `url` field | External URL; makes title a hyperlink |
| `coauthors` | `author` field | All authors except `Paul Ohm` |
| `draft` | — | Always `false` |

**Articles only** (`pubtype: article`):

| Field | Source | Notes |
|---|---|---|
| `publication` | `journal` field | Used for journals, book titles, edited volume names |
| `volume` | `volume` field | |
| `pages` | `pages` field | |

**Books only** (`pubtype: book`):

| Field | Source | Notes |
|---|---|---|
| `publisher` | `publisher` field | Publishing house |

### BibTeX conventions

- Use `@Article` for journal articles, book chapters, and essays in edited volumes.
- Use `@Book` for monographs. Standard fields: `author`, `title`, `publisher`, `year`, `url`.
- The `journal` field on `@Article` holds the venue for all article types, including edited volumes.
- `OPTkey`, `OPTnumber`, `OPTmonth`, etc. are ignored by the importer.
- `yearadorn` is a custom non-standard field for annotations before the year (e.g., `forthcoming`).
- BibTeX keys use CamelCase (e.g., `FactAndFriction`, `VanBuren`); the importer converts these to slug form.

### Adding a forthcoming book

```bibtex
@Book{YourKey,
  author    = {Paul Ohm and Co-Author Name},
  title     = {Your Book Title},
  publisher = {Publisher Name},
  year      = {2026},
  yearadorn = {forthcoming},
  url       = {https://...}
}
```

Then run `python scripts/import_pubs.py bib/mypubs.bib`.

## Hugo Structure

```
content/
  pub/
    _index.md          # Section title page ("Publications")
    <slug>/
      index.md         # One file per publication, front matter only, no body
  ...
themes/monopriv/
  layouts/
    partials/
      citation.html    # Renders a single publication as a formatted citation
    _default/
      list.html        # Pub section splits into Books / Articles; other sections list links
```

### Citation rendering (`citation.html`)

The partial always receives a dict: `(dict "page" . "bookprefix" true/false)`.

**Article format:**
```
[linked-title], [volume] [publication] [pages] ([yearadorn] [year]) (with [coauthors]).
```

**Book format:**
```
[linked-title] ([publisher], [yearadorn] [year]) (with [coauthors]).
```

- Title is italic (`<em>`) for both types; a hyperlink if `link` is set.
- Optional fields (`volume`, `pages`, `publisher`, `yearadorn`, `coauthors`) are omitted when empty.
- When `bookprefix: true` is passed (homepage only), book citations are prepended with `Book: `.

### Publications list page

Books appear first under an *Books* subheading, followed by articles under *Articles and Book Chapters*. Both subheadings are hidden when there are no books (i.e., the page looks unchanged until the first `@Book` entry is added).

### Homepage Recent Publications

The homepage shows the 7 most recent entries sorted by date, mixing books and articles chronologically. Books get a `Book: ` prefix so they're identifiable in the mixed list.

## Running locally

```
hugo server
```

## Deployment

GitHub Actions deploys to GitHub Pages on push to `master`. Node.js 24 opt-in is intentionally reverted — it breaks the deploy-pages OIDC auth step.
