# Md Bodrud-Doza, PhD

Academic website of a Postdoctoral Scholar at the University of Guelph. REAL Decision Lab is a developing research program connecting agricultural landscapes, water quality, and environmental decisions.

[Visit the website](https://bdzion.github.io/) · [Research Lab](https://bdzion.github.io/research.html) · [Publications](https://bdzion.github.io/publications.html) · [Academic CV](https://bdzion.github.io/cv.html)

The active Mitacs Accelerate project works with Healthy Lake Huron partners; Ausable Bayfield Conservation Authority (ABCA) is the formal Mitacs partner. Earth observation, GeoAI, and food-system resilience are developing research directions.

Start with [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) for beginner-friendly editing, publication cards, photos, status wording, checks, deployment, and rollback instructions.

Live site: https://bdzion.github.io

## Edit the website

Each page is a separate Quarto Markdown file. Edit text in `index.qmd`, `research.qmd`, `research-journey.qmd`, `experience.qmd`, `publications.qmd`, `cv.qmd`, `collaboration.qmd`, or `contact.qmd`. Navigation, site metadata, and footer links are in `_quarto.yml`; colours, spacing, and responsive layout are in `styles.css`.

You can edit these files directly on GitHub. Use a new branch and pull request for every edit. Review the passing build before merging; merging to `main` publishes automatically. Pull requests build and check without deploying.

## Add a publication

Edit `publications.json`, the single source for the publication page and homepage featured papers. Copy an existing object and give it a unique `id`. Supply the citation, category, year (or `null`), DOI (or `null`), URL (or `null`), `first_authored`, `featured`, and `topics`. For featured entries also supply a `title`; optional `journal`, `contribution`, and `display_tags` improve the compact cards. Use exact publication metadata and DOI links, and do not invent missing fields.

Categories follow the supplied CV: First-Authored Articles, Co-Authored Articles, Book Chapters, Working Papers, Conference Abstracts, Technical Reports and Policy Contributions, Policy Brief, and Selected Public and Policy Writing. Topic tags are editorial browsing aids based on the supplied titles, not claims that every tagged paper uses each method. Earth observation and GeoAI remain developing directions.

`python scripts/render_publications.py` regenerates the HTML includes. Quarto runs this automatically before every render, so do not edit the generated publication includes directly. Entries remain readable when JavaScript is disabled; JavaScript adds search and topic/authorship/year/category/view filters. Exact totals are not used as profile metrics.

## Replace or update the CV

The manually reviewed `assets/Md_Bodrud_Doza_Academic_CV.pdf` is the canonical download. The owner's finalized eight-page PDF, supplied 9 October 2026, is published unchanged using this stable filename. Update the master document outside the repository, export/review every page, then replace the PDF through a pull request. Update the web summaries and `publications.json` separately when facts change; Quarto does not regenerate the CV.

The stale `assets/cv-content.json` was removed. `scripts/build_cv.py` is a retired entry point that stops without writing a file, preventing accidental replacement of the final PDF. See maintenance guide section J. No PDF-generation library is needed.

Never upload a private CV, home address, phone number, immigration or family details, or referee contacts. The current photo policy permits the homepage portrait, research-only journey image, and one professional consultation photograph on Experience. Audit text, links, metadata, and embedded content before publishing. Only institutional contact details belong on this site. Original Word documents are deliberately excluded from this repository.

## Replace photos or add research projects

The portrait is `assets/portrait.webp`; the social-sharing image is `assets/social-preview.png`. Use compressed derivatives with EXIF metadata removed. Update image alt text and size attributes when replacing them. Add research project text to `research.qmd`, with a clear distinction between completed work and developing ideas. Do not imply the REAL Decision Lab is a staffed established lab. Keep the portrait, journey, and single leadership photograph policy; replace the existing derivative when a photo needs updating. Do not upload sensitive datasets.

## Preview locally

Install Python 3 and Quarto 1.10.19, then from this folder:

```sh
quarto preview
```

To build and check:

```sh
quarto render
python -m unittest discover -s tests
python scripts/check_site.py
```

The publication renderer and site checker use only the Python standard library. The canonical CV is a separately reviewed upload. The rendered `_site/` directory and Quarto cache are ignored by Git.

## Deployment

`.github/workflows/publish.yml` renders on GitHub Actions, checks local links and document structure, uploads `_site`, and deploys through the official GitHub Pages action. Repository Settings → Pages → Source must be **GitHub Actions**. No personal access token or extra secret is required. The deployment job requests only `pages: write` and `id-token: write`; repository content is read-only in the workflow. Check the Actions tab for progress or failures. A successful deployment publishes https://bdzion.github.io.

## Custom domain later

First obtain a domain and configure its DNS using GitHub's current custom-domain documentation. Add it in Settings → Pages → Custom domain, update `website.site-url` in `_quarto.yml`, and ensure HTTPS is enabled. If using a `CNAME` file, add it as a project resource. See https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site.

## Content conventions

The supplied Website Content document controlled the public wording and research framing. The public academic CV supplied the historical record. The postdoctoral appointment begins September 2026, as confirmed by the owner. Publication and citation totals are omitted as headline metrics; Google Scholar provides current citation information. The site uses Canadian prose conventions while preserving published titles. There is no analytics or tracking code and no third-party font dependency. This is a personal research website and does not use official university branding.

## Research and teaching content

The Research Lab tab leads to the prominent REAL Decision Lab page. `updates.json` supplies the dated homepage Updates list through `scripts/render_updates.py`. The current Mitacs project was confirmed active by the owner; the CPRA direction remains submitted. Teaching approach, supported courses, future interests, and two selected evaluation quotes are in Experience. The journey derivative is `assets/images/journey/research-journey.webp`, from `ResearchJourney - only.jpg`. One professional consultation photograph appears in Experience as `assets/images/experience/leadership-consultation.webp`. See the maintenance guide for updating areas, the return loop, project status, Updates, teaching, and the journey photo.

## Academic website refinement

Research Lab uses OBSERVE → UNDERSTAND → PLAN → DECIDE & LEARN, with a five-step adaptive return loop. Five project cards in `research.qmd` separate active Mitacs research, the PhD foundation, the submitted OMAFA proposal, emerging Earth observation/GeoAI, and the submitted CPRA direction. `updates.json` retains news records; the renderer displays only the two newest. Experience groups academic/applied research and climate/development/leadership, with teaching kept on the same page. Featured publication cards retain exact titles and show journal/year before the contribution. The web CV is a concise overview with one main download button. The publication system and Quarto/GitHub Pages architecture are preserved. Shared links use a landscape preview and page-specific search metadata; deployment is restricted to the main branch.

The publication timeline uses journal articles and book chapters for its overlapping domain bands, followed by selected DOI-linked milestones. The complete record and filters still include all output categories. Featured contributions explain the studies' findings or methods without changing formal titles/citations. The supplied lab logo appears only beside the Research Lab name. Collaboration has compact section shortcuts and concise proposal wording.

Main protection was absent when checked on 9 October 2026. The GitHub connection cannot administer rules. Follow maintenance guide section T to require PRs and the `build` check and disable force pushes/deletion; repository visibility is unchanged.
