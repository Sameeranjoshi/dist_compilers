# Diagnostic review of the manuscript (draft of 2026-11-07, commit 71a761f)

Manuscript: `paper/main.tex`, "Compiling for Distributed Memory: A Historical Survey and Taxonomy from Global Arrays to Mesh-Sharded AI Systems", IEEEtran journal format, 20 pages, 14 sections, 5 figures, 2 tables in the body plus the sensitivity table, 83 cited keys from a 112-entry bibliography. Reviewer: an evaluation of the full LaTeX source, the rendered PDF, the generated tables in `paper/tables/`, and the figures. Nothing outside the repository was consulted; where a claim below depends on literature not in the catalog it is marked "possible omission".

Page numbers refer to the PDF built from the current source: §I p.1, §II p.2, §III p.3, §IV p.4, §V p.4–5, §VI p.5–10, §VII p.10, §VIII p.11, §IX p.11, §X p.12, §XI p.12–13, §XII p.13–17, §XIII p.17, §XIV p.18, references p.18–20.

---

## Report A: Executive assessment

**What the paper is.** A hybrid historical survey and taxonomy whose distinguishing feature is its method: an open, schema-validated catalog, paper cards with section-level evidence, two independent codings of 78 read papers on five axes, agreement statistics and a sensitivity analysis. The central thesis, stated in §I-A, is that the distributed-memory compilation stack (ownership, computation mapping, communication synthesis) is rebuilt each time a new machine class appears, and that the 2020s sharding compilers rebuild the 1990s HPF stack under new names. The intended audience is compiler researchers in both the HPC and the ML-systems communities. What a reader gains that the individual papers do not give: the then-and-now correspondence (Table I), the era narratives with quoted measurements (§VI), and Kennedy, Koelbel and Zima's four causes of HPF's decline applied to GSPMD, PartIR and Alpa (§XII-D).

**What it currently achieves.** §VI is a genuinely good piece of historical writing: every era is built from primary-source facts with numbers, and each era's "what it learned" paragraphs are analytical, not descriptive. §XII delivers synthesis: Table I is a mechanism-level comparison with an honest citation column, the four-causes test is the paper's best idea, and the generalization table with refuting observations is a model of falsifiable survey writing. The methodology (§II, §V-D) is more rigorous than almost any narrative survey in compilers: the counts are regenerable and the second coding is reported even where it destroys the first coding's claims.

**Central weaknesses.** First, structure: §VII to §XI (five mechanism sections, four pages) restate facts already given in §VI and defer every count to §XII, so the middle of the paper is a catalog of pointers rather than analysis. Second, the taxonomy is asserted rather than argued: §V defines eleven axes in one paragraph, never defines their values in the paper, gives no coding rules, and the resulting low agreement (41 to 15 percent exact-set) is then allowed to withdraw most of the paper's quantitative findings. The abstract reads as a list of what did not survive. Third, there is no common-criteria comparison of systems in the manuscript. The repository generates a 28-system table, a decomposition-support table, an architecture table and an evaluation table, but none is included, and the evaluation table is entirely unfilled. Fourth, internal inconsistency: the abstract says 71 papers and §XII says 78; §V-D reports agreement of 26/20/20/52/6 percent while §XII reports 41/28/32/51/15; G8 claims "seven of eight mechanisms reappear with the same structure" while the paragraph after Table I says the design is unchanged in two rows; §VI says Eras 0 and 1 "have no full-text reads" while §III says every foundations paper has a card. Fifth, Fig. 5 (the rediscovery map) names four catalog entries that are unread (`zima1988superb`, `das1994communication`, `hiranandani1992compiling`, `koelbel1991compiling`) and pairs concepts differently from Table I, which violates the paper's own evidence rule.

**Most important changes.** (1) Collapse §VII–§XI into §VI or into §XII so that each mechanism is treated once, analytically. (2) Put the taxonomy on the page: define each value used in a finding, give the coding rule, and treat the agreement figures as a validity study rather than as the main result. (3) Include a curated systems table on common criteria, with the evaluation columns filled from the cards. (4) Reconcile every number and every figure with the catalog, and regenerate the rediscovery map from read entries only. (5) Rewrite the abstract and conclusion around the positive thesis (the stack is rebuilt per machine class; the program class, not compiler technology, is what changed) and answer the ten research questions that §I-C promises.

**Readiness.** Substantially developed; major revisions needed. Overall completion about 70 percent; weighted quality about 3.2 of 5.

---

## Report B: Scorecard

Weights are the diagnostic defaults. No adjustment was made: the paper claims both a taxonomy and synthesis, so dimensions 3 and 6 deserve their weight.

