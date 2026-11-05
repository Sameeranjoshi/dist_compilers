# Beyond Data and Model Parallelism for Deep Neural Networks

**Catalog id:** `jia2019flexflow`
**Citation:** Zhihao Jia, Matei Zaharia, Alex Aiken. "Beyond Data and Model Parallelism for Deep Neural Networks." Proceedings of the Conference on Systems and Machine Learning (SysML/MLSys), 2019. arXiv:1807.05358.
**Paper type:** full-system
**Access:** open (arXiv) — full text read.
**Card status:** full-read

## Problem
Data parallelism replicates the model and is inefficient for parameter-heavy operations; model parallelism avoids synchronization but forbids parallelism inside an operation; expert hybrids remain suboptimal; and prior automated frameworks explore either placement across operations (REINFORCE) or parallelism within operations on linear graphs (OptCNN), missing strategies using both (§1, §2). Evaluating candidates by running them on hardware is argued to be too expensive for a larger space (§1).

## Input abstraction
An operator graph G (nodes are operations, edges tensors) as in existing frameworks, plus a device topology D whose nodes are devices (CPU or GPU) and whose edges are connections labeled with bandwidth and latency (§3.1). The user supplies no parallelization annotations; FlexFlow searches for the strategy, presented as a programmability and portability benefit (§3.1).

## Target
Two GPU clusters: 4 nodes × 4 P100 with NVLink and 100 GB/s Infiniband, and 16 nodes × 4 K80 on PCIe switches with 56 GB/s Infiniband, up to 64 GPUs (§8.1, Fig. 6). The runtime is built on Legion with cuDNN and cuBLAS (§7).

## Data decomposition
The SOAP space names four parallelizable dimension classes: Sample, Operation, Attribute (e.g., image height/width, sequence length) and Parameter (e.g., channel) (§4, Table 1). A parallelization configuration c_i gives a positive degree per parallelizable dimension of o_i's output tensor with equal-size partitions; the product |c_i| is the task count, each task assigned a device (§4, Fig. 4). Input sub-tensors are inferred from the output partition, so partitioning is defined on outputs only; sample-only configurations recover data parallelism and parameter-dimension configurations recover model parallelism (§4, Fig. 3).

## Computation mapping
A strategy S chooses a configuration independently per operation; each device computes a disjoint subset of the operation's output tensor (owner computes) (§4). The operation dimension assigns different operations to different devices, so inter- and intra-operation parallelism coexist; for RNNs the best strategies mix layer-level concurrency with channel splitting inside operations (§4, §8.5). The runtime uses Legion's high-dimensional partitioning and fine-grain control to parallelize each operation independently (§7).

## Communication generation
Derived structurally in the simulator's task graph: for each producer/consumer task pair sharing a tensor on different devices, a communication task is placed on the connection "device" between them with time s/b (§5.1). Modeling connections as devices lets transfers overlap computation (§5.1), and the runtime overlaps them (§8.2.1). No collectives are named; communication is evaluated as total data transferred per iteration, with 2–5.5× reductions on NMT (§8.2.1, Fig. 8).

## Compiler / runtime split
Strategy selection is offline. An execution simulator builds the task graph and schedules it with a Dijkstra-style full algorithm or a Bellman-Ford-style delta algorithm that re-simulates only tasks affected by one configuration change (§5.2, §5.3). Task times are measured once per operation type and input size on the real device and cached, assuming predictable, data-independent execution (§5, A1). The optimizer runs Metropolis-Hastings MCMC, proposing a random configuration for a random operation, from data-parallel, expert or random starting points with a 30-minute budget (§6, §8.1). The best strategy is handed to the Legion runtime (§3.2, §7).

## Evaluation
Six DNNs: AlexNet, Inception-v3, ResNet-101, RNNTC, RNNLM, NMT (Table 3). Reported: 1.3–3.3× per-iteration speedups over data-parallel and expert strategies on the non-ResNet benchmarks (§8.2.1); 38% shorter end-to-end Inception-v3 training than TensorFlow on 16 P100s (§8.2.2); 3.4–3.8× over REINFORCE's published placements with search in 14–40 s instead of 12–27 hours; 1.2–1.6× over OptCNN on non-linear graphs (§8.2.3). Simulated and real times differ by under 30% with ordering preserved (§8.3.1); delta simulation is 2.2–6.9× faster (Table 4). For LeNet and a small RNNLM the search found the exhaustively verified optimum (§8.4).

## Principal limitation
The authors state the main limitation is the simulator's assumption that execution time is predictable and independent of input contents, excluding data-dependent workloads (§3.3). Our observation: the space partitions only output tensors into equal blocks and has no microbatched pipeline schedule, so stage-level pipelining lies outside SOAP as defined.

## Relationship to earlier / later work
- Extends OptCNN (Jia et al. 2018), which handled linear graphs via DP, and compares against it (§1, §2, §8.2.3).
- Compares against REINFORCE (Mirhoseini et al.) and cites its hierarchical placement follow-up (§1, §2, §8.2.3).
- Uses Krizhevsky's "one weird trick" and GNMT's placement as expert baselines (§2, §8.2.1).
- Built on the Legion runtime and dependent partitioning (§7); contrasts with Quincy/Firmament schedulers (§2).
- inferred: Mesh-TensorFlow (App. B), GSPMD (§6) and Alpa (§4, §9) later position themselves against this paper's owner-computes space and randomized search.

## Sources used
| claim | section / page |
|---|---|
| Problem | §1, §2 |
| Operator graph and device topology | §3.1 |
| Clusters, runtime libraries | §7, §8.1 |
| SOAP, configurations, output partitioning | §4, Table 1, Figs. 3–4 |
| Strategy, inter/intra-op mixing | §4, §7, §8.5 |
| Task graph communication model | §5.1, §8.2.1 |
| Simulator, MCMC, task profiling | §5, §6, §8.1 |
| Results | §8.2–§8.4, Tables 3–4 |
| Limitations | §3.3 |
| Related work | §1, §2, §7, §8.2.3 |

## Open questions for the survey
- How does simulator-driven randomized search compare in plan quality with Alpa's ILP/DP on the same model and space?
- Does the owner-computes restriction materially cost communication on contraction-heavy models, as Mesh-TensorFlow's appendix claims?
- Can delta simulation serve exact optimizers as an incremental cost oracle?
