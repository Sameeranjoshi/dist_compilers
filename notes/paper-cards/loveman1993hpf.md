# High Performance Fortran  
**Catalog id:** `loveman1993hpf`  
**Citation:** Loveman, D. B. "High Performance Fortran." IEEE Parallel & Distributed Technology, February 1993, pp. 25-42. No DOI printed; record used: PDF title page and IEEE copyright line 1063-6552/93/0200-0025.  
**Paper type:** language  
**Access:** PDF supplied by the repository owner. Full text read. The text layer is complete for all 18 pages. Sidebars and the two-column layout are extracted out of order in places, and figures are not recoverable as text.  
**Card status:** full-read

## Problem
Fortran-90 offers array operations but no way to say how data is allocated across the processors of a distributed-memory machine (Introduction). The HPF Forum, formed in 1992, aimed to make Fortran-90 perform well and be usable for computationally intensive work on SIMD, MIMD and vector machines (Introduction). The article presents Fortran-90, its basis in Fortran-77, its parallel implications and the HPF extensions (Introduction).

## Input abstraction
HPF is Fortran-90 plus directives written as !HPF$ comments, together with a few first-class constructs such as FORALL (Introduction; Data distribution). The mapping vocabulary is PROCESSORS, TEMPLATE, ALIGN, DISTRIBUTE, DYNAMIC, REALIGN, REDISTRIBUTE, VIEW and INHERIT. Alignment allows offsets, collapse, transposition, reversal and replication. Distribution gives BLOCK, CYCLIC, BLOCK(n) or "*" per dimension onto a rectilinear processor arrangement (The Align directive; The Distribute directive).

## Target
The article addresses SIMD and MIMD systems and vector processors (Introduction). Its examples are a DECmpp 12000 Sx Model 200 with 8,192 processors and a single DEC 3000 AXP workstation (Intrinsic functions and library routines). Extrinsic procedures are the interface for distributed local code (Extrinsic procedures).

## Data decomposition
Objects are aligned to an index space, which is distributed onto a rectilinear processor arrangement. Templates are index spaces that occupy no storage (Data distribution; Template directive). Replication lets the compiler read whichever copy is nearest (The Align directive). The extrinsic interface assumes each array axis maps to at most one processor axis, with no skewed distributions (Extrinsic procedures).

## Computation mapping
The article leaves placement of work to the compiler, which uses the annotations to minimize communication while keeping parallelism (Data distribution). Parallelism is asserted, not derived: FORALL assignments must not assign one element twice, and functions called from FORALL must be PURE (The ForAll construct; Pure procedures). INDEPENDENT asserts that loop iterations do not interfere, which the compiler may use to reorganize communication (The Independent directive).

## Communication generation
Some Fortran-90 statements imply communication, such as broadcasting a scalar assigned to an array (Fortran-90 on parallel machines). Reduction, scatter and parallel-prefix intrinsics cover global operations (Intrinsic functions and library routines). Programmers can write explicit SPMD local code through extrinsic procedures (Extrinsic procedures). No communication-generation method is described.

## Compiler / runtime split
Specification directives take effect on entry to a scoping unit, but some of their expressions depend on run-time values (Data distribution). Allocatable objects are mapped each time they are allocated (Data distribution). System inquiry functions report the configuration at run time, and the article states that HPF programs can be compiled for machines whose configuration is unknown at compile time (Intrinsic functions and library routines).

## Evaluation
None. The article is an overview and reports no measurements. Its future-work section says there is as yet no real experience with first compilers or with the code users will write (Future work).

## Principal limitation
Stated: the Forum simplified the design to reach agreement within a year. Missing capabilities include irregular and user-defined distributions, nonrectangular processor arrangements, explicit MIMD message passing and parallel I/O (Future work; The HPF subset). Our observation: the author edited the specification and the article reports no implementation, so its performance statements are design intent.

## Relationship to earlier / later work
The article builds on Fortran-77, Fortran-90 and MIL-STD-1753 (Fortran-90 sections; The HPF subset). It traces ForAll to Fortran-8x, to implementations at Compass, Digital, MasPar and Thinking Machines, and to research at Rice, Syracuse and Vienna (The ForAll construct). Its related-works sidebar lists Vienna Fortran, Kali, Fortran-D and Fortran-90D (Related works sidebar). The article points to a planned workshop and a second Forum process as the next steps (Future work).

## Sources used
| claim | section / page |
|---|---|
| Motivation, HPF Forum history, article scope | Introduction |
| Two-level mapping model, templates, dynamic attribute | Data distribution; Template directive |
| Processors arrangements and views | The Processors directive and processor views |
| Align forms, replication | The Align directive |
| Distribute forms | The Distribute directive |
| Realign, Redistribute, Dynamic | Dynamic, Realign, and Redistribute directives |
| FORALL, PURE, INDEPENDENT | The ForAll construct; Pure procedures; The Independent directive |
| Inquiry and library intrinsics; example machines | Intrinsic functions and library routines |
| Extrinsic procedure model and axis restriction | Extrinsic procedures |
| Sequence and storage association | Sequence and storage association |
| Subset, simplifications, missing features | The HPF subset; Future work |
| Related works | Related works sidebar |

## Open questions for the survey
- Which Journal of Development constructs (Execute-On-Home, Local-Access) were later adopted, and did their absence from the subset change early placement of work?
- How do the rectangular-processor and no-skew restrictions affect codes whose data maps do not fit a rectangular arrangement?
- Which directive forces the most run-time analysis, for example dynamic realignment, and what does that imply for a decomposition-based model?
