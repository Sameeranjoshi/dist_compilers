# Programming Distributed Memory Architectures Using Kali

**Catalog id:** `mehrotra1990kali`  
**Citation:** Mehrotra, P., Van Rosendale, J. "Programming Distributed Memory Architectures Using Kali." NASA CR-187453 / ICASE Report 90-69, October 1990 (also Proc. Workshop on Languages and Compilers for Parallel Computers, MIT/Pitman, 1990). No DOI. Open copy: https://ntrs.nasa.gov/citations/19910002904  
**Paper type:** language  
**Access:** open (NASA NTRS report) — full text read.  
**Card status:** full-read

## Problem
The report states that current environments for nonshared-memory machines make the user encode every detail of data and code placement, yielding complex, inflexible programs (Sec. 1). Kali provides a global name space in which distributed structures are single objects, while annotations keep the user in charge of data distribution and load balancing, which the authors deem performance-critical (Sec. 2). The syntax shown is KF1 (Kali Fortran 1); the primitives were earlier attached to BLAZE (Sec. 1).

## Input abstraction
A KF1 program adds three things to a sequential algorithm (Sec. 3): a `processors` array, whose size may be a tilde-range resolved by the run-time system (Sec. 3.1); a `dist` statement using `block`, `cyclic`, `block_cyclic(b)`, `*` for undistributed dimensions, or user-defined `map` functions from array indices to processor indices (Sec. 3.2); and `doall` loops with an `on` clause naming the executing processor via `owner(A(i))` or a processor-array element (Sec. 3.3). A `distribute` statement redistributes arrays whose `map` depends on variables (Sec. 3.2). `parsub` parallel subroutines take a processor (sub)array as a special parameter (Sec. 3.4). The report says `doall`, not forall, and has no alignment construct.

## Target
No machine is named. Kali assumes an architecture allowing processor arrays of at least two dimensions, so hypercubes and meshes both suffice (Sec. 4). Code runs in SPMD mode (Sec. 2). Physical rather than virtual processor arrays are exposed, in contrast to C* (Sec. 4).

## Data decomposition
Block, cyclic, block-cyclic, user-defined `map` functions (a 2-D cyclic example is shown), undistributed dimensions; distributed dimensions must equal the processor-array rank (Sec. 3.2). Scalars and non-distributed arrays are replicated, one copy per processor (Secs. 3.2, 5). Redistribution moves elements unless the compiler proves every element dead (Sec. 3.2). Load-balanced distribution of irregular grids is out of scope (Sec. 5). No overlap regions are described.

## Computation mapping
The `on` clause assigns iterations; the common form `on owner(A(i))` runs each iteration on the owner of a named element, but any processor expression is legal (Sec. 3.3). The compiler strip-mines each `doall` across processors per the `on` clause (Sec. 5). Sequential code is replicated on all processors rather than run on a "king processor" (Sec. 2). A `parsub` called inside a `doall` on `owner(A(i,*))` gives a second parallelism level (Sec. 3.4).

## Communication generation
Sec. 5 defines per-loop sets in(p,q) (referenced by p, stored on q) and out(p,q). When distributions, `on` clauses and subscripts admit closed forms, the sets are computed symbolically at compile time (details deferred to ref. [9]). Otherwise an inspector, a modified copy of the loop, records nonlocal references at run time; out sets come from routing in(q,p) through a global exchange using Fox's Crystal router; the executor then communicates and computes. Sets are saved and reused across repeated loop executions. Assignment between differently distributed arrays yields an implicit transpose (Sec. 3.5).

## Compiler / runtime split
Compiler: loop partitioning, reference analysis, send/receive insertion, dead-array redistribution optimization (Secs. 2, 3.2, 5). Run time: processor count (Sec. 3.1), redistribution checks and data movement (Sec. 3.2), inspector/executor set construction and caching (Sec. 5). The conclusions state both analyses are relied upon (Sec. 7).

## Evaluation
None quantitative. Examples: ADI (Fig. 1), tree summation (Fig. 2), unstructured-mesh relaxation (Fig. 3); run-time performance is delegated to ref. [10].

## Principal limitation
Stated: only distributed arrays, no lists or common blocks (Secs. 3.2, 3.5); physical processor arrays are "occasionally awkward" (Sec. 4); whether run-time overhead is justified is "not clear a priori" (Sec. 5). Our observation: no measurements or implementation status appear.

## Relationship to earlier / later work
Grown out of BLAZE (Sec. 1). Sec. 6 compares to Quinn & Hatcher and Reeves (SIMD compilation), SPOT, the AL compiler, Linda, Pingali & Rogers' Id Nouveau (run-time resolution without saving sets), Onyx, Griswold's ensembles, Kennedy and coworkers (Callahan & Kennedy; Kennedy & Zima) and SUPERB, DINO, and Saltz/Mirchandaney run-time scheduling. Sec. 4 contrasts C*; Sec. 5 uses Fox's Crystal router.

## Sources used
| claim | section / page |
|---|---|
| Global name space with user-controlled distribution | Sec. 2, pp. 1-2 |
| `processors`, `dist`, `map`, `distribute` | Secs. 3.1-3.2, pp. 3-6 |
| `doall` with `on owner(...)`, `parsub` | Secs. 3.3-3.4, pp. 6-9 |
| Hypercube/mesh assumption; physical vs virtual processors | Sec. 4, pp. 10-14 |
| in/out sets, inspector/executor, Crystal router, set reuse | Sec. 5, pp. 14-16 |
| Related systems | Sec. 6, pp. 16-18 |

## Open questions for the survey
- How often did loops get closed-form communication sets versus the inspector path, and at what cost?
- How did `map` functions evolve into Vienna Fortran's INDIRECT and DFUNCTION?
- Was the "all elements dead" redistribution optimization implemented?
