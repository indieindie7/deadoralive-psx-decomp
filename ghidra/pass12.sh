#!/bin/bash
cd /c/Users/john/Documents/DeadOrAlive/psx/ghidra
G='C:\Users\john\Documents\DeadOrAlive\psx\ghidra'
for p in SLUS MOVIE OV00 OV02 OV04; do
 bash run.sh $PWD/logs/ds12_$p.log -process $p.BIN -noanalysis -postScript DefineStructs.java "$G"'\'"structs_DOA_all.txt" "/DeadOrAlivePSX" >/dev/null
 bash run.sh $PWD/logs/apply12_$p.log -process $p.BIN -noanalysis -postScript ApplyNames.java "$G"'\'"hand_$p.txt" >/dev/null
 bash run.sh $PWD/logs/glob12_$p.log -process $p.BIN -noanalysis -postScript ApplyGlobals.java "$G"'\'"globals_$p.txt" >/dev/null
 bash run.sh $PWD/logs/dump12_$p.log -process $p.BIN -noanalysis -readOnly -postScript CsDumpAll.java "$G"'\'"dec12_$p.c" >/dev/null
 echo done $p >> logs/pass12.done
done
