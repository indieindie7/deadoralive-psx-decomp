#!/bin/bash
cd <WORK>/ghidra
G='<WORK>\ghidra'
for p in SLUS MOVIE OV00; do
 bash run.sh $PWD/logs/apply7_$p.log -process $p.BIN -noanalysis -postScript ApplyNames.java "$G"'\'"hand_$p.txt" >/dev/null
 bash run.sh $PWD/logs/export7_$p.log -process $p.BIN -noanalysis -readOnly -postScript ExportFuncInfo.java "$G"'\'"funcinfo4_$p.tsv" >/dev/null
 bash run.sh $PWD/logs/dump7_$p.log -process $p.BIN -noanalysis -readOnly -postScript CsDumpAll.java "$G"'\'"dec7_$p.c" >/dev/null
 echo done $p >> logs/pass7.done
done
