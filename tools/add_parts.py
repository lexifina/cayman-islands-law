"""Cayman Islands: core statutes (Law Revision PDFs from legislation.gov.ky) as corpus.d parts, one part per statute.
Reads .cache only (text from `pdftotext -enc UTF-8 -layout`); deterministic. Usage: python add_parts.py [slug ...]"""
import hashlib, json, os, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ky_statute as K

here = Path(__file__).parent
BASE = 'https://legislation.gov.ky/cms/images/LEGISLATION/PRINCIPAL/'
RETRIEVED = '2026-10-30'
PARTS = [
 {'part': '30-criminal-procedure-code', 'slug': 'criminal-procedure-code', 'short': 'Criminal Procedure Code', 'title': 'The Criminal Procedure Code',
  'folder': '1975-0013', 'revisions': [
   {'year': '2019', 'from': '2019-02-14', 'title_upper': 'CRIMINAL PROCEDURE CODE'},
   {'year': '2021', 'from': '2021-01-22', 'title_upper': 'CRIMINAL PROCEDURE CODE'},
   {'year': '2026', 'from': '2026-02-03', 'title_upper': 'CRIMINAL PROCEDURE CODE'}],
  'decision': 'Revisions before 2019 use other layouts and are not included.'},
 {'part': '31-evidence-act', 'slug': 'evidence-act', 'short': 'Evidence Act', 'title': 'The Evidence Act (the Evidence Law)',
  'folder': '1978-0013', 'revisions': [
   {'year': '2018', 'from': '2018-03-16', 'title_upper': 'EVIDENCE LAW'},
   {'year': '2019', 'from': '2019-02-14', 'title_upper': 'EVIDENCE LAW'},
   {'year': '2021', 'from': '2021-01-29', 'title_upper': 'EVIDENCE ACT'}],
  'decision': 'Revisions before 2018 are not included. The 2018 and 2019 Revisions are titled the Evidence Law.'},
 {'part': '40-labour-act', 'slug': 'labour-act', 'short': 'Labour Act', 'title': 'The Labour Act (the Labour Law)',
  'folder': '1987-0030', 'revisions': [
   {'year': '2011', 'from': '2011-11-07', 'title_upper': 'LABOUR LAW'},
   {'year': '2021', 'from': '2021-02-05', 'title_upper': 'LABOUR ACT'}],
  'decision': 'Revisions before 2011 are not included. The 2011 Revision is titled the Labour Law.'},
 {'part': '50-interpretation-act', 'slug': 'interpretation-act', 'short': 'Interpretation Act', 'title': 'The Interpretation Act (the Interpretation Law)',
  'folder': '1963-0017', 'revisions': [
   {'year': '1995', 'from': '1995-03-20', 'title_upper': 'INTERPRETATION LAW'}],
  'decision': 'The 1995 Revision is the current revision on the site, dated from the commencement date the site gives (20 March 1995); the site lists no amending Act against it. The text is titled the Interpretation Law. Section 63 is printed in the source as \"64. 63. No Law ...\"; it is kept as printed, under its own heading.'},
]


def rd(p):
    b = Path(p).read_bytes()
    try:
        return b.decode('utf8')
    except UnicodeDecodeError:
        return b.decode('cp1252')


def url_of(st, year):
    return BASE + '%s/%s/%s_%s Revision.pdf' % (st['folder'][:4], st['folder'], st['folder'], year)


def verify(txt, units):
    """Every body line of every unit must occur in the source text (spacing normalised), so nothing is invented."""
    src = re.sub(r'\s+', ' ', ' '.join(K.norm(l) for l in txt.replace('\r', '').split('\n')))
    bad = []
    for k, u in units.items():
        for l in u['text'].splitlines()[1:]:
            if l not in src:
                # a paragraph may run across a page break: check it piecewise
                if not all(seg.strip() in src for seg in re.split(r'(?<=\.) ', l) if seg.strip()):
                    bad.append((k, l[:90]))
    return bad


def rejoin_revision_refs(txt):
    """A citation such as "the Penal Code (2026 Revision)" can wrap so that "(2026 Revision)" stands alone on a line, which
    ky_statute drops as a cover-page line. Put it back on the line it belongs to (the cover's own line follows the
    upper-case title and is left alone)."""
    L = txt.replace('\r', '').split('\n')
    # running page headers such as "SCHEDULE 3  Criminal Procedure Code (2026 Revision)" (two-space gap, which
    # ky_statute's three-space header pattern misses)
    HDR = re.compile(r'\f?\s*(?:(?:SCHEDULE|Schedule|Section|Part|PART)(?: [0-9A-Z]+)?\s{2,}[A-Z][A-Za-z ]+ \(\d{4} Revision\)'
                     r'|[A-Z][A-Za-z ]+ \(\d{4} Revision\)\s{2,}(?:SCHEDULE|Schedule|Section|Part|PART)(?: [0-9A-Z]+)?)\s*')
    L = ['' if HDR.fullmatch(l) else l for l in L]
    for i, l in enumerate(L):
        if re.fullmatch(r'\s*\(\d{4} Revision\)\s*', l):
            j = i - 1
            while j >= 0 and i - j <= 2 and not L[j].strip(): j -= 1
            if j >= 0 and i - j <= 2 and not L[j].strip().isupper() and not re.search(r'\S\s{3,}\S', L[j]) and re.search(r'\b(Code|Act|Law|Rules|Regulations|Order)$', L[j].strip()):
                L[j] = L[j].rstrip() + ' ' + l.strip(); L[i] = ''
    return '\n'.join(L)


