# Automatic Data Structure Selection and Transformation for Sparse Matrix Computations
**Catalog id:** `bik1996automatic`
**Citation:** Bik, Aart J. C., and Harry A. G. Wijshoff. "Automatic Data Structure Selection and Transformation for Sparse Matrix Computations." IEEE Transactions on Parallel and Distributed Systems 7, no. 2 (1996): 109-126. No DOI appears in the PDF text; record used: title page and running headers of the PDF.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read (text layer complete for prose, equations and references; 18 PDF pages, journal pages 109-126; figure graphics and some garbled table cells, such as Table 4 exponents, not interpreted).
**Card status:** full-read

## Problem
Sparse codes that manage storage explicitly, through indirect addressing, are hard to maintain and block most compiler optimisations (Sec. 1, p. 109). The method keeps the program on dense arrays, marks the sparse matrices with an annotation, and selects and generates storage at compile time (Sec. 1, pp. 109-110). The abstract also states that the programmer's task is greatly reduced (p. 109).

## Input abstraction
The input is a FORTRAN-like program on dense two-dimensional arrays, and annotated matrices are treated as implicitly sparse (Sec. 1, p. 110). Loop bounds are affine, and each access is described by a single affine mapping (Sec. 2.2, pp. 110-111). Accidentally stored zeros are not exploited (Sec. 3, p. 113).

## Target
The generated code is FORTRAN-like and calls primitives kept in a separate library file (Sec. 6, p. 120). The choice between (DL) and (LL) storage depends on the target machine (Sec. 5.2, p. 118). Timings use an HP-UX 9000/720 and one Cray C98/4256 CPU (Sec. 7, pp. 123-125). No distributed or multiprocessor target is described.

## Data decomposition
Not applicable in this paper. Data-structure selection picks a storage format for each matrix on one machine (Sec. 5.2, pp. 118-119). The word "partitioned" in Sec. 4 (p. 112) refers to splitting execution sets, not data.

## Computation mapping
Not applicable in this paper. Guard encapsulation restricts each loop to the iterations that touch stored entries (Sec. 4.4, pp. 114-115). Nothing is assigned to processors, and parallel execution does not appear in the body text (Secs. 4 to 6).

## Communication generation
Not applicable in this paper. The introduction cites communication overhead on distributed-memory computers as one reason sparse codes run slowly (Sec. 1, p. 109), but the method neither analyses nor generates communication. Expansion's scatter and gather are local moves (Sec. 6.4, p. 121).

## Compiler / runtime split
Compile-time work includes fixing storage when the nonzero structure is known (Sec. 2.1, p. 110) and resolving conflicts (Sec. 5.3, pp. 118-120). Dynamic structures are adapted at run time (Sec. 4.1, p. 112).

## Evaluation
The authors call the experiments preliminary (Sec. 1, p. 110). LU factorisation of D(n,5) matrices shows a substantial gain over the dense version, even for small n (Table 3, p. 123). The generated tridiagonal solver performs identically to a hand-coded one (p. 124). The reshaped version is clearly superior to the row-wise and column-wise versions on four Harwell-Boeing matrices (Table 4, p. 125).

## Principal limitation
The paper states that not all conflicts between access patterns can be resolved, so control strategies are still needed (Sec. 5.3, p. 119). Fill-in reordering and use of nonzero structure are listed as open issues (Sec. 8, p. 125).
our observation: all experiments run on one HP-UX 9000/720 machine or one Cray CPU, so the paper gives no evidence for parallel or distributed targets.

## Relationship to earlier / later work
The introduction states that earlier "concurrentization" methods pre-evaluate and reorder indirectly addressed loops, and fail when subscripts change (Sec. 1, p. 109; refs. 33, 35, 36). Conflicts are resolved with unimodular transformations and index set splitting (Sec. 5.3, p. 119). The authors compare with SPARK hand-coded versions (Sec. 7, p. 125). The reference list has no Allen and Kennedy entry, so the paper states no relationship to that work (pp. 125-126).
inferred: the survey's distributed-memory link is not stated here. Reference 35 is titled as work on message-passing machines, but the text does not describe it.

## Sources used
| claim | section / page |
|---|---|
| Only distributed-memory mention: communication overhead in the introduction | Sec. 1, p. 109 |
| Pre-evaluation and reordering methods fail when subscripts change | Sec. 1, p. 109 |
| Annotation of implicitly sparse matrices; three-phase outline | Sec. 1, pp. 109-110 |
| Static versus dynamic structures; affine bounds and subscripts | Sec. 2, pp. 110-111 |
| Accidentally stored zeros not exploited | Sec. 3, p. 113 |
| Abstract data structure, conditions, dominating guards | Sec. 4, pp. 112-113 |
| Guard encapsulation, expansion, loop distribution and fusion | Secs. 4.4-4.5, pp. 114-116 |
| Access pattern collections; storage schemes (DL) and (LL) | Sec. 5, pp. 117-118 |
| Conflicts not always resolvable | Sec. 5.3, p. 119 |
| Generated primitives; scatter and gather | Sec. 6, pp. 120-122 |
| LU factorisation; Table 3 | Sec. 7, pp. 122-123 |
| Tridiagonal solver; identical performance | Sec. 7, p. 124 |
| Table 4 (Cray CPU timings); SPARK comparison | Sec. 7, p. 125 |
| Open issues; prototype compiler MT1 | Sec. 8, p. 125 |
| No processor, data-partitioning, message or communication content; no Allen and Kennedy citation (full-text search of pp. 109-126) | pp. 109-126 |

## Open questions for the survey
- Its only distributed-memory content is one introductory sentence (Sec. 1, p. 109). Should it stay as background?
- Refs. 33, 35 and 36 are the only parallelisation methods the text discusses. Should the survey pull them?
- The taxonomy lacks values for storage-format selection and operation count. Should it gain them?
