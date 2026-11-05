# Generating Local Addresses and Communication Sets for Data-Parallel Programs
**Catalog id:** `chatterjee1993generating`
**Citation:** Siddhartha Chatterjee, John R. Gilbert, Fred J. E. Long, Robert Schreiber, and Shang-Hua Teng. "Generating Local Addresses and Communication Sets for Data-Parallel Programs." Fourth ACM PPOPP (text layer: "4th ACM PPOPP, 5/93, CA, USA"), 1993, pp. 149-158. Record used: ACM 0-89791-589-5/93/0005/0149.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete for prose and references, while several table cells and figure labels are garbled, so no table cell values are quoted.
**Card status:** full-read

## Problem
For HPF-style arrays under a cyclic(k) distribution, a compiler must generate each processor's local memory addresses for a regular section A(l:h:s) and the messages it sends (Sec. 1). The authors state that the general solution does not appear in the literature or, to their knowledge, in any implementation (Sec. 1).

## Input abstraction
An array A is affinely aligned to a template (cell a*i + b) and distributed cyclic(k) over p processors, with a section stride s > 0 (Sec. 1, Table 1). Two-level and multidimensional cases reduce to one-level problems (Sec. 3, Sec. 4). Block and cyclic are the special cases cyclic(ceil(n/p)) and cyclic(1) (Sec. 1).

## Target
Distributed memory is the design target (Sec. 1). The reported measurements are sequential, on a Sparcstation 2, with a repeat on one iPSC/860 processor (Sec. 6). The text does not say how the 32-processor values in Table 2 and Figure 6 were obtained.

## Data decomposition
Element A(i) lies on processor (i div k) mod p, in course (i div pk) at offset (i mod k) (Eqs. 1-3, Sec. 2). Its local memory location is k times the course plus the offset (Eq. 4). Two-level mappings allocate storage only for occupied template cells (Sec. 3).

## Computation mapping
No separate rule is given. Each processor finds the elements of the section that it holds (Sec. 2.1). Local iterations follow the execution model of Koelbel [7] (Sec. 5).

## Communication generation
Each processor makes one pass over its local data and sends one message per destination of (address, value) pairs; local iterations run from the message buffer (Sec. 5). For shifts, the state machine is augmented with AP and AC columns (Sec. 5.1). Stride changes need a different construction because the destination pattern can have a period longer than k, and the authors use a simpler technique (Sec. 5.2). Termination is detected by counting elements rather than messages (Sec. 5.3).

## Compiler / runtime split
Each processor builds its tables at run time, independently of the others (Sec. 2.1, Sec. 7). The table depends on p, k and s but not on the section bounds or the processor number, so one state machine serves all processors (Sec. 2). If the access sequence is known at compile time, loops can be unrolled, but the benefit is mixed (Sec. 6.1).

## Evaluation
The kernel is DAXPY over regular sections, with throughput plotted against stride for several block sizes (Fig. 5). Unit stride reaches 2.0 Mflops on long vectors (Sec. 6). Table generation time is roughly linear in k (Fig. 6, Sec. 6.1). Table 2 reports FSM generation time and run-time loop cost for shifts and stride changes (Sec. 6.2).

## Principal limitation
The authors state that an O(k) table-construction algorithm remains an open problem, and that a fully parallel algorithm with O(k) parallel time or O(p+k) total work also remains open (Sec. 2.1, Sec. 7).
our observation: The evaluation is one kernel on one workstation, and the message-generation figures are preprocessing and marshalling costs, not end-to-end parallel runs.

## Relationship to earlier / later work
- Koelbel and Mehrotra [8] treat unit-stride sections with block or cyclic mappings, and Koelbel [7] treats non-unit strides (Sec. 1).
- MacDonald et al. [9] (Cray MPP Fortran) restrict block sizes and processor counts to powers of two to avoid address overhead; this paper says its approach avoids that restriction (Sec. 1, Sec. 2).
- The inspector-executor model of Mirchandaney et al. [10] is named as the closest analogy to the communication scheme (Sec. 5).
- No later work is discussed.

## Sources used
| claim | section / page |
|---|---|
| Problem statement; general solution absent from literature | Sec. 1, p. 149 |
| Cyclic(k) layout functions P, C, O and local location M | Sec. 2, Eqs. 1-4, p. 150 |
| Table generation algorithm; O(k) open problem | Sec. 2.1, Algorithm 1, pp. 151-152 |
| Table depends on p, k, s only | Sec. 2, p. 150 |
| Two-level mappings | Sec. 3, p. 152 |
| Per-element pass, one message per destination, (address, value) pairs | Sec. 5, p. 155 |
| Shifts with AP and AC columns | Sec. 5.1, p. 155 |
| Stride changes handled by simpler technique | Sec. 5.2, p. 155 |
| Termination by element count | Sec. 5.3, p. 155 |
| DAXPY results, unit stride 2.0 Mflops, unrolling | Sec. 6, Fig. 5, p. 156; Sec. 6.1, p. 157 |
| Table 2 preprocessing and loop cost; communication not measured | Sec. 6.2, Table 2, p. 157 |
| Fully parallel algorithm remains open | Sec. 7, p. 157 |

## Open questions for the survey
- The O(k) table construction and the fully parallel variant are open. How do their costs compare with the runtime redistribution analysis in other work for the same distributions?
- The reported results are sequential. What do the communication-set costs look like end to end on a real distributed-memory machine?
- The stride-change construction has no stated bound. Does its cost grow with the period of the destination pattern in practice?
