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
from matplotlib.patches import FancyArrowPatch
from matplotlib import font_manager

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_DIR   = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent

# ── Font setup ─────────────────────────────────────────────────────────────────
_granesta_path = DATA_DIR / "granesta" / "Granesta.ttf"
if _granesta_path.exists():
    font_manager.fontManager.addfont(str(_granesta_path))
    FONT_NAME = font_manager.FontProperties(fname=str(_granesta_path)).get_name()
else:
    FONT_NAME = "DejaVu Sans"

# Fallback for Arial Black — use Liberation Sans Bold or DejaVu Sans Bold
FONT_HC = "Liberation Sans"
_has_liberation = any("Liberation Sans" in f.name for f in font_manager.fontManager.ttflist)
if not _has_liberation:
    FONT_HC = "DejaVu Sans"

# ── Visual constants ───────────────────────────────────────────────────────────
BG = "#0d0d1a"

GEN_COLOR = {
    0: "#FFD700",   # Holtz — Notre Dame gold
    1: "#4A8FD4",   # Gen 1 — steel blue
    2: "#48C774",   # Gen 2 — emerald
    3: "#F0993A",   # Gen 3 — amber
}

HC_TEXT_COLOR = "#48C774"  # Green for HC position labels

RADII      = {0: 0.0, 1: 3.5, 2: 7.8, 3: 12.0}
FONT_SZ    = {0: 14,  1: 8.5, 2: 6.5, 3: 5.0}
HC_FONT_SZ = {0: 0,   1: 5.0, 2: 4.5, 3: 3.8}
EDGE_W     = {1: 1.4, 2: 0.9, 3: 0.5}
EDGE_A     = {1: 0.60, 2: 0.45, 3: 0.30}

# Gap between comb sections on each ring, expressed as a fraction of one coach-slot
GAP_SLOTS = 1.5

# Comb geometry: junction radius as fraction of the gap between parent and child ring
COMB_JUNCTION_FRAC = 0.60

# School label on comb trunks
SCHOOL_LABEL_SZ = 4.5
SCHOOL_LABEL_COLOR = "#48C774"

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
    "Tampa Bay":               "TB",
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
    "Arizona Cardinals":       "ARI",
}

# ── Known locations for context parsing ────────────────────────────────────────
KNOWN_LOCATIONS = [
    "Notre Dame", "Ohio State", "Florida", "Wisconsin", "Cincinnati",
    "Maryland", "NC State", "Bowling Green", "Utah", "Arkansas",
    "Minnesota", "South Carolina", "Texas", "Louisville", "Western Michigan",
    "Kent State", "UNLV", "USC", "LSU", "Ole Miss", "Rutgers",
    "New Mexico", "Iowa State", "Mississippi State", "Michigan State",
    "Grand Valley State", "Central Michigan", "Northern Illinois",
    "Houston", "Nevada", "UConn", "Eastern Michigan",
    # NFL
    "Tampa Bay", "Minnesota Vikings", "San Diego Chargers",
    "Seattle Seahawks", "NY Jets", "New York Jets", "Indianapolis Colts",
    "Chicago Bears", "Pittsburgh Steelers", "Baltimore Ravens",
    "Atlanta Falcons", "Jacksonville Jaguars", "Washington Redskins",
    "Washington", "Oakland Raiders", "Detroit Lions", "New England Patriots",
]

# Fallback mentoring location when context is vague
MENTOR_DEFAULT_LOCATION = {
    "monte-kiffin": "Tampa Bay",
}


# ── Helpers ────────────────────────────────────────────────────────────────────
_HOLTZ_DIRECT = "__holtz_direct__"   # virtual bucket for Gen-2 coaches directly under Holtz


def abb(school: str) -> str:
    s = school.replace(" (interim)", "").strip()
    return ABB.get(s, ABB.get(school, school))


def extract_mentor_schools(coach_id: str, coaches: dict) -> list:
    """Extract the school(s) where this coach was mentored, for comb grouping."""
    info = coaches[coach_id]
    gen = info.get("generation", 0)

    if gen == 1:
        ctx = info.get("holtz_connection", "")
        mentor_id = "lou-holtz"
    elif gen >= 2:
        ctx = info.get("mentor_context", "")
        mentor_id = info.get("mentor", "")
    else:
        return []

    mentor_info = coaches.get(mentor_id, {})
    parent_hc = mentor_info.get("hc_schools", [])

    if not ctx:
        # Check for default location
        default = MENTOR_DEFAULT_LOCATION.get(mentor_id)
        if default:
            return [default]
        return parent_hc[:1] if parent_hc else ["Unknown"]

    ctx_lower = ctx.lower()

    # Common abbreviations in context strings
    _ALIASES = {
        "New York Jets": ["ny jets", "new york jets"],
        "South Carolina": ["south carolina", "s. carolina"],
        "NC State": ["nc state", "n.c. state"],
    }

    # 1. Match against parent HC schools
    matched_hc = []
    for school in parent_hc:
        if school.lower() in ctx_lower:
            matched_hc.append(school)
            continue
        # Check aliases
        for alias in _ALIASES.get(school, []):
            if alias in ctx_lower:
                matched_hc.append(school)
                break

    # Handle slash-separated (e.g. "Florida/Ohio State")
    if "/" in ctx:
        for part in ctx.split("/"):
            part = part.strip()
            for school in parent_hc:
                if school.lower() in part.lower() and school not in matched_hc:
                    matched_hc.append(school)

    if matched_hc:
        return matched_hc

    # 2. No HC school matched — extract location from context
    matched_any = []
    for loc in KNOWN_LOCATIONS:
        if loc.lower() in ctx_lower:
            matched_any.append(loc)

    # Deduplicate substrings (keep longer match)
    deduped = []
    for m in matched_any:
        if not any(m != other and m in other for other in matched_any):
            deduped.append(m)
    if not deduped:
        deduped = matched_any

    if deduped:
        return deduped

    # 3. Fallback to mentor default or first HC school
    default = MENTOR_DEFAULT_LOCATION.get(mentor_id)
    if default:
        return [default]
    return parent_hc[:1] if parent_hc else ["Unknown"]


