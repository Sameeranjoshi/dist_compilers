# Automatic Translation of FORTRAN Programs to Vector Form
**Catalog id:** `allen1987automatic`
**Citation:** Allen, Randy, and Ken Kennedy. "Automatic Translation of FORTRAN Programs to Vector Form." ACM Transactions on Programming Languages and Systems 9, no. 4 (1987): 491-542. No DOI appears in the PDF text; record used: journal line on the first PDF page.
**Paper type:** foundational
**Access:** PDF supplied by the repository owner. Full text read (text layer complete for prose, equations and references; 52 PDF pages per pdfinfo, about 19,500 words; figure graphics not interpreted, only captions and labels).
**Card status:** full-read

## Problem
The paper asks how existing FORTRAN DO loops can be rewritten automatically as FORTRAN 8x array statements without changing their meaning (Sec. 1, pp. 491-493). A translator is offered as a way to avoid massive manual recoding (p. 491). It treats data dependence as the criterion: a translation is correct if it preserves the dependences (p. 491). The authors argue that a translator can attempt more ambitious transformations than an embedded vectorising stage, because the translation is usually done only once (p. 492).

## Input abstraction
The input is FORTRAN 66 or 77 (Sec. 1, p. 492). The translator normalises loops and rewrites subscripts as linear functions of induction variables before testing dependences (Sec. 3, pp. 498-499). The exact test covers linear subscripts (Sec. 4.1, p. 501). IF conversion turns control dependences into data dependences (Sec. 6, p. 531).

## Target
The output is FORTRAN 8x, with array assignments, sections, IDENTIFY, WHERE and reduction functions (Sec. 2, pp. 493-497). The motivating hardware is vector computers and array processors (Sec. 1, p. 491). No distributed-memory or multiprocessor target is described.

## Data decomposition
Not applicable in this paper. The output operates on single arrays, and no data partitioning or placement across processors appears (Sec. 2, pp. 493-497). IDENTIFY only aliases existing storage (Sec. 2.3, p. 496).

## Computation mapping
The mapping decision is which loop levels become vector operations. A statement may run in parallel over its innermost p(S) loops (Sec. 4.4, p. 514), and the code generator emits parallel statements over those dimensions (Sec. 5.2, p. 518). Nothing is assigned to processors, so data-parallelism is the nearest tag.

## Communication generation
Not applicable in this paper. The text has no model of messages or inter-processor transfer. "Distributed" appears only in the copyright notice (p. 491), and "communication" only in a reference entry (p. 541).

## Compiler / runtime split
All decisions are made at compile time (Secs. 4 to 6). The only input parameter the paper names is the minimum profitable vector length (Sec. 5.3.3, p. 529). Code generation is bounded by O((m+n)N) (Theorem 7, pp. 519-520). No run-time component is described.

## Evaluation
Most support is analytic: proofs (Secs. 4 and 5; Appendix, pp. 533-540) and worked examples (Sec. 3, pp. 497-500). The only measurement is translation time: roughly one minute of CPU time for PFC against roughly ten for PARAFRASE, on a composite set of Los Alamos kernels (Sec. 7, p. 533).

## Principal limitation
The paper states that its dependence tests are necessary but not sufficient. When the gcd or Banerjee conditions cannot exclude a dependence, the algorithm assumes one (Sec. 4.1, pp. 502-504). Unknown symbolic constants are treated the same way (Sec. 5.4, p. 530).
our observation: the evaluation times only the translator, so the paper gives no evidence on the speed of the vector code it generates.

## Relationship to earlier / later work
The paper states that PFC began from Kuck and others' Illinois research and first used PARAFRASE, which proved too inefficient (Sec. 1, p. 493; Sec. 7, p. 533). It names the Texas Instruments ASC compiler, the Cray-1 FORTRAN compiler and the Massachusetts Computer Associates Vectorizer as influences (Sec. 1, p. 493). Wolfe is credited with the interchange observation (Sec. 5.3.1, p. 521).
inferred: the survey brief presents this paper as the base for later distributed-memory compilers. The paper mentions no such later work.

## Sources used
| claim | section / page |
|---|---|
| Translation must preserve dependences; a loop and an array statement differ in semantics | Sec. 1, p. 491 |
| Translator approach, one-time cost, PFC as FORTRAN to FORTRAN 8x translator | Sec. 1, pp. 492-493 |
| FORTRAN 8x array, section, IDENTIFY and WHERE forms | Sec. 2, pp. 493-497 |
| Normalisation, induction variable substitution, folding, worked example | Sec. 3, pp. 498-499 |
| Three vector translation subphases; abstract syntax tree as internal form | Sec. 3, p. 500 |
| Self-dependence test; gcd and Banerjee conditions; necessary-only character | Sec. 4.1, pp. 501-504 |
| True, anti and output dependence; dependence graph; r-blocks | Sec. 4.2, pp. 505-509 |
| Carrier-level tests (Theorems 4 and 5) | Sec. 4.3, pp. 510-512 |
| Dependence depth, nesting level, parallelism index | Sec. 4.4, pp. 512-515 |
| Augmented dependence graph, level-k code generation, complexity | Secs. 5.1-5.2, pp. 515-520 |
| Loop interchange, recurrence breaking, thresholds | Sec. 5.3, pp. 520-530 |
| Unknown symbolic constants | Sec. 5.4, p. 530 |
| IF conversion | Sec. 6, pp. 530-533 |
| Implementation size; translation-time comparison with PARAFRASE | Sec. 7, p. 533 |
| No distributed-memory, message or data-placement content (full-text search of pp. 491-542) | pp. 491-542 |

## Open questions for the survey
- The paper has no processor or message model. Should the survey cite it only for the dependence test, with any distributed-memory extension marked inferred?
- Does the message-vectorization tag need a link to the level-k vector code generator (Sec. 5.2)? The paper makes no such link.
- The paper gives no measurements of generated code. Does the survey need that evidence from elsewhere?
