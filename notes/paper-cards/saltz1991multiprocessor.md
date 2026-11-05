# Multiprocessors and Runtime Compilation

**Catalog id:** `saltz1991multiprocessor`  
**Citation:** Joel Saltz, Harry Berryman, Janet Wu. "Multiprocessors and runtime compilation." Concurrency: Practice and Experience 3(6):573–592, 1991. DOI 10.1002/cpe.4330030607. Report version: ICASE Report 90-59 / NASA CR-182100, September 1990 (documentation page: "Submitted to Concurrency, Practice and Experience"). Open copy: NASA NTRS scan of CR-182100 (local file `saltz1990multiprocessor.pdf`).  
**Paper type:** compiler-technique  
**Access:** open — full text read (ICASE 90-59 / NASA CR-182100 OCR scan; the journal article is the catalog's primary record and was not read. Table 1's block-MVM rows are partly illegible in the scan).  
**Card status:** full-read

## Problem
Many programs' computational patterns are fixed only once key data structures are initialised (non-uniform meshes, sparse factorisation without pivoting, sparse iterative solvers), so compile-time partitioning and communication scheduling is impossible (Sec. 1.1). The report names the needed execution-time preprocessing "runtime compilation": it decides not *what* is computed but how work is scheduled, data mapped and data movement scheduled on a multiprocessor (Sec. 1.1), and argues it can be amortised like classic algorithmic preprocessing (indices, threaded trees, symbolic factorisation) (Sec. 2).

## Input abstraction
Sequential loops with indirect references whose inter-iteration dependences do not depend on values computed inside the loop (Sec. 3, Fig. 1). For distributed memory, a Fortran subset "ARF" (ARguably Fortran) with declarations of distributed arrays, e.g. `distributed irregular using map real y(4)`, and `doall` loops (Sec. 4.2, Fig. 7). The SIMD section takes lists of destination addresses as input to a communications compiler (Sec. 5).

## Target
Three machines: Encore Multimax/320 (shared memory, 18 processors) for runtime parallelisation (Sec. 3); Intel iPSC/860, 32–64 (up to 128 available) nodes for distributed-memory inspectors/executors (Sec. 4.2); an 8192-processor CM-2 for compiled communication (Sec. 5).

## Data decomposition
Distributed arrays are either partitioned uniformly (equal contiguous blocks) or irregularly, where an integer `map` array, typically produced by a partitioner, gives the owning processor of each element (Sec. 4.2). Irregular mappings are described by a *distributed translation table* defined by the partitioning algorithm (Sec. 4.1, Fig. 6). ARF distributes only the last declared dimension, though the primitives support more (Sec. 4.2). Meshes in the experiments were partitioned by recursive orthogonal dissection (Sec. 4.2).

## Computation mapping
Shared memory: the inspector topologically sorts iterations into wavefronts (`wf`, `schedule`, `count`) and the executor runs a parallel do per wavefront with two copies of the written array (Sec. 3, Figs. 2–3); a cheaper "preprocessed doacross" uses a shared `ready` array and busy-waiting (Sec. 3). Distributed memory: the distribution of parallel-loop indices to processors determines where computation happens; the report assumes iterations have already been partitioned, and ARF has no syntax yet to say where work is done — partitioners decide, with the interface not automated (Sec. 4.1, 4.2).

## Communication generation
Distributed-memory inspector (Fig. 4, Fig. 6): each processor preprocesses its own iterations, records off-processor fetches and stores in a *hashed cache* so each remote element is moved once, consults the distributed translation table for irregular mappings, generates its fetch list, learns from other processors what it must send, and stores the resulting send/receive pairs. Executor (Fig. 5): before the loop, remote data is read, exchanged and written into the hashed cache; computation reads and writes off-processor elements through the cache; afterwards, stored values are sent back to their homes. PARTI primitives also do off-processor accumulation (Sec. 4.2). On the CM-2, Dahl's communications compiler decomposes an irregular pattern into scheduled hypercube transfers, invoked as a preprocessor plus a data-delivery routine (Sec. 5).