def extract_roles_by_school(ctx: str) -> dict:
    """
    Parse a holtz_connection or mentor_context string into {school: role}.

    Handles patterns like:
      "DC at Notre Dame, 1987-89"
      "WR/QB at Notre Dame, 1986-90; WR at Minnesota, 1984-85"
      "NFL Asst under Kiffin (Tampa Bay era)"
      "WR Coach on NY Jets, 1976"
    """
    if not ctx:
        return {}
    roles = {}
    clauses = [c.strip() for c in ctx.split(";")]
    for clause in clauses:
        # "ROLE at SCHOOL under MENTOR, YEARS" — strip the "under X" part
        cleaned = re.sub(r'\s+under\s+\w+', '', clause)

        # "ROLE at/on SCHOOL, YEARS"
        m = re.match(r'^(.+?)\s+(?:at|on)\s+(.+?)(?:,\s*\d{4}.*)?$', cleaned)
        if m:
            role = m.group(1).strip()
            school = m.group(2).strip()
            school = re.sub(r',\s*\d{4}.*$', '', school).strip()
            roles[school] = _normalise_role(role)
            continue

        # "ROLE under Mentor (LOCATION, YEAR)"
        m = re.match(r'^(.+?)\s+under\s+\w+\s*\(([^)]+)\)', clause)
        if m:
            role = m.group(1).strip()
            loc = m.group(2).strip()
            loc = re.sub(r',?\s*\d{4}.*$', '', loc).strip()
            loc = re.sub(r'\s+era$', '', loc).strip()
            roles[loc] = _normalise_role(role)
            continue

        # "ROLE under Mentor at SCHOOL, YEARS"
        m = re.match(r'^(.+?)\s+under\s+\w+\s+at\s+(.+?)(?:,\s*\d{4}.*)?$',
                     clause)
        if m:
            role = m.group(1).strip()
            school = m.group(2).strip()
            school = re.sub(r',\s*\d{4}.*$', '', school).strip()
            roles[school] = _normalise_role(role)
            continue

        # "ROLE under Mentor" (no location — use _default)
        m = re.match(r'^(.+?)\s+under\s+', clause)
        if m:
            role = m.group(1).strip()
            roles["_default"] = _normalise_role(role)
    return roles


def _normalise_role(role: str) -> str:
    """Shorten role titles for display: 'WR Coach' -> 'WR', etc."""
    r = role.strip()
    # Remove trailing "Coach" / "Coord" / "Coordinator"
    r = re.sub(r'\s+(Coach|Coord|Coordinator)$', '', r, flags=re.I)
    # Common abbreviations
    r = r.replace("Asst HC", "AHC").replace("Associate HC", "AHC")
    r = r.replace("Assistant", "Asst")
    return r


def primary_holtz_school(coach_id: str, coaches: dict) -> str:
    """For a Gen 1 coach, return their primary Holtz school for grouping."""
    schools = extract_mentor_schools(coach_id, coaches)
    # Prefer Notre Dame if present (it's the most significant Holtz stop)
    if "Notre Dame" in schools:
        return "Notre Dame"
    return schools[0] if schools else "Other"


def get_role_at_school(coach_id: str, school: str, coaches: dict) -> str:
    """Get a coach's role at a specific school from their connection context."""
    info = coaches[coach_id]
    ctx = info.get("holtz_connection", "") or info.get("mentor_context", "")
    roles = extract_roles_by_school(ctx)
    # Try exact match
    if school in roles:
        return roles[school]
    # Try alias match (e.g. "NY Jets" in ctx vs "New York Jets" in school name)
    for k, v in roles.items():
        if k.lower() in school.lower() or school.lower() in k.lower():
            return v
    # Fallback to _default
    return roles.get("_default", "")


def _year_range(ctx: str) -> str:
    """Extract compact year range from a context string, e.g. '1987-89'."""
    full_years = [int(y) for y in re.findall(r'\b((?:19|20)\d{2})\b', ctx)]
    # Handle 2-digit suffixes like "89" in "1987-89"
    for m in re.finditer(r'((?:19|20)\d{2})\s*-\s*(\d{2})\b', ctx):
        base_century = int(m.group(1)[:2])
        suffix = int(m.group(2))
        full_years.append(base_century * 100 + suffix)

    if not full_years:
        return ""

    mn, mx = min(full_years), max(full_years)
    if mn == mx:
        return str(mn)
    if mn // 100 == mx // 100:
        return f"{mn}-{mx % 100:02d}"
    return f"{mn}-{mx}"


