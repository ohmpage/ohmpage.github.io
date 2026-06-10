I'm using this to document what I've reverse engineered about Hugo.

# Publication Import Workflow

Publications are tracked in `bib/mypubs.bib` (standard BibTeX format, compatible with Zotero and other tools). A Python script
converts that file into Hugo content pages under `content/pub/`, one directory per publication.

## Adding or updating a publication

1. Edit `bib/mypubs.bib`. Each entry needs at minimum:
   - A **key** (the string after `@Article{` — use CamelCase for multi-word keys, e.g. `DataAnalysisRules`)
   - `author`, `title`, `journal`, `year`
   - Optionally: `volume`, `pages`
   - For forthcoming articles: `yearadorn = {forthcoming}` (no trailing space needed)
   - For coauthors: just list everyone in the `author` field as normal BibTeX (`{Paul Ohm and Jane Smith}`) — the script filters
you out automatically

2. Run the import script from the repo root:
   ```
   python scripts/import_pubs.py bib/mypubs.bib
   ```
   This creates new entries and skips existing ones. To update an existing entry (e.g., changing forthcoming to published, or
fixing a typo):
   ```
   python scripts/import_pubs.py bib/mypubs.bib --overwrite
   ```

3. Commit and push as usual — GitHub Actions builds and deploys automatically.

## First-time setup on a new machine

```
pip install "bibtexparser<2"
```

The version pin matters — bibtexparser 2.x has a completely different API and will break the script.

## How the script works (if you need to modify it)

The script lives at `scripts/import_pubs.py`. Key behaviors:

- **BibTeX key → directory name**: CamelCase keys get hyphenated and lowercased. `DataAnalysisRules` → `data-analysis-rules`,
`VanBuren` → `van-buren`, `Branding` → `branding`. Once a pub has a directory, don't rename its BibTeX key or the old directory
becomes an orphan.

- **Coauthors**: The script strips `Paul Ohm` from the author list (see `SITE_AUTHOR` constant at the top of the script) and
stores only the remaining authors under a `coauthors:` field. Solo papers get no `coauthors` field. The citation template
(`themes/monopriv/layouts/partials/citation.html`) uses this field to render the "(with X, Y)" parenthetical — it has no
knowledge of your name.

- **Fields written**: Only the fields Hugo actually uses: `title`, `date`, `publication`, `volume`, `year`, `pages`, `yearadorn`,
`coauthors`. All the boilerplate fields the old `academic` tool generated (abstract, doi, url_pdf, etc.) are omitted because the
site never displayed them.

- **`OPT*` fields**: Emacs bibtex-mode prefixes optional/empty fields with `OPT` (e.g., `OPTvolume`). The script ignores these
automatically.




# Getting the pub entries to appear

## Hugo Basics

Each subfolder under `content/` is known as a "section". But until it has a `_index.html` file, the URLs to `pub/` do not render.

The landing page is created using the file `layouts/_default/list.html` in the `themes/monopriv/` subdirectory.

I added this new block to the big `if` statement:

```
	{{else if eq .Section "pub"}}
		<div class="row">
                  {{range .Pages}}
                  <div class="m-3">
		    {{ .Title }}, 
		    {{ .Params.publication }}
                  </div>
                  {{end}}
		</div>
```

The key variables are at [https://gohugo.io/variables/page/](here). Especially important is the `.Params` which can pull any variable from the markdown page itself, which is how I grab all of the pubs metadata.
