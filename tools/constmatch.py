# constmatch.py: ISA-independent function match PSX vs Saturn: sets of distinctive numeric literals plus callee-name sets.
# usage: py -3.13 -I constmatch.py <ghidra dir> <out dir>
import re,sys,collections
G=sys.argv[1]; O=sys.argv[2]
SATD='<SATURN>/decomp_00DOA.c'
def bodies(path):
    d={}; cur=None
    for l in open(path,errors='replace'):
        m=re.match(r'// ==== (\S+) @ ([0-9a-f]+)',l)
        if m: cur=(m.group(1),m.group(2)); d[cur]=[]
        elif cur: d[cur].append(l)
    return d
def feats(lines):
    t=''.join(lines); t=re.sub(r'/\*.*?\*/','',t,flags=re.S)
    cs=set()
    for x in re.findall(r'\b0x[0-9a-fA-F]+\b|\b\d+\b',t):
        v=int(x,16) if x.startswith('0x') else int(x)
        if 0x20<=v<0x100000 and v not in (0x100,0x1000,0x80,0xff,0xffff,0x7f,0x3f): cs.add(v)
    calls=set(re.findall(r'\b([A-Za-z]\w+)\s*\(',t))-{'if','while','for','switch','return','sizeof'}
    return cs,calls
sat=bodies(SATD); sf={k:feats(v) for k,v in sat.items()}
rows=[]
for pn in ['SLUS','MOVIE','OV00','OV02','OV04']:
    for k,v in bodies('%s/dec8_%s.c'%(G,pn)).items():
        cs,ca=feats(v)
        if len(cs)<3: continue
        best=None
        for sk,(sc,sca) in sf.items():
            if len(sc)<3: continue
            i=len(cs&sc)
            if i<3: continue
            j=i/len(cs|sc)
            j2=len(ca&sca)/max(1,len(ca|sca))
            sc_=j+0.5*j2
            if j>=0.5 and (best is None or sc_>best[0]): best=(sc_,sk[0],sk[1],j,j2,i)
        if best: rows.append((pn,k[1],k[0],best[1],best[2],round(best[3],2),round(best[4],2),best[5]))
with open(O+'/const_matches.tsv','w') as o:
    for r in rows: o.write('\t'.join(map(str,r))+'\n')
print(len(rows),sum(1 for r in rows if r[2]==r[3]))
