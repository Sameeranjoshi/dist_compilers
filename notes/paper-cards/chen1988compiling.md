# Compiling Parallel Programs by Optimizing Performance
**Catalog id:** `chen1988compiling`
**Citation:** Marina Chen, Young-Il Choo, Jingke Li. "Compiling Parallel Programs by Optimizing Performance." The Journal of Supercomputing 2, 171-207, 1988. Record used: journal name, volume and pages as printed on the supplied PDF; no DOI is printed.
**Paper type:** language
**Access:** PDF supplied by the repository owner. Full text read. The text layer is present and the body text is complete; some figure labels (Figs. 1, 7-9) and table headers (Tables 1-4) are garbled, so values were taken from the running text and legible numbers.
**Card status:** full-read

## Problem
Sec. 1 argues that large machines are hard to use because of coordination overhead, hot spots, load imbalance and communication cost. The authors want programmers to state concurrency and leave the rest to the compiler and run-time system.

## Input abstraction
Crystal is a functional language built on mathematical notation and the lambda calculus (Sec. 1, 3). A program is a set of mutually recursive definitions of data fields over index domains (Sec. 3.1.5). The source contains no locks and no send or receive; those appear only in generated target code (Sec. 1). Matrix multiplication and LU decomposition are written as index-domain definitions (Sec. 5).

## Target
Experiments run on the Intel iPSC/1 (32 nodes) and the NCUBE (128 nodes), both hypercube multiprocessors (Sec. 6.2, Tables 2-4). Sec. 2.4 lists further intended targets, but the reported results cover only the hypercubes. Generated code is per-processor C or Fortran with communication commands (Sec. 2.4).

## Data decomposition
Data fields are functions over index domains that carry communication metrics (Sec. 4.1-4.3). A partition morphism splits a domain into blocks of size b, h_b(i) = (i div b, i mod b) (Sec. 4.5.2, 5.2), which yields a two-dimensional block decomposition for matrix multiplication. Contraction morphisms fold a data field onto a smaller domain in layers (Sec. 4.5.3). Morphisms are chosen by an optimization library or a programmer (Sec. 2.1-2.2).

## Computation mapping
A space-time realization embeds each index domain into a space domain times a time domain (Sec. 4.5.4). Affine morphisms reshape the domain to use fewer processors (Sec. 4.5.1, Fig. 3). Processor assignment is left to the compiler (Sec. 1). Pipelined matrix multiplication arises from a fan-in tree followed by an affine morphism chosen by linear programming (Sec. 5.3).

## Communication generation
A reduction over a data field is rewritten as a fan-in tree (left-associative, balanced or butterfly) to avoid hot spots (Sec. 4.5.5, 5.1). Values needed at many indices are fanned out the same way (Sec. 5.3). The compiler detects the need from a syntactic cue: a bound variable that is absent from an argument list (Sec. 5.3). No general algorithm for deriving message sets from arbitrary programs is given.

## Compiler / runtime split
Transformations are source-to-source, carried out by a metalanguage processor under an optimization library (Sec. 2.1-2.2). Closed-form morphisms serve compile-time optimization and recursive-form morphisms serve run-time optimization (Sec. 1). The run-time environment is described with a data and task distributor, a dynamic allocator, and a garbage collector (Sec. 2.3, Fig. 2). Strategy choices use an analytic performance model (Sec. 6.1, 6.3.4).

## Evaluation
Three programs were compiled to C: block matrix multiplication, pipelined matrix multiplication and pipelined LU decomposition (Sec. 6.3). The block code performs close to hand-written code on the iPSC/1 (Sec. 6.3.1, Fig. 7). Speedups are about 22.6 to 22.7 on 32 iPSC/1 nodes for 100 x 100 inputs (Table 2) and 85.8 to 94.2 on 128 NCUBE nodes (Table 4). In Table 1 (M = 50, p = 4) the model and the measurements are both minimized near k = 17 to 20.

## Principal limitation
The paper has no limitations section. It calls Crystal "an experiment in the design of a language and a metalanguage" (Sec. 1), says the system is "under design and implementation" (Sec. 2), and lists large applications as future work (Sec. 7).
our observation: the evaluation covers three kernels at a few fixed sizes on two hypercubes, and the run-time environment of Sec. 2.3 has no reported measurements.

## Relationship to earlier / later work
- Crystal is introduced in Chen 1986a,b and its metalanguage theory in Choo and Chen 1988 (Sec. 1, 3.2).
- Fortran parallelization techniques (Allen and Kennedy 1985; Cytron 1986; Padua and Wolfe 1986) and strip mining (Loveman 1977) are said to be expressible as morphisms (Sec. 7).

## Sources used
| claim | section / page |
|---|---|
| Functional language, lambda calculus | Sec. 1, 3; pp. 171-172 |
| No locks or send/receive in source | Sec. 1; p. 172 |
| Partition morphism and block result | Sec. 4.5.2, 5.2; pp. 187, 193 |
| Contraction morphism | Sec. 4.5.3; p. 188 |
| Space-time realization | Sec. 4.5.4; p. 189 |
| Affine morphism | Sec. 4.5.1, Fig. 3; p. 187 |
| Fan-in and fan-out trees, butterfly | Sec. 4.5.5, 5.1, 5.3; pp. 190-195 |
| Syntactic cue for fan-out | Sec. 5.3; p. 193 |
| Closed-form versus recursive-form morphisms | Sec. 1; p. 172 |
| Optimization library, metalanguage | Sec. 2.1-2.2; pp. 175-176 |
| Run-time environment | Sec. 2.3, Fig. 2; pp. 176-177 |
| Targets and hypercubes | Sec. 2.4, 6.2; pp. 176, 199 |
| Compiler versus hand-written code | Sec. 6.3.1, Fig. 7; p. 200 |
| Speedups | Tables 2-4; pp. 204-205 |
| Granularity model | Sec. 6.3.4, Table 1; pp. 202-203 |
| "Experiment", "under design", future work | Sec. 1, 2, 7; pp. 172, 175, 206 |
| Related work | Sec. 7; pp. 205-206 |

## Open questions for the survey
- Did later compilers keep the morphism idea, or replace it with polyhedral or dependence-based formulations?
- Which parts of the run-time environment in Sec. 2.3 were implemented, given that the reported results concern compile-time code?
- Do the block-versus-pipelined and tree-versus-butterfly choices depend on the machine constants of Sec. 6?
