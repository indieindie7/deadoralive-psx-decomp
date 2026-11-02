#!/bin/bash
cd <WORK>/ghidra
G='<WORK>\ghidra'
for p in SLUS OV00; do
 A=$(cat orph_$p.txt | tr '\n' ' ')
 bash run.sh $PWD/logs/create3_$p.log -process $p.BIN -noanalysis -postScript CreateAt.java $A >/dev/null
 bash run.sh $PWD/logs/export3_$p.log -process $p.BIN -noanalysis -readOnly -postScript ExportFuncInfo.java "$G"'\'"funcinfo3_$p.tsv" >/dev/null
 echo done $p >> logs/pass3.done
done
