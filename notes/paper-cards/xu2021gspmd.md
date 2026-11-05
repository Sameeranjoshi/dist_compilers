# GSPMD: General and Scalable Parallelization for ML Computation Graphs

**Catalog id:** `xu2021gspmd`
**Citation:** Yuanzhong Xu, HyoukJoong Lee, Dehao Chen, Blake Hechtman, Yanping Huang, Rahul Joshi, Maxim Krikun, Dmitry Lepikhin, Andy Ly, Marcello Maggioni, Ruoming Pang, Noam Shazeer, Shibo Wang, Tao Wang, Yonghui Wu, Zhifeng Chen. "GSPMD: General and Scalable Parallelization for ML Computation Graphs." arXiv preprint, 2021. arXiv:2105.04663.
**Paper type:** compiler-technique
**Access:** open (arXiv) — full text read.
**Card status:** full-read

## Problem
Model scaling needs parallelism over data and parameters, and the authors want one mechanism covering data, in-layer model, image-spatial, weight-update/optimizer-state and (via a wrapper) pipeline parallelism, including nested combinations in one layer (§1, §2.1). Production constraints drive the design: one program per partition would compile too slowly at thousands of partitions; accelerators need static shapes although dimensions are not always evenly divisible; and the full XLA operator set, including Convolution, must be handled (§1).

## Input abstraction
A single-device program (TensorFlow, JAX or other XLA frontends) with a few tensors annotated via `mesh_split(tensor, device_mesh, dims_mapping)`, mapping each tensor dimension to at most one mesh dimension or −1 (§3.1). In TensorFlow this is the identity-like `XlaSharding` op whose gradient copies the annotation backward (§3.6). A manual-partitioning mode exists for subgraphs (§3.4). Pipelining is expressed by vectorizing a stage body with `vmap`/`vectorized_map` over a leading stage dimension L and sharding L (§3.3). The dense Transformer study annotates 7 tensors per layer, about 0.7% of the graph (§5.1).

## Target
XLA backends for CPUs, GPUs and Cloud TPUs (§1). Measurements use Cloud TPUv3 (16 GB per core, homogeneous links forming a 2D mesh) up to 2048 cores; the GPU backend is enabled and verified but not measured at scale (§5, footnote 1).

## Data decomposition
Each tensor carries a sharding property: replicated; tiled, a device-ID tensor of the same rank as the data with no duplication; or partially tiled, where equal device subgroups replicate internally and tile across subgroups, encoded by a trailing replication dimension (§3.1). Mesh device order is preserved in collectives so users can match the network topology (§3.1). Uneven partitions work under static shapes by rounding shards up and masking padding with `Iota`/`PartitionId`/`Select` and dynamic offsets (§4.1, Appendix A.1).

## Computation mapping
GSPMD emits a single SPMD program (§4) through two HLO passes: sharding completion and per-operator partitioning (§3). Completion propagates shardings along preserved dimensions, merges compatible shardings from different operands (equal per-device shard offsets), and iterates forward and backward with priorities (elementwise highest, Dot lower, Broadcast favored backward) to a fixed point (§3.5). Nested patterns are handled by recursive pattern matching: a device-context object plus partition grouping rewrites logical partition IDs into device subgroups, so one rule set covers, e.g., batch and feature sharding in a single Einsum or Convolution (§4.4). Pipelining becomes sharding of L with a shifting buffer; non-contiguous layer assignment yields a circular schedule (§3.3).

## Communication generation
XLA's MPI-style collectives: CollectivePermute, AllGather, AllReduce, AllToAll and ReduceScatter, the last described as half the cost of AllReduce (§4.2). Halo exchange for windowed operators and for data-formatting ops (Slice, Pad, Reverse, uneven Reshape) uses CollectivePermute with the maximum halo then DynamicSlice trimming (§4.3, A.2). Resharding, inserted whenever annotations do not match a supported pattern, composes AllGather, AllToAll, CollectivePermute and DynamicSlice, possibly in several steps (§4.5). An `SPMD_Rotate` pattern and Pad/Slice merging reduce exchanges; fusion and code motion hide formatting overhead (§4.6). There is no cost model; choices follow fixed priorities.

## Compiler / runtime split
Everything is decided at compile time in XLA; shapes are static and per-partition variation is expressed through partition-ID-based dynamic offsets (§4.1). No search: the authors say propagation "may not always be optimal" and position GSPMD as a mechanism that could define the search space for an automatic policy (§3.5, §6).

## Evaluation
Dense Transformers of 64B–1T parameters on 128–2048 TPUv3 cores reached 54–62% FLOPS utilization (47.5% at 512B); doubling devices roughly doubled batch at similar step time (§5.1, Table 2). Pipelining a 16B model on an (L,X,Y) mesh gave 46–58% raw utilization, yet the best configuration was 24% slower than pure 2D sharding (§5.2, Table 4). Conformer pipelining showed the circular schedule cutting bubbles from about 30% to about 10% at small batch (§5.3, Table 5). Sparse MoE models of 10B–577B parameters on 32–2048 cores kept step time between 0.98 s and 1.51 s with AllToAll at 2–11% (§5.4, Table 6); hybrid MoE up to 804B held near-constant step time (§5.5, Table 7). Spatially partitioned 3D U-Net gained 15.7× on 16 partitions (§5.6, Table 8). No external system baseline is compared.

## Principal limitation
The authors state that sharding completion is deliberately simple and may be suboptimal, requiring extra annotations (§3.5); GSPMD pipelining supports only homogeneous stages (§3.3); GPU results are absent (§5). Our observation: with no cost model guiding annotation or propagation, reported efficiency depends on expert-chosen initial shardings, as the three attempts in Table 1 illustrate.

## Relationship to earlier / later work
- Generalized from the GShard backend, adding partial tiling, manual subgroups, priority propagation, recursive partitioning and pipelining (§1, §6).
- Contrasts with Mesh TensorFlow, which rewrites the model in a Python library rather than annotating the compiler graph (§6).
- Contrasts with Tofu's limited strategies; treats ZeRO and weight-update sharding as special cases (§6).
- Complementary to FlexFlow's automated search (§6); circular pipelining likened to the interleaved schedule of Narayanan et al. (§3.3).
- Reported as used in LaMDA, GShard-M4, MetNet-2 and BigSSL (§1, §5.3, §5.6).
- inferred: Alpa (2022) uses GSPMD/XLA to compile each pipeline stage.

## Sources used
| claim | section / page |
|---|---|
| Problem, production constraints | §1, §2.1 |
| mesh_split, XlaSharding, manual mode, pipeline wrapper | §3.1, §3.3, §3.4, §3.6 |
| Targets and TPUv3 testbed | §1, §5 |
| Three sharding types, uneven partitions | §3.1, §4.1, App. A.1 |
| Sharding completion, recursive partitioning | §3.5, §4.4 |
| Collectives, halo exchange, resharding, optimizations | §4.2–§4.6, App. A.2 |
| Compile-time only, no search | §3.5, §4, §6 |
| Benchmarks | §5.1–§5.6, Tables 2–8 |
| Limitations | §3.3, §3.5, §5 |
| Related work | §1, §6 |

## Open questions for the survey
- How does priority-based sharding propagation compare, in outcomes, with cost-driven assignment on the same graphs?
- Is reducing pipelining to a sharded stage dimension a general technique or an artifact of homogeneous Transformer stacks?
- What does static-shape padding for uneven partitions cost at scale, which the paper does not quantify?
