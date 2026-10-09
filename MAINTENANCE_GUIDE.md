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

### Adjust the homepage headshot

The full original portrait remains in `assets/portrait.webp`. The homepage displays it inside a square `headshot-frame` and uses CSS to focus on the head and shoulders. In `styles.css`, find `.headshot-frame img`: `object-position` controls the crop position and `scale(1.7)` controls the zoom. Make small adjustments, preview desktop and phone, then commit. Keep the wrapper in `index.qmd`; do not change the original image's width/height attributes unless replacing the image itself.

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
  "id": "pub-091",
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

Do not edit the generated publication includes (`_includes/featured.html` and `_includes/publication-list.html`); rendering regenerates them. The PDF builder also reads `publications.json`. Add or correct a publication here once, then rebuild the PDF so the website and CV stay aligned. Keep links in the `url` field; do not append placeholder text such as `(Link:` to a citation. Home Updates are separate: add an article to both `updates.json` and `publications.json` if it should appear in both places.

## H. Mark or unmark featured papers

Set `"featured": true` or `false`. Cards follow JSON order; Home displays the first three featured papers. Supply `title` for featured records. Optional card fields are:

```json
"title": "Exact published title",
"journal": "Journal name",
"contribution": "One accurate sentence about the contribution.",
"display_tags": ["Precision conservation", "Machine learning"]
```

Use two or three short display tags; `topics` still drives filtering. Retain the full `citation`. Featured cards show title, journal/year, one contribution sentence, tags, and paper link. The full citation appears only in the complete record. Timeline milestones are selected separately; featuring a paper does not automatically add it to the timeline.

## I. Maintain the Research & Publication Timeline

The Publications page shows six selected milestone groups above overlapping publication domains. `publications.json` remains the factual source for years, topics and paper links. `publication-timeline.json` selects domain labels and milestone papers. Do not edit `_includes/publication-timeline.html`; `scripts/render_publication_timeline.py` regenerates it whenever Quarto renders.

### Add publications and update date ranges

1. Add the verified publication to `publications.json` as described in G. Use a new, unused ID (the current record already includes `pub-089` and `pub-090`).
2. Use the appropriate existing `topics` labels. Each domain's first and latest years are calculated automatically from matching dated records. You do not need to type a new date range into the page.
3. Correct a year only when supported by publication metadata. An unknown year should be `null`; it is excluded from the timeline until verified.
4. Render, check the resulting spans and filters, and rebuild the PDF if the publication record changed. A newly added paper need not become a milestone.

The bands include dated records across publication categories, including conference contributions and public writing. For example, the 2015 water-quality start is a conference contribution; the 2026 climate record is public writing. Marks show years with records, not continuous journal output. Domain spans describe published work, not appointment dates or future projects.

### Add or edit a research domain

1. Open `publication-timeline.json`. In `domains`, copy one object, keeping commas between objects.
2. Set `label` to a concise research-domain name and `topics` to one or more exact topic labels already present in `publications.json`. The visible Geospatial Analysis & Machine Learning label currently uses the existing `Geospatial & Machine Learning` filter topic.
3. Add a domain only when dated publication records support it. Emerging directions such as Earth Observation & GeoAI should not be added solely because they appear in your research plans.
4. The timeline axis expands automatically; the mobile layout stacks the rows. Rendering stops with a clear error if a domain has no matching dated records. Check desktop and phone after adding a row.

To change a domain's scope, edit its matching `topics`, then review the automatically calculated range. Never change verified publication years merely to fit a preferred span.

### Add, remove or replace a milestone paper

1. In `publication-timeline.json`, find `milestones`. Each object has a short `label`, one-sentence `summary`, and a `papers` list.
2. Copy a milestone object to add one; delete the complete object to remove one. Keep the selection small. Remove a paper by deleting its object from `papers`; if no papers remain, remove the milestone too.
3. Each paper uses an existing publication `id` and a short link `label`. Verify the ID against `publications.json`. Its year and DOI link are taken from that record automatically; do not duplicate dates or URLs in the configuration.
4. Papers grouped into one milestone must share a verified year. Milestones sort chronologically. Missing IDs, unknown years or unavailable public links fail the render rather than silently linking to the wrong work.
5. Edit the short summary only to reflect the actual linked work. Render and run `python scripts/check_site.py`, then inspect the timeline, DOI links and publication filters before merging.

