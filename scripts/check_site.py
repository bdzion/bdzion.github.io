"""Check rendered local links, document structure, and public content using the standard library."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json, re
root=Path(__file__).resolve().parents[1]
output=root/'_site'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set(); self.headings=[]; self.bad_images=[]; self.lang=None; self.description=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='meta' and a.get('name')=='description':self.description=True
        if tag in ['a','link'] and 'href' in a:self.links.append(a['href'])
        if tag in ['img','script'] and 'src' in a:self.links.append(a['src'])
        if tag=='img' and not a.get('alt'):self.bad_images.append(a.get('src'))
        if tag in ['h1','h2','h3','h4','h5','h6']:self.headings.append(int(tag[1]))
errors=[]; pages={}
for f in output.glob('*.html'):
    p=Page(); p.feed(f.read_text(encoding='utf-8')); pages[f.resolve()]=p
    if not p.lang or not p.lang.startswith('en'):errors.append(f'{f.name}: missing English language')
    if not p.description:errors.append(f'{f.name}: missing description')
    if p.headings.count(1)!=1:errors.append(f'{f.name}: expected one H1')
    for x,y in zip(p.headings,p.headings[1:]):
        if y>x+1:errors.append(f'{f.name}: heading jump {x} -> {y}')
    if p.bad_images:errors.append(f'{f.name}: missing image alt {p.bad_images}')
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
expected={'index.html','research.html','research-journey.html','experience.html','publications.html','cv.html','collaboration.html','contact.html'}
if not expected.issubset({p.name for p in pages}):errors.append('Missing required pages')
records=json.loads((root/'publications.json').read_text(encoding='utf-8'))
assert len({p['id'] for p in records})==len(records),'Duplicate publication IDs'
assert len({p['doi'] for p in records if p['doi']})==sum(bool(p['doi']) for p in records),'Duplicate DOI records'
if errors:raise SystemExit('\n'.join(errors))
print(f'Passed: {len(pages)} pages, internal links and anchors, headings, alt text, metadata, and {len(records)} publication records')
