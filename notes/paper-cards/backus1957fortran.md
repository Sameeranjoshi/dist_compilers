# The FORTRAN Automatic Coding System
**Catalog id:** `backus1957fortran`

**Citation:** J. W. Backus, R. J. Beeber, S. Best, R. Goldberg, L. M. Haibt, H. L. Herrick, R. A. Nelson, D. Sayre, P. B. Sheridan, H. Stern, I. Ziller, R. A. Hughes and R. Nutt. "The FORTRAN Automatic Coding System." 1957 Western Computer Proceedings, pp. 188-198, 1957. No DOI printed; catalog record used.

**Paper type:** foundational

**Access:** PDF supplied by the repository owner. Full text read (text layer complete on all 11 pages; the PDF metadata names ABBYY FineReader, so the text is OCR output).

**Card status:** full-read

## Problem

The paper reports the FORTRAN project, begun in 1954, which aimed to cut the effort of preparing scientific problems for the IBM 704 (Introduction, p. 188). The authors describe a language and a translator that turn algebraic statements into 704 programs. The paper does not discuss distributed memory, message passing or data placement across processors. Its target is a single processor.

## Input abstraction

The input is a FORTRAN source deck with one statement per card (Preparation, p. 191). The language has arithmetic, function, DO, IF, GO TO, READ, PRINT, FORMAT and DIMENSION statements, and subscripted variables with up to three subscripts (The FORTRAN Language, pp. 189-191). Within the translator, compiled instructions use a four-word symbolic format (translator Section 1, p. 192).

## Target

The object program runs on one IBM 704. The final translator section reduces it to the machine's three index registers (General Organization, p. 191; Section 5, p. 195). The output may be a list of input errors, a binary deck, a binary tape or a symbolic program (Translation, p. 191).

## Data decomposition

Not applicable in this paper. There is one processor and no distribution of arrays. DIMENSION statements declare array sizes (Examples 3 and 4, pp. 189-190). The storage discussed is index cells and index registers (translator Section 2, p. 194; Section 5, p. 195).

## Computation mapping

Not applicable in this paper. No work is mapped to processors. Translator Section 1 orders a formula's operations by level analysis and reorders them to reduce memory accesses (pp. 192-193). Section 2 places index computations at the outermost DO that allows it (p. 194). These are single-processor scheduling choices.

## Communication generation

Not applicable in this paper. There is no inter-processor communication. The only transfers are input-output calls and loop control on one processor (translator Section 1, p. 192).

## Compiler / runtime split

The translator runs on the 704 and performs almost all analysis before the object program runs (General Organization, pp. 191-192). DO-parameter decrement values are computed by the executive when constant, and by object instructions when variable (Section 2, p. 194). Section 4 simulates the program with branch outcomes weighted by programmer-supplied FREQUENCY statements (p. 195). This is best described as static with programmer directives.

## Evaluation

The paper reports no controlled benchmark. It reports one job: four hours to write 47 statements, six minutes to compile them into about 1000 instructions, and one correction (p. 188). Across the problems listed, output instructions per input statement and coding time per job both range from about 4 to 20 (Conclusion, p. 197). The authors state that FORTRAN programs are not normally appreciably longer than hand-coded ones (p. 197). No run times are given.

## Principal limitation

As stated, many language features were omitted from the description (p. 191). The authors also state that some efficiency techniques may be superfluous in many common applications (p. 198).

our observation: The efficiency claims rest on one case history and instruction-count ratios, not on measured run times of the generated code.

## Relationship to earlier / later work

The paper states that the object program can be written in SHARE symbolic language (translator Section 6, p. 191), and that a separate reference manual describes the full language (p. 191). It names no other compiler or system in the text, and it discusses no later work.

## Sources used

| claim | section / page |
|---|---|
| Project aim; one-job case history (47 statements, six minutes, about 1000 instructions) | Introduction, p. 188 |
| Language examples: DO, DIMENSION, subscripts, I/O, IF, GO TO | The FORTRAN Language, pp. 189-191 |
| One statement per card; output options | Preparation and Translation, p. 191 |
| Six translator sections; Section 5 reduces to three index registers | General Organization, pp. 191, 195 |
| Level analysis; reordering to reduce memory accesses | Translator Section 1, pp. 192-193 |
| Index registers for DO subscripts; executive-time decrement values | Translator Section 2, pp. 193-194 |
| Branch simulation weighted by FREQUENCY statements | Translator Sections 4-5, p. 195 |
| Program sizes; debugging by PRINT snapshots; ratios of 4 to 20 | Conclusion, pp. 196-197 |
| Instruction counts per section (table) | Conclusion, p. 198 |
| No distributed memory, message passing or data placement across processors | whole paper |
| Text of other papers at top of p. 188 and bottom of p. 198 (not used as evidence) | pp. 188, 198 |

## Open questions for the survey

- Should a single-processor translator with index-register optimization stay in the corpus as background, given that it has no parallel or distributed content?
- Which subscript and index-register techniques in translator Section 2 should be linked to later loop-level array work in the survey?
- Should the example programs be checked against the page images before quotation, since the text layer is OCR output?
