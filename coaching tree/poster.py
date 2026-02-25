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
# Embed fonts as TrueType in PDF so text remains searchable/selectable
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype']  = 42
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

# Gap between comb sections on each ring, expressed as a fraction of one coach-slot
GAP_SLOTS = 1.5

# Comb geometry: junction radius as fraction of the gap between parent and child ring
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
    "Los Angeles Chargers":    "LAC",
    "Cleveland Browns":        "CLE",
    "Philadelphia Eagles":     "PHI",
    "Green Bay Packers":       "GB",
    "Arizona":                 "Ariz",
    "Tennessee Titans":        "TEN",
    "Cincinnati Bengals":      "CIN",
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


# ── Layout ─────────────────────────────────────────────────────────────────────
def assign_ring_positions(groups_ordered: list, r: float, gap_slots: float = GAP_SLOTS):
    """
    Place coaches on a ring of radius r, equally spaced, grouped by parent.

    groups_ordered: list of (parent_id, [child_ids])  — in desired angular order
    gap_slots: angular gap between groups expressed as multiples of one coach-slot

    Returns:
        pos_dict   : coach_id → (x, y)
        angle_map  : coach_id → raw layout angle (monotonically increasing, for comb drawing)
        group_spans: parent_id → (first_child_angle, last_child_angle)
    """
    nonempty = [(gid, cids) for gid, cids in groups_ordered if cids]
    N = sum(len(cids) for _, cids in nonempty)
    G = len(nonempty)
    if N == 0:
        return {}, {}, {}

    # step * N + gap * G = 2π,   gap = gap_slots * step
    step = 2 * math.pi / (N + G * gap_slots)
    gap  = step * gap_slots

    pos_dict    = {}
    angle_map   = {}
    group_spans = {}

    angle = math.pi / 2   # 12 o'clock, advancing counter-clockwise

    for gid, cids in nonempty:
        first_a = last_a = None
        for cid in cids:
            a = angle + step / 2
            pos_dict[cid]  = (r * math.cos(a), r * math.sin(a))
            angle_map[cid] = a
            if first_a is None:
                first_a = a
            last_a = a
            angle += step
        group_spans[gid] = (first_a, last_a)
        angle += gap

    return pos_dict, angle_map, group_spans


def compute_positions(coaches: dict):
    """
    Equal-spacing radial layout.

    Gen 1  — equally spaced, sorted chronologically.
    Gen 2  — equally spaced, grouped by Gen 1 parent in Gen 1 order, with inter-group gaps.
    Gen 3  — equally spaced, grouped by Gen 2 parent in Gen 2 angle order, with inter-group gaps.

    Returns:
        pos          : coach_id → (x, y)
        angle_map    : coach_id → raw layout angle (for comb drawing)
        gen1_order   : list of Gen 1 ids in layout order
        gen2_groups  : parent_id → [gen2_child_ids] in layout order
        gen3_groups  : parent_id → [gen3_child_ids] in layout order
    """
    # ── Gather generations ──────────────────────────────────────────────────
    gen1 = [cid for cid, info in coaches.items() if info.get("generation") == 1]
    gen2_direct = [
        cid for cid, info in coaches.items()
        if info.get("generation") == 2 and info.get("mentor") == "lou-holtz"
    ]

    # ── Sort Gen 1 chronologically by earliest Holtz contact year ──────────
    def chrono_key(cid):
        return (earliest_year(coaches[cid].get("holtz_connection", "")), coaches[cid]["name"])

    gen1_sorted = sorted(gen1, key=chrono_key)

    # ── Selective Gen 1 reordering to improve comb alignment ─────────────────
    # Charlie Strong's Gen-2 children cluster near Dean Pees's natural position;
    # swapping them brings the comb trunk much closer to its children.
    def _swap(lst, a, b):
        if a in lst and b in lst:
            i, j = lst.index(a), lst.index(b)
            lst[i], lst[j] = lst[j], lst[i]
    _swap(gen1_sorted, "charlie-strong", "dean-pees")

    # ── Gen 1 ring: all coaches equally spaced, one group (all connect to Holtz)
    gen1_groups_ordered = [("lou-holtz", gen1_sorted)]
    pos_g1, angle_map_g1, _ = assign_ring_positions(gen1_groups_ordered, RADII[1], gap_slots=0)

    # ── Build Gen 2 groups in Gen 1 order ────────────────────────────────────
    gen2_groups_ordered = []
    for g1 in gen1_sorted:
        ch2 = children_of(g1, 2, coaches)
        gen2_groups_ordered.append((g1, ch2))
    if gen2_direct:
        gen2_groups_ordered.append((_HOLTZ_DIRECT, gen2_direct))

    # ── Gen 2 ring: equally spaced with gaps between groups ──────────────────
    pos_g2, angle_map_g2, gen2_group_spans = assign_ring_positions(
        gen2_groups_ordered, RADII[2]
    )

    # ── Build Gen 3 groups ordered by Gen 2 parent's angle ───────────────────
    gen2_by_angle = sorted(pos_g2.keys(), key=lambda c: angle_map_g2[c])
    gen3_groups_ordered = []
    for g2 in gen2_by_angle:
        ch3 = children_of(g2, 3, coaches)
        gen3_groups_ordered.append((g2, ch3))

    # ── Gen 3 ring: equally spaced with gaps between groups ──────────────────
    pos_g3, angle_map_g3, gen3_group_spans = assign_ring_positions(
        gen3_groups_ordered, RADII[3]
    )

    # ── Assemble results ──────────────────────────────────────────────────────
    pos       = {"lou-holtz": (0.0, 0.0)}
    angle_map = {}

    pos.update(pos_g1)
    pos.update(pos_g2)
    pos.update(pos_g3)

    angle_map.update(angle_map_g1)
    angle_map.update(angle_map_g2)
    angle_map.update(angle_map_g3)

    gen2_groups = {gid: cids for gid, cids in gen2_groups_ordered}
    gen3_groups = {gid: cids for gid, cids in gen3_groups_ordered}

    return pos, angle_map, gen1_sorted, gen2_groups, gen3_groups