def format_role_text(coach_id: str, coaches: dict) -> str:
    """
    Format role subtitle for the new label schema.

    Single-school:  "DC"
    Multi-school same role:  "OC at BG, Utah, Florida"
    Multi-school diff roles: "WR/QB at ND; WR at Minn, Ark"
    """
    info = coaches[coach_id]
    gen = info.get("generation", 0)
    if gen == 0:
        return ""

    ctx = info.get("holtz_connection", "") if gen == 1 else info.get("mentor_context", "")
    if not ctx:
        return ""

    roles_dict = extract_roles_by_school(ctx)
    if not roles_dict:
        return ""

    mentor_schools = extract_mentor_schools(coach_id, coaches)

    years = _year_range(ctx)

    if len(mentor_schools) <= 1:
        # Single school — include school name for gen 2+ to clarify tree placement
        school_roles = {k: v for k, v in roles_dict.items() if k != "_default"}
        role = ""
        if school_roles:
            role = list(school_roles.values())[0]
        else:
            role = roles_dict.get("_default", "")
        # For gen 2+, always show school name (e.g. "DC at Florida, 2005-09")
        school_label = ""
        if gen >= 2 and mentor_schools:
            school_label = abb(mentor_schools[0])
        if role and school_label:
            if years:
                return f"{role} at {school_label}, {years}"
            return f"{role} at {school_label}"
        if role and years:
            return f"{role}, {years}"
        return role

    # Multiple schools — build role-per-school map via mentor_schools
    role_per_school = {}
    for school in mentor_schools:
        role = get_role_at_school(coach_id, school, coaches)
        if role:
            role_per_school[school] = role

    if not role_per_school:
        all_roles = [v for k, v in roles_dict.items() if k != "_default"]
        role = all_roles[0] if all_roles else roles_dict.get("_default", "")
        if role and years:
            return f"{role}, {years}"
        return role

    # Group schools by role for compact display
    role_groups = {}
    for school, role in role_per_school.items():
        role_groups.setdefault(role, []).append(abb(school))

    if len(role_groups) == 1:
        role, schools = next(iter(role_groups.items()))
        result = f"{role} at {', '.join(schools)}"
    else:
        parts = []
        for role, schools in role_groups.items():
            parts.append(f"{role} at {', '.join(schools)}")
        result = "; ".join(parts)

    if years:
        result += f", {years}"
    return result


def earliest_year(ctx: str) -> int:
    """Extract the earliest 4-digit year from a context string."""
    years = [int(m) for m in re.findall(r'\b(19\d{2}|20[0-2]\d)\b', ctx)]
    return min(years) if years else 9999


