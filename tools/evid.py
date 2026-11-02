# evid.py: per-function evidence tags for DOA PSX names. usage: py -3.13 -I evid.py <ghidra dir> <out dir>
import re,sys,collections,os
G=sys.argv[1]; O=sys.argv[2]; PR=['SLUS','MOVIE','OV00','OV02','OV04']
SAT='<SATURN>/funcinfo_00DOA.tsv'
def parse(tsv):
    F={}; cur=None
    for l in open(tsv,errors='replace'):
        f=l.split()
        if not f: continue
        if f[0]=='F': cur=f[1]; F[cur]={'name':f[2],'size':int(f[4]),'C':[],'S':[]}
        elif f[0]=='C' and cur: F[cur]['C'].append(f[1])
        elif f[0]=='S' and cur: F[cur]['S'].append(' '.join(f[1:]))
    return F
def toks(n): return set(t.lower() for t in re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+',n) if len(t)>2)
sat=parse(SAT); satn={v['name']:a for a,v in sat.items()}
def calleenames(F,a,addr2name): return set(addr2name[c] for c in F[a]['C'] if c in addr2name)
satA2N={a:v['name'] for a,v in sat.items()}
satcs={a:calleenames(sat,a,satA2N) for a in sat}
lib={}
for l in open(O+'/psyq_matches.tsv'): 
    p=l.rstrip('\n').split('\t'); lib[(p[0],p[1])]=p[4].split()
GENERIC=re.compile(r'^(stub_|FUN_)|_[0-9a-f]{8}$')
tot=collections.Counter(); out={}; report=[]; xcheck=[]
for pn in PR:
    F=parse('%s/funcinfo5_%s.tsv'%(G,pn)); a2n={a:v['name'] for a,v in F.items()}
    # dump bodies
    body={}; cur=None
    for l in open('%s/dec8_%s.c'%(G,pn),errors='replace'):
        m=re.match(r'// ==== (\S+) @ ([0-9a-f]+)',l)
        if m: cur=m.group(2); body[cur]=[]
        elif cur: body[cur].append(l)
    tags={}
    for a,v in F.items():
        t=set(); b=''.join(body.get(a,[]))
        if any(re.search(r'[A-Za-z]{3,}',s) and not re.fullmatch(r'[0-9a-fA-F ]+',s) for s in v['S']): t.add('STR')
        if re.search(r'\bhw_|0x1f80[0-9a-f]{4}|0xbf80',b): t.add('HW')
        if re.search(r'setCopReg|getCopReg|copFunction|CopControlWord',b): t.add('GTE')
        if (pn,a) in lib: t.add('LIB')
        gl=set(re.findall(r'\b((?:g|tbl|hw|buf|pad|cd|gpu|spu|card|krn|s)_[A-Za-z0-9_]+)',b))
        nt=toks(v['name'])
        if any(nt&toks(g) for g in gl): t.add('ctxGLOB')
        if v['size']<=16 and not (t-{'ctxGLOB'}): t.add('TRIV')
        # saturn
        cn=calleenames(F,a,a2n); nm=v['name']
        if nm in satn:
            sa=satn[nm]; sc=satcs[sa]
            if (cn&sc) or (not cn and not sc): t.add('SAT'); xcheck.append((pn,a,nm,'name+callee',nm,len(cn&sc),len(cn),len(sc)))
        elif len(cn)>=2:
            best=None
            for sa,sc in satcs.items():
                j=len(cn&sc)/max(1,len(cn|sc))
                if j>=0.6 and (best is None or j>best[0]): best=(j,sa)
            if best: xcheck.append((pn,a,nm,'callee-set',satA2N[best[1]],round(best[0],2),len(cn),0))
        tags[a]=t
    # chain pass
    rev=collections.defaultdict(set)
    for a,v in F.items():
        for c in v['C']:
            if c in F: rev[c].add(a)
    for a,v in F.items():
        if tags[a]-{'ctxGLOB'}: continue
        pre=v['name'].split('_')[0]
        nb=set(c for c in v['C'] if c in F)|rev[a]
        good=[n for n in nb if tags[n] and F[n]['name'].split('_')[0]==pre and not GENERIC.search(F[n]['name'])]
        if len(good)>=2: tags[a].add('ctxCHAIN')
    out[pn]=(F,tags)
    c=collections.Counter()
    for a,t in tags.items(): c['proven' if any(not x.startswith('ctx') for x in t) else ('weak' if t else 'OPEN')]+=1
    weak=sum(1 for v in F.values() if GENERIC.search(v['name']))
    report.append((pn,len(F),'proven',c['proven'],'ctxonly',c['weak'],'OPEN',c['OPEN'],'weaknames',weak))
    with open('%s/ev_%s.tsv'%(O,pn),'w') as o:
        for a,t in sorted(tags.items()): o.write('%s\t%s\t%s\n'%(a,F[a]['name'],','.join(sorted(t)) or 'OPEN'))
for r in report: print(*r)
with open(O+'/saturn_xcheck.tsv','w') as o:
    for x in xcheck: o.write('\t'.join(map(str,x))+'\n')
print('xcheck',len(xcheck))
