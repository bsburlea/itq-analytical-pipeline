# ============================================================
# 08_generate_diagrams.py
# FINAL aligned structural diagrams
# STRONG / MODERATE / WEAK arrows
# + spacing tweak
# + final alignment refinement
# ============================================================

from graphviz import Digraph
from pathlib import Path

OUTPUT_DIR = Path("data/diagrams")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# VISUAL SETTINGS
# ============================================================

ARROW_STYLES = {
    "STRONG": {"penwidth": "3"},
    "MODERATE": {"penwidth": "1.5"},
    "WEAK": {"penwidth": "0.7", "style": "dashed"},
}

NODE_STYLE = {
    "shape": "box",
    "style": "rounded",
    "fontname": "Helvetica",
}

# ============================================================
# BASE BLOCK DIAGRAM STRUCTURE
# (FINAL ALIGNMENT)
# ============================================================

def build_base_diagram(name: str):
    dot = Digraph(name=name, format="pdf")

    dot.attr(rankdir="LR")
    dot.attr(nodesep="0.9")
    dot.attr(ranksep="1.25")

    # --------------------------------------------------------
    # LEFT LAYER (Perfect vertical symmetry)
    # --------------------------------------------------------
    with dot.subgraph() as s:
        s.attr(rank="same")
        s.node("Personality", "Personality", **NODE_STYLE)
        s.node("Support", "Support / Context", **NODE_STYLE)

    # Invisible edge forces vertical alignment symmetry
    dot.edge("Personality", "Support", style="invis", weight="10")

    # --------------------------------------------------------
    # MIDDLE LAYER (Aligned mechanisms)
    # --------------------------------------------------------
    with dot.subgraph() as s:
        s.attr(rank="same")
        s.node("Task", "Task Effectiveness", **NODE_STYLE)
        s.node("Team", "Team Effectiveness", **NODE_STYLE)

    # Stress intentionally placed slightly lower
    dot.node("Stress", "Job Stress", **NODE_STYLE)

    # Invisible edges enforce visual balance
    dot.edge("Task", "Team", style="invis", weight="10")
    dot.edge("Team", "Stress", style="invis", weight="1")

    # --------------------------------------------------------
    # RIGHT LAYER
    # --------------------------------------------------------
    with dot.subgraph() as s:
        s.attr(rank="same")
        s.node("ITQ", "ITQ", **NODE_STYLE)

    return dot


# ============================================================
# HELPER TO ADD ARROWS
# ============================================================

def add_arrow(dot, src, dst, strength):
    style = ARROW_STYLES[strength]
    dot.edge(src, dst, **style)


# ============================================================
# MASTER ARROW DEFINITIONS
# ============================================================

def apply_personality_to_mechanisms(dot):
    add_arrow(dot, "Personality", "Stress", "STRONG")
    add_arrow(dot, "Personality", "Team", "STRONG")
    add_arrow(dot, "Personality", "Task", "MODERATE")
    add_arrow(dot, "Personality", "ITQ", "WEAK")


def apply_support_to_mechanisms(dot):
    add_arrow(dot, "Support", "Stress", "MODERATE")
    add_arrow(dot, "Support", "Team", "MODERATE")
    add_arrow(dot, "Support", "Task", "WEAK")


def apply_mechanisms_to_itq(dot):
    # STRONG pathway emphasized via edge weight
    dot.edge("Stress", "ITQ", penwidth="3", weight="6")
    add_arrow(dot, "Team", "ITQ", "MODERATE")
    add_arrow(dot, "Task", "ITQ", "WEAK")


# ============================================================
# DIAGRAM BUILDERS
# ============================================================

def build_stage_A():
    dot = build_base_diagram("stage_A")
    apply_mechanisms_to_itq(dot)
    return dot


def build_stage_B():
    dot = build_base_diagram("stage_B")
    apply_personality_to_mechanisms(dot)
    return dot


def build_stage_C():
    dot = build_base_diagram("stage_C")
    apply_personality_to_mechanisms(dot)
    apply_support_to_mechanisms(dot)
    apply_mechanisms_to_itq(dot)
    return dot


def build_stage_D():
    dot = build_base_diagram("stage_D")

    # emphasize emotional pathway
    dot.edge("Stress", "ITQ", penwidth="3", weight="6")
    add_arrow(dot, "Team", "ITQ", "MODERATE")

    return dot


def build_block_diagram():
    dot = build_base_diagram("block_diagram")

    add_arrow(dot, "Personality", "Stress", "MODERATE")
    add_arrow(dot, "Support", "Team", "MODERATE")

    dot.edge("Stress", "ITQ", penwidth="3", weight="6")
    add_arrow(dot, "Team", "ITQ", "MODERATE")
    add_arrow(dot, "Task", "ITQ", "WEAK")

    return dot


# ============================================================
# EXPORT
# ============================================================

def export_diagram(dot, filename):
    path = OUTPUT_DIR / filename
    dot.render(str(path), cleanup=True)
    print(f"Created: {path}.pdf")


# ============================================================
# MAIN
# ============================================================

def main():

    print("Generating FINAL aligned structural diagrams...")

    export_diagram(build_block_diagram(), "block_diagram_clean")
    export_diagram(build_stage_A(), "stage_A")
    export_diagram(build_stage_B(), "stage_B")
    export_diagram(build_stage_C(), "stage_C")
    export_diagram(build_stage_D(), "stage_D")

    print("Done.")


if __name__ == "__main__":
    main()