def join_wrapped_headings(units):
    """A section heading that wraps leaves its second half as the first body line; put it back in the heading."""
    for k, u in units.items():
        if not k.startswith('sec-'):
            continue
        lines = u['text'].rstrip('\n').split('\n')
        num = lines[0][2:].split('.', 1)[0]
        if len(lines) > 2 and not re.match(r'\d+[A-Z]{0,3}\.', lines[1]) and re.match(r'%s\.' % re.escape(num), lines[2]) and len(lines[1]) < 120:
            u['text'] = '\n'.join([lines[0] + ' ' + lines[1]] + lines[2:]) + '\n'


def split_missed_heading(units):
    """A section whose body misnumbers itself (Interpretation Law 1995 s. 63 reads "64. 63. No Law ...") is not
    seen as a heading by ky_statute; split it out of the section before it, keeping the words as printed."""
    for k in list(units):
        lines = units[k]['text'].rstrip('\n').split('\n')
        for i in range(1, len(lines) - 1):
            m = re.fullmatch(r'(\d+[A-Z]{0,3})\. ([A-Z][^.]{2,120})', lines[i])
            if m and K.key(m.group(1)) not in units and re.match(r'(\d+[A-Z]?\. )?%s\. ' % re.escape(m.group(1)), lines[i + 1]):
                units[k]['text'] = '\n'.join(lines[:i]) + '\n'
                units[K.key(m.group(1))] = {'label': 'Section ' + m.group(1), 'kind': 'sec', 'text': '\n'.join(['# ' + lines[i]] + lines[i + 1:]) + '\n'}
                break
    order = sorted(units, key=lambda x: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', x)])
    snapshot = dict(units); units.clear(); units.update((k, snapshot[k]) for k in order)


def toc_count(txt):
    """Section numbers listed in the Arrangement of Sections."""
    return len(set(re.findall(r'^(\d+[A-Z]{0,3})\. .*?\.{4,}\s*\d+\s*$', txt, re.M)))


def build(st):
    laws, vers, prev, report = {}, [], None, []
    for rev in st['revisions']:
        pdf = here / '.cache' / st['slug'] / ('%s.pdf' % rev['year'])
        txt = rejoin_revision_refs(rd(pdf.with_suffix('.txt')))
        units = K.parse(txt, rev['title_upper'])
        for u in units.values():
            u['text'] = re.sub(r' Page \d+\n', '\n', u['text'])
        split_missed_heading(units)
        join_wrapped_headings(units)
        nsec = len([k for k in units if k.startswith('sec-')])
        report.append((rev['year'], nsec, toc_count(txt), len(units), verify(txt, units)))
        lk = '%s-%s-revision' % (st['slug'], rev['year'])
        url = url_of(st, rev['year'])
        v = {'from': rev['from'], 'source_url': url, 'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(), 'units': units}
        if prev is None:
            v['credits'] = {}
            v['note'] = 'Oldest version available of the %s in this build: the %s Revision, in force from %s.' % (st['title'], rev['year'], rev['from'])
        else:
            v['credits'] = {k: [lk] for k in sorted(set(units) | set(prev)) if units.get(k) != prev.get(k)}
            v['note'] = 'The %s Revision (consolidation published by the Cayman Islands Government).' % rev['year']
        laws[lk] = {'label': '%s (%s Revision)' % (st['title'], rev['year']), 'title': '%s, %s Revision (consolidated and revised text)' % (st['title'], rev['year']),
                    'kind': 'publisher', 'enacted': rev['from'], 'published': rev['from'], 'url': url, 'temporary_until': None, 'restores': None, 'note': None}
        vers.append(v)
        prev = units
    act = {'slug': st['slug'], 'short': st['short'], 'title': st['title'], 'url': url_of(st, st['revisions'][-1]['year']),
           'first_law': None, 'earlier_laws': [], 'versions': vers}
    part = {'acts': [act], 'laws': laws,
            'sources': [{'name': 'Cayman Islands Legislation: %s, Law Revisions %s' % (st['title'], ', '.join(r['year'] for r in st['revisions'])),
                         'url': url_of(st, st['revisions'][-1]['year']), 'retrieved': RETRIEVED,
                         'licence': 'Official legislation; the PDFs carry no licence statement.',
                         'notes': 'Born-digital Law Revision PDFs linked from the legislation history table on legislation.gov.ky.'}],
            'decisions': ['[statutes] %s: %d Law Revision(s) from legislation.gov.ky (%s); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. %s' % (
                st['title'], len(vers), ', '.join(r['year'] for r in st['revisions']), st['decision'])],
            'ai_use': ['none']}
    p = here / 'corpus.d' / (st['part'] + '.json')
    p.parent.mkdir(exist_ok=True)
    t = p.with_suffix('.json.tmp')
    t.write_text(json.dumps(part, ensure_ascii=False, indent=1) + '\n', encoding='utf8', newline='\n')
    os.replace(t, p)
    return report


if __name__ == '__main__':
    want = sys.argv[1:]
    for st in PARTS:
        if want and st['slug'] not in want:
            continue
        for year, nsec, ntoc, nunits, bad in build(st):
            print(st['slug'], year, 'sections', nsec, 'toc', ntoc, 'units', nunits, 'unverified lines', len(bad), bad[:3])