The former `#how-the-research-program-developed` anchor still points to the new timeline; the complete record retains `#publication-record`. Keep these anchors so previously shared links work.

## J. Update the public CV PDF safely

Use **Add file → Upload files** inside `assets` to replace `Md_Bodrud_Doza_Academic_CV.pdf` with a reviewed public PDF using the same filename. Alternatively edit `assets/cv-content.json` for your profile, appointments, teaching, experience, awards, skills, and training. Publication entries come from `publications.json`. Install ReportLab locally (`python -m pip install reportlab`), then run `python scripts/build_cv.py` from the website folder. The builder produces white pages, clickable profile/publication links, and page numbers. It places research and teaching before the complete publication record. Rebuild whenever either source changes; Quarto does not rebuild the PDF automatically.

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
- New publications, featured papers, DOI links, and the publication timeline are current.
- Public CV is readable, current, and free of private information.
- Project/collaboration status and proposal wording remain accurate.
- Teaching, awards, and service are current.
- External/profile links are checked; blocked links receive manual review.
- Image permission, alt text, captions, and mobile layouts remain appropriate.

- Updates dates, research areas, and the learning loop remain current.


### Homepage navigation and Healthy Lake Huron partnership

Your name in the navigation links to Home, so there is no second Home menu item. Edit the website title and the remaining page links in `_quarto.yml`. Keep the name visible on mobile.

Use `https://healthylakehuron.ca/` for Healthy Lake Huron. The main applied partnership is Healthy Lake Huron partners; ABCA remains the formal Mitacs partner. Keep this distinction consistent in `research.qmd`, `collaboration.qmd`, and `assets/cv-content.json`. Write “and” in partnership headings. Label unfinished maps, indicators, and recommendations as intended outputs.


## Social sharing and search visibility

Share the homepage address `https://bdzion.github.io/`. Each page has its own title and description in its QMD header. Keep these concise and factual; they are used in search results and shared links. The build adds a canonical address, large-image social metadata, and safe external-link attributes automatically.

The shared-link image is `assets/social-preview.png`, a 1200 × 630 landscape PNG. Its editable layout is `scripts/social-preview.html`, using the existing portrait. To update it, edit the name, role, affiliation, research theme, or photo in that template; preview it locally and capture the exact 1200 × 630 card area as a PNG. Replace the asset using the same filename. Check the image at small sizes before publishing. This image is metadata, not an additional photograph on a page.

Homepage academic-profile metadata is in `_includes/profile-metadata.html`. When changing your title, affiliation, or profile links, update that file too. Do not put private information, unsupported claims, publication counts, or citation counts into metadata.

`robots.txt` points search engines to the sitemap. The build uses the root homepage address in the sitemap and excludes the error page. `404.qmd` helps visitors return to Home or Research Lab from an outdated link. Search engines and social networks may cache previews; a successful deployment does not immediately replace every cached result. Check a fresh shared link after deployment.

In GitHub, keep the repository About description, website URL, and topics current. The separate repository social-preview image is optional and can use the same PNG via **Settings → General → Social preview**. It controls shared repository links; website social metadata controls shared website links.

Deployment is restricted to `main`, including manually started workflows. Pull requests and manual feature-branch runs build and check without publishing. The build checks canonical URLs, social-preview dimensions and metadata, the sitemap, and the error page as well as links and content. Keep **Pages → Source → GitHub Actions** and enforced HTTPS.


### OMAFA proposal and Canada Postdoctoral Research Award

The OMAFA proposal is listed as **submitted / under review**, with Dr. Prasad Daggupati as lead applicant and Md Bodrud-Doza as a contributor to proposal development and proposed project collaborator. Its ACPF approach extends the PhD foundation; participation in the future project depends on acceptance. Update the project card in `research.qmd`, the proposal section in `collaboration.qmd`, the web CV in `cv.qmd`, and the project/funding entries in `assets/cv-content.json` together. Rebuild and visually check the PDF after changing those entries. Do not change the status to active or awarded without confirmation. The full application, budget, and team attachments are not published.

Write **Canada Postdoctoral Research Award (CPRA) program** on first use and link to the official NSERC program page. The food-system application remains submitted, with no confirmed award. The PDF builder adds a clickable program link; update its link mapping if the official address changes.
