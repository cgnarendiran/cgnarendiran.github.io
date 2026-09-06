# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Narendiran Chembu's personal site (blog + project portfolio), a Jekyll site built on the
third-party [Reked](https://github.com/artemsheludko/reked) theme. It is deployed by
GitHub Pages directly from the `master` branch of `cgnarendiran/cgnarendiran.github.io`
(no CI workflow) — pushing to `master` publishes. `README.md` describes this site; the
upstream theme's original readme was replaced in `9cba132`.

**Known production gap:** `_config.yml` enables `jekyll/tagging`, which is *not* on GitHub
Pages' plugin allowlist, so it is silently skipped on the live build. The 124 `/tag/<tag>/`
pages generate locally but 404 in production, which means every tag link rendered on a post
page is dead. Don't assume tag links work just because they resolve on a local server.

The agreed fix is to drop the plugin and add a plugin-free `/tags/` index page that works on
the stock GitHub Pages build, so local and production finally match. Until that lands, tags
authored in the new format are still correct — only the link targets are pending.

Most work here is authoring content in `_posts/` and `_projects/`, not changing code.

## Automation

Three cloud routines (claude.ai/code/routines) write and publish content on a schedule. All work
from `origin/master`, open a PR, self-check it and merge it; none pushes to `master` directly.

- **Blog job**, Sun + Wed 9:15am Pacific. Reads `.claude/blog-topic-queue.md` and
  `.claude/writing-style-guide.md`, writes the next queued post into `_posts/` and
  `images/blogN/`, and moves the queue row to Published. Figures come from
  `.claude/scripts/fetch_arxiv_figures.py`.
- **LinkedIn companion job**, Sun + Wed 12:15pm Pacific. Reads `.claude/linkedin-ledger.md` and
  `.claude/linkedin-style-guide.md`, writes a companion post for the oldest eligible blog post
  not yet in the ledger or the outbox, and commits it to `.claude/linkedin-outbox/<slug>.md`
  with a `publish_after` time.
- **LinkedIn publisher**, weekdays 16:35 UTC (9:35am PDT, 8:35am PST, always after the 8:30am publish time). Runs `.claude/scripts/linkedin_publish.py`,
  which posts every due outbox file through LinkedIn's Posts API, appends the ledger row and
  deletes the file. Needs `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_URN` in its cloud
  environment; setup and the 60-day token renewal are in `.claude/linkedin-api-setup.md`.

The gap between the companion run and the publisher run is the review window: edit the outbox
file to change a post, delete it and add a ledger row to veto it.

Cloud sandbox facts learned the hard way: the egress proxy blocks cgnarendiran.github.io, so
liveness is checked through the GitHub Pages deployment record; and the Edit and Write tools
prompt for permission on `.claude/` paths, so routines change those files through Bash. Both
jobs run the vendored `humanizer` skill in `.claude/skills/`. `.claude/` is a dot-directory, so
Jekyll never serves any of it.

## Commands

```bash
# What actually works on this machine today:
PATH="$HOME/.gem/ruby/2.6.0/bin:$PATH" JEKYLL_NO_BUNDLER_REQUIRE=true jekyll build
PATH="$HOME/.gem/ruby/2.6.0/bin:$PATH" JEKYLL_NO_BUNDLER_REQUIRE=true jekyll serve
```

**Do not reach for `bundle` here — it is broken.** The Gemfile is unpinned (`gem "jekyll"`),
so `bundle install` resolves to Jekyll 4.x, which needs Ruby >= 3.0; the machine's only Ruby
is the macOS system Ruby 2.6, so it fails on `ffi`. The commands above use a user-installed
Jekyll 3.9.5 outside bundler. Once a modern Ruby exists, the usual `bundle exec jekyll
serve --drafts --incremental` becomes available again.

Note `JEKYLL_NO_BUNDLER_REQUIRE=true` means every plugin in `_config.yml` must be installed
locally or the build fails outright — which is why this site avoids plugins that GitHub Pages
would allow but this machine lacks.

A full build takes ~2.5 minutes. There are no tests, linters, or a JS build step — vendored JS
in `js/vendors/` is committed as-is and SCSS is compiled by Jekyll at request time.

## Content conventions

Both content types share the same front-matter shape; only `layout` differs.

Blog post — `_posts/YYYY-MM-DD-slug.md`, published at `/blog/:title/`:

```yaml
---
layout: post
title:  "ViT - Pixels to Tokens"
date:   2025-11-08
image:  images/blogN/cover.jpg
description: "One sentence about what the post argues. 110-155 characters."
tags: [vision-transformers, computer-vision, transformers]
---
*On the cover: <caption>*
```

Project — `_projects/YYYY-MM-DD-slug.md`, published at `/projects/:title/` (a Jekyll
collection, not posts; the `/projects/` index sorts by `date` descending):

```yaml
---
layout: project
title:  Legal Research Assistant
date:   2025-07-10
image:  images/projectN/cover.png
description: "One sentence about what the project built and for whom."
tags: [rag, retrieval, legal, llms]
---
```

Key points when adding content:

- **Image directories are sequentially numbered, not named after the slug.** The Nth blog
  post lives in `images/blogN/`, the Nth project in `images/projectN/`. A new post takes
  the next free number — check `ls images | grep blog` before creating one. Each directory
  holds a `cover.*` (any of jpg/jpeg/png/webp) plus the post's figures.
- Front-matter `image:` is a repo-relative path (`images/blog27/cover.png`) — it is run
  through `relative_url`, so no leading slash.
- Figures inside post bodies use **root-relative paths**
  (`![descriptive alt](/images/blog27/vla-architecture.png)`), as do cross-links between
  posts (`/blog/<slug>/`). An absolute `https://cgnarendiran.github.io/...` URL fetches from
  the live site during local preview, so a new figure cannot be verified before it ships.
- Alt text describes the image. Never the literal string `alt` — see the style guide §8.
- `tags:` is a YAML flow list drawn from `.claude/tag-vocabulary.md`, 3-6 per document,
  lowercase and hyphenated: `tags: [mixture-of-experts, llms, deepseek]`. A bare
  space-separated string splits on whitespace, so `Mixture of Experts` becomes three tags,
  one of which is `of`.
- `description:` is required on new posts and projects. It is the meta description *and* the
  card excerpt on `/blog/`, `/projects/` and the home page.
- Posts open with the `*On the cover: ...*` caption line, then the opening paragraph. There
  is **no body `# Title`** — the layout renders the front-matter title as the page's `<h1>`,
  so a body `#` produces two `<h1>`s. The first in-body heading is `##`.
- MathJax 2.7 is loaded globally in `_layouts/default.html` with `$...$` for inline and
  `$$...$$` for display math. Prose is written for a technical-but-general audience with
  extended analogies; recent posts form linked series (ViT → VLM → VLA) that cross-link to
  each other with root-relative `/blog/<slug>/` links.

## Layout of the theme

- `_layouts/default.html` — the shell every page wraps in: `head.html`, `header.html`,
  content, `footer.html`, `javascripts.html`, then the MathJax config block.
- `_layouts/post.html` / `project.html` — near-identical; `post.html` keeps the share
  buttons and "Recent posts" widget, `project.html` has them commented out. Disqus and the
  MailChimp newsletter are commented out everywhere and disabled in `_config.yml`.
- `_includes/article-content.html` — the shared card for every index. It expects a `post`
  variable in scope and takes one parameter: `{% include article-content.html style="grid" %}`
  renders the compact two-column card (`.article-card`, cover image on top, no tags), while
  omitting `style` renders the original full-width list row (image floated left, tags, author).
  `/blog/` (paginated, 12 per page via `jekyll-paginate`) and `/projects/` (all, unpaginated)
  use the grid; the generated tag pages still use the list. Card styles live at the bottom of
  `_sass/4-layouts/_home-page.scss`; the two-up layout is just the theme's own grid classes
  (`col-6` desktop, `col-t-12` below 768px), so no new grid system was introduced.
- `_includes/head.html` inlines `_includes/main.scss` through Jekyll's `scssify` filter —
  **there is no separate stylesheet request**. `main.scss` is only a table of contents of
  `@import`s into `_sass/{0-settings,1-tools,2-base,3-modules,4-layouts}`; edit the
  partials there and add an `@import` line if you add a file.
- Top nav is generated from `site.pages` that have a `title` (`about.md`, `resume.md`,
  `_pages/projects.html`, `blog/index.html`), so adding a titled page adds a nav item.
- `search.json` feeds client-side search (`simple-jekyll-search`) and indexes **posts
  only**, not projects.

## Untracked/in-progress files

`_posts/temp.md` is a scratch draft with no front matter — Jekyll will not publish it
(no date-prefixed filename), leave it alone unless asked.
