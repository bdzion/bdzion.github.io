# Maintaining your academic website

Your live site is https://bdzion.github.io. The source repository is `bdzion/bdzion.github.io`. You edit source files; GitHub builds and publishes the pages automatically.

## A. Edit text directly on GitHub

1. Open the repository **Code** tab and a page file, such as `research.qmd`.
2. Click the pencil (**Edit this file**). Edit below the opening `---` metadata block. Keep surrounding HTML tags, quotation marks, and links intact.
3. Click **Commit changes** with a clear description. Routine corrections can go to `main`; substantial edits should use a new branch and pull request.
4. Open **Actions**, wait for a green deployment, and check the live page. A pull request builds but does not publish before merging.

Page map: `index.qmd` = Home; `research.qmd` = Research Lab; `research-journey.qmd` = Journey; `experience.qmd` = Experience; `publications.qmd` = Publications introduction; `cv.qmd` = web CV; `collaboration.qmd` = Collaboration; `contact.qmd` = Contact. Navigation and metadata live in `_quarto.yml`; appearance lives in `styles.css`.

## B. Update the current position and homepage

Edit the appointment and affiliation in `index.qmd`, then the corresponding entries in `experience.qmd`, `cv.qmd`, and `assets/cv-content.json`. The confirmed Postdoctoral Scholar start is **September 2026**. Follow J to update the PDF separately. Keep the homepage's direction cards brief and label emerging work clearly. Link to Scholar for current metrics rather than adding fixed publication/citation totals.

### Homepage Updates


1. Edit `updates.json`. Copy one complete object, keeping commas between objects.
2. Supply `date` as `YYYY-MM-DD`, plus `type`, `publisher`, `title`, a brief original `summary`, and the public HTTPS `url`.
3. Verify the title and publication date at the publisher. Do not confuse the article date with the date you add it.
4. The homepage automatically shows only the two newest entries, sorted by their verified publication dates. Older entries can remain in `updates.json`; they are preserved but not shown in the homepage list.
5. Render and check the links. Do not edit `_includes/updates.html`; `scripts/render_updates.py` regenerates it.

## C. Update the four Research Lab areas


1. Open `research.qmd` on GitHub and click Edit.
2. Find `<div class="framework research-framework">`. Each `<li id="area-...">` contains an action label (OBSERVE, UNDERSTAND, PLAN, DECIDE & LEARN), an area title, a plain-language question, and a short explanation.
3. Edit those words while preserving the four IDs (`area-observe`, `area-understand`, `area-design`, `area-learn`). The return link relies on the first ID.
4. Keep GeoAI and Earth observation described as growing directions below the framework. Commit, check Actions, then inspect desktop and phone layouts.

## D. Maintain the learning loop


Find `<div class="learning-loop">` in `research.qmd`. Edit the five `<li>` steps in `<ol class="loop-steps">` and the SVG `<title id="loop-title">` together so the accessible description agrees with the diagram. Keep the order: Monitor outcomes → Compare results with expectations → Learn → Update models and priorities → Observe again. Keep the arrow path and return-link destination unchanged unless you are redesigning the framework.

## E. Update the current Mitacs project


The owner confirmed on 7 October 2026 that Mitacs is the current postdoctoral project. In `research.qmd`, find “Current project: Healthy Lake Huron”. Keep intended outputs distinct from completed findings. ABCA is the formal Mitacs partner; MVCA and other Healthy Lake Huron participants are the wider data/collaboration context. Update the related short entry in `experience.qmd` and “Current applied collaboration” in `collaboration.qmd` together. Do not upload the source proposal or private partner data. Confirm any change to partner roles, dates, or project status before editing.

### Edit project cards and status

1. Open `research.qmd` and find “Current and developing projects” and `<div class="project-grid">`.
2. Each `<article class="project-card">` contains a status label, title, one short explanation, and sometimes a link.
3. Edit these words and check the linked section. Keep statuses precise: Active, PhD foundation, Developing, or Submitted proposal / Developing.
4. A submitted proposal becomes awarded or active only after confirmation. Update Research Lab, Experience, Collaboration, and the web CV together where relevant.
5. Keep methods described as emerging when they are still being developed. Render and inspect the cards on a phone.

