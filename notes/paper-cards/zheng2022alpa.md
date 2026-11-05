# Alpa: Automating Inter- and Intra-Operator Parallelism for Distributed Deep Learning

**Catalog id:** `zheng2022alpa`
**Citation:** Lianmin Zheng, Zhuohan Li, Hao Zhang, Yonghao Zhuang, Zhifeng Chen, Yanping Huang, Yida Wang, Yuanzhong Xu, Danyang Zhuo, Eric P. Xing, Joseph E. Gonzalez, Ion Stoica. "Alpa: Automating Inter- and Intra-Operator Parallelism for Distributed Deep Learning." OSDI 2022. arXiv:2201.12023.
**Paper type:** full-system
**Access:** open (arXiv) — full text read.
**Card status:** full-read

## Problem
Combining data, operator and pipeline parallelism at operator granularity is said to require scarce expertise and not to transfer across models or clusters; prior automatic systems cover one parallelism class or assume linear graphs (§1, §2.1). The joint plan space is combinatorial, so Alpa seeks a decomposition that makes each level tractable.

## Input abstraction
A JAX training-step function decorated with `@parallelize`, plus a cluster configuration; on first call Alpa traces it to Jaxpr/HLO and compiles (§3, Fig. 4, §8). No per-tensor sharding annotations are needed.

## Target
GPU clusters with a bandwidth hierarchy of fast intra-node and slower inter-node links (§1, §2.2). Testbed: 8 AWS p3.16xlarge nodes, 64 V100 16 GB GPUs, NVLink within nodes, 25 Gbps between (§8). The cluster is an N×M mesh; submeshes are restricted to (1, 2^k) or (n, M) shapes (§5.2).

## Data decomposition
On a 2D device mesh a tensor's layout is a sharding spec X0…Xn−1 with Xi ∈ {S, R}; partitioned axes carry mesh-axis superscripts (S0, S1, S01), so S0R is row-partitioned over axis 0 and replicated along axis 1 (§4.1, Table 1). Resharding costs are tabulated, e.g. RR→S0S1 is free local slicing and S0R→RS0 is an all-to-all (Table 2). Tensors crossing pipeline stages may change spec and mesh shape (§6).

## Computation mapping
Two levels. Intra-operator parallelism is SPMD on one mesh: each primitive HLO operator has an enumerated list of parallel algorithms from mapping loop indices to mesh axes (Table 3), covering data parallelism, ZeRO and Megatron-style operator parallelism (§4). Inter-operator parallelism slices the operator sequence into stages assigned to submeshes and pipelines them with synchronous 1F1B; forward and backward operators are colocated (§2.2, §5.1). Operators are pre-clustered into "layers" by a DP balancing FLOPs and minimizing data crossing boundaries (§5.2). Across meshes execution is MPMD: each mesh gets distinct static instruction lists (§6).

## Communication generation
Intra-op communication is the collective implied by each algorithm (all-reduce when a reduction loop is split) plus edge resharding, costed as bytes over mesh-axis bandwidth; compute cost is set to zero because algorithms divide work evenly (§4.2). After the ILP, all-reduce is rewritten to reduce-scatter + all-gather where possible, giving the ZeRO effect (§4.2). XLA and GSPMD insert collectives at stage compilation (§6). Cross-mesh resharding is treated as many-to-many multicast: send/recv between tiles, rewritten to one transfer plus a local all-gather when the destination spec contains replication (§6). Inter-stage cost is not modeled (§7).

## Compiler / runtime split
All decisions precede execution. The intra-op pass solves an ILP (off-the-shelf solver) over node and resharding costs with trivial operators merged (§4.2). The inter-op pass runs a DP over stage boundaries, submesh shapes and tmax with early pruning and ε-quantized tmax (§5.2). Each candidate stage-mesh pair is compiled and profiled for latency and memory against the 1F1B bound (Eq. 5) (§5.2); a piecewise-linear XLA-level cost model accelerates profiling (§8.4). The runtime uses Ray actors, the XLA runtime and NCCL; a driver pre-generates instructions (§6, §8). Compiling GPT-39B on 64 GPUs took 2393 s, mostly profiling and stage compilation (§8.4, Table 5).

## Evaluation
Weak scaling on GPT-3 (0.35–39B), GShard MoE (0.38–70B) and Wide-ResNet (0.25–13B) up to 64 GPUs, in cluster PFLOPS (§8.1, Table 4). Alpa matches or slightly exceeds grid-searched Megatron-LM v2 on GPT; on MoE it reports 3.5× over DeepSpeed on 2 nodes and 9.7× on 4; on Wide-ResNet it reaches 80% scaling on 32 GPUs where PP-DP and inter-op-only baselines run out of memory (§8.1). Ablations: the ILP beats ZeRO-2/3 and a GSPMD-propagation heuristic (§8.2); the DP beats equal-operator and equal-layer slicing by 2.6× and 1.6× on Wide-ResNet (§8.3); local all-gather gives 2.0× on cross-mesh resharding (§8.5).

## Principal limitation
The authors list: cross-stage communication cost unmodeled; microbatch count B is a hyperparameter; the pipeline schedule is static and linear; overlap is not optimized; only static graphs with known shapes (§7). Our observation: the submesh-shape restriction and equal-capability assumption tie the formulation to homogeneous cloud GPU nodes.

## Relationship to earlier / later work
- Intra-op compilation builds on XLA and GSPMD; SPMD style follows GShard/GSPMD (§4, §6).
- Inter-op DP builds on TeraPipe (§5.2); synchronous 1F1B taken from DAPPLE/PipeDream-style work (§2.2).
- Compares against Megatron-LM v2 and DeepSpeed; contrasts with Tofu (linear graphs) and FlexFlow (randomized search, no pipelining) (§4, §8.1, §9).
- Classes Mesh-TensorFlow, GSPMD and OneFlow as manual annotation APIs; names Pathways as concurrent work with a similar SPMD/MPMD split; cites Piper, TensorOpt and Varuna as related planners (§9).

## Sources used
| claim | section / page |
|---|---|
| Problem and motivation | §1, §2.1 |
| API and IR | §3, Fig. 4, §8 |
| Cluster model and testbed | §2.2, §5.2, §8 |
| Sharding specs and resharding | §4.1, Tables 1–3 |
| Hierarchical mapping, 1F1B, clustering, MPMD | §2.2, §4, §5, §6 |
| Cost model, post-ILP rewrite, cross-mesh resharding | §4.2, §6, §7 |
| ILP, DP, profiling, runtime, compile time | §4.2, §5.2, §6, §8.4 |
| Benchmarks and ablations | §8.1–§8.6 |
| Limitations | §7 |
| Related work | §2, §4, §5.2, §9 |

## Open questions for the survey
- How sensitive is the DP to the submesh-shape restriction on clusters whose per-node device counts are not powers of two?
- Can the ILP's zero-compute-cost assumption hold for operators where replicated computation is allowed?
- Does the SPMD-inside/MPMD-outside runtime split generalize to heterogeneous accelerators?
