# Tiramisu: A Polyhedral Compiler for Expressing Fast and Portable Code

**Catalog id:** `baghdadi2019tiramisu`
**Citation:** Riyadh Baghdadi, Jessica Ray, Malek Ben Romdhane, Emanuele Del Sozzo, Abdurrahman Akkas, Yunming Zhang, Patricia Suriana, Shoaib Kamil, Saman Amarasinghe. "Tiramisu: A Polyhedral Compiler for Expressing Fast and Portable Code." CGO 2019. DOI 10.1109/cgo.2019.8661197; arXiv:1804.10694.
**Paper type:** full-system
**Access:** open — arXiv 1804.10694v5 (20 Dec 2018) full text read; CGO 2019 version not read, so references are to the arXiv text.
**Card status:** full-read

## Problem
Automatic polyhedral compilers fall short of hand-tuned libraries, and existing polyhedral scheduling languages (AlphaZ, CHiLL) cannot partition computations, send data across nodes or insert synchronization (§I, Fig. 1). Memory-based IRs fix layout before scheduling, so the data to copy or send is unknown until loops are transformed (§IV-A).

## Input abstraction
A C++-embedded DSL: a pure algorithm of computations over iteration domains, with no notion of data location, plus scheduling commands in four groups: loop transformations; hardware mapping (`parallelize`, `vectorize`, `gpu`, `distribute`); data manipulation (buffers, `store_in`, caches, copies); synchronization (`barrier_at`, `send`, `receive`) (§III-B, §III-C, Table II).

## Target
Multicore CPUs (LLVM IR), CUDA GPUs, distributed machines via MPI; FPGA in [14] (§I, §III, §V-A). Table I claims distributed GPU code generation, never evaluated. Testbed: 16 dual-socket 24-core Xeon E5-2680v3 nodes, Infiniband, MVAPICH2 2.0; one K40 GPU (§VI).

## Data decomposition
No distribution construct: Layer I has no data location, and the distributed examples assume the input is "already distributed across the nodes by rows" (§III-C, §VI-B.c). In the blur, node n holds rows n·(N−2)/Nodes to (n+1)·(N−2)/Nodes in local array `lin` and receives two border rows from node n+1 into the end of that chunk (§III-C, Fig. 3c). Layer III holds data layout as affine access relations from computations to buffer elements; it says nothing about which node owns a buffer (§IV-C.3).

## Computation mapping
Layer II orders computations lexicographically on time dimensions and tags space dimensions with a processor type (`cpu`, `node`, `gpuT`, `gpuB`), without specifying memory (§IV-C.2). `C.distribute(i)` tags loop level i so "each iteration [runs] on a different node"; the blur splits i by N/Ranks and distributes the outer loop of `bx`, `by` and of the send/receive operations (§III-C, Table II, Fig. 3c). Each distributed loop becomes an MPI-rank conditional (§V-A).

## Communication generation
Communication lives in Layer IV, generated from Layer III by user commands (§IV-C.4, §V.c). `send(d, src, s, q, p)` / `receive(d, dst, s, q, p)` take an iteration domain, buffer, size, peer node and properties (synchronous, asynchronous, blocking) and are schedulable like computations (`s.before(r, root)`, `r.distribute(ir)`) (§III-C, Table II). In the blur, node `is` sends M·2·3 elements from `lin(0,0,0)` to `is−1` `{ASYNC}`; node `ir` receives from `ir+1` `{SYNC}` (§III-C, Fig. 3c). They lower to MPI calls (§V.c, §V-A). The user chooses sync/async, granularity, buffer sizes and when to send (§II.a); automatic domain computation is stated for `allocate_at`, `copy_at`, `barrier_at`, not for `send`/`receive` (§III-C).

## Compiler / runtime split
All decisions are static, from the schedule; the only runtime element is the rank test (§V-A). Legality uses dependence analysis [18] (§II.c). Code generation uses ISL's Cloog implementation; CPU lowering passes through Halide IR used only as an LLVM library (§V-A).

