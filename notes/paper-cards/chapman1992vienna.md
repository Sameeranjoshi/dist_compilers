# Programming in Vienna Fortran

**Catalog id:** `chapman1992vienna`  
**Citation:** Chapman, B., Mehrotra, P., Zima, H. "Programming in Vienna Fortran." NASA CR-189623 / ICASE Report 92-9, March 1992; journal version: Scientific Programming 1(1):31-50, 1992, DOI 10.1155/1992/258136. Open copy: https://ntrs.nasa.gov/citations/19920013037  
**Paper type:** language  
**Access:** open (NASA NTRS report) — full text read. The ICASE report was read for this card; the journal version is the catalog's primary record.  
**Card status:** full-read

## Problem
Using a hand-parallelized Jacobi relaxation (Figs. 1-2), Sec. 2 argues that message-passing code hard-wires the distribution: local arrays with overlap areas, guarded sends and receives and the owner-computes convention must all be rewritten to try another blocking. The report presents the FORTRAN 77 version of Vienna Fortran so programs use global addresses while the user controls distribution (Sec. 1); a Fortran 90 variant is deferred.

## Input abstraction
Sec. 3.3 overviews the extensions: `PROCESSORS` with `RESHAPE`, load-time bounds and assertions; `$P`, `$NP`, `$MY_PROC`. `DIST(...)` with an optional `TO` clause naming a processor array, subset or permutation; `BLOCK`, `CYCLIC`, `CYCLIC(width)`, elision `:`, `=A.d`, `INDIRECT(map array)`, and user-defined distribution functions, shown in Sec. 5.2 as a `DFUNCTION` with an implicit `TARGET`. `ALIGN target WITH source` using bound variables and linear expressions. `DYNAMIC`, `RANGE`, `CONNECT`, `DISTRIBUTE ... :: ... NOTRANSFER`; `SELECT DCASE`; `ALLOCATABLE` arrays distributed after `ALLOCATE`; distributed arrays in named common; dummies with `DIST(*)`, `RESTORE`, `NOCOPY`, `RANGE`. A `FORALL` loop with private variables, an `ON` clause and `REDUCE` (ADD, MULT, MAX, MIN or user-defined); only tightly nested FORALLs are allowed.

## Target
Intel hypercube series and NCUBE are the named machine class (Sec. 1). The Vienna Fortran Compilation System generates code for the Intel iPSC/860, GENESIS and SUPRENUM (Sec. 7).

## Data decomposition
Block in even segments, cyclic (scatter), cyclic with width, 2-D block grids, default replication of undistributed arrays and scalars, replication across uncovered processor dimensions, distribution to subsets, alignment (Sec. 4.1 shows an alignment giving 28/28/28/16 elements versus 25 each for `DIST(=ZX)`), INDIRECT mapping arrays, user-defined functions (edges mapped to the owner of their first node, Sec. 5.2), and dynamic redistribution with `NOTRANSFER` suppressing data motion. Generated code keeps local parts plus overlap areas (Sec. 3.1). Arbitrary rectilinear blocks are implemented (Sec. 7). Common-block arrays may not be dynamic (Sec. 5.3).

## Computation mapping
Sec. 2 names owner computes as the hand-written SPMD convention; Sec. 3.1 adopts SPMD. FORALL iterations run on a named processor, on the owner of a datum (`ON OWNER(EDGE(I,1))`, Sec. 5.2), or as the compiler decides (Sec. 3.2). Reductions are applied by the system after all iterations (Sec. 5.2). For DO loops no rule is stated beyond producing code "similar to" the hand version (Sec. 4.1).

## Communication generation
The compiler inserts message passing for non-local references, combining messages and sending early (Sec. 1). Column blocks need vectors from two neighbours; square blocks fewer items but four messages (Sec. 4.1). Redistribution, at a subroutine boundary or via `DISTRIBUTE`, is an all-to-all transpose (Sec. 5.1). Non-local FORALL inputs can be gathered beforehand; indirect references need run-time techniques from Kali and PARTI (Sec. 5.2). Implemented optimizations: interprocedural communication analysis, matching access patterns to aggregate communication routines, redundant-communication elimination, fusion of communication statements, PARTI-based irregular access optimization (Sec. 7).

## Compiler / runtime split
Processor counts bind at load time; `DISTRIBUTE` and `ALLOCATE` evaluate distributions at run time (Secs. 3.3, 5.3). `RANGE` and `DCASE` supply distribution facts when interprocedural analysis fails or compilation is separate (Sec. 4.2). Sec. 7 reports interprocedural distribution analysis/propagation and procedure cloning; dynamic distributions are still being implemented.

## Evaluation
No quantitative evaluation. Sec. 7 gives status only: static distributions, rectilinear blocks, inherited distributions, FORALL and the listed optimizations are done; dynamic distributions are under way.

## Principal limitation
Stated: dynamic distributions are unimplemented and efficient user-defined distribution and alignment functions remain open research (Sec. 7); inherited distributions can starve the compiler of information while explicit dummy distributions can force costly redistribution (Sec. 4.2). Our observation: the Jacobi performance comparison is qualitative only.

## Relationship to earlier / later work
Sec. 1 lists contemporaneous proposals (Yale extensions, DEC's HPF proposal, Cray MPP Fortran, Fortran D, Steele's HPF amendments) and the Kali/SUPERB/MIMDizer prototypes. Sec. 6 discusses BLAZE, Kali (strong influence), DINO, Booster, Yale Extensions (bijective maps, no replication), Fortran D (executable, dynamic-only alignment; authors prefer direct mapping), Fortran 90D/CM Fortran, DEC and Cray extensions, SUPERB, the Kali compiler's inspector/executor, MIMDizer, ASPAR, Pandore, Id Nouveau, Crystal, SIMD compilers, the AL compiler, PARTI and Koelbel & Mehrotra. Sec. 7 states VFCS builds on SUPERB and uses PARTI. Secs. 3.3 and 5.1 cite the authors' 1991 report.

## Sources used
| claim | section / page |
|---|---|
| Hand-parallelized Jacobi, overlap areas, owner computes | Sec. 2, pp. 3-6 |
| SPMD model; feature list incl. FORALL ON options | Secs. 3.1-3.2, pp. 6-8 |
| Full construct overview | Sec. 3.3, pp. 8-14 |
| Jacobi distributions; alignment vs =ZX; subroutines, RANGE, DCASE | Sec. 4, pp. 14-21 |
| ADI transpose; INDIRECT, DFUNCTION, FORALL/REDUCE; common/allocatable | Sec. 5, pp. 21-30 |
| Related work | Sec. 6, pp. 30-33 |
| VFCS targets, status, optimizations | Sec. 7, pp. 33-34 |

## Open questions for the survey
- How were DFUNCTION and INDIRECT distributions represented at run time alongside PARTI?
- Does the Scientific Programming version differ from the report (e.g. Sec. 7 status)?
- Did "compiler-determined" FORALL placement default to owner computes in VFCS?
