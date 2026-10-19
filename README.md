<p align="center">
  <a href="https://cgnarendiran.github.io">
    <img src="images/cg_logo.png" alt="CG, the teal circle logo of cgnarendiran.github.io" width="120">
  </a>
</p>

<h1 align="center">Narendiran Chembu</h1>

<p align="center">
  <em>Trying to understand this resplendent chaos called life.</em>
</p>

<p align="center">
  Staff Machine Learning Engineer at <a href="https://www.fastcode.ai/">fastcode.ai</a>.
  Long-form explainers on how machine learning actually works.
</p>

<p align="center">
  <a href="https://cgnarendiran.github.io"><img alt="Website" src="https://img.shields.io/badge/website-cgnarendiran.github.io-008080?style=flat-square"></a>
  <a href="https://cgnarendiran.github.io/blog/"><img alt="Blog" src="https://img.shields.io/badge/blog-read-008080?style=flat-square"></a>
  <a href="https://cgnarendiran.github.io/projects/"><img alt="Projects" src="https://img.shields.io/badge/projects-browse-008080?style=flat-square"></a>
  <a href="https://linkedin.com/in/cgnarendiran/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-cgnarendiran-008080?style=flat-square"></a>
  <a href="https://github.com/cgnarendiran"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-cgnarendiran-008080?style=flat-square&logo=github"></a>
  <a href="mailto:cgnarendiran@gmail.com"><img alt="Email" src="https://img.shields.io/badge/email-cgnarendiran%40gmail.com-008080?style=flat-square&logo=gmail&logoColor=white"></a>
</p>

---

## About me

