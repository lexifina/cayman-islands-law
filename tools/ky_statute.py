"""Cayman Islands: parse a Law Revision PDF text (pdftotext -layout) into section units. Reads files only."""
import re

SEC = re.compile(r'^(\d+[A-Z]{0,3})\.? (\S.*)$')
MARK = re.compile(r'^(\(\w{1,6}\)|"|\d+[A-Z]?\.\s|[-•]\s)')


def norm(s):
    s = s.replace(' ', ' ').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '--').replace('\f', '')
    return re.sub(r'[ \t]+', ' ', s).strip()


def key(num):
    m = re.fullmatch(r'(\d+)([A-Z]*)', num)
    return 'sec-%03d%s' % (int(m.group(1)), ('-' + m.group(2).lower()) if m.group(2) else '')


def is_head(L, i):
    m = SEC.match(L[i])
    if not m or L[i].startswith(' ') or re.match(r'^\d+[A-Z]*\.? \(', L[i]):
        return None
    j = i + 1
    seen = 0
    while j < len(L) and seen < 3:
        t = L[j]
        if t.strip():
            seen += 1
            if SEC.match(t) and not t.startswith(' ') and not t.strip().startswith(m.group(1) + '.'):
                return None
            if t.strip().startswith(m.group(1) + '.'):
                return m
        j += 1
    return None


def parse(txt, title_upper, tail_markers=('Table of Legislation history', 'ENDNOTES')):
    L = txt.replace('\r', '').split('\n')
    # body start: first "N. Heading" at column 0 whose next non-blank line is the indented "N. text"
    start = None
    for i in range(len(L)):
        m = is_head(L, i)
        if m and m.group(1) == '1':
            start = i
            break
    if start is None:
        raise ValueError('no body start')
    end = len(L)
    for i in range(start, len(L)):
        if re.match(r'^(Table of Legislation history|ENDNOTES|Publication in consolidated and revised form|Notes:)', L[i].strip()) and i > start + 20:
            end = i
            break
    noise = [re.compile(p) for p in (
        r'^\s*c\s+Revised as at .*$', r'^.*Revised as at .*Page \d+\s*(c)?\s*$', r'^\s*Page \d+\s+Revised as at .*$',
        r'(?i)^\s*(?:(?:Section|Part|Schedule|Arrangement of Sections|Endnotes).*?\s{3,})?' + re.escape(title_upper) + r' \(\d{4} Revision\)(?:\s{3,}.*)?$',
        r'^\s*(Section|Part|Schedule|Arrangement of Sections)\b.*?\s{3,}' + re.escape(title_upper.title()) + r'\s*$', r'^\s*' + re.escape(title_upper.title()) + r'\s{3,}(Section|Part|Schedule|Arrangement of Sections)\b.*$',
        r'^\s*CAYMAN ISLANDS\s*$', r'^\s*\(\d{4} Revision\)\s*$', r'^\s*' + re.escape(title_upper) + r'\s*$')]
    out = []  # list of (kind, num, heading, [lines])
    cur = None
    part_head = False
    for idx, l in enumerate(L[start:end]):
        if any(p.match(l) for p in noise):
            continue
        s = l.strip()
        if re.match(r'^(PART|Part) [0-9IVXLC]+\b', s) and (len(l) - len(l.lstrip())) >= 12:
            part_head = True
            continue
        if part_head:
            if not s:
                part_head = False
            continue
        if re.fullmatch(r'(SCHEDULE|Schedule) \d+[A-Z]?|(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH) SCHEDULE|SCHEDULE', s):
            cur = ['sched', s, s, []]
            out.append(cur)
            continue
        m = is_head(L, start + idx)
        if m:
            cur = ['sec', m.group(1), norm(m.group(2)), []]
            out.append(cur)
            continue
        if cur is not None:
            cur[3].append(l)
    units = {}
    order = []
    for kind, num, head, lines in out:
        paras = []
        buf = ''
        for l in lines:
            s = norm(l)
            if not s:
                if buf:
                    paras.append(buf)
                buf = ''
                continue
            if buf and MARK.match(s):
                paras.append(buf)
                buf = s
            else:
                buf = (buf + ' ' + s) if buf else s
        if buf:
            paras.append(buf)
        if kind == 'sec':
            k = key(num)
            label = 'Section ' + num
            body = ['# %s. %s' % (num, head)] + paras
        else:
            mm = re.search(r'\d+[A-Z]?', num)
            n = mm.group(0) if mm else str(len([1 for u in order if u.startswith('sched-')]) + 1)
            k = 'sched-' + (('%03d' % int(re.match(r'\d+', n).group(0)) + n[len(re.match(r'\d+', n).group(0)):].lower()) if re.match(r'\d', n) else n)
            label = head.title() if head.isupper() else head
            body = ['# ' + head] + paras
        if k in units:
            k = k + '-dup%d' % len(order)
        units[k] = {'label': label, 'kind': 'sec' if kind == 'sec' else 'schedule', 'text': '\n'.join(body) + '\n'}
        order.append(k)
    return units