# ── Rendering helpers ──────────────────────────────────────────────────────────
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


def draw_comb(ax, pos, angle_map, parent_id,
              children, r_parent, r_children,
              color, edge_w, edge_a,
              junction_frac=COMB_JUNCTION_FRAC,
              step_frac=0.65):
    """
    Generic comb-style edges: trunk from parent → junction arc → teeth to each child.

    Works for any parent→children pair:
      - Gen 1 → Gen 2   (r_parent=RADII[1], r_children=RADII[2])
      - Gen 2 → Gen 3   (r_parent=RADII[2], r_children=RADII[3])

    Uses pre-computed raw layout angles (angle_map) to avoid atan2 wraparound issues.

    When the parent's radial angle is far from its children's angular centre, the trunk
    uses circuit-board routing: radial segment out → circular arc → radial segment to
    junction.  This avoids ugly diagonal lines and keeps "vertical" lines on radii and
    "horizontal" lines on circular arcs.
    """
    if not children or parent_id not in pos:
        return

    px, py     = pos[parent_id]
    par_angle  = math.atan2(py, px)   # parent's radial angle
    r_junc     = r_parent + (r_children - r_parent) * junction_frac

    # Collect children that have positions, keep them in their raw layout angle order
    child_data = [
        (cid, angle_map[cid])
        for cid in children
        if cid in pos and cid in angle_map
    ]
    if not child_data:
        return

    # Sort by raw layout angle (monotonically increasing — no wraparound ambiguity)
    child_data.sort(key=lambda x: x[1])

    # ── Shared threshold for circuit-board routing ────────────────────────────
    # Nearly every comb should route "out (radial) THEN over (arc)".
    # Only perfectly aligned trunks (< ~1°) skip circuit-board routing.
    CIRCUIT_THRESHOLD = 0.02  # radians (~1°)
    trunk_w = edge_w + 0.2
    trunk_a = edge_a + 0.05

    def _normalise_angle(a, reference):
        """Shift a into (reference - π, reference + π]."""
        while a < reference - math.pi:
            a += 2 * math.pi
        while a > reference + math.pi:
            a -= 2 * math.pi
        return a

    def _circuit_board(target_angle, r_out, r_dest, start_angle=None):
        """
        Draw a circuit-board trunk from the parent node to (r_dest, target_angle).

        r_out  : intermediate "horizontal arc" radius
        r_dest : final destination radius (e.g. r_junc or r_children for single child)
        start_angle : if None, starts from the parent node (px, py); otherwise
                      from (r_out, start_angle) and only draws the arc + final radial.
        """
        if start_angle is None:
            # Segment 1 — radial from parent outward to r_out along par_angle
            ax.plot([px, r_out * math.cos(norm_par)],
                    [py, r_out * math.sin(norm_par)],
                    color=color, alpha=trunk_a, linewidth=trunk_w,
                    solid_capstyle="round", zorder=1)
            a_from = norm_par
        else:
            a_from = start_angle

        # Segment 2 — circular arc at r_out from a_from → target_angle
        span = target_angle - a_from
        n    = max(20, int(abs(span) * 30))
        ts   = [a_from + span * i / (n - 1) for i in range(n)]
        ax.plot([r_out * math.cos(t) for t in ts],
                [r_out * math.sin(t) for t in ts],
                color=color, alpha=trunk_a, linewidth=trunk_w,
                solid_capstyle="round", zorder=1)

        # Segment 3 — radial from r_out to r_dest at target_angle
        ax.plot([r_out * math.cos(target_angle), r_dest * math.cos(target_angle)],
                [r_out * math.sin(target_angle), r_dest * math.sin(target_angle)],
                color=color, alpha=trunk_a, linewidth=trunk_w,
                solid_capstyle="round", zorder=1)

    # ── Single-child case ─────────────────────────────────────────────────────
    if len(child_data) == 1:
        cid, c_angle = child_data[0]
        cx, cy = pos[cid]
        norm_par_s = _normalise_angle(par_angle, c_angle)
        diff = abs(norm_par_s - c_angle)
        if diff > CIRCUIT_THRESHOLD:
            # Temporarily set norm_par so _circuit_board can reference it
            norm_par = norm_par_s
            r_step = r_parent + (r_children - r_parent) * step_frac
            _circuit_board(c_angle, r_step, math.hypot(cx, cy))
        else:
            ax.plot([px, cx], [py, cy],
                    color=color, alpha=edge_a, linewidth=edge_w,
                    solid_capstyle="round", zorder=1)
        return

    # ── Multi-child: compute angular span of children ─────────────────────────
    theta_min = child_data[0][1]
    theta_max = child_data[-1][1]

    while theta_max < theta_min:
        theta_max += 2 * math.pi

    children_center_angle = (theta_min + theta_max) / 2

    # Normalise par_angle into the same unwrapped frame as children_center_angle
    norm_par = _normalise_angle(par_angle, children_center_angle)

    angle_diff = abs(norm_par - children_center_angle)

    # ── Trunk: circuit-board or straight ─────────────────────────────────────
    # The trunk ALWAYS arrives at children_center_angle on the junction arc so
    # there is never a floating / orphaned segment disconnected from the arc bar.
    r_step = r_parent + (r_junc - r_parent) * step_frac

    if angle_diff > CIRCUIT_THRESHOLD:
        _circuit_board(children_center_angle, r_step, r_junc)
    else:
        # Straight trunk — but still land at children_center_angle, not par_angle,
        # so the endpoint is guaranteed to sit on the arc bar.
        jx = r_junc * math.cos(children_center_angle)
        jy = r_junc * math.sin(children_center_angle)
        ax.plot([px, jx], [py, jy],
                color=color, alpha=trunk_a, linewidth=trunk_w,
                solid_capstyle="round", zorder=1)

    # ── Arc bar at junction radius spanning all children ──────────────────────
    n_arc = max(30, int(abs(theta_max - theta_min) * 40))
    arc_thetas = [theta_min + (theta_max - theta_min) * i / (n_arc - 1)
                  for i in range(n_arc)]
    arc_xs = [r_junc * math.cos(t) for t in arc_thetas]
    arc_ys = [r_junc * math.sin(t) for t in arc_thetas]
    ax.plot(arc_xs, arc_ys,
            color=color, alpha=edge_a, linewidth=edge_w,
            solid_capstyle="round", zorder=1)

    # ── Teeth: junction arc → each child node ──
    for cid, c_angle in child_data:
        bx = r_junc * math.cos(c_angle)
        by = r_junc * math.sin(c_angle)
        cx, cy = pos[cid]
        ax.plot([bx, cx], [by, cy],
                color=color, alpha=edge_a, linewidth=edge_w,
                solid_capstyle="round", zorder=1)


