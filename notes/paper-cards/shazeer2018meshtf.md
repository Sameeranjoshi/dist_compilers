# Mesh-TensorFlow: Deep Learning for Supercomputers

**Catalog id:** `shazeer2018meshtf`
**Citation:** Noam Shazeer, Youlong Cheng, Niki Parmar, Dustin Tran, Ashish Vaswani, Penporn Koanantakool, Peter Hawkins, HyoukJoong Lee, Mingsheng Hong, Cliff Young, Ryan Sepassi, Blake Hechtman. "Mesh-TensorFlow: Deep Learning for Supercomputers." NeurIPS (NIPS) 2018. arXiv:1811.02084.
**Paper type:** language
**Access:** open (arXiv) — full text read.
**Card status:** full-read

## Problem
Batch-splitting maps naturally onto SPMD programming, but the authors state it cannot train models whose parameters or activations exceed one device's memory, incurs synchronization latency, and is inefficient at small per-processor batches. Model-parallel alternatives are described as hard to discover and implement, with MIMD implementations producing large programs that are hard to compile (§1). The goal is a notation in which any tensor dimension, not only the batch, can be split while keeping one SPMD program.

## Input abstraction
A TensorFlow-like graph written in a Python library in which every tensor dimension has a name as well as a size, with statically known shapes (§7). The user declares a processor mesh with named dimensions and a global "computation layout": a partial map from tensor-dimension names to mesh-dimension names (§4). The same model code is reused under different layouts; §8 shows data-parallel, model-parallel and mixed 2D/3D layouts for two fully-connected layers written once with `mtf.einsum`. The library lowers to a TensorFlow graph (§7).

## Target
Clusters of identical, reliable processors with local memory. The mesh is a naming abstraction independent of physical topology, though the authors note grouped allreduce is efficient when each group is physically connected (§2). SPMD code is generated for TPUs, MIMD device-placement code for multi-CPU/GPU; experiments use TPUv2 meshes up to 512 cores (§7, §9).

## Data decomposition
One slice per processor. A tensor's layout is the restriction of the global layout to its dimensions and must be injective; a mapped dimension is striped by the processor's coordinate on that mesh dimension, and an empty layout means full replication (§5). Two dimensions of one tensor may not share a mesh dimension (§8.5). Mixed layouts tile tensors over two mesh dimensions and replicate over a third (§8.3). Dimension sizes must be evenly divisible by mesh-dimension sizes (§5).

## Computation mapping
Compilation yields an SPMD program: each operation becomes one local operation per processor producing its output slice from its input slices, plus collectives where required (§4, §6). Because layouts allow replication, the authors argue the scheme expresses iteration-space partitionings of matrix multiply (2D, 3D, 2.5D-style) beyond "owner computes" (§10, Appendix B). Layout choice is manual; §8.4 advises that every expensive einsum have an input dimension split across each mesh dimension.

## Communication generation
Derived per operation from layouts. Component-wise ops need none. Reductions and einsums do a local reduction then MPI-allreduce over the mesh dimensions of reduced-out tensor dimensions (§6). Reshape may require allgather (split in input only), local slicing (split in output only), or alltoall (different dimensions on the same mesh dimension), the latter used to switch between data and model parallelism across layers (§6.1). Table 1 (§8.6) is an analytic cost model per layout: computation, communication volume, their ratio, and memory per processor, with allreduce time proportional to slice size over per-link bandwidth.

## Compiler / runtime split
All decisions are made at graph construction from the user-supplied layout; no search, profiling or runtime adaptation. Automated layout search is future work (§11).

## Evaluation
A model-parallel Transformer splits vocab, d_ff and heads across processors, combined with batch splitting on a 2D mesh (§9). On TPUv2 meshes up to 16×32 = 512 cores, models with d_ff up to 262144 and 256 heads reached over 50% compute efficiency (6 of 11.5 PFLOP/s) (§9). A 4.9B-parameter model trained 13 hours on 512 cores reached 24.0 (23.5 rescaled) perplexity on the One Billion Word benchmark; a 2.9B model reached 43.9 BLEU on WMT14 En-Fr after 22 hours on 128 cores (§9.1, Tables 2–3). No comparison with another distributed system is reported.

## Principal limitation
The authors note the divisibility requirement (§5), manual layout choice (§11), missing halo communication for spatially partitioned convolutions and TPU-only SPMD generation (§11), and possibly higher memory than specialized algorithms (§10). Our observation: the evaluation shows feasibility and model quality but no head-to-head throughput comparison against another parallelization approach.

## Relationship to earlier / later work
- Generalizes SPMD synchronous data parallelism (§3).
- Feature-wise similar to the Cyclops Tensor Framework; expresses 3D, 2.5D, CARMA and 1.5D matrix-multiply mappings (§10).
- Contrasts with Jia et al. (FlexFlow/OptCNN), whose owner-computes dimensions are argued to be communication-suboptimal (§10, Appendix B).
- Cites Gholami et al. on integrated data/model parallelism as unimplemented (§10).
- Alltoall reshape motivated by layer-wise layout switching in the mixture-of-experts work [20] (§6.1).
- inferred: GSPMD (2021) and Alpa (2022) later cite Mesh-TensorFlow as a manual rewrite/annotation approach.

## Sources used
| claim | section / page |
|---|---|
| Problem statement | §1 |
| Named dimensions, mesh, computation layout | §4, §7, §8 |
| Hardware assumptions, TPU mesh shapes | §2, §7, §9 |
| Layout as injective partial map, replication, divisibility | §5, §8.3, §8.5 |
| SPMD per-op implementation, beyond owner-computes | §4, §6, §10, App. B |
| Allreduce/allgather/alltoall derivation, cost table | §6, §6.1, §8.6 (Table 1) |
| Manual layout, future automated search | §11 |
| Transformer layouts and results | §9, §9.1, Tables 2–3 |
| Limitations | §5, §10, §11 |

## Open questions for the survey
- How much of the later "mesh + per-dimension sharding" vocabulary (GSPMD, Alpa) directly inherits the computation-layout abstraction versus rediscovering HPC tensor-contraction practice?
- The mesh is topology-agnostic yet performance relies on physically connected allreduce groups; how should the survey classify topology awareness that lives only in the user's mesh choice?
- Is the absence of automated search a design position or a gap, given the analytic cost table already in §8.6?