| Dimension | Weight | Completion % | Quality / 5 | Severity | One-line diagnosis |
|---|---:|---:|---:|---|---|
| 1. Research problem and motivation | 8 | 85 | 3 | Moderate | Clear three-question framing and thesis (§I); RQ1–RQ10 announced but never listed; no statement of what prior surveys lack |
| 2. Scope and literature coverage | 10 | 65 | 3 | Major | 78 of 112 read; Era 4 and HPF production compilers thin; core entries cited in §I and Fig. 5 are unread; Crossref-only search |
| 3. Taxonomy / organizing framework | 15 | 70 | 3 | Major | Eleven machine-readable axes, but values undefined in the paper, no codebook; the decision-procedure refinement (§V-B) is the one argued contribution |
| 4. Technical depth and accuracy | 10 | 75 | 4 | Moderate | §VI is mechanism-level with numbers; §VII–§XI shallow; no worked example tracing one program through eras |
| 5. Comparative analysis | 12 | 55 | 3 | Major | Table I is strong; no system-by-system table in the body; generated evaluation table is all "?"; cross-era numbers not normalised |
| 6. Critical insights and synthesis | 15 | 70 | 3 | Major | Four-causes test and Table I are real synthesis; G5/G6 near-tautological; the "program class changed" insight (§XII-B) is the best idea and is one paragraph |
| 7. Research gaps and future directions | 8 | 70 | 3 | Moderate | Derived from G-table with test status (good); mostly "we did not find", two items are closed, none specifies a technical formulation |
| 8. Narrative and logical progression | 7 | 65 | 3 | Major | §VI → §VII–XI → §XII repeats the same facts three times; coding discourse crowds out the history |
| 9. Clarity and readability | 5 | 80 | 4 | Moderate | Prose is precise; "under both codings" appears dozens of times; several numeric contradictions |
| 10. Figures, tables, visual communication | 4 | 60 | 3 | Moderate | Fig. 5 contradicts Table I and the evidence rule; Fig. 3 timeline illegible at print size; no systems table |
| 11. Methodological rigor and reproducibility | 4 | 85 | 4 | Minor | Best-in-class for a narrative survey; disclose the role of agents in carding and coding; §II-E points to a superseded file |
| 12. Conclusions and contribution delivery | 2 | 70 | 3 | Moderate | §XIV repeats the abstract; does not answer the central question or state what the taxonomy is for |
| **Overall** | 100 | **70** | **3.2** | | **Substantially developed; major revisions needed** |

Computation: completion = Σ weight × completion = 69.8; quality = Σ weight × quality = 3.19. These are expert estimates with roughly ±5 points of uncertainty on completion and ±0.3 on quality.

---

## Report C: Section-by-section audit

| Section | Purpose | Completion % | Quality / 5 | Main problem | Priority |
|---|---|---:|---:|---|---|
| Abstract | State thesis and findings | 80 | 3 | Stale count (71); reads as a list of withdrawn claims | P0 |
| §I Introduction (p.1) | Problem, scope, RQs, contributions | 85 | 3 | RQ1–RQ10 never listed; cites unread entries as facts | P1 |
| §II Methodology (p.2) | Inclusion, sources, screening, evidence levels | 85 | 4 | Reading strategy says "abstract, introduction, overview" for most papers, which conflicts with "only read entries support claims"; superseded historical-claims file | P1 |
| §III Foundations (p.3) | Separate inheritance from invention | 90 | 3 | Descriptive; its synthesis paragraph is the only analysis | P2 |
| §IV Common architecture (p.4) | Pipeline abstraction | 75 | 3 | Fig. 1 is generic; each stage is one sentence of examples; "stable since the early 1990s" asserted without a test | P2 |
| §V Taxonomy (p.4–5) | Axes and coding | 60 | 3 | Values undefined; no codebook; stale agreement numbers; two axes refined, nine not discussed | P0 |
| §VI Historical evolution (p.5–10) | Six eras in five parts | 90 | 4 | Era 1 is two paragraphs with no distributed-memory compiler; "no full-text reads" contradicts §III | P2 |
| §VII Decomposition and mapping (p.10) | Classes of ownership | 60 | 3 | Introduces a second framework (three classes) not reconciled with axis C; otherwise pointers to §XII | P1 |
| §VIII Communication (p.11) | Element vs collective generation | 60 | 3 | Four facts and one inference per subsection; restates §VI | P1 |
| §IX Runtime (p.11) | Forms and costs of run-time stage | 65 | 3 | Good framing (three forms); no cost comparison table | P1 |
| §X Performance modelling (p.12) | Decision procedures and objectives | 70 | 4 | Best of the mechanism sections; the analytic-vs-measured inference is testable and stated as such | P2 |
| §XI Modern systems (p.12–13) | Propagation, search, pipeline, sparse, wafer | 70 | 3 | Mostly fact lists; no comparison on common criteria among GSPMD, PartIR, Alpa, DISTAL | P1 |
| §XII Synthesis (p.13–17) | Then-and-now, patterns, four causes, generalizations | 80 | 4 | G8 contradicts Table I paragraph; G5/G6 weak; Fig. 5 inconsistent with Table I | P0 |
| §XIII Open problems (p.17) | Derived gaps | 70 | 3 | Two items marked "run" are not open; none formulated technically | P2 |
| §XIV Conclusion (p.18) | Synthesis and delivery | 60 | 2 | Repeats abstract; no answer to RQs; no statement of the taxonomy's use | P1 |

### Abstract
A. Works: states the method and the falsifiable findings; names the withdrawn claims.
B. Missing: the thesis (rebuilding per machine class; the program class changed). The count is 71; the body says 78.
C. Hard to read: "Agreement is low on most axes, so only the patterns that hold under both codings are reported" leads the reader to expect a negative paper.
D. Lacks insight: none of the three differences of §XII-B appears.
E. Change: lead with the thesis and Table I; give the coding as validation in one sentence; fix the count.
F. Expect: a reader sees a contribution before the caveats.

