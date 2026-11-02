#!/bin/bash
cd <WORK>/ghidra
G='<WORK>\ghidra'
for p in SLUS MOVIE OV00 OV02 OV04; do
 bash run.sh $PWD/logs/apply2_$p.log -process $p.BIN -noanalysis -postScript ApplyNames.java "$G"'\'"hand_$p.txt" >/dev/null
 bash run.sh $PWD/logs/export2_$p.log -process $p.BIN -noanalysis -readOnly -postScript ExportFuncInfo.java "$G"'\'"funcinfo2_$p.tsv" >/dev/null
 echo done $p >> logs/pass2.done
done
