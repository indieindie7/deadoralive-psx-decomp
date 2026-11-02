# glplan.py <ghidra dir>: split globals into naming groups -> ctx_DOA_<n>.txt (+ glgroups.txt). Groups: main (SLUS + shared addrs seen by overlays),
# MOVIE-local, OV00 slot-local, OV02 slot-local, OV04-local. usage: py -3.13 -I glplan.py <dir>
import sys, re, subprocess, os
d = sys.argv[1]
def rd(p):
    return {int(l.split()[0], 16): l.strip() for l in open(os.path.join(d, 'gl_%s.txt' % p)) if l.startswith('0x')}
G = {p: rd(p) for p in ['SLUS', 'MOVIE', 'OV00', 'OV02', 'OV04']}
SLOT = (0x80093420, 0x800e5400)
grp = {'main': dict(G['SLUS'])}
def lowshared(a): return a < 0x80010000 or (0x1f800000 <= a < 0x1f810000)
for p in ['MOVIE', 'OV00', 'OV02', 'OV04']:
    loc = {}
    for a, l in G[p].items():
        if a in grp['main'] and not (SLOT[0] <= a < SLOT[1]) : continue
        if lowshared(a): grp['main'].setdefault(a, l); continue
        if p != 'MOVIE' and a < 0x80093420: grp['main'].setdefault(a, l); continue
        loc[a] = l
    if loc: grp[p] = loc
for g, m in grp.items():
    print(g, len(m))
# write combined dump for glctx
with open(os.path.join(d, 'all5.c'), 'w', encoding='utf-8') as o:
    for p, f in [('SLUS', 'dec7_SLUS.c'), ('OV00', 'dec7_OV00.c'), ('OV02', 'dec5_OV02.c'), ('OV04', 'dec5_OV04.c'), ('MOVIE', 'dec7_MOVIE.c')]:
        if not os.path.exists(os.path.join(d, f)): f = 'dec5_%s.c' % p
        o.write(open(os.path.join(d, f), encoding='utf-8', errors='replace').read())
n = 0
for g, m in grp.items():
    with open(os.path.join(d, 'glgrp_%s.txt' % g), 'w') as o:
        for a in sorted(m): o.write(m[a] + '\n')
    subprocess.run([sys.executable, '-I', os.path.join(d, '..', 'tools', 'glctx.py'), os.path.join(d, 'all5.c'), os.path.join(d, 'glgrp_%s.txt' % g), os.path.join(d, 'ctxfull_%s.txt' % g), '4'], check=True)
    L = open(os.path.join(d, 'ctxfull_%s.txt' % g)).read().split('\n0x')
    L = [('0x' + x if not x.startswith('0x') else x) for x in L if x.strip()]
    # chunk by entries
    for i in range(0, len(L), 220):
        n += 1
        with open(os.path.join(d, 'ctx_DOA_%d.txt' % n), 'w') as o:
            o.write('### PROGRAM %s\n' % g); o.write('\n'.join(L[i:i + 220]) + '\n')
        print('ctx_DOA_%d.txt' % n, g, len(L[i:i + 220]))
