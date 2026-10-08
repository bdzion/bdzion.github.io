"""Render the dated homepage Updates list from editable public source metadata."""
from pathlib import Path
from datetime import date
import json,html
root=Path(__file__).resolve().parents[1]
updates=json.loads((root/'updates.json').read_text(encoding='utf-8'))
def e(value):return html.escape(str(value),quote=True)
items=[]
for update in sorted(updates,key=lambda x:x['date'],reverse=True)[:2]:
    when=date.fromisoformat(update['date'])
    if not update['url'].startswith('https://'):raise ValueError('Update links must use HTTPS')
    label=f'{when.day} {when.strftime("%B %Y")}'
    items.append(f'<li><time datetime="{e(update["date"])}">{label}</time><article><p class="update-source">{e(update["type"])} · {e(update["publisher"])}</p><h3><a href="{e(update["url"])}" target="_blank" rel="noopener noreferrer">{e(update["title"])} ↗</a></h3><p>{e(update["summary"])}</p></article></li>')
(root/'_includes/updates.html').write_text('<ul class="updates-list">'+''.join(items)+'</ul>',encoding='utf-8')
print(f'Generated Updates from {len(updates)} entries')
