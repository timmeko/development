#!/usr/bin/env python3
"""
Lou Holtz Coaching Tree — Radial poster / shareable image generator.

Produces coaching_tree_poster.png (200 dpi) and coaching_tree_poster.pdf.

Usage:
    python poster.py
"""

import json
import math
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_DIR   = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent

# ── Visual constants ───────────────────────────────────────────────────────────
BG = "#0d0d1a"

GEN_COLOR = {
    0: "#FFD700",   # Holtz — Notre Dame gold
    1: "#4A8FD4",   # Gen 1 — steel blue
    2: "#48C774",   # Gen 2 — emerald
    3: "#F0993A",   # Gen 3 — amber
}

RADII      = {0: 0.0, 1: 3.5, 2: 7.8, 3: 14.0}
NODE_SZ    = {0: 280, 1: 110, 2: 55,  3: 26}
FONT_SZ    = {0: 11,  1: 7.5, 2: 6.0, 3: 4.8}
EDGE_W     = {1: 1.4, 2: 0.9, 3: 0.5}
EDGE_A     = {1: 0.60, 2: 0.45, 3: 0.30}
PAD        = 0.06   # sector edge padding fraction

# Comb geometry: junction radius as fraction between Gen 2 and Gen 3
COMB_JUNCTION_FRAC = 0.60

# ── School abbreviations ───────────────────────────────────────────────────────
ABB = {
    "Notre Dame":              "ND",
    "Ohio State":              "Ohio St",
    "Mississippi State":       "Miss St",
    "Florida":                 "Florida",
    "Wisconsin":               "Wisconsin",
    "Cincinnati":              "Cincy",
    "Maryland":                "Maryland",
    "Illinois":                "Illinois",
    "Indiana":                 "Indiana",
    "Michigan State":          "MSU",
    "Penn State":              "Penn St",
    "North Carolina":          "UNC",
    "NC State":                "NC St",
    "Colorado State":          "CSU",
    "Utah State":              "USU",
    "Arkansas State":          "Ark St",
    "Louisiana Tech":          "LA Tech",
    "East Carolina":           "ECU",
    "Western Michigan":        "W Mich",
    "Central Michigan":        "C Mich",
    "Northern Illinois":       "NIU",
    "Bowling Green":           "BG",
    "Georgia Tech":            "Ga Tech",
    "South Florida":           "USF",
    "South Carolina":          "SC",
    "Iowa State":              "Iowa St",
    "Texas A&M":               "TAMU",
    "Texas State":             "TX St",
    "Florida Atlantic":        "FAU",
    "Florida International":   "FIU",
    "Appalachian State":       "App St",
    "James Madison":           "JMU",
    "Miami (FL)":              "Miami",
    "Miami (OH)":              "Miami OH",
    "Jacksonville Jaguars":    "JAX",
    "Baltimore Ravens":        "BAL",
    "Pittsburgh Steelers":     "PIT",
    "Tampa Bay Buccaneers":    "TB",
    "Indianapolis Colts":      "IND",
    "Washington Redskins":     "WSH",
    "Washington Commanders":   "WSH",
    "New York Jets":           "NYJ",
    "New York Giants":         "NYG",
    "Kansas City Chiefs":      "KC",
    "Chicago Bears":           "CHI",
    "Houston Texans":          "HOU",
    "Atlanta Falcons":         "ATL",
    "San Diego Chargers":      "SD",
    "Detroit Lions":           "DET",
    "Oakland Raiders":         "OAK",
    "Las Vegas Raiders":       "LVR",
    "Minnesota Vikings":       "MIN",
    "Denver Broncos":          "DEN",
    "Carolina Panthers":       "CAR",
    "San Francisco 49ers":     "SF",
    "Seattle Seahawks":        "SEA",
    "Dallas Cowboys":          "DAL",
    "New England Patriots":    "NE",
    "New Orleans Saints":      "NO",
    "Buffalo Bills":           "BUF",
    "St. Louis Rams":          "STL",
    "Boston College":          "BC",
    "William & Mary":          "W&M",
    "New Mexico":              "UNM",
    "Grand Valley State":      "GVS",
    "Phoenix Cardinals":       "PHX",
    "Eastern Michigan":        "E Mich",
    "Southwest Minnesota State": "SMS",
    "Denver Broncos (interim)": "DEN",
    "Detroit Lions (interim)":  "DET",
    "Jacksonville Jaguars (interim)": "JAX",
    "Michigan State (interim)": "MSU",
    "Wisconsin (interim)":      "Wis",
    "Washington Redskins (interim)": "WSH",
    "New Orleans Saints (interim)": "NO",
    "Maryland (interim)":       "MD",
    "Arkansas (interim)":       "Ark",
    "Clemson (interim)":        "Clem",
    "East Carolina (interim)":  "ECU",
    "South Florida (interim)":  "USF",
    "UNLV":                    "UNLV",
    "Nevada":                  "Nevada",
    "McNeese State":           "McNeese",
    "Indiana State":           "Ind St",
    "Marshall":                "Marshall",
    "Connecticut":             "UConn",
    "Elon":                    "Elon",
    "Jackson State":           "Jkson St",
    "Mississippi Valley State":"Miss Val",
    "Bucknell":                "Bucknell",
    "Rutgers":                 "Rutgers",
    "Vanderbilt":              "Vandy",
    "Baylor":                  "Baylor",
    "Nebraska":                "Nebraska",
    "Youngstown State":        "YSU",
    "Liberty":                 "Liberty",
    "Auburn":                  "Auburn",
    "Ole Miss":                "Ole Miss",
    "Oregon":                  "Oregon",
    "Oregon State":            "Ore St",
    "USC":                     "USC",
    "Washington":              "UW",
    "Texas":                   "Texas",
    "Houston":                 "Houston",
    "LSU":                     "LSU",
    "Arkansas":                "Ark",
    "Kentucky":                "UK",
    "Louisville":              "UofL",
    "Duke":                    "Duke",
    "Syracuse":                "Syr",
    "Temple":                  "Temple",
    "Tulane":                  "Tulane",
    "Tulsa":                   "Tulsa",
    "Coastal Carolina":        "CCU",
    "Toledo":                  "Toledo",
    "Missouri":                "Mizzou",
    "Minnesota":               "Minn",
    "Utah":                    "Utah",
    "Hawaii":                  "Hawaii",
    "Rice":                    "Rice",
    "Air Force":               "AFA",
    "Clemson":                 "Clem",
    "Boise State":             "BSU",
    "Pittsburgh":              "Pitt",
    "Memphis":                 "Memphis",
    "Chattanooga":             "UTC",
    "Tennessee":               "Tenn",
    "IUP":                     "IUP",
    "Nevada (Reno)":           "UNR",
    "Millersville":            "Millersvl",
    "Eastern Illinois":        "EIU",
    "Tennessee Tech":          "TNTech",
    "Austin Peay":             "APSU",
    "Holy Cross":              "HC",
    "Alabama A&M":             "Ala A&M",
    "Northeast Louisiana":     "NE La",
    "Western Kentucky":        "WKU",
    "South Carolina State":    "SC St",
    "Middle Tennessee":        "MTSU",
    "North Texas":             "NT",
    "Kent State":              "Kent St",
    "UTSA":                    "UTSA",
    "FIU":                     "FIU",
    "Buffalo":                 "UB",
    "San Diego State":         "SDSU",
}

