"""
Parse coaching stint data from:
1. coaches.json mentor_context / holtz_connection fields
2. Research markdown files (chatgpt/*.md tables)
3. coaches.json hc_schools arrays

Merges into stints.json, deduplicating by ID.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent
coaches_path = BASE / "data/coaches.json"
stints_path = BASE / "data/stints.json"
relationships_path = BASE / "data/relationships.json"
research_dir = BASE / "research/chatgpt"

with open(coaches_path) as f:
    coaches = json.load(f)
with open(stints_path) as f:
    existing_stints = json.load(f)
with open(relationships_path) as f:
    relationships = json.load(f)

existing_ids = {s["id"] for s in existing_stints}

new_stints = []


def make_id(parts):
    """Generate a slug ID from parts."""
    slug = "-".join(str(p) for p in parts if p)
    slug = re.sub(r"[^a-z0-9-]", "", slug.lower().replace(" ", "-"))
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def school_slug(school):
    """Normalize school name to slug."""
    s = school.strip()
    s = re.sub(r"\s*\(.*?\)\s*", "", s)  # remove parentheticals for slug
    s = s.lower().replace(" ", "-").replace(".", "").replace("'", "")
    s = re.sub(r"[^a-z0-9-]", "", s)
    return s


def add_stint(stint):
    """Add stint if ID not already present."""
    sid = stint["id"]
    if sid not in existing_ids and sid not in {s["id"] for s in new_stints}:
        new_stints.append(stint)


def normalize_coach_id(name):
    """Convert a coach name to coach_id format."""
    name = name.strip()
    slug = name.lower().replace(" ", "-").replace(".", "").replace("'", "")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return slug


def parse_year_range(text):
    """Parse year ranges like '2001-2003', '2001-03', '2001'."""
    text = text.strip()
    # Handle "2001-2003, 2005-2006" -> take first range
    if "," in text:
        text = text.split(",")[0].strip()
    m = re.match(r"(\d{4})\s*[-–]\s*(\d{2,4})", text)
    if m:
        start = int(m.group(1))
        end_str = m.group(2)
        if len(end_str) == 2:
            end = int(str(start)[:2] + end_str)
        else:
            end = int(end_str)
        return start, end
    m = re.match(r"(\d{4})", text)
    if m:
        yr = int(m.group(1))
        return yr, yr
    return None, None


def role_to_slug(role_str):
    """Convert role description to role slug."""
    r = role_str.lower().strip()
    if "head coach" in r or r == "hc":
        return "head_coach"
    if "offensive coordinator" in r or r == "oc":
        return "offensive_coordinator"
    if "defensive coordinator" in r or r == "dc":
        return "defensive_coordinator"
    if "special teams" in r:
        return "special_teams_coordinator"
    if "graduate assistant" in r or r == "ga":
        return "graduate_assistant"
    if any(x in r for x in ["coach", "backs", "line", "end", "receiver", "quarterback",
                             "linebacker", "safety", "corner", "tight end", "running back"]):
        return "position_coach"
    if "coordinator" in r:
        return "coordinator"
    if "assistant" in r:
        return "assistant_coach"
    return "assistant_coach"


# ──────────────────────────────────────────────────────────────────────────────
# PHASE 1: Parse mentor_context / holtz_connection from coaches.json
# ──────────────────────────────────────────────────────────────────────────────

# Build mentor lookup from relationships
mentor_map = {}  # protege_id -> list of (mentor_id, school, years)
for rel in relationships:
    pid = rel["protege_id"]
    mid = rel["mentor_id"]
    if pid not in mentor_map:
        mentor_map[pid] = []
    mentor_map[pid].append(mid)

for coach_id, coach in coaches.items():
    context = coach.get("mentor_context") or coach.get("holtz_connection")
    if not context:
        continue

    # Parse entries like "DC at Notre Dame, 1987-89" or "DL at Notre Dame, 1995-96; DC at South Carolina, 1999-2002"
    entries = [e.strip() for e in context.split(";")]
    for entry in entries:
        # Match pattern: Role at School, Years
        m = re.match(r"(.+?)\s+at\s+(.+?),\s*(\d{4}.*?)$", entry)
        if not m:
            continue
        role_str = m.group(1).strip()
        school_name = m.group(2).strip()
        year_str = m.group(3).strip()

        year_start, year_end = parse_year_range(year_str)
        if not year_start:
            continue

        role = role_to_slug(role_str)

        # Determine head_coach_id from relationships or context
        mentor_id = None
        if coach_id in mentor_map:
            # Find mentor associated with this school
            for mid in mentor_map[coach_id]:
                for rel in relationships:
                    if rel["mentor_id"] == mid and rel["protege_id"] == coach_id:
                        if school_name.lower() in rel.get("school", "").lower():
                            mentor_id = mid
                            break
                if mentor_id:
                    break
        if not mentor_id:
            # Try to find from coach's mentor field
            mentor_slug = coach.get("mentor")
            if mentor_slug and mentor_slug in coaches:
                mentor_id = mentor_slug

        ss = school_slug(school_name)
        stint_id = make_id([coach_id, ss, role_str.lower().replace(" ", ""), str(year_start)])

        add_stint({
            "id": stint_id,
            "coach_id": coach_id,
            "school": school_name,
            "year_start": year_start,
            "year_end": year_end,
            "role": role,
            "role_detail": role_str,
            "head_coach_id": mentor_id,
            "confidence": "medium",
            "sources": ["coaches.json mentor_context"],
            "notes": None
        })


# ──────────────────────────────────────────────────────────────────────────────
# PHASE 2: Parse research markdown tables
# ──────────────────────────────────────────────────────────────────────────────

def parse_research_file(filepath):
    """Parse a research markdown file and extract stint data."""
    stints_found = []
    text = filepath.read_text()

    # Find section headers to determine the HC and school context
    # Patterns like "## USC", "### Notre Dame", "## New York Jets"
    sections = re.split(r"^(#{2,3})\s+(.+)$", text, flags=re.MULTILINE)

    current_school = None
    current_hc = None

    # Determine the HC from filename or first heading
    # Files are named like "01_pete_carroll.md" or "07_brian_kelly.md"
    fname = filepath.stem
    parts = fname.split("_", 1)
    if len(parts) == 2:
        hc_name_from_file = parts[1].replace("_", "-")
    else:
        hc_name_from_file = None

    # Check if this is a "deep" file or batch file
    is_deep = "deep" in fname
    is_batch = "batch" in fname or "gen3" in fname or "completeness" in fname

    i = 0
    while i < len(sections):
        part = sections[i]

        # Check if this is a heading marker
        if part in ("##", "###"):
            if i + 1 < len(sections):
                heading = sections[i + 1].strip()
                if is_batch and part == "##":
                    current_hc = normalize_coach_id(heading)
                    current_school = None
                elif is_batch and part == "###":
                    current_school = heading
                elif not is_batch:
                    current_school = heading
                    current_hc = hc_name_from_file
                i += 2
                continue
        # Look for markdown tables in this section
        if "|" in part:
            rows = part.strip().split("\n")
            table_rows = [r for r in rows if r.strip().startswith("|")]
            if len(table_rows) >= 3:  # header + separator + at least one data row
                # Parse header to find column indices
                header = [c.strip() for c in table_rows[0].split("|")]
                header = [h for h in header if h]  # remove empty strings

                for row in table_rows[2:]:  # skip header and separator
                    cols = [c.strip() for c in row.split("|")]
                    cols = [c for c in cols if c != ""]

                    if not cols or cols[0].lower() in ("none found", "none", ""):
                        continue
                    if len(cols) < 3:
                        continue

                    name = cols[0].strip().strip("*")
                    if name.lower() in ("none found", "none", "---", ""):
                        continue

                    # Find role and years columns
                    role_col = None
                    years_col = None
                    hc_stops_col = None
                    confidence_col = None

                    for idx, h in enumerate(header):
                        hl = h.lower()
                        if "role" in hl and idx < len(cols):
                            role_col = idx
                        if "year" in hl and idx < len(cols):
                            years_col = idx
                        if "later" in hl or "hc stop" in hl and idx < len(cols):
                            hc_stops_col = idx
                        if "confidence" in hl and idx < len(cols):
                            confidence_col = idx

                    if role_col is None:
                        role_col = 1 if len(cols) > 1 else None
                    if years_col is None:
                        years_col = 2 if len(cols) > 2 else None

                    if role_col is None or years_col is None:
                        continue
                    if role_col >= len(cols) or years_col >= len(cols):
                        continue

                    role_str = cols[role_col].strip()
                    years_str = cols[years_col].strip()
                    confidence = "medium"
                    if confidence_col and confidence_col < len(cols):
                        conf = cols[confidence_col].strip().lower()
                        if conf in ("high", "medium", "low"):
                            confidence = conf

                    year_start, year_end = parse_year_range(years_str)
                    if not year_start:
                        continue

                    coach_id = normalize_coach_id(name)
                    role_slug = role_to_slug(role_str)

                    # Only create stint if coach exists in our database
                    if coach_id not in coaches:
                        continue

                    hc_id = current_hc
                    school = current_school

                    if not school or not hc_id:
                        continue

                    ss = school_slug(school)
                    stint_id = make_id([coach_id, ss, str(year_start)])

                    stints_found.append({
                        "id": stint_id,
                        "coach_id": coach_id,
                        "school": school,
                        "year_start": year_start,
                        "year_end": year_end,
                        "role": role_slug,
                        "role_detail": role_str,
                        "head_coach_id": hc_id if hc_id in coaches else None,
                        "confidence": confidence,
                        "sources": [filepath.name],
                        "notes": None
                    })

        i += 1

    return stints_found


for md_file in sorted(research_dir.glob("*.md")):
    if md_file.name.startswith("_"):
        continue
    found = parse_research_file(md_file)
    for s in found:
        add_stint(s)


# ──────────────────────────────────────────────────────────────────────────────
# PHASE 3: Generate HC stints from hc_schools in coaches.json
# ──────────────────────────────────────────────────────────────────────────────

# Try to find year data from relationships and research for HC stints
# Build a lookup of known HC years from existing stints
known_hc_stints = set()
for s in existing_stints + new_stints:
    if s["role"] == "head_coach":
        known_hc_stints.add((s["coach_id"], school_slug(s["school"])))

for coach_id, coach in coaches.items():
    hc_schools = coach.get("hc_schools", [])
    for school in hc_schools:
        ss = school_slug(school)
        if (coach_id, ss) in known_hc_stints:
            continue
        # We don't have exact years, so mark as low confidence
        stint_id = make_id([coach_id, ss, "hc"])
        add_stint({
            "id": stint_id,
            "coach_id": coach_id,
            "school": school,
            "year_start": None,
            "year_end": None,
            "role": "head_coach",
            "role_detail": None,
            "head_coach_id": None,
            "confidence": "low",
            "sources": ["coaches.json hc_schools"],
            "notes": "Years not yet confirmed"
        })
        known_hc_stints.add((coach_id, ss))


# ──────────────────────────────────────────────────────────────────────────────
# MERGE AND WRITE
# ──────────────────────────────────────────────────────────────────────────────

all_stints = existing_stints + new_stints

with open(stints_path, "w") as f:
    json.dump(all_stints, f, indent=2)

# ──────────────────────────────────────────────────────────────────────────────
# REPORT
# ──────────────────────────────────────────────────────────────────────────────

print("=" * 70)
print("STINT PARSING REPORT")
print("=" * 70)

print(f"\nExisting stints:       {len(existing_stints)}")
print(f"New stints added:      {len(new_stints)}")
print(f"Total stints:          {len(all_stints)}")

# Breakdown by source
from collections import Counter
sources = Counter()
for s in new_stints:
    src = s["sources"][0] if s["sources"] else "unknown"
    sources[src] += 1
print(f"\nNew stints by source:")
for src, count in sources.most_common():
    print(f"  {src}: {count}")

# Breakdown by role
roles = Counter(s["role"] for s in new_stints)
print(f"\nNew stints by role:")
for role, count in roles.most_common():
    print(f"  {role}: {count}")

# Coaches with stints
coaches_with_stints = set(s["coach_id"] for s in all_stints)
coaches_without = set(coaches.keys()) - coaches_with_stints
print(f"\nCoaches with stints:   {len(coaches_with_stints)}")
print(f"Coaches without stints: {len(coaches_without)}")
if coaches_without:
    print("  Missing:")
    for c in sorted(coaches_without):
        print(f"    {c}")

print(f"\n{'─' * 70}")
