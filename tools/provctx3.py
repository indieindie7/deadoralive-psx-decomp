# provctx3.py: review contexts for every provisional line of a hand file, from a CsDumpAll dump made AFTER
# ApplyNames (so callee/caller names are current). Entry = body + callee names + up to 2 caller bodies (cut).
# usage: py -3.13 -I provctx3.py <dump.c> <funcinfo.tsv> <hand.txt> <PROG> <out prefix> <per file>
import re, sys
dump, fi, hand, prog, outp, per = sys.argv[1:7]; per = int(per)
body, cur = {}, None
for l in open(dump, encoding='utf-8', errors='replace'):
    m = re.match(r'// ==== (\S+) @ ([0-9a-fA-F]+)', l)
    if m: cur = int(m.group(2), 16); body[cur] = []
    if cur is not None: body[cur].append(l.rstrip('\n'))
names, callees, cf = {}, {}, None
for l in open(fi, encoding='utf-8', errors='replace'):
    t = l.split()
    if not t: continue
    if t[0] == 'F': cf = int(t[1], 16); names[cf] = t[2]; callees[cf] = []
    elif t[0] == 'C' and cf is not None: callees[cf].append(int(t[1], 16))
callers = {}
for a, cs in callees.items():
    for c in set(cs): callers.setdefault(c, []).append(a)
items = []
for l in open(hand, encoding='utf-8', errors='replace'):
    if 'provisional' not in l: continue
    t = l.split(None, 4)
    a = int(t[0], 16); items.append((a, t[2], t[4].strip() if len(t) > 4 else ''))
def cut(a, n):
    b = body.get(a, ['// (no decompile)'])
    return b if len(b) <= n else b[:n] + ['  ... (%d more lines)' % (len(b) - n)]
for k in range(0, len(items), per):
    o = []
    for a, n, c in items[k:k + per]:
        o.append('#### %s 0x%08x %s | %s' % (prog, a, n, c))
        o += cut(a, 150)
        ce = sorted({names.get(x, '%x' % x) for x in callees.get(a, [])})
        o.append('---- callees: ' + (' '.join(ce) if ce else '(none)'))
        cl = callers.get(a, [])
        o.append('---- callers: %d (%s)' % (len(cl), ' '.join(names.get(x, '%x' % x) for x in cl[:8])))
        for x in cl[:2]: o += cut(x, 70)
        o.append('')
    p = '%s%d.txt' % (outp, k // per + 1)
    open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(o) + '\n')
    print(p, len(items[k:k + per]), len(o))
