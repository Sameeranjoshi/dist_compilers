# Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism

**Catalog id:** `shoeybi2019megatron`
**Citation:** Mohammad Shoeybi, Mostofa Patwary, Raul Puri, Patrick LeGresley, Jared Casper, Bryan Catanzaro. "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism." arXiv preprint, 2019. arXiv:1909.08053.
**Paper type:** runtime (per catalog; a PyTorch training library, no compiler, §1, §3)
**Access:** open (arXiv) — full text of arXiv v4 (13 Mar 2020) read, including Appendices A–E.
**Card status:** full-read

## Problem
Transformer models exceed accelerator memory and ADAM adds optimizer state (§1). GPipe and Mesh-TensorFlow "require rewriting the model, and rely on custom compilers and frameworks that are still under development" (§1); data parallelism still needs the whole model on one worker (§2.3). Goal: intra-layer model parallelism "with no custom C++ code or compiler required" (§1).

## Input abstraction
An existing PyTorch transformer with "a few targeted modifications" (§1, §2.3): the programmer inserts two conjugate `torch.autograd.Function` operators, f (identity forward, all-reduce backward) and g (all-reduce forward, identity backward), Code 1 (§3, Fig. 3). No annotations; the split is fixed in source for MLP, self-attention and embedding (§3).

## Target
Up to 32 NVIDIA DGX-2H servers, 512 V100 32GB GPUs; NVSwitch within a server, InfiniBand between (§5). Model-parallel groups sit within one server, data-parallel groups span servers (App. B.1, Fig. 8); communication is PyTorch calls to NCCL (App. B.1).

## Data decomposition
Weights are split by hand along one dimension: the first MLP GEMM column-wise (A = [A1, A2]) so GeLU applies locally, the second row-wise so no communication precedes it (§3, eqs. 2–3, Fig. 3a); K, Q, V column-wise per attention head, the output linear layer row-wise (§3, Fig. 3b); the shared embedding along the vocabulary dimension, padded to a multiple of 1024 (§3, §5.1). Layer-norm parameters are duplicated on every GPU; each worker optimizes only its own parameters, so no updates are communicated (§3). Parameters are replicated across data-parallel groups (App. B.1).

## Computation mapping
Tensor parallelism within groups of up to 8 GPUs times up to 64-way data parallelism (§5.1, App. B.1). Dropout, layer norm and residuals are recomputed on every GPU rather than broadcast (§3); dropout inside model-parallel regions uses a per-worker seed, outside a shared one (App. B.2). Pipelining is called orthogonal but not implemented (§1, §3).

## Communication generation
Programmer-written: two all-reduces forward and two backward per layer through f/g (§3, Fig. 4), one after the input embedding (§3). Parallel logits are fused with the cross-entropy loss so b × s losses replace an all-gather of b × s × v logits (§3). Data-parallel gradient all-reduces run in parallel per group (App. B.1). No overlap or scheduling is described.

## Compiler / runtime split
No compiler, no partitioner: "It does not require a compiler" (§3); "does not require a new compiler or library changes" (Abstract). The authors choose every split, the f/g positions and what to replicate from transformer structure and encode it in the model source (§3); PyTorch autograd runs the inserted collectives over NCCL (App. B.1). Our observation: the hand-derived instance of the scheme sharding compilers later automate.

## Evaluation
Weak scaling over GPT-2 configurations of 1.2B–8.3B parameters (Table 1) against a 1.2B single-GPU baseline sustaining 39 TFLOPs, 30% of peak (§5.1.1): 8-way model parallel reaches 77% of linear; 8-way model plus 64-way data on 512 GPUs reaches 74% and 15.1 PFLOPs (§5.1.1, Fig. 5). Strong scaling of the 1.2B model at batch 8 gives 1.64×, 2.34×, 2.98× on 2, 4, 8 GPUs, "diminishing returns" (App. D.2, Table 8). More attention heads cut efficiency, 82% to 77% (App. D.1, Table 7). The rest is accuracy on WikiText103, LAMBADA, RACE and the BERT layer-norm reordering (§5.2–§5.3, Tables 3–5, Fig. 7). No other parallel training system is compared.