Hello! I'm Naren, though most people know me as CG (which inspired the logo). I hold a Master's
degree in Artificial Intelligence from [University of Amsterdam](https://www.uva.nl) and a
Bachelor's in Mechanical Engineering from [IIT Madras](https://www.iitm.ac.in/).

Currently, I'm a Staff Machine Learning Engineer at [fastcode.ai](https://www.fastcode.ai/),
working at the intersection of causal reasoning and autonomous driving. I recently authored
CausalDriveBench, a benchmark that asks whether driving vision-language-action models actually
reason about cause and effect or just pattern-match — across thirteen models, the answer leaned
firmly toward pattern-matching. I'm now building action-conditioned world models for ADAS with
[Renesas](https://www.renesas.com/), and I've previously worked with clients like Mercedes-Benz
and Aramco on in-cabin perception and industrial automation.

Over the past decade I've shipped AI systems across robotics, manufacturing, oil and gas, speech,
automotive, healthcare, and legal - from field robots and flight stacks to reinforcement learning
on factory floors and retrieval systems over half a million case files. Working across that many
domains has taught me the part that transfers: how to find the real problem underneath a stated
one, and how to tell which of them AI can actually solve.

When I'm not diving into the latest AI developments, you'll find me strumming my ukulele or
strategizing my next chess move.

## On the site

**[The blog](https://cgnarendiran.github.io/blog/)** has been running since 2017. Each post
explains how one thing works, with the real numbers, the ablation that proves the claim, and one
everyday picture carried from the first line to the last. Several posts run as series:

- **Is Attention All You Really Need?** [KV caching & MLA](https://cgnarendiran.github.io/blog/kv-caching-mla-is-attention-all-you-really-need/), [RoPE](https://cgnarendiran.github.io/blog/rope-is-attention-all-you-really-need/), [MoE](https://cgnarendiran.github.io/blog/moe-is-attention-all-you-really-need/), [speculative decoding](https://cgnarendiran.github.io/blog/speculative-decoding/), [Mamba](https://cgnarendiran.github.io/blog/mamba-is-attention-all-you-really-need/)
- **Pixels to Tokens.** [ViT](https://cgnarendiran.github.io/blog/vit-pixels-to-tokens/) → [VLMs](https://cgnarendiran.github.io/blog/vlm-pixels-to-tokens/) → [VLAs](https://cgnarendiran.github.io/blog/vla-pixels-to-tokens/)
- **Predicting the world.** [JEPA](https://cgnarendiran.github.io/blog/jepa-nobody-cares-about-the-wallpaper/), [LeJEPA](https://cgnarendiran.github.io/blog/lejepa/), [world models](https://cgnarendiran.github.io/blog/world-models-learned-simulators/)
- **Search and games.** [Solving chess](https://cgnarendiran.github.io/blog/solving-chess-paths-nodes/), [MCTS and AlphaZero](https://cgnarendiran.github.io/blog/mcts-alphazero/)
- **Voice models.** [From sound to tokens](https://cgnarendiran.github.io/blog/voice-models-sound-to-tokens/), [holding a conversation](https://cgnarendiran.github.io/blog/voice-models-holding-a-conversation/)

**[Projects](https://cgnarendiran.github.io/projects/)** are write-ups of things I've built, from an
autonomous ground vehicle and fixed-wing swarms to reinforcement learning for semiconductor fabs and a
legal research assistant. Every post and project is tagged, and
[/tags/](https://cgnarendiran.github.io/tags/) lists them all.

---

## How it's built

Jekyll, deployed by GitHub Pages straight from `master`. **There is no CI workflow, so pushing
to `master` publishes the site.** Content changes go through a pull request.

- Markdown is rendered by **kramdown**; math by **MathJax 2.7.9** with SVG output
- Blog posts live in `_posts/`, published at `/blog/:title/`, paginated 12 to a page
- Projects are a Jekyll **collection** in `_projects/`, published at `/projects/:title/`
- Styles are SCSS under `_sass/`, inlined into `<head>` at build time, so there is no separate
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

There are no tests and no linters.

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
description: "One sentence about what the post argues. 110-155 characters."
tags: [jepa, self-supervised-learning, world-models, representation-learning]
---
*On the cover: a police sketch in progress*
```

A few conventions that are easy to get wrong:

- **Image directories are numbered, not named.** The Nth post uses `images/blogNN/`, the Nth
  project `images/projectNN/`. Check `ls images | grep blog` before creating one.
- **Covers are real images**, found on Wikimedia Commons with `.claude/scripts/commons_cover.py`
  and credited in the `*On the cover:*` line. Pick one that looks good at card size.
- `image:` is repo-relative with no leading slash. Body figures use **root-relative** paths
  (`/images/blog28/foo.png`), as do cross-links between posts (`/blog/<slug>/`). An absolute
  URL would fetch from the live site during local preview.
- Alt text describes the image; never the literal string `alt`.
- `tags:` is a YAML flow list drawn from `.claude/tag-vocabulary.md`, 3-6 per post,
  lowercase and hyphenated. A bare space-separated string splits on whitespace, so
  `Self-Supervised Learning` would become two tags.
- `description:` is required. It is the meta description and the card excerpt.
- **Display math is `$$ ... $$`.** Not `\[ \]`, because kramdown strips the backslash before
  MathJax sees the page. Inline is `$...$`, which also means a dollar sign followed by a digit
  turns into math: write prices in words.

## Tags

Tags resolve to `/tags/#<tag>`, a single plugin-free index page. The site previously used
`jekyll/tagging`, which is not on the GitHub Pages plugin allowlist. It was skipped on the live
build, so every `/tag/<tag>/` page 404'd in production while resolving locally. The vocabulary
is in `.claude/tag-vocabulary.md`.

## Automation

`.claude/` holds the config for four scheduled Claude Code routines. Each one works from
`origin/master`, opens a pull request, checks it and merges it:

- the **blog job** writes the next post from a topic queue on Sundays and Wednesdays;
- a **same-day job** writes part 2 when the queue says a series ships both parts together;
- the **LinkedIn companion job** writes a short plain-language post for each new blog post;
- the **LinkedIn publisher** posts those through LinkedIn's API.

That directory also holds the writing and LinkedIn style guides, a prose lint, the image
scripts and a vendored editing skill. None of it is ever served: Jekyll ignores dot-directories,
which is deliberate.

---

## Credits

Built on the [**Reked**](https://github.com/artemsheludko/reked) Jekyll theme by
[Artem Sheludko](https://github.com/artemsheludko), MIT licensed, and adapted since. The card
grid, the projects collection, MathJax support and the SCSS are all local changes. This README
replaces the theme's original one; see `LICENSE.txt`.
