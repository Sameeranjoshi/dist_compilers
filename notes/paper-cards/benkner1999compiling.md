# Compiling High Performance Fortran for distributed-memory architectures  
**Catalog id:** `benkner1999compiling`  
**Citation:** Benkner, S., Zima, H. "Compiling High Performance Fortran for distributed-memory architectures." Parallel Computing 25 (1999) 1785-1825. No DOI printed; record used: PDF first page, PII S0167-8191(99)00074-5.  
**Paper type:** compiler-technique  
**Access:** PDF supplied by the repository owner. Full text read. The text layer is complete for all 41 pages, including the references. Some figures are not recoverable as text, and some symbols are garbled.  
**Card status:** full-read

## Problem
The paper surveys how HPF programs are translated into explicitly parallel SPMD message-passing Fortran, and asks how the generated code can approach hand-written message-passing performance (Secs. 1, 4). It covers distribution and alignment processing, the basic scheme and optimization for regular computations, and transformation and runtime support for independent loops with irregular accesses (Abstract; Sec. 1).

## Input abstraction
HPF 2.0 is built on Fortran 95, with a base language and approved extensions (Sec. 3). The base language offers BLOCK, CYCLIC and BLOCK-CYCLIC distributions, alignment, INDEPENDENT with REDUCTION, FORALL and extrinsic procedures. The extensions add GEN_BLOCK, INDIRECT mapping arrays, RANGE, SHADOW, dynamic REALIGN and REDISTRIBUTE, ON and TASK_REGION (Sec. 3). HPF has no explicit communication statements (Sec. 3).

## Target
The target is a distributed-memory multiprocessor under the SPMD model, with the abstract processor count fixed at load time (Sec. 4.1). The VFC system generates MPI-based code (Sec. 2).

## Data decomposition
A distribution is either one-level, which is replication-free, or two-level, through alignment, which can replicate elements (Sec. 4.2). Local index sets have closed forms for the basic distributions (Sec. 5.2.2, Fig. 2). Non-unit-stride alignment onto a block-cyclic target yields irregular local sections that need table-driven index translation. The authors conclude that removing such mappings from the language would allow more efficient implementation without losing needed functionality (Secs. 5.2.2-5.2.3).

## Computation mapping
Work follows owner-computes: the work set of an array section is its local index set intersected with the left-hand side (Secs. 5.1, 5.5.1). Scalar assignments are masked by ownership (Sec. 5.4.1). Independent loops use an ON HOME clause, or a chosen array term, to assign iterations to processors (Sec. 6.3).

## Communication generation
For regular assignments, gather and scatter schedules are built from regular-section intersections. Execution sends first, computes local work, receives, and then computes the non-local part, so communication overlaps computation (Secs. 4.4, 5.5.1). Irregular loops use inspector/executor: the inspector builds schedules and buffer addresses, and the executor gathers, computes and scatters (Secs. 6.4-6.5). Messages between a processor pair are combined (Sec. 6.4.1).

## Compiler / runtime split
Statically distributed arrays have their layout evaluated once, at the start of the executable section that declares them. Dynamically distributed or allocated arrays evaluate layout descriptors at run time (Secs. 5.2, 5.2.1, 5.3). Reaching distribution analysis reduces the cases handled at run time (Sec. 5.2). Irregular loops are handled at run time, and the VFCS used CHAOS routines to automate partitioning of irregular data (Secs. 6, 7.1).

## Evaluation
The paper reports no new experiments. It relies on worked examples and on the statement that regular dense codes reach performance comparable to hand-written message passing (Sec. 7). Section 7.2 cites an evaluation that finds commercial compilers comparable on regular single-grid codes but weaker on more complex ones (Sec. 7.2).

## Principal limitation
Stated: HPF directives are complex, commercial compilers implement different subsets, irregular codes need low-level features such as HPF_LOCAL, and the data-parallel model is too limited for task-parallel work (Secs. 7.1-7.3). Our observation: the conclusions about the state of compilers rest on cited sources and the authors' judgment rather than on data in this paper.

## Relationship to earlier / later work
The history names SUPERB as the first system to translate Fortran into explicit message passing for several machines, Kali as the first MIMD language with HPF-like directives, and Vienna Fortran as the first complete specification of mapping constructs (Sec. 2). It also lists Fortran D, CM-Fortran, Pandore, Crystal, Id Nouveau, ASPAR and MIMDizer among contributing projects (Sec. 2). Ponnusamy et al.'s time stamping and Give-N-Take are discussed for schedule reuse (Sec. 6.6.1). Later proposals include HPF+ with its REUSE clause (Sec. 6.6.2) and OpenMP (Sec. 7.3).

## Sources used
| claim | section / page |
|---|---|
| HPF history and earlier systems | Sec. 2 |
| HPF 2.0 base language and approved extensions | Sec. 3 |
| Model: global name space, SPMD, abstract processors | Sec. 4.1 |
| One- and two-level mappings; replication | Sec. 4.2 |
| Work sets, schedules, communication sets | Secs. 4.3-4.4 |
| Compilation phases; layout descriptors; array declarations | Secs. 5.1-5.3, Example 5.1 |
| Local index sets; block-cyclic alignment | Secs. 5.2.2-5.2.3, Figs. 2-3 |
| Scalar, array and forall statements | Secs. 5.4-5.5.2 |
| Procedure calls and extrinsic procedures | Secs. 5.6-5.7 |
| Inspector/executor and schedule reuse | Secs. 6.1-6.6 |
| Commercial compilers, task parallelism, outlook | Secs. 7.1-7.3 |

## Open questions for the survey
- If block-cyclic alignment with non-unit strides were removed from the language, which published HPF codes would need rewriting?
- Which schedule-reuse mechanism (compiler analysis, time stamps or explicit REUSE) gives the largest saving on realistic irregular codes?
- Which measured comparison would support the claim that regular codes reach hand-written performance, as the survey needs it?
