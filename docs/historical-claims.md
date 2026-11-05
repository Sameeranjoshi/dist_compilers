# Historical Claims and Their Evidence

Every cross-era claim made in the paper that is an inference or synthesis
(evidence class 3 in `docs/methodology.md`) is listed here with the evidence
currently available and what would confirm or refute it.  Source-supported
facts are not listed; they carry citations in the paper.

| # | claim (as hypothesised) | current evidence | status | what would settle it |
|---|---|---|---|---|
| H1 | The HPF processor grid and the ML device mesh are the same abstraction (a logical multi-dimensional arrangement of places over which per-dimension distributions are defined). | HPF 1.0 spec (PROCESSORS, DISTRIBUTE onto processor arrangements); Mesh-TensorFlow Sec. 4-5 and GSPMD Sec. 3.1 (device mesh, per-dimension tiling), from paper cards. | functional correspondence supported; no citation link found | Check whether Mesh-TensorFlow / GSPMD / Shardy cite HPF or ScaLAPACK; search their related-work sections. |
| H2 | ALIGN/DISTRIBUTE directives and sharding annotations play the same role (programmer-supplied partial ownership information completed by the compiler). | Fortran D / HPF (metadata-level); GSPMD Sec. 3.5 "sharding completion" (card). | plausible; Fortran D side not yet read | Read hiranandani1992compiling to confirm that Fortran D infers unannotated distributions. |
| H3 | Owner-computes and sharding propagation both derive computation mapping from data mapping. | Kali card (doall on owner(), Sec. 3); GSPMD card (propagation from annotated operands). | supported at mechanism level | Document the exceptions: DEC HPF explicitly did not adopt strict owner-computes (card); Alpa's ILP chooses per-operator shardings. |
| H4 | Communication-set generation (1991-94) and collective insertion (2018-25) solve the same problem on different representations. | Koelbel 1991, Chatterjee 1993, Stichnoth 1994 (metadata-level); Mesh-TensorFlow Sec. 6, GSPMD Sec. 4, PartIR Sec. 6 (cards). | plausible; 1990s side not yet read | Read the three 1990s papers. |
| H5 | HPF REDISTRIBUTE / PARADIGM dynamic partitioning and ML resharding are the same operation. | Vienna Fortran DISTRIBUTE statement (card, 1991 Sec. 2.4); GSPMD Sec. 4.5 and Alpa Sec. 6 cross-mesh resharding (cards). | supported for the language-level operation | Compare the redistribution algorithms (ramaswamy1996redistribution, unread) with Alpa's. |
| H6 | Inspector-executor is the ancestor of runtime communication planning in SpDISTAL and MLIR distributed sparse tensors. | saltz1990runtime, saltz1991multiprocessor, das1991irregular (cards); SpDISTAL card (image/preimage dependent partitioning at run time). | functional correspondence; SpDISTAL does not use the term | Check whether yadav2022spdistal or vaidya2025distributed cite PARTI/CHAOS. |
| H7 | PARTI import/export schedules correspond to sparse tensor slice exchange. | das1991irregular card (schedules, flocalize); SpDISTAL card. | weak; terminology differs | Needs a mechanism-level comparison. |
| H8 | Hierarchical machine mappings (Sequoia, PARADIGM task+data parallelism) prefigure Alpa's inter-/intra-operator split. | Alpa card (hierarchical plan space); Sequoia metadata-level. | plausible | Read fatahalian2006sequoia; check Alpa related work. |
| H9 | Explicit MPI won in Eras 3-4 because its cost model is transparent and does not depend on compiler maturity. | kennedy2007rise (metadata-level; the HOPL paper is the authoritative retrospective). | hypothesis | Read kennedy2007rise and benkner1999compiling. |
| H10 | High-level partitioning returned in Era 6 because operator graphs make propagation and cost modelling tractable. | GSPMD card (no cost model needed; operator-level patterns); Alpa card (ILP over enumerated per-operator algorithms). | hypothesis with partial support | Compare against evidence from the 1990s on why distribution selection was intractable (ramanujam1991compiletime, gupta1992automatic). |
| H11 | The inspector/executor vocabulary originates in ICASE 90-59 (1990), not in the 1989 report. | ICASE 89-7 uses "preprocessor"/"schedule executer"; ICASE 90-59 Sec. 3 uses inspector/executor (card). | supported by the two reports | Check the JPDC 1990 journal version of 89-7, which may have changed the wording. |

Conflicts between sources are recorded here as they are found:

- **C1** Crossref author order for `saltz1990runtime` is Saltz, Crowley,
  Mirchandaney, Berryman; the ICASE 89-7 cover lists Crowley, Saltz,
  Mirchandaney, Berryman.  The catalog follows the journal record.
- **C2** The MPI 1.1 document gives "Version 1.0: June, 1994" in its header
  but refers to "the MPI document of May 5, 1994 ... Version 1.0" in its
  text.  The catalog records May 1994.
- **C3** Crossref spells the second author of `su1993paradigm` "Palerrno";
  the correct spelling is Palermo (Crossref data error, noted in the entry).