# ── Helpers ────────────────────────────────────────────────────────────────────
_HOLTZ_DIRECT = "__holtz_direct__"   # virtual bucket for Gen-2 coaches directly under Holtz


def abb(school: str) -> str:
    s = school.replace(" (interim)", "").strip()
    return ABB.get(s, ABB.get(school, school))


def node_label(coach_id: str, coaches: dict) -> str:
    info = coaches[coach_id]
    name = info["name"]
    hc   = [s for s in info.get("hc_schools", []) if s]
    if not hc:
        return name
    shorts = [abb(s) for s in hc]
    if len(shorts) > 3:
        shorts = shorts[:3] + [f"+{len(shorts) - 3}"]
    return f"{name}\n{', '.join(shorts)}"


def short_ctx(ctx: str) -> str:
    """First semicolon clause, ≤28 chars."""
    if not ctx:
        return ""
    first = ctx.split(";")[0].strip()
    return first[:28] + "…" if len(first) > 30 else first


def earliest_year(ctx: str) -> int:
    """Extract the earliest 4-digit year from a context string."""
    years = [int(m) for m in re.findall(r'\b(19\d{2}|20[0-2]\d)\b', ctx)]
    return min(years) if years else 9999


# ── Graph helpers ──────────────────────────────────────────────────────────────
def children_of(parent_id: str, child_gen: int, coaches: dict) -> list:
    """All coaches in child_gen whose primary mentor is parent_id."""
    return [
        cid for cid, info in coaches.items()
        if info.get("generation") == child_gen
        and info.get("mentor") == parent_id
    ]


