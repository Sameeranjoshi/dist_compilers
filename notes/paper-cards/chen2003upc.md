# A Performance Analysis of the Berkeley UPC Compiler
**Catalog id:** `chen2003upc`
**Citation:** Wei-Yu Chen, Dan Bonachea, Jason Duell, Parry Husbands, Costin Iancu, Katherine Yelick. "A Performance Analysis of the Berkeley UPC Compiler." Proceedings of ICS'03, San Francisco, 2003, pp. 63-73. Record used: venue, year and page numbers as printed on the supplied PDF; no DOI is printed.
**Paper type:** full-system
**Access:** PDF supplied by the repository owner. Full text read. The text layer is present and the body text is complete; the figure text is partly garbled (Figs. 5, 8, 15-18 in particular), so figure-based statements rely on the running text.
**Card status:** full-read

## Problem
The authors describe the Berkeley UPC compiler, a portable open-source compiler for UPC, and ask whether it can match commercial UPC compilers while remaining easy to port (Sec. 1). The costs they target are pointer arithmetic on shared data, many small remote accesses, and per-iteration affinity tests (Sec. 1, 3.1, 4).

## Input abstraction
UPC is an SPMD extension of C with a global address space, shared arrays with a declared block size, three pointer kinds, and the upc_forall construct (Sec. 2). The compiler emits ANSI C with calls to a runtime library (Sec. 2.1, Fig. 4). The evaluation uses UPC versions of NAS kernels and synthetic programs (Sec. 3.2, Table 1).

## Target
Experiments run on the PSC Lemieux system, with HP AlphaServer ES45 nodes on a Quadrics interconnect and one thread per node (Sec. 3).

## Data decomposition
A shared array is distributed block by block, round robin over threads, using the block size in its declaration. Block size one gives a cyclic layout and block size zero an indefinite layout on one thread (Sec. 2). A pointer to shared carries address, thread and phase fields (Sec. 2, Fig. 3). The authors' "phaseless" pointers for cyclic and indefinite layouts and a packed 8-byte format reduce the cost of this representation (Sec. 3.1, 5).

## Computation mapping
Iterations are assigned by the programmer's upc_forall affinity expression: an integer is compared with the thread id modulo THREADS, and a shared address with the thread's affinity (Sec. 2). Table 2 gives 6 cycles per iteration for a plain C for loop and 17 with an integer affinity test (Sec. 5).

## Communication generation
Programs use explicit bulk transfers (upc_memget, upc_memput) in IS, NPBCG and MG, and fine-grained shared reads and writes in CG and the synthetic kernels, which the translator maps to GASNet operations (Sec. 3.2, Table 1). The evaluated translator does no UPC-specific communication optimization (Sec. 4). Hand-applied transformations give upper bounds: pipelining gains about 5% on scale (Fig. 15), software pipelining 15 to 20% at high remote fractions (Fig. 16), and combining two reads cuts gups time by about 50% (Fig. 17).

## Compiler / runtime split
The native C compiler does most of the code generation, and the runtime handles thread start-up, shared allocation and communication (Sec. 2.1). The authors locate their main optimizations in the pointer representation and in local shared access (Sec. 3.1, 5.2.4). They say the compiler does no language-specific optimization yet (Sec. 4).

## Evaluation
The packed pointer format beats HP UPC on pointer arithmetic (Fig. 5). Local shared accesses cost about two cycles more than private ones, and remote accesses about two orders of magnitude more (Sec. 5, Figs. 6-7). On applications the compilers are close on EP and small IS runs, and Berkeley is faster on CG, where HP's software caching narrows the gap (Sec. 5.2). HP scales poorly on IS beyond 16 threads and again on MG, where Berkeley is near linear; the authors suspect an HP performance bug (Sec. 5.1, 5.2.2, Figs. 11, 14).

## Principal limitation
The authors state that the reported results "represent an upper bound" on running time and that the compiler does not yet perform UPC-specific optimization (Sec. 4). They also say upc_all_alloc cost grows linearly with thread count (Sec. 5).
our observation: every comparison is against one commercial compiler on one cluster with one thread per node, so the portability claim is not tested on a second platform.

## Relationship to earlier / later work
- The HP UPC compiler is the only commercial comparison, and El-Ghazawi and Cantonnet (2002) is the motivating study (Sec. 1, 3).
- Communication runs on GASNet (Bonachea 2002) (Sec. 2.1).
- Prior analyses are cited for placement and consistency: Krishnamurthy and Yelick (1996), Chakrabarti et al. (1996), Lee and Padua (2001), Zhu and Hendren (1999) (Sec. 4.1); local-pointer inference by Liblit and Aiken (2000) (Sec. 4.4); prefetching from Luk and Mowry (1996) (Sec. 4.2).
- Titanium and Co-Array Fortran are named as related global address space languages; the paper cites the latter as Numwich and Reid (1998) (Sec. 1, references).

## Sources used
| claim | section / page |
|---|---|
| Portable compiler, goals vs. commercial compilers | Sec. 1; p. 63 |
| UPC model, block layout, affinity | Sec. 2; pp. 64-65 |
| Pointer fields, Fig. 3 | Sec. 2; p. 65 |
| Translator and runtime structure | Sec. 2.1, Fig. 4; p. 65 |
| Platform, one thread per node, HP UPC 2.1-003 | Sec. 3; p. 65 |
| Micro-benchmarks and synthetic kernels | Sec. 3.1-3.2, Table 1; pp. 65-67 |
| Communication and computation overlap | Sec. 4.1; p. 67 |
| Prefetching | Sec. 4.2; p. 67 |
| Message aggregation | Sec. 4.3; p. 67 |
| Local shared access | Sec. 4.4; p. 67 |
| Pointer arithmetic, Fig. 5 | Sec. 5; pp. 68-69 |
| Local and remote access costs, Table 2 | Sec. 5, Figs. 6-7, Table 2; pp. 68-69 |
| Application results | Sec. 5.1, Figs. 9-14; pp. 68-70 |
| Pipelining, aggregation, optimization results | Sec. 5.2.1-5.2.4, Figs. 15-18; pp. 69-71 |
| Upper bound and limits | Sec. 4, 5; pp. 66, 68 |

## Open questions for the survey
- Do the measured gains from pipelining (about 5%) and aggregation (about 50%) survive automatic application, and on networks other than the Quadrics system used here?
- Did the phaseless and packed pointer representations persist in later UPC implementations, and how did the reported HP scaling issues resolve?
- Where does a runtime-library, C-emitting design such as this one sit against the survey's source-to-source and communication-generation categories?
