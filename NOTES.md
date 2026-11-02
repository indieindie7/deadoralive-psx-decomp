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

## Evidence audit (11-02, rule: no guesswork; tools/evid.py, psyq_match.py, constmatch.py; outputs in evid/)
Every hand line now ends with `[ev:TAGS]`. Anchors: STR = function references a real text string; HW = touches a hw_ MMIO global; GTE = COP2 instructions; LIB = byte-pattern (immediates masked) identical to a function in another PS1 binary (SK, Rakugaki, Ducati); SAT = same name as a Saturn function AND shared callee names; TRIV = body <= 4 instructions (name restates the instruction). `ctx*` tags (name shares a token with a referenced global, or same-prefix call-graph neighbours) are NOT counted as proof (circular, the globals were named by the same readers).
| Program | Functions | Anchored | Context only (unproven) | No anchor (OPEN) |
|---|---|---|---|---|
| SLUS | 1011 | 539 | 367 | 105 |
| MOVIE | 301 | 213 | 62 | 26 |
| OV00 | 767 | 147 | 401 | 219 |
| OV02 | 87 | 25 | 24 | 38 |
| OV04 | 15 | 2 | 9 | 4 |
| Total | 2181 | 926 | 863 | 392 |
**Unproven names (context only + OPEN = 1255) are still OPEN, not done.** List of the 392 with no anchor: evid/open_names.tsv. 48 names are still address-style (stub_/_<addr>).

### PsyQ library identification
No PsyQ .lib, signature file or SDK source exists on this PC (searched). Method used: masked byte-pattern match of every function >= 12 instructions against SK (SLPS), Rakugaki and Ducati World binaries. 394 DOA functions have a library-identical twin (SLUS 267, MOVIE 121, OV00 6): 165 match in 3 games, 141 in 2, 88 in 1. That proves they are shared library code. The exact PsyQ API name is proven only where a reference game's name agrees (SLUS 39, MOVIE 25 of the CamelCase PsyQ-style names); reference names are themselves hand names, so the other library names stay OPEN until a real libgpu/libgte/libspu/libcd/libetc/libapi/libc/libpress/libcard/libsnd binary is available. Full table: evid/psyq_matches.tsv. Libraries are not statically distinguishable per object here (no per-.obj boundaries).

### Saturn name cross-check
The PSX build is a different codebase from the Saturn one (different engine layer), so structural matching is weak. Results (evid/saturn_xcheck.tsv, evid/const_matches.tsv):
| Method | Result |
|---|---|
| Same name and shared callee names | 37 functions confirmed (35 in OV00 fighter/AI code) |
| Callee-set Jaccard >= 0.6, different name | 1 candidate (ai_PickAttackTierAlt vs Saturn ai_PickHitReactionAlt), unverified |
| Numeric-constant set match (>=3 constants, Jaccard >= 0.5) | 42 candidates, only 7 agree by name; the rest are coincidental, rejected |
Saturn names were reused only where the first row holds.

### Types and globals
- DAT_ in code and in comments: 0 in all five programs (SLUS 23, OV02 5, OV04 1 were hand-comment mentions, now replaced with global names).
- Structs defined (/DeadOrAlivePSX): DOA_PlayerHeader (4), DOA_FighterState (0x54), DOA_SndVoice, DOA_SfxEntry, DOA_CdFileEntry, DOA_ThreadSlot, DOA_BodyPoint, DOA_SndSeq (the last six proven by strides in at least two code sites, evidence in structs_DOA2.txt). Applied: g_player0_header 0x80093c10, g_player1_header 0x80093c68, g_fighter_state 0x80093c14, tbl_sfx_a..e, snd_voice_seq_id (single element), tbl_cd_file_entry[512], tbl_thread_state[16], tbl_hit_body_objects[15], tbl_fighter_bone_rot[15]. Negative-offset field fixed (g_title_menu_active was outside the block).
- The earlier 0x58 player stride is NOT proven (g_round_timer_cur sits at 0x80093c88, inside it), so no 0x58 struct is applied.
- 26 tables/structs OPEN (stage, move, camera, sound entry counts or strides not provable from code): ghidra/types_open.txt.

### Stages (data)
tbl_stage_data_cd_index (0x80083434, 16-bit CD file indices, read by the stage loader): entries 0..15 = 0xe8..0xf7 (16 consecutive stage files), then a sparse block (0x10f 0x112 0x116 0x113 0x110 0x118 0x115 0x119 0x11a 0x11d 0x121 0x11e 0x11b 0x123 0x120 0x124, 0x101 0x10c 0xf9 0x104 ...). PS_DOA.BIN contains labels STAGE1..STAGE9 only. No stage names exist in the executable, overlays or OMAKE assets, so **stage names are OPEN** (not guessed). Stage count proven from the table: at least 16.

