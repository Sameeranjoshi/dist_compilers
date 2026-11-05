# Vienna Fortran: A Fortran Language Extension for Distributed Memory Multiprocessors

**Catalog id:** `chapman1991vienna`  
**Citation:** Chapman, B., Mehrotra, P., Zima, H. "Vienna Fortran — A Fortran Language Extension for Distributed Memory Multiprocessors." NASA CR-187634 / ICASE Report 91-72, September 1991 (to appear in Saltz & Mehrotra, eds., Languages, Compilers and Runtime Environments for Distributed Memory Machines, Elsevier). No DOI. Open copy: https://ntrs.nasa.gov/citations/19920002452  
**Paper type:** language  
**Access:** open (NASA NTRS report) — full text read.  
**Card status:** full-read

## Problem
The report states that message-passing programming of machines like the iPSC or NCUBE forces users to spell out all synchronization and communication, which is tedious, error prone and discourages experimentation (Sec. 1). Prototypes (Kali, SUPERB, MIMDizer) already accept global references plus a distribution; Vienna Fortran is a machine-independent FORTRAN 77 extension in that line with broader mapping facilities, including alignment and dynamic redistribution. Only the "basic" language is covered; the full language and compilation model are deferred (Secs. 1, 2.5).

## Input abstraction
`PROCESSORS P2D(R,R) ASSERT R .GE. 8` declares a processor array with a load-time bound; `RESHAPE` gives secondary views; `$P`, `$NP`, `$PL` are implicit (Sec. 2.1). Arrays carry `DIST` with one function per dimension: `BLOCK`, `CYCLIC`, `CYCLIC(K)`, elision `:`; the "context rank" must match a processor structure (Sec. 2.2). Alignment uses `DISTRIBUTION(A)` (`=A`), `=(A.d)`, `PERMUTE`, `TRANSPOSE` (Sec. 2.2). `DYNAMIC` arrays may carry a `RANGE` of admissible distributions; `CONNECT` ties secondary arrays to a primary one; `DISTRIBUTE A :: dex NOTRANSFER(...)` redistributes a primary array and its connect set; `INDIRECT(B)` maps elements through a mapping array (Sec. 2.2). Formal parameters support enforced distributions, `RESTORE`, `NOTRANSFER`, `NOCOPY` and `DIST(*)` inheritance (Sec. 2.3). Queries use `==` with `*` and `?K` patterns and `SELECT DCASE` (Sec. 2.4). Parallel loops and on clauses exist but are undefined here (Sec. 2.5).

## Target
Intel iPSC series, NCUBE and transputer systems are named as the motivating machine class (Sec. 1); no compilation target or implementation is given. A processor declaration implies no topology (Sec. 2.1).

## Data decomposition
Block, cyclic, block-cyclic, elided dimensions, 2-D block on 2-D processor arrays, alignment-derived distributions (`B(11:60) DIST(=A)` keeps A's block sizes; `C(50) DIST(=A)` does not), dynamic redistribution and element-wise INDIRECT (Sec. 2.2). Undistributed arrays and scalars are conceptually single copies the compiler may replicate and must keep consistent (Sec. 2.2). The extended language adds processor subsets and replication of an array dimension across a processor dimension; skewed distributions need it (Secs. 2.2, 2.5). No overlap areas are described.

## Computation mapping
No work-assignment rule is defined in the basic language; on clauses are said to exist in the full language (Sec. 2.5). Examples use DO loops; in Gaussian elimination the J loop "can be executed in parallel" and a temporary was expanded into an array so each processor holds a local copy for its columns (Sec. 3.1).

## Communication generation
The compiler classifies references as local or non-local, inserts message passing for the latter, and optimizes by combining statements and sending data early (Sec. 1). In ADI, redistributing V is a transpose in which every processor exchanges with every other; assigning V to U induces similar traffic (Sec. 3.2). References through NBR cannot be resolved statically, so run-time techniques from Kali and PARTI are needed (Sec. 3.3).

## Compiler / runtime split
Processor counts bind at load time (Sec. 2.1). `DISTRIBUTE` is executable, so expressions such as `CYCLIC(M)` are evaluated at run time (Sec. 2.2). Copy-in/copy-out is used when the compiler cannot validate reference transmission (Sec. 2.3). `DCASE` specializes code per distribution (Sec. 2.4). The compilation model is deferred (Sec. 1).

## Evaluation
None. Illustrations: Gaussian elimination, N = 4000, cyclic columns motivated by cited performance studies (Sec. 3.1); a 100 x 100 ADI step (Sec. 3.2); a 1000-node mesh with at most 12 neighbours (Sec. 3.3).

## Principal limitation
Stated: only the basic feature set is described and skewed distributions lie outside it (Sec. 2.5); redistribution at subroutine entry may be required (Sec. 2.3); indirect accesses need run-time support (Sec. 3.3). Our observation: no implementation or measurements are reported.

## Relationship to earlier / later work
Sec. 1 names Kali, SUPERB and MIMDizer as predecessors. Sec. 4 states processor arrays originated in BLAZE and that Kali "greatly influenced" Vienna Fortran; it discusses DINO, Fortran D (alignment to decompositions; the authors prefer direct mapping), Griswold's ensembles, SUPERB (static arrays), the Kali compiler (first inspector/executor support for irregular codes), MIMDizer, ASPAR, Pandore, Id Nouveau, Crystal, Quinn & Hatcher, Reeves, the AL compiler, PARTI and Koelbel & Mehrotra; OCCAM, LINDA and STRAND are mentioned as explicitly parallel languages.

## Sources used
| claim | section / page |
|---|---|
| Motivation; predecessors; compiler inserts and optimizes messages | Sec. 1, pp. 1-2 |
| PROCESSORS, ASSERT, RESHAPE | Sec. 2.1, p. 3 |
| DIST intrinsics, alignment, DYNAMIC/RANGE/CONNECT, DISTRIBUTE, INDIRECT | Sec. 2.2, pp. 4-9 |
| Formal parameters; queries and DCASE | Secs. 2.3-2.4, pp. 9-13 |
| Extended language, undefined loops | Sec. 2.5, p. 13 |
| Examples; run-time techniques for indirection | Sec. 3, pp. 14-22 |
| Related work | Sec. 4, pp. 22-24 |

## Open questions for the survey
- Did the two alignment semantics for differing extents survive into HPF-style ALIGN?
- What did the undefined parallel-loop/on-clause constructs look like relative to Kali's doall?
- Which SUPERB mechanisms were reused for the static subset?
