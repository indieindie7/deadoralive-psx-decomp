# Dead or Alive (PlayStation, Tecmo, 1998) reverse-engineering notes and symbols

Hand-named function map, naming prompts, globals and tools for **Dead or Alive** (SLUS-00606, PS1): main exe `SLUS_006.06`
(MIPS R3000 + GTE, PsyQ, base 0x80010000), `MOVIE.EXE` (0x80100000) and the overlays of `PS_DOA.BIN`
(OV00 and OV02 share the slot at 0x80093420, OV04 at 0x801e8000). The Saturn version has its own map in deadoralive-decomp.

| Program | Functions | Named | Provisional | Globals |
|---|---|---|---|---|
| SLUS_006.06 | 1,011 | 1,011 | 0 | 1,452 |
| MOVIE.EXE | 301 | 301 | 0 | 321 |
| OV00 | 767 | 767 | 0 | 982 |
| OV02 | 87 | 87 | 0 | 97 |
| OV04 | 15 | 15 | 0 | 69 |

0 `FUN_` left; no `DAT_` references left in code. Method as in shamanking-decomp: Ghidra headless seeds functions, `psxrules.py` names BIOS stubs,
hinted dumps are sliced and named by agents, orphan scan for missed code, two review rounds, then globals and structs.
Non-commercial, for study and preservation. **No game data is included** (no disc, exe, overlays, decompiled C or game text).

## What is here

| Path | Content |
|---|---|
| `NOTES.md` | disc layout, overlays, counts, PsyQ id method, gp finding, roster and modes |
| `ghidra/hand_<prog>.txt` | hand names `0x<addr> func <name> hand <comment>` (ApplyNames.java) |
| `ghidra/funcinfo_<prog>.tsv` | per-function export (F address name source size, C callees) |
| `ghidra/del_SLUS.txt` | 283 data blocks wrongly seen as functions, deleted |
| `ghidra/naming/prompt_DOAPSX.txt`, `ghidra/review/` | naming prompt, review prompt and round 1 and 2 verdicts |
| `ghidra/globals/` | `globals_<prog>.txt` (`0x<addr> <name>`), `structs_DOA.txt` (DOA_PlayerBlock), naming prompt |
| `ghidra/scripts/` | Java scripts: ApplyNames, ApplyGlobals, DefineStructs, CreateAt, DeleteFunctions, ExportFuncInfo, CsDumpAll, Seed*, SetGp, AddBss |
| `ghidra/run.sh`, `ghidra/pass*.sh` | headless job chains (paths use `<WORK>` placeholders) |
| `tools/` | psxrules, injecthints, slice, mergehand, orphans, provctx3, srprovapply, glscan, glctx, glctxn, glmerge, glmerge_doa, glplan, findbase, psdoa_scan |

MIT licence for notes, names and tools. Dead or Alive belongs to its rights holders.
