# Maintaining your academic website

Your live site is https://bdzion.github.io. The source repository is `bdzion/bdzion.github.io`. You edit source files; GitHub builds and publishes the pages automatically.

## A. Edit text directly on GitHub

1. Open the repository **Code** tab and a page file, such as `research.qmd`.
2. Click the pencil (**Edit this file**). Edit below the opening `---` metadata block. Keep surrounding HTML tags, quotation marks, and links intact.
3. Click **Commit changes** with a clear description. Routine corrections can go to `main`; substantial edits should use a new branch and pull request.
4. Open **Actions**, wait for a green deployment, and check the live page. A pull request builds but does not publish before merging.

Page map: `index.qmd` = Home; `research.qmd` = Research; `research-journey.qmd` = Journey; `experience.qmd` = Experience; `publications.qmd` = Publications introduction; `cv.qmd` = web CV; `collaboration.qmd` = Collaboration; `contact.qmd` = Contact. Navigation and metadata live in `_quarto.yml`; appearance lives in `styles.css`.

## B. Update the current position and homepage

Edit the appointment and affiliation in `index.qmd`, then the corresponding entries in `experience.qmd`, `cv.qmd`, and `assets/cv-content.json`. The confirmed Postdoctoral Scholar start is **September 2026**. Follow E to update the PDF separately. Keep the homepage's direction cards brief and label emerging work clearly. Link to Scholar for current metrics rather than adding fixed publication/citation totals.

## C. Add a publication

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

## D. Mark or unmark featured papers

Set `"featured": true` or `false`. Cards follow JSON order; Home displays the first three featured papers. Supply `title` for featured records. Optional card fields are:

```json
"title": "Exact published title",
"journal": "Journal name",
"contribution": "One accurate sentence about the contribution.",
"display_tags": ["Precision conservation", "Machine learning"]
```

Use two or three short display tags; `topics` still drives filtering. Retain the full `citation`. Update the separate research-arc text in `publications.qmd` when needed.

## E. Update the public CV PDF safely

Use **Add file → Upload files** inside `assets` to replace `Md_Bodrud_Doza_Academic_CV.pdf` with a reviewed public PDF using the same filename. Alternatively edit `assets/cv-content.json`, install ReportLab locally, and run `python scripts/build_cv.py`.

Review every page and link after rebuilding. Remove private phone numbers, home addresses, immigration details, referee contacts, hidden comments, and private metadata. Use institutional contact details only. Never upload the original private Word CV. Test the live download. Editing `cv.qmd` alone does not update the PDF.

## F. Add or replace a photo and its alt text

Use a compressed WebP/JPEG derivative with EXIF/GPS metadata removed and aspect ratio preserved. Keep high-resolution originals outside the repository. Store derivatives under `assets/images/research`, `experience`, or `journey`; `_quarto.yml` already includes these folders.

Copy an existing `<figure class="evidence-photo">` block and change `src`, pixel `width`/`height`, `alt`, and caption. Keep `loading="lazy"`. Describe what the image shows and why it matters, for example “Md Bodrud-Doza beside a stream during field monitoring”. Do not invent dates or locations. Update `assets/images/manifest.json` if maintaining the source/dimensions inventory.

The research-and-family collage was included with your explicit permission on 7 October 2026. It is an exception to the professional-photo default. Do not add family names or further private details; review permission before adding other personal photographs. Remove the figure and derivative if you later prefer an entirely professional portfolio.

## G. Add a research project

In `research.qmd`, copy a current-work `<article class="research-card">`. Add a concise title, status, question/contribution, and supporting link. Distinguish published foundations, ongoing work, submitted proposals, and future ideas. Update Home only if it changes the overall research story.

## H. Update teaching feedback

Edit quote cards in `experience.qmd`. Use at most two or three short anonymous quotes, copied accurately, with course/term attribution and the label **selected feedback**. Do not publish raw evaluation screenshots. A named recommendation needs accurate attribution and permission; use at most one short excerpt. Update course grids in both Experience and CV if teaching changes.

## I. Update collaboration and project status

Edit `collaboration.qmd` and related cards in Research/CV. Change submitted/prospective wording to awarded/funded/active only after official confirmation. CPRA currently describes a submitted proposal. REAL Decision Lab remains a developing research program. FAO, Oxford Martin School, Cornell, and RAAPID are prospective network connections for the proposal, not claims of your established personal partnerships.

## J. Update profile links

Edit `contact.qmd`. Scholar also appears in Home and Publications; footer links are in `_quarto.yml`. Copy complete public URLs and check while signed out. LinkedIn uses your supplied `md-bodrud-doza-phd-33156a80` profile. A sign-in page or HTTP 403/429/999 cannot establish whether a link is broken; review blocked links manually. New-tab links receive `noopener noreferrer` during rendering.

## K. Preview locally with Quarto

Install Python 3 and Quarto 1.10.19. Open a terminal in the source folder (locally `E:\Z_website\site`) and run:

```sh
quarto preview
```

Open the local address shown, inspect desktop/phone layouts, and stop with Ctrl+C. Python is required for publication generation. ReportLab is only required when rebuilding the PDF.

## L. Run checks

```sh
quarto render
python scripts/check_site.py
python scripts/check_external_links.py --output external-link-report.json
```

The site check validates internal links/anchors, headings, alt text, metadata, publication uniqueness, and safe new-tab links. The separate external audit uses bounded requests and treats blocking/rate limits as **unverified**; investigate confirmed 404/410 responses. It does not run as a deployment gate. Keep its output outside the repository or delete it after review.

For major edits, inspect at 390, 768, 1024, 1200, and 1440 pixels. Check no horizontal scrolling, the desktop name, readable frameworks, navigation, filters/reset, keyboard focus, images, and PDF download. Automated checks do not establish research accuracy or replace visual review.

## M. How Actions deployment works

`.github/workflows/publish.yml` installs Python/Quarto, generates publication views, renders, finalizes new-tab links, checks the site, uploads `_site`, and deploys changes to `main`. Pull requests only build/check. Keep **Settings → Pages → Source** set to **GitHub Actions**. No additional token or secret is needed. Open a failed run's red step, fix the reported source error, and commit again. Allow a short delay after a green deployment before refreshing the live site.

## N. Undo a bad change using GitHub history

For one file, click **History**, open the previous good version, and copy its contents. Edit the current file, restore those contents, and commit “Restore previous version”. For a merged pull request, use **Revert** if offered, then merge the resulting revert PR after checks pass. Restore coordinated files together for a multi-file change. Do not delete the repository or rewrite history to roll back.

## O. Quarterly checklist

- Current title, affiliation, and dates agree across Home, Experience, web CV, and PDF.
- New publications, featured papers, DOI links, and the research arc are current.
- Public CV is readable, current, and free of private information.
- Project/collaboration status and proposal wording remain accurate.
- Teaching, awards, and service are current.
- External/profile links are checked; blocked links receive manual review.
- Image permission, alt text, captions, and mobile layouts remain appropriate.

## P. Five-minute routine update

1. Open the relevant source file on GitHub and make one correction.
2. Keep dates and status wording consistent across affected pages.
3. Review the diff and commit a clear description.
4. Wait for Actions deployment to succeed.
5. Check the live change. If needed, restore the previous file through History.
