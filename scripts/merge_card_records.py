#!/usr/bin/env python3
"""Merge structured card records (notes/paper-cards/_records/<id>.json) into catalog/papers.yaml.

Each record was written with its paper card from an owner-supplied PDF.  The merge
copies classification fields, summaries and evidence, sets status to 'read' and
records the metadata source.  It never sets verified; verification is a separate step.
Run again after more records appear; it is idempotent.
"""
import glob, json, os, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FIELDS = ("summary", "why_read", "main_contribution", "main_limitation", "evaluation_method", "benchmarks",
          "optimization_objectives", "data_decomposition", "computation_mapping", "communication_generation",
          "compiler_runtime_boundary", "target_hardware", "ir_representation", "compiler_architecture")
doc = yaml.safe_load(open("catalog/papers.yaml", encoding="utf-8"))
P = {p["id"]: p for p in doc["papers"]}
merged, skipped = [], []
for path in sorted(glob.glob("notes/paper-cards/_records/*.json")):
    rec = json.load(open(path, encoding="utf-8"))
    pid = rec.get("id")
    if pid not in P:
        skipped.append((pid, "no catalog entry")); continue
    p = P[pid]
    for k in FIELDS:
        if rec.get(k) not in (None, "", []):
            p[k] = rec[k]
    if rec.get("evidence"):
        p["evidence"] = rec["evidence"]
    if rec.get("states_relationship_to"):
        p["notes"] = ((p.get("notes") or "") + " Discusses: " + "; ".join(rec["states_relationship_to"]) + ".").strip()
    if rec.get("notes"):
        p["notes"] = ((p.get("notes") or "") + " " + rec["notes"]).strip()
    p["status"] = "read"
    p["metadata_sources"] = sorted(set((p.get("metadata_sources") or []) + ["full text read (paper card)"]))
    merged.append(pid)
yaml.safe_dump(doc, open("catalog/papers.yaml", "w", encoding="utf-8"), sort_keys=False, allow_unicode=True, width=110)
print("merged", len(merged), ":", " ".join(merged))
for s in skipped:
    print("skipped", s)
