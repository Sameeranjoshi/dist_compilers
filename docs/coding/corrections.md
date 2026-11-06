# Coding corrections and definitional changes

This file records every change made to a coded value, or to the definition of a
generalization test, after the second coding existed. Each entry says what changed,
why, and what it does to the counts. The sensitivity analysis still reports the
first and second codings separately, so each correction can be checked against them.

## Reconciling records with the reviewed catalog (Era 4 round)

The merge script copies classification fields from `notes/paper-cards/_records/*.json`
into the catalog. Some catalog values had been edited directly after the records were
written (commit `d6ffcc1`, which restructured the paper around the taxonomy). The merge
then overwrote them. The records have been corrected to the reviewed values:

- `gupta1992automatic`, `lee1995techniques`, `palermo1996dynamic`:
  `compiler_runtime_boundary` is `analytic-optimization`. The paper's taxonomy section
  describes these as cost-model decision procedures, and the reviewed catalog said so.
  The card had recorded `fully-static`.
- `numrich1998coarray`: `data_decomposition` is empty. The reviewed catalog had removed
  `application-defined`, because a per-image declaration with no map object does not fit
  that value. The merge skips empty lists, so the catalog value was set directly.

## Correction to a first-coding value (Pluto)

`bondhugula2008pluto` was coded `fully-static` and `static-with-directives` from its
card. The card instruction list given to the card writer omitted `analytic-optimization`.
The card text describes an integer linear program over a bounding cost function, and
no programmer annotations, so the value is `analytic-optimization`. The record's notes
say so. The computation-mapping values for this paper were coded by the first coder and
are left as coded; they differ from the second coding, and the sensitivity analysis
reports that.

## Change to the definition of the G1 test

The G1 claim says that where ownership is set by an explicit map, the read systems that
describe a run-time mechanism for it have a run-time stage. The script tested a broader
set: every paper with irregular or user-defined ownership (population A). The claim's
own rationale is that a compiler adds a run-time stage when it must generate communication
for an owner it cannot know. Population B keeps papers whose communication is generated
by the system (any communication value other than `programmer-explicit`). B was defined
after the Era 4 papers were coded. A is reported beside B, and the exceptions are named.

Under B, the result is 17 of 19 papers with a run-time stage under the first coding and
17 of 20 under the second. The load-time variant (counting load-time evaluation of a user
map as a run-time stage) gives 19 of 19 and 19 of 20.

## Change to the G2 test

G2 was stated as "search-based decomposition appears only from 2019". The script counts a
paper as search-based when its compiler/runtime boundary includes `profile-guided` or
`autotuned`. That counts tuning of an update strategy as well as a decomposition choice,
so the test is wider than the claim. Under the first coding the pre-2019 exception is
Fortran D's 1992 evaluation. Under the second it is Su's 2010 dissertation, whose tuning is
of the multicore update strategy. The claim is therefore reported as suggested.

## Merge behaviour

`scripts/merge_card_records.py` now appends notes only when the text is absent, so
repeated runs no longer duplicate them. The merge still skips empty lists, so it cannot
clear a value. Clearing a value must be done in the catalog, and the record should be
changed to match.
