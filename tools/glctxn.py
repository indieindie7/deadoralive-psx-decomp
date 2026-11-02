import sys, re, collections
# glctxn.py <full.c> <globals.txt> <addr list> <out prefix> <parts> [maxlines]: like glctx.py but for globals that
# already carry a name (weak-name round): finds usage lines by name in a dump made after ApplyGlobals.
mx = int(sys.argv[6]) if len(sys.argv) > 6 else 5
name = {l.split()[0]: l.split()[1] for l in open(sys.argv[2]) if l.strip()}
want = {name[a.strip()]: a.strip() for a in open(sys.argv[3]) if a.strip() in name}
pat = re.compile(r'\b(' + '|'.join(map(re.escape, want)) + r')\b')
lines = collections.defaultdict(list); seen = collections.defaultdict(set); fn = None
for l in open(sys.argv[1], encoding='utf-8', errors='replace'):
    m = re.match(r'// ==== (\S+) @', l)
    if m: fn = m.group(1); continue
    if fn is None or l.lstrip().startswith(('/*', '*')): continue
    for n in set(pat.findall(l)):
        if fn not in seen[n] and len(lines[n]) < mx:
            seen[n].add(fn); lines[n].append('  %s: %s' % (fn, l.strip()[:180]))
items = sorted(want.items(), key=lambda kv: kv[1]); k = int(sys.argv[5]); per = -(-len(items) // k)
for i in range(k):
    with open('%s%d.txt' % (sys.argv[4], i + 1), 'w') as o:
        for n, a in items[i * per:(i + 1) * per]:
            o.write('%s now %s\n%s\n' % (a, n, '\n'.join(lines[n])))
print(len(items), 'per', per, 'no usage', sum(1 for n in want if not lines[n]))