def subtree_sz(gen1_id: str, coaches: dict) -> int:
    """Gen 2 + Gen 3 descendants of a Gen 1 coach."""
    g2 = children_of(gen1_id, 2, coaches)
    g3 = sum(len(children_of(g, 3, coaches)) for g in g2)
    return max(len(g2) + g3, 1)


# ── Layout ─────────────────────────────────────────────────────────────────────
def compute_positions(coaches: dict) -> dict:
    pos = {}
    pos["lou-holtz"] = (0.0, 0.0)

    # ── Gen 1: real proteges on inner ring ────────────────────────────────────
    gen1 = [cid for cid, info in coaches.items() if info.get("generation") == 1]

    # Gen 2 coaches whose mentor is Holtz directly (e.g. Ken Hatfield, Joe Gibbs)
    gen2_direct = [
        cid for cid, info in coaches.items()
        if info.get("generation") == 2 and info.get("mentor") == "lou-holtz"
    ]

    # Virtual node handles the direct-to-Holtz Gen 2 coaches as a sector block
    all_g1 = gen1 + ([_HOLTZ_DIRECT] if gen2_direct else [])

    sizes = {cid: subtree_sz(cid, coaches) for cid in gen1}
    if gen2_direct:
        g3_under = sum(len(children_of(g, 3, coaches)) for g in gen2_direct)
        sizes[_HOLTZ_DIRECT] = max(len(gen2_direct) + g3_under, 1)

    total = sum(sizes.values())

    # ── Sort Gen 1 chronologically by earliest Holtz contact year ─────────
    def chrono_key(cid):
        if cid == _HOLTZ_DIRECT:
            years = [earliest_year(coaches[c].get("mentor_context", ""))
                     for c in gen2_direct]
            return (min(years) if years else 9999, "")
        return (earliest_year(coaches[cid].get("holtz_connection", "")),
                coaches[cid]["name"])

    all_g1_sorted = sorted(all_g1, key=chrono_key)

    sectors1: dict = {}
    angle = math.pi / 2   # start at 12 o'clock, proceed counter-clockwise
    for cid in all_g1_sorted:
        span = (sizes[cid] / total) * 2 * math.pi
        sectors1[cid] = (angle, angle + span)
        angle += span

    r1 = RADII[1]
    for cid in gen1:
        a0, a1 = sectors1[cid]
        mid = (a0 + a1) / 2
        pos[cid] = (r1 * math.cos(mid), r1 * math.sin(mid))

    # ── Gen 2: placed within parent's sector ──────────────────────────────────
    sectors2: dict = {}
    r2 = RADII[2]

    def place_gen2(children2: list, a0: float, a1: float):
        if not children2:
            return
        g3c = {c: max(len(children_of(c, 3, coaches)), 1) for c in children2}
        total3 = sum(g3c.values())
        span  = a1 - a0
        inner_a = a0 + span * PAD
        inner_b = a1 - span * PAD
        inner_span = inner_b - inner_a
        cur = inner_a
        for c2 in sorted(children2, key=lambda x: g3c[x], reverse=True):
            sub = (g3c[c2] / total3) * inner_span
            sectors2[c2] = (cur, cur + sub)
            mid = cur + sub / 2
            pos[c2] = (r2 * math.cos(mid), r2 * math.sin(mid))
            cur += sub

    for g1 in gen1:
        place_gen2(children_of(g1, 2, coaches), *sectors1[g1])
    if gen2_direct:
        place_gen2(gen2_direct, *sectors1[_HOLTZ_DIRECT])

    # ── Gen 3: placed within parent Gen 2 sector ──────────────────────────────
    r3 = RADII[3]
    for g2, (a0, a1) in sectors2.items():
        children3 = children_of(g2, 3, coaches)
        if not children3:
            continue
        span   = a1 - a0
        inner_a = a0 + span * PAD
        inner_b = a1 - span * PAD
        n = len(children3)
        if n == 1:
            angles = [(inner_a + inner_b) / 2]
        else:
            angles = [inner_a + (inner_b - inner_a) * i / (n - 1) for i in range(n)]
        for c3, ang in zip(children3, angles):
            pos[c3] = (r3 * math.cos(ang), r3 * math.sin(ang))

    return pos


# ── Rendering ──────────────────────────────────────────────────────────────────
def draw_edge_label(ax, x1, y1, x2, y2, label, fs):
    if not label:
        return
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    deg = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if deg > 90:
        deg -= 180
    elif deg < -90:
        deg += 180
    ax.text(
        mx, my, label,
        fontsize=fs, color="#cccccc", alpha=0.80,
        ha="center", va="center",
        rotation=deg, rotation_mode="anchor",
        bbox=dict(boxstyle="round,pad=0.15", fc=BG, ec="none", alpha=0.75),
        zorder=5,
    )


