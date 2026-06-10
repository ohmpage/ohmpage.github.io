# paulohm.com-source
Hugo source files for paulohm.com (public is submodule for ohmpage.github.io)

# File tree

The user who owns this repo is *ohmpage*. The user *paulkohm* is also a co-owner.

This repo is a hugo source repo, so you need Hugo installed on the computer.

The usual hugo navigation works:
* content <- the raw markdown behind all of the content.
* static <- static files like favicon.ico.
* themes <- four themes
  * ../monopriv <- the theme I chose, customized pretty heavily.
	* ../layouts <- html templates
		* ../partials <- html snippets

The `public` directory is a github submodule that is the home directory for ohmpage.github.io. It must be sync'd (pull/add/commit/push) independent to the source tree.

The file `doc.md` contains some notes about how I've customized things and gotten my bibtex importer to work.

## Workflow

1. Make content edits to files in `content` directory.
2. Make structure edits to files in `themes/monopriv`
3. To preview, sit in `paulohm.com-source` directory and type
   * `% hugo server`
   Visit localhost:1313
4. Once satisfied, from the same directory, run an unadorned `% hugo`.
5. Key: Do the git commits/pushes in this order: 1. `public` and 2. `root`.
   * Reasoning: Pushing the public directory changes the submodule metadata, flipping the dirty bit for the root directory.
6. For changes to the pubs list, follow the workflow instructions in doc.md.

## Using scratch

As of 2022, I now have a scratch folder for a quick wormhole (e.g. I use this to make slides available to me in a publicly reachable space that doesn't require a password.)

1. The main `/scratch` endpoint is just in `content/scratch` like other content. You can put markdown files here.
2. Also in the source tree, there is a `static` folder with both `img` and `files` folders. You can deposit data, including binary files, in there, and they will populate to the website after the next `hugo/add/commit/push/process` dance.
   - These are available at the `paulohm.com/files` and `paulohm.com/img` (no "static")
3. But if you're in a hurry, you can also just dump the files through the github UI into `scratch` of the ohmpage.github.io source tree. These don't get overwritten.
   - These are available at `paulohm.com/scratch`

# Resyncing on new compute

When you are recloning these repos on a new computer, you need to do a few things to get the submodules working, to avoid the dreaded "HEAD detached."

1. Directions
   - the first time you reclone the tree, you need to run `git submodule init` to make that connection.
   - Then, every time you edit, you need to run `git submodule update` to fetch data from the project
   - You can also do `git clone --recurse-submodules`
   - Note that the hugo theme used is also a submodule.
2. Another workaround: For preexisting projects with submodules, this seemed to work (1/2023):
   - git clone the top repo
   - Still in the top level, `git submodule init`
   - Then `git submodule update` which is like `git clone` for the subdir.
   - Go into the subdir and `git status`.
	 - You might get the red error that says "Detached HEAD"
   - Look up the name of the main/master branch in the submodule repo
   - cd into the submodule subdir
   - `git checkout master` (or `main` or whatever).
   - `git status` again to confirm it worked.
