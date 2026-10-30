"""Cayman Islands: Constitution Order 2009 as made (UKSI 2009/1379), from legislation.gov.ky. Reads .cache only."""
import json, re, hashlib, subprocess
from pathlib import Path
here = Path(__file__).parent
pdf = here / '.cache' / 'order2009.pdf'
sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
txt = subprocess.run(['pdftotext', '-enc', 'UTF-8', '-layout', str(pdf), '-'], capture_output=True, text=True, encoding='utf8').stdout
NL = chr(10)


def norm(s):
    s = s.replace(' ', ' ').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = re.sub(r'\.{4,}', '', s)
    return re.sub(r'[ \t]+', ' ', s).strip()


lines = []
for l in txt.split(NL):
    s = l.strip()
    if s.startswith('Document Generated') or s.startswith('Status: This is the original') or s.startswith('item of legislation is currently'):
        continue
    if re.fullmatch(r'\d{1,3}', s):
        continue
    lines.append(l.replace('\f', ''))


def idx(pat, start=0):
    return next(i for i in range(start, len(lines)) if re.fullmatch(pat, lines[i].strip()))


def ind(l):
    return len(l) - len(l.lstrip())


i_order = next(i for i, l in enumerate(lines) if l.strip().startswith('Citation and commencement'))
i_s1 = idx(r'SCHEDULE 1')
i_s2 = idx(r'SCHEDULE 2')
i_const = next(i for i, l in enumerate(lines) if l.strip() == 'THE CONSTITUTION OF THE CAYMAN ISLANDS')
i_end = idx(r'EXPLANATORY NOTE')
titles = {}
for l in lines[i_s2:i_const]:
    m = re.match(r'\s*(\d+)\.\s+(.+)$', l)
    if m:
        titles[int(m.group(1))] = norm(m.group(2))
assert max(titles) == 129 or max(titles) == 125, max(titles)


def paragraphs(block):
    paras = []
    first_is_item = False
    for l in block:
        if not l.strip():
            continue
        s = norm(l)
        starts = ind(l) > 0 and re.match(r'^(\(\w{1,5}\)|\d+\.\S*)(\s|$)', s) is not None
        if not paras or starts or (ind(l) == 0 and first_is_item):
            paras.append(s)
            first_is_item = ind(l) >= 5 and re.match(r'^(\([a-z]{1,3}\)|\([ivx]+\))', s) is not None
        else:
            paras[-1] += ' ' + s
    return paras


def mk(label, title, block):
    return {'label': label, 'kind': 'section', 'text': '# ' + label + ('. ' + title if title else '') + NL + NL.join(paragraphs(block)) + NL}


units = {}
body = lines[i_const:i_end]
j = next(i for i, l in enumerate(body) if l.strip().startswith('Now, therefore'))
ps = []
for l in body[1:j + 1]:
    if not l.strip():
        continue
    s = norm(l)
    if re.match(r'^(A |Affirm|Now|The people)', s) or not ps:
        ps.append(s)
    else:
        ps[-1] += ' ' + s
units['preamble'] = {'label': 'Preamble', 'kind': 'preamble', 'text': '# Preamble' + NL + NL.join(ps) + NL}
exp = 1
cur = []
cur_n = None


def close():
    global cur
    if cur_n is not None:
        blk = cur
        t = titles.get(cur_n)
        if t is None:
            t = norm(cur[0]).split('. ', 1)[1]
            blk = cur[1:]
        units['sec-%03d' % cur_n] = mk('Section %d' % cur_n, t, blk)
    cur = []


for l in body[j + 1:]:
    s = l.strip()
    if not s:
        cur.append(l)
        continue
    if re.fullmatch(r'PART [IVX]+', s) or (s.upper() == s and re.search('[A-Z]', s) and not s[0].isdigit() and not s.startswith('(')):
        continue
    m = re.match(r'^(\d+)\.(\s|—)', s)
    if m and int(m.group(1)) == exp and ind(l) > 0:
        close()
        cur_n = exp
        exp += 1
        cur = [l]
        continue
    if exp in titles and ind(l) == 0 and norm(s) == titles[exp]:
        continue
    cur.append(l)
close()
print('constitution sections', exp - 1)