def draw_comb(ax, pos, g2_id, children3, coaches):
    """Draw comb-style edges: trunk from Gen 2 → junction, arc bar, teeth → Gen 3."""
    if not children3:
        return

    x2, y2 = pos[g2_id]
    g2_angle = math.atan2(y2, x2)
    r_junc = RADII[2] + (RADII[3] - RADII[2]) * COMB_JUNCTION_FRAC
    color = GEN_COLOR[3]

    # Collect child angles (only those with positions)
    child_data = []
    for c3 in children3:
        if c3 not in pos:
            continue
        cx, cy = pos[c3]
        child_data.append((c3, math.atan2(cy, cx)))
    if not child_data:
        return

    child_data.sort(key=lambda x: x[1])

    if len(child_data) == 1:
        # Single child: just draw a straight line
        c3, _ = child_data[0]
        cx, cy = pos[c3]
        ax.plot([x2, cx], [y2, cy],
                color=color, alpha=EDGE_A[3], linewidth=EDGE_W[3],
                solid_capstyle="round", zorder=1)
        return

    # Junction point on the trunk (at parent angle)
    jx = r_junc * math.cos(g2_angle)
    jy = r_junc * math.sin(g2_angle)

    # ── Trunk: Gen 2 node → junction ──
    ax.plot([x2, jx], [y2, jy],
            color=color, alpha=EDGE_A[3] + 0.05, linewidth=EDGE_W[3] + 0.2,
            solid_capstyle="round", zorder=1)

    # ── Bar: smooth arc at r_junc from first to last child angle ──
    theta_min = child_data[0][1]
    theta_max = child_data[-1][1]
    n_arc = max(30, int(abs(theta_max - theta_min) * 40))
    if n_arc > 1:
        arc_thetas = [theta_min + (theta_max - theta_min) * i / (n_arc - 1)
                      for i in range(n_arc)]
        arc_xs = [r_junc * math.cos(t) for t in arc_thetas]
        arc_ys = [r_junc * math.sin(t) for t in arc_thetas]
        ax.plot(arc_xs, arc_ys,
                color=color, alpha=EDGE_A[3], linewidth=EDGE_W[3],
                solid_capstyle="round", zorder=1)

    # ── Teeth: junction arc → each Gen 3 node ──
    for c3, c_angle in child_data:
        bx = r_junc * math.cos(c_angle)
        by = r_junc * math.sin(c_angle)
        cx, cy = pos[c3]
        ax.plot([bx, cx], [by, cy],
                color=color, alpha=EDGE_A[3], linewidth=EDGE_W[3],
                solid_capstyle="round", zorder=1)