### §I Introduction
A. Works: the three questions (store, execute, communicate) are a strong frame and recur through the paper; honest statement that this is not the first survey, with six named prior overviews.
B. Missing: RQ1–RQ10 are "refined" into existence (§I-C) but never listed; §V does not map them to axes as promised. No statement of what the prior surveys do not do (all six predate or exclude the ML-era systems, which is the obvious gap, but the paper does not say so). Era 0 to 6 are referenced before they are defined (defined only in §VI and Table A, which is not included).
C. Hard to read: "We refine it into ten research questions ... Section V maps each to an axis" sends the reader to a section that does not.
D. Lacks insight: "often with terminology that does not acknowledge the earlier work" is the paper's sharpest claim and is supported only later, by the citation column of Table I; say so here.
E. Change: list the RQs (a table of RQ → section → finding), state the gap in prior surveys in one sentence, and move the era definitions forward or include Table A.
F. Expect: the reader knows what will be answered and can check in §XIV that it was.

### §II Methodology
A. Works: operational inclusion criteria; five statuses; the three kinds of statement; honest limitation that only Crossref was queried.
B. Missing: a threats-to-validity paragraph (single author, agent-drafted cards, coder independence, LLM involvement if any); the codebook; the date range of the search; how the 28 systems were chosen.
C. Hard to read: §II-E says inferences are "listed with their current evidence in the repository's historical-claims file"; the handoff marks that file superseded by Table III. §II-D says most papers were read at the level of abstract, introduction, overview, related work and conclusion, while §II-C says only read and verified entries support mechanism-level claims; a reader cannot tell which applies to a given claim.
D. Lacks insight: n/a (method section).
E. Change: add "Threats to validity"; replace the historical-claims reference; state the reading level per status; disclose the role of agents in card drafting and in the second coding (the §V-D phrase "agents drafting cards" is the only mention).
F. Expect: the paper's main selling point, its method, becomes auditable from the paper alone.

### §III Foundations
A. Works: the "bargain" framing (FORTRAN 1957 to HPF to sharding) is a genuine through-line; every claim cites a card.
B. Missing: nothing structural; it is a background section.
C. Hard to read: none.
D. Lacks insight: §III-A to §III-D are descriptive; only §III-E synthesises ("what they did not supply was any representation of where data resides").
E. Change: shorten §III-A to §III-D by a third and keep §III-E; move the bargain idea to §I so it frames the whole paper.
F. Expect: a page saved, and a frame that pays off in §XII.

### §IV A common compiler architecture
A. Works: the five-stage pipeline is a reasonable scaffold; Fig. 1 is clean.
B. Missing: evidence that the pipeline is "stable since the early 1990s" (§IV, Synthesis); any system that does not fit (Legion's runtime scheduler and Mesh-TensorFlow's graph-construction-time decisions are placed in the pipeline by assertion).
C. Hard to read: each paragraph is a list of two to four facts from different eras with no connecting sentence.
D. Lacks insight: the section does not say which stage each era innovated in, although §IV-Synthesis claims that axes B, K and F are what separate the eras.
E. Change: add one row per era to Fig. 1 or a small table "which stage changed in each era"; name the misfits.
F. Expect: the architecture becomes an analytic device rather than a diagram.

### §V Taxonomy
A. Works: §V-B (splitting "fully static" into closed-form analysis and analytic optimisation) is the paper's one argued taxonomic contribution, with named examples; §V-C (adding partition propagation) is justified.
B. Missing: definitions of the values of axes C, D, E, F and H (the five axes the findings use); the coding rule for each; the nine axes not discussed; the mapping from RQs to axes; a coverage matrix (era × axis) showing where the read set is empty.
C. Hard to read: §V-D gives agreement of 26/20/20/52/6 percent; §XII-C gives 41/28/32/51/15; §X gives 12 of 78 for objectives. Fig. 2 draws six axes and says the catalog has eleven.
D. Lacks insight: the taxonomy is not used to explain relationships between approaches anywhere except in §VII's separate "three classes".
E. Change: a value-definition table for the five counted axes with one-line coding rules (this is the codebook the G-table repeatedly asks for); reconcile numbers by generating them; either draw all eleven axes or say which five matter.
F. Expect: agreement should rise on recoding, and the taxonomy becomes reusable by others.

### §VI Historical evolution
A. Works: the strongest section. Each era quotes primary measurements (95 µs startup vs 0.4 µs per byte; 18.5 s vs 19.8 s vs 301 s for CHAOS reuse; 2393 s Alpa compile). The "what the era learned" paragraphs are analytical. The five-part structure is consistent.
B. Missing: Era 0 has no subsection (§III stands in but is not called Era 0); Era 1 contains no distributed-memory compiler and says so, which raises the question why it is an era. The HPF production compilers (PGHPF, xlhpf, ADAPTOR, VFC) are absent from Era 3, so "the compilers were good on regular codes" rests on DEC and pHPF alone.
C. Hard to read: "Eras 0 and 1 have no full-text reads" (§VI intro) contradicts §III and the sensitivity table (5 read papers in each). Fig. 3 (timeline) is unreadable at print size; labels are 4-point.
D. Lacks insight: Era 4's "What remained" says automatic placement "returned in the next era by two different routes" but Era 5 names three ideas.
E. Change: fix the contradiction; either merge Eras 0 and 1 into "Before 1988" or justify the split; redraw Fig. 3 with fewer events and larger type.
F. Expect: the section already carries the paper; the fixes remove avoidable reviewer objections.

