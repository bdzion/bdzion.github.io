"""Give all new-tab links safe relationship attributes, including Quarto links."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]/'_site'
def safe(match):
 tag=match[0]
 if not re.search(r'\btarget=["\x27]_blank["\x27]',tag):return tag
 rel=re.search(r'\brel=(["\x27])(.*?)\1',tag)
 values=list(dict.fromkeys((rel[2].split() if rel else [])+['noopener','noreferrer']))
 replacement='rel="'+' '.join(values)+'"'
 return tag[:rel.start()]+replacement+tag[rel.end():] if rel else tag[:-1]+' '+replacement+'>'
for file in root.glob('*.html'):
 text=file.read_text(encoding='utf-8')
 file.write_text(re.sub(r'<a\b[^>]*>',safe,text,flags=re.I),encoding='utf-8')
print('Finalized new-tab link relationships')
