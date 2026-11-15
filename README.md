# www.blahfe.com

Public website for Blahfe & Grpr (https://www.blahfe.com/).

## Structure

- `content/`: Public Markdown content (`page/*.md` for static pages, `space/knowledge/README.md` for the knowledge index, `space/knowledge/*.md` for knowledge articles, and `space/knowledge/blog/*.md` for blog posts).
- `assets/`: Images (`design/`, `attachments/`, `blog/`), fonts, CSS, and `site.js`.
- `templates/`: HTML templates for static pages (`home`, `vision`, `member`, `contact`, `knowledge`) and the shared header and footer.
- `scripts/build.py`: Static site generator that renders Markdown and templates into HTML, search index, and sitemap.
- `docs/`: GitHub Pages publish directory (generated output is committed to the repository).

## Build & Update

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
python3 -m http.server 8000 --directory docs
```

- Edit knowledge articles and blog posts in `content/`, or update static page layouts and copy in both `templates/` and the corresponding `content/` Markdown files, then run `scripts/build.py` and commit the regenerated `docs/` directory together with the source changes.
- Running `build.py` with no arguments outputs canonical URLs for `https://www.blahfe.com/`, `docs/CNAME`, `docs/search-index.json`, `docs/sitemap.xml`, and `docs/404.html`.
- Knowledge search, tree expansion, and blog pagination are handled by `assets/site.js`. The blog displays 30 posts per page and navigates via `Prev`, page number, and `Next` links (`?page=`).
- GitHub Pages serves `/docs` from the `master` branch of this repository (`blahfe/www.blahfe.com`). Merging into `master` publishes changes directly.

## Custom Domain (DNS)

The authoritative Route 53 hosted zone is `Z052732628FNUHCOJ247C` in the Infrastructure account (`158393879384`), delegated to `ns-218.awsdns-27.com`, `ns-1645.awsdns-13.co.uk`, `ns-1347.awsdns-40.org`, and `ns-635.awsdns-15.net`. The `Z05416883ATWMHT2BYQGW` zone in CorporateSite shares the same domain name but is not delegated and should not be used.

- `www`: `CNAME blahfe.github.io.`
- apex (`blahfe.com`): GitHub Pages `A` records (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`) and `AAAA` records (`2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`). Because the custom domain is configured as `www.blahfe.com`, requests to the apex redirect to `www`.
- `MX`, `TXT`, `DKIM`, `mail`, and `autodiscover` records are used for email and must not be modified.

## Display Specifications

- The header navigation remains visible across all viewport widths over a transparent background sharing the top 500px banner image.
- To prevent dark-mode browser extensions (such as Night Eye) from altering colors or overriding CSS backgrounds, pages set `html[nighteye="disabled"]`, apply inverse filter compensation on background images, and place a matching `#0086ea` decorative SVG behind the services section.