## Compiler / runtime split
A prototype shared-memory compiler emits inspector/executor pairs for runtime parallelisation (Sec. 3, citing [29]). For distributed memory, the ARF model compiler recognises a Fortran subset and generates inspector and executor loops with embedded PARTI primitives (translation-table setup/lookup, hashed-cache maintenance, irregular gather/scatter/accumulate) (Sec. 4.2). Partitioning remains outside the compiler. Future work: scheduling communication to reduce contention, and generating standardised dependency-pattern records for partitioners (Sec. 4.3).

## Evaluation
Multimax/320: lower-triangular solve from an incompletely factored Boeing–Harwell matrix, 241 ms on one processor; on 16, inspector 100 ms, executor 23 ms; preprocessed doacross 45 ms (Sec. 3). iPSC/860: block sparse MVM and a Roe-flux kernel ("fluxroe") on 21,672- and 37,741-element unstructured meshes; inspector time 3–5× one iteration's compute time, mostly translation-table work (e.g. 122 ms total, 111 ms table-related, MVM on 64 processors); amortised efficiency on 64 processors 0.48–0.59 vs single-sweep 0.10–0.17; fluxroe on the 37,741 mesh: 393/249/191/203 ms inspector and 534/269/156/69 ms compute on 8/16/32/64 processors (Table 1, Sec. 4.2). CM-2, 64×128 synthetic mesh with random rewiring probability q: relative to NEWS (0.80 ms), general router / compiled get / compiled gather were 15.4×/9.2×/1.1× slower at q = 0 and 22.6×/4.4×/2.7× at q = 0.5; schedule construction took 1–18 s (Sec. 5, Fig. 8).

## Principal limitation
Stated: transformations apply only to loops whose dependences do not depend on values computed inside the loop; hybrid inspector/executors for fully dynamic algorithms are left open (Sec. 3). Inspector cost (dominated by translation tables) is several iterations' worth and must be amortised (Sec. 4.2); the CM-2 communications compiler's simulated-annealing cost is "extremely high" (Sec. 5). Our observation: parallel code also runs its computation less efficiently than sequential code because of hashed-cache accesses and extra indirection (Sec. 4.2).

## Relationship to earlier / later work
States that distributed-memory runtime compilation was proposed in the Crystal runtime system [25], expanded in the PARTI principles paper [20] and the JPDC loop-scheduling paper [26] (= saltz1990runtime), and developed independently in Kali [17]; DIME [34] embodies similar principles; Callahan & Kennedy, Rogers & Pingali and DINO proposed runtime resolution without these optimisations (Sec. 4.2). Shared-memory runtime parallelisation builds on [28], [29], [27] and Cytron's doacross [9] (Sec. 3). Dahl's CM-2 communications compiler [10] is the SIMD counterpart (Sec. 5).

## Sources used
| claim | section / page |
|---|---|
| definition of runtime compilation | Sec. 1.1, p. 1 |
| inspector/executor naming, restriction to loop-invariant dependences | Sec. 3, p. 3–4 |
| wavefront inspector/executor, doacross timings | Sec. 3, Figs. 2–3, p. 4–6 |
| hashed cache, DM inspector and executor steps | Sec. 4.1, Figs. 4–6, p. 6–9 |
| distributed translation table | Sec. 4.1, p. 8–9 |
| ARF declarations, PARTI primitives, last-dimension restriction | Sec. 4.2, p. 10–11 |
| iPSC/860 results, 3–5× inspector ratio, efficiencies | Sec. 4.2, Table 1, p. 11–12 |
| CM-2 communications compiler benchmarks | Sec. 5, Fig. 8, p. 14–17 |
| related systems (Crystal, PARTI, Kali, DIME) | Sec. 4.2, p. 9–10 |

## Open questions for the survey
- The hashed cache versus a dedicated buffer region: when did PARTI drop the cache for the "ghost tail" layout seen in das1991irregular?
- How did later work cut translation-table cost, which dominates inspector time here?
- Was the proposed contention-aware message scheduling for MIMD machines ever implemented?
