# Parallel Languages and Compilers: Perspective From the Titanium Experience
**Catalog id:** `yelick2007titanium`
**Citation:** Katherine Yelick, Paul Hilfinger, Susan Graham, Dan Bonachea, Jimmy Su, Amir Kamil, Kaushik Datta, Phillip Colella, Tong Wen. "Parallel Languages and Compilers: Perspective From the Titanium Experience." The International Journal of High Performance Computing Applications 21(3), 266-290, 2007. DOI 10.1177/1094342007078449 (as printed on the supplied PDF). Note: the catalog id carries 1998; see the Notes field of the record.
**Paper type:** experience
**Access:** PDF supplied by the repository owner. Full text read. The text layer is complete for the body and references; the chart data in Figs. 4, 5, 7 and 8 is not legible in the text layer, so statements about those figures rely on captions and the running text.
**Card status:** full-read

## Problem
The authors aim for a language that is portable, balances expressiveness with user-supplied concurrency and locality information, and supports adaptive, irregular and pointer-based applications (Sec. 1). They chose a Java dialect over C++ for its simpler semantics and type safety (Sec. 1).

## Input abstraction
Titanium adds to Java multi-dimensional arrays indexed by points over rectangular domains, with view operators such as shrink, translate and copy (Sec. 2.1-2.2). The foreach loop iterates over a domain and may be reordered (Sec. 2.3). Other additions are immutable value classes, operator overloading, templates, and native calls to C (Sec. 5.1-5.3). Parallelism is SPMD with textually aligned barriers (Sec. 4.1). Pointers are global by default, with a local qualifier (Sec. 4.3).

## Target
Measurements cover six production systems, among them PSC Lemieux (Alpha with Quadrics) and NERSC Jacquard (Opteron with InfiniBand) (Table 1, Sec. 6.4). The compiler emits C, and distributed backends use GASNet (Sec. 7.1, 7.4).

## Data decomposition
Distributed structures are built locally: each process allocates its block, and an exchange operation builds a replicated directory of pointers (Sec. 4.2, Fig. 2). The programmer chooses affinity through allocation (Sec. 4.2). In AMR, grids are assigned to balance load (Sec. 6.1).

## Computation mapping
Work is assigned by the programmer in the SPMD style (Sec. 3.1.3). The compiler does not place work.

## Communication generation
Remote access is fine-grained and implicit through global pointers and arrays (Sec. 4.3). Array copy is blocking by default, with a non-blocking form (copyNB) for overlap, used in the FT transpose (Sec. 4.4). The compiler converts blocking copies to non-blocking ones (Sec. 7.2.4), and applies an inspector/executor to a[b[i]] patterns, choosing pack, bound or bulk transfer with a performance model (Sec. 7.2.5).

## Compiler / runtime split
The compiler is source-to-source to C, with the vendor C compiler and GASNet below it (Sec. 7.1). Static analyses cover barrier alignment, concurrency, alias analysis and local qualification inference (Sec. 4.1.1, 7.2.1-7.2.3). The runtime uses a conservative collector (Sec. 7.3). The authors report that C back-end differences can reach a factor of three (Sec. 7.1).

## Evaluation
On FT, Titanium outperforms Fortran with MPI, and the best Titanium code is 36% faster on 64 Opteron processors (Sec. 6.4, Fig. 5). On MG it is only marginally slower than Fortran (Sec. 6.4). The AMR code matches Chombo on uniprocessors and SMP and scales comparably to 112 processors (Sec. 6.1). Local qualification inference gives total speedups of 239% on CG and 443% on MG (Sec. 7.2.3, Fig. 7). GASNet matches or exceeds MPI on microbenchmarks (Sec. 7.4.2, Fig. 8). Expressiveness is shown by line counts, with the AMR code under one tenth the size of Chombo (Sec. 6.3, 8, Fig. 4).

## Principal limitation
The authors state that distributed garbage collection is "still not entirely solved" and that a production system would need a specialized collector; deleting a region with live objects is an error the implementation may not detect (Sec. 4.5). Dynamic thread creation is an open area (Sec. 5.4).
our observation: the expressiveness claim rests on line counts rather than a controlled study, and the performance comparisons use a small set of Fortran, MPI and Chombo baselines.

## Relationship to earlier / later work
- Built on Split-C, CC++ and AC (Sec. 1), with FIDIL domains (Sec. 2.1); data-parallel and task-parallel models are contrasted (Sec. 3.1).
- Barrier analysis follows Aiken and Gay (1998) (Sec. 4.1); regions follow Gay and Aiken (2001) (Sec. 4.5); local qualification follows Liblit and Aiken (2000) (Sec. 7.2.3); inspector/executor follows Su and Yelick (2005) (Sec. 7.2.5).
- GASNet is shared with UPC and Co-Array Fortran compilers (Sec. 7.4.1); MPI and ARMCI are discussed as targets (Sec. 7.4).

## Sources used
| claim | section / page |
|---|---|
| Design goals and language choice | Sec. 1; pp. 266-267 |
| Arrays, domains, copy, translate | Sec. 2.1-2.2; pp. 267-268 |
| foreach | Sec. 2.3; p. 268 |
| Models of parallelism and PGAS | Sec. 3.1-3.2; pp. 268-270 |
| SPMD, barriers, single qualification | Sec. 4.1; pp. 270-272 |
| Distributed arrays | Sec. 4.2; pp. 272-273 |
| Local and global pointers, LQI | Sec. 4.3, 7.2.3; pp. 273-274, 283 |
| Non-blocking array copy and FT | Sec. 4.4, 6.4; pp. 273, 279-280 |
| Regions and garbage collection | Sec. 4.5, 7.3; pp. 273-274, 284 |
| Immutables, templates, native calls | Sec. 5.1-5.3; pp. 274-276 |
| Restrictions | Sec. 5.4; pp. 276-277 |
| Application experience and line counts | Sec. 6.1-6.3; pp. 277-279 |
| Platforms | Table 1; p. 280 |
| Performance results | Sec. 6.4, Fig. 5; pp. 279-280 |
| Compiler architecture | Sec. 7.1, Fig. 6; pp. 280-281 |
| Analyses | Sec. 7.2.1-7.2.5; pp. 281-284 |
| GASNet and microbenchmarks | Sec. 7.4, Fig. 8; pp. 283-285 |
| Conclusions and AMR size claim | Sec. 8; pp. 285-286 |

## Open questions for the survey
- The paper ties communication to one-sided operations and collects the results on several networks; how do the survey's other one-sided systems handle the same small-message cost?
- Which of the analyses (barrier alignment, concurrency, LQI) were carried into the later Titanium and UPC implementations, and how do they compare with the survey's static compiler categories?
- How does the survey treat the reported C back-end variance (up to a factor of three), which affects how compile-time results should be compared across compilers?
