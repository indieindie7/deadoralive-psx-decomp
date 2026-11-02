#!/bin/bash
cd <LOCAL>
G='<WORK>\ghidra'
bash run.sh $PWD/logs/ds9.log -process SLUS.BIN -noanalysis -postScript DefineStructs.java "$G"'\'"structs_DOA_all.txt" "/DeadOrAlivePSX" >/dev/null
for p in SLUS MOVIE OV00 OV02 OV04; do
 bash run.sh $PWD/logs/apply9_$p.log -process $p.BIN -noanalysis -postScript ApplyNames.java "$G"'\'"hand_$p.txt" >/dev/null
 bash run.sh $PWD/logs/glob9_$p.log -process $p.BIN -noanalysis -postScript ApplyGlobals.java "$G"'\'"globals_$p.txt" >/dev/null
 bash run.sh $PWD/logs/dump9_$p.log -process $p.BIN -noanalysis -readOnly -postScript CsDumpAll.java "$G"'\'"dec9_$p.c" >/dev/null
 echo done $p >> logs/pass9.done
done
