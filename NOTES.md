# Dead or Alive (PlayStation, Tecmo 1998, US) decomp
Goal: research decomp (names only) + PSX roster/stage notes; publish github.com/indieindie7/deadoralive-psx-decomp. Started 2026-11-02.
Step 0 (11-02): only public item = 3dge7161/Jiggle-or-Physics (static recompilation, generated C, no names, 6 KB repo, 10-02). Not a named decomp -> go on.

## Disc
- Source: Downloads/Dead or Alive.7z -> disc/ (cue + 29 tracks: track 01 MODE2/2352 data, 02-29 CDDA).
- Extract: `py -3.13 -I Documents/Scorcher/tools/isoextract.py "disc/Dead or Alive (Track 01).bin" cd 2352 24` -> cd/ 56 files.
- Serial SLUS-00606 (US; SYSTEM.CNF BOOT cdrom:\SLUS_006.06;1, STACK 801FFF00).
- cd/: SLUS_006.06 (542720+2048 B main exe), MOVIE.EXE (separate FMV player exe), PS_DOA.BIN (46 MB archive), OPENING.STR, ENDING.STR, OMAKE/*.BMP (gallery), SOUND/DA/*.DA.
- SLUS_006.06 PS-X EXE: pc 0x80010e44, t_addr 0x80010000, t_size 0x84800 (end 0x80094800), sp 0x801fff00. ghidra/SLUS.BIN = file from 0x800.
- MOVIE.EXE: pc 0x8010178c, t_addr 0x80100000, t_size 0x8d800. ghidra/MOVIE.BIN = from 0x800.
- PS_DOA.BIN: table of 8-byte entries (u32 size LE + BCD min,sec,frame,0 = absolute LBA, entry 0 at LBA 0; offset=(lba-lba0)*2048), 256 entries. Entry 0 = header + big code (code file 0x2000..0x52000), entry 2 = code (0x72800, 0xd712), entry 4 = code (0x83800, 0x2660); entries 1,3,5..255 data (no code density).
- Overlay load addresses (jal->prologue score, tools/findbase.py style): OV00 and OV02 both at 0x80093420 (same slot, alternate), OV04 at 0x801e8000. OV00 = PS_DOA[0:0x52000], OV02 = [0x72800:+0xd800], OV04 = [0x83800:+0x2800].

## Ghidra
- Project ghidra/DOAPSX, run.sh. MIPS:LE:32:default BinaryLoader + SeedMipsFunctionsAt. Scripts copied from ShamanKing (unchanged).
- 11-02 imported: SLUS (seeds 938), MOVIE (274), OV00 (746), OV02 (86), OV04 (15). funcinfo_<p>.tsv F counts: SLUS 965, MOVIE 301, OV00 752, OV02 87, OV04 15.
- ram_<p>.bin 2 MB RAM images for psxrules.py; rules_/hints_<p>.txt from it.

## Step 0 (11-02)
GitHub search (gh search repos: "dead or alive playstation decompilation", "doa psx decomp", "SLUS_006.06", "dead or alive decompilation"): no PSX DOA decomp found. Proceeding.

## Final state (11-02)
| Program | Base | Functions | FUN_ | Provisional | Globals named |
|---|---|---|---|---|---|
| SLUS_006.06 | 0x80010000 | 1011 | 0 | 0 | 1452 |
| MOVIE.EXE | 0x80100000 | 301 | 0 | 0 | 321 |
| OV00 (PS_DOA.BIN) | 0x80093420 (code from 0x8009554c) | 767 | 0 | 0 | 982 |
| OV02 (same slot as OV00) | 0x80093420 | 87 | 0 | 0 | 97 |
| OV04 | 0x801e8000 | 15 | 0 | 0 | 69 |
Total 2181 functions. Names live in ghidra/hand_<prog>.txt; globals in ghidra/globals/globals_<prog>.txt.

- Orphan pass (tools/orphans.py): SLUS +329 candidates, 283 were data (gap detection) and deleted (ghidra/del_SLUS.txt), 46 real functions named; OV00 +15 (4 named by hand: game_CheckPlayTimeUnlocks, ai_GetFighterTableEntry, camera_IsOutsideViewBox, camera_IsOutsideViewZ).
- Review round 1: SLUS 15 confirmed/63 renamed/7 unsure; MOVIE 26/10/1; OV00 49/10/4. Round 2: all unsure resolved (SLUS 7 renamed, MOVIE 1 and OV00 3 confirmed, 1 renamed). 0 provisional. OV04 dbgpad_InitFontTables keeps a comment: tail of the function is data.
- PsyQ library ids: no sig-file / library source offline, so by strings + call shape. SLUS and MOVIE carry bios.c v1.86 (1997/03/28), intr.c v1.76, sys.c v1.135 and "Library Programs (c) 1993-1997"; OV00 has none. About 80 functions got PsyQ API names (Pad*, Cd*, ResetGraph/DrawSync/LoadImage/DrawOTag/PutDrawEnv, GTE InitGeom/MulMatrix/RotMatrix/SetRotMatrix/RotTransPers4, InitCARD/InitPAD, rcnt) by call shape.
- gp: entry sets gp = 0x800428ac but a binary scan found 0 gp-relative accesses (built without small data), so SetGp is not needed.
- Globals: glscan -> 16 context files -> Sonnet batches -> glmerge_doa.py -> ApplyGlobals (SLUS 1452, MOVIE 321, OV00 982, OV02 97, OV04 69, 0 problems). Names made unique by _<last4hex> suffix where agents collided. Leftover DAT_ in dumps: SLUS 23 / OV02 5 / OV04 1 are inside comment text or non-listed ranges, not code refs.
- Types: structs_DOA.txt defines DOA_PlayerBlock (0x58 per player, g_player_*/g_fighter_* fields at 0x80093c10..0x80093c67; player 1 block at 0x80093c68). Defined in category /DeadOrAlivePSX; not laid over the individually named globals.
- Saturn reuse: agents grepped hand_00DOA.txt (Saturn SH-2 hand names, same game logic) for matching function names; matches only taken where code matched.

## Roster and stages (from strings)
- Roster, 11 fighters, same as Saturn: Kasumi, Ayane, Lei-Fang, Jann-Lee, Zack, Tina, Gen-Fu, Bayman, Raidou, Hayabusa, Bass. No PSX-only fighters in the strings; PSX extras are in modes: TOURNAMENT, VERSUS, TEAM BATTLE, TIME ATTACK, SURVIVAL, KUMITE (30/50/100 challenge), TRAINING, POPULARITY VOTE, reports (TOURNAMENT/VERSUS/TIME ATTACK/SURVIVAL/KUMITE REPORT), NEW COSTUME GET, EXTRA CONFIG OPEN, OPTION, memory card save/load. Disc OMAKE/ holds per-character costume BMP galleries (Kasumi 3, Leifang 3, Tina 3, Zack 3, Jann-Lee 2, Bass 2, Bayman 2, Gen-Fu 1, Raidou 1, Ryu 1).
- Stages: no stage-name strings. Stage data is indexed by tbl_stage_data_cd_index (0x80083434) into PS_DOA.BIN with animated-texture tables (tbl_stage_anim_tex_*); stage loader stage_LoadAll. "SELECT RING TYPE" menu selects the ring.
