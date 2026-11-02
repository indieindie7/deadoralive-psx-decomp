import re,sys,collections,csv
G='C:/Users/john/Documents/DeadOrAlive/psx/ghidra'
HW=[(0x1f801040,0x1f80104f,'pad'),(0x1f801050,0x1f80105f,'sio'),(0x1f801070,0x1f801077,'irq'),(0x1f801080,0x1f8010ff,'dma'),(0x1f801100,0x1f80112f,'rcnt'),(0x1f801800,0x1f801803,'cd'),(0x1f801810,0x1f801817,'gpu'),(0x1f801820,0x1f801827,'mdec'),(0x1f801c00,0x1f801fff,'spu'),(0x1f801000,0x1f80103f,'memctl')]
def parse(p):
    F={};cur=None
    for l in open('%s/funcinfo5_%s.tsv'%(G,p),errors='replace'):
        f=l.split()
        if not f:continue
        if f[0]=='F':cur=f[1];F[cur]={'name':f[2],'size':int(f[4]),'C':[],'S':[]}
        elif f[0]=='C' and cur:F[cur]['C'].append(f[1])
        elif f[0]=='S' and cur:F[cur]['S'].append(' '.join(f[1:]))
    return F
def bodies(p):
    b={};cur=None
    for l in open('%s/dec9_%s.c'%(G,p),errors='replace'):
        m=re.match(r'// ==== (\S+) @ ([0-9a-f]+)',l)
        if m:cur=m.group(2);b[cur]=[]
        elif cur:b[cur].append(l)
    return {k:''.join(v) for k,v in b.items()}
def hwset(b):
    s=set()
    for m in re.finditer(r'0x(1f80[0-9a-f]{4}|bf80[0-9a-f]{4})',b,re.I):
        v=int(m.group(1),16)|0x1f800000 if m.group(1).startswith('bf80') else int(m.group(1),16)
        v=0x1f800000|(v&0xffff)
        for lo,hi,n in HW:
            if lo<=v<=hi:s.add(n)
    for m in re.finditer(r'\bhw_([a-z]+)',b):s.add(m.group(1))
    return s
