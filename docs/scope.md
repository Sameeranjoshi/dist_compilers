# Scope and Inclusion Criteria

This document fixes what the survey *is about* so that screening decisions in
`docs/discovery-log.md` can be audited.  The same text, condensed, appears in
`paper/sections/02-methodology.tex`.

## Central question

How have compilers for machines with physically distributed memories
represented, decomposed, mapped, communicated, optimized, and executed data and
computation?

## Operational definition

A **distributed-memory compiler** is a compiler, compiler framework, programming
system, or compiler-integrated runtime that transforms a program for execution
across multiple computational *places* whose memories are physically or
logically distinct at the relevant compilation level.

A system is **included** when it performs or represents at least one of:

1. data distribution or ownership;
2. computation partitioning or placement;
3. communication generation;
4. collective insertion;
5. halo or ghost-region construction;
6. global-to-local address conversion;
7. import/export schedule generation;
8. redistribution or resharding;
9. hierarchical parallelism across nodes/devices;
10. distributed execution-plan generation;
11. distributed-memory performance modeling used by a compiler.

### Multi-GPU and spatial targets

Multiple GPUs are a distributed-memory target when the compiler must partition
data or computation and generate communication between device memories.  Shared
memory, caches, or registers *inside* one GPU do not remove the
distributed-memory problem at the multi-GPU level.

A wafer-scale or spatial architecture counts when individual processing
elements (or groups of them) have distinct local memories and data movement
must be compiled explicitly.

## Categories

**Central**

- automatic distributed-memory parallelization;
- global-array and data-parallel compilers;
- Fortran D, HPF, and related systems;
- automatic MPI or message-passing generation;
- distributed tensor and sparse-tensor compilers;
- SPMD partitioners;
- distributed GPU/accelerator compiler systems;
- spatial and wafer-scale compiler systems.

**Bridge / compiler-adjacent**

- languages whose compiler implements distributed memory (PGAS, HPCS languages);
- compiler-integrated runtimes such as inspector–executor systems;
- task/region systems when compilation and placement are central;
- distributed-training systems with substantial plan generation or compilation;
- performance models that drive compiler decomposition decisions.

**Excluded or de-emphasized**

- distributed databases;
- distributed operating systems without compiler relevance;
- generic cloud job scheduling;
- network-routing protocols;
- hardware-only papers with no programming/compiler contribution
  (a small number are kept in the catalog with `relevance_tier: foundation`
  and `paper_type: hardware` purely to date the *target classes*; they are not
  classified on the compiler axes);
- application scaling studies with no compiler method;
- shared-memory-only compilers;
- generic GPU kernel compilers that never address inter-device distribution;
- pure runtime systems unless a compiler or high-level program transformation
  is an essential part of the design.

## Time span and the "foundations" caution

The survey covers 1950 through the end of 2026, but **mature distributed-memory
compilers did not exist before the late 1980s**.  Work from roughly 1950–1979
is classified as *foundations*: automatic programming and FORTRAN, compiler
construction, dependence analysis, vectorization, dataflow, array processors,
and early parallel-machine abstractions that later enabled distributed-memory
compilation.  The paper must never imply that these systems distributed data
across memories.

Representative machines for the foundations era must be validated from
primary architecture papers.  Historically appropriate examples are the ILLIAC
IV array processor, CDC and Cray vector systems, systolic arrays, and (for Era
1) hypercubes and multicomputers.  The PDP-11 is a minicomputer and is **not**
a representative vector machine; it must not be used as one.

## Deduplication rule

Workshop, technical-report, conference, and journal versions of the same work
are catalogued as **one primary entry** (normally the most complete archival
version) with other versions listed under `related_versions` or in `notes`.
If two versions differ materially in content (for example the Fortran D
"compiling" and "evaluation" papers of 1992), both are kept.

## Relevance tiers

| tier | meaning |
|------|---------|
| `core` | central to the taxonomy; eventually needs a paper card |
| `bridge` | compiler-adjacent with substantial compilation content |
| `foundation` | pre-distributed-memory foundation or hardware context |
| `adjacent` | referenced for context only; not classified on every axis |
