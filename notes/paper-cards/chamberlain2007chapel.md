# Parallel Programmability and the Chapel Language
**Catalog id:** `chamberlain2007chapel`
**Citation:** B. L. Chamberlain, D. Callahan, H. P. Zima. "Parallel Programmability and the Chapel Language." The International Journal of High Performance Computing Applications 21(3): 291-312, 2007. DOI 10.1177/1094342007078442.
**Paper type:** language
**Access:** PDF supplied by the repository owner. Full text read (pages 291-312); the text layer is complete. Code fragments were read as extracted text.
**Card status:** full-read

## Problem
The paper asks how parallel language design can raise end-user productivity. It sets out a list of desiderata (global view, general parallelism, separation of algorithm and implementation, broad-market features and others) and describes how Chapel addresses them (Sec. 2.2, 4, Table 1).

## Input abstraction
Chapel is a block-imperative, global-view language. Parallelism is expressed with forall loops, cobegin and begin, synchronization variables and on-clauses; domains and arrays separate index sets from storage (Sec. 4.1-4.3). The programmer identifies parallelism and synchronization (Sec. 2.1).

## Target
An idealized machine with a global shared address space, hardware multithreading and a low-latency network. The authors expect software overhead on machines that lack these features (Sec. 4.8). A locale is a node with its local memory, as on a cluster (Sec. 4.1).

## Data decomposition
A domain can be distributed over locales, and adding or changing a distribution does not require changing code that uses the domain (Sec. 4.2.1, 4.3). The planned standard library includes block, cyclic, recursive bisection and graph partitioning (Sec. 4.2.1). Custom distributions are written as five classes, which the authors call one of their most aggressive research areas (Sec. 4.2.1).

## Computation mapping
By default a forall iteration runs on the locale that owns its index. On-clauses override this, and can bind computation to the locale that owns a named variable (Sec. 4.3). Task parallelism comes from cobegin, begin and nested forall (Sec. 4.2.2-4.2.3).

## Communication generation
The paper describes no communication scheme. The distribution classes must provide data-transfer methods that the compiler will target (Sec. 4.2.1).

## Compiler / runtime split
The compiler is to turn global-view code into local allocations, iterations and communication (Sec. 2.2.3). The runtime is to schedule anonymous threads with work sharing and stealing, throttled by laziness (Sec. 4.2.3). The authors say a portable proof-of-concept implementation is still in progress (Sec. 5).

## Evaluation
The paper reports no experiments. It evaluates the design against its ten desiderata in a qualitative table (Sec. 5, Table 1) and says the language will be evaluated later by HPCS agencies and users (Sec. 5).

## Principal limitation
As the paper states it: execution-model transparency is the weakest area, since Chapel favours programmability over performance transparency (Sec. 4.7, 5). Portability to machines without shared memory or multithreading costs performance (Sec. 4.8). Interoperability through domain distributions is still in progress (Sec. 4.9, 5). Our observation: with no performance data reported, the performance claims cannot be checked from this text.

## Relationship to earlier / later work
- Chapel's domains evolve ZPL's regions, generalized to sets, graphs and associative arrays (Sec. 3.5, 4.2.1).
- The authors build on HPF's global-view approach for distributed arrays while adding general parallelism (Sec. 3.4).
- Contrasted with MPI, PVM, SHMEM, ARMCI, GASNet (Sec. 3.1), Co-array Fortran, UPC, Titanium (Sec. 3.2), OpenMP (Sec. 3.3) and Cilk (Sec. 3.6).
- Interoperability is to be provided through Babel (Sec. 4.9). The distribution design is detailed in Diaconescu and Zima (2007) (Sec. 4.2.1).

## Sources used
| claim | section / page |
|---|---|
| Ten desiderata and Table 1 | Sec. 2.2, Sec. 5 |
| Domains, forall, on-clauses | Sec. 4.2.1-4.3 |
| Locales | Sec. 4.1 |
| Planned standard distributions | Sec. 4.2.1 |
| Compiler and runtime roles | Sec. 2.2.3, 4.2.3 |
| No experiments; prototype in progress | Sec. 5 |
| Transparency and portability limits | Sec. 4.7, 4.8 |
| Related languages | Sec. 3.1-3.6 |

## Open questions for the survey
- Did the stricter execution-model mode mentioned in Sec. 4.7 appear, and how does it bear on the 90/10 argument of Sec. 2.2.6?
- How do the user-defined distribution classes of Sec. 4.2.1 perform against measured distributed-memory baselines?
- Which of the ten desiderata have later evaluations confirmed, since this paper offers only a qualitative table?
