"""Shared helpers for the generation scripts."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
ASSETS = ROOT / "assets"
FIGDIR = ROOT / "paper" / "figures"


def load_yaml(name):
    with open(CATALOG / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def papers():
    return load_yaml("papers.yaml")["papers"]


def systems():
    return load_yaml("systems.yaml")["systems"]


def taxonomy():
    return load_yaml("taxonomy.yaml")


def eras():
    return load_yaml("eras.yaml")["eras"]


def paper_link(p):
    """Best official link for a paper, in the order required by the methodology."""
    if p.get("doi"):
        return f"https://doi.org/{p['doi']}"
    if p.get("arxiv"):
        return f"https://arxiv.org/abs/{p['arxiv']}"
    if p.get("official_url"):
        return p["official_url"]
    if p.get("pdf_url"):
        return p["pdf_url"]
    return None


def short_authors(p, max_names=2):
    names = [a.split()[-1] for a in p["authors"]]
    if len(names) <= max_names:
        return " and ".join(names) if len(names) == 2 else names[0]
    return f"{names[0]} et al."


def render_graph(g, stem):
    """Write assets/<stem>.svg and paper/figures/<stem>.pdf from a graphviz.Digraph."""
    ASSETS.mkdir(exist_ok=True)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    svg = g.pipe(format="svg")
    (ASSETS / f"{stem}.svg").write_bytes(svg)
    pdf = g.pipe(format="pdf")
    (FIGDIR / f"{stem}.pdf").write_bytes(pdf)
    print(f"wrote assets/{stem}.svg and paper/figures/{stem}.pdf")


def save_fig(fig, stem):
    ASSETS.mkdir(exist_ok=True)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(ASSETS / f"{stem}.svg", format="svg", bbox_inches="tight", metadata={"Date": None})
    fig.savefig(FIGDIR / f"{stem}.pdf", format="pdf", bbox_inches="tight", metadata={"CreationDate": None})
    print(f"wrote assets/{stem}.svg and paper/figures/{stem}.pdf")