## F. Replace the journey photo


1. Start from `ResearchJourney - only.jpg`, keeping the complete frame and original aspect ratio.
2. Export a compressed WebP with EXIF/GPS metadata removed; use the existing derivative filename.
3. Replace `assets/images/journey/research-journey.webp` on GitHub.
4. Update its width/height, alt text, and caption in `research-journey.qmd` and the inventory in `assets/images/manifest.json`.
5. Confirm the three phase panels remain visible without clicking. Run the site check: it enforces the portrait/journey/one-leadership-image policy.

The site photos are the homepage portrait, this journey image, and one professional consultation image on Experience. Keep originals outside the repository. Do not add galleries or personal/family photographs.

## G. Add a publication

Edit `publications.json`. Copy a complete record and give it a unique ID. Add a comma between neighbouring objects, retain the surrounding `[` and `]`, use double quotes, and avoid trailing commas. Example:

```json
{
  "id": "pub-089",
  "category": "First-Authored Articles",
  "citation": "Exact complete published citation.",
  "year": 2027,
  "doi": "10.xxxx/exact-doi",
  "url": "https://doi.org/10.xxxx/exact-doi",
  "first_authored": true,
  "featured": false,
  "topics": ["Water Quality & Watershed Science"]
}
```

Replace all example values with verified metadata. Use `null` for an unavailable year, DOI, or URL. Reuse existing categories: First-Authored Articles, Co-Authored Articles, Book Chapters, Working Papers, Conference Abstracts, Technical Reports and Policy Contributions, Policy Brief, or Selected Public and Policy Writing. Keep non-peer-reviewed work in the proper category. Topics should describe the paper accurately.

Do not edit `_includes/*.html`; rendering regenerates them. The PDF source is separate, so also add new citations to `assets/cv-content.json` when updating your CV.

## H. Mark or unmark featured papers

Set `"featured": true` or `false`. Cards follow JSON order; Home displays the first three featured papers. Supply `title` for featured records. Optional card fields are:

```json
"title": "Exact published title",
"journal": "Journal name",
"contribution": "One accurate sentence about the contribution.",
"display_tags": ["Precision conservation", "Machine learning"]
```

Use two or three short display tags; `topics` still drives filtering. Retain the full `citation`. Featured cards show title, journal/year, one contribution sentence, tags, and paper link. The full citation appears only in the complete record. Update the separate research-arc text in `publications.qmd` when needed.

## I. Update the publication research arc


“How the research program developed” is a four-step overview in `publications.qmd`, separate from the full JSON record. Edit the years and short step descriptions together. Preserve published titles in `publications.json`; do not silently rename a paper to fit the arc.

## J. Update the public CV PDF safely

Use **Add file → Upload files** inside `assets` to replace `Md_Bodrud_Doza_Academic_CV.pdf` with a reviewed public PDF using the same filename. Alternatively edit `assets/cv-content.json`, install ReportLab locally, and run `python scripts/build_cv.py`.

Review every page and link after rebuilding. Remove private phone numbers, home addresses, immigration details, referee contacts, hidden comments, and private metadata. Use institutional contact details only. Never upload the original private Word CV. Test the live download. Editing `cv.qmd` alone does not update the PDF.

### Edit professional experience

1. In `experience.qmd`, find “Academic & Applied Research” or “Climate, Development & Leadership”.
2. Each timeline `<article>` contains dates, role title, institutional link, and a short contribution description.
3. Update those fields together using your verified records. Keep institutional links official; Ispahani Agro uses `https://ispahaniagro.com/`.
4. Retain short paragraphs; the full CV holds the detailed record. Check that a role remains in the appropriate group.

### Maintain the single leadership photograph

1. The current source is `E:\Z_website\Pictures\Leadership and science–policy practice1.jpg`. Only one photograph is used in this section.
2. Export a compressed WebP with metadata removed, preserving the full frame and original aspect ratio.
3. Replace `assets/images/experience/leadership-consultation.webp` using **Add file → Upload files** inside that repository folder.
4. Update its width, height, alt text, and caption in the Experience `leadership-panel`, plus `assets/images/manifest.json`.
5. Use a caption supported by your records. Do not infer names, dates, organisations, or event details from an image alone. Keep the photograph relevant to leadership, engagement, or science–policy practice.
6. Run the checks and view Experience on desktop and phone. Adding a gallery violates the current image policy and will fail the check.

