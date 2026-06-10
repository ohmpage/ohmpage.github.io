# paulohm.com-source
Hugo source files for paulohm.com (public is submodule for ohmpage.github.io)

# File tree

The user who owns this repo is *ohmpage*. The user *paulkohm* is also a co-owner.

This repo is a hugo source repo, so you need Hugo installed on the computer.

The usual hugo navigation works:
* content <- the raw markdown behind all of the content.
* static <- static files like favicon.ico.
* themes <- the theme files
  * ../monopriv <- the theme I chose, customized pretty heavily.
	* ../layouts <- html templates
		* ../partials <- html snippets

The file `doc.md` contains some notes about how I've customized things and gotten my bibtex importer to work.

## Workflow

1. Make content edits to files in the `content/` directory.
2. Make structural edits to files in `themes/monopriv/`.
3. To preview locally: from the repo root, run `hugo server` and visit `http://localhost:1313`.
4. To publish: `git add`, `git commit`, `git push`. GitHub Actions builds the site and deploys it automatically — no manual
`hugo` command needed, no two-step submodule dance.

For changes to the publications list, see the detailed instructions in `doc.md`.

## First-time setup on a new machine

After cloning:
```
pip install "bibtexparser<2"
```
That's the only non-standard dependency. Hugo itself is needed for local preview (`brew install hugo` on Mac); the GitHub Actions
deployment installs its own copy.

## Using scratch

As of 2022, I now have a scratch folder for a quick wormhole (e.g. I use this to make slides available to me in a publicly reachable space that doesn't require a password.)

1. The main `/scratch` endpoint is just in `content/scratch` like other content. You can put markdown files here. The index file is just a simple list of "scratchy" links.
2. Also in the source tree, there is a `static` folder with `img` and `files` and `scratch` folders. You can deposit data, including binary files, in there, and they will populate to the website after the next `hugo/add/commit/push/process` dance.
   - These are available at the `paulohm.com/files` and `paulohm.com/img` (no "static")
3. But if you're in a hurry, you can also just dump the files through the github UI into `static/scratch` of the ohmpage.github.io source tree. These don't get overwritten.
   - These are available at `paulohm.com/scratch`

