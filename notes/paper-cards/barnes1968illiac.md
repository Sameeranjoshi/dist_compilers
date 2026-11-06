# The ILLIAC IV Computer
**Catalog id:** `barnes1968illiac`

**Citation:** G. H. Barnes, R. M. Brown, M. Kato, D. J. Kuck, D. L. Slotnick and R. A. Stokes. "The ILLIAC IV Computer." IEEE Transactions on Computers, vol. C-17, no. 8, pp. 746-757, Aug. 1968. No DOI printed; catalog record used.

**Paper type:** hardware

**Access:** PDF supplied by the repository owner. Full text read (text layer complete on all 12 pages).

**Card status:** full-read

## Problem

The paper describes ILLIAC IV, a parallel-array computer of 256 processing elements, aimed at large matrix work, grid models and signal correlation (Introduction, p. 746). The authors argue that signal propagation limits sequential machines, while explicit parallelism can scale with gate count (p. 746). The paper is a hardware description. It discusses per-element memories and routing, but not message passing or a method for distributing data.

## Input abstraction

Not applicable in this paper as a source abstraction, because no source language or compiler is described. The machine's input is an instruction stream of 32-bit words in two classes: control-unit instructions and processing-element instructions (Section 3.4, p. 749). Appendix I lists the instructions (pp. 754-757).

## Target

The target is the machine itself. Four 64-PE arrays each have a control unit and can be joined into 128- or 256-PE configurations (Sections 2.6, 3.2, pp. 747-748). Each PE has a 2048-word memory with a 240 ns cycle and a 16-bit index register (Sections 2, 3.9, 3.12, pp. 747, 751-752). The host is a Burroughs B6500 (Section 3.14, pp. 752-753).

## Data decomposition

Placement is discussed only at the hardware level. Each PE can address only its own memory, while the control unit can reach all of it (Section 3.5, p. 750). Each PE adds a local index to a control-unit index, which the authors say suits rows and columns of matrices (Sections 2.1, 3.5, pp. 747, 750). No method for choosing or changing a distribution of arrays is described.

## Computation mapping

Not applicable in this paper as a compiler mapping. The execution model is data-parallel: one control unit broadcasts a single instruction stream, and a per-PE mode bit enables or disables execution for each element (Sections 2.2, 3.1, pp. 747-748).

## Communication generation

Not applicable in this paper as compiler-generated communication. The hardware provides nearest-neighbour and distance-8 routing, with at most 7 routing steps in a 64-PE array (Section 2.3, p. 747). The control unit broadcasts common operands (Section 2.4, p. 747), and routing appears as explicit instructions (Appendix I, pp. 754-755). Message passing is not described.

## Compiler / runtime split

Not applicable in this paper, because no compiler is described. The runtime side is the B6500 executive, which supervises program loading, array reconfiguration and I/O (Section 3, p. 748; Section 3.14, p. 752). The paper says the B6500 also compiles ILLIAC IV programs (Section 3.14, p. 753), that programmer or compiler attention to instruction order can speed programs (Section 3.4, p. 749), and that software is covered in a companion paper [5] (Section 2, p. 748).

## Evaluation

No benchmarks are reported. The abstract gives design targets of 4 x 10^6 instructions per second per PE and about 10^9 operations per second overall (p. 746). The 64-bit add is given as 240 ns in Section 2 (p. 747), while the leading column of Table I appears to give 200 ns for it (p. 752), so the card reports both. Reliability is estimated at about 10^5 hours per element and 2 x 10^3 hours per memory unit (Section 4, p. 753).

## Principal limitation

The paper has no limitation section. It notes that several array configurations complicate memory addressing (Sections 3.2, 3.5, pp. 748, 750), and that control-unit overlap prevents an immediate response to an arithmetic fault (Section 3.8, p. 751).

our observation: The performance and reliability figures are design estimates, so delivered performance cannot be read from the paper.

## Relationship to earlier / later work

The paper states that a SOLOMON-type array could reach about 10^9 word operations per second (Section 1, p. 747), and it describes the SOLOMON computer's four principal features (Introduction, pp. 746-747). It cites SOLOMON [1] and other parallel designs [2]-[4] (p. 746). It credits an earlier Westinghouse group with starting the parallel computer effort (Acknowledgment, p. 757). It defers software to [5] (Section 2, p. 748) and says a later paper will give the logical layout and hardware (p. 748). It discusses no later work.

## Sources used

| claim | section / page |
|---|---|
| Design of a 256-PE array; per-PE and aggregate rates; design-target wording | Abstract, p. 746 |
| Application areas; limits of sequential speed; SOLOMON features | Introduction, pp. 746-747 |
| Four 64-PE arrays, control units, multiarray configurations | Sections 2.6, 3.1, 3.2, pp. 747-748 |
| Mode control; enable bits; data-parallel execution | Sections 2.2, 3.1, pp. 747-748 |
| Routing: nearest-neighbour and distance 8; 7 steps for 64 PEs | Sections 2.3, 3.11, pp. 747, 752 |
| Common-operand broadcast | Section 2.4, p. 747 |
| Instruction classes; overlap of CU and PE work; programmer or compiler ordering | Section 3.4, p. 749 |
| PE memory reachable only by its PE; address composition; column layout | Section 3.5, p. 750 |
| Interrupts and arithmetic faults; overlap limits | Sections 3.8, p. 751 |
| PE operation times (Table I); PE memory cycle | Sections 3.9-3.12, pp. 751-752 |
| B6500 executive and compilation role | Sections 3.14, pp. 752-753 |
| Reliability estimates | Section 4, p. 753 |
| Instruction lists | Appendix I, pp. 754-757 |
| SOLOMON, Unger, Holland, Murtha; companion paper [5]; Westinghouse effort | References and Acknowledgment, p. 757 |
| Text of another paper at top of p. 746 (not used as evidence) | p. 746 |

## Open questions for the survey

- The survey's paper types have no machine-only value. Should `hardware` be added to the taxonomy, or should this catalog entry move to full-system as the card does?
- The paper defers software to the companion paper [5] in the same issue (p. 748). Should that paper be obtained before the ILLIAC IV compiler work is compared with this one?
- Section 2 and Table I disagree on the 64-bit add time (240 ns versus 200 ns). Which figure should the survey cite, or should the discrepancy be recorded?
