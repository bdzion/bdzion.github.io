"""Render a small publication timeline; dates and paper links come from the record."""
import html
import json
from pathlib import Path

PEER_REVIEWED_CATEGORIES = frozenset({'First-Authored Articles', 'Co-Authored Articles', 'Book Chapters'})


def build_timeline(records, config):
    by_id = {p['id']: p for p in records}
    if len(by_id) != len(records):
        raise ValueError('Publication IDs must be unique')
    domains = []
    for domain in config['domains']:
        years = sorted({p['year'] for p in records
                        if p['category'] in PEER_REVIEWED_CATEGORIES
                        and isinstance(p['year'], int) and not isinstance(p['year'], bool)
                        and set(domain['topics']).intersection(p['topics'])})
        if not years:
            raise ValueError(f"No dated peer-reviewed publications match domain: {domain['label']}")
        domains.append(dict(label=domain['label'], years=years))
    if not domains:
        raise ValueError('At least one research domain is required')
    milestones = []
    for milestone in config['milestones']:
        papers = []
        for paper in milestone['papers']:
            if paper['id'] not in by_id:
                raise ValueError(f"Unknown milestone publication ID: {paper['id']}")
            record = by_id[paper['id']]
            if record['category'] not in PEER_REVIEWED_CATEGORIES:
                raise ValueError(f"Milestone needs a scholarly article or chapter: {paper['id']}")
            if not isinstance(record['year'], int) or isinstance(record['year'], bool):
                raise ValueError(f"Milestone needs a verified year: {paper['id']}")
            url = 'https://doi.org/' + record['doi'] if record['doi'] else record['url']
            if not url or not url.startswith('https://'):
                raise ValueError(f"Milestone needs a public HTTPS link: {paper['id']}")
            papers.append(dict(id=paper['id'], label=paper['label'], year=record['year'],
                               url=url, title=record.get('title') or record['citation']))
        if not papers or len({p['year'] for p in papers}) != 1:
            raise ValueError('Each milestone must contain papers from one year')
        milestones.append(dict(label=milestone['label'], summary=milestone['summary'],
                               year=papers[0]['year'], papers=papers))
    milestones.sort(key=lambda m: m['year'])
    first = min(d['years'][0] for d in domains)
    last = max(d['years'][-1] for d in domains)
    return domains, milestones, first, last


def render_timeline(records, config):
    domains, milestones, first, last = build_timeline(records, config)
    escape = lambda value: html.escape(str(value), quote=True)
    count = last - first + 1
    axis = ''.join(f'<span>{year}</span>' for year in range(first, last + 1))
    rows = []
    for domain in domains:
        start, end = domain['years'][0], domain['years'][-1]
        span = str(start) if start == end else f'{start}–{end}'
        markers = ''.join(f'<i style="grid-column:{year-first+1}" aria-hidden="true"></i>'
                          for year in domain['years'])
        rows.append(f'<li class="publication-domain" data-start="{start}" data-end="{end}">'
                    f'<div class="domain-label"><strong>{escape(domain["label"])}</strong>'
                    f'<span class="domain-span">{span}</span></div>'
                    f'<div class="domain-track" aria-hidden="true">'
                    f'<span class="domain-band" style="grid-column:{start-first+1} / {end-first+2}"></span>'
                    f'{markers}</div></li>')
    cards = []
    for milestone in milestones:
        links = ''.join(f'<a href="{escape(p["url"])}" data-publication-id="{escape(p["id"])}" '
                        f'aria-label="{escape(p["title"])}" target="_blank" rel="noopener noreferrer">'
                        f'{escape(p["label"])} →</a>' for p in milestone['papers'])
        cards.append(f'<li><span class="milestone-year">{milestone["year"]}</span>'
                     f'<strong>{escape(milestone["label"])}</strong>'
                     f'<p>{escape(milestone["summary"])}</p><div class="milestone-links">{links}</div></li>')
    return (f'<div class="publication-timeline" style="--timeline-years:{count}">'
            '<h3>Overlapping Peer-Reviewed Research Domains</h3>'
            f'<div class="domain-axis" aria-hidden="true"><span></span><div>{axis}</div></div>'
            f'<ul class="publication-domains">{"".join(rows)}</ul>'
            '<p class="timeline-note">Spans use journal articles and book chapters only. Marks show years with '
            'scholarly publications, not continuous annual output; conference contributions, reports and public '
            'or policy writing remain in the complete record below.</p>'
            f'<h3>Selected Publication Milestones</h3><ol class="publication-milestones">{"".join(cards)}</ol></div>')


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    records = json.loads((root / 'publications.json').read_text(encoding='utf-8'))
    config = json.loads((root / 'publication-timeline.json').read_text(encoding='utf-8'))
    (root / '_includes/publication-timeline.html').write_text(render_timeline(records, config), encoding='utf-8')
    print(f'Generated {len(config["domains"])} publication domains and {len(config["milestones"])} milestones')
