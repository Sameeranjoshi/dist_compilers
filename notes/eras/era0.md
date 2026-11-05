# Era 0: Foundations (1950–1979)

Working notes for the era section of the paper. Everything here is either a pointer to catalog evidence or an explicitly labelled hypothesis.

**Machine driver.** Stored-program machines, FORTRAN, pipelined vector processors, lock-step array processors, dataflow and systolic proposals.

**Programming abstraction.** Sequential FORTRAN; vector statements; early parallel-language proposals.

**Decomposition representation.** None for distribution; dependence graphs and loop-level analysis for vectorization.

**Generated communication.** None (shared or centralised memory).

**Limitation that motivated the next era.** No notion of data placement as a compiler problem; machines had a single address space or SIMD broadcast control.

**Boundary evidence.** FORTRAN I (1957); ILLIAC IV (1968 design paper); Lamport hyperplane (1974); CRAY-1 (1978); dependence-graph optimizations (Kuck et al. 1981 sits at the boundary).

## Catalog entries in this era

| id | year | status | paper card |
|---|---|---|---|
| `backus1957fortran` | 1957 | discovered |  |
| `barnes1968illiac` | 1968 | discovered |  |
| `lamport1974parallel` | 1974 | discovered |  |
| `dennis1975preliminary` | 1975 | discovered |  |
| `russell1978cray1` | 1978 | discovered |  |
| `kuck1981dependence` | 1981 | discovered |  |

## Synthesis (draft)

- What changed: TODO after the era's core papers are read.
- What remained: TODO.
- Limitation motivating the next era: see above; to be confirmed from primary sources.
