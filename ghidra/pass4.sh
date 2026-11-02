#!/bin/bash
cd <WORK>/ghidra
G='<WORK>\ghidra'
bash run.sh $PWD/logs/del4.log -process SLUS.BIN -noanalysis -postScript DeleteFunctions.java $(cat del_SLUS.txt | tr '\n' ' ') >/dev/null
for p in SLUS OV00; do
 bash run.sh $PWD/logs/apply4_$p.log -process $p.BIN -noanalysis -postScript ApplyNames.java "$G"'\'"hand_$p.txt" >/dev/null
 bash run.sh $PWD/logs/export4_$p.log -process $p.BIN -noanalysis -readOnly -postScript ExportFuncInfo.java "$G"'\'"funcinfo4_$p.tsv" >/dev/null
 echo done $p >> logs/pass4.done
done