### §VII Data decomposition and computation mapping
A. Works: the three classes (closed-form owners, declared maps, propagated shardings) and the claim that they predict the decision procedure is a real analytic idea.
B. Missing: reconciliation with axis C of the taxonomy (fifteen values) and with Fig. 4 (A/B/C groups, which are rectilinear/structured/irregular, a different trichotomy). Counts are deferred to §XII.
C. Hard to read: three different three-way groupings of decompositions appear in the paper (Fig. 4, §VII-A, axis C) and are never related.
D. Lacks insight: §VII-B and §VII-C are pointers; §VII-D ("alternatives to ownership") is the interesting case and is one paragraph.
E. Change: make the three classes the organising principle of axis C in §V, or drop them; develop §VII-D into the argument that pipeline and expert parallelism are placement of stages rather than elements.
F. Expect: one framework instead of three.

### §VIII Communication generation and redistribution
A. Works: the element-level vs collective distinction and its consequence ("the cost of a collective can be stated in volume alone") is a good analytic point.
B. Missing: a table of what each system generates (point-to-point, collectives, halo, resharding) on common criteria; the dmp/stencil and Kong facts duplicate §XI.
C. Hard to read: the section opens by saying the two codings disagree on Era 4 and 5, so no trend is stated; the reader then gets four one-paragraph subsections of facts.
D. Lacks insight: the "reduction overlapped with the computation that feeds it" candidate open problem is good and should be formulated.
E. Change: merge into a single "mechanisms" section with §VII and §IX, organised by the three questions of §I, each with a comparison table.
F. Expect: the middle of the paper becomes comparative rather than pointer-based.

### §IX Runtime analysis and irregular computation
A. Works: the three forms (inspector-executor, dynamic scheduling, run-time resolution) and "the reuse condition is the decisive design point" are analytical; §IX-C's separation of compile-time decision from closed-form decision is a sharp observation.
B. Missing: a cost table (inspector overhead as fraction of compute, reuse condition, break-even) across Saltz, Kali, CHAOS, Titanium, Su, SpDISTAL.
C. Hard to read: first sentence has a lower-case "the runtime pattern" after a colon and leans on §XII twice in two lines.
D. Lacks insight: the question the section raises, whether the run-time stage ever pays against a static alternative, is answered "not measured"; the section could at least tabulate the overheads that are reported.
E. Change: add the cost table; fix the sentence.
F. Expect: a reader can compare run-time stages across thirty years, which no cited paper allows.

### §X Performance modelling and optimisation objectives
A. Works: the analytic-vs-measured distinction with a stated test ("a system that uses a network model and a profile on the same workload") is the paper's cleanest testable inference.
B. Missing: a small table of cost-model inputs (startup, bandwidth, profile, simulator) per system.
C. Hard to read: "12 of 78" here vs "15 percent" in §XII is consistent but the §V-D figure is not.
D. Lacks insight: adequate.
E. Change: keep; add the inputs table.
F. Expect: minor.

### §XI Multi-GPU, ML, spatial and AI-accelerator compilers
A. Works: facts are now card-backed for every named system; the wafer-scale inference (compiler contributes the schedule, not the decomposition) is good.
B. Missing: a comparison of GSPMD, PartIR, Alpa, Shardy, DISTAL on common criteria (input, what is automated, cost model, communication, result); vendor compilers (Graphcore, SambaNova, Tenstorrent, Groq) are declared out of coverage but are named in the title's promise ("AI systems").
C. Hard to read: five subsections of two to four facts each; the closing paragraph is repository bookkeeping ("carded from documentation pages") that belongs in §II.
D. Lacks insight: the section's opening claim ("the recent systems share one design choice") is contradicted by its own §XI-C and §XI-E (pipeline libraries and wafer-scale codes do not propagate anything).
E. Change: open with the comparison table; move bookkeeping to §II; state which modern systems do and do not fit the propagation description.
F. Expect: the ML-systems reader, half the intended audience, gets a usable comparison.

### §XII Cross-era synthesis
A. Works: Table I with the citation column; §XII-B's three differences; §XII-D's four causes applied; Table III with refuting observations and tests; honest withdrawal paragraph.
B. Missing: a figure that shows the thesis (the stack rebuilt per machine class) rather than Fig. 5's concept pairs; a discussion of why the citation column is almost all "no" (community separation, venue, terminology) since this is the paper's sharpest observation.
C. Hard to read: G8 says "seven of the eight 1990s mechanisms reappear with the same structure" while the paragraph after Table I says the design is unchanged in two rows and changed in the others; "five to seven of the eleven Era 6 papers" (also §VI, §XIII) while Era 6 now has 15 read papers; Fig. 5's date range (1988–2006 → 2018–2025) differs from Table I's (1988–2000 → 2018–2026); Fig. 5 pairs "ALIGN/DISTRIBUTE → tensor sharding annotations" while Table I pairs alignment with Mesh-TensorFlow and DISTAL.
D. Lacks insight: G5 ("model-state sharding is recorded from 2010; sparse partitions from 2020") and G6 ("partition propagation appears only in Era 6") are close to true by construction, because those tag values were introduced to describe those systems. Say so, or drop them.
E. Change: reconcile G8; regenerate Fig. 5 from read entries and Table I's pairs; expand §XII-B into the paper's central argument; add one paragraph on why the newer work does not cite the older.
F. Expect: the synthesis carries the thesis instead of the coding statistics.

