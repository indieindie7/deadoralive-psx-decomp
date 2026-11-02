# psyq_match.py: byte-pattern (immediate-masked) function match of DOA PSX programs against other PS1 binaries
# whose functions are named. usage: py -3.13 -I psyq_match.py <out.tsv>
import struct,re,sys,collections
H='<LOCAL>
D=H+'DeadOrAlive/psx/ghidra/'
refs=[('SK',H+'ShamanKing/ghidra/SLPS.BIN',0x80010000,H+'ShamanKing/ghidra/funcinfo_SLPS.tsv'),
      ('RK',H+'Rakugaki/ghidra/rkram.bin',0x80000000,H+'Rakugaki/ghidra/funcinfo_rkram.tsv'),
      ('DW',H+'DucatiWorld/ghidra/dwram.bin',0x80000000,H+'DucatiWorld/ghidra/funcinfo_0.tsv')]
progs=[('SLUS',0x80010000),('MOVIE',0x80100000),('OV00',0x80093420),('OV02',0x80093420),('OV04',0x801e8000)]
def funcs(tsv):
    out=[]
    for l in open(tsv,errors='replace'):
        f=l.split()
        if len(f)>=5 and f[0]=='F': out.append((int(f[1],16),f[2],int(f[4])))
    return out
def norm(buf):
    n=len(buf)//4; ws=struct.unpack('<%dI'%n,buf[:n*4]); hi=set(); out=[]
    for w in ws:
        op=w>>26; rs=(w>>21)&31; rt=(w>>16)&31; rd=(w>>11)&31
        if op in(2,3): out.append(w>>26)
        elif op==0x0f: hi.add(rt); out.append(w&0xffff0000)
        elif op==0: hi.discard(rd); out.append(w)
        elif 8<=op<=0x2f or 0x30<=op<=0x3b:
            if rs in hi: v=w&0xffff0000
            else: v=w
            if op in(8,9,0xa,0xb,0xc,0xd,0xe) or 0x20<=op<=0x26:
                if not(op in(9,0xd) and rs in hi): hi.discard(rt)
            out.append(v)
        else: out.append(w)
    return tuple(out)
def load(path,base,tsv):
    d=open(path,'rb').read(); r={}
    for a,nm,sz in funcs(tsv):
        o=a-base
        if o<0 or o+sz>len(d) or sz<48: continue
        r.setdefault(hash(norm(d[o:o+sz])),[]).append((nm,a,sz))
    return r
R=[(t,load(p,b,f)) for t,p,b,f in refs]
res=[]
for pn,base in progs:
    d=open(D+pn+'.BIN','rb').read()
    for a,nm,sz in funcs(D+'funcinfo5_%s.tsv'%pn):
        o=a-base
        if o<0 or o+sz>len(d) or sz<48: continue
        h=hash(norm(d[o:o+sz])); m=[]
        for t,r in R:
            for (rn,ra,rsz) in r.get(h,[]): m.append('%s:%s@%x'%(t,rn,ra))
        if m: res.append((pn,a,nm,sz,m))
with open(sys.argv[1],'w') as o:
    for pn,a,nm,sz,m in res: o.write('%s\t%08x\t%s\t%d\t%s\n'%(pn,a,nm,sz,' '.join(m)))
print(len(res))