def render(coaches: dict, output_base: str = "coaching_tree_poster"):
    pos, angle_map, gen1_order, gen2_groups, gen3_groups = compute_positions(coaches)

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

    # ── Holtz → Gen 1: straight radial lines with relationship label ──────────
    for g1 in gen1_order:
        if g1 not in pos:
            continue
        x1, y1 = 0.0, 0.0
        x2, y2 = pos[g1]
        ctx = short_ctx(coaches[g1].get("holtz_connection", ""))
        ax.plot([x1, x2], [y1, y2],
                color=GEN_COLOR[1], alpha=EDGE_A[1], linewidth=EDGE_W[1],
                solid_capstyle="round", zorder=1)
        draw_edge_label(ax, x1, y1, x2, y2, ctx, fs=4.8)

    # ── Gen 1 → Gen 2: comb edges ────────────────────────────────────────────
    # Sort active G1 parents by angle for consistent alternation.
    active_g2 = [
        (g1, ch2) for g1, ch2 in gen2_groups.items()
        if g1 != _HOLTZ_DIRECT and g1 in pos and ch2
    ]
    active_g2.sort(key=lambda x: angle_map.get(x[0], 0))

    # 4-lane cycle: each adjacent comb turns at a different radius AND has
    # a different junction height, so no two neighbours share geometry.
    G12_JFRACS = [0.50, 0.58, 0.66, 0.74]
    G12_SFRACS = [0.30, 0.47, 0.64, 0.81]

    # Draw Holtz-direct G2 coaches first (straight lines from center)
    if _HOLTZ_DIRECT in gen2_groups:
        for g2 in gen2_groups[_HOLTZ_DIRECT]:
            if g2 not in pos:
                continue
            x2, y2 = pos[g2]
            ctx = short_ctx(coaches[g2].get("mentor_context", ""))
            ax.plot([0, x2], [0, y2],
                    color=GEN_COLOR[2], alpha=EDGE_A[2], linewidth=EDGE_W[2],
                    solid_capstyle="round", zorder=1)
            draw_edge_label(ax, 0, 0, x2, y2, ctx, fs=4.2)

    for i, (g1, ch2) in enumerate(active_g2):
        lane = i % 4
        draw_comb(
            ax, pos, angle_map,
            parent_id=g1, children=ch2,
            r_parent=RADII[1], r_children=RADII[2],
            color=GEN_COLOR[2],
            edge_w=EDGE_W[2], edge_a=EDGE_A[2],
            junction_frac=G12_JFRACS[lane],
            step_frac=G12_SFRACS[lane],
        )

    # ── Gen 2 → Gen 3: comb edges ────────────────────────────────────────────
    # Sort active G2 parents by angle so we can assign alternating junction heights,
    # preventing adjacent combs from stacking their arc bars at the same radius.
    active_g3 = [
        (g2, ch3) for g2, ch3 in gen3_groups.items()
        if ch3 and g2 in pos
    ]
    active_g3.sort(key=lambda x: angle_map.get(x[0], 0))

    # 4-lane cycle: each adjacent comb turns at a different radius AND has
    # a different junction (arc-bar) height, avoiding line-on-line overlap.
    G23_JFRACS = [0.48, 0.56, 0.64, 0.72]
    G23_SFRACS = [0.28, 0.44, 0.60, 0.76]

    for i, (g2, ch3) in enumerate(active_g3):
        lane = i % 4
        draw_comb(
            ax, pos, angle_map,
            parent_id=g2, children=ch3,
            r_parent=RADII[2], r_children=RADII[3],
            color=GEN_COLOR[3],
            edge_w=EDGE_W[3], edge_a=EDGE_A[3],
            junction_frac=G23_JFRACS[lane],
            step_frac=G23_SFRACS[lane],
        )

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
            ax.text(0, -0.70, label,
                    fontsize=fs, color="white",
                    ha="center", va="top",
                    fontweight="bold", zorder=4)

        elif gen == 3:
            # Rotated radial labels
            angle_deg = math.degrees(math.atan2(y, x))
            if -90 <= angle_deg <= 90:
                rot = angle_deg
                ha  = "left"
            else:
                rot = angle_deg + 180 if angle_deg < 0 else angle_deg - 180
                ha  = "right"
            off = 0.30 + (ns ** 0.5) * 0.045
            lx  = x + (x / dist) * off
            ly  = y + (y / dist) * off
            ax.text(lx, ly, label,
                    fontsize=fs, color="white",
                    ha=ha, va="center",
                    rotation=rot, rotation_mode="anchor",
                    linespacing=1.25, zorder=4)

        else:
            # Gen 1 and Gen 2: horizontal labels, radially offset
            off = 0.30 + (ns ** 0.5) * 0.045
            lx  = x + (x / dist) * off
            ly  = y + (y / dist) * off
            ax.text(lx, ly, label,
                    fontsize=fs, color="white",
                    ha="center", va="center",
                    fontweight="bold" if gen == 1 else "normal",
                    linespacing=1.25, zorder=4)

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
