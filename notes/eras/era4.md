# Era 4: MPI dominance and alternative programming models (2000–2010)

Working notes for the era section of the paper. Everything here is either a pointer to catalog evidence or an explicitly labelled hypothesis.

**Machine driver.** Commodity clusters, early multicore nodes, Cell/BE and explicitly managed memories.

**Programming abstraction.** MPI(+OpenMP); PGAS (UPC, Co-array Fortran, Titanium); HPCS languages (Chapel, X10); hierarchical memory models (Sequoia).

**Decomposition representation.** Language-level distributions and locales/places; hierarchical task trees.

**Generated communication.** One-sided communication, compiler-scheduled bulk transfers for memory hierarchies.

**Limitation that motivated the next era.** Adoption of new languages remained limited; automatic distribution rarely used in production.

**Boundary evidence.** Co-array Fortran (1998); UPC/Titanium compilers; Sequoia (2006); X10 (2005); Chapel (2007); Pluto (2008).

## Catalog entries in this era

| id | year | status | paper card |
|---|---|---|---|
| `numrich1998coarray` | 1998 | screened |  |
| `yelick1998titanium` | 1998 | discovered |  |
| `tang2000tiled` | 2000 | discovered |  |
| `chen2003upc` | 2003 | discovered |  |
| `charles2005x10` | 2005 | discovered |  |
| `fatahalian2006sequoia` | 2006 | discovered |  |
| `chamberlain2007chapel` | 2007 | screened |  |
| `kennedy2007rise` | 2007 | discovered |  |
| `baskaran2008automatic` | 2008 | discovered |  |
| `bondhugula2008pluto` | 2008 | discovered |  |

## Synthesis (draft)

- What changed: TODO after the era's core papers are read.
- What remained: TODO.
- Limitation motivating the next era: see above; to be confirmed from primary sources.