def build_school_groups(mentor_id: str, child_gen: int, coaches: dict) -> dict:
    """
    Group proteges of mentor_id by the school where they were mentored.

    Returns: {school_name: [protege_ids]}
    """
    groups = {}
    for cid, info in coaches.items():
        if info.get("generation") != child_gen:
            continue
        # Gen 1 coaches don't have an explicit "mentor" field — all are Holtz proteges
        if child_gen == 1:
            if mentor_id != "lou-holtz":
                continue
        else:
            if info.get("mentor") != mentor_id:
                continue
        schools = extract_mentor_schools(cid, coaches)
        for school in schools:
            groups.setdefault(school, [])
            if cid not in groups[school]:
                groups[school].append(cid)
    return groups


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
        angle_map  : coach_id → raw layout angle
        group_spans: parent_id → (first_child_angle, last_child_angle)
    """
    nonempty = [(gid, cids) for gid, cids in groups_ordered if cids]
    N = sum(len(cids) for _, cids in nonempty)
    G = len(nonempty)
    if N == 0:
        return {}, {}, {}

    step = 2 * math.pi / (N + G * gap_slots)
    gap  = step * gap_slots

    pos_dict    = {}
    angle_map   = {}
    group_spans = {}

    angle = math.pi / 2   # 12 o'clock, proceeding clockwise

    for gid, cids in nonempty:
        first_a = last_a = None
        for cid in cids:
            a = angle - step / 2
            pos_dict[cid]  = (r * math.cos(a), r * math.sin(a))
            angle_map[cid] = a
            if first_a is None:
                first_a = a
            last_a = a
            angle -= step
        group_spans[gid] = (first_a, last_a)
        angle -= gap

    return pos_dict, angle_map, group_spans


def compute_positions(coaches: dict):
    """
    Equal-spacing radial layout with Gen 1 grouped by primary Holtz school.
    """
    # ── Gather generations ──────────────────────────────────────────────────
    gen1_all = [cid for cid, info in coaches.items() if info.get("generation") == 1]
    gen2_direct = [
        cid for cid, info in coaches.items()
        if info.get("generation") == 2 and info.get("mentor") == "lou-holtz"
    ]

    # Only keep Gen 1 coaches who have at least one Gen 2 protege (downstream tree)
    gen2_mentors = {
        info.get("mentor") for cid, info in coaches.items()
        if info.get("generation") == 2 and info.get("mentor")
    }
    gen1 = [cid for cid in gen1_all if cid in gen2_mentors]

    # ── Sort Gen 1 chronologically by earliest Holtz contact year ──────────
    def chrono_key(cid):
        return (earliest_year(coaches[cid].get("holtz_connection", "")), coaches[cid]["name"])

    gen1_sorted = sorted(gen1, key=chrono_key)

    # ── Group Gen 1 by primary Holtz school ────────────────────────────────
    # School order: chronological by Holtz's tenure
    HOLTZ_SCHOOL_ORDER = [
        "William & Mary", "NC State", "New York Jets",
        "Arkansas", "Minnesota", "Notre Dame", "South Carolina",
    ]

    school_buckets = {s: [] for s in HOLTZ_SCHOOL_ORDER}
    school_buckets["Other"] = []

    for cid in gen1_sorted:
        primary = primary_holtz_school(cid, coaches)
        if primary in school_buckets:
            school_buckets[primary].append(cid)
        else:
            school_buckets["Other"].append(cid)

    # Build Gen 1 groups ordered by Holtz school order
    gen1_groups_ordered = []
    for school in HOLTZ_SCHOOL_ORDER + ["Other"]:
        bucket = school_buckets.get(school, [])
        if bucket:
            gen1_groups_ordered.append((f"holtz-{school}", bucket))

    pos_g1, angle_map_g1, gen1_group_spans = assign_ring_positions(
        gen1_groups_ordered, RADII[1], gap_slots=1.0
    )

    # ── Build Gen 2 groups in Gen 1 placement order (clockwise) ─────────
    # Use the flattened gen1 placement order (already chronological) rather
    # than sorting by raw angle, which can wrap around with clockwise layout.
    gen1_by_angle = [cid for _, cids in gen1_groups_ordered
                     for cid in cids if cid in pos_g1]

    def chrono_key_g2(cid):
        return (earliest_year(coaches[cid].get("mentor_context", "")),
                coaches[cid]["name"])

    gen2_groups_ordered = []
    for g1 in gen1_by_angle:
        ch2 = sorted(children_of(g1, 2, coaches), key=chrono_key_g2)
        gen2_groups_ordered.append((g1, ch2))
    if gen2_direct:
        gen2_groups_ordered.append((_HOLTZ_DIRECT, sorted(gen2_direct, key=chrono_key_g2)))

    pos_g2, angle_map_g2, gen2_group_spans = assign_ring_positions(
        gen2_groups_ordered, RADII[2]
    )

    # ── Build Gen 3 groups in Gen 2 placement order (clockwise) ────────────
    gen2_by_angle = [cid for _, cids in gen2_groups_ordered
                     for cid in cids if cid in pos_g2]

    def chrono_key_g3(cid):
        return (earliest_year(coaches[cid].get("mentor_context", "")),
                coaches[cid]["name"])

    gen3_groups_ordered = []
    for g2 in gen2_by_angle:
        ch3 = sorted(children_of(g2, 3, coaches), key=chrono_key_g3)
        gen3_groups_ordered.append((g2, ch3))

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

    return (pos, angle_map, gen1_by_angle, gen1_groups_ordered,
            gen2_groups, gen3_groups)


# ── Rendering helpers ──────────────────────────────────────────────────────────

def _normalise_angle(a, reference):
    """Shift a into (reference - π, reference + π]."""
    while a < reference - math.pi:
        a += 2 * math.pi
    while a > reference + math.pi:
        a -= 2 * math.pi
    return a


def draw_school_comb(ax, pos, angle_map, parent_id,
                     school_groups, r_parent, r_children,
                     color, edge_w, edge_a,
                     junction_frac=COMB_JUNCTION_FRAC,
                     step_frac=0.65):
    """
    Draw school-grouped combs from a mentor to their proteges.

    school_groups: {school_name: [protege_ids]}
    Each school gets its own mini-comb with a perpendicular school label.
    Multi-school proteges get lines from multiple school combs.
    """
    if not school_groups or parent_id not in pos:
        return

    px, py = pos[parent_id]
    par_angle = math.atan2(py, px)
    r_junc = r_parent + (r_children - r_parent) * junction_frac

    # Collect all children with positions
    all_children_with_pos = set()
    for school, cids in school_groups.items():
        for cid in cids:
            if cid in pos and cid in angle_map:
                all_children_with_pos.add(cid)

    if not all_children_with_pos:
        return

    # If only one school or few total children, draw a simple comb
    # with a school label on the trunk
    total_schools = len([s for s, cids in school_groups.items()
                         if any(c in pos for c in cids)])

    if total_schools <= 1:
        # Single school: draw standard comb with school label
        school_name = list(school_groups.keys())[0]
        children = [c for c in school_groups[school_name] if c in pos]
        _draw_simple_comb(ax, pos, angle_map, parent_id, children,
                          r_parent, r_children, color, edge_w, edge_a,
                          junction_frac, step_frac, school_label=school_name)
        return

    # Multiple schools: draw separate mini-combs for each school
    # Sort schools by the average angle of their proteges
    school_list = []
    for school, cids in school_groups.items():
        valid = [(cid, angle_map[cid]) for cid in cids
                 if cid in pos and cid in angle_map]
        if valid:
            avg_angle = sum(a for _, a in valid) / len(valid)
            school_list.append((school, cids, avg_angle))

    school_list.sort(key=lambda x: x[2])

    # Draw each school's mini-comb at slightly different junction radii
    n_schools = len(school_list)
    for i, (school, cids, _) in enumerate(school_list):
        valid_cids = [c for c in cids if c in pos and c in angle_map]
        if not valid_cids:
            continue

        # Offset junction fraction slightly for each school to avoid overlap
        frac_offset = (i - (n_schools - 1) / 2) * 0.06
        jf = junction_frac + frac_offset
        jf = max(0.3, min(0.85, jf))

        _draw_simple_comb(ax, pos, angle_map, parent_id, valid_cids,
                          r_parent, r_children, color, edge_w, edge_a,
                          jf, step_frac, school_label=school)


def _draw_simple_comb(ax, pos, angle_map, parent_id, children,
                      r_parent, r_children, color, edge_w, edge_a,
                      junction_frac, step_frac, school_label=None):
    """
    Draw a comb from parent to children with optional school label.
    """
    if not children or parent_id not in pos:
        return

    px, py = pos[parent_id]
    par_angle = math.atan2(py, px)
    r_junc = r_parent + (r_children - r_parent) * junction_frac

    child_data = [
        (cid, angle_map[cid])
        for cid in children
        if cid in pos and cid in angle_map
    ]
    if not child_data:
        return

    child_data.sort(key=lambda x: x[1])

    CIRCUIT_THRESHOLD = 0.02
    trunk_w = edge_w + 0.2
    trunk_a = edge_a + 0.05

    def _circuit_board(target_angle, r_out, r_dest, norm_par_ref):
        # Segment 1 — radial from parent outward
        ax.plot([px, r_out * math.cos(norm_par_ref)],
                [py, r_out * math.sin(norm_par_ref)],
                color=color, alpha=trunk_a, linewidth=trunk_w,
                solid_capstyle="round", zorder=1)
        # Segment 2 — circular arc
        span = target_angle - norm_par_ref
        n = max(20, int(abs(span) * 30))
        ts = [norm_par_ref + span * i / (n - 1) for i in range(n)]
        ax.plot([r_out * math.cos(t) for t in ts],
                [r_out * math.sin(t) for t in ts],
                color=color, alpha=trunk_a, linewidth=trunk_w,
                solid_capstyle="round", zorder=1)
        # Segment 3 — radial to destination
        ax.plot([r_out * math.cos(target_angle), r_dest * math.cos(target_angle)],
                [r_out * math.sin(target_angle), r_dest * math.sin(target_angle)],
                color=color, alpha=trunk_a, linewidth=trunk_w,
                solid_capstyle="round", zorder=1)

    # ── Single-child case ─────────────────────────────────────────────────
    if len(child_data) == 1:
        cid, c_angle = child_data[0]
        cx, cy = pos[cid]
        norm_par = _normalise_angle(par_angle, c_angle)
        diff = abs(norm_par - c_angle)
        if diff > CIRCUIT_THRESHOLD:
            r_step = r_parent + (r_children - r_parent) * step_frac
            _circuit_board(c_angle, r_step, math.hypot(cx, cy), norm_par)
        else:
            ax.plot([px, cx], [py, cy],
                    color=color, alpha=edge_a, linewidth=edge_w,
                    solid_capstyle="round", zorder=1)

        # School label on the connecting line
        if school_label:
            child_r = math.hypot(cx, cy)
            if diff > CIRCUIT_THRESHOLD:
                # Circuit-board routing: place on the final radial segment
                r_step_lbl = r_parent + (r_children - r_parent) * step_frac
                label_r = (r_step_lbl + child_r) / 2
            else:
                # Straight line: midpoint
                label_r = (math.hypot(px, py) + child_r) / 2
            _draw_school_label(ax, label_r, c_angle, school_label)
        return

    # ── Multi-child: compute angular span ─────────────────────────────────
    theta_min = child_data[0][1]
    theta_max = child_data[-1][1]
    while theta_max < theta_min:
        theta_max += 2 * math.pi
    children_center_angle = (theta_min + theta_max) / 2
    norm_par = _normalise_angle(par_angle, children_center_angle)
    angle_diff = abs(norm_par - children_center_angle)

    r_step = r_parent + (r_junc - r_parent) * step_frac

    if angle_diff > CIRCUIT_THRESHOLD:
        _circuit_board(children_center_angle, r_step, r_junc, norm_par)
    else:
        jx = r_junc * math.cos(children_center_angle)
        jy = r_junc * math.sin(children_center_angle)
        ax.plot([px, jx], [py, jy],
                color=color, alpha=trunk_a, linewidth=trunk_w,
                solid_capstyle="round", zorder=1)

    # ── Arc bar ────────────────────────────────────────────────────────────
    n_arc = max(30, int(abs(theta_max - theta_min) * 40))
    arc_thetas = [theta_min + (theta_max - theta_min) * i / (n_arc - 1)
                  for i in range(n_arc)]
    ax.plot([r_junc * math.cos(t) for t in arc_thetas],
            [r_junc * math.sin(t) for t in arc_thetas],
            color=color, alpha=edge_a, linewidth=edge_w,
            solid_capstyle="round", zorder=1)

    # ── Teeth ──────────────────────────────────────────────────────────────
    for cid, c_angle in child_data:
        bx = r_junc * math.cos(c_angle)
        by = r_junc * math.sin(c_angle)
        cx, cy = pos[cid]
        ax.plot([bx, cx], [by, cy],
                color=color, alpha=edge_a, linewidth=edge_w,
                solid_capstyle="round", zorder=1)

    # ── School label on the arc bar ────────────────────────────────────────
    if school_label:
        _draw_school_label(ax, r_junc, children_center_angle, school_label)


def _draw_school_label(ax, r, angle, label, fontsize=None):
    """Draw a school name label tangential to the arc at the given position."""
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    # Tangential rotation = angle + 90°
    angle_deg = math.degrees(angle)
    tang_deg = angle_deg + 90
    # Normalize for readability
    if tang_deg > 90:
        tang_deg -= 180
    elif tang_deg < -90:
        tang_deg += 180

    # Offset slightly inward (toward center) so label doesn't overlap comb lines
    inward = 0.15
    lx = x - (x / (r or 1e-6)) * inward
    ly = y - (y / (r or 1e-6)) * inward

    ax.text(lx, ly, abb(label).upper(),
            fontsize=fontsize or SCHOOL_LABEL_SZ,
            fontfamily=FONT_HC,
            fontweight="bold",
            color=SCHOOL_LABEL_COLOR,
            alpha=0.85,
            ha="center", va="center",
            rotation=tang_deg, rotation_mode="anchor",
            bbox=dict(boxstyle="round,pad=0.08", fc=BG, ec="none", alpha=0.7),
            zorder=5)


def draw_node(ax, x, y, coach_id, coaches, gen):
    """Draw a coach node: Granesta name + role subtitle (new label schema)."""
    info = coaches[coach_id]
    name = info["name"]

    dist = math.hypot(x, y) or 1e-6
    angle_rad = math.atan2(y, x)
    angle_deg = math.degrees(angle_rad)

    if gen == 0:
        # Holtz at center — horizontal
        ax.text(0, -0.5, name,
                fontsize=FONT_SZ[0],
                fontfamily=FONT_NAME,
                color=GEN_COLOR[0],
                ha="center", va="top",
                zorder=4)
        hc_schools = info.get("hc_schools", [])
        if hc_schools:
            shorts = [abb(s) for s in hc_schools]
            hc_text = " · ".join(shorts)
            ax.text(0, -1.2, hc_text.upper(),
                    fontsize=HC_FONT_SZ[1],
                    fontfamily=FONT_HC,
                    fontweight="bold",
                    color=HC_TEXT_COLOR,
                    ha="center", va="top",
                    zorder=4)
        return

    # Determine text rotation and alignment based on which half of the circle
    right_side = -90 <= angle_deg <= 90
    if right_side:
        rot = angle_deg
        ha = "left"
    else:
        rot = angle_deg + 180 if angle_deg < 0 else angle_deg - 180
        ha = "right"

    # Offset inward from the ring so names don't overlap outward HC stubs
    off = -1.0
    lx = x + (x / dist) * off
    ly = y + (y / dist) * off

    # Role subtitle for all generations (label 2)
    role_text = format_role_text(coach_id, coaches)

    # Name in Granesta font, rotated radially (anchored inward, extends toward ring)
    ax.text(lx, ly, name,
            fontsize=FONT_SZ[gen],
            fontfamily=FONT_NAME,
            color="white",
            ha=ha, va="bottom",
            rotation=rot, rotation_mode="anchor",
            zorder=4)

    # Role text at same anchor, extending further inward
    if role_text:
        ax.text(lx, ly, role_text,
                fontsize=HC_FONT_SZ.get(gen, 3.8) - 0.5,
                fontfamily=FONT_HC,
                color=GEN_COLOR.get(gen, "#cccccc"),
                alpha=0.70,
                ha=ha, va="top",
                rotation=rot, rotation_mode="anchor",
                zorder=4)


HC_STUB_LEN  = {1: 0.7, 2: 0.5, 3: 0.3}
HC_STUB_FONT = {1: 4.0, 2: 3.5, 3: 3.0}
HC_STUB_W    = 0.5
HC_STUB_A    = 0.40


def draw_hc_stubs(ax, pos, angle_map, coaches):
    """Draw short outward HC-school stubs with perpendicular labels (label 3)."""
    for cid, (x, y) in pos.items():
        if cid not in coaches:
            continue
        info = coaches[cid]
        gen = info.get("generation", 99)
        if gen not in (2, 3):
            continue  # Skip Gen 1: their HC schools show as downstream comb labels

        hc_schools = info.get("hc_schools", [])
        if not hc_schools:
            continue

        dist = math.hypot(x, y) or 1e-6
        angle_rad = math.atan2(y, x)
        stub_len = HC_STUB_LEN.get(gen, 0.3)
        fs = HC_STUB_FONT.get(gen, 3.0)

        n_hc = len(hc_schools)
        # Angular fan for multiple stubs — small, proportional to count
        if n_hc == 1:
            stub_angles = [angle_rad]
        else:
            spread = min(0.03 * (n_hc - 1), 0.20)
            stub_angles = [
                angle_rad + spread * (i - (n_hc - 1) / 2) / max(n_hc - 1, 1)
                for i in range(n_hc)
            ]

        for school, sa in zip(hc_schools, stub_angles):
            # End point outward from the coach
            ex = x + stub_len * math.cos(sa)
            ey = y + stub_len * math.sin(sa)

            ax.plot([x, ex], [y, ey],
                    color=HC_TEXT_COLOR, alpha=HC_STUB_A, linewidth=HC_STUB_W,
                    solid_capstyle="round", zorder=1)

            # Place label directly at stub endpoint (not via origin-based polar)
            sa_deg = math.degrees(sa)
            tang_deg = sa_deg + 90
            if tang_deg > 90:
                tang_deg -= 180
            elif tang_deg < -90:
                tang_deg += 180
            ax.text(ex, ey, abb(school).upper(),
                    fontsize=fs,
                    fontfamily=FONT_HC,
                    fontweight="bold",
                    color=SCHOOL_LABEL_COLOR,
                    alpha=0.85,
                    ha="center", va="center",
                    rotation=tang_deg, rotation_mode="anchor",
                    bbox=dict(boxstyle="round,pad=0.08", fc=BG, ec="none", alpha=0.7),
                    zorder=5)


SECONDARY_COLOR = "#FF6B9D"   # Muted rose for secondary mentor lines
SECONDARY_W     = 0.4
SECONDARY_A     = 0.30
ARROW_SIZE      = 0.25        # Size of arrowhead triangle


def draw_secondary_connections(ax, pos, coaches, relationships):
    """Draw thin dashed arrows from secondary mentors to their proteges.

    Direction: mentor → protege (arrow points at the protege).
    Each arrow is a quadratic Bezier curve that bows toward the center
    with a small filled triangle arrowhead at the protege end.
    """
    # Build lookup: protege_id → list of mentor_ids from relationships.json
    mentor_map = {}
    for r in relationships:
        pid = r["protege_id"]
        mid = r["mentor_id"]
        mentor_map.setdefault(pid, set()).add(mid)

    drawn = set()  # avoid duplicate lines

    for cid, mentors in mentor_map.items():
        if cid not in pos or cid not in coaches:
            continue
        primary = coaches[cid].get("mentor")
        gen = coaches[cid].get("generation", 99)
        if gen not in (1, 2, 3):
            continue

        # For gen 1, primary mentor is always lou-holtz (implicit)
        if gen == 1:
            primary = "lou-holtz"

        for mid in mentors:
            if mid == primary:
                continue
            if mid not in pos:
                continue
            # Avoid duplicate lines (same pair in either direction)
            key = tuple(sorted([cid, mid]))
            if key in drawn:
                continue
            drawn.add(key)

            mx, my = pos[mid]    # mentor position (start)
            cx, cy = pos[cid]    # protege position (end / arrow tip)

            # Control point: midpoint pulled toward center
            mid_x = (mx + cx) / 2
            mid_y = (my + cy) / 2
            dist_from_center = math.hypot(mid_x, mid_y)
            if dist_from_center > 0.1:
                pull = 0.3
                ctrl_x = mid_x * (1 - pull)
                ctrl_y = mid_y * (1 - pull)
            else:
                ctrl_x, ctrl_y = mid_x, mid_y

            # Sample the quadratic Bezier curve (mentor → protege)
            n_pts = 40
            xs, ys = [], []
            for i in range(n_pts + 1):
                t = i / n_pts
                bx = (1 - t)**2 * mx + 2 * (1 - t) * t * ctrl_x + t**2 * cx
                by = (1 - t)**2 * my + 2 * (1 - t) * t * ctrl_y + t**2 * cy
                xs.append(bx)
                ys.append(by)

            # Shorten the curve slightly so arrow doesn't overlap the node dot
            # Stop at ~95% of the way to the protege
            stop = int(n_pts * 0.92)
            xs_draw = xs[:stop + 1]
            ys_draw = ys[:stop + 1]

            ax.plot(xs_draw, ys_draw,
                    color=SECONDARY_COLOR,
                    alpha=SECONDARY_A,
                    linewidth=SECONDARY_W,
                    linestyle=(0, (3, 4)),  # dashed
                    solid_capstyle="round",
                    zorder=0.5)

            # Draw arrowhead at the end pointing toward protege
            # Use the last two points of the drawn curve for direction
            if len(xs_draw) >= 2:
                dx = xs_draw[-1] - xs_draw[-2]
                dy = ys_draw[-1] - ys_draw[-2]
                length = math.hypot(dx, dy)
                if length > 0:
                    # Unit vector in arrow direction
                    ux, uy = dx / length, dy / length
                    # Perpendicular vector
                    px, py = -uy, ux

                    # Arrow tip at the end of the drawn curve
                    tip_x, tip_y = xs_draw[-1], ys_draw[-1]
                    # Two base points of the triangle
                    sz = ARROW_SIZE
                    b1x = tip_x - sz * ux + sz * 0.4 * px
                    b1y = tip_y - sz * uy + sz * 0.4 * py
                    b2x = tip_x - sz * ux - sz * 0.4 * px
                    b2y = tip_y - sz * uy - sz * 0.4 * py

                    arrow = plt.Polygon(
                        [[tip_x, tip_y], [b1x, b1y], [b2x, b2y]],
                        closed=True,
                        facecolor=SECONDARY_COLOR,
                        edgecolor="none",
                        alpha=SECONDARY_A + 0.1,
                        zorder=0.5,
                    )
                    ax.add_patch(arrow)


# ── Main render ────────────────────────────────────────────────────────────────
def render(coaches: dict, output_base: str = "coaching_tree_poster", relationships: list = None):
    (pos, angle_map, gen1_order, gen1_groups_ordered,
     gen2_groups, gen3_groups) = compute_positions(coaches)

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

    # ── Holtz → Gen 1: mini-combs per school group ─────────────────────────
    for gid, cids in gen1_groups_ordered:
        valid = [(c, angle_map[c]) for c in cids if c in pos and c in angle_map]
        if not valid:
            continue

        school_name = gid.replace("holtz-", "")
        trunk_w = EDGE_W[1] + 0.2
        trunk_a = EDGE_A[1] + 0.05

        if len(valid) == 1:
            # Single coach: straight line with school label
            cid, ca = valid[0]
            cx, cy = pos[cid]
            ax.plot([0, cx], [0, cy],
                    color=GEN_COLOR[1], alpha=EDGE_A[1], linewidth=EDGE_W[1],
                    solid_capstyle="round", zorder=1)
            _draw_school_label(ax, RADII[1] * 0.45, ca, school_name)
            continue

        # Multiple coaches: mini-comb (trunk → arc → teeth)
        valid.sort(key=lambda x: x[1])
        theta_min = valid[0][1]
        theta_max = valid[-1][1]
        center_angle = sum(a for _, a in valid) / len(valid)
        r_junc = RADII[1] * COMB_JUNCTION_FRAC

        # Trunk: center → junction at group center angle
        jx = r_junc * math.cos(center_angle)
        jy = r_junc * math.sin(center_angle)
        ax.plot([0, jx], [0, jy],
                color=GEN_COLOR[1], alpha=trunk_a, linewidth=trunk_w,
                solid_capstyle="round", zorder=1)

        # Arc bar spanning the group
        n_arc = max(30, int(abs(theta_max - theta_min) * 40))
        arc_thetas = [theta_min + (theta_max - theta_min) * i / (n_arc - 1)
                      for i in range(n_arc)]
        ax.plot([r_junc * math.cos(t) for t in arc_thetas],
                [r_junc * math.sin(t) for t in arc_thetas],
                color=GEN_COLOR[1], alpha=EDGE_A[1], linewidth=EDGE_W[1],
                solid_capstyle="round", zorder=1)

        # Teeth: arc → individual coaches
        for cid, ca in valid:
            bx = r_junc * math.cos(ca)
            by = r_junc * math.sin(ca)
            cx, cy = pos[cid]
            ax.plot([bx, cx], [by, cy],
                    color=GEN_COLOR[1], alpha=EDGE_A[1], linewidth=EDGE_W[1],
                    solid_capstyle="round", zorder=1)

        # School label on the trunk
        _draw_school_label(ax, r_junc, center_angle, school_name)

    # ── Gen 1 → Gen 2: school-grouped combs ───────────────────────────────
    active_g2 = [
        (g1, ch2) for g1, ch2 in gen2_groups.items()
        if g1 != _HOLTZ_DIRECT and g1 in pos and ch2
    ]
    active_g2.sort(key=lambda x: angle_map.get(x[0], 0))

    G12_STEP_MIN, G12_STEP_MAX = 0.25, 0.85
    G12_JUNC_MIN, G12_JUNC_MAX = 0.45, 0.80
    n12 = len(active_g2)

    # Draw Holtz-direct G2 coaches (straight lines from center)
    if _HOLTZ_DIRECT in gen2_groups:
        for g2 in gen2_groups[_HOLTZ_DIRECT]:
            if g2 not in pos:
                continue
            x2, y2 = pos[g2]
            ax.plot([0, x2], [0, y2],
                    color=GEN_COLOR[2], alpha=EDGE_A[2], linewidth=EDGE_W[2],
                    solid_capstyle="round", zorder=1)

    for i, (g1, ch2) in enumerate(active_g2):
        frac = i / max(1, n12 - 1)
        step_f = G12_STEP_MIN + frac * (G12_STEP_MAX - G12_STEP_MIN)
        junc_f = G12_JUNC_MIN + frac * (G12_JUNC_MAX - G12_JUNC_MIN)

        # Build school groups for this mentor
        sg = build_school_groups(g1, 2, coaches)

        draw_school_comb(
            ax, pos, angle_map,
            parent_id=g1, school_groups=sg,
            r_parent=RADII[1], r_children=RADII[2],
            color=GEN_COLOR[2],
            edge_w=EDGE_W[2], edge_a=EDGE_A[2],
            junction_frac=junc_f,
            step_frac=step_f,
        )

    # ── Gen 2 → Gen 3: school-grouped combs ───────────────────────────────
    active_g3 = [
        (g2, ch3) for g2, ch3 in gen3_groups.items()
        if ch3 and g2 in pos
    ]
    active_g3.sort(key=lambda x: angle_map.get(x[0], 0))

    G23_STEP_MIN, G23_STEP_MAX = 0.20, 0.82
    G23_JUNC_MIN, G23_JUNC_MAX = 0.40, 0.78
    n23 = len(active_g3)

    for i, (g2, ch3) in enumerate(active_g3):
        frac = i / max(1, n23 - 1)
        step_f = G23_STEP_MIN + frac * (G23_STEP_MAX - G23_STEP_MIN)
        junc_f = G23_JUNC_MIN + frac * (G23_JUNC_MAX - G23_JUNC_MIN)

        sg = build_school_groups(g2, 3, coaches)

        draw_school_comb(
            ax, pos, angle_map,
            parent_id=g2, school_groups=sg,
            r_parent=RADII[2], r_children=RADII[3],
            color=GEN_COLOR[3],
            edge_w=EDGE_W[3], edge_a=EDGE_A[3],
            junction_frac=junc_f,
            step_frac=step_f,
        )

    # ── Nodes & labels ────────────────────────────────────────────────────
    for cid, (x, y) in pos.items():
        if cid not in coaches:
            continue
        info = coaches[cid]
        gen = info.get("generation", 99)
        if gen > 3:
            continue
        draw_node(ax, x, y, cid, coaches, gen)

    # ── HC stubs (label 3 — outward HC school branches) ──────────────────
    draw_hc_stubs(ax, pos, angle_map, coaches)

    # ── Secondary mentor connections (dashed lines) ────────────────────
    if relationships:
        draw_secondary_connections(ax, pos, coaches, relationships)

    # ── Title ─────────────────────────────────────────────────────────────
    top = RADII[3] + 2.5
    ax.text(0, top, "Lou Holtz Coaching Tree",
            color="white", fontsize=24, fontweight="bold",
            fontfamily=FONT_NAME,
            ha="center", va="center", zorder=6)
    ax.text(0, top - 1.1,
            "Generations 0 – 3  ·  Role under mentor → HC stops as branches",
            color="#777788", fontsize=10,
            ha="center", va="center", zorder=6)

    # ── Legend ────────────────────────────────────────────────────────────
    handles = [
        mpatches.Patch(color=GEN_COLOR[0], label="Gen 0 — Lou Holtz"),
        mpatches.Patch(color=GEN_COLOR[1], label="Gen 1 — Direct protégés"),
        mpatches.Patch(color=GEN_COLOR[2], label="Gen 2"),
        mpatches.Patch(color=GEN_COLOR[3], label="Gen 3"),
        mpatches.Patch(color=SECONDARY_COLOR, alpha=SECONDARY_A + 0.2,
                       label="Secondary mentor link"),
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
    import sys
    with open(DATA_DIR / "coaches.json") as f:
        coaches = json.load(f)
    rels_path = DATA_DIR / "relationships.json"
    relationships = []
    if rels_path.exists():
        with open(rels_path) as f:
            relationships = json.load(f)
    print(f"Loaded {len(coaches)} coaches")
    render(coaches, relationships=relationships)


if __name__ == "__main__":
    main()
