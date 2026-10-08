"""Give all new-tab links safe relationship attributes, including Quarto links."""
from pathlib import Path
import re
import html
import json
import posixpath
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]/'_site'
base=re.search(r'^\s*site-url:\s*(\S+)',(root.parent/'_quarto.yml').read_text(encoding='utf-8'),re.M)[1].rstrip('/')
def safe(match):
 tag=match[0]
 if not re.search(r'\btarget=["\x27]_blank["\x27]',tag):return tag
 rel=re.search(r'\brel=(["\x27])(.*?)\1',tag)
 values=list(dict.fromkeys((rel[2].split() if rel else [])+['noopener','noreferrer']))
 replacement='rel="'+' '.join(values)+'"'
 return tag[:rel.start()]+replacement+tag[rel.end():] if rel else tag[:-1]+' '+replacement+'>'
for file in root.glob('*.html'):
 text=file.read_text(encoding='utf-8')
 text=re.sub(r'<a\b[^>]*>',safe,text,flags=re.I)
 if file.name=='404.html':
  # Pages serves this document at unknown (including nested) URL paths.
  def error_url(match):
   value=match[2]
   if value.startswith(('#','http:','https:','mailto:','data:')):return match[0]
   path=posixpath.normpath('/'+value.lstrip('/'))
   if path=='/index.html':path='/'
   return match[1]+'="'+base+path+'"'
  text=re.sub(r'\b(href|src)="([^"]*)"',error_url,text)
 # Explicit shared previews prevent Quarto from selecting a tall first image.
 text=re.sub(r'<meta\b[^>]*(?:name|property)=["\x27](?:og:image(?:\:[^"\x27]+)?|twitter:image(?:\:[^"\x27]+)?|og:url|og:type|og:locale|twitter:card|theme-color|robots)["\x27][^>]*>\s*','',text,flags=re.I)
 text=re.sub(r'<link\b[^>]*rel=["\x27]canonical["\x27][^>]*>\s*','',text,flags=re.I)
 url=base+'/' if file.name=='index.html' else base+'/'+file.name
 tags=[f'<link rel="canonical" href="{url}">']
 for key,value in {'og:url':url,'og:type':'website','og:locale':'en_CA','og:image':base+'/assets/social-preview.png','og:image:width':'1200','og:image:height':'630','og:image:type':'image/png','og:image:alt':'Md Bodrud-Doza, PhD, Postdoctoral Scholar at the University of Guelph; REAL Decision Lab.','twitter:card':'summary_large_image','twitter:image':base+'/assets/social-preview.png','twitter:image:alt':'Md Bodrud-Doza, PhD, University of Guelph; REAL Decision Lab.','theme-color':'#234b3a','robots':'noindex, follow' if file.name=='404.html' else 'index, follow'}.items():
  attribute='property' if key.startswith('og:') else 'name'
  tags.append(f'<meta {attribute}="{key}" content="{html.escape(value,quote=True)}">')
 text=text.replace('</head>','\n'.join(tags)+'\n</head>')
 file.write_text(text,encoding='utf-8')
sitemap=root/'sitemap.xml'
if sitemap.exists():
 ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
 tree=ET.parse(sitemap)
 for item in list(tree.getroot()):
  loc=item.find('{'+ns+'}loc')
  if loc is None:continue
  if loc.text==base+'/404.html':tree.getroot().remove(item)
  elif loc.text==base+'/index.html':loc.text=base+'/'
 tree.write(sitemap,encoding='utf-8',xml_declaration=True)
search=root/'search.json'
if search.exists():
 entries=json.loads(search.read_text(encoding='utf-8'))
 search.write_text(json.dumps([e for e in entries if not e.get('href','').startswith('404.html')],ensure_ascii=False),encoding='utf-8')
print('Finalized safe links, social previews, canonical URLs, sitemap and search index')
