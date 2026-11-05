# Distributed Memory Compiler Methods for Irregular Problems — Data Copy Reuse and Runtime Partitioning

**Catalog id:** `das1991irregular`  
**Citation:** Raja Das, Ravi Ponnusamy, Joel Saltz, Dimitri Mavriplis. "Distributed memory compiler methods for irregular problems — data copy reuse and runtime partitioning." ICASE Report No. 91-73 / NASA Contractor Report 187635, September 1991 (documentation page: to appear in *Languages, Compilers and Runtime Environments for Distributed Memory Machines*, eds. Saltz and Mehrotra, Elsevier). Open copy: NASA NTRS scan of CR-187635 (local file `das1991irregular.pdf`).  
**Paper type:** runtime  
**Access:** open — full text read (ICASE 91-73 / NASA CR-187635 OCR scan; the report number printed matches NASA CR-187635 / ICASE 91-73).  
**Card status:** full-read

## Problem
Sparse and unstructured codes access distributed arrays through indirection, so communication cannot be predicted at compile time (Sec. 2.2). Two gaps remain in runtime compilation: (1) Fortran D requires the programmer to supply an explicit `map` array for an irregular distribution, yet no standard interface exists to the partitioners that produce it (Sec. 2.1, 4.1.1); (2) several loops often access the same off-processor locations, so a per-loop inspector fetches redundant data (Sec. 1, 3.1).

## Input abstraction
Fortran D (Fortran 77 plus `DECOMPOSITION`, `DISTRIBUTE`, `ALIGN`), where `DISTRIBUTE irreg(map)` gives an irregular distribution (Sec. 2.1, Fig. 1). New extensions: `distribute coupling(implicit using <loop>)` and `implicitmap(x,y) <loop>`, which name a loop whose indirection pattern should drive partitioning of the listed, identically distributed arrays (Sec. 4.1.1, Fig. 8). Running example: an edge sweep and a boundary-face sweep over an unstructured mesh accumulating into `y` from `x` (Fig. 2).

## Target
Intel iPSC/860, up to 64 processors (Sec. 5). The report's model is distributed-memory MIMD with significant message startup cost (Sec. 2.2).

## Data decomposition
Irregular, element-to-processor mappings held in a *distributed translation table*: for an N-element array the table has N entries, stored block-wise (N/P per processor), so element m's home is looked up on processor ⌊m/N·P⌋+1; `ifbuild_translation_table` builds it from each processor's list of owned indices (Sec. 2.2, 3.1.2). Runtime partitioning: a compiler-generated *loop RDG* (undirected graph from LHS–RHS index pairs, edge weights counting occurrences, accumulation self-edges ignored, stored in a CSR-like distributed structure) is passed to any `RDG_partitioner` with the right calling sequence, which returns a translation table (Sec. 3.2, 3.3, Fig. 7). Experiments used a parallelised version of Simon's eigenvalue (spectral) partitioner (Sec. 5.2).

## Computation mapping
Data first, then iterations: a *runtime iteration graph* (RIG) lists the array indices each iteration touches; `deref_rig` resolves them to processors via translation tables, producing a RIPA; `iter_partition` assigns each iteration to the processor holding most of its references (Sec. 3.2, 3.3). This is explicitly a departure from strict owner-computes, which is said to be the implicit assumption behind the data partition but not the rule for work (Sec. 3.2).

## Communication generation
Inspector primitives: `flocalize` takes a translation table and a processor's global index list, returns a communication *schedule*, a localised index list, and the count of distinct off-processor references; `fmlocalize` additionally takes pre-existing schedules and returns both a full schedule and an *incremental schedule* covering only references not already fetched, plus a `buffer_mapping` (Sec. 3.1.2). Duplicates are removed by hashing the earlier schedules' references, then the new loop's (Fig. 6). Off-processor copies live in a buffer appended after the owned elements, `x(n_on_proc+1...)`, so executor loops are textually identical to the sequential ones (Sec. 3.1.1, Fig. 3, Fig. 5). Executor primitives: `dfmgather` (gather with an array of schedules), `dfscatter_add` (accumulate from contiguous buffer), `dfscatter_addnc` (non-contiguous buffer via `buffer_mapping`) (Sec. 3.1.1, 3.1.3). Schedules are not bound to a particular array and can be shared by conforming arrays with the same subscript function (Sec. 4.1.3).

