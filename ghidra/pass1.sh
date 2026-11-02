#!/bin/bash
# apply rules names, re-export funcinfo, dump decomp (one Ghidra job at a time)
cd <WORK>/ghidra
G='<WORK>\ghidra'
for p in SLUS MOVIE OV00 OV02 OV04; do
 bash run.sh $PWD/logs/apply_$p.log -process $p.BIN -noanalysis -postScript ApplyNames.java "$G"'\'"rules_$p.txt" >/dev/null
 bash run.sh $PWD/logs/dump_$p.log -process $p.BIN -noanalysis -readOnly -postScript CsDumpAll.java "$G"'\'"decomp_$p.c" >/dev/null
 echo done $p >> logs/pass1.done
done
