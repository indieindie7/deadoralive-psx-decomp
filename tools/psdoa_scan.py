# psdoa_scan.py <PS_DOA.BIN>: list table entries (u32 size + BCD msf) and MIPS code density per entry.
import struct, sys
b = open(sys.argv[1], 'rb').read()
bcd = lambda x: (x >> 4) * 10 + (x & 15)
ents = []
off = 0
first = struct.unpack_from('<I', b, 0)[0]
base = None
while off < 0x800:
    sz = struct.unpack_from('<I', b, off)[0]; m, s, f = b[off+4], b[off+5], b[off+6]
    if sz == 0 and m == 0 and s == 0: break
    ents.append((sz, (bcd(m) * 60 + bcd(s)) * 75 + bcd(f))); off += 8
print('entries', len(ents))
# the table maps to absolute LBAs; find base of file: smallest lba whose data starts at offset
l0 = ents[0][1]
for i, (sz, lba) in enumerate(ents):
    o = (lba - l0) * 2048
    if o + 4 > len(b): print(i, 'beyond', sz, lba); continue
    d = b[o:o + min(sz, 65536)]
    w = len(d) // 4
    pro = sum(1 for k in range(w) if struct.unpack_from('<I', d, 4*k)[0] >> 16 == 0x27bd and (struct.unpack_from('<I', d, 4*k)[0] & 0x8000))
    jr = sum(1 for k in range(w) if struct.unpack_from('<I', d, 4*k)[0] == 0x03e00008)
    print(i, hex(o), hex(sz), d[:4].hex(), 'pro', pro, 'jr', jr, 'MAGIC' if d[:8] == b'PS-X EXE' else '')
