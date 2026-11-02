# findbase.py <bin> <skip hex> <len hex> [step]: guess PSX load base by jal->prologue hits inside the blob.
import struct, sys, collections
b = open(sys.argv[1], 'rb').read(); s = int(sys.argv[2], 16); n = int(sys.argv[3], 16); d = b[s:s+n]
w = struct.unpack('<%dI' % (len(d)//4), d[:len(d)//4*4])
tg = collections.Counter((x & 0x3ffffff) << 2 | 0x80000000 for x in w if x >> 26 == 3)
pro = [i for i, x in enumerate(w) if x >> 16 == 0x27bd and x & 0x8000]
best = []
for base in range(0x80010000, 0x80200000, 0x4):
    hit = 0
    for t, c in tg.items():
        o = (t - base) // 4
        if 0 <= o < len(w) and w[o] >> 16 == 0x27bd and w[o] & 0x8000: hit += c
    best.append((hit, base))
best.sort(reverse=True); print(len(tg), 'targets', [(h, hex(b_)) for h, b_ in best[:5]])
