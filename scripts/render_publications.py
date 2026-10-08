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
  contribution=f'<p class="contribution">{e(p["contribution"])}</p>' if p.get('contribution') else ''
  tags='<div class="topic-tags">'+''.join(f'<span>{e(t)}</span>' for t in p.get('display_tags',p['topics'])[:3])+'</div>'
  return f'<article class="publication-feature"><p class="eyebrow">{"First-authored" if p["first_authored"] else "Featured research"}</p><h3>{e(p.get("title",p["citation"]))}</h3>{contribution}{journal}{tags}{link}</article>'
 attrs=f'data-category="{e(p["category"])}" data-view="{e(view(p))}" data-year="{e(p["year"])}" data-topics="{e("|".join(p["topics"]))}" data-first="{str(p["first_authored"]).lower()}"'
 citation=re.sub(r'Bodrud-Doza(?:,?\s*M\.?)?',lambda m:'<strong>'+m[0]+'</strong>',e(p['citation']))
 return f'<article class="publication-entry" {attrs}><p class="citation">{citation}</p><div class="publication-meta">{badge}{link}</div></article>'
featured=[p for p in records if p.get('featured')]
for name,subset in [('featured.html',featured),('featured-home.html',featured[:3])]:
 (root/'_includes'/name).write_text(('<div class="featured-grid home-featured">' if name=='featured-home.html' else '<div class="featured-grid">')+''.join(item(p,True) for p in subset)+'</div>',encoding='utf-8')
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
(root/'_includes/publication-list.html').write_text(controls+'<div id="publication-record">'+''.join(sections)+'</div>',encoding='utf-8')
print(f'Generated publication views from {len(records)} records')
