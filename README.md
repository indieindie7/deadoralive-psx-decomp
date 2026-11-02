# Dead or Alive (PlayStation, Tecmo, 1998) reverse-engineering notes and symbols

Hand-named function map, naming prompts, globals and tools for **Dead or Alive** (SLUS-00606, PS1): main exe `SLUS_006.06`
(MIPS R3000 + GTE, PsyQ, base 0x80010000), `MOVIE.EXE` (0x80100000) and the overlays of `PS_DOA.BIN`
(OV00 and OV02 share the slot at 0x80093420, OV04 at 0x801e8000). The Saturn version has its own map in deadoralive-decomp.

| Program | Functions | FUN_ | Anchored by evidence | Context only | No anchor (OPEN) | Globals |
|---|---|---|---|---|---|---|
| SLUS_006.06 | 1,011 | 0 | 539 | 367 | 105 | 1,393 |
| MOVIE.EXE | 301 | 0 | 213 | 62 | 26 | 321 |
| OV00 | 767 | 0 | 147 | 401 | 219 | 982 |
| OV02 | 87 | 0 | 25 | 24 | 38 | 97 |
| OV04 | 15 | 0 | 2 | 9 | 4 | 69 |

Every hand line ends in `[ev:...]`. Only 926 of 2,181 names are anchored (string, hw register, GTE, byte-identical library twin in another PS1 game, Saturn match). The other 1,255 are NOT proven and are open. See NOTES.md (evidence audit).
0 `FUN_` and 0 `DAT_` left. Method as in shamanking-decomp: Ghidra headless seeds functions, `psxrules.py` names BIOS stubs,
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
| `ghidra/globals/` | `globals_<prog>.txt` (`0x<addr> <name>`), `structs_DOA.txt`, `structs_DOA2.txt`, `structs_DOA_all.txt`, `gtypes_DOA2.txt`, `types_open.txt`, naming prompt |
| `ghidra/scripts/` | Java scripts: ApplyNames, ApplyGlobals, DefineStructs, CreateAt, DeleteFunctions, ExportFuncInfo, CsDumpAll, Seed*, SetGp, AddBss |
| `ghidra/run.sh`, `ghidra/pass*.sh` | headless job chains (paths use `<WORK>` placeholders) |
| `evid/` | per-function evidence tags (`ev_<prog>.tsv`), `open_names.tsv`, `psyq_matches.tsv`, `saturn_xcheck.tsv`, `const_matches.tsv` |
| `tools/` | psxrules, injecthints, slice, mergehand, orphans, provctx3, srprovapply, glscan, glctx, glctxn, glmerge, glmerge_doa, glplan, findbase, psdoa_scan, evid, psyq_match, constmatch |

MIT licence for notes, names and tools. Dead or Alive belongs to its rights holders.
