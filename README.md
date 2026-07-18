# Mwatha Maina — Copywriting & Creative Studio (Blog)

A marketing blog and mini-site for **Mwatha Maina**, freelance copywriter and creative.
It began as an academic-writing blog; it's now scaled into a lead-generating site for a
freelance copywriting business, with supporting services in web design, graphic design and
academic writing.

## Purpose

The blog is a marketing engine: each article gives readers something useful *and*
demonstrates the writing/design skills clients can hire. Every page funnels toward one
action — starting a project.

## Structure

```
index.html          Home — value proposition, services snapshot, featured posts, CTA
blog.html           Blog index with client-side category filtering
services.html       The four services + how we work together
about.html          Positioning and story (academic roots → copywriting)
contact.html        Enquiry form (mailto-based) + how to get in touch
styles.css          Design system (variables, components, responsive)
script.js           Mobile nav, category filtering, footer year, contact form
posts/              Individual articles
  copywriting-that-converts.html
  website-copy-that-sells.html
  web-design-that-converts.html
  design-that-communicates.html
  pricing-copywriting-projects.html
  clear-argument.html            (academic — original, upgraded)
  reproducible-research.html     (academic — original, upgraded)
```

## Content categories

Copywriting (core), Web Design, Graphic Design, Academic Writing, Freelancing.
The blog index filters posts by these categories.

## Tech

Plain, dependency-free static HTML/CSS/JS — no build step. Works on any static host
(GitHub Pages, Netlify, etc.).

## Run locally

Open `index.html` directly, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deploy

Push to a static host. For GitHub Pages, enable Pages on the default branch — the site is
served as-is from the repo root.

## Contact

Mwatha Maina — mwaszac2@gmail.com
