import sys
edits = {
"ramaswamy1996redistribution.md": [
("The paper gives a runtime method for moving a distributed array from one regular distribution to another, where the source and target may be different or overlapping processor sets (Sec. 1.1, Fig. 1). It is motivated by programs that change distributions between phases and by task-parallel pipelines in which an inter-task dependence forces a redistribution (Sec. 1.1). The authors argue that using distribution information directly beats the runtime resolution scheme, which computes each element's target at the source (Sec. 1.1, Sec. 2).",
 "A runtime method for moving a distributed array between regular distributions on different or overlapping processor sets (Sec. 1.1, Fig. 1). The authors motivate it with phase changes and task-parallel pipelines, and argue that it beats runtime resolution, which computes each element's target at the source (Sec. 1.1, Sec. 2)."),
("Multidimensional arrays are handled by intersecting the per-dimension sets (Sec. 3.4). Reshaping is excluded, and only whole arrays are redistributed (Sec. 1.1, Sec. 5).",
 "Multidimensional arrays are handled per dimension (Sec. 3.4)."),
("Each source intersects its FALLS with each target's FALLS, packs the result, and sends it; the target does the reverse (Sec. 3.3, Fig. 9).",
 "Sources intersect their FALLS with each target's FALLS, pack and send; targets unpack (Sec. 3.3, Fig. 9)."),
("- ScaLAPACK routine [15] is described as unclear for arbitrary processor sets, and the HPF runtime routines [17] treat source-target pairs individually with runtime resolution for general cases (Sec. 2).",
 "- The ScaLAPACK [15] and HPF runtime [17] routines are described as unclear for arbitrary processor sets or as pairwise (Sec. 2)."),
],
"koelbel1991regular.md": [
("Message-passing programs are hard to write because the programmer must insert every send and receive (Sec. 1). The paper gives explicit formulas",
 "Explicit message passing is hard to program. The paper gives formulas"),
(" The author states that the methods apply to any language with array distributions and forall statements (Sec. 1).", ""),
("The test program is cyclic reduction for a tridiagonal system, run on iPSC/860 for N = 10000 to 40000 and up to 32 processors (Fig. 5, Fig. 8).",
 "Cyclic reduction on iPSC/860, N = 10000 to 40000, up to 32 processors (Fig. 5, Fig. 8)."),
("- Run-time analysis is treated in [7] and [8], and the author's thesis [7] covers negative and zero coefficients (Sec. 2.5, Sec. 3.3).",
 "- The thesis [7] covers negative and zero coefficients (Sec. 3.3)."),
],
"chatterjee1993generating.md": [
("Two-level mappings reduce to two one-level problems (Sec. 3), and multidimensional arrays are handled per dimension (Sec. 4).",
 "Two-level and multidimensional cases reduce to one-level problems (Sec. 3, Sec. 4)."),
("The sender does the work. Each processor makes one pass over its local data, uses the state tables to find each element's destination, and sends one message per destination containing (address, value) pairs. Local iterations run from the message buffer (Sec. 5).",
 "Each processor makes one pass over its local data and sends one message per destination of (address, value) pairs; local iterations run from the message buffer (Sec. 5)."),
(" Communication time is not measured because it varies between machines (Sec. 6.2).", ""),
],
"rogers1994compiling.md": [
("Hand-written message-passing code is error-prone, so the paper proposes a compiler that takes a sequential program and a data decomposition and specializes the code for each process (Sec. I, Sec. II). Process decomposition is driven by data placement, not by program text (Abstract, Sec. II).",
 "The paper proposes a compiler that takes a sequential program and a data decomposition and specializes the code for each process, so that process decomposition follows data placement (Abstract, Sec. I, Sec. II)."),
("The examples use loops with step 1 (Sec. V), and the SIMPLE compiler handles only flat arrays (p. 294, note 7).",
 "The SIMPLE compiler handles only flat arrays (p. 294, note 7)."),
("Pipelining moves sends to the point where the value is ready, using mailbox numbers and, for array elements, a monotonicity condition (Sec. IX).",
 "Pipelining moves sends to where values are ready, using mailboxes (Sec. IX)."),
],
}
for fn, pairs in edits.items():
    path = "/home/user/notes/paper-cards/" + fn
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            print("MISS", fn, n, old[:60]); sys.exit(1)
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)
print("applied")