### §XIII Open problems
A. Works: every item traces to a generalization and reports a test status; two are honestly "partly run".
B. Missing: a technical formulation for the ones that are open (e.g. "propagation under constraints": state the uniqueness question as a property of the rewrite system; "unified ownership IR": state what the IR must express).
C. Hard to read: two items ("wafer-scale", "productivity") are marked "run", so they are findings, not open problems.
D. Lacks insight: the list is "what we did not find in the read set" rather than "what the field cannot yet do".
E. Change: move the two closed items to §XII; formulate the remaining six as problems with a success criterion.
F. Expect: directions a PhD student could start on.

### §XIV Conclusion
A. Works: short.
B. Missing: an answer to the central question of §I-C; the thesis; what the taxonomy is for; what a practitioner should take away.
C. Hard to read: it is the abstract's second half, reworded.
D. Lacks insight: no synthesis beyond §XII.
E. Change: rewrite as answers to the RQs plus the one-paragraph thesis.
F. Expect: a reader who reads only abstract and conclusion learns the argument.

---

## Report D: Taxonomy and intellectual contribution audit

**Validity.** The eleven axes are defensible design dimensions (target, abstraction, decomposition, mapping, communication, boundary, architecture, objective, maturity, paper type, representation) and they are orthogonal in the sense that a system takes values on each. The axis refinement in §V-B is argued from cases and is the one place where the taxonomy is derived rather than declared. However, the paper never defines the values of the five axes it counts. Low exact-set agreement (41, 28, 32, 51, 15 percent) is the predictable result of uncodified values, and the paper treats it as a property of the field rather than of the codebook. Per Nickerson et al.'s criteria for a useful taxonomy (concise, robust, comprehensive, extendible, explanatory), the taxonomy is comprehensive and extendible (machine-readable, validated), is not concise (eleven axes, roughly 120 values, six drawn), and is explanatory only through §VII's separate three-class scheme, which is not the taxonomy.

**Novelty.** The decision-procedure split (directives, closed-form analysis, analytic optimisation, profile or search, runtime) and the partition-propagation value are useful and, as far as this reviewer can tell from the catalog, not present in the prior surveys the paper names. The rest of the axes resemble the organisation of Unat et al. 2017 and of the HPF-era overviews; that is acceptable, but the paper should say which axes are inherited and which are new.

**Consistency of application.** Not demonstrable from the paper; it is demonstrable from the repository. For a journal reader the codebook must be in the paper or an appendix.

**Does the taxonomy generate knowledge?** Partly. It generates G3, G4 and the decision-procedure counts (Table "decision", generated but not included). It does not yet explain relationships: nothing in §V says that closed-form owners imply static decisions and declared maps imply run-time stages; that argument lives in §VII and is the real taxonomic insight.

**Contributions claimed vs delivered (§I-E).**

| Claimed | Demonstrated | Evidence sufficient | Missing |
|---|---|---|---|
| 1. Operational definition and inclusion criteria | Yes (§I-B, §II-A) | Yes | Boundary cases (pipeline libraries, documentation sources) are handled ad hoc in §XI |
| 2. Reproducible method, open catalog | Yes (§II, §V-D, repository) | Yes | Threats to validity; disclosure of agent involvement |
| 3. Common architecture and taxonomy | Architecture yes; taxonomy partly | No for taxonomy | Value definitions, codebook, RQ mapping |
| 4. Six-era history in five parts; mechanism sections placing systems on axes | History yes; mechanism sections do not place systems on axes (they defer to §XII) | History yes | Mechanism sections do not deliver the stated function |
| 5. Then-and-now, six counted patterns, four causes, eight generalizations | Yes | Mostly | G8 inconsistent; G5/G6 weak; "six patterns" vs five in abstract |

**Present but under-emphasised.** (a) The citation column of Table I: almost no 2020s system cites the 1990s line. This is the paper's most striking empirical observation and it gets one sentence. (b) §XII-B: the claim that the program class (few large static-shape operators on homogeneous devices) is what made propagation and volume-only cost models possible, not better compiler technology. This is the explanatory core and is one paragraph. (c) §IX-C: compile-time decision is not the same as closed-form decision. (d) The withdrawal paragraph itself is a methodological contribution to how surveys report pattern claims.

---

## Report E: Insight and synthesis audit

| Section | Class | Evidence | Missing insight | Improvement |
|---|---|---|---|---|
| §I | A | Three questions; rebuilding thesis | Why the rebuilding happens (community separation? venue? abstraction gap?) | Hypothesis to test: the citation column of Table I correlates with venue community |
| §II | D (method) | Procedures | n/a | Add threats to validity |
| §III | D/C | Facts per card; §III-E synthesis | What the foundations lacked is stated; why they lacked it is not | One sentence: single address space made placement a non-problem |
| §IV | C | Pipeline with examples per stage | Which stage each era changed | Era × stage table |
| §V | A | §V-B argued refinement | Relationship between axes (C predicts F) | Move §VII-A's argument here |
| §VI | A | Measured numbers explain bets (startup cost → message count) | Why HPF's lessons were not transmitted | Pair with Table I's citation column |
| §VII | C | Three classes; "classes predict procedure" | Reconciliation of three competing groupings | One framework |
| §VIII | C | Element vs collective; volume-only cost follows | When collectives lose (irregular, heterogeneous) | State the limit of the collective model |
| §IX | C/A | Three forms; reuse condition decisive | Break-even across systems | Cost table |
| §X | A | Analytic vs measured with a stated test | n/a | Keep |
| §XI | D/C | Fact lists | Common-criteria comparison of 2020s systems | Table |
| §XII | S | Table I, four causes, G-table | Why no citation; why program class changed; what practitioners should do | Expand §XII-B and the citation discussion |
| §XIII | A | Derived gaps with status | Technical formulations | Formulate |
| §XIV | D | Repeats | Answers to RQs | Rewrite |

