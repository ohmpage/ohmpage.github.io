I'm using this to document what I've reverse engineered about Hugo.

# Workflow

To add new pubs, do the following:

1. Edit the file at `Documents/Active/administrative/CVs/mypubs.bib` and add new entries for the new pubs.
   - You need to have keys (these are just the strings after the opening curly brackets in the .bib file.)
	 -  There is some magic I don't understand. If you use CamelCase for a bibtex key, it gets turned into a hyphenated lowercase equivalent for the Unix directory name!
	 -  If the article is forthcoming, use the optional key "yearadorn" to have a string like "forthcoming ". The space is necessary.
   - You need to have the modified python code listed below
   - If you have coauthors, just enter them as "and Blah Blah" and it'll do the right thing.
	 -  For more than one coauthor, just put Blah Blah and Blah Blah and Blah Blah etc and it'll turn those ands into commas
   - forthcoming 20xx seems to do the right thing.
2. Run academic to turn these bibtex entries into input directories in Hugo, one per pub with this command:
   - % `academic --verbose import --bibtex ~/Documents/Active/administrative/CVs/mypubs.bib --publication-dir content/pub/ --overwrite`
   - It will show errors for preexisting pubs. No errors the new ones.
	 -  If you change something (e.g. forthcoming to published) you need to rerun by deleting the correct directory in content/pub/.
3. Run Hugo to generate files and preview the changes.
4. As usual, add/commit/push the public/ directory first and then the root directory second.

# Turning bibtex into Hugo posts with `academic`

I am using the `academic` tool from Wowchemy to turn BibTeX entries into Hugo folders and markdown files, one for each publication.

The tool itself comes from PyPi and the `pip3` call. It installs a command line script called `academic`. I called it like so (while cwd is ~/gitpit/paulohm.com-source):

`% academic --verbose import --bibtex ~/Documents/Active/administrative/CVs/mypubs.bib --publication-dir content/pub/ --overwrite`

It took me a while to figure out that the emacs bibtex library doesn't give the bibtex entries a key, and entries without keys are ignored. So I had to add keys for this to do anything. (keys are just the strings after the opening curly brackets in the .bib file.)

By default, it puts the folders and files in `content/publication/` so I had to use the `--publication-dir` flag to use `pub` which I liked better for my URLs.

It imports everything as `draft=true` by default. It took me a while to figure out that I had to change `draft=false` to get posts to compare.

Update: Turns out, `academic` didn't export some of the fields, e.g. `volume`, `year`, or `pages`. So I hand-edited the file at `/Users/ohm/.pyenv/versions/3.12.3/lib/python3.12/site-packages/academic/import_bibtex.py` by adding this block near the very end of the `parse_bibtex_entry` function (after the similar if statements adding various things to the page.yaml dictionary):

```
    # Modified by Paul Ohm, 4/5/2025 to accommodate volumes, page numbers, and years
    others = ("volume", "year", "pages", "yearadorn")
    for curr in others:
        if curr in entry:
            page.yaml[curr] = clean_bibtex_str(entry[curr])
```

I also removed the asterisks that used to bracket the journal name. They were being treated as html rather than markdown and thus being shown.

That worked!

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