## K. Maintain teaching and selected feedback


The main teaching account lives in `experience.qmd#teaching-and-mentoring`; the web CV links there. Keep documented GTA responsibilities distinct from future teaching interests and goals. Replace quotes only with accurately attributed feedback from your own evaluations. The sample teaching dossier is a structural reference; its courses, certifications, syllabi, and student comments do not belong in your record.

Keep exactly two short anonymous quotes from your own evaluations, with course/term attribution. Do not publish evaluation screenshots. Keep the full supported-course list in Experience. The concise web CV links to it; the downloadable PDF remains a separate record.

## L. Update collaboration and project status

Edit `collaboration.qmd` and related cards in Research/CV. Keep four collaboration themes: Earth Observation & GeoAI; Agricultural Water & Conservation; Climate & Food-System Resilience; Decision Science, Economics & Implementation. Change submitted/prospective wording to awarded/funded/active only after official confirmation. CPRA currently describes a submitted proposal. REAL Decision Lab remains a developing research program. FAO, Oxford Martin School, Cornell, and RAAPID are prospective network connections for the proposal, not claims of your established personal partnerships.

## M. Update collaboration and profile links

Edit `contact.qmd`. Scholar also appears in Home and Publications; footer links are in `_quarto.yml`. Copy complete public URLs and check while signed out. LinkedIn uses your supplied `md-bodrud-doza-phd-33156a80` profile. A sign-in page or HTTP 403/429/999 cannot establish whether a link is broken; review blocked links manually. New-tab links receive `noopener noreferrer` during rendering.

Update organisation links in `collaboration.qmd` and the linked role cards in `experience.qmd`. Check official organisation pages and preserve the distinction between formal partners and prospective connections.

## N. Preview locally with Quarto

Install Python 3 and Quarto 1.10.19. Open a terminal in the source folder (locally `E:\Z_website\site`) and run:

```sh
python scripts/render_updates.py
quarto preview
```

Open the local address shown, inspect desktop/phone layouts, and stop with Ctrl+C. Python is required for publication generation. ReportLab is only required when rebuilding the PDF.

## O. Run checks

```sh
quarto render
python scripts/check_site.py
python scripts/check_external_links.py --output external-link-report.json
```

The site check validates internal links/anchors, headings, alt text, metadata, publication uniqueness, and safe new-tab links. The separate external audit uses bounded requests and treats blocking/rate limits as **unverified**; investigate confirmed 404/410 responses. It does not run as a deployment gate. Keep its output outside the repository or delete it after review.

For major edits, inspect at 390, 768, 1024, 1200, and 1440 pixels. Check no horizontal scrolling, the desktop name, readable frameworks, navigation, filters/reset, keyboard focus, images, and PDF download. Automated checks do not establish research accuracy or replace visual review.

## P. How Actions deployment works

`.github/workflows/publish.yml` installs Python/Quarto, generates publication views, renders, finalizes new-tab links, checks the site, uploads `_site`, and deploys changes to `main`. Pull requests only build/check. Keep **Settings → Pages → Source** set to **GitHub Actions**. No additional token or secret is needed. Open a failed run's red step, fix the reported source error, and commit again. Allow a short delay after a green deployment before refreshing the live site.

## Q. Restore a previous version


For one file, click **History**, open the previous good version, and copy its contents. Edit the current file, restore those contents, and commit “Restore previous version”. For a merged pull request, use **Revert** if offered, then merge the resulting revert PR after checks pass. Restore coordinated files together for a multi-file change. Do not delete the repository or rewrite history to roll back.

## R. Quarterly checklist

- Current title, affiliation, and dates agree across Home, Experience, web CV, and PDF.
- New publications, featured papers, DOI links, and the research arc are current.
- Public CV is readable, current, and free of private information.
- Project/collaboration status and proposal wording remain accurate.
- Teaching, awards, and service are current.
- External/profile links are checked; blocked links receive manual review.
- Image permission, alt text, captions, and mobile layouts remain appropriate.

- Updates dates, research areas, and the learning loop remain current.

