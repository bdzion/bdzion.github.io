"""Generate accessible publication HTML from the single JSON source."""
import json,html,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
records=json.loads((root/'publications.json').read_text(encoding='utf-8'))
def e(v): return html.escape(str(v),quote=True)
def view(p):
 c=p['category']
 if c in ('First-Authored Articles','Co-Authored Articles','Book Chapters'):return 'Peer-reviewed research & chapters'
 if c=='Working Papers':return 'Working papers'
 if c=='Conference Abstracts':return 'Conference contributions'
 if c=='Selected Public and Policy Writing':return 'Public writing'
 return 'Reports & policy'
def item(p,featured=False):
 link=f'<a class="doi-link" href="{e(p["url"])}" target="_blank" rel="noopener noreferrer">{"Read paper / DOI" if p["doi"] else "Read publication"} ↗</a>' if p['url'] else ''
 badge='<span class="authorship">First-authored</span>' if p['first_authored'] else ''
 if featured:
  journal=f'<p class="journal">{e(p.get("journal", ""))} · {e(p["year"] if p["year"] is not None else "Undated")}</p>'
  contribution=f'<p class="contribution"><strong>Contribution:</strong> {e(p["contribution"])}</p>' if p.get('contribution') else ''
  tags='<div class="topic-tags">'+''.join(f'<span>{e(t)}</span>' for t in p.get('display_tags',p['topics'])[:3])+'</div>'
  feature_link=link.replace(" ↗</a>"," →</a>")
  role='<p class="feature-role">'+('First author' if p['first_authored'] else 'Co-author')+'</p>'
  return f'<article class="publication-feature">{role}<h3>{e(p.get("title",p["citation"]))}</h3>{journal}{contribution}{tags}{feature_link}</article>'
 attrs=f'data-category="{e(p["category"])}" data-view="{e(view(p))}" data-year="{e(p["year"])}" data-topics="{e("|".join(p["topics"]))}" data-first="{str(p["first_authored"]).lower()}"'
 citation=re.sub(r'Bodrud-Doza(?:,?\s*M\.?)?',lambda m:'<strong>'+m[0]+'</strong>',e(p['citation']))
 return f'<article class="publication-entry" {attrs}><p class="citation">{citation}</p><div class="publication-meta">{badge}{link}</div></article>'
featured=[p for p in records if p.get('featured')]
for name,subset in [('featured.html',featured),('featured-home.html',featured[:3])]:
 (root/'_includes'/name).write_text(('<div class="featured-grid home-featured">' if name=='featured-home.html' else '<div class="featured-grid">')+''.join(item(p,True) for p in subset)+'</div>',encoding='utf-8')
# One factual sentence, counted from the records so it cannot drift from the list.
journal=[p for p in records if p['category'] in ('First-Authored Articles','Co-Authored Articles')]
first=sum(1 for p in journal if p['first_authored'])
chapters=sum(1 for p in records if p['category']=='Book Chapters')
summary=f'{len(journal)} peer-reviewed journal articles, {first} of them first-authored, and {chapters} book chapters.'
# Quarto includes must stand on their own line, so each file is a complete block.
(root/'_includes/record-summary.html').write_text(f'<p class="record-summary">{summary}</p>',encoding='utf-8')
(root/'_includes/record-glance.html').write_text(f'<div><dt>Scholarly record</dt><dd>{summary} <a href="publications.qmd">Publications →</a></dd></div>',encoding='utf-8')
# Peer-reviewed output by year. Readable as text; site.js makes each year a filter button.
scholarly=[p for p in records if p['category'] in ('First-Authored Articles','Co-Authored Articles','Book Chapters') and p['year'] is not None]
years=range(min(p['year'] for p in scholarly),max(p['year'] for p in scholarly)+1)
by_year={y:[p for p in scholarly if p['year']==y] for y in years}
peak=max(len(v) for v in by_year.values())
bars=''
for y,items in by_year.items():
 lead=sum(1 for p in items if p['first_authored']);total=len(items)
 bars+=(f'<li data-year="{y}"><span class="bar-count">{total}</span><span class="bar" aria-hidden="true" style="height:{total/peak*100:.1f}%">'
        f'<i class="bar-first" style="height:{(lead/total*100 if total else 0):.1f}%"></i></span><span class="bar-year">{y}</span>'
        f'<span class="visually-hidden"> {total} peer-reviewed publications, {lead} first-authored</span></li>')
(root/'_includes/publication-chart.html').write_text('<figure class="pub-chart"><figcaption>Peer-reviewed articles and chapters by year</figcaption><ol class="pub-bars">'+bars+'</ol><p class="chart-legend"><span class="key key-first"></span>First-authored <span class="key key-co"></span>Co-authored<span class="chart-hint" hidden> · Select a year to filter the record below</span></p></figure>',encoding='utf-8')
quick=[('Precision conservation','Agricultural Landscapes & Precision Conservation'),('Water quality & watersheds','Water Quality & Watershed Science'),('Geospatial & machine learning','Geospatial & Machine Learning'),('Climate & resilience','Climate & Resilience'),('Groundwater & environmental quality','Environmental Quality & Groundwater')]
all_topics={t for p in records for t in p['topics']}
assert all(t in all_topics for _,t in quick),'Quick-filter topic is not used by any publication'
quick_html='<div class="quick-filters" hidden><span class="quick-label">Quick filters</span>'+''.join(f'<button type="button" aria-pressed="false" data-topic="{e(t)}">{e(l)}</button>' for l,t in quick)+'<button type="button" aria-pressed="false" data-first="true">First-authored</button></div>'
def select(id,label,values,first):
 return f'<div><label for="{id}">{label}</label><select id="{id}"><option value="">{first}</option>'+''.join(f'<option>{e(v)}</option>' for v in values)+'</select></div>'
views=list(dict.fromkeys(view(p) for p in records))
controls='<div class="publication-controls" hidden><div class="search-control"><label for="pub-search">Search publications</label><input id="pub-search" type="search" placeholder="Title, author, year, or keyword"></div>'
controls+=select('pub-view','Publication view',views,'All views')
controls+=select('pub-topic','Research topic',sorted({t for p in records for t in p['topics']}),'All topics')
controls+=select('pub-year','Year',sorted({p['year'] for p in records if p['year'] is not None},reverse=True),'All years')
controls+=select('pub-category','Category',list(dict.fromkeys(p['category'] for p in records)),'All categories')
controls+='<div><label for="pub-author">Authorship</label><select id="pub-author"><option value="">All authorship</option><option value="first">First-authored articles</option></select></div><button id="pub-reset" type="button">Reset filters</button></div><p id="pub-status" role="status" aria-live="polite" hidden></p>'
sections=[]
for group in views:
 body=''
 for category in dict.fromkeys(p['category'] for p in records if view(p)==group):
  body+='<section class="publication-group"><h4>'+e(category)+'</h4>'+''.join(item(p) for p in records if p['category']==category)+'</section>'
 sections.append('<section class="publication-view"><h3 class="publication-view-heading">'+e(group)+'</h3>'+body+'</section>')
(root/'_includes/publication-list.html').write_text(quick_html+controls+'<div id="publication-entries">'+''.join(sections)+'</div>',encoding='utf-8')
print(f'Generated publication views from {len(records)} records')
