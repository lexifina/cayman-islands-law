"""Cayman Islands: add core statutes (Law Revision PDFs from legislation.gov.ky) to corpus.json. Reads .cache only.
The first build's Constitution acts are kept byte-for-byte; added acts are rebuilt from the cache on every run."""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ky_statute as K

here = Path(__file__).parent
BASE = 'https://legislation.gov.ky/cms/images/LEGISLATION/PRINCIPAL/'
RETRIEVED = '2026-10-30'
CONST = ('constitution', 'constitution-order-2009')

# slug, short, title, title_upper, folder, [(revision label, commenced)]
STATUTES = json.loads((here / 'statutes.json').read_text(encoding='utf8'))


def rd(p):
    b = Path(p).read_bytes()
    try:
        return b.decode('utf8')
    except UnicodeDecodeError:
        return b.decode('cp1252')


def main():
    c = json.loads((here / 'corpus.json').read_text(encoding='utf8'))
    keep_acts = [a for a in c['acts'] if a['slug'] in CONST]
    base_laws = {k: v for k, v in c['laws'].items() if k == 'si-2009-1379'}
    base_src = [s for s in c['sources'] if not s.get('added')]
    base_dec = [d for d in c['decisions'] if not d.startswith('[statutes]')]
    laws = dict(base_laws)
    acts = list(keep_acts)
    decisions = list(base_dec)
    sources = list(base_src)
    for st in STATUTES:
        vers = []
        prev = None
        for rev in st['revisions']:
            pdf = here / '.cache' / st['slug'] / ('%s.pdf' % rev['year'])
            txtp = pdf.with_suffix('.txt')
            if not txtp.exists():
                subprocess.run(['pdftotext', '-enc', 'UTF-8', '-layout', str(pdf), str(txtp)], check=True)
            units = K.parse(rd(txtp), rev.get('title_upper', st['title_upper']))
            for k, u in units.items():
                u['text'] = re.sub(r' Page \d+\n', '\n', u['text'])
            lk = '%s-%s-revision' % (st['slug'], rev['year'])
            url = BASE + '%s/%s/%s_%s Revision.pdf' % (st['folder'][:4], st['folder'], st['folder'], rev['year'])
            sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
            v = {'from': rev['from'], 'source_url': url, 'sha256': sha, 'units': units}
            if prev is None:
                v['credits'] = {}
                v['note'] = rev.get('note') or 'Oldest version available of the %s in this build: the %s Revision, in force from %s.' % (st['title'], rev['year'], rev['from'])
            else:
                cr = {}
                for k in set(units) | set(prev):
                    if units.get(k) != prev.get(k):
                        cr[k] = [lk]
                v['credits'] = cr
                v['note'] = 'The %s Revision (consolidation published by the Cayman Islands Government).' % rev['year']
            laws[lk] = {'label': '%s (%s Revision)' % (st['title'], rev['year']), 'title': '%s, %s Revision (consolidated and revised text)' % (st['title'], rev['year']),
                        'kind': 'publisher', 'enacted': rev['from'], 'published': rev['from'], 'url': url, 'temporary_until': None, 'restores': None, 'note': None}
            vers.append(v)
            prev = units
        first_lk = '%s-%s-revision' % (st['slug'], st['revisions'][0]['year'])
        acts.append({'slug': st['slug'], 'short': st['short'], 'title': st['title'], 'url': BASE + '%s/%s/%s_%s Revision.pdf' % (st['folder'][:4], st['folder'], st['folder'], st['revisions'][-1]['year']),
                     'first_law': None, 'earlier_laws': [], 'versions': vers})
        # first version credited to the publisher as oldest available
        decisions.append('[statutes] %s: %d Law Revision(s) from legislation.gov.ky (%s); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. %s' % (
            st['title'], len(vers), ', '.join(r['year'] for r in st['revisions']), st.get('decision', '')))
    c['acts'] = acts
    c['laws'] = laws
    sources.append({'name': 'Cayman Islands Legislation, current Acts by title (Law Revision PDFs)', 'url': 'https://legislation.gov.ky/cms/legislation/current/by-title.html', 'retrieved': RETRIEVED,
                    'requests': 0, 'licence': 'Official legislation; the PDFs carry no licence statement.', 'notes': 'Added statutes are the revisions linked from the site\'s history table; robots.txt (checked 2026-10-30) disallows only system folders under /cms/.', 'added': True})
    c['sources'] = sources
    c['decisions'] = decisions
    (here / 'corpus.json.tmp').write_text(json.dumps(c, ensure_ascii=False, indent=1) + '\n', encoding='utf8', newline='\n')
    os.replace(here / 'corpus.json.tmp', here / 'corpus.json')


main()
