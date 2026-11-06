# Optimizing Irregular Data Accesses for Cluster and Multicore Architectures
**Catalog id:** `su2010irregular`  
**Citation:** Jimmy Zhigang Su. "Optimizing Irregular Data Accesses for Cluster and Multicore Architectures." PhD dissertation, University of California, Berkeley (Technical Report UCB/EECS-2010-170), 2010. No DOI; record used: the report number and URL on the title page.  
**Paper type:** compiler-technique  
**Access:** Official open copy (UC Berkeley EECS technical report UCB/EECS-2010-170, https://www2.eecs.berkeley.edu/Pubs/TechRpts/2010/EECS-2010-170.html). Full text read (the text layer covers all 111 pages; Tables 4.1, 4.2 and 6.1 are image-only and were read from rendered pages; plotted results are not in the text layer and were not read off the plots).  
**Card status:** full-read

## Problem

Remote irregular accesses are costly, and a naive remote synchronized update needs four round trips (Sec. 1.2, p. 3). The thesis covers inspector-executor reads (Ch. 4), update-by-owner writes (Ch. 5), multicore lock and replication tradeoffs (Ch. 6), and ti-trend-prof, a trace tool for scaling bugs (Ch. 7).

## Input abstraction

Titanium source: an SPMD Java dialect with global pointers, foreach loops, synchronized regions and textually aligned barriers (Sec. 2.1-2.5, pp. 6-12). The pattern is A[B[i]] (Ch. 3, p. 16).

## Target

Cluster code is C over the Titanium runtime and GASNet (Sec. 2.6, p. 13). Machines: Table 4.1 (p. 27), Sec. 5.6 (p. 47) and Table 6.1 (p. 52).

## Data decomposition

The program sets the layout; the text does not describe the compiler changing it. SpMV uses row blocks (Sec. 4.5, p. 30). Histogram samples are split across processors, and heart fiber points are partitioned by a graph partitioner (Sec. 5.6, p. 47). Chapter 6 uses unequal slabs set from sorted particles (Sec. 6.6.2, p. 68).

## Computation mapping

Each processor works on its own rows or particles (Sec. 4.5, p. 30; Sec. 5.2, p. 38). Owners pack or push read data (Sec. 4.2.2, p. 26) and apply writes, which is update by owner (Sec. 5.5, p. 46). Chapter 6 pins threads (Sec. 6.5, p. 58).

## Communication generation

Reads: each remote A[B[i]] becomes an inspector that builds a schedule, a transfer and an executor (Sec. 4.2.1, pp. 24-25). Pack or bounding-box transfers are chosen per processor pair at run time (Sec. 4.4, pp. 27-30). Push sends about half the messages of pull (Sec. 4.2.2, p. 26). Writes: updates are cached per processor, sent as one active message per destination, and applied at the owner (Sec. 5.5, p. 46).

## Compiler / runtime split

Cluster part: yes, it is the compiler part. Legality checks, push placement and update-by-owner analysis run in the Titanium compiler (Sec. 4.2, 5.3). The transfer choice is made at run time from a per-machine model calibrated at install time (Sec. 4.4, p. 29; Sec. 4.8, p. 36). Multicore part: yes, a code-generation and tuning study on C code (Sec. 6.1, p. 51); how the variants were generated is not stated. Chapter 7 is a post-run trace tool, not a compiler pass.

## Evaluation

Reads: SpMV on 22 matrices against Aztec (MPI), 1 to 16 processes: average 1.2x, some runs above 2x (Sec. 4.7, pp. 33-35); "up to 2.25x" in the conclusion (Sec. 4.8, p. 36). Writes: three benchmarks on a Xeon cluster, 2 to 128 cores: 90x, 120x and 70x over sequential at 128 cores; unoptimized code gives 6.74x for spread force and misses sequential speed for the others (Sec. 1.5, p. 5; Sec. 5.6, p. 48). Multicore: thread sweeps on three SMPs; the 4.8x headline lacks a body configuration (Sec. 1.5, p. 5; Sec. 6.6). Debugging: three bugs, two already known (Sec. 7.7, p. 87).

## Principal limitation

No limitations section. Stated limits: a point-to-point cost model that "does not account for network contention" (Sec. 4.4, p. 29); no check for conflicting cross-thread writes to A and B (Sec. 4.2.1, p. 24); an associativity requirement for accumulation (Sec. 5.2, p. 39).

our observation: the evaluations differ in machines, baselines and metrics, so the headline figures are not directly comparable.

## Relationship to earlier / later work

Stated: Walker's precomputed schedules [70], PARTI [12] and CHAOS [59] as source-level primitives, and KALI [43] and ARF [72] as automatic inspector-executor compilers (Sec. 8.1, p. 88). Unlike Benkner's halos [10] and Kelp [7], these transforms are hidden from the programmer (p. 88). Schedule reuse is prior work, but these schedules also record the transfer method (Sec. 4.2.1, p. 25). UPC is only named as another GASNet client (Sec. 2.7, p. 14). Diniz and Rinard's lock elimination [26] is contrasted with update by owner (Sec. 8.2, p. 89). No later work is discussed. inferred: Chapter 4 may continue the earlier Titanium work [62, 63] cited in Sec. 2.1 (p. 6); the text does not say so.

## Sources used

Page numbers are the dissertation's printed numbers (PDF page = printed page + 11 for Chapters 1 to 9).

| claim | section / page |
|---|---|
| Titanium is a Java-based PGAS language, translated to C over GASNet | Sec. 2.1, 2.6, 2.7; pp. 6, 13-14 |
| Textually aligned barriers, checked statically | Sec. 2.3; p. 11 |
| Inspector-executor candidate conditions | Sec. 4.2.1; pp. 24-25 |
| Push variant halves messages; single analysis places calls | Sec. 4.2.2; pp. 26-27 |
| Non-blocking puts overlap communication | Sec. 4.2.3; p. 27 |
| Pack and bounding-box transfers; per-pair runtime choice; whole array as special case | Sec. 4.4; pp. 27-30 |
| Model parameters measured per machine at install time | Sec. 4.4, 4.8; pp. 29, 36 |
| Machines | Sec. 4.3; Table 4.1 p. 27 |
| SpMV versus Aztec: 22 matrices, 1.2x average, some runs above 2x | Sec. 4.7; pp. 33-35; Table 4.2 p. 34 |
| Update by owner: conditions, caching, active messages | Sec. 5.2-5.5; pp. 38-46 |
| Greedy bounding-box split and claimed optimality | Sec. 5.4; pp. 44-46 |
| Speedups 90x, 120x, 70x at 128 processors; 6.74x unoptimized | Sec. 1.5; pp. 4-5; Sec. 5.6; p. 48 |
| Multicore machines and strategies | Sec. 6.1, 6.2, 6.4, 6.6; Table 6.1 p. 52 |
| Bugs found by trend analysis | Sec. 7.6, 7.7; pp. 81-87 |
| Prior work | Sec. 8.1-8.4; pp. 88-92 |

## Open questions for the survey

- Which cluster transforms depend on Titanium-specific rules (textually aligned barriers, single analysis, concurrency analysis), and what would a UPC or Co-Array Fortran compiler need to reproduce them?
- Should the survey record speedups per baseline (MPI library, unoptimized code, sequential) rather than one headline figure?
- How portable are the install-time cost model (Sec. 4.4) and the vendor-latency box model (Sec. 5.4) across machines?
