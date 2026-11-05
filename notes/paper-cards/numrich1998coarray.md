# Co-Array Fortran for parallel programming
**Catalog id:** `numrich1998coarray`
**Citation:** Robert W. Numrich and John Reid. "Co-Array Fortran for parallel programming." 1998. Record used: title page and text of the supplied PDF (31 pages). The PDF prints no venue or date; the 1998 year is taken from the catalog id and from the reference to this work in chen2003upc (Sec. 1 and its reference list, which gives Rutherford Appleton Laboratory technical report RAL-TR-1998-060).
**Paper type:** language
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete. A few OCR artifacts (for example spaced-out keywords and "Numfich") do not affect content.
**Card status:** full-read

## Problem
The paper asks for the smallest change that makes Fortran 95 a robust, efficient parallel language (Sec. 1). It separates work distribution from data distribution, which the authors say HPF, CRAFT and OpenMP entangle (Sec. 1, 5).

## Input abstraction
A Co-Array Fortran program is replicated into images that run asynchronously, each with its own data objects (Abstract, Sec. 3.1). Variables may be declared with trailing co-dimensions in square brackets. A reference without brackets is local, and a reference with brackets is remote (Sec. 1, 3.2-3.3). Co-array subobjects appear only in intrinsic operations, assignments and I/O lists (Sec. 3.4). Synchronization uses intrinsics such as sync_all, sync_team and sync_memory (Sec. 3.8, 3.10).

## Target
The paper is language-level and does not name a machine for evaluation. It says a co-array may be an array of higher rank on shared-memory machines, or stored at the same address on each processor of a distributed-memory machine (Sec. 3.2, note). The one-sided SHMEM library on Cray T3D and T3E systems is the motivating model (Sec. 1, 5).

## Data decomposition
The programmer chooses the distribution by declaring co-arrays. Every co-array has the same bounds on every image, and each image holds its own part (Sec. 1, 3.2). Allocatable co-arrays and pointer components allocated only on needed images handle non-uniform sizes (Sec. 1, 3.6-3.7). No automatic decomposition is described; the examples use a 2-D image grid (Sec. 4.1).

## Computation mapping
Work is assigned by the programmer through the image index (this_image) and ordinary Fortran control constructs (Sec. 1, 3.1). Subsets of images can synchronize as teams (Sec. 2.6, 3.8), for example the hydro and radiation split in Sec. 2.6. The compiler does not place work.

## Communication generation
Communication is explicit: it occurs at bracketed references and in procedures that contain them (Abstract, Sec. 1, 3.3). The authors say the compiler "generates in-line code" for fine-grained patterns, and that execution need not block until communication completes (Sec. 5). Collective and neighbour patterns are written by hand: a halo assemble with sync_all (Sec. 2.4), a gather to image 1 for maxima (Sec. 2.3), a tree sum in log2 steps (Sec. 4.4-4.5), and data redistribution between differently spread co-arrays (Sec. 2.2, 4.2).

## Compiler / runtime split
The compiler may keep co-array data in registers or cache between synchronization points, and sync_memory is the only mechanism that makes such data visible (Sec. 3.8). The number of images may be fixed at compile, link or execute time (Sec. 3.1). The specification leaves the runtime design open. The paper treats critical sections as an intrinsic, and says the authors have not found a way to program them in Co-Array Fortran (Sec. 3.8).

## Evaluation
The paper reports no timings, speedups or benchmark measurements. Its evidence is code size and clarity over examples (Sec. 2, 4). The only performance statement is a quoted remark by Wallcraft that a co-array halo exchange is typically two to three times faster than MPI on SMP and DSM systems (Sec. 5). The authors do not measure it.

## Principal limitation
The authors place synchronization on the programmer: "it is the programmer's responsibility" to order accesses, and the compiler may assume a single image between synchronization calls (Sec. 3.8). They also restrict co-arrays: they cannot be pointers or automatic, components cannot be co-arrays, and co-array rank is capped at seven (Sec. 3.2, 3.7).
our observation: the performance case rests on an unmeasured anecdote, so the claimed benefit over message passing is untested in the paper.

## Relationship to earlier / later work
- The language grows from F-- (Numrich 1997; Numrich and Steidel 1997) and from Cray internal reports (Sec. 1).
- Compared with directive models (HPF, CRAFT, OpenMP) and with MPI and its inconsistencies with Fortran 90 (Sec. 1, 5).
- Compared with the SHMEM library (Sawdey et al. 1995) and with BSP (Valiant 1990; Hill et al. 1997) (Sec. 5).
- Parts entered the Cray Fortran 90 compiler, and an application was converted (Numrich, Reid and Kim 1998) (Sec. 1).
- inferred: the Berkeley UPC analysis in this survey set (chen2003upc, Sec. 1) lists Co-Array Fortran as a contemporary global address space language.

## Sources used
| claim | section / page |
|---|---|
| Design question and separation of work and data distribution | Sec. 1; pp. 1-2 |
| Images, co-arrays, bracketed remote references | Sec. 1, 3.2-3.3; pp. 2-3, 9-11 |
| Examples: Laplacian, redistribution, maximum, halo assemble, teams, tiled I/O | Sec. 2.1-2.7; pp. 3-6 |
| Compiler freedom and sync_memory | Sec. 3.8; pp. 13-15 |
| Restrictions on co-arrays and pointers | Sec. 3.2, 3.7; pp. 9-10, 12-13 |
| Critical sections not programmable | Sec. 3.8; p. 15 |
| Improved examples | Sec. 4.1-4.5; pp. 19-22 |
| Comparison with directives, SHMEM, BSP, MPI, and the Wallcraft remark | Sec. 5; pp. 22-24 |
| Summary of features | Sec. 6; pp. 24-25 |
| Earlier F-- work and references | Sec. 1, 8; pp. 2-3, 25-26 |
| Appendix extensions | App. 1-3; pp. 27-31 |

## Open questions for the survey
- Did implementations honour the register and cache freedom of Sec. 3.8, and how did the sync_memory rules hold up in practice?
- Is the 2-3x advantage over MPI (Sec. 5) reproducible on measured benchmarks, and on which machine classes?
- How do the team-based synchronization rules (Sec. 3.8, 3.10) compare with the synchronization models of the other language entries in the survey?
