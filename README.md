# cgnarendiran.github.io

The personal site of **Narendiran Chembu** — a technical blog and a project portfolio.

**Live at [cgnarendiran.github.io](https://cgnarendiran.github.io)**

Mostly long-form explainers on machine learning: how a thing actually works, with the real
numbers, the ablation that proves the claim, and one extended metaphor carried from the first
line to the last. 27 posts since 2017, plus 14 project write-ups.

Several run as series:

- **Pixels to Tokens** — [ViT](https://cgnarendiran.github.io/blog/vit-pixels-to-tokens/) → [VLMs](https://cgnarendiran.github.io/blog/vlm-pixels-to-tokens/) → [VLAs](https://cgnarendiran.github.io/blog/vla-pixels-to-tokens/) → [JEPA](https://cgnarendiran.github.io/blog/jepa-nobody-cares-about-the-wallpaper/)
- **Is Attention All You Really Need?** — [KV Caching & MLA](https://cgnarendiran.github.io/blog/kv-caching-mla-is-attention-all-you-really-need/), [RoPE](https://cgnarendiran.github.io/blog/rope-is-attention-all-you-really-need/), [MoE](https://cgnarendiran.github.io/blog/moe-is-attention-all-you-really-need/)

## How it's built

Jekyll, deployed by GitHub Pages straight from `master` — **there is no CI workflow, so pushing
to `master` publishes the site.** Content changes go through a pull request.

- Markdown is rendered by **kramdown**; math by **MathJax 2.7.9** with SVG output
- Blog posts live in `_posts/`, published at `/blog/:title/`, paginated 12 to a page
- Projects are a Jekyll **collection** in `_projects/`, published at `/projects/:title/`
- Styles are SCSS under `_sass/`, inlined into `<head>` at build time — there is no separate
  stylesheet request and no JS build step

```
_posts/        blog posts             _sass/      SCSS partials
_projects/     project write-ups      _layouts/   page shells
_pages/        standalone pages       _includes/  shared partials
images/        blogNN/ and projectNN/ .claude/    automation config (never served)
```

## Running it locally

```bash
bundle install                # first time, or after Gemfile changes
bundle exec jekyll serve      # http://localhost:4000, rebuilds on save
bundle exec jekyll build      # output to _site/ (gitignored)
```

A full build takes roughly 30 seconds. There are no tests and no linters.

**Ruby version caveat.** The Gemfile is unpinned, so `bundle install` resolves to Jekyll 4.x,
which needs Ruby >= 3.0. macOS ships Ruby 2.6, on which `bundle install` fails building `ffi`.
Until a modern Ruby is installed, build with a user-installed Jekyll 3.9.5 outside bundler:

```bash
PATH="$HOME/.gem/ruby/2.6.0/bin:$PATH" JEKYLL_NO_BUNDLER_REQUIRE=true jekyll build
```

## Writing a post

```yaml
---
layout: post
title:  "JEPA - Nobody Cares About the Wallpaper"
date:   2026-09-05
image:  images/blog28/cover.jpg
tags:  JEPA Self-Supervised Learning World Models
---
*On the cover: a police sketch in progress*
```

A few conventions that are easy to get wrong:

- **Image directories are numbered, not named.** The Nth post uses `images/blogNN/`, the Nth
  project `images/projectNN/`. Check `ls images | grep blog` before creating one.
- `image:` is repo-relative with no leading slash. Body figures use the **absolute production
  URL**, so they won't render locally until pushed.
- `tags:` is a bare space-separated list — each word becomes its own tag, not a YAML array.
- **Display math is `$$ ... $$`.** Not `\[ \]` — kramdown strips the backslash before MathJax
  sees the page. Inline is `$...$`.

## Known gap: tag pages 404 in production

`_config.yml` enables `jekyll/tagging`, which is **not** on the GitHub Pages plugin allowlist,
so it is silently skipped on the live build. All 130 `/tag/<tag>/` pages generate locally and
return 404 in production, which means every tag link on a post page is dead. Fixing it needs a
GitHub Actions build, or dropping the plugin. Don't assume tag links work because they resolve
on a local server.

## Automation

`.claude/` holds the config for a scheduled agent that drafts one post a week and opens it as a
pull request — a topic queue, a writing style guide, and a vendored editing skill. Nothing in
that directory is ever served: Jekyll ignores dot-directories, which is deliberate.

---

## Credits

Built on the [**Reked**](https://github.com/artemsheludko/reked) Jekyll theme by
[Artem Sheludko](https://github.com/artemsheludko), MIT licensed, and adapted since — the card
grid, the projects collection, MathJax support and the SCSS are all local changes. This README
replaces the theme's original one; see `LICENSE.txt`.
