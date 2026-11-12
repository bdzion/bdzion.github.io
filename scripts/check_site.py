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
    allowed={'index.html':['assets/portrait.webp','assets/images/research/field-monitoring-site.webp'],'projects.html':['assets/images/research/field-monitoring-site.webp'],'publications.html':['assets/images/journey/research-journey.webp'],'research.html':['assets/lab-logo.webp'],'research-journey.html':['assets/images/journey/research-journey.webp'],'experience.html':['assets/images/experience/leadership-consultation.webp']}.get(f.name,[])
    if p.images!=allowed:errors.append(f'{f.name}: unexpected image under the portrait/field-site/journey/one-leadership-photo/lab-logo policy: {p.images}')
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
expected={'index.html','research.html','projects.html','teaching.html','research-journey.html','experience.html','publications.html','cv.html','collaboration.html','contact.html','404.html'}
if not expected.issubset({p.name for p in pages}):errors.append('Missing required pages')
# Faculty-recruitment structure: primary navigation, stable anchors, and status wording.
def page(name):return pages[(output/name).resolve()]
def source(name):return (output/name).read_text(encoding='utf-8')
for name in expected-{'404.html'}:
    for target in ['research.html','publications.html','teaching.html','cv.html','contact.html']:
        if not any(urlsplit(l).path.endswith(target) for l in page(name).links):errors.append(f'{name}: primary navigation is missing {target}')
required_ids={'index.html':{'problem-to-solution','career-path'},'research.html':{'research-pillars','four-connected-research-areas','current-and-developing-projects','current-project-healthy-lake-huron','five-year-program','case-studies','area-observe','area-understand','area-design','area-learn'},'projects.html':{'precision-conservation','healthy-lake-huron','environmental-intelligence'},'teaching.html':{'teaching-philosophy','teaching-experience','teaching-effectiveness','courses-i-can-teach','mentoring','teaching-materials'},'experience.html':{'teaching-and-mentoring','academic-applied-research','climate-development-leadership'},'cv.html':{'selected-awards','teaching','academic-service','short-biography','short-bio'},'contact.html':{'contact-email'}}
for name,ids in required_ids.items():
    if not ids.issubset(page(name).ids):errors.append(f'{name}: missing section anchors {sorted(ids-page(name).ids)}')
# Statements that keep roles and project status accurate must not be dropped silently.
required_text={'research.html':['A developing research program','not yet a staffed laboratory','funding is not confirmed','no award is confirmed'],'projects.html':['None has been delivered yet','No results are reported in this section','no award is confirmed'],'teaching.html':['not yet been an instructor of record','Graduate Teaching Assistant','GEOG*3480','GEOG*2480','GEOG*2000','GEOG*3000','not yet formally supervised'],'cv.html':['not yet held a grant as principal investigator']}
for name,phrases in required_text.items():
    for phrase in phrases:
        if phrase not in source(name):errors.append(f'{name}: missing required accuracy statement "{phrase}"')
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
assert publication_page.index('id="featured-research"') < publication_page.index('Overlapping Peer-Reviewed Research Domains') < publication_page.index('Selected Publication Milestones') < publication_page.index('id="publication-record"'), 'Incorrect publication page hierarchy: selected papers, timeline, complete record'
featured_records=[p for p in records if p.get('featured')]
assert 4<=len(featured_records)<=6,'Select four to six featured publications'
assert all(p.get('title') and p.get('journal') and p.get('contribution') and p.get('url') for p in featured_records),'Featured publications need title, journal, contribution and link'
assert publication_page.count('class="publication-feature"')==len(featured_records),'Featured publications are not all rendered'
journal_records=[p for p in records if p['category'] in ('First-Authored Articles','Co-Authored Articles')]
summary=f"{len(journal_records)} peer-reviewed journal articles, {sum(p['first_authored'] for p in journal_records)} of them first-authored"
chart_years={p['year'] for p in records if p['category'] in ('First-Authored Articles','Co-Authored Articles','Book Chapters') and p['year'] is not None}
assert publication_page.count('<li data-year=')==max(chart_years)-min(chart_years)+1,'Publication chart does not cover every year'
assert publication_page.count('data-topic=')==5 and 'class="quick-filters"' in publication_page,'Missing publication quick filters'
for name in ['index.html','cv.html']:
    assert summary in (output/name).read_text(encoding='utf-8'),f'{name}: publication summary does not match publications.json'
cv_pdf=output/'assets/Md_Bodrud_Doza_Academic_CV.pdf'
assert cv_pdf.exists() and cv_pdf.read_bytes().startswith(b'%PDF-'), 'Missing canonical CV download'
if errors:raise SystemExit('\n'.join(errors))
print(f'Passed: {len(pages)} pages, internal links and anchors, headings, alt text, metadata, and {len(records)} publication records')