## Evaluation
Single-node CPU DL/linear-algebra kernels vs. Intel MKL and reference code: sgemm matches MKL after tile/unroll autotuning; VGG 2.3× over MKL (§VI-A, Fig. 5). No DL benchmark runs distributed. Seven image kernels vs. Halide and PENCIL (CPU, GPU) and vs. distributed Halide [15] on 16 nodes (§VI-B, Fig. 6). Distributed: data pre-distributed by rows; three kernels need no communication, four exchange overlapping boundary regions; Tiramisu is 1.31–3.25× faster, attributed to distributed Halide over-estimating sends under clamped accesses and packing before sending; explicit `send`/`receive` is "the only difference" (§VI-B.c, Fig. 6). Fig. 7: strong scaling on 2–16 nodes relative to 2 nodes, no absolute times.

## Principal limitation
Distribution is manual: the user writes partitioning, sends, receives and ordering, contrasted with automation in [1], [7] (§II.a). No parametric tiling (Table I). Our observation: the distributed evaluation is seven image kernels on 16 nodes against one baseline; distributed GPU support has no experiment; whether send/receive domains are checked for correctness is not stated.

## Relationship to earlier / later work
- Amarasinghe & Lam [1] and Bondhugula [7] automate distributed code generation; Tiramisu relies on user commands instead (§II.a).
- Pluto [8], PENCIL [3][4], Polly [22], Tensor Comprehensions [46], PolyMage [34]: fully automatic, no asynchronous communication (§II.a).
- AlphaZ [51], CHiLL [10][24], URUK [19]: polyhedral scheduling languages without distributed targets (§II.b, Table I).
- Halide [39][40]: interval-based, no dependence analysis; distributed Halide [15] over-approximates communication (§II.c, §VI-B.c). Also TVM [11], POET [50], GraphIt [52], Delite [9], NOVA [12], Lift [42], [48] (§II.c–d).
- Builds on ISL [47], Cloog [5], Benabderrahmane et al. [6], overlapped tiling [28]; FPGA backend [14] (§I, §III-C, §V).

## Sources used
| claim | section / page |
|---|---|
| Problem, related work | §I, §II, Table I, §IV-A |
| Commands, blur schedules | §III-C, Table II, Fig. 3c |
| Four layers | §IV-C.1–4 |
| MPI lowering | §V.c, §V-A |
| Evaluation | §VI-A, §VI-B.c, Figs. 5–7 |

## Open questions for the survey
- Does the compiler verify that user-written send/receive domains match what a consumer needs?
- How does explicit send/receive compare in communication volume with distributed Pluto [7], cited but not measured?
- Was distributed GPU code generation (Table I) ever evaluated?

## Reference list check
Total reference entries: 52 ([1]–[52]).

| line | present? |
|---|---|
| High Performance Fortran (Loveman 1993 / HPF Forum) | absent |
| Fortran D (Hiranandani/Kennedy/Fox) | absent |
| Kali (Mehrotra/Koelbel/Van Rosendale) | absent |
| Koelbel 1991, compiling programs for distributed memory | absent |
| Saltz / PARTI / CHAOS (Saltz, Ponnusamy, Das) | absent |
| Vienna Fortran (Chapman/Zima) | absent |
| Pluto / distributed-memory Pluto (Bondhugula) | present: [8] Bondhugula, Hartono, Ramanujam, Sadayappan, "A practical automatic polyhedral parallelizer and locality optimizer," PLDI 2008; [7] U. Bondhugula, "Compiling affine loop nests for distributed-memory parallel architectures," SC 2013 |
| Halide | present: [39] Ragan-Kelley et al., "Decoupling algorithms from schedules...," ACM Trans. Graph. 2012; [40] Ragan-Kelley et al., "Halide: a language and compiler...," PLDI 2013; also [15] Denniston, Kamil, Amarasinghe, "Distributed Halide," PPoPP 2016 |
| Legion (Bauer 2012) | absent |
| Sequoia (Fatahalian 2006) | absent |
| Chapel | absent |
| Co-Array Fortran (Numrich) | absent |
| Mesh-TensorFlow (Shazeer 2018) | absent |

Closest older distributed-memory compiler entry: [1] Amarasinghe and Lam, "Communication optimization and code generation for distributed memory machines," SIGPLAN Not. 1993.
