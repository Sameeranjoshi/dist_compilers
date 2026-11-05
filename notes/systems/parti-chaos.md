# PARTI / CHAOS

Runtime library family from ICASE and the University of Maryland (Saltz and
collaborators) that compilers targeted for irregular computations.

Evidence so far (from the paper cards of the open ICASE reports):

- **ICASE 89-7** (`saltz1990runtime`): preprocessor builds paired
  send/receive lists, translates global to local indices and reorganises
  data; a table-driven "schedule executer" runs the loop. The words
  inspector/executor are not yet used.
- **ICASE 90-59** (`saltz1991multiprocessor`): introduces the inspector /
  executor vocabulary, the hashed cache and the distributed translation
  table; describes ARF, the first prototype compiler generating PARTI calls
  for irregularly distributed arrays.
- **ICASE 91-73** (`das1991irregular`): PARTI primitives (translation tables,
  schedules, gather/scatter/accumulate), incremental schedules, and a mapper
  coupler that feeds runtime dependence/iteration graphs to graph
  partitioners; proposes Fortran D extensions (`implicitmap`,
  `distribute ... implicit using`).

Still to read: CHAOS papers (`ponnusamy1993schedule`, `das1994communication`,
`ponnusamy1995runtime`, `hwang1995chaos`) and the PARTI primitives report
(Sussman, Saltz, Das 1992) downloaded from NTRS.

Open question: when did the library name change from PARTI to CHAOS, and
which paper first documents schedule reuse across time steps?
