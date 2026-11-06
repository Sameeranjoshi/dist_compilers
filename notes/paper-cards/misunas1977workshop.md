# Report on the Workshop on Data Flow Computer and Program Organization
**Catalog id:** `misunas1977workshop`
**Citation:** Misunas, David P. "Report on the Workshop on Data Flow Computer and Program Organization." MIT Laboratory for Computer Science, Technical Memo MIT/LCS/TM-92, 1977 (November). No DOI printed; record used: supplied PDF.
**Paper type:** foundational
**Access:** PDF supplied by the repository owner. Full text read (the text layer covers all 53 pages but is error-prone OCR of a typed transcript, so claims are paraphrased; cover and front matter were checked against page images).
**Card status:** full-read

## Problem
The report compiles edited talks from a July 1977 MIT workshop on data-flow computers and program organization, co-sponsored by Lawrence Livermore Laboratory (front matter, PDF p. 4). The workshop aimed to bring data-driven computation into practical use, and LLL wanted to see whether data-flow machines could beat its current computers on large codes (Dennis, p. 3; Michael, p. 13).

## Input abstraction
Programs are written in single-assignment or mathematics-style languages (Syre's LAU, p. 11; Arvind's ID, p. 20; Kosinski's language, p. 22). Bryant attempted translations of LLL Fortran programs (p. 19). Program representations are data-driven nets or data dependency graphs (Davis, p. 10; Sandry, p. 9).

## Target
The talks describe four data-flow machine levels (Dennis, pp. 4-5), multiprocessors from Irvine, Burroughs, Clarkson and CERT (Arvind, p. 7; Davis, pp. 25-26; Meyer, pp. 33-34; Syre, pp. 34-35) and a proposed cell array (Dennelly, p. 28). "Distributed" refers to control, operating systems or function (Dennis, p. 5; Davis, p. 10; Meyer, p. 33), and distributed memory is not discussed as such.

## Data decomposition
Program-data placement is not discussed; the storage placement described is architectural: instruction memory is divided into sections (Dennis, p. 5), and packet memory is split into units holding address subsets (Ackerman, p. 25). The airline reservation example partitions its database across flight modules (Dennis, p. 22), with no compiler role.

## Computation mapping
Placement is described as dynamic. A task supervisor assigns each task to an idle processor (Syre, p. 34), and each instruction goes to a computation-activation module once its operands arrive (Meyer, p. 34). Burroughs decomposes a process onto physical substructure when parallelism is available (Davis, pp. 25-26). In the cell-array proposal, each operator occupies one cell linked to its neighbors (Dennelly, p. 28).

## Communication generation
Not applicable in this paper: no compiler-generated communication is described. Communication is only at the hardware level: interconnection networks and packet switching (Dennis, pp. 5, 17), network design (Boughton, pp. 26-27), modules that exchange packets (Leung, p. 33; Ellis, p. 38), and results sent back through a scheduler (Meyer, p. 34).

## Compiler / runtime split
Compilers are mentioned only briefly: two PDP-10 compilers (Arvind, p. 8), microcode generation from a data dependency graph (Sandry, p. 9), an interface module that translates programs into nets (Meyer, p. 33), a LAU compiler (Syre, p. 34), and a Fortran-to-data-flow translator that LLL needs (Hendrickson, p. 15). Placement decisions are made at run time (Syre, p. 34; Meyer, p. 34). No compile-time and run-time split for distributed execution is described.

## Evaluation
No controlled evaluation. Irvine simulations measured processors allocated and waiting times, and found execution time linear in mean communication delay (Thomas, p. 30). Iowa State reports speedups for unoptimized graphs (Oldehoeft and Zingg, p. 31). Syre reports an optimal expansion degree near the square root of the data-processor count (p. 35). The 175 MHz packet-switching requirement and the 100-fold target are design targets, not measurements (Dennis, p. 17).

## Principal limitation
Bryant states that efficient translation from Fortran to data flow would be very difficult (p. 19).
our observation: the report is an edited summary of talks, so its claims are informal and largely unmeasured.

## Relationship to earlier / later work
- Arvind's machine follows Dennis's base language, but its instructions wait at processors, not in a special memory (p. 7).
- Sandry's operating-systems work began from Kosinski's paper (p. 9). Syre's LAU was inspired by a paper by Tesler (p. 11).
- Davis's data-driven nets resemble MIT's, but resources are allocated dynamically, unlike in the Irvine and MIT architectures (p. 10). Guskov's 1974 IFIP paper explains the concepts of such machines (p. 25).
- inferred: packet communication between modules is the nearest the report comes to message passing; the report does not present it as a programming model.

## Sources used
| claim | section / page |
|---|---|
| Cover and title page: title, author, November 1977, MIT/LCS/TM-92 | Front matter, PDF pp. 1-4 |
| Edited, summarized transcription of July 1977 talks | Front matter, PDF p. 4 |
| Instruction memory split into sections; results sent over an interconnection network | Session 1, Dennis, p. 5 |
| Resource allocation is dynamic during execution | Session 1, Davis, p. 10 |
| Efficient Fortran-to-data-flow translation would be very difficult | Session 3, Bryant, p. 19 |
| Packet memory split into units holding address subsets | Session 4, Ackerman, p. 25 |
| Process decomposed onto physical substructure | Session 4, Davis, pp. 25-26 |
| Operators placed one per cell of a programmable array | Session 4, Dennelly, p. 28 |
| Simulated mean communication delay and execution time | Session 5, Thomas, p. 30 |
| Task assigned to an idle processor | Session 6, Syre, p. 34 |
| Instructions assigned to modules; results returned via a scheduler | Session 6, Meyer, pp. 33-34 |
| Optimal expansion degree near the square root of data processors | Session 6, Syre, p. 35 |
| 175 MHz packet switching; 100-fold target | Session 2, Dennis, p. 17 |

## Open questions for the survey
- Does the survey need the 1977 runtime placement ideas (task supervisors, computation-activation modules, hierarchical decomposition) as background, or are they hardware choices outside its scope?
- The report's communication is packet-based and hardware-level. Should the survey cite it only as background to message passing, or mark it out of scope for compiler-generated communication?
- Did any of the operator or task placements proposed here reach the later compilers the survey covers? Answering that needs sources beyond this report.
