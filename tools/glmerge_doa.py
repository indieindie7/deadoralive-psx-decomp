# glmerge_doa.py <ghidra dir>: gn_DOA_<n>.txt (order = ctx_DOA_<n>.txt, "### PROGRAM <group>") -> globals_<prog>.txt for ApplyGlobals.
# main group names apply to every program that references the address (outside the overlay slot); local groups only to their program.
import re, sys, os
d = sys.argv[1]
SLOT = (0x80093420, 0x800e5400)
grp = {}; used = set()
n = 1
while os.path.exists(os.path.join(d, 'ctx_DOA_%d.txt' % n)):
    ctx = open(os.path.join(d, 'ctx_DOA_%d.txt' % n), encoding='utf-8').read().splitlines()
    gn = [l.split() for l in open(os.path.join(d, 'gn_DOA_%d.txt' % n), encoding='utf-8') if l.strip()]
    prog, k = None, 0
    for l in ctx:
        m = re.match(r'### PROGRAM (\S+)', l)
        if m: prog = m.group(1); continue
        if not l.startswith('0x'): continue
        a = int(l.split()[0], 16); ga, name = int(gn[k][0], 16), gn[k][1]; k += 1
        assert ga == a, (n, hex(a), hex(ga))
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name): name = 'g_var_%08x' % a
        key = prog + name
        if (prog if prog != 'main' else 'main', name) in used: name += '_%04x' % (a & 0xffff)
        used.add((prog, name)); grp.setdefault(prog, {})[a] = name
    assert k == len(gn), (n, k, len(gn))
    n += 1
for p in ['SLUS', 'MOVIE', 'OV00', 'OV02', 'OV04']:
    refs = {int(l.split()[0], 16) for l in open(os.path.join(d, 'gl_%s.txt' % p)) if l.startswith('0x')}
    out = {}
    for a in refs:
        if a in grp.get('main', {}) and not (p != 'SLUS' and SLOT[0] <= a < SLOT[1] and p != 'MOVIE'): out[a] = grp['main'][a]
        if p in grp and a in grp[p]: out[a] = grp[p][a]
    seen = {}
    for a in sorted(out):
        if out[a] in seen: out[a] += '_%04x' % (a & 0xffff)
        seen[out[a]] = a
    with open(os.path.join(d, 'globals_%s.txt' % p), 'w') as o:
        for a in sorted(out): o.write('0x%08x %s\n' % (a, out[a]))
    print(p, len(out), 'of', len(refs))
