"""mergehand.py: rules + agent hand files -> one hand file (rules win, first name per address, unique names).
    py -3.13 -I mergehand.py <out> <rules> <agent files...>"""
import re, sys
out, srcs = sys.argv[1], sys.argv[2:]
pat = re.compile(r'^0x([0-9a-fA-F]{8}) func (\S+) hand ?(.*)$')
got, used, bad = {}, {}, 0
for s in srcs:
    for l in open(s, encoding='utf-8', errors='replace'):
        m = pat.match(l.strip())
        if not m:
            bad += bool(l.strip()); continue
        a = int(m.group(1), 16)
        if a in got: continue
        n = m.group(2)
        if n in used: n = '%s_%08x' % (n, a)
        used[n] = a; got[a] = (n, m.group(3))
with open(out, 'w', encoding='utf-8') as w:
    for a in sorted(got): w.write('0x%08x func %s hand %s\n' % (a, *got[a]))
print(out, len(got), 'bad', bad)