**Sections dominated by description:** §III, §XI, §XIV, and §IV, §VII, §VIII in their middle paragraphs. For each, the question "what does the reader learn that the cited papers do not give" is answered only by the closing inference sentence.

**Proposed analytical questions (hypotheses; validate before asserting):**
1. For §XI/§XII: is the absence of citation to the 1990s line explained by venue (ML systems conferences vs PLDI/SC) or by the abstraction gap (operators vs loops)? Testable from the catalog's venues and the citation column.
2. For §VII/§X: does the decision procedure (axis F) follow from the ownership class (closed-form, declared, propagated) in the read set? The paper asserts it in §VII-A; the catalog can count it.
3. For §VI/§XII: HPF's cause 4 (program-to-performance link) is said to be a design goal of PartIR. Is there any measured evidence that predictability was achieved? If not, say the cause is addressed in design, not in evidence.
4. For §VIII: at what point does a collective-only model lose to point-to-point generation? Kong et al. forbid such mappings; the sparse systems reintroduce point-to-point. That boundary is an insight the paper is one sentence away from.

---

## Report F: Clarity and narrative audit

**Argument reconstruction.** Problem (§I, strong) → Existing approaches (§III, §VI, strong) → Classification (§V, weak: declared not derived) → Comparisons (Table I strong; §VII–§XI weak: pointers) → Insights (§XII-B, §XII-D strong but short) → Gaps (§XIII adequate) → Conclusions (§XIV weak: repeats).

**Where the paper becomes a catalog:** §IV paragraphs, §VII-B/C, §VIII, §XI. **Where the reader loses the central question:** §V-D onward, whenever a paragraph opens with coding agreement rather than with the mechanism; §VII to §X refer the reader to §XII eleven times.

**Repetition.** The same facts appear in §VI, again in §VII–§XI, and again in Table I: Kali's on-clauses (§IV, §VI-B, §VII-C, Table I), Koelbel's closed forms (§IV, §VI-B, §VIII-A, Table I), GSPMD's propagation (§IV, §VI-F, §VII-A, §VIII-B, §XI-A, Table I), the 17-of-22 count (abstract, §IX, §XII-C, Table III, §XIV), "five to seven of the eleven Era 6 papers" (§VI-F, §X-E, §XIII).

**Difficult passages.**
- §II-D vs §II-C: reading level vs evidence level (see §II audit).
- §V-D: stale agreement numbers; reader who reaches §XII-C will think one of them is a typo.
- §VI intro: "Eras 0 and 1 have no full-text reads" vs §III.
- §VII-A: "The third class is propagated shardings ... Here the compiler needs the mesh and the propagation rules, not a table of owners" is clear, but the paragraph before it (declared maps) ends with "the owner of an element is data", which a reader may misparse as "is given data" rather than "is itself data".
- §IX first sentence: "the runtime pattern in Section XII states the central regularity, which holds in most cases under both codings and is not settled" is three qualifications before the claim.
- §XII-C "Search-based decomposition is rare before 2019": the paragraph spends 120 words on exceptions and then calls the claim "suggested"; a reader cannot tell whether to believe it.
- Hedging density: "under both codings" or "under the second coding" occurs more than 40 times in §VI, §X, §XII. Once the rule is stated (§XII-C), the phrase can be dropped from individual claims and carried by the table.

**Suggested reordering (warranted).**
1. Introduction (with RQ table, thesis, era definitions).
2. Methodology (with threats to validity and the coding rule).
3. Foundations (shortened).
4. Taxonomy, including the common architecture as its motivation and the codebook for the counted axes.
5. History in six eras (as now).
6. Mechanisms across eras: one section, three subsections for the three questions (ownership and mapping; communication and redistribution; the run-time stage and the decision procedure), each with a common-criteria table drawn from the systems table. This absorbs §VII–§XI.
7. Synthesis (Table I, three differences expanded, four causes, generalizations).
8. Open problems (six, formulated).
9. Conclusion (answers to RQs).
Rationale: the reader meets each mechanism once in history and once in comparison, the taxonomy is defined before it is used to count, and the synthesis follows directly from the comparison tables rather than from pointers.

---

## Report G: Top 10 problems

