# The CRAY-1 Computer System
**Catalog id:** `russell1978cray1`
**Citation:** Richard M. Russell. "The CRAY-1 Computer System." Communications of the ACM 21(1), pp. 63-72, January 1978. Record used: supplied PDF (no DOI printed in it).
**Paper type:** hardware
**Access:** PDF supplied by the repository owner. Full text read (text layer complete on all 10 pages; page 1 also carries closing text and references of an unrelated article, which I excluded).
**Card status:** full-read

## Problem
The paper describes the CRAY-1 vector computer, its architecture's evolution and some manufacturing problems (pp. 63, 72). It covers one machine, its compiler and its operating system. It does not discuss distributed memory, message passing, data placement across processors, or compiler-generated communication.

## Input abstraction
ANSI Fortran IV source. The optimizing compiler (CFT, p. 71) vectorizes innermost DO loops and needs no source changes (p. 63). Loops with GOTO, IF or CALL statements were not vectorized at the time (p. 71).

## Target
One CPU with twelve functional units, eight 64-element vector registers and sixteen interleaved memory banks (Table I, p. 65; Table II, p. 67). The text gives twelve I/O channels (pp. 64, 71), but Table I lists 24 (p. 65).

## Data decomposition
Not applicable in this paper. The paper distributes no data across processors. The one placement detail is interleaving within a single memory, which the authors say prevents bank conflicts except for strides of 8 or 16 words (Main Memory Speed, p. 65).

## Computation mapping
Innermost loop iterations map onto vector instructions (pp. 63, 71), and each vector element is processed identically (p. 68). Vectors longer than 64 elements are segmented into 64-element pieces (p. 69). Chaining passes results between functional units without memory references (p. 69). The targets are functional units in one CPU, not processors.

## Communication generation
Not applicable in this paper. The paper describes no communication between processors and no generated messages. The only transfers are I/O to front-end computers (p. 71).

## Compiler / runtime split
Vectorization decisions are made before execution (pp. 63, 71). Chaining and the exchange sequence, with the Cray Operating System as a partner, happen at run time (p. 69). The paper describes no runtime layer for the compiler, so the fully-static tag covers only its loop decisions.

## Evaluation
The authors cite independent benchmark studies (refs 3 and 4) that report 138 MFLOPS sustained and 250 MFLOPS in short bursts (p. 64). Table III gives clock periods per result for sixteen simple DO loops at lengths 1 to 1000, and Fig. 7 gives library-routine timings (p. 71). These timings are attributed to Cray Research work (refs 7 and 8). No multiprocessor or distributed measurements are reported.

## Principal limitation
As the paper states, most early compiled Fortran loops ran slower than hand-coded machine language, and loops with branches were not vectorized (p. 71). Our observation: the evaluation covers one processor and says nothing about scaling.

## Relationship to earlier / later work
The authors state that the design stems from first-generation vector processors and is partly evolved from the CDC 7600 (p. 72). They name the STAR 100 and the Texas Instruments ASC (p. 70), and Cray's earlier CDC 1604, 6600 and 7600 designs (p. 70). They say the reciprocal method for division was used before, for example in the IBM System/360 Model 91 (p. 67). Future compilers are expected to vectorize IF and GOTO loops (p. 71).

## Sources used
| claim | section / page |
|---|---|
| Vectorizing Fortran compiler, no source changes | Introduction, pp. 63-64 |
| Benchmarks of 138 and 250 MFLOPS (refs 3, 4) | Introduction, p. 64 |
| Memory shared by I/O channels and registers | Architecture, p. 64 |
| I/O channel count, text versus Table I | pp. 64, 65, 71 |
| Interleaving and bank conflicts | Main Memory Speed, p. 65 |
| Functional units and registers | Table II; Registers, pp. 67-68 |
| Chaining and 64-element segments | Chaining, p. 69 |
| Exchange sequence and COS | Interrupts and Exchange Sequence, p. 69 |
| Vector versus scalar crossover of 2 to 4 elements | Evolution of the CRAY-1, p. 70 |
| Loop and library timings | Table III; Fig. 7, p. 71 |
| Compiler limits, CAL, multiprogramming | Software, p. 71 |
| Front-end attachment through I/O channels | Front-End Computer Interface, p. 71 |
| CDC 7600 scalar comparison (ref 1) | Summary, p. 72 |

## Open questions for the survey
- Should the CRAY-1 compiler rules (innermost loops only, no branches) serve as the single-node baseline for the survey's vectorization column?
- Should interleaved memory banks be recorded as memory-level placement, or left out of the data-placement column?
- The catalog type "hardware" is not in the taxonomy list. Should the taxonomy add it, or should this card and the Cosmic Cube card keep "full-system"?