## Compiler / runtime split
Runtime: PARTI primitives (translation tables, localize/mlocalize, gather/scatter/accumulate, `eliminate_dup_edges`, `edges_to_RDG`, `deref_rig`, `iter_partition`). Compiler: locates the loop named in `implicit using`, verifies by data-flow (or interprocedural) analysis that subscript-determining variables are not killed before the loop, emits loops L' (RDG generation) and L'' (RIG generation), and hoists inspectors out of loops whose indexing is loop-invariant (Sec. 4.1.2, 4.1.3). Incremental schedules need whole-program analysis — the report proposes "reuse edges" in a program dependence graph and slicing, in joint work with Rice (Sec. 4.1.3). The report states most of this compiler is unimplemented; the experiments embedded the primitives by hand (Sec. 4.1.3, 6).

## Evaluation
3-D unstructured Euler solver (Mavriplis), meshes 3.6K–210K vertices (1.2M edges), iPSC/860. Non-incremental vs incremental schedules: 26K mesh on 16 processors, communication/iteration 2.0 s → 1.1 s; 210K mesh on 64 processors, 3.7 s → 2.3 s, time/iteration 8.4 s → 7.1 s, 118.6 → 144.3 Mflops (Tables 1–2, Sec. 5.1). Parallel code on one node is within 2% of sequential; preprocessing < 3% of parallel execution time over ≥100 iterations (Sec. 5.1). Mapper coupler: RDG generation 0.20–1.50 s and iteration partitioning 0.34–3.30 s, versus 11.5–673 s for the spectral partitioner (Table 3, Sec. 5.2).

## Principal limitation
Stated: indexing patterns must be loop-invariant; incremental scheduling needs invalidation and schedule-ordering information that requires whole-program analysis not yet built; the compiler transformations are largely unimplemented (Sec. 4.1.3). The partitioner itself dominates cost (Sec. 5.2). Our observation: single-node performance is only ~4 Mflops, which the authors attribute to irregular access on the i860 (Sec. 5.1).

## Relationship to earlier / later work
States it builds on earlier PARTI primitives [6], hashed-cache data migration [22] and the ARF/runtime compilation work [45], [38] (= saltz1991multiprocessor), [39] (= saltz1990runtime) (Sec. 1, 2.2, 3). Identifies Kali as the first compiler with inspector/executor preprocessing and ARF as the first supporting irregularly distributed arrays; Fortran D, Kali and PARTI are the three compiler projects using runtime compilation (Sec. 6). Partitioner-coupling idea credited to Fox and to [32]; DIME, Baden's environment and DecTool are related environments (Sec. 1, 6). Work is being integrated into the Rice Fortran D compiler (Sec. 4.1.3, 6).

## Sources used
| claim | section / page |
|---|---|
| Fortran D irregular distribution syntax | Sec. 2.1, Fig. 1, p. 2–4 |
| translation table layout and lookup | Sec. 2.2, p. 5 |
| schedules: gather/scatter/accumulate | Sec. 2.2, p. 4–5 |
| executor with buffer after owned data; dfmgather/dfscatter_add(nc) | Sec. 3.1.1, 3.1.3, Fig. 3, p. 7–8, 14 |
| flocalize/fmlocalize arguments and incremental schedule | Sec. 3.1.2, Figs. 4–6, p. 8–13 |
| loop RDG, RIG, RIPA, iteration partition rule | Sec. 3.2, p. 15–17 |
| mapper-coupler primitives | Sec. 3.3, Fig. 7, p. 17–18 |
| implicitmap extension and compiler analysis | Sec. 4.1.1–4.1.2, Fig. 8, p. 19–21 |
| hoisting, schedule reuse, reuse edges, mostly unimplemented | Sec. 4.1.3, p. 22–24 |
| Euler timings, 2% single-node loss, <3% preprocessing | Sec. 5.1, Tables 1–2, p. 24–26 |
| mapper coupler timings | Sec. 5.2, Table 3, p. 26–27 |
| Kali first, ARF first, three projects | Sec. 6, p. 28 |

## Open questions for the survey
- Did the planned slicing-based automation of incremental schedules ship in Fortran D or later CHAOS work?
- How does the "iteration goes to the processor with most references" rule compare in load balance to owner-computes on these meshes?
- Is the hashed-cache approach of saltz1991multiprocessor fully superseded by the appended-buffer layout here?
