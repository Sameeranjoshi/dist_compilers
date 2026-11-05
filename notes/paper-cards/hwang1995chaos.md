# Runtime and Language Support for Compiling Adaptive Irregular Programs on Distributed-memory Machines
**Catalog id:** `hwang1995chaos`
**Citation:** Yuan-Shin Hwang, Bongki Moon, Shamik D. Sharma, Ravi Ponnusamy, Raja Das, and Joel H. Saltz. "Runtime and Language Support for Compiling Adaptive Irregular Programs on Distributed-memory Machines." Software-Practice and Experience, vol. 25, no. 6, pp. 597-621, June 1995. DOI or record used: no DOI printed in the PDF; PDF text used.
**Paper type:** runtime
**Access:** PDF supplied by the repository owner. Full text read (text layer complete, 25 pages; table values read from the text layer and checked against column order).
**Card status:** full-read

## Problem
In adaptive irregular programs, indirection arrays change during the run, so inspector work and data movement must be repeated (Sec. "Adaptive irregular loop structures", pp. 598-600). The paper presents the CHAOS library, which subsumes PARTI and adds light-weight schedules for such programs, and tests it in a Fortran 90D/HPF compiler (Abstract, p. 597).

## Input abstraction
Loops that reach distributed arrays through indirection arrays indexed by the loop variable. The modification pattern is occasional in CHARMM (non-bonded list) and frequent in DSMC (cell membership) (pp. 598-600, Figs. 2-4). Language inputs are Fortran D directives, REDUCE, and a proposed reduce(append) intrinsic (pp. 612-615, Figs. 10-13).

## Target
Distributed-memory message-passing machines. The library is described for the Paragon, Delta, CM-5 and SP-1 (p. 597). All measurements are on an Intel iPSC/860 hypercube (pp. 604, 616).

## Data decomposition
Distributed arrays are laid out irregularly through a translation table that gives processor and offset for each global index (p. 602). CHARMM atoms are partitioned by recursive coordinate and inertial bisection, which use spatial data and load (pp. 605-606). DSMC cells are repartitioned every 40 steps by RCB, RIB or a one-dimensional chain partitioner (pp. 610-611, Table V).

## Computation mapping
Non-bonded loop iterations go to the processor that owns the atom. Bonded loop iterations go to the processor holding the most of their elements, with ties broken by lower load (pp. 606-607).

## Communication generation
Schedule generation has two phases. An index analysis phase hashes global indices into a table, removes duplicate off-processor references and assigns buffer slots. Each indirection array gets a stamp, so stamp combinations give gather and scatter schedules, including incremental and merged ones (pp. 601-604, Figs. 6-7). Light-weight schedules omit the placement order that regular schedules must keep, which suits set-valued data such as DSMC particles (pp. 604-605, 610).

## Compiler / runtime split
Directive processing and the loop transformations are compile time (pp. 613-618). The generated code calls CHAOS for remapping, inspection and execution. It records when indirection arrays may have changed and rebuilds schedules only when needed (p. 616, Fig. 15). The reduce(append) intrinsic lets the compiler choose light-weight schedules (pp. 613-615).

## Evaluation
CHARMM (MbCO plus 3830 water molecules) and a 2-D and 3-D DSMC code, both on the iPSC/860 (pp. 605-618). Compiler-generated CHARMM loops are within about 2 percent of hand code in total time on 32 and 64 processors (Table VI, p. 616). Compiler-generated DSMC is slower: total time 15.47 s versus 8.51 s on 4 processors and 5.30 s versus 3.75 s on 32 (Table VII, p. 618). Light-weight schedules cut 2-D DSMC time from 63.74 s to 20.14 s on 16 processors with 48x48 cells (Table IV, p. 611).

## Principal limitation
The authors state that in highly adaptive programs the inspector is not a one-time cost and must be repeated whenever an indirection array changes (p. 601). They also state that current compilers do not detect reductions in data movement, so the user must signal reduce(append) through the proposed intrinsic (p. 613).
our observation: both application studies use one machine (iPSC/860) and one prototype compiler, so the compiler-versus-hand comparison rests on a narrow base.

## Relationship to earlier / later work
The paper states that CHAOS subsumes PARTI, which had its own specialized incremental and merged schedules, and that CHAOS unifies them behind one global hash table (pp. 597, 603-604). It credits Kali with the first inspector/executor preprocessing and ARF with the first irregular arrays (p. 618). It cites a technical report by Ponnusamy and co-authors on irregular distributions for preprocessing reuse (ref. 6, "to appear in IEEE TPDS"; p. 616). inferred: that report is the same work as the ponnusamy1995runtime card in this set, which has the same title and authors. It notes that HPF-1 supports only BLOCK and CYCLIC (p. 614) and that reduce(append) can be carried into HPF as a list-scatter reduction (p. 615).

## Sources used
| claim | section / page |
|---|---|
| CHAOS subsumes PARTI; target machines | Abstract, p. 597 |
| Phases A-F of irregular solution | Sec. "Overview of CHAOS", pp. 600-601, Fig. 5 |
| Two-phase schedules, stamps, incremental schedules | pp. 601-604, Fig. 7 |
| Light-weight schedules | pp. 604-605 |
| CHARMM execution times | Table I, p. 607 |
| Schedule merging | Table III, p. 608 |
| Light-weight vs regular schedules in DSMC | Table IV, p. 611 |
| Remapping in DSMC, load imbalance | p. 611, Table V |
| Reduce(append) and HPF extension | pp. 613-615 |
| Compiler-generated vs hand CHARMM | Table VI, p. 616 |
| Compiler-generated vs manual DSMC | Table VII, p. 618 |
| Prior compilers and systems | p. 618 |
| Ponnusamy et al. technical report and TPDS paper | p. 616; ref. 6 |

## Open questions for the survey
- Light-weight schedules are measured only in DSMC. How do they compare in codes where element order matters but access is still adaptive?
- The compiler reuse test is a per-loop modification record. What does it cost when indirection arrays change every step, as in DSMC?
- Reduce(append) relies on user signalling. How would compiler-detected reductions compare on the same loops?
