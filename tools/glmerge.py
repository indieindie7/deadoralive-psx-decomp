# glmerge.py: merge Sonnet global-name files gn_SK_<n>.txt (order = ctx_SK_<n>.txt) into ApplyGlobals lists.
# usage: py -3.13 -I glmerge.py <ghidra dir>  -> globals_SLPS.txt (main) + globals_O_<x>.txt (overlay-local + main)
import re, sys, os
d = sys.argv[1]
MAIN = ['1', '2a', '2b', '3', '4', '5']; OVL = ['6a', '6b', '7']
progs = {}; used = set()
def load(n, default):
    ctx = open(os.path.join(d, 'ctx_SK_%s.txt' % n), encoding='utf-8').read().splitlines()
    gn = [l.split() for l in open(os.path.join(d, 'gn_SK_%s.txt' % n), encoding='utf-8') if l.strip()]
    prog, k = default, 0
    for l in ctx:
        m = re.match(r'### PROGRAM (\S+)', l)
        if m: prog = m.group(1); continue
        if not l.startswith('0x'): continue
        a = l.split()[0].lower(); ga, name = gn[k][0].lower(), gn[k][1]; k += 1
        assert ga == a, (n, a, ga)
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name): name = 'g_var_' + a[-4:]
        key = (prog if prog != 'SLPS' else '', name)
        if name in used: name = '%s_var_%s' % (name, a[-4:])
        used.add(name)
        progs.setdefault(prog, []).append((int(a, 16), name))
for n in MAIN: load(n, 'SLPS')
for n in OVL: load(n, 'O_MINI')
main = sorted(progs['SLPS'])
for p, lst in progs.items():
    out = sorted(lst) if p == 'SLPS' else sorted(lst) + main
    open(os.path.join(d, 'globals_%s.txt' % p), 'w', newline='\n').write(''.join('0x%08x %s\n' % x for x in out))
    print(p, len(lst), len(out))
