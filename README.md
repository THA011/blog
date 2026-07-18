# Prowriters101 — Copywriting & Creative Studio (THA_011)

A marketing blog and portfolio site for **Prowriters101** (signed **THA_011**), a
freelance **copywriting** and creative studio offering copywriting (the core
service), web design, graphic design and academic writing. The brand is
deliberately kept separate from the founder's day job — the founder writes under
the pen-name **Kho Wata**.

> Rebranding is a one-file change: edit `site.name`, `site.signature`,
> `site.author` and `site.email` in `config.yaml`, then rebuild.

It began as a small academic-writing blog and has been scaled into a full,
content-driven marketing site: the blog demonstrates the writing on offer, and
every page funnels toward starting a project.

## How it works

This is a **static site** produced by a small, dependency-light **static site
generator** written in Python. You edit content and configuration; a build step
renders the finished HTML. Nothing is hand-maintained twice — the header, footer
and nav come from one template, and every post is a Markdown file.

```
blog/
├── README.md              Project description, setup, architecture
├── requirements.txt       Build/test dependencies (Jinja2, Markdown, PyYAML, pytest)
├── .gitignore             Ignore venv, caches, build logs
├── config.yaml            Single source of truth: site meta, nav, categories, services, page copy
├── build.py               Entry point — `python build.py` builds the site
├── src/
│   ├── generator/         The generator, split into focused modules
│   │   ├── config.py      Load & validate config.yaml
│   │   ├── content.py     Parse Markdown + YAML frontmatter into Page/Post objects
│   │   ├── renderer.py    Jinja2 environment wrapper
│   │   └── site.py        Orchestrates a full build (+ logging)
│   ├── templates/         Jinja2 templates (base, home, blog, post, page, services, contact)
│   └── assets/            Source CSS & JS (copied to assets/ on build)
├── content/
│   ├── pages/             Prose pages as Markdown (about)
│   └── posts/             Blog posts as Markdown + frontmatter
├── tests/                 pytest suite: config, content parsing, build output, link integrity
├── logs/                  Build logs (gitignored)
└── *.html, assets/        Generated output, served at the repo root (GitHub Pages friendly)
```

### Design principles (mirrored from the structure)

- **Configuration is separate from code.** Nav, categories, services and page
  copy live in `config.yaml`; you never touch HTML to change them.
- **Content is separate from presentation.** Posts are Markdown in
  `content/posts/`; layout is Jinja2 in `src/templates/`.
- **Clean, modular, testable.** The generator is split into small modules, each
  covered by tests, so the project stays easy to maintain and extend.

## Getting started

```bash
# 1. Install dependencies (ideally in a virtualenv)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Build the site (regenerates the HTML at the repo root)
python build.py

# 3. Preview locally
python -m http.server 8000
# then open http://localhost:8000
```

## Adding a blog post

1. Create `content/posts/my-post.md` with frontmatter:

   ```markdown
   ---
   title: "My Post Title"
   category: "copywriting"      # must match a slug in config.yaml
   description: "One-line excerpt shown on cards."
   read_time: "5 min read"
   date: "2026-07-20"
   callout_title: "Want copy like this?"
   callout_text: "Tell me about your project."
   callout_cta: "Start a project"
   ---

   Your article body in **Markdown**.
   ```

2. Run `python build.py`. The post, the blog index and (optionally) the home
   page update automatically.

To feature a post on the home page, add its filename (without `.md`) to
`home.featured` in `config.yaml`.

## Blog categories

Copywriting · Web Design · Graphic Design · Academic Writing · Freelancing
(defined in `config.yaml` and used for the blog's live category filter).

## Testing

```bash
python -m pytest
```

Tests cover config validation, frontmatter/Markdown parsing, the built output
(page counts, category counts, core-service labelling) and local link integrity.

## Deployment

The generated files live at the repo root, so the site can be served as-is by
**GitHub Pages** (root of the branch), Netlify, Cloudflare Pages or any static
host. No server-side code is required.

The contact form uses a `mailto:` handoff so it works on static hosting; it can
be wired to Formspree or Netlify Forms if real submission handling is needed.

## Author & maintainer

Built and maintained by **Mwatha Maina** — writing under the studio brand
**Prowriters101**, signed **THA_011**. The brand is deliberately kept separate
from my day-to-day name so the site stays focused on freelance work; this section
is the developer-facing record of who owns the repo.

| | |
|---|---|
| **Maintainer** | Mwatha Maina (`THA_011`) |
| **GitHub** | [github.com/THA011](https://github.com/THA011) |
| **LinkedIn** | [mwatha-maina](https://www.linkedin.com/in/mwatha-maina-a44146238) |
| **Email** | [mwaszac2@gmail.com](mailto:mwaszac2@gmail.com) |
| **Academic** | [maina.mwatha@students.jkuat.ac.ke](mailto:maina.mwatha@students.jkuat.ac.ke) |

## Client contact (public brand)

For project enquiries, the site points clients to the studio:
**Prowriters101** — [Prowriters101@gmail.com](mailto:Prowriters101@gmail.com)

## License

© Mwatha Maina (Prowriters101 · THA_011). All rights reserved. The code is a
personal project; please ask before reusing the content or brand.
