# Era 5: Compiler/runtime co-design and accelerators (2010–2019)

Working notes for the era section of the paper. Everything here is either a pointer to catalog evidence or an explicitly labelled hypothesis.

**Machine driver.** GPU clusters, heterogeneous nodes, early TPU pods.

**Programming abstraction.** Affine loop nests; task/region programs (Legion, Regent); tensor DSLs; ML graph frameworks.

**Decomposition representation.** Polyhedral partitions; logical regions and partitions; named-dimension layouts (Mesh-TensorFlow).

**Generated communication.** Polyhedral communication-set generation with MPI; dynamic region coherence; collectives in ML frameworks.

**Limitation that motivated the next era.** Each system covered one domain; no shared ownership IR; ML partitioning still largely manual.

**Boundary evidence.** Bondhugula distributed polyhedral codegen (2011/2013); Legion (2012); Molly (2014); Mesh-TensorFlow (2018); FlexFlow/PipeDream/Megatron (2019).

## Catalog entries in this era

| id | year | status | paper card |
|---|---|---|---|
| `bondhugula2011automatic` | 2011 | read | yes |
| `bauer2012legion` | 2012 | discovered |  |
| `bondhugula2013compiling` | 2013 | discovered |  |
| `kruse2014molly` | 2014 | read | yes |
| `ravishankar2015mixed` | 2015 | discovered |  |
| `slaughter2015regent` | 2015 | discovered |  |
| `dathathri2016compiling` | 2016 | screened |  |
| `unat2017trends` | 2017 | discovered |  |
| `huang2019gpipe` | 2018 | discovered |  |
| `shazeer2018meshtf` | 2018 | read | yes |
| `baghdadi2019tiramisu` | 2019 | discovered |  |
| `jia2019flexflow` | 2019 | read | yes |
| `narayanan2019pipedream` | 2019 | discovered |  |
| `shoeybi2019megatron` | 2019 | discovered |  |
| `wang2019tofu` | 2019 | discovered |  |

## Synthesis (draft)

- What changed: TODO after the era's core papers are read.
- What remained: TODO.
- Limitation motivating the next era: see above; to be confirmed from primary sources.