ob = lines[i_order:i_s1]
exp_o = 1
cur = []
cur_n = None
unit_o = {}
heads_o = {}
last_head = 'Citation and commencement'
for l in ob:
    s = l.strip()
    if not s:
        cur.append(l)
        continue
    m = re.match(r'^(\d+)\.(\s|—)', s)
    if m and int(m.group(1)) == exp_o and ind(l) > 0:
        if cur_n is not None:
            unit_o[cur_n] = cur
        cur_n = exp_o
        heads_o[exp_o] = last_head
        exp_o += 1
        cur = [l]
        continue
    if s == 'Citation and commencement' and exp_o == 1:
        continue
    if ind(l) == 0 and len(s) < 60 and not re.search(r'[.;:,]$', s) and not s.startswith('(') and cur_n is not None:
        last_head = norm(s)
        continue
    if ind(l) == 0 and re.match(r'^\(\d+\) ', s) and re.search(r'S\.I\.|c\.', s):
        continue
    if re.match(r'^(Judith Simpson|Clerk of the Privy)', s):
        continue
    cur.append(l)
unit_o[cur_n] = cur
oacts = {}
for n, blk in unit_o.items():
    oacts['art-%03d' % n] = mk('Article %d' % n, heads_o[n], blk)
sch1 = [norm(l) for l in lines[i_s1:i_s2] if l.strip() and norm(l) not in ('SCHEDULE 1', 'Revocations')]
oacts['schedule-1'] = {'label': 'Schedule 1', 'kind': 'schedule', 'text': '# Schedule 1. Revocations' + NL + NL.join(sch1) + NL}
print('order articles', sorted(oacts))

LAW = 'si-2009-1379'
URL = 'https://legislation.gov.ky/cms/legislation/constitution/current.html?download=55:the-cayman-islands-constitution-order-2009-uksi-1379-2009'
corpus = {
    'country': {'code': 'KY', 'name': 'Cayman Islands', 'slug': 'cayman-islands', 'lang': 'en', 'tz': 'America/Cayman', 'future_branch': 'future',
                'publisher': {'name': 'Cayman Islands Government, Legislation Unit (legislation.gov.ky)', 'email': 'legislation@legislation-gov-ky.invalid'},
                'default_in_force_rule': {'text': "The Cayman Islands Constitution Order 2009 came into force on the day the Governor appointed by proclamation (section 1(2)); this first build dates its one version from the day the Order was made, the source's own date.", 'source': URL},
                'licence_note': 'Text from the Cayman Islands Government legislation site, https://legislation.gov.ky: the Cayman Islands Constitution Order 2009 (SI 2009/1379) as originally made.'},
    'sources': [{'name': 'Cayman Islands Legislation, Constitution (current)', 'url': 'https://legislation.gov.ky/cms/legislation/constitution/current.html', 'retrieved': '2026-10-29', 'requests': 5, 'licence': 'Official legislation; the PDF carries no licence statement.', 'notes': 'robots.txt of legislation.gov.ky checked 2026-10-29: it disallows only system folders under /cms/ (administrator, cache, components and similar) and /cms/search/; the constitution pages and downloads are not disallowed.'}],
    'laws': {LAW: {'label': 'SI 2009/1379', 'title': 'The Cayman Islands Constitution Order 2009 (SI 2009 No. 1379)', 'kind': 'decree', 'enacted': '2009-06-10', 'published': '2009-06-10', 'url': URL, 'temporary_until': None, 'restores': None, 'note': None}},
    'acts': [
        {'slug': 'constitution', 'short': 'Const.', 'title': 'The Constitution of the Cayman Islands (Schedule 2 to the Cayman Islands Constitution Order 2009)', 'url': URL, 'first_law': None, 'earlier_laws': [],
         'versions': [{'from': '2009-06-10', 'source_url': URL, 'sha256': sha, 'units': units, 'note': 'The Constitution as made by the Order of 10 June 2009. It came into force on the day appointed by the Governor, and Part I (Bill of Rights) three years later; the source gives neither date, so the version is dated from the day the Order was made.'}]},
        {'slug': 'constitution-order-2009', 'short': 'Order', 'title': 'The Cayman Islands Constitution Order 2009: the Order itself (articles 1 to 9 and Schedule 1)', 'url': URL, 'first_law': None, 'earlier_laws': [],
         'versions': [{'from': '2009-06-10', 'source_url': URL, 'sha256': sha, 'units': oacts}]}],
    'applies': [],
    'decisions': ['Only the Constitution Order 2009 as made is recorded. The Cayman Islands Constitution (Amendment) Orders 2016 (UKSI 780/2016) and 2020 (UKSI 1283/2020) amend it; they are not replayed in this first build, so the text here is not the current Constitution.',
                  'The version is dated 10 June 2009, the day the Order was made, because the source does not give the appointed day.',
                  "Section headings come from the Order's own contents list; footnotes, page headers and the signature were left out."],
    'ai_use': ['none']}
json.dump(corpus, open(here / 'corpus.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(len(units), len(oacts))