def render(coaches: dict, output_base: str = "coaching_tree_poster"):
    pos = compute_positions(coaches)

    unplaced = [cid for cid, info in coaches.items()
                if info.get("generation", 99) in (1, 2, 3) and cid not in pos]
    if unplaced:
        print(f"  WARNING: {len(unplaced)} coach(es) have no computed position: {unplaced}")

    fig, ax = plt.subplots(figsize=(24, 24))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_aspect("equal")
    ax.axis("off")

    # Subtle generation rings
    for gen, r in RADII.items():
        if r == 0:
            continue
        ring = plt.Circle((0, 0), r, fill=False, color="#ffffff",
                           alpha=0.05, linewidth=0.8, zorder=0)
        ax.add_patch(ring)

    # Ring generation labels
    ring_labels = {1: "Gen 1", 2: "Gen 2", 3: "Gen 3"}
    for gen, lbl in ring_labels.items():
        r = RADII[gen]
        ax.text(-r - 0.25, 0, lbl,
                fontsize=7, color="#555566", ha="right", va="center",
                fontstyle="italic", zorder=2)

    # ── Gen 1 & Gen 2 edges (straight lines with labels) ─────────────────────
    for cid, info in coaches.items():
        gen = info.get("generation", 99)
        if gen not in (1, 2):
            continue

        if gen == 1:
            mentor_id = "lou-holtz"
            ctx = short_ctx(info.get("holtz_connection", ""))
        else:
            mentor_id = info.get("mentor")
            if not mentor_id:
                continue
            ctx = short_ctx(info.get("mentor_context", ""))

        if mentor_id not in pos or cid not in pos:
            continue

        x1, y1 = pos[mentor_id]
        x2, y2 = pos[cid]

        ax.plot(
            [x1, x2], [y1, y2],
            color=GEN_COLOR[gen],
            alpha=EDGE_A[gen],
            linewidth=EDGE_W[gen],
            solid_capstyle="round",
            zorder=1,
        )

        draw_edge_label(ax, x1, y1, x2, y2, ctx,
                        fs=4.2 if gen == 2 else 4.8)

    # ── Gen 3 edges (comb style) ─────────────────────────────────────────────
    gen2_parents = set()
    for cid, info in coaches.items():
        if info.get("generation") == 3 and info.get("mentor"):
            gen2_parents.add(info["mentor"])

    for g2_id in gen2_parents:
        ch3 = children_of(g2_id, 3, coaches)
        if g2_id in pos:
            draw_comb(ax, pos, g2_id, ch3, coaches)

    # ── Nodes & labels ────────────────────────────────────────────────────────
    for cid, (x, y) in pos.items():
        if cid not in coaches:
            continue
        info = coaches[cid]
        gen  = info.get("generation", 99)
        if gen > 3:
            continue

        color = GEN_COLOR.get(gen, "#cccccc")
        ns    = NODE_SZ[gen]
        fs    = FONT_SZ[gen]

        ax.scatter(x, y, s=ns, c=color, zorder=3,
                   edgecolors="#ffffff",
                   linewidths=1.8 if gen == 0 else 0.6)

        label = node_label(cid, coaches)
        dist  = math.hypot(x, y) or 1e-6

        if gen == 0:
            # Holtz: label just below node
            ax.text(0, -0.70, label,
                    fontsize=fs, color="white",
                    ha="center", va="top",
                    fontweight="bold", zorder=4)

        elif gen == 3:
            # ── Rotated Gen 3 labels: follow radial angle ──
            angle_deg = math.degrees(math.atan2(y, x))
            if -90 <= angle_deg <= 90:
                rot = angle_deg
                ha = "left"
            else:
                rot = angle_deg + 180 if angle_deg < 0 else angle_deg - 180
                ha = "right"

            off = 0.30 + (ns ** 0.5) * 0.045
            lx  = x + (x / dist) * off
            ly  = y + (y / dist) * off
            ax.text(lx, ly, label,
                    fontsize=fs, color="white",
                    ha=ha, va="center",
                    rotation=rot, rotation_mode="anchor",
                    linespacing=1.25,
                    zorder=4)

        else:
            # Gen 1 and Gen 2: horizontal labels, radially offset
            off = 0.30 + (ns ** 0.5) * 0.045
            lx  = x + (x / dist) * off
            ly  = y + (y / dist) * off
            ax.text(lx, ly, label,
                    fontsize=fs, color="white",
                    ha="center", va="center",
                    fontweight="bold" if gen == 1 else "normal",
                    linespacing=1.25,
                    zorder=4)

    # ── Title ─────────────────────────────────────────────────────────────────
    top = RADII[3] + 2.5
    ax.text(0, top, "Lou Holtz Coaching Tree",
            color="white", fontsize=24, fontweight="bold",
            ha="center", va="center", zorder=6)
    ax.text(0, top - 1.1,
            "Generations 0 – 3  ·  Head coaching stops listed per coach",
            color="#777788", fontsize=10,
            ha="center", va="center", zorder=6)

    # ── Legend ────────────────────────────────────────────────────────────────
    handles = [
        mpatches.Patch(color=GEN_COLOR[0], label="Gen 0 — Lou Holtz"),
        mpatches.Patch(color=GEN_COLOR[1], label="Gen 1 — Direct proteges"),
        mpatches.Patch(color=GEN_COLOR[2], label="Gen 2"),
        mpatches.Patch(color=GEN_COLOR[3], label="Gen 3"),
    ]
    ax.legend(handles=handles, loc="lower left",
              facecolor="#1a1a2e", edgecolor="#333333",
              labelcolor="white", fontsize=10,
              framealpha=0.9)

    lim = RADII[3] + 4.0
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim - 0.5, lim)

    plt.tight_layout(pad=0.3)

    png = OUTPUT_DIR / f"{output_base}.png"
    pdf = OUTPUT_DIR / f"{output_base}.pdf"
    plt.savefig(png, dpi=200, facecolor=BG, bbox_inches="tight")
    print(f"  PNG → {png}")
    plt.savefig(pdf, facecolor=BG, bbox_inches="tight")
    print(f"  PDF → {pdf}")
    plt.close()


def main():
    with open(DATA_DIR / "coaches.json") as f:
        coaches = json.load(f)
    print(f"Loaded {len(coaches)} coaches")
    render(coaches)


if __name__ == "__main__":
    main()
