# ZeRO: Memory Optimizations Toward Training Trillion Parameter Models

**Catalog id:** `rajbhandari2020zero`
**Citation:** Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, Yuxiong He. "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models." SC20, 2020. DOI 10.1109/sc41405.2020.00024; arXiv:1910.02054.
**Paper type:** runtime
**Access:** open — arXiv 1910.02054v3 (13 May 2020) full text read; the SC20 version (catalog primary record) not read, so section numbers are the arXiv ones.
**Card status:** full-read

## Problem
Data parallelism (DP) replicates all model states and runs out of memory above about 1.4B parameters on 32 GB GPUs; model parallelism (MP) partitions them but degrades beyond one node (§1). Memory = model states (optimizer states, gradients, parameters) + residual states (activations, buffers, fragmentation) (§1, §3). Mixed-precision Adam needs 16Ψ bytes for Ψ parameters: 2Ψ fp16 parameters, 2Ψ fp16 gradients, KΨ optimizer state, K = 12 (§3.1).

## Input abstraction
An unmodified PyTorch `torch.nn.module`, wrapped by the ZeRO interface and used like classic DP; combinable with any MP (§10.1). No annotations, language or IR is described.

## Target
400 NVIDIA V100 GPUs in 25 DGX-2 nodes, 800 Gbps internode (§10.1); NVSwitch 300 GB/s per link in-node versus 12.5 GB/s InfiniBand EDR across nodes (§10.2).

## Data decomposition
ZeRO-DP partitions the model states across the N_d data-parallel processes instead of replicating them, in three cumulative stages (§5, Fig. 1):
- P_os: optimizer states in N_d equal partitions; process i stores and updates only partition i; 4Ψ + KΨ/N_d, about 4x (§5.1).
- P_g: gradients kept only on the updating process, released after reduction; 2Ψ + 14Ψ/N_d, about 8x (§5.2).
- P_p: each process stores only its parameter partition; 16Ψ/N_d (§5.3). Table 1 tabulates 7.5B, 128B and 1T models.
ZeRO-R partitions activation checkpoints across the MP processes (P_a), optionally offloaded to CPU (P_a+cpu), uses constant-size buffers (C_B) and defragments into pre-allocated contiguous memory (M_D) (§6.1–§6.3). With MP the theoretical reduction is N_d × N_m (§1).

## Computation mapping
Data parallelism: every process runs the full forward and backward pass on its mini-batch slice (§2.1); partitioning changes ownership of state and of the update step, not of computation (§5.1). Any MP is Megatron-LM's, outside ZeRO (§10.1).

## Communication generation
Baseline DP all-reduce = reduce-scatter + all-gather, 2Ψ per step (§7.1). P_os+g: reduce-scatter of gradients (Ψ) + all-gather of updated parameters (Ψ) = 2Ψ, same as DP (§7.2.1). P_os+g+p: the owner broadcasts each parameter partition just before it is needed in forward and again in backward; receivers discard it after use; 3Ψ, 1.5x DP (§5.3, §7.2.2). Gradient reduction is bucketized per partition to overlap communication and computation (§5.2). P_a adds one all-gather per transformer block, under 10% of Megatron-LM's MP volume; P_a+cpu doubles CPU data movement over P_a (§8). All are library collectives issued by the runtime.

## Compiler / runtime split
No compiler. The runtime library fixes the partition from the DP degree N_d (§5.1) and runs a "dynamic communication schedule" (§4.1). P_a and P_a+cpu are enabled from the §8 volume analysis "given model and hardware characteristics" (§8); P_a+cpu "is turned on only when it is beneficial" (§10.5). Our observation: no decision algorithm is given.

## Evaluation
ZeRO-100B implements P_os+g plus ZeRO-R; P_p is not implemented (§1, §10). GPT-2-like transformers (Tables 4–10). With Megatron-LM MP: 170B parameters on 400 GPUs, 15 PFLOPS sustained for 8B–100B, up to 10x over Megatron-LM alone (§10.2, Fig. 2). Super-linear scaling of a 60B model from 64 to 400 GPUs, attributed to larger per-GPU batch as N_d grows (§10.3, Fig. 3). 13B parameters with DP only on 128 GPUs versus 1.4B for PyTorch DDP (§10.4, Fig. 4). Ablation C1–C5 (Table 3, Figs. 6–8, §10.5). Measured maxima with P_os match the analytic bound (Table 2). Turing-NLG 17B (§10.6). Comparison is per-GPU throughput; baselines used 256–384 GPUs (pp. 23–24).

