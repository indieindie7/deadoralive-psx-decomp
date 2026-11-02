#!/bin/bash
cd <WORK>/ghidra
G='<WORK>\ghidra'
for p in SLUS MOVIE OV00 OV02 OV04; do
 bash run.sh $PWD/logs/apply8_$p.log -process $p.BIN -noanalysis -postScript ApplyNames.java "$G"'\'"hand_$p.txt" >/dev/null
 bash run.sh $PWD/logs/glob8_$p.log -process $p.BIN -noanalysis -postScript ApplyGlobals.java "$G"'\'"globals_$p.txt" >/dev/null
 bash run.sh $PWD/logs/export8_$p.log -process $p.BIN -noanalysis -readOnly -postScript ExportFuncInfo.java "$G"'\'"funcinfo5_$p.tsv" >/dev/null
 bash run.sh $PWD/logs/dump8_$p.log -process $p.BIN -noanalysis -readOnly -postScript CsDumpAll.java "$G"'\'"dec8_$p.c" >/dev/null
 echo done $p >> logs/pass8.done
done