## Principal limitation
Stated: models above about 16B parameters exceed one DGX-2H's 16 GPUs and need hybrid intra-/inter-layer and inter-node model parallelism (§6); strong scaling diminishes beyond 2 GPUs (App. D.2). Our observation: the decomposition is transformer-specific and must be re-derived by hand for other operators; no cost argument beyond the removed synchronization point is given.

## Relationship to earlier / later work
- GPipe (Huang et al. 2018): needs rewriting and a custom compiler (§1), has pipeline bubbles (§2.3); Megatron is "orthogonal and complementary" (§3).
- Mesh-TensorFlow (Shazeer et al. 2018): compiled "with proper collective primitives"; Megatron uses "similar insights" without a compiler (§1, §2.3).
- FlexFlow (Jia et al. 2018) picks the best strategy (§2.3).
- PipeDream (Harlap et al. 2018), Chen et al. 2018: parameter-server pipelining, inconsistency issues (§2.3).
- Activation checkpointing (Chen et al. 2016) used per layer (§4.2); data parallelism attributed to Valiant 1990, ALBERT parameter sharing as the alternative (§2.3).
- Turing-NLG 17B was trained using Megatron (§5.2).
- inferred: the hand-written tensor-parallel baseline that automatic partitioners (GSPMD, Alpa) compare against.

## Sources used
| claim | section / pages |
|---|---|
| Motivation, related systems | Abstract, §1, §2.3 |
| f/g operators, splits, replication | §3, Figs. 3–4, Code 1 |
| Hardware, NCCL, grouping, RNG | §5, App. B |
| Scaling and accuracy | §5.1–§5.3, Tables 1–8, App. D |
| Limits | §6, App. D.2 |

## Open questions for the survey
- Do sharding-propagation compilers rediscover the column/row split, and at what annotation cost?
- Is the fused logits/loss trick (§3) expressible in annotation-based systems?
- No communication model is given; what share of step time are the four all-reduces at 8-way?

## Reference list check
Total reference entries: 51 (author–year style, unnumbered).

| line | present? | entry |
|---|---|---|
| High Performance Fortran (Loveman 1993 / HPF Forum) | absent | — |
| Fortran D (Hiranandani / Kennedy / Fox) | absent | — |
| Kali (Mehrotra / Koelbel / Van Rosendale) | absent | — |
| Koelbel 1991, compiling programs for distributed memory | absent | — |
| Saltz / PARTI / CHAOS (Saltz, Ponnusamy, Das) | absent | — |
| Vienna Fortran (Chapman / Zima) | absent | — |
| Mesh-TensorFlow (Shazeer 2018) | yes | Shazeer, N., Cheng, Y., Parmar, N., Tran, D., Vaswani, A., Koanantakool, P., Hawkins, P., Lee, H., Hong, M., Young, C., Sepassi, R., and Hechtman, B. "Mesh-TensorFlow: Deep learning for supercomputers." NeurIPS, 2018. |
| GPipe (Huang 2018/2019) | yes | Huang, Y., Cheng, Y., Chen, D., Lee, H., Ngiam, J., Le, Q. V., and Chen, Z. "GPipe: Efficient training of giant neural networks using pipeline parallelism." CoRR abs/1811.06965, 2018. |
| PipeDream (Narayanan / Harlap) | yes | Harlap, A., Narayanan, D., Phanishayee, A., Seshadri, V., Devanur, N., Ganger, G., and Gibbons, P. "PipeDream: Fast and efficient pipeline parallel DNN training." arXiv:1806.03377, 2018. |
| Legion (Bauer 2012) | absent | — |
| Sequoia (Fatahalian 2006) | absent | — |
| Chapel | absent | — |
| Halide | absent | — |
| Co-Array Fortran (Numrich) | absent | — |

Also present and relevant to the survey: Jia, Zaharia, Aiken, "Beyond data and model parallelism for deep neural networks" (FlexFlow), arXiv:1807.05358, 2018; Valiant, "A bridging model for parallel computation," CACM 33(8), 1990. No pre-2010 distributed-memory compiler work is cited.
