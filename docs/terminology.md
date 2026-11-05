# Terminology

Working definitions used throughout the repository and the paper.  Where a
term has a canonical source, it is named; otherwise the definition is ours.

| term | definition | origin / note |
|------|------------|---------------|
| **place** | A computational locus with its own memory (node, process, GPU, PE, core on a wafer). | X10 uses *place*; Chapel uses *locale*; we use *place* generically. |
| **distribution** | A map from array (or tensor) elements to places. | HPF `DISTRIBUTE`. |
| **alignment** | A map from elements of one array to elements of another (or a template) so that aligned elements land on the same place. | HPF `ALIGN`; Li & Chen 1991 data alignment. |
| **template / decomposition** | An abstract index space to which arrays are aligned and which is then distributed. | Fortran D `DECOMPOSITION`; HPF `TEMPLATE`. |
| **processor arrangement / grid** | The logical array of places over which a distribution is defined. | HPF `PROCESSORS`; the ML term is *device mesh*. |
| **device mesh** | A logical multi-dimensional arrangement of accelerators used to define sharding. | Mesh-TensorFlow; GSPMD; JAX. |
| **sharding** | ML-era term for distribution of a tensor over a device mesh, including replication along mesh axes. | GSPMD, Shardy. |
| **BLOCK / CYCLIC / CYCLIC(k)** | Contiguous-block, round-robin, and block-cyclic distributions. | HPF specification. |
| **owner-computes rule** | The place that owns the left-hand-side element of an assignment performs the assignment. | Named in the Fortran D and Kali literature; see paper cards. |
| **communication set** | The set of elements a place must send to or receive from another to execute a statement under a given distribution. | Koelbel 1991; Chatterjee et al. 1993; Stichnoth et al. 1994. |
| **local address generation** | Translating a global index to the index in a place's local array. | Chatterjee et al. 1993. |
| **message vectorization** | Hoisting element-wise messages out of loops and coalescing them. | Fortran D papers. |
| **overlap / halo / ghost region** | Extra local storage for copies of neighbouring places' boundary elements. | SUPERB *overlap*; stencil DSLs *halo*. |
| **redistribution / resharding** | Changing a distribution between program phases. | HPF `REDISTRIBUTE`; ML *resharding*. |
| **inspector–executor** | A runtime scheme in which an *inspector* loop examines indices to build a communication schedule that an *executor* loop then uses. | Saltz and collaborators (PARTI). |
| **import / export schedule** | Lists of off-place elements a place needs (import) or must supply (export). | PARTI; also Tpetra `Import`/`Export`. |
| **mapping array / INDIRECT distribution** | An explicit array giving the owner of each element. | PARTI/CHAOS; HPF-2 `INDIRECT`. |
| **SPMD** | Single program, multiple data: one program text executed by every place with place-dependent control. | Term used in the Fortran D and HPF literature; ML *SPMD partitioner*. |
| **partition propagation** | Inferring shardings of unannotated tensors from annotated ones through the graph. | GSPMD; Shardy. |
| **inter-/intra-operator parallelism** | Splitting the graph into stages across devices vs. splitting individual operators. | Alpa. |
| **logical region** | A named set of data with privileges that tasks declare; the runtime maps it to memories. | Legion. |
| **spatial placement** | Assigning computation to positions on a 2-D fabric so that communication becomes neighbour routing. | Wafer-scale / CGRA literature. |
| **foundations** | Pre-1980 compiler and architecture work that did not address distributed memory but supplied the analysis and machine concepts later used. | This survey. |
