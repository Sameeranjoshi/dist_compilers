# The Parallel Execution of DO Loops
**Catalog id:** `lamport1974parallel`

**Citation:** Leslie Lamport. "The Parallel Execution of DO Loops." Communications of the ACM, vol. 17, no. 2, pp. 83-93, Feb. 1974. No DOI printed; catalog record used.

**Paper type:** foundational

**Access:** PDF supplied by the repository owner. Full text read (text layer complete on all 11 pages).

**Card status:** full-read

## Problem

The paper asks how the iterations of a DO loop nest can run concurrently on a multiprocessor or an array computer and still give the sequential results (Abstract and Introduction, p. 83). It calls expanding the loop into separate statements at best a formidable task, and impossible when the bounds are unknown at compile time (pp. 83-84). The paper does not discuss distributed memory or message passing. Communication appears only as motivation: independent iterations need much less communication between processors (p. 83).

## Input abstraction

The input is a nest of DO loops whose bounds may be integer expressions in outer indices (p. 85). The paper states that its methods are independent of FORTRAN syntax (p. 83). The loop body may contain no I/O, no transfer out of the loop and no call that modifies data (A1-A3, p. 85). Assigned array variables must have restricted subscript forms (A4-A5, pp. 85, 87). The coordinate method also needs tightly nested loops without conditional branches (A6-A7, p. 90), and assigned scalars must be eliminated first (p. 93).

## Target

Two target classes are named. Asynchronous multiprocessors run the DO CONC form, with one processor per index point and no synchronization assumed (p. 84). Synchronous single-instruction-stream array machines run the DO SIM form, and the paper names ILLIAC IV, CDC STAR-100 and TI ASC (pp. 83, 89, 93). The memory organization of the multiprocessor is not described.

## Data decomposition

Not applicable in this paper as a decomposition method, because no distribution of arrays across processors is defined. The storage remarks concern the target only. On ILLIAC IV the synchronous form needs a peculiar array storage scheme that the authors expect to conflict with the rest of a program. On the STAR-100 the hyperplane method needs dynamic reformatting of arrays (p. 93).

## Computation mapping

This is the core of the paper. The hyperplane method uses a linear map so that all index points on a plane, such as 2I+J+K = constant, can run together (p. 84; Hyperplane Theorem, p. 88). The map is chosen to minimize sequential steps (p. 88). In DO CONC each index point gets a processor, and fewer processors suffice because executions may be asynchronous (p. 84). DO SIM runs each statement across all processors in step (p. 89).

## Communication generation

Not applicable in this paper as generated communication code. Correctness rules constrain the order of references to the same array element (rules C1-C2, pp. 86-87; S1-S3, p. 91). A parallel scalar sum, or a maximum or minimum, is delegated to a special subroutine (p. 93), the only reduction the paper mentions.

## Compiler / runtime split

The rewriting is compile-time work. The chosen mapping is independent of the index set (p. 88), which may not be known at compile time (p. 85). At run time the DO CONC or DO SIM constructs execute, and the paper notes that DO CONC overhead reduces the saving (p. 84). No runtime system is described beyond the reduction subroutine (p. 93).

## Evaluation

There are no measurements. The evidence is analytic. Loop (1) falls from L(M-1)(N-1) sequential iterations to 2L+M+N-5 (p. 84). A variant applied to the outer loops gives M+N-3 (p. 85). For loop (11), the hyperplane method gives M+N-2 steps and the coordinate method gives N (pp. 89-90). The paper says the methods are being implemented in the ILLIAC IV FORTRAN compiler, and it describes preliminary results only qualitatively (pp. 83, 93).

## Principal limitation

As stated, the authors know of no practical method for the general optimal mapping (p. 88). A real compiler must restrict subscript expressions, which the paper does not treat (p. 90). The target's data-access mechanism and loop restrictions also limit the methods (p. 93).

our observation: Speed-up depends on DO CONC overhead and processor count, which the paper leaves unquantified (p. 84).

## Relationship to earlier / later work

The paper states that the approach was inspired by ILLIAC IV, the only type of parallel computation that machine can perform (p. 83). It says the expansion approach would need techniques from [2] (p. 83). It says the plane theorem may be viewed as a generalization of a result in [5] (p. 88), notes a weaker version in [3] (p. 88), uses the method of [4] (p. 88), and uses an algorithm from [6] (p. 91). Details are in the 1971 report [7] (p. 93), and nontightly nested loops are deferred to a future paper [8] (p. 92).

## Sources used

| claim | section / page |
|---|---|
| Aim: run DO-loop iterations concurrently with sequential results; methods for multiprocessors and array computers | Abstract, p. 83 |
| Approach inspired by ILLIAC IV; less communication between processors | Introduction, p. 83 |
| Expansion approach "formidable", impossible if bounds unknown at compile time | Introduction, pp. 83-84 |
| DO CONC with one processor per point; no synchronization assumed | Section I, p. 84 |
| Hyperplane transform; loop (1) reduced to 2L+M+N-5 steps | Section I, p. 84 |
| Outer-loop variant reduced to M+N-3 steps | Section I, p. 85 |
| Assumptions A1-A5; index set may be unknown at compile time | Section I, pp. 85, 87 |
| Rules C1-C2, Table I, Hyperplane Theorem, optimal mapping | Section I, pp. 86-88 |
| Coordinate method, DO SIM, loop (11) with N steps versus M+N-2 | Section II, pp. 89-90 |
| Coordinate rules S1-S3 and steps 1-11 | Section II, pp. 91-92 |
| Restrictions: subscripts, scalars, storage schemes, STAR-100 reformatting, parallel sum | Section III, pp. 92-93 |
| Preliminary ILLIAC IV compiler experience; no timings | Conclusion, p. 93 |
| Cited works [1]-[8] | References, p. 93 |

## Open questions for the survey

- The paper never states the memory model of its multiprocessor. Should the survey record that as open, given that its ordering rules concern shared array elements?
- The paper defers details to the 1971 report [7] and the coordinate-method paper [8]. Should those be added to the corpus before this card is treated as complete?
- How should the survey classify the target-specific restrictions on pp. 92-93 when they constrain a machine rather than the method?
