# Data Parallel Algorithms
**Catalog id:** `hillis1986data`
**Citation:** W. Daniel Hillis and Guy L. Steele, Jr. "Data Parallel Algorithms." Communications of the ACM 29(12), special issue, pp. 1170-1183, December 1986. Record used: supplied PDF (no DOI printed in it).
**Paper type:** foundational
**Access:** PDF supplied by the repository owner. Full text read (text layer complete on all 14 pages; minor OCR errors in some reference numbers and symbols, which I did not rely on).
**Card status:** full-read

## Problem
The paper argues that data parallel algorithms suit fine-grained machines with general communication (p. 1170). The algorithms use one processor per data element and typically run in O(log N) time (pp. 1170, 1172). It is a programming-style paper and describes no compiler. It does not discuss distributed memory as such, message passing between autonomous processes, or compiler-generated communication.

## Input abstraction
The notation is parallel pseudo-code over virtual processors, such as "for all k in parallel do ... od", with context flags that select active processors (pp. 1171, 1173). A SEND instruction takes a processor pointer, so communication patterns are data (pp. 1171-1172). The paper defines a notation rather than a language.

## Target
A Connection Machine with 16,384 or 65,536 processors, each with 4,096 bits of memory, driven by a VAX or Symbolics 3600 front end (p. 1170). Any processor can reach any other in unit time through SEND (p. 1171). A microcoded controller maps virtual processors onto hardware processors (p. 1172).

## Data decomposition
Application-defined, at the level of virtual processors. Each data element has its own processor (p. 1172), and addresses such as x + Wy can encode image pixels (p. 1182). Run-time allocation through processor-cons gives new storage its own processor (pp. 1172, 1177). The paper says the programmer is freed from the data-to-hardware mapping (p. 1170).

## Computation mapping
Data parallelism in which each active processor updates the element it holds; in the summation example, processor k updates x[k] (p. 1173). Counting and enumerating are built from sums and sum-prefix (pp. 1174-1175).

## Communication generation
Programmer-explicit. SEND moves data to a destination named by a pointer, and pointers for regular patterns are computed when needed (p. 1172). The front end can broadcast one value to all processors (p. 1171). Reductions and scans use logarithmic-depth exchanges (pp. 1173-1174). The paper does not describe a compiler that derives communication from array references.

## Compiler / runtime split
No compiler is described. At run time the front end controls the SIMD array (p. 1171), and a microcoded controller implements virtual processors (p. 1172). Our observation: a compiler for this model would have to turn array index expressions such as x[k - 2^(j-1)] into SEND or pointer operations, which the paper does not discuss.

## Evaluation
Some run times were measured on the 65,536-processor machine (p. 1170). A sum of 65,536 elements takes about 200 microseconds (p. 1173), and partial sums, counting and enumerating each take about 200 microseconds (p. 1175). Sorting 65,536 32-bit keys takes about 30 ms (p. 1175). The parsing and linked-list examples give no timings (pp. 1176-1180).

## Principal limitation
As the authors state, the model is more sensible with thousands rather than tens of processors (p. 1170), and the combinator example glosses over difficult resource-management issues (p. 1178). Our observation: most timings come from one machine, and the paper makes no comparison with control-parallel implementations, which it raises only as an open question (p. 1182).

## Relationship to earlier / later work
Most algorithms were described earlier in other contexts (p. 1170). Some ideas appear in APL and FP (p. 1172). Earlier SIMD machines, among them ILLIAC IV, Goodyear MPP, Non-Von and ICL DAP, restricted communication to wired patterns (p. 1171). They cite Lim's linked-list labeling and the Pan-Reif sparse matrix algorithm (p. 1182). The paper cites no later systems.

## Sources used
| claim | section / page |
|---|---|
| Front end and array; 16,384 or 65,536 processors | Model of the machine, p. 1170 |
| Context flags, SEND, broadcast, unit-time model | Model of the machine, pp. 1171-1172 |
| Virtual processors and microcoded controller | Model of the machine, p. 1172 |
| Sum of an array and its timing | Sum of an Array of Numbers, pp. 1172-1173 |
| Partial sums; count and enumerate timings | pp. 1173-1175 |
| Radix sort timings and Batcher comparison | Radix Sort, p. 1175 |
| Parsing via parallel prefix | Parsing a Regular Language, pp. 1175-1176 |
| processor-cons | Parallel Processing of Pointers, p. 1177 |
| Combinator reduction and resource issues | Parallel Combinator Reduction, pp. 1177-1178 |
| Linked-list end, partial sums and matching | pp. 1178-1180 |
| Region labeling, Lim, time bounds, x + Wy addresses | pp. 1181-1182 |
| Recursive data parallelism; control-parallel question | Summary and Conclusions, p. 1182 |
| MIMD versus SIMD as a separate question | Summary and Conclusions, p. 1183 |

## Open questions for the survey
- The model hides physical mapping and assumes one processor per element (pp. 1170, 1172). Is "application-defined" the right data-decomposition value?
- SEND is treated as unit time (p. 1172). Does the survey need a cost-model column?
- Should SIMD data-parallel languages be a separate class from distributed-memory compilers?
