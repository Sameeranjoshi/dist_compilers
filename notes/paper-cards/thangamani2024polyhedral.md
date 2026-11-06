# A Survey of General-purpose Polyhedral Compilers
**Catalog id:** `thangamani2024polyhedral`  
**Citation:** Arun Thangamani, Vincent Loechner, Stéphane Genaud. "A Survey of General-purpose Polyhedral Compilers." ACM Transactions on Architecture and Code Optimization, vol. 21, no. 4, Article 72, 2024. DOI 10.1145/3674735 (ACM reference format, p. 72:1).  
**Paper type:** survey
**Access:** PDF supplied by the repository owner. Full text read (text layer complete: all 26 pages carry text; pdfinfo reports 26 pages, not 27; Figures 1-10 appear only as captions).  
**Card status:** full-read  

## Problem
The paper asks which general-purpose polyhedral compilers exist as of 2024 and how well they optimize and parallelize loop nests (Abstract, p. 72:1; Sec. 1, p. 72:2). It lists the tools, then benchmarks eight of them on PolyBench/C for correctness and performance (Sec. 1, p. 72:2; Sec. 4, p. 72:6).

## Input abstraction
Inputs are C loop nests. Built-in tools detect static control parts automatically, while source-to-source tools may need the regions annotated (Sec. 1, p. 72:2). Benchmarks are PolyBench/C kernels, chosen over the NAS, UTDSP and Livermore suites (Sec. 3, p. 72:5).

## Target
Only single-node hardware is measured: a 2 x 20-core Intel Xeon node for sequential and OpenMP runs (Sec. 4.1, pp. 72:6, 72:9) and an A100 GPU for PPCG's CUDA and OpenCL output (Sec. 4.6, p. 72:20). R-Stream is described as targeting multicores, GPUs and FPGAs, and its successor exposes a node-distribution level, but neither is benchmarked (Sec. 2.3.2, p. 72:4).

## Data decomposition
Not treated. Tiling appears as a loop transformation for locality and tile-level parallelism (Sec. 2.1.1, p. 72:3; Sec. 4.5, p. 72:18), not as partitioning data across memories. "Data locality" in this paper means cache behavior, measured as last-level cache misses (Sec. 4.4.1, p. 72:12; Table 2, p. 72:13).

## Computation mapping
Loop parallelism is mapped to cores through OpenMP. The authors examine which loop is parallelized and how many regions and cores each run uses, attributing poor efficiency to region creation or limited core use (Sec. 4.4.3, pp. 72:15-72:17; Table 4, p. 72:17). PPCG decides the host and GPU split (Sec. 2.1.4, p. 72:3).

## Communication generation
Not treated for distributed memory. The body text contains no MPI or message-passing discussion. The only transfers discussed are PPCG's host-device copies, a 0.2 to 0.3 second setup overhead (Sec. 4.6.1, p. 72:20). The body text never uses the word "communication"; it appears only in reference entries, including the title of [46], which the text cites for iteration space slicing (Sec. 2.1.6, pp. 72:3-72:4; reference list, pp. 72:25-72:26).

## Compiler / runtime split
The general-purpose tools are static compilers (Sec. 7, p. 72:23): SCoP extraction, ILP-based scheduling and code generation (Sec. 1, p. 72:2). Runtime-adaptive designs appear only in the unbenchmarked set, such as APOLLO's profile-and-rollback loop optimizer (Sec. 2.3.8, p. 72:5) and a JIT built on PPCG (Sec. 2.3.3, pp. 72:4-72:5). Source-to-source tools emit OpenMP or CUDA code (Sec. 2.1.4, p. 72:3).

## Evaluation
Eight compilers (GRAPHITE, Polly, Polygeist, PolyOpt, Pluto, PoCC, PPCG, CHiLL) run on the 30 PolyBench/C kernels with gcc, clang and icc back ends, reported as speedups and perf counters (Sec. 4.1-4.4, pp. 72:6-72:19). Errors and wrong outputs are listed per tool (Sec. 4.1.1-4.1.2, p. 72:7). The authors conclude that sequential gains come mainly from data locality, while parallel gains are limited by region overhead and core use (Sec. 5, pp. 72:21-72:22).

## Principal limitation
As the authors state, PolyBench/C has seen no significant recent extension, lacks machine-learning affine patterns, and uses dataset sizes that are outdated for current HPC nodes (Sec. 5, p. 72:22).  
our observation: the study covers one CPU node and one GPU, so none of its performance findings bear on multi-node or distributed-memory targets.

## Relationship to earlier / later work
- The authors cite earlier surveys (Schneck 1973; Mustafa 2022) and studies covering one or two compilers (Simbürger et al. 2013; Pfaffe et al. 2019; Fontaine et al. 2018), and say theirs compares most of the tools (Sec. 6, p. 72:23).
- They compare their PPCG CUDA results with Verdoolaege et al. (2013) and report the same trends at smaller speedups (Sec. 4.6.1, p. 72:20).
- They note that the R-Stream team joined Qualcomm, which now develops the Qualcomm Polyhedral Mapper (Sec. 2.3.2, p. 72:4).
- inferred: unat2017trends (Sec. 4.2, p. 3013) mentions polyhedral analysis but none of the tools surveyed here.

## Sources used
| claim | section / page |
|---|---|
| Survey scope: most of the currently available polyhedral compilers | Sec. 1, p. 72:2 |
| Static control parts; source-to-source annotation needs | Sec. 1, p. 72:2 |
| Three-way classification: source-to-source, built-in, application or target-specific | Secs. 2.1-2.3, pp. 72:3-72:5 |
| Compilers excluded from benchmarking, with reasons | Sec. 2.3, p. 72:4 |
| R-Stream FPGA and node-distribution mentions; Qualcomm successor | Sec. 2.3.2, p. 72:4 |
| APOLLO runtime profiling; Tensor Comprehensions JIT | Secs. 2.3.3, 2.3.8, pp. 72:4-72:5 |
| PolyBench/C chosen and its categories | Sec. 3, pp. 72:5-72:6 |
| Hardware: Xeon 2 x 20 cores; A100; AMD results omitted | Sec. 4.1, p. 72:6; footnote 2, p. 72:6 |
| Eight compilers and versions | Sec. 4.1, Table 1, pp. 72:6-72:7 |
| Errors and wrong outputs | Secs. 4.1.1-4.1.2, p. 72:7 |
| Parallel speedups and parallel regions | Secs. 4.2.2, 4.4.3; Table 4, pp. 72:8-72:17 |
| Cache-miss, vector and branch counters | Sec. 4.4, Tables 2-3, pp. 72:11-72:16 |
| Vectorization hints the back-end compiler may ignore | Sec. 4.4.1, p. 72:12 |
| PPCG CUDA and OpenCL on A100; 2013 comparison | Secs. 4.6.1-4.6.2, pp. 72:20-72:21 |
| Conclusions on sequential and parallel code | Sec. 5, pp. 72:21-72:22 |
| PolyBench/C limits | Sec. 5, p. 72:22 |
| Related surveys and studies | Sec. 6, p. 72:23 |
| No MPI or message passing in the body text (full-text search) | Secs. 1-7 |

## Open questions for the survey
- R-Stream's node-distribution level (Sec. 2.3.2, p. 72:4) is the only hint of multi-node generation, and it is not evaluated. Which surveyed tools generate multi-node code?
- Should the source-to-source versus built-in axis (Secs. 2.1-2.2) be paired with a target-scope axis before comparing with distributed-memory compilers?
- Is there a distributed analogue of the cache-miss measure in Table 2, such as remote-data traffic? The survey does not say.
