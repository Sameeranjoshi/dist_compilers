# Why Systolic Architectures?
**Catalog id:** `kung1982systolic`  
**Citation:** H. T. Kung. "Why Systolic Architectures?" IEEE Computer, January 1982, pp. 37-46. DOI 10.1109/mc.1982.1653825, taken from the catalog record (not printed on the pages read).  
**Paper type:** hardware  
**Access:** PDF supplied by the repository owner. No text layer; full text read from page images (PDF pages 1-10, printed pages 37-46).  
**Card status:** full-read

## Problem
The paper argues that ad hoc special-purpose systems are often limited by I/O bandwidth rather than cell speed (pp. 37-38). Its remedy is a systolic array, a pipeline of simple cells that reuses each fetched item (pp. 37, 39). A worked example caps a host-fed device at 5 million operations per second (p. 38, Figure 1).

## Input abstraction
The input is a mathematical definition rather than a program. The running example is the convolution y_i = w_1 x_i + ... + w_k x_{i+k-1} (p. 39). Designs are diagrams with cell equations (Figure 3b, p. 40; read from the image, high confidence), drawn for k = 3 (p. 40). The authors call a rigorous specification notation desirable (p. 45).

## Target
Special-purpose hardware built from VLSI chips and boards (pp. 37, 44). A single-chip cell should probably hold simple logic and few words; a board cell could hold an arithmetic unit and a few thousand words (p. 44). Distributed-memory machines are not discussed.

## Data decomposition
Placement is fixed by hand for each design, and no data is spread across processors. Weight-stationary designs preload one weight per cell (B1, F, W1, W2; pp. 40-42). Result-stationary designs keep each partial result in one cell (B2, R1, R2; pp. 40-41). B1 and B2 broadcast each x_i to all cells in one cycle (p. 40). No distributed-memory discussion.

## Computation mapping
Each design fixes which cell performs which products; the paper gives only rules of thumb for choosing (p. 42). In B1, the cell holding w_1 adds w_1 x_1 into y_1 in cycle one, and the cell holding w_2 adds w_2 x_2 into y_1 as it passes (p. 40). Concurrency comes from pipelining one result, computing many results at once, or both (p. 43). No distributed-memory discussion.

## Communication generation
No generator is described. Pure-systolic designs R1, R2, W1 and W2 move data only between neighboring cells (pp. 41-42). Designs B1, B2 and F use a global broadcast or fan-in, which the paper says is hard to extend as arrays grow (pp. 40-41). The paper says Leiserson and Saxe (ref. 42) can convert some such designs, without describing how (p. 45).

## Compiler / runtime split
Not applicable in this paper: there is no compiler, no runtime and no distributed-memory discussion. Control is a global clock (p. 44) and an optional systolic control path that selects weights from cell memories (p. 42). The user simply pumps in input and receives results (p. 44).

## Evaluation
The paper reports no experiments or measurements. Its evidence is analytic: the I/O-rate example and FFT I/O bound (p. 38), cell utilization and response time per design (pp. 41-42), and cell port counts (p. 43).

## Principal limitation
As the paper states it, automatic design of systolic structures is still an open question (p. 45). It also notes that global networks and large two-dimensional arrays are hard to scale (pp. 41, 44). Our observation: the designs are drawn by hand for k = 3 (p. 40), with no formal derivation procedure.

## Relationship to earlier / later work
The paper names these earlier links: the concept developed at Carnegie-Mellon (refs. 1-7; p. 37), design B1 proposed earlier for pattern matching and polynomial multiplication (refs. 16-20; p. 40), and W1 as a special case of a proposed filtering array (ref. 3; p. 42). It cites Weiser and Davis (ref. 27) and Leiserson and Saxe (ref. 42) for automatic-design progress (p. 45). It discusses no later work.

## Sources used
| claim | section / page |
|---|---|
| Title page: "Why Systolic Architectures?", H. T. Kung, Carnegie-Mellon University; January 1982 | p. 37 |
| Ad hoc special-purpose design; I/O and computation balance | pp. 37-38 |
| Systolic principle; cells, boundary I/O, compute-bound vs I/O-bound | p. 39 |
| I/O cap of 5 million operations per second | p. 38 |
| FFT I/O count and O(log S) speed-up bound (ref. 14); FFT split into S-point blocks with partial results sent to the host | p. 38; Figure 2, p. 39 |
| Convolution definition; k = 3 for illustrations | pp. 39-40 |
| Design B1: weights preloaded, x broadcast, y moves; cell accumulation timing | p. 40 |
| Design B2: y stays, w moves, tag bit, output bus | p. 40 |
| Design F: weights stay, x moves, fan-in adder | p. 41 |
| Global network wiring difficulty | p. 41 |
| Design R1: y stays, x and w move in opposite directions; about half of cells busy | p. 41 |
| Design R2: x moves twice as fast as w | pp. 41-42 |
| Design W1: w stays, x and y move in opposite directions; constant response | p. 42 |
| Design W2: x and y move in the same direction at different speeds | p. 42 |
| Cell memories, systolic control path, ESL processor (refs. 8, 10) | p. 42 |
| Concurrency sources; two-level pipelining | pp. 43-44 |
| Port counts: three for B1 and F, four for pure-systolic designs | p. 43 |
| Two-dimensional arrays, types R, H and T | p. 43 |
| Single-chip vs board cells; clock skew; global clock; user model | p. 44 |
| Application list (signal, matrix, non-numeric) | pp. 44-45 |
| Automatic design open; Leiserson and Saxe; specification notation; research directions | p. 45 |
| Reference list, latest entries dated January 1982 | p. 46 |
| Figure 1: memory-PE loop limited to 5 MOPS vs memory feeding six PEs labeled 30 MOPS possible | p. 38; high confidence on labels |
| Figure 2: 16-point FFT graph; decomposition into 4-point device blocks (n = 16, S = 4) | p. 39; high confidence |
| Figure 3: design B1 array and cell, with y_out ← y_in + w · x_in | p. 40; high confidence |
| Figure 4: design B2 array and cell; dashed bus collects outputs | p. 40; high confidence |
| Figure 5: design F array and cell; products fan in to an adder | p. 41; high confidence |
| Figure 6: design R1 array and cell; systolic output path drawn with broken arrows | p. 41; high confidence |
| Figure 7: design R2 array and cell; x and w in the same direction | p. 41; high confidence |
| Figure 8: design W1 array and cell; w stays, x and y oppose | p. 42; high confidence |
| Figure 9: design W2 array and cell; x and y in the same direction | p. 42; high confidence |
| Figure 10: design W1 with separate multiplier and adder, overlapped | p. 43; high confidence |
| Figure 11: two-dimensional arrays of types R, H and T | p. 43; high confidence |
| Figure 12: least-squares arrays with p = 4 (triangularization, then triangular solve) | p. 44; medium confidence on small labels |

## Open questions for the survey
- Which surveyed compilers make the stationary-operand choice explicit, and what cost criterion do they use (compare p. 42)?
- Do any surveyed compilers turn global communication into neighbor-only communication, as the paper says Leiserson and Saxe can (p. 45)?
- Which surveyed spatial-accelerator compilers keep the cell program and the data placement separate, as Kung's designs do (p. 40)?
