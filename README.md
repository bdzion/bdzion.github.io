# bdzion.github.io
Academic website of Md Bodrud-Doza.

Start with [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) for beginner-friendly editing, publication cards, photos, status wording, checks, deployment, and rollback instructions.

Live site: https://bdzion.github.io

## Edit the website

Each page is a separate Quarto Markdown file. Edit text in `index.qmd`, `research.qmd`, `research-journey.qmd`, `experience.qmd`, `publications.qmd`, `cv.qmd`, `collaboration.qmd`, or `contact.qmd`. Navigation, site metadata, and footer links are in `_quarto.yml`; colours, spacing, and responsive layout are in `styles.css`.

You can edit these files directly on GitHub. Commit to `main` to publish automatically. Pull requests build and check the website without deploying it.

## Add a publication

Edit `publications.json`, the single source for the publication page and homepage featured papers. Copy an existing object and give it a unique `id`. Supply the citation, category, year (or `null`), DOI (or `null`), URL (or `null`), `first_authored`, `featured`, and `topics`. For featured entries also supply a `title`; optional `journal`, `contribution`, and `display_tags` improve the compact cards. Use exact publication metadata and DOI links, and do not invent missing fields.

Categories follow the supplied CV: First-Authored Articles, Co-Authored Articles, Book Chapters, Working Papers, Conference Abstracts, Technical Reports and Policy Contributions, Policy Brief, and Selected Public and Policy Writing. Topic tags are editorial browsing aids based on the supplied titles, not claims that every tagged paper uses each method. Earth observation and GeoAI remain developing directions.

`python scripts/render_publications.py` regenerates the HTML includes. Quarto runs this automatically before every render, so do not edit `_includes/*.html` directly. Entries remain readable when JavaScript is disabled; JavaScript adds search and topic/authorship/year/category/view filters. Exact totals are not used as profile metrics.

## Replace or update the CV

Replace `assets/Md_Bodrud_Doza_Academic_CV.pdf` with a reviewed public-safe PDF using the same filename. The links then keep working. Alternatively edit `assets/cv-content.json`, install ReportLab (`python -m pip install reportlab`), and run `python scripts/build_cv.py`. Review every PDF page after rebuilding. The CV JSON is a separate editable CV source; also update its publication section when adding publications to the website.

Never upload a private CV, home address, phone number, immigration or family details, or referee contacts. The journey collage is an explicitly owner-approved personal-photo exception; do not add further private family details. Audit text, links, metadata, and embedded content before publishing. Only institutional contact details belong on this site. Original Word documents are deliberately excluded from this repository.

## Replace photos or add research projects

The portrait is `assets/portrait.webp`; the social-sharing image is `assets/social.jpg`. Use compressed derivatives with EXIF metadata removed. Update image alt text and size attributes when replacing them. Add research project text and images to `research.qmd`, with a clear distinction between completed work and developing ideas. Do not imply the REAL Decision Lab is a staffed established lab. Place new images under `assets/images/` and list them under `project.resources` in `_quarto.yml` if needed. Do not upload sensitive datasets.

## Preview locally

Install Python 3 and Quarto 1.10.19, then from this folder:

```sh
quarto preview
```

To build and check:

```sh
quarto render
python scripts/check_site.py
```

The publication renderer and site checker use only the Python standard library. ReportLab is needed only when rebuilding the CV PDF. The rendered `_site/` directory and Quarto cache are ignored by Git.

## Deployment

`.github/workflows/publish.yml` renders on GitHub Actions, checks local links and document structure, uploads `_site`, and deploys through the official GitHub Pages action. Repository Settings → Pages → Source must be **GitHub Actions**. No personal access token or extra secret is required. The deployment job requests only `pages: write` and `id-token: write`; repository content is read-only in the workflow. Check the Actions tab for progress or failures. A successful deployment publishes https://bdzion.github.io.

## Custom domain later

First obtain a domain and configure its DNS using GitHub's current custom-domain documentation. Add it in Settings → Pages → Custom domain, update `website.site-url` in `_quarto.yml`, and ensure HTTPS is enabled. If using a `CNAME` file, add it as a project resource. See https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site.

## Content conventions

The supplied Website Content document controlled the public wording and research framing. The public academic CV supplied the historical record. The postdoctoral appointment begins September 2026, as confirmed by the owner. Publication and citation totals are omitted as headline metrics; Google Scholar provides current citation information. The site uses Canadian prose conventions while preserving published titles. There is no analytics or tracking code and no third-party font dependency. This is a personal research website and does not use official university branding.
