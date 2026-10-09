"""Check rendered local links, document structure, and public content using the standard library."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json, re, struct
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
output=root/'_site'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.images=[]; self.ids=set(); self.duplicate_ids=[]; self.headings=[]; self.bad_images=[]; self.bad_rel=[]; self.lang=None; self.description=False; self.meta={}; self.canonicals=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:self.duplicate_ids.append(a['id'])
            self.ids.add(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='meta' and a.get('name')=='description':self.description=True
        if tag=='meta':self.meta.setdefault(a.get('property',a.get('name','')),[]).append(a.get('content',''))
        if tag=='link' and a.get('rel')=='canonical':self.canonicals.append(a.get('href'))
        if tag in ['a','link'] and 'href' in a:self.links.append(a['href'])
        if tag in ['img','script'] and 'src' in a:self.links.append(a['src'])
        if tag=='img' and not a.get('alt'):self.bad_images.append(a.get('src'))
        if tag=='img':self.images.append(a.get('src'))
        if tag=='a' and a.get('target')=='_blank' and not {'noopener','noreferrer'}.issubset(set(a.get('rel','').split())):self.bad_rel.append(a.get('href'))
        if tag in ['h1','h2','h3','h4','h5','h6']:self.headings.append(int(tag[1]))
errors=[]; pages={}
base=re.search(r'^\s*site-url:\s*(\S+)',(root/'_quarto.yml').read_text(encoding='utf-8'),re.M)[1].rstrip('/')
for f in output.glob('*.html'):
    p=Page(); p.feed(f.read_text(encoding='utf-8')); pages[f.resolve()]=p
    if p.duplicate_ids:errors.append(f'{f.name}: duplicate IDs {p.duplicate_ids}')
    if not p.lang or not p.lang.startswith('en'):errors.append(f'{f.name}: missing English language')
    if not p.description:errors.append(f'{f.name}: missing description')
    canonical=base+'/' if f.name=='index.html' else base+'/'+f.name
    if p.canonicals!=[canonical]:errors.append(f'{f.name}: incorrect canonical URL')
    for key,value in {'og:url':canonical,'og:type':'website','og:image':base+'/assets/social-preview.png','og:image:width':'1200','og:image:height':'630','twitter:card':'summary_large_image','twitter:image':base+'/assets/social-preview.png','robots':'noindex, follow' if f.name=='404.html' else 'index, follow'}.items():
        if p.meta.get(key)!=[value]:errors.append(f'{f.name}: incorrect or duplicate {key}')
    for key in ['og:title','og:description','og:image:alt','twitter:title','twitter:description','twitter:image:alt']:
        if len(p.meta.get(key,[]))!=1 or not p.meta[key][0].strip():errors.append(f'{f.name}: missing or duplicate {key}')
    if p.headings.count(1)!=1:errors.append(f'{f.name}: expected one H1')
    for x,y in zip(p.headings,p.headings[1:]):
        if y>x+1:errors.append(f'{f.name}: heading jump {x} -> {y}')
    if p.bad_images:errors.append(f'{f.name}: missing image alt {p.bad_images}')
    if p.bad_rel:errors.append(f'{f.name}: unsafe new-tab links {p.bad_rel}')
    if f.name=='404.html' and not {base+'/',base+'/research.html'}.issubset(set(p.links)):errors.append('404.html: missing recovery links')
    allowed={'index.html':['assets/portrait.webp'],'research-journey.html':['assets/images/journey/research-journey.webp'],'experience.html':['assets/images/experience/leadership-consultation.webp']}.get(f.name,[])
    if p.images!=allowed:errors.append(f'{f.name}: unexpected image under the portrait/journey/one-leadership-image policy: {p.images}')
    text=f.read_text(encoding='utf-8')
    for forbidden in ['7,000+','60+','h-index','2026 – Present','{{< include']:
        if forbidden in text:errors.append(f'{f.name}: stale or unrendered content {forbidden}')
for f,p in pages.items():
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=(output/unquote(u.path.lstrip('/')) if u.path.startswith('/') else f.parent/unquote(u.path)).resolve() if u.path else f
        if not target.is_relative_to(output.resolve()):errors.append(f'{f.name}: link escapes site {link}');continue
        if not target.exists():errors.append(f'{f.name}: broken link {link}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{f.name}: broken anchor {link}')
expected={'index.html','research.html','research-journey.html','experience.html','publications.html','cv.html','collaboration.html','contact.html','404.html'}
if not expected.issubset({p.name for p in pages}):errors.append('Missing required pages')
preview=output/'assets/social-preview.png'
if not preview.exists() or struct.unpack('>II',preview.read_bytes()[16:24])!=(1200,630):errors.append('Social preview must be a 1200 by 630 PNG')
if not (output/'robots.txt').exists() or f'Sitemap: {base}/sitemap.xml' not in (output/'robots.txt').read_text():errors.append('Missing robots or sitemap declaration')
locs=[e.text for e in ET.parse(output/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
if base+'/' not in locs or base+'/index.html' in locs or base+'/404.html' in locs:errors.append('Sitemap must use the canonical homepage and exclude 404')
home=(output/'index.html').read_text(encoding='utf-8')
profile=re.search(r'<script type="application/ld\+json">(.*?)</script>',home,re.S)
if not profile or json.loads(profile[1])['@graph'][0]['jobTitle']!='Postdoctoral Scholar':errors.append('Missing academic profile structured data')
records=json.loads((root/'publications.json').read_text(encoding='utf-8'))
assert len({p['id'] for p in records})==len(records),'Duplicate publication IDs'
assert len({p['doi'] for p in records if p['doi']})==sum(bool(p['doi']) for p in records),'Duplicate DOI records'
from render_publication_timeline import render_timeline
timeline_config=json.loads((root/'publication-timeline.json').read_text(encoding='utf-8'))
timeline=render_timeline(records,timeline_config)
assert (root/'_includes/publication-timeline.html').read_text(encoding='utf-8')==timeline,'Stale generated publication timeline'
publication_page=(output/'publications.html').read_text(encoding='utf-8')
assert publication_page.count('class="publication-domain"')==len(timeline_config['domains']),'Missing publication domains'
assert publication_page.count('data-publication-id=')==sum(len(m['papers']) for m in timeline_config['milestones']),'Missing milestone papers'
assert {'research-publication-timeline','how-the-research-program-developed','featured-research','publication-record'}.issubset(pages[(output/'publications.html').resolve()].ids),'Missing publication section anchors'
if errors:raise SystemExit('\n'.join(errors))
print(f'Passed: {len(pages)} pages, internal links and anchors, headings, alt text, metadata, and {len(records)} publication records')