## Round 3 (11-02): OPEN driven down (rule: no guesswork)
Evidence tier BODY = the name's every claim was checked against the function's own decompile (Sonnet reader, proof phrase stored in the hand_*.txt line and evid/neutral_names.tsv, evid/ctx_verdicts.tsv). It is a single-reader check, weaker than STR/LIB/SAT/GTE/HW anchors (not independently reviewed yet).
- 392 no-anchor names: all renamed to neutral behaviour-only names `<behaviour>_<addr>` (old guess kept in the hand line as "prior unproven guess"). PsyQ/API names that rested on nothing are gone.
- 863 context-only names: 642 body-VERIFIED (tag BODY added), 221 OVERCLAIM renamed neutral `<behaviour>_<addr>`.
- Result: 2181 functions = 926 externally anchored + 1255 BODY-only (642 verified names + 613 neutral names). Name guesses with no check: 0. Real PsyQ/game names for the 613 neutral ones stay unknown (need a real PsyQ lib or a second reader).
- Tables (evid/tables_proof.tsv): 14 PROVEN from code (loop bounds / consistent strides / terminator), 13 BLOCKED with the missing evidence listed there. Player stride 0x58 PROVEN (index (&g_player0_header)[x*0x16] and byte *0x58 at several sites). Not yet applied to the Ghidra types.
- Stages (evid/stages_proof.tsv, stages_proof.txt): stage id = byte at 0x80085a14 (written only in fight_SelectStageIndex 0x800c12cc); N=16 (clamp id>0xf, 16-entry cd table), ids 0..15 -> cd files 0xe8..0xf7, index names stage_00..stage_15. Reachable ids 0 and 3..13; no stage-select menu exists. No stage NAMES exist on disc (ASCII+cp932 searched SLUS, MOVIE, PS_DOA.BIN, OMAKE): names BLOCKED. Correction: PS_DOA.BIN header table has 512 entries, not 256.
- Still BLOCKED: stage names; ids 1,2,14,15 have no producer; cd table entries >=16 no proven reader; library API names; 13 tables.

## Round 4 (11-02)
- Types applied in Ghidra (pass12.sh + OV00 bss block 0x800e5420..0x800f0000 + glob13): 13 of 14 proven tables typed (ushort[15] ranking, uint[2] model ptrs, short[90] title logo, ptr seq base, short[2] joint flags in SLUS; int[4], uint[80] random rows (OV00+OV02), uint[124] posture, byte[9], int[2], char[2], DOA_AnimInit[33] in OV00) plus DOA_Player[2] (stride 0x58 = DOA_PlayerHeader 4 + DOA_FighterState 0x54) at g_player0_header. Decompile verified: tbl_posture_data indexed as uint array, g_player0_header[+1]. snd_voice_seq_id (count 24 x 0x36 overlaps spu_voice_bit_table) NOT retyped: conflict unresolved.
- Blind second check of the 642 body-verified names: random sample 100 by a fresh reviewer: 99 pass, 1 fail (800704f8, renamed store_byte_call_snd_set_reverb_volume_800704f8). Fail rate 1% (< 5% threshold), so no full pass; remaining 542 unsampled stay single-checked + 100 double-checked.

## Round 5 (11-02)
- Stage names: evid/stage_names.tsv, shots evid/stage_shots/. All 16 ids render when forced (1,2,14,15 included); no producer writes them (watched 0x80085a14, 60000 vb: only ids 5 and 0xb). Only id 5 named (Zack's stage, fan wiki, medium). 15 OPEN: no public PS1 stage list.
- Tables: evid/tables_proof2.tsv, pass13.sh, dec14_*.c. 14 typed, 5 BLOCKED (tbl_sfx_b..e runtime index; movie entry/frames count unbounded; part_flags size from runtime header; effect_piece_set count; vibration scripts no reader). snd_voice_seq_id = DOA_SndVoice[24]; spu_voice_bit_table dead (flag never set) -> spu_shadow_regs_dead_80049c38. cd entries >=16 = fighter model tables, typed.
- Full blind review of remaining 542: 536 PASS, 6 FAIL (1.1%), fails renamed. Combined 642 names: 635 pass, 7 fixed.
- PsyQ names (evid/psyq_open_names.tsv, open sources only: psx-spx BIOS tables, PSn00bSDK): 10 APPLY (8 applied, 2 need function creation at 80015b0c, 800161ec), 648 BLOCKED (libgpu/pad/cd/snd/mdec/libc internals need leaked lib to match).
