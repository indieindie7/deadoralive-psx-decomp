#!/bin/bash
cd /c/Users/john/Documents/DeadOrAlive/psx/ghidra
G='C:\Users\john\Documents\DeadOrAlive\psx\ghidra'
bash run.sh $PWD/logs/mk14_SLUS.log -process SLUS.BIN -noanalysis -postScript CreateAt.java 80015b0c 800161ec >/dev/null
for p in SLUS MOVIE OV00 OV02 OV04; do
 bash run.sh $PWD/logs/apply14_$p.log -process $p.BIN -noanalysis -postScript ApplyNames.java "$G"'\'"hand_$p.txt" >/dev/null
 bash run.sh $PWD/logs/ds14_$p.log -process $p.BIN -noanalysis -postScript DefineStructs.java "$G"'\'"structs_DOA_all.txt" "/DeadOrAlivePSX" >/dev/null
 bash run.sh $PWD/logs/glob14_$p.log -process $p.BIN -noanalysis -postScript ApplyGlobals.java "$G"'\'"globals_$p.txt" >/dev/null
 bash run.sh $PWD/logs/export14_$p.log -process $p.BIN -noanalysis -readOnly -postScript ExportFuncInfo.java "$G"'\'"funcs14_$p.tsv" >/dev/null
 echo done $p >> logs/pass14.done
done
