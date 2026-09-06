# Provenance

Vendored from https://github.com/blader/humanizer (MIT), version 2.2.0 as declared
in `SKILL.md`'s frontmatter. `README.md` is kept alongside because it carries the
upstream MIT licence statement.

Vendored rather than referenced so the weekly blog routine can find it: that job
runs in a fresh cloud sandbox with a git checkout of this repo and no access to a
local `~/.claude/skills/` directory. Project-level skills are discovered from
`.claude/skills/<name>/SKILL.md` in the working tree, so committing it here is what
makes `Skill(humanizer)` resolve during a routine run.

To update: re-download the upstream repo and replace `SKILL.md`, keeping this file.
