#!/bin/bash
# headless Ghidra on the DOAPSX project. usage: run.sh <abs log> <args...>
log="$1"; shift
cd <WORK>/ghidra || exit 1
cmd //c "<LOCAL> <WORK>\ghidra DOAPSX $* -scriptPath ${SP:-<WORK>\ghidra\scripts}" < /dev/null > "$log" 2>&1
tail -2 "$log"
