# PipeDream: Generalized Pipeline Parallelism for DNN Training

**Catalog id:** `narayanan2019pipedream`
**Citation:** Deepak Narayanan, Aaron Harlap, Amar Phanishayee, Vivek Seshadri, Nikhil R. Devanur, Gregory R. Ganger, Phillip B. Gibbons, Matei Zaharia. "PipeDream: Generalized Pipeline Parallelism for DNN Training." SOSP '19 (ACM Symposium on Operating Systems Principles), 2019. DOI 10.1145/3341301.3359646.
**Paper type:** full-system
**Access:** PDF supplied by the repository owner — full text read.
**Card status:** full-read

## Problem
Data parallelism loses efficiency as workers grow: Fig. 1 reports communication stalls of up to 90% of training time at 32 GPUs from cross-server `all_reduce` (Sec. 1, 2.1). Model parallelism underutilizes workers and leaves partitioning to the programmer; GPipe-style pipelining flushes often (Sec. 2.1-2.2); hardware diversity makes manual choice hard (Sec. 2.3). PipeDream adds inter-batch pipelining to intra-batch parallelism and, the compiler-adjacent part, partitions layers into stages from a profile.

## Input abstraction
A DNN as an operator graph grouped into layers, given as a PyTorch model (Sec. 2, 4). The profiler records per layer l the forward-plus-backward time T_l, activation size a_l and parameter size w_l (Sec. 3.1). The machine is a hierarchy of levels, level k holding m_k components of level k-1 linked at bandwidth B_k (Sec. 3.1, Fig. 7). The optimizer returns an operator graph annotated with a stage ID per layer (Sec. 4).

## Target
Multi-GPU cloud servers with commodity interconnects (Sec. 2.1). Table 2: Cluster-A (Azure, 4x V100, PCIe, 10 Gbps), Cluster-B (AWS p3.16xlarge, 8x V100, NVLink, 25 Gbps), Cluster-C (one Titan X per server, 40 Gbps); up to 16 GPUs per run (Sec. 5.1).

## Data decomposition
Model state is partitioned by stage: each worker keeps its layers' parameters in GPU memory and, with weight stashing, one version per in-flight minibatch (Sec. 3.3, 4). A replicated stage holds a full copy per replica, synchronized via PyTorch DistributedDataParallel (Sec. 4); inputs are split across replicas round-robin by minibatch ID (Sec. 3.2). Peak per-worker memory is argued to match data parallelism (Sec. 3.3, Fig. 16).

## Computation mapping
Layers form stages of consecutive layers, each on one GPU and optionally replicated; vanilla data parallelism is one replicated stage (Sec. 1, 3). The partitioner is a dynamic program over topology levels, solved bottom-up (Sec. 3.1): A^k(i->j, m) is the slowest-stage time of the best pipeline over layers i..j with m level-k workers; a replicated stage costs max(compute via level k-1, 2(m-1)/m * sum|w_l| / B_k); the recurrence minimizes over split s and replica count m' the max of A^k(i->s, m-m'), 2 a_s / B_k and the last stage's cost. Complexity is O(N^3 m_k^2) per level; runs took under 8 s (Sec. 3.1, 5.5). Outputs: stage boundaries, replication factors and NOAM = ceil(workers / input-stage replicas) in-flight minibatches, run under the static 1F1B-RR schedule (Sec. 3.2).

## Communication generation
Between stages, activations and gradients go point-to-point to one neighbour, asynchronously, overlapping the next minibatch's compute (Sec. 1, 3, Fig. 5). Replicated stages use `all_reduce` via DistributedDataParallel with wait-free backpropagation (Sec. 4). The cost model divides bytes by link bandwidth, charging (m-1)/m * |w_l| per worker for data-parallel layers, with topology entering through B_k (Sec. 3.1). Gloo carries pipeline traffic and NCCL the data-parallel baselines, as the two cannot be mixed in one stage (Sec. 4).

