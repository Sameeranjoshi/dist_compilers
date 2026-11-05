# The Rise and Fall of High Performance Fortran: An Historical Object Lesson
**Catalog id:** `kennedy2007rise`
**Citation:** Kennedy, K., Koelbel, C., and Zima, H. "The Rise and Fall of High Performance Fortran: An Historical Object Lesson." History of Programming Languages III (HOPL III), San Diego, CA, June 2007, article 7. DOI 10.1145/1238844.1238851 (printed on p. 7-1).
**Paper type:** experience
**Access:** PDF supplied by the repository owner. Full text read. The text layer is complete in the body; the page-1 copyright text is interleaved with the abstract and is partly unreadable, which does not affect the content.
**Card status:** full-read

## Problem
HPF, a standardization effort begun in 1991, brought data-parallel programming to distributed-memory Fortran. The paper traces its precursors, describes the HPF 1.0, 1.1 and 2.0 standards and HPF/JA, and analyzes why HPF lost users despite its influence (pp. 7-1 to 7-17).

## Input abstraction
HPF 1.0 is based on Fortran 90, with the extensions written as directive comments that a sequential compiler can ignore, so one program can run on either kind of machine (Section 3, p. 7-10). Distributions are set by DISTRIBUTE and ALIGN, parallel loops by INDEPENDENT, and FORALL offers an alternative to array assignment (Section 3, pp. 7-10 to 7-12).

## Target
Distributed-memory computers, in which each processor has its own memory and processors are linked by meshes or hypercubes (Section 1.1, p. 7-3). Period compilers generally translated HPF into Fortran with MPI calls (Section 3, p. 7-13).

## Data decomposition
HPF 1.0 provided BLOCK, CYCLIC and CYCLIC(K), with ALIGN for matching arrays (Section 3, pp. 7-10 to 7-11). Block-cyclic was kept because it balances load on triangular computations such as LU decomposition (Section 2, p. 7-8). HPF 2.0 added GEN_BLOCK and INDIRECT distributions (Section 5, p. 7-14).

## Computation mapping
The owner-computes rule places each calculation on the processors that own its operands (Section 2, p. 7-6; Section 3, p. 7-11). The Rice group later generalized it to any processor that maximizes locality (Section 2, pp. 7-7). HPF 2.0 added an ON directive so that the programmer can choose the executing processor (Section 5, p. 7-14).

## Communication generation
Communication is generated automatically from the declared layout (Section 1.2, p. 7-5). Fortran D aimed to move data in large blocks rather than single words (Section 2, p. 7-6). General block and indirect distributions need an inspector that builds a communication schedule at run time (Section 2, p. 7-7). The HPF library supplies sum reductions, gather, scatter and prefix operations (Section 3, p. 7-12).

## Compiler / runtime split
The paper argues that proper HPF compilation needs extensive global analysis of distributions, partitioning, communication generation and overlap of communication with computation (Section 4, p. 7-12). The inspector handles the irregular distributions at run time (Section 2, p. 7-7).

## Evaluation
None. The paper reports no measurements of its own. It cites other results: dHPF, with multipartitioning added, came within a few percentage points of hand-coded MPI on NAS SP and BT (Section 7, p. 7-17, citing [25]). An HPF Impact3D run reached over 17 percent efficiency on 128 to 1024 processors (p. 7-17, citing [24]). Impact3D on the Earth Simulator ran at nearly 15 teraflops (Section 6.1, p. 7-15).

## Principal limitation
The authors attribute HPF's limited success to four causes: immature compiler technology combined with impatience in the HPC community, insufficient support for important features, inconsistent implementations, and the complex link between a program and its performance (Sections 3-4, p. 7-12). They also state that no vendor or project implemented the full set of HPF 2.0 approved extensions (Section 5, p. 7-14).

our observation: the causal analysis is interpretive, drawn from experience and reports rather than from controlled comparisons.

## Relationship to earlier / later work
Stated by the paper: Fortran D and Vienna Fortran deeply influenced HPF (Section 2, p. 7-5). Fortran D's two-level template-and-distribution scheme was adopted into HPF in a similar form (Section 2, p. 7-6). SUPERB took a Fortran 77 program and a generalized block distribution and produced message-passing code (Section 2, pp. 7-6 to 7-7). An overview of that compilation technology is given by Zima and Chapman [101] (Section 2, p. 7-7). General block and indirect distributions from Vienna Fortran were later incorporated into HPF 2.0 (Section 2, p. 7-7; Section 5, p. 7-14). HPF+ and HPF/JA extended HPF (Section 6.1, pp. 7-14 to 7-15). Chapel, Fortress and X10 are named as successors that carry HPF's ideas forward (Section 6.2, pp. 7-15 to 7-16).

## Sources used
| claim | section / page |
|---|---|
| Parallel architecture background | Section 1, pp. 7-1 to 7-5 |
| Precursors: Fortran D, SUPERB, Vienna Fortran, CM Fortran | Section 2, pp. 7-5 to 7-8 |
| HPF 1.0 language features | Section 3, pp. 7-10 to 7-12 |
| Reasons for limited success | Section 4, pp. 7-12 to 7-14 |
| HPF 2.0, HPF/JA, OpenMP, HPCS languages | Sections 5-6, pp. 7-14 to 7-16 |
| Lessons, dHPF and Impact3D results | Section 7, pp. 7-16 to 7-18 |
| Citation of Zima and Chapman [101] | Section 2, p. 7-7; reference list, p. 7-21 |

## Open questions for the survey
- The paper says most HPF 2.0 extensions were never implemented. Should the survey treat HPF 2.0 as a separate entry from HPF 1.x?
- The authors weigh user impatience alongside compiler maturity. How should the survey weigh the two?
- The dHPF and Earth Simulator results are reported here only from cited sources. Should the survey verify them against those sources?
