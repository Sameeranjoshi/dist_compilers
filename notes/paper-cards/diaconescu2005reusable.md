# Reusable and Extensible High Level Data Distributions
**Catalog id:** `diaconescu2005reusable`
**Citation:** Roxana E. Diaconescu, Bradford Chamberlain, Mark L. James, Hans P. Zima. "Reusable and Extensible High Level Data Distributions." Workshop on Patterns in High Performance Computing, 2005. Record: https://resolver.caltech.edu/CaltechCACR:2005.103. The venue and year come from the catalog; neither is printed in the PDF text layer, so both are unconfirmed.
**Paper type:** language
**Access:** Official open copy (Caltech repository, https://resolver.caltech.edu/CaltechCACR:2005.103). Full text read (text layer complete: yes, all 10 pages; two-column lines were reordered by reading).
**Card status:** full-read

## Problem
The paper argues that existing tools need tedious, error-prone low-level code or offer a few fixed kinds (Abstract, p. 1; Sec. 1, pp. 1-2). It proposes a pattern, "independent of a concrete implementation" (Abstract, p. 1), that lets users define new kinds while the system hides communication and synchronization (Sec. 2.2, p. 2). Chapel is the only realization (Sec. 3, p. 5).

## Input abstraction
Programs declare domains, each pairing an index set with a distribution, and arrays over them (Sec. 2.5, p. 3). Indefinite domains may use object references as indices (Sec. 3.1, p. 5). A user distribution overrides Map(Index), giving the locale, and LocalLayout(Index), giving the offset within it (Sec. 2.5, p. 3).

## Target
The paper names NUMA machines, clusters and peta-scale systems such as Cascade (Sec. 1, p. 2). The model is the Chapel abstract machine with a fixed locale set; local accesses are cheaper (Sec. 3, p. 5). No machine is evaluated.

## Data decomposition
Arrays over a domain follow its distribution (Sec. 2.6, p. 5). Examples are a block class using ceiling division (Sec. 3.2, p. 6), a per-dimension block distribution onto a three-dimensional locale array, and a general distribution in which user code assigns each index (Sec. 3.2, p. 7). Figure 1 lists a cyclic class without code (p. 4).

## Computation mapping
Data and computations can both be mapped to locales, and co-location makes access local (Sec. 3, p. 5). A forall splits its iteration space by the distribution (Sec. 3.2, p. 7). No general placement rule is given.

## Communication generation
Accesses to distributed data are said to handle communication and synchronization transparently (Sec. 2.6, p. 5). The authors argue that a distribution's kind and functionality suffice for a system to infer both (Sec. 2.2, p. 2). The generation method is not described, and code generation is outside the paper's scope (Sec. 3.2, p. 7).

## Compiler / runtime split
The Chapel compiler is written in C++, with domains, indices and distributions as C++ classes (Sec. 3.2, p. 6). The locale set is fixed at program start, and domain instantiation applies Map and LocalLayout to every index (Sec. 2.6, p. 5). The paper gives no static, profile-guided, JIT or adaptive classification.

## Evaluation
None. No measurements or benchmarks are reported. The authors state that they are still evaluating user-defined distributions and their efficiency impact (Sec. 3.2, p. 7), and hope to provide empirical evidence later (Sec. 5, p. 9).

## Principal limitation
The paper states that full user freedom in specifying distributions increases the burden of ensuring good run-time performance (Sec. 2.7, p. 5).

our observation: the paper has no performance data, so its claim that communication and synchronization are inferred is untested here.

## Relationship to earlier / later work
- Chapel (ref. 4) realizes the design (Sec. 1, p. 1; Sec. 3, p. 5); the pattern format follows Gamma et al. (ref. 10; Sec. 1, p. 1).
- HPF encodes distribution kinds in the compiler (Sec. 1, p. 2; refs 14, 15).
- Section 4.1 (pp. 7-8) reviews IVTRAN, Kali, SUPERB, Fortran D, Vienna Fortran, HPF-2 and the PGAS languages; Section 4.2 (pp. 8-9) reviews Hawk, EPEE, CO2P3S, distributed recursive sets (ref. 8, the first author's thesis), ICC++, pC++, Mentat, HPC++ and Charm++.
- Section 4.2 (p. 9) credits Chapel with generalized arrays and combined system-supported and user-defined distributions.

## Sources used
| claim | section / page |
|---|---|
| Tedious, error-prone low-level tuning; few fixed kinds in high-level tools | Abstract, p. 1; Sec. 1, pp. 1-2 |
| Design stated as a pattern independent of implementation | Abstract, p. 1 |
| Concrete distributions override Map and LocalLayout | Sec. 2.5, p. 3 |
| Indefinite domains with object references as indices | Sec. 3.1, p. 5 |
| Arrays follow their domain's distribution; instantiation maps every index | Sec. 2.6, p. 5 |
| Targets: NUMA, clusters, Cascade; local access cheaper | Sec. 1, p. 2; Sec. 3, p. 5 |
| Execution locale set fixed at start; affinity | Sec. 3, p. 5 |
| Block class code (ceiling mapping) | Sec. 3.2, p. 6 |
| Per-dimension block onto a locale array; general distribution | Sec. 3.2, p. 7 |
| Cyclic class listed without code | Fig. 1, p. 4 |
| forall splits iteration space by distribution | Sec. 3.2, p. 7 |
| Transparent communication; inferred synchronization | Sec. 2.6, p. 5; Sec. 2.2, p. 2 |
| Code generation outside scope | Sec. 3.2, p. 7 |
| Burden on run-time performance | Sec. 2.7, p. 5 |
| Evaluation still in progress | Sec. 3.2, p. 7; Sec. 5, p. 9 |
| Venue and year not printed in text layer | Title page, p. 1 (not found); PDF creation metadata (May 2005) |

## Open questions for the survey
- Which parts of the Map and LocalLayout interface reached the Chapel compiler, and is there evidence beyond this paper for the inferred communication and synchronization (Sec. 2.2, p. 2; Sec. 3.2, p. 7)?
- Sec. 2.5 (p. 3) mentions alignment but never develops it. How does the design treat alignment across arrays?
- Which distributions does Sec. 4.2 (p. 9) count as system-supported, and how does the compiler treat them?