## Compiler / runtime split
Profile-guided, otherwise static. A profiling run of 1000 minibatches on one GPU feeds the optimizer; a BFS pass generates one `torch.nn.Module` per stage preserving dependences; the runtime (about 3000 lines of Python on PyTorch) assigns stages to workers and runs 1F1B-RR without distributed coordination (Sec. 3.1, 3.2, 4, Fig. 6). The optimizer relies on the stated low variance of per-input compute time (Sec. 3.1).

## Evaluation
Seven models (VGG-16, ResNet-50, AlexNet, GNMT-8, GNMT-16, AWD LM, S2VT) on ImageNet, WMT16 En-De, PTB and MSVD, measured as time to target accuracy against data parallelism with identical learning-rate schedules (Sec. 5.1, Table 1). Speedups: VGG-16 5.28x (4x4 on A, config 15-1) and 2.46x (2x8 on B); GNMT-16 up to 3.14x; GNMT-8 up to 2.95x; AWD LM 4.25x with 88% less communication; S2VT 3.01x; ResNet-50 1x because the optimizer picks data parallelism (Sec. 5.2, Fig. 17). Versus model parallelism 14.9x (VGG-16) and 6.5x (AlexNet); hybrid parallelism gains up to 80%, FlexFlow is beaten 1.9x (Sec. 5.3); the authors' GPipe with PipeDream's partitions is 55%/71% slower (Sec. 5.4). Predicted and measured throughput correlate strongly (Sec. 5.5, Fig. 15).

## Principal limitation
Stated: stages must be consecutive layers (footnote 2); the optimizer assumes uniform bandwidth per topology level and low per-input compute variance (Sec. 3.1); weight stashing is inconsistent across stages and vertical sync is off by default (Sec. 3.3); the optimizer balances compute and communication, not memory (Sec. 5.5). Our observation: the recurrence indexes layers as a linear range, so branching graphs must be linearized first, which the paper does not discuss.

## Relationship to earlier / later work
- GPipe [28] is concurrent with the PipeDream preprint [25]; it assumes a partitioned model and uses microbatches with recomputation (Sec. 2.2, 5.4).
- Earlier pipelined backpropagation: Chen et al. [15], Huo et al. [29] (Sec. 2.2).
- Hybrid intra-batch work without pipelining: OWT [36], FlexFlow [33, 34] (Sec. 2.1, 5.3); RL device placement [42] is called time- and resource-intensive (Sec. 2.1).
- Compared or cited data-parallel techniques: wait-free backpropagation [57], ASP, gradient quantization [45, 46], LARS [24, 31, 56] (Sec. 2.1, 5.2); bounded staleness [19, 43] motivates weight stashing (Sec. 1, 3.3).

## Sources used
| claim | section / page |
|---|---|
| Communication overhead of DP, motivation | Sec. 1, 2.1, Fig. 1 |
| Model/hybrid/inter-batch background | Sec. 2.1, 2.2, 2.3 |
| Pipeline stages, benefits | Sec. 3, Fig. 5 |
| Profiler quantities, cost model | Sec. 3.1 |
| Partitioning DP, topology levels, complexity | Sec. 3.1, Fig. 7 |
| NOAM, 1F1B, 1F1B-RR | Sec. 3.2, Figs. 4, 8 |
| Weight stashing, vertical sync, memory | Sec. 3.3, Fig. 9 |
| Implementation, codegen, Gloo/NCCL | Sec. 4, Fig. 6 |
| Clusters, models, TTA results | Sec. 5.1, 5.2, Tables 1-2 |
| Model/hybrid/GPipe comparisons | Sec. 5.3, 5.4, Fig. 14 |
| Optimizer accuracy, memory, communication, depth | Sec. 5.5, Figs. 15-18 |

## Open questions for the survey
- The partitioner is a profile-driven DP over a linear layer chain with a bytes/bandwidth model; where does it sit relative to graph-based searches (FlexFlow, Alpa) in the survey's cost-model and search-space taxonomy?
- Point-to-point activation transfers plus per-stage all_reduce form a fixed communication shape; should pipeline parallelism be classed under communication generation or computation mapping?
- Weight stashing changes training semantics; should the survey track semantics-preserving versus semantics-changing partitioners as a separate axis?
