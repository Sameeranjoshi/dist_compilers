# Reading Paths

Curated paths through the catalog for different readers.  The README's
"Start here" list is generated from the `start_here` field of
`catalog/papers.yaml`; this page explains the rationale and adds paths for
specific goals.

## Path 1 — Newcomer (the README "Start here" list)

1. **Foundational map.** Zima & Chapman 1993 (Proc. IEEE) then Benkner &
   Zima 1999: what a distributed-memory compiler must do, before and after HPF.
2. **Global arrays and owner-computes.** Callahan & Kennedy 1988; the Kali
   report (Mehrotra & Van Rosendale 1990) and Koelbel & Mehrotra 1991; the
   Fortran D CACM article (Hiranandani, Kennedy, Tseng 1992).
3. **Automatic distribution.** Li & Chen 1991 (alignment); Ramanujam &
   Sadayappan 1991 (distribution from dependences); PARADIGM (Banerjee et
   al. 1995).
4. **Irregular computation.** Saltz et al. 1990 (inspector–executor), then
   the open ICASE reports 90-59 and 91-73.
5. **Automatic MPI generation.** Bondhugula 2013 (and the open 2011 report);
   Molly (Kruse 2014).
6. **Modern distributed tensors.** GSPMD; Alpa; PartIR; DISTAL/SpDISTAL; the
   shared MLIR stencil stack (Bisbas et al. 2024) and its wafer-scale
   extension (Stawinoga et al. 2026).

## Path 2 — "I know ML sharding, show me the history"

GSPMD → Mesh-TensorFlow → HPF specification (PROCESSORS/DISTRIBUTE) → Fortran
D CACM article → Kali report → Saltz 1990.  Then `docs/historical-claims.md`
for the rediscovery hypotheses.

## Path 3 — "I know HPF, show me what changed"

Kennedy, Koelbel, Zima 2007 (why HPF faded) → Legion 2012 → GSPMD → Alpa →
PartIR → MLIR shard dialect documentation.

## Path 4 — Irregular and sparse

Saltz 1990 → Saltz, Berryman, Wu 1991 → Das et al. 1991/1994 → Ponnusamy et
al. 1995 → Hwang et al. 1995 → Ravishankar et al. 2015 → SpDISTAL 2022 →
Vaidya et al. 2025.

## Path 5 — Spatial and wafer-scale

Kung 1982 (systolic) → Rocki et al. 2020 → Jacquelin et al. 2022 → Bisbas et
al. 2024 → Stawinoga et al. 2026.
