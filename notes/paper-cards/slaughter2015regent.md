# Regent: A High-Productivity Programming Language for HPC with Logical Regions
**Catalog id:** `slaughter2015regent`
**Citation:** Elliott Slaughter, Wonchan Lee, Sean Treichler, Michael Bauer, Alex Aiken. "Regent: A High-Productivity Programming Language for HPC with Logical Regions." SC '15, Austin, Texas, 2015. DOI 10.1145/2807591.2807629.
**Paper type:** language
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete (12 pages, references included).
**Card status:** full-read

## Problem
MPI+X codes make the programmer manage data movement and overlap of communication with computation, and task-based runtimes such as Legion are verbose when embedded in a host language (Sec. 1). Regent offers a language whose programs look sequential, infer dependences, and check region privileges in the type system, and compiles them to Legion (Abstract, Sec. 1).

## Input abstraction
Tasks declare region requirements by field and privilege, including reductions with named operators. Partitions are first-class values, and pointers are typed by the regions they point into (Sec. 2, 3). Examples are PENNANT excerpts (Listings 1-2).

## Target
Legion, run on the Certainty supercomputer: dual-socket Xeon X5650 nodes with 12 cores and QDR InfiniBand (Sec. 6). No accelerator experiments are reported.

## Data decomposition
Regions are partitioned by user colorings into disjoint or aliased subregions (Sec. 2). In PENNANT, zones form a disjoint partition, and points split into private and ghost subregions, refined per submesh so that private data stays free of movement (Sec. 2, Fig. 1).

## Computation mapping
Loops of task launches become index-space launches when the compiler proves the launch non-interfering (Sec. 4.3). A default mapper is provided, and mapping remains under application control (Sec. 3.3). The paper states that Regent binds threads to cores and round-robins them across NUMA domains (Sec. 6.2).

## Communication generation
Regent inserts the synchronization and copy operations that interfering tasks need, so the programmer does not manage data movement (Sec. 3.1). Mapping elision places map and unmap calls at region-use boundaries, which avoids copy-back barriers between consecutive tasks (Sec. 4.1, 6.1). The runtime runs ahead of execution asynchronously (Sec. 3.1).

## Compiler / runtime split
The compiler performs static work: leaf-task inference (Sec. 4.2), index-launch eligibility (Sec. 4.3), future lifting (Sec. 4.4), pointer-check elision (Sec. 4.5), and LLVM vectorization through Terra (Sec. 4.7, 5). Some work stays dynamic: Legion still performs runtime non-interference checks on index launches (Sec. 3.1.3), and dynamic branch elision tests co-location at runtime with a fast path (Sec. 4.6). A failed static proof does not serialize the program (Sec. 4.3).

## Evaluation
Three applications on Certainty. The circuit simulation (up to 8 nodes) matches a manually vectorized C++ Legion code. PENNANT (about 2.6M zones) beats OpenMP by 8% at 10 cores and degrades beyond 12 cores. MiniAero (4M cells, up to 4 nodes) is 2.8x faster than MPI+Kokkos on 8 cores, credited to a hybrid SOA-AOS layout (Sec. 6.1-6.3, Fig. 4). Knockout experiments disable optimizations singly and in pairs (Fig. 5). Lines of code are 825 vs 1701 for circuit, 1789 vs 2416 for PENNANT, and 2836 vs 3993 for MiniAero (Fig. 3).

## Principal limitation
As the paper states it, simultaneous (SPMD-style) region access is not implemented in Regent. The authors advise SPMD structure at the outer level to scale past roughly 10 to 100 nodes (Sec. 6.4).
Our observation: multi-node data stop at 8 nodes (circuit) and 4 nodes (MiniAero), so scaling is not measured at the size the paper's own discussion flags.

## Relationship to earlier / later work
- Targets Legion [9], whose static type system [33] Regent extends (Sec. 3, 7). Legion succeeds Sequoia [22]; leaf tasks are inherited from it (Sec. 3.1.1, 7).
- Regent's compiler plays a different role toward the runtime than the Sequoia compiler [29] (Sec. 7).
- Structure slicing [10] is cited for a layout similar to Regent's (Sec. 6.3). Simultaneous coherence is credited to Legion work at more than 10K nodes [7] (Sec. 6.4).
- DPJ [11, 12], Jade [30], Swift/T [5, 34], several task runtimes, and PGAS models are compared (Sec. 7).
- No later work is discussed.

## Sources used
| claim | section / page |
|---|---|
| Problem and language goals | Abstract, Sec. 1 |
| Tasks, regions, partitions | Sec. 2, 3, Fig. 1 |
| Mapping and default mapper | Sec. 3.3, 6.2 |
| Compiler optimizations | Sec. 4.1-4.7 |
| Runtime dynamic checks | Sec. 3.1.3, 4.6 |
| Evaluation | Sec. 6.1-6.3, Figs. 3-5 |
| Limitations | Sec. 6.4 |
| Related work | Sec. 7 |

## Open questions for the survey
- Does compile-time index-launch analysis generalize beyond simple loops over partitions, and do later compilers keep the static/dynamic split?
- The paper reports results up to 8 nodes; what did later work measure at the scale where SPMD structure becomes necessary?
- Does the language-level hiding of physical instances persist when accelerators with separate memories are added?
