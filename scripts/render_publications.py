"""Generate accessible publication HTML from the single JSON source before Quarto renders."""
import json, html
from pathlib import Path
root = Path(__file__).resolve().parents[1]
records = json.loads((root / "publications.json").read_text(encoding="utf-8"))
def e(value): return html.escape(str(value), quote=True)
def item(p, featured=False):
    title = p.get("title", p["citation"])
    attrs = f'data-category="{e(p["category"])}" data-topics="{e("|".join(p["topics"]))}" data-first="{str(p["first_authored"]).lower()}"'
    badge = '<span class="authorship">First-authored</span>' if p["first_authored"] else ''
    link = f'<a class="doi-link" href="{e(p["url"])}" target="_blank" rel="noopener noreferrer">{"Read paper / DOI" if p["doi"] else "Read publication"} ↗</a>' if p["url"] else ''
    if featured:
        return f'<article class="publication-feature"><p class="eyebrow">{e(p["year"])} · First-authored</p><h3><a href="{e(p["url"])}" target="_blank" rel="noopener noreferrer">{e(title)}</a></h3><p class="citation">{e(p["citation"])}</p>{link}</article>'
    return f'<article class="publication-entry" {attrs}><p class="citation">{e(p["citation"])}</p><div class="publication-meta">{badge}{link}</div></article>'
featured = [p for p in records if p.get("featured")]
for name, subset in [("featured.html", featured), ("featured-home.html", featured[:3])]:
    (root / "_includes" / name).write_text('<div class="featured-grid">' + ''.join(item(p, True) for p in subset) + '</div>', encoding="utf-8")
topics = sorted({t for p in records for t in p["topics"]})
controls = '<div class="publication-controls" hidden><div><label for="pub-search">Search publications</label><input id="pub-search" type="search" placeholder="Title, author, year, or keyword"></div><div><label for="pub-topic">Research topic</label><select id="pub-topic"><option value="">All topics</option>' + ''.join(f'<option>{e(t)}</option>' for t in topics) + '</select></div><div><label for="pub-author">Authorship</label><select id="pub-author"><option value="">All authorship</option><option value="first">First-authored articles</option></select></div><button id="pub-reset" type="button">Reset</button></div><p id="pub-status" role="status" aria-live="polite" hidden></p>'
sections = []
for category in dict.fromkeys(p["category"] for p in records):
    sections.append('<section class="publication-group"><h3>' + e(category) + '</h3>' + ''.join(item(p) for p in records if p["category"] == category) + '</section>')
(root / "_includes/publication-list.html").write_text(controls + '<div id="publication-record">' + ''.join(sections) + '</div>', encoding="utf-8")
print(f"Generated publication views from {len(records)} records")