| Rank | Problem | Location | Severity | Why it matters | Recommended fix |
|---|---|---|---|---|---|
| 1 | Mechanism sections duplicate §VI and defer analysis to §XII | §VII–§XI (p.10–13) | Critical (contribution) | Four pages that claim to "place each system on the taxonomy's axes" (§I-E item 4) do not; the paper's comparative middle is missing | Merge into one comparative section with tables (Report F reordering) |
| 2 | Taxonomy values and coding rules are not in the paper | §V (p.4–5) | Critical (contribution) | The counted findings rest on tags a reader cannot interpret; low agreement is then attributed to the field | Codebook table for axes C, D, E, F, H; state coding rules; present agreement as validation |
| 3 | No common-criteria system comparison in the body; generated evaluation table unfilled | §XI, `paper/tables/table-b..e` | Major (analysis) | A survey of 28 systems without a systems table fails reader expectations; the generated tables also have a LaTeX escaping bug (`\textbackslash{}bullet`) and all-"?" evaluation cells | Curate Table B for the body; fill evaluation columns from cards; fix `generate_tables.py` escaping |
| 4 | Internal numeric and factual inconsistencies | Abstract (71), §V-D (26/20/20/52/6), G8 vs Table I paragraph, "eleven Era 6 papers" vs 15, §VI "no full-text reads" vs §III | Major (credibility) | A reviewer who finds one will distrust every count | Generate every count in the text from the catalog or check them in CI; reconcile G8 |
| 5 | Fig. 5 names four unread entries and pairs concepts differently from Table I | §XII-A Fig. 5 | Major (credibility) | Violates the paper's own evidence rule (§II-C) in its headline figure | Regenerate from read entries and Table I's pairs; align date ranges |
| 6 | Positive thesis buried under coding caveats | Abstract, §XII-C, §XIV | Major (contribution) | The abstract lists what did not survive; the explanatory insight (§XII-B) and the citation finding get one paragraph each | Lead with the thesis; expand §XII-B; discuss the citation column |
| 7 | Coverage gaps that touch claims | §VI-C (no PGHPF, xlhpf, ADAPTOR, VFC), §VI-D (Era 4 thin, X10 unread), §I (cites unread `callahan1988compiling`, `gropp1996mpich` as facts), vendor compilers absent | Major (coverage) | "Compilers were good on regular codes" rests on two compilers; the title promises AI systems the body excludes | Read or drop; mark dating-only citations as such; narrow the title or add the vendor documentation cards |
| 8 | RQ1–RQ10 promised, never listed or answered | §I-C, §V, §XIV | Moderate (structure) | The paper announces a research-question design and does not close it | RQ table in §I; answers in §XIV |
| 9 | Cross-era performance numbers quoted without normalisation | §VI (speedups vs hand code, vs sequential, utilisation) | Moderate (analysis) | Readers will compare 2.2 percent overhead, 62.5× over single GPU and 62 percent utilisation as if comparable | A short evaluation-practice table (baseline type, scale, metric) and one sentence of caution |
| 10 | Undisclosed role of agents in carding and second coding; superseded file cited | §V-D "agents drafting cards", §II-E | Moderate (method) | Methodological credibility depends on knowing who the "independent coder" is | One paragraph of disclosure in §II; replace the historical-claims reference |

Problems 1, 2, 6 undermine the contribution; 3, 5, 7, 9 weaken the analysis; 4, 8 reduce credibility and readability; 10 is editorial but necessary.

---

## Report H: Missing content and recommended additions

Discussions
- Why the 2020s systems do not cite the 1990s line (one subsection in §XII, hypothesis-labelled).
- Threats to validity (single author, agent-drafted cards, coder independence, Crossref-only search, paywalled Era 2–3 texts).
- What a practitioner should take from the survey (a half-page "choosing a mechanism" guide: closed-form owners when subscripts are affine; declared maps with a run-time stage when ownership is data; propagation when the program is an operator graph with static shapes).
- Which taxonomy axes are inherited from prior surveys and which are new.

Analyses
- Does ownership class predict decision procedure (axis C → axis F)? Countable now.
- Does the citation column correlate with venue community? Countable from catalog venues.
- Run-time stage overheads tabulated across Saltz, Kali, CHAOS, Titanium, Su, SpDISTAL.

Tables
- Systems on common criteria (curated from Table B): input, decomposition, mapping rule, communication family, decision procedure, run-time stage, target, evaluation baseline.
- Codebook: value, definition, coding rule, example card, for axes C, D, E, F, H.
- RQ → section → finding.
- Evaluation practice by era: baseline type, scale, metric, variance reported.
- Cost-model inputs per system (§X).

Figures
- Replace Fig. 5 with a figure of the thesis: the five-stage stack of Fig. 1 drawn once per machine class (hypercube, cluster, GPU node, accelerator pod, wafer) with the system that rebuilt each stage. Regenerate from read entries only.
- Redraw Fig. 3 with at most 25 events and legible type, or move it to the repository.
- Fig. 2: draw the five counted axes with their values and mark the values used in Table III.

Methodological elements
- Codebook (above).
- Search date range and the database list with hit counts (the roadmap already plans ACM DL and IEEE Xplore).
- Disclosure of agent involvement in card drafting and in the second coding.
- A coverage matrix (era × axis value) showing empty cells, which is also the honest form of the "claim about the read set, not the field" caveat the paper repeats.

Repository fixes that affect the paper
- `scripts/generate_tables.py` escapes `\bullet` as `\textbackslash{}bullet`; Tables C and D cannot be included until fixed.
- Table E (evaluation) is empty; the cards contain the data.
- `docs/historical-claims.md` is superseded but is cited in §II-E.

---

## Report I: Prioritised revision roadmap

### Phase 1: intellectual and structural

| # | Action | Priority | Effort | Impact | Depends on |
|---|---|---|---|---|---|
| 1.1 | Reconcile every count and figure with the catalog (abstract 71→78; §V-D agreement; G8; Era 6 "eleven"; §VI "no full-text reads"); add a CI check that greps the text for hard-coded counts | P0 | Small | High | none |
| 1.2 | Regenerate Fig. 5 from read entries and Table I's pairs, or drop it in favour of a thesis figure | P0 | Medium | High | 1.1 |
| 1.3 | Write the codebook for axes C, D, E, F, H and put it in §V or an appendix; present agreement as validation, not as the headline | P0 | Medium | High | none |
| 1.4 | Merge §VII–§XI into one comparative mechanisms section organised by the three questions, each with a common-criteria table | P0 | Large | High | 1.3, 2.1 |
| 1.5 | Rewrite abstract and §XIV around the thesis and the RQ answers; add the RQ table to §I | P0 | Medium | High | 1.4 |
| 1.6 | Expand §XII-B (program class, not compiler technology, changed) and add a subsection on the citation column | P1 | Medium | High | 1.2 |
| 1.7 | Decide the title's promise: either card the vendor compilers from official documentation or narrow "AI systems" to "sharding compilers" | P1 | Medium | Medium | none |
| 1.8 | Drop or relabel G5 and G6 as descriptive (true by construction of the tag values) | P1 | Small | Medium | 1.3 |

