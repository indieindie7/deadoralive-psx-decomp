#!/bin/bash
cd <WORK>/ghidra
G='<WORK>\ghidra'
for p in SLUS MOVIE OV00 OV02 OV04; do
 bash run.sh $PWD/logs/dump5_$p.log -process $p.BIN -noanalysis -readOnly -postScript CsDumpAll.java "$G"'\'"dec5_$p.c" >/dev/null
 [ -f funcinfo4_$p.tsv ] || cp funcinfo2_$p.tsv funcinfo4_$p.tsv
 echo done $p >> logs/pass5.done
done
