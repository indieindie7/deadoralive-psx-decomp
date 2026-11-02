# orphans.py: code no Ghidra function owns (pointer-table handlers, leaf fns) in a PSX exe / overlay.
# usage: py -3.13 -I orphans.py <bin> <base hex> <funcinfo.tsv> <code end hex> [extra ptr-source bin base]
# Prints candidate entries: jal/data-pointer targets outside functions, plus gap starts and words after a jr ra delay slot.
import sys, struct, bisect
b = open(sys.argv[1], 'rb').read(); B = int(sys.argv[2], 16); end = int(sys.argv[4], 16)
fs = []
for l in open(sys.argv[3], encoding='utf-8', errors='replace'):
    f = l.split()
    if f and f[0] == 'F':
        n = [int(x) for x in f[3:] if x.isdigit()]; fs.append((int(f[1], 16), n[0] if n else 0))
fs.sort(); st = [a for a, _ in fs]
def owned(x):
    i = bisect.bisect_right(st, x) - 1; return i >= 0 and x < fs[i][0] + fs[i][1]
W = lambda a: struct.unpack_from('<I', b, a - B)[0]
lo = fs[0][0]
def okins(w):  # rough MIPS sanity: known primary opcodes
    op = w >> 26
    return w == 0 or op in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 46, 50, 58)
cand = {}
src = [(b, B)]
if len(sys.argv) > 6: src.append((open(sys.argv[5], 'rb').read(), int(sys.argv[6], 16)))
for m, mb in src:
    for i in range(0, len(m) - 3, 4):
        w = struct.unpack_from('<I', m, i)[0]
        t = ((w & 0x3ffffff) << 2) | 0x80000000 if w >> 26 == 3 else w
        if lo <= t < end and t % 4 == 0 and not owned(t) and W(t) != 0: cand[t] = 'ref'
a = lo
while a < end:
    if owned(a): a += 4; continue
    s = a
    while s < end and not owned(s) and W(s) == 0: s += 4
    if s >= end or owned(s): a = s; continue
    # region of unowned non-zero code: split after each jr ra + delay slot
    e = s; ok = True; start = s
    while e < end and not owned(e):
        w = W(e)
        if not okins(w): ok = False; break
        if w == 0x03e00008:
            if ok and start not in cand: cand[start] = 'gap'
            e += 8
            while e < end and not owned(e) and W(e) == 0: e += 4
            start = e; continue
        e += 4
    a = e + 4 if not ok else e
for t in sorted(cand): print('0x%08x %s' % (t, cand[t]))
