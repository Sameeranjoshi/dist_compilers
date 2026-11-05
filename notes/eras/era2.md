# Era 2: Global arrays and data decomposition (1988–1992)

Working notes for the era section of the paper. Everything here is either a pointer to catalog evidence or an explicitly labelled hypothesis.

**Machine driver.** Commercial hypercubes and MPPs (iPSC/2, iPSC/860, nCUBE-2, CM-2).

**Programming abstraction.** Sequential or global-array programs with distribution annotations (SUPERB, Kali, Vienna Fortran, Fortran D).

**Decomposition representation.** BLOCK/CYCLIC distributions, alignment to templates/decompositions, overlap regions.

**Generated communication.** Compiler-generated point-to-point messages; message vectorization; first inspector-executor runtimes.

**Limitation that motivated the next era.** Regular, affine programs only; automatic distribution selection intractable in general; communication costs poorly modelled.

**Boundary evidence.** Callahan & Kennedy, SUPERB, Chen/Choo/Li (all 1988); Fortran D and Vienna Fortran papers 1991-92.

## Catalog entries in this era

| id | year | status | paper card |
|---|---|---|---|
| `callahan1988compiling` | 1988 | discovered |  |
| `chen1988compiling` | 1988 | discovered |  |
| `zima1988superb` | 1988 | discovered |  |
| `gerndt1990updating` | 1990 | screened |  |
| `mehrotra1990kali` | 1990 | read | yes |
| `saltz1990runtime` | 1990 | read | yes |
| `chapman1991vienna` | 1991 | read | yes |
| `das1991irregular` | 1991 | read | yes |
| `hiranandani1991fortrand` | 1991 | discovered |  |
| `koelbel1991compiling` | 1991 | discovered |  |
| `koelbel1991kali` | 1991 | discovered |  |
| `koelbel1991regular` | 1991 | discovered |  |
| `li1991alignment` | 1991 | discovered |  |
| `ramanujam1991compiletime` | 1991 | discovered |  |
| `saltz1991multiprocessor` | 1991 | read | yes |
| `chapman1992vienna` | 1992 | read | yes |
| `gupta1992automatic` | 1992 | discovered |  |
| `hiranandani1992compiling` | 1992 | discovered |  |
| `hiranandani1992evaluation` | 1992 | discovered |  |

## Synthesis (draft)

- What changed: TODO after the era's core papers are read.
- What remained: TODO.
- Limitation motivating the next era: see above; to be confirmed from primary sources.
