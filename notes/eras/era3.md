# Era 3: HPF, MPI, and compiler maturity (1993–2000)

Working notes for the era section of the paper. Everything here is either a pointer to catalog evidence or an explicitly labelled hypothesis.

**Machine driver.** MPPs (CM-5, Paragon, SP2, T3D/T3E) and early clusters.

**Programming abstraction.** HPF directives; MPI library calls; irregular extensions.

**Decomposition representation.** HPF ALIGN/DISTRIBUTE with BLOCK, CYCLIC(k), templates and processor arrangements; INDIRECT/mapping arrays in HPF-2 and research systems.

**Generated communication.** Communication sets, local address generation, redistribution, collectives; PARTI/CHAOS schedules for irregular code.

**Limitation that motivated the next era.** HPF compilers were slow to mature and performance was unpredictable; explicit MPI became the dominant practice.

**Boundary evidence.** HPF 1.0 (1993); MPI 1.0 (1994); PARADIGM journal paper (1995); Benkner/Zima HPF overview (1999).

## Catalog entries in this era

| id | year | status | paper card |
|---|---|---|---|
| `amarasinghe1993communication` | 1993 | discovered |  |
| `anderson1993global` | 1993 | discovered |  |
| `bik1993sparse` | 1993 | discovered |  |
| `bozkus1993fortran90d` | 1993 | discovered |  |
| `chatterjee1993generating` | 1993 | discovered |  |
| `hpfforum1993spec` | 1993 | screened |  |
| `loveman1993hpf` | 1993 | discovered |  |
| `ponnusamy1993schedule` | 1993 | discovered |  |
| `su1993paradigm` | 1993 | discovered |  |
| `zima1993compiling` | 1993 | discovered |  |
| `das1994communication` | 1994 | discovered |  |
| `mpiforum1994standard` | 1994 | screened |  |
| `rogers1994compiling` | 1994 | discovered |  |
| `stichnoth1994generating` | 1994 | discovered |  |
| `ancourt1997linear` | 1995 | screened |  |
| `banerjee1995paradigm` | 1995 | discovered |  |
| `gupta1995hpf` | 1995 | discovered |  |
| `harris1995dechpf` | 1995 | read | yes |
| `hwang1995chaos` | 1995 | screened |  |
| `lee1995techniques` | 1995 | discovered |  |
| `ponnusamy1995runtime` | 1995 | discovered |  |
| `gropp1996mpich` | 1996 | discovered |  |
| `palermo1996dynamic` | 1996 | discovered |  |
| `ramaswamy1996redistribution` | 1996 | discovered |  |
| `benkner1999compiling` | 1999 | discovered |  |

## Synthesis (draft)

- What changed: TODO after the era's core papers are read.
- What remained: TODO.
- Limitation motivating the next era: see above; to be confirmed from primary sources.