### Phase 2: technical and explanatory

| # | Action | Priority | Effort | Impact | Depends on |
|---|---|---|---|---|---|
| 2.1 | Fix `generate_tables.py` escaping; fill Table E from cards; curate Table B for the body | P1 | Medium | High | none |
| 2.2 | Read or obtain the HPF production compilers (PGHPF, xlhpf, ADAPTOR, VFC) and the unread core Era 2 entries (`zima1988superb`, `hiranandani1992compiling`, `koelbel1991compiling`, `das1994communication`) | P1 | Large | Medium | none |
| 2.3 | Run the axis C → axis F count and the venue vs citation count; report as hypotheses tested | P1 | Small | Medium | 1.3 |
| 2.4 | Run-time stage cost table (§IX) and cost-model inputs table (§X) | P2 | Medium | Medium | 1.4 |
| 2.5 | Evaluation-practice table and a caution paragraph on cross-era numbers | P2 | Small | Medium | 2.1 |
| 2.6 | Formulate the six genuinely open problems with success criteria; move the two "run" items to §XII | P2 | Small | Medium | 1.6 |
| 2.7 | Threats to validity and disclosure paragraph in §II; replace the historical-claims reference | P1 | Small | Medium | none |
| 2.8 | One worked example (a stencil and a matmul) traced through Fortran D, Legion or Pluto-dist, and GSPMD, showing what each compiler decides | P2 | Medium | High | 1.4 |

### Phase 3: presentation and editorial

| # | Action | Priority | Effort | Impact | Depends on |
|---|---|---|---|---|---|
| 3.1 | Reduce "under both codings" to the table and the rule statement; one caveat per paragraph at most | P2 | Medium | Medium | 1.4 |
| 3.2 | Redraw Fig. 3 (timeline) at legible scale or move it to the repository | P2 | Medium | Low | none |
| 3.3 | Fig. 2: draw the counted axes only, mark values used in Table III | P3 | Small | Low | 1.3 |
| 3.4 | Shorten §III-A to §III-D; move the bargain frame to §I | P3 | Small | Low | 1.5 |
| 3.5 | Fix the §IX opening sentence and the §II-D vs §II-C reading-level statement | P3 | Small | Low | none |
| 3.6 | Move repository bookkeeping sentences out of §XI into §II | P3 | Small | Low | 1.4 |

Suggested order: 1.1 → 1.3 → 2.1 → 1.4 → 1.2 → 1.6 → 1.5, with 2.2 and 2.7 in parallel.

---

## Report J: Final assessment

1. **Strongest intellectual contribution present.** Table I's then-and-now correspondence with its citation column, together with §XII-D's application of Kennedy, Koelbel and Zima's four causes to the sharding compilers. Behind both is §XII-B's explanation that the program class, not compiler technology, is what changed. The method (open catalog, two codings, refutable generalizations) is a contribution to how surveys are written in this field.

2. **Weakest aspect.** The middle of the paper. §VII–§XI promise to place systems on the taxonomy and instead restate §VI and point to §XII; there is no systems comparison table; and the taxonomy's values are never defined in the paper, so the counts that the paper then hedges cannot be interpreted by a reader.

3. **More descriptive than analytical?** Mixed. §VI and §XII are analytical and partly synthetic. §III, §IV, §VII–§IX, §XI and §XIV are descriptive or pointer-based. By page count the descriptive share is about half.

4. **Is the taxonomy useful?** Partly. The decision-procedure refinement and the partition-propagation value are useful and new relative to the named prior surveys. As presented in the paper the taxonomy is a figure and a list, not a defined instrument; its usefulness is demonstrated in the repository, not on the page.

5. **Three most important missing insights.**
   - Why the 2020s systems do not cite the 1990s line (community, venue, abstraction gap), which the paper's own data can test.
   - Whether ownership class predicts decision procedure, which would turn §VII's assertion into the taxonomy's central explanatory relationship.
   - Where collective-only communication models fail (irregular ownership, heterogeneous devices), which the sparse and wafer-scale cards already show and §VIII stops one sentence short of saying.

6. **Single highest-impact revision.** Merge §VII–§XI into one comparative mechanisms section built on common-criteria tables, and move the thesis of §XII-B to the front of the paper. This fixes structure, comparison and contribution delivery at once.

7. **What to do before rewriting paragraphs.** (a) Reconcile every number and figure with the catalog and add the check to CI. (b) Write the codebook for the five counted axes. (c) Fix the table generator and fill the evaluation table, so that the comparative section has material. (d) Decide the title's scope. Only then restructure.

---

### Strengths to preserve
- The five-part era narratives with quoted primary measurements (§VI).
- Table I and its citation column.
- Table III's "refuting observation" and "test" columns.
- The withdrawal paragraph (§XII-C) and the honesty of the method section.
- The precise, short-sentence prose.
