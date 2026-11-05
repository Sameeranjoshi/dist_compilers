# Runtime Support and Compilation Methods for User-Specified Irregular Data Distributions
**Catalog id:** `ponnusamy1995runtime`
**Citation:** Ravi Ponnusamy, Joel Saltz, Alok Choudhary, Yuan-Shin Hwang, and Geoffrey Fox. "Runtime Support and Compilation Methods for User-Specified Irregular Data Distributions." IEEE Transactions on Parallel and Distributed Systems, vol. 6, no. 8, pp. 815-831, 1995. DOI or record used: no DOI printed in the PDF; PDF text used.
**Paper type:** runtime
**Access:** PDF supplied by the repository owner. Full text read (text layer complete; some table columns are garbled in the extracted text, so table values are cited only where the column order is unambiguous).
**Card status:** full-read

## Problem
Irregular concurrent problems (unstructured Euler solvers, molecular dynamics, flame codes) index data through arrays known only at run time, so data distribution and work partitioning must be decided at run time (Sec. I-A and II-A, pp. 815-818). The paper asks how a compiler can let users choose a partitioner and avoid repeated preprocessing when access patterns are unchanged (Sec. I-B and I-C, pp. 816-817).

## Input abstraction
Loops in which each array is reached through one level of indirection by a distributed array indexed by the loop variable, with inter-iteration dependences only from reductions (Sec. I-B, p. 816). The user adds CONSTRUCT directives that build a GeoCoL graph from coordinates (GEOMETRY), connectivity (LINK) and vertex weights (LOAD), and names the partitioner (Sec. IV-A, pp. 823-825, Figs. 11-12).

## Target
Distributed-memory machines; measurements use an Intel iPSC/860 (Sec. VI, p. 827). The runtime is described as a portable, compiler-independent library (Sec. VIII, p. 829).

## Data decomposition
Each distributed array has a translation table giving the home processor and local offset of every global index; the table is itself blocked across processors (Sec. II-B, pp. 818-819). Irregular layouts come either from a map array (Fortran D, Fig. 9, p. 821) or from a partitioner applied to a GeoCoL graph, followed by a remap (Sec. IV-A, pp. 823-826; Sec. V.A, p. 825). BLOCK is the baseline and is kept during the convection phase of the combustion code (Sec. II-A.2, p. 818).

## Computation mapping
The owner-computes rule is described (Sec. V.C, p. 825), but the implemented default is the "almost owner computes" rule: an iteration runs on the processor owning most of the distributed elements it touches (Sec. V.B, pp. 826-827).

## Communication generation
An inspector translates indirect references and builds a schedule. A hash table removes duplicate off-processor references so each off-processor element is fetched once (software caching), and the schedule fetches blocks of data together (communication vectorization) (Sec. II-B and II-C, pp. 819-820, Figs. 6-7). The executor gathers off-processor values and scatter-adds off-processor updates (Sec. II-C, p. 820, Fig. 6).

## Compiler / runtime split
The compiler inserts CHAOS calls for GeoCoL construction, partitioning, remapping and the inspector/executor pair (Sec. IV-A, pp. 823-826, Fig. 8). Reuse is a run-time decision: a global modification counter and per-descriptor timestamps show whether the inspector may be skipped (Sec. III, pp. 821-823).

## Evaluation
Measured on the iPSC/860 with an unstructured Euler solver, a CHARMM loop and a combustion code (Sec. VI, pp. 827-829). For the 53K mesh with recursive coordinate bisection on 32 processors, total time is 18.5 s hand coded, 19.8 s compiled with schedule reuse and 301 s compiled without it (Table IV, p. 827). The authors report compiler output within 15 percent of hand code (Sec. VI.C, p. 828; Table IX). Recursive spectral bisection gives the lowest executor time but a much higher partitioning cost (Sec. VI.B, p. 828).

## Principal limitation
The authors state that the reuse test is conservative and can carry high runtime overhead in some cases (Sec. III, p. 823), and that the best partitioner depends on run length because spectral partitioning is costly (Sec. VI.B, p. 828).
our observation: the hand-coded baselines use the same CHAOS runtime (Sec. VIII, p. 829), so the 15 percent figure does not compare against any other runtime.

## Relationship to earlier / later work
The paper states that CHAOS is a superset of the PARTI library (Sec. II-D, p. 820). It credits the Kali compiler with the first inspector/executor preprocessing and the ARF compiler with the first irregularly distributed arrays (Sec. VII, p. 829). It relates its GEOMETRY construct to von Hanxleden's value-based decompositions (Sec. IV-A.2, p. 824; Sec. VII, p. 828). It cites its own earlier work: a 1992 runtime mapping scheme, a 1993 conference version, and a related HPF proposal (refs. [34]-[36]; Sec. VII, p. 829).

## Sources used
| claim | section / page |
|---|---|
| Irregular concurrent problems and their access patterns | Sec. I-A, pp. 815-816 |
| One-level indirection and reduction-only dependence assumptions | Sec. I-B, p. 816 |
| Translation table blocked across processors | Sec. II-B, pp. 818-819 |
| Localize with hash table; gather and scatter-add | Sec. II-B and II-C, pp. 819-820, Figs. 6-7 |
| Schedule reuse test (DAD, n-mod, last-mod) | Sec. III, pp. 821-823 |
| GeoCoL construction and partitioner coupling | Sec. IV-A, pp. 823-825, Figs. 11-12 |
| Almost owner computes rule | Sec. V.B-V.C, pp. 825-827 |
| Platform is Intel iPSC/860 | Sec. VI, p. 827 |
| Table IV totals (18.5 s, 19.8 s, 301 s) | Table IV, p. 827 |
| Within 15 percent of hand code | Sec. VI.C, p. 828; Table IX; Sec. VIII, p. 829 |
| Spectral partitioning cost and run-length dependence | Sec. VI.B, p. 828 |
| CHAOS is a superset of PARTI | Sec. II-D, p. 820 |
| Kali and ARF first-to claims | Sec. VII, p. 829 |

## Open questions for the survey
- The 15 percent result compares against hand code on the same runtime. What does a comparison against a different irregular runtime show?
- The reuse test is kept per loop and array. How does it behave when an indirection array changes at every step?
- Iteration placement uses the almost-owner rule, and workload partitioners were left for future work (p. 827). How do later systems choose iteration placement when work per iteration varies widely?