## Principal limitation
P_p, the stage behind the linear reduction and the 1T claim, is analysed (§5.3, §7.2.2, Table 1) but not implemented or measured (§1, §10); a 1T model would take over a year to train (§9). Activation memory still needs MP (§6.1). Our observation: the 1.5x figure rests on the bandwidth-bound assumption of §7.1 and ignores per-layer broadcast latency.

## Relationship to earlier / later work
- Megatron-LM [3], Mesh-TensorFlow [5]: MP systems contrasted and combined with (§1, §2.1, §10.1).
- GPipe [10], PipeDream [11, 12]: PP alternatives with batch-size or staleness costs ZeRO avoids (§2.1).
- Checkpointing [7, 14], Gist [13], SuperNeurons [15]: complementary (§2.2.1).
- CPU offload [16, 17]: ZeRO keeps model states off CPU (§2.2.2).
- Adafactor [18], Anil et al. [19]: orthogonal (§2.2.3).
- NVIDIA AMP/Apex [25]: bucketing model (§5.2, §6.2). Released in DeepSpeed; P_p planned (§1).
- inferred: GSPMD (xu2021gspmd, its §6) treats ZeRO as a special case of its sharding.

## Sources used
| claim | section / pages |
|---|---|
| Memory accounting | §1, §3.1 |
| Three stages, memory formulas | §5.1–§5.4, Fig. 1, Table 1 |
| ZeRO-R | §4.2, §6.1–§6.3 |
| Volumes 2Ψ / 2Ψ / 3Ψ, P_a | §7.1–§7.2, §8 |
| Interface, hardware, baselines | §10.1 |
| Results | §10.2–§10.6, Figs. 2–8, Tables 2–10 |
| Related work | §2 |
| Limitations | §1, §9, §10 |

## Open questions for the survey
- Is ZeRO-DP's partition (of state ownership, not computation) a data decomposition in the taxonomy's sense, or a memory policy on top of data parallelism?
- Which later compilers reproduce P_os/P_g/P_p at compile time with the same 2Ψ/3Ψ volumes?

## Reference list check
Total reference entries: 26.

| line | present? | entry |
|---|---|---|
| High Performance Fortran (Loveman 1993 / HPF Forum) | absent | — |
| Fortran D (Hiranandani/Kennedy/Fox) | absent | — |
| Kali (Mehrotra/Koelbel/Van Rosendale) | absent | — |
| Koelbel 1991, compiling programs for distributed memory | absent | — |
| Saltz / PARTI / CHAOS (Saltz, Ponnusamy, Das) | absent | — |
| Vienna Fortran (Chapman/Zima) | absent | — |
| Mesh-TensorFlow (Shazeer 2018) | yes | [5] Noam Shazeer et al. "Mesh-tensorflow: Deep learning for supercomputers." CoRR abs/1811.02084, 2018. |
| GPipe (Huang) | yes | [10] Yanping Huang et al. "Gpipe: Efficient training of giant neural networks using pipeline parallelism." arXiv abs/1811.06965, 2018. |
| Megatron-LM (Shoeybi 2019) | yes | [3] Mohammad Shoeybi et al. "Megatron-lm: Training multi-billion parameter language models using model parallelism," 2019. |
| PipeDream | yes | [11] Aaron Harlap et al. "Pipedream: Fast and efficient pipeline parallel DNN training." CoRR abs/1806.03377, 2018; [12] Deepak Narayanan et al. "Pipedream: Generalized pipeline parallelism for dnn training." SOSP 2019. |
| Legion (Bauer 2012) | absent | — |
| Sequoia (Fatahalian 2006) | absent | — |
| Chapel | absent | — |
| Halide | absent | — |
| Co-Array Fortran (Numrich) | absent | — |
