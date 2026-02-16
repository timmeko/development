#!/usr/bin/env python3
"""
Lou Holtz Coaching Tree — NetworkX + pyvis prototype visualization.

Reads coaches.json, stints.json, and relationships.json from data/
and produces an interactive HTML network graph.

Usage:
    python visualize.py              # outputs coaching_tree.html
    python visualize.py --static     # outputs coaching_tree.png (matplotlib)
"""

import json
import sys
from pathlib import Path

import networkx as nx

DATA_DIR = Path(__file__).parent / "data"


def load_data():
    with open(DATA_DIR / "coaches.json") as f:
        coaches = json.load(f)
    with open(DATA_DIR / "stints.json") as f:
        stints = json.load(f)
    with open(DATA_DIR / "relationships.json") as f:
        relationships = json.load(f)
    return coaches, stints, relationships


def count_hc_stints(coach_id, stints):
    """Count head coaching stints for a given coach."""
    return sum(
        1 for s in stints
        if s["coach_id"] == coach_id and s["role"] == "head_coach"
    )


def build_graph(coaches, stints, relationships):
    G = nx.DiGraph()

    for coach_id, info in coaches.items():
        hc_count = count_hc_stints(coach_id, stints)
        hc_schools = [
            s["school"] for s in stints
            if s["coach_id"] == coach_id and s["role"] == "head_coach"
        ]

        gen = info.get("generation", 99)
        label = info["name"]
        if hc_schools:
            label += f"\nHC: {', '.join(hc_schools)}"

        G.add_node(
            coach_id,
            label=label,
            name=info["name"],
            generation=gen,
            hc_count=hc_count,
            hc_schools=hc_schools,
            size=max(15, 10 + hc_count * 8),
        )

    for rel in relationships:
        mentor = rel["mentor_id"]
        protege = rel["protege_id"]
        if mentor not in G or protege not in G:
            continue

        edge_label = f"{rel['school']} {rel['year_start']}-{rel['year_end']}"
        G.add_edge(
            mentor,
            protege,
            label=edge_label,
            school=rel["school"],
            year_start=rel["year_start"],
            year_end=rel["year_end"],
            relationship_type=rel["relationship_type"],
            confidence=rel.get("confidence", "unknown"),
        )

    return G


# --- Color scheme by generation ---
GENERATION_COLORS = {
    -1: "#888888",  # upstream (Holtz's mentors)
    0: "#FFD700",   # Holtz himself (gold — ND)
    1: "#0C2340",   # Gen 1 — direct proteges (ND navy)
    2: "#00843D",   # Gen 2 — proteges of proteges
    3: "#AE9142",   # Gen 3
}


def render_pyvis(G, output="coaching_tree.html"):
    from pyvis.network import Network

    net = Network(
        height="900px",
        width="100%",
        directed=True,
        bgcolor="#1a1a2e",
        font_color="white",
        heading="Lou Holtz Coaching Tree",
    )
    net.barnes_hut(
        gravity=-3000,
        central_gravity=0.3,
        spring_length=200,
        spring_strength=0.05,
    )

    for node_id, data in G.nodes(data=True):
        gen = data.get("generation", 99)
        color = GENERATION_COLORS.get(gen, "#cccccc")
        size = data.get("size", 15)

        title_parts = [f"<b>{data['name']}</b>"]
        title_parts.append(f"Generation: {gen}")
        if data.get("hc_schools"):
            title_parts.append(f"HC at: {', '.join(data['hc_schools'])}")
        title = "<br>".join(title_parts)

        net.add_node(
            node_id,
            label=data.get("name", node_id),
            title=title,
            color=color,
            size=size,
            font={"size": 14, "color": "white"},
        )

    for u, v, data in G.edges(data=True):
        edge_color = "#666666"
        if data.get("confidence") == "high":
            edge_color = "#888888"
        elif data.get("confidence") == "medium":
            edge_color = "#555555"

        width = 2
        dashes = False
        if data.get("relationship_type") == "direct_report":
            width = 2.5

        # Thinner dashed lines for secondary mentorships (holdover coaches)
        notes = ""
        for rel in []:  # placeholder — could cross-ref relationship notes
            pass
        edge_title = data.get("label", "")

        net.add_edge(
            u, v,
            title=edge_title,
            color=edge_color,
            width=width,
            dashes=dashes,
            arrows="to",
        )

    net.set_options("""
    {
      "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "shape": "dot"
      },
      "edges": {
        "smooth": {
          "type": "continuous"
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "navigationButtons": true
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -3000,
          "centralGravity": 0.3,
          "springLength": 200,
          "springConstant": 0.05,
          "avoidOverlap": 0.5
        }
      }
    }
    """)

    net.save_graph(output)
    print(f"Interactive graph saved to {output}")
    return output


def render_static(G, output="coaching_tree.png"):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    node_colors = [
        GENERATION_COLORS.get(G.nodes[n].get("generation", 99), "#cccccc")
        for n in G.nodes()
    ]
    node_sizes = [G.nodes[n].get("size", 15) * 30 for n in G.nodes()]

    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color="#555555",
        arrows=True,
        arrowsize=15,
        width=1.5,
        alpha=0.7,
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_colors,
        node_size=node_sizes,
        edgecolors="white",
        linewidths=1.5,
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels={n: G.nodes[n]["name"] for n in G.nodes()},
        font_size=9,
        font_color="white",
        font_weight="bold",
    )

    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(
        G, pos, ax=ax,
        edge_labels=edge_labels,
        font_size=6,
        font_color="#aaaaaa",
    )

    ax.set_title(
        "Lou Holtz Coaching Tree",
        color="white", fontsize=18, fontweight="bold", pad=20,
    )
    # Legend
    legend_items = [
        ("Holtz (Gen 0)", GENERATION_COLORS[0]),
        ("Gen 1 — Direct proteges", GENERATION_COLORS[1]),
        ("Gen 2 — Proteges of proteges", GENERATION_COLORS[2]),
    ]
    for i, (text, color) in enumerate(legend_items):
        ax.plot([], [], "o", color=color, markersize=10, label=text)
    ax.legend(
        loc="lower left", facecolor="#2a2a3e", edgecolor="#555555",
        labelcolor="white", fontsize=9,
    )

    plt.tight_layout()
    plt.savefig(output, dpi=150, facecolor=fig.get_facecolor())
    print(f"Static graph saved to {output}")
    plt.close()
    return output


def main():
    coaches, stints, relationships = load_data()
    G = build_graph(coaches, stints, relationships)

    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    if "--static" in sys.argv:
        render_static(G)
    else:
        render_pyvis(G)


if __name__ == "__main__":
    main()
