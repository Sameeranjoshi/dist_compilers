# GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism

**Catalog id:** `huang2019gpipe`
**Citation:** Yanping Huang, Youlong Cheng, Ankur Bapna, Orhan Firat, Mia Xu Chen, Dehao Chen, HyoukJoong Lee, Jiquan Ngiam, Quoc V. Le, Yonghui Wu, Zhifeng Chen. "GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism" (v1 title, as in the catalog; v5 is titled "GPipe: Easy Scaling with Micro-Batch Pipeline Parallelism"). arXiv preprint, 2018; also NeurIPS 2019. arXiv:1811.06965.
**Paper type:** runtime (the paper calls itself a "pipeline parallelism library", Abstract, §2)
**Access:** open (arXiv) — full text of arXiv:1811.06965v5 (25 Jul 2019), printed title "GPipe: Easy Scaling with Micro-Batch Pipeline Parallelism", read; the supplementary material is referred to but not included.
**Card status:** full-read

## Problem
Model capacity beyond one accelerator's memory has required architecture-specific algorithms or infrastructure (Abstract, §1). Naive model parallelism over a layer sequence under-utilizes devices because of the sequential dependency (Figure 2b). The goal is task-independent model parallelism for "any network that can be expressed as a sequence of layers" with near-linear speedup (Abstract).

## Input abstraction
A model is a sequence of L layers, each with forward function f_i, parameters w_i and an optional cost estimate c_i; the user supplies the partition count K, the micro-batch count M and the layer definitions (§2.1). Implemented under the Lingvo framework; the design is said to be portable to other frameworks [17, 18, 19] (§2).

## Target
Cloud TPUv2 (8 GB per accelerator) and TPUv3 (16 GB per core) (§3); NVIDIA P100 GPUs on one host without NVLink, transferring via PCI-E (§3, Table 3). Table 1 heads the AmoebaNet rows "NVIDIA GPUs (8GB each)" while §3 says Cloud TPUv2; unresolved.

## Data decomposition
Consecutive layers i..j form a cell p_k holding parameters w_i..w_j; cell k lives on accelerator k (§2.1, §2.2). Cell boundaries are uneven: the partitioner balances estimated cost C_k = Σ c_l, not layer count (§2.1, §2.2). Each mini-batch of N examples is split into M equal micro-batches (§2.2). Only boundary activations are stored; re-materialization recomputes F_k in the backward pass, giving peak activation memory O(N + (L/K)(N/M)) versus O(N × L) (§2.3). Data parallelism may be added on top but is not described (§1).

## Computation mapping
Pipeline parallelism: micro-batches flow through the K cells; gradients of all M micro-batches are accumulated and applied once per mini-batch, so updates are "consistent regardless of the number of partitions" (§2.2, Figure 2c). The partitioner "minimizes the variance in the estimated costs of all cells" (§2.2); the authors call it a heuristic (§2.3). Bubble overhead is O((K−1)/(M+K−1)), negligible for M ≥ 4K, helped by scheduling recomputation early (§2.3). BatchNorm statistics are per micro-batch, with mini-batch moving averages for evaluation (§2.2, §6).

## Communication generation
"Communication primitives are automatically inserted at partition boundaries" between neighbouring partitions (§2.2). Only activation tensors cross boundaries, once per micro-batch, so GPipe is claimed usable without high-speed interconnects (§2.3, §6). No primitive is named.

## Compiler / runtime split
There is no compiler: GPipe is a library layered on Lingvo (§2). Partitioning is decided before execution from user-supplied K, M and cost estimates (§2.1, §2.2); backward functions come from automatic symbolic differentiation (§2.1). Our observation: the text gives neither the partitioning algorithm nor when it runs.

## Evaluation
Maximum model size: AmoebaNet 82M → 318M parameters on one accelerator via re-materialization, 1.8B on 8 (25×, sub-linear from imbalanced layers); Transformer 282M → 83.9B on 128 TPUv3 cores (298×, linear) (§3, Table 1). Throughput: Transformer 6.3× at K=8, M=32; AmoebaNet 3.48× (§3, Table 2). P100 without NVLink, M=32, K 2→8: 2.7× (AmoebaNet) and 3.3× (24-layer Transformer) (§3, Table 3). Applications: 557M-parameter AmoebaNet-B(18,512) on 4 partitions, 84.4% ImageNet top-1 (§4, Table 4); 6B-parameter 128-layer multilingual Transformer on 16 accelerators beats bilingual baselines (§5, Figure 3). No other model-parallel system is measured.

## Principal limitation
Stated: a single layer must fit one accelerator (§6, footnote 3); cross-batch statistics complicate micro-batching (§6); the heuristic partitioner can leave load imbalance (§2.3). Our observation: speedups are normalized (to K=2 or M=1), so absolute utilization is never reported.

## Relationship to earlier / later work
- Re-materialization taken from Griewank & Walther [13] and Chen et al. [14] (§1, §2.3).
- Built in Lingvo [16]; portable to [17–19] (§2).
- Contrasts with generic model parallelism/device placement [42–45], which suffer low utilization (§6).
- Contrasts with Mesh-TensorFlow [34] SPMD: AllReduce-heavy, needs fast interconnects, limited operator set (§6).
- Extends earlier pipelined training [46, 47]; contrasts with PipeDream [48] (asynchronous, weight staleness, versioned weights) and parameter servers [49] (§6).
- inferred: GSPMD (`xu2021gspmd`) and Alpa later subsume or automate this manual, sequence-of-layers pipelining.

## Sources used
| claim | section / pages |
|---|---|
| Problem, goals | Abstract, §1, Figure 2 |
| Interface (K, M, layers, cost c_i) | §2.1 |
| Partition, micro-batching, sync update, BatchNorm | §2.2, Figure 2c |
| Re-materialization, bubble, communication claim | §2.3 |
| Hardware and scale results | §3, Tables 1–3 |
| Applications | §4, §5, Tables 4–5, Figure 3 |
| Limitations, related work | §2.3, §6 |

## Open questions for the survey
- What is the actual partitioning algorithm, and is it run over a graph IR or over the Python layer list?
- Which transfer primitives are inserted at boundaries, and do they overlap compute?
- How should a compiler-less library be scored on the compiler-architecture axis against GSPMD/Alpa?

## Reference list check
Total reference entries: 49.

| line | in reference list? |
|---|---|
| High Performance Fortran (Loveman 1993 / HPF Forum) | absent |
| Fortran D (Hiranandani/Kennedy/Fox) | absent |
| Kali (Mehrotra/Koelbel/Van Rosendale) | absent |
| Koelbel 1991 "compiling programs for distributed memory" | absent |
| Saltz/PARTI/CHAOS (Saltz, Ponnusamy, Das) | absent |
| Vienna Fortran (Chapman/Zima) | absent |
| Mesh-TensorFlow (Shazeer 2018) | yes: [34] Shazeer et al., "Mesh-tensorflow: Deep learning for supercomputers", NeurIPS 2018 |
| Legion (Bauer 2012) | absent |
| Sequoia (Fatahalian 2006) | absent |
| Chapel | absent |
| Halide | absent |
| Co-Array Fortran (Numrich) | absent |
