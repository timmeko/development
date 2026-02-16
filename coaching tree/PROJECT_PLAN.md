# The Lou Holtz Coaching Tree Project

## Goal
Build a comprehensive, interactive network diagram centered on **Lou Holtz's
coaching tree** — tracing his upstream mentors (Woody Hayes, Forest Evashevski),
every staff member across his seven head coaching stops, and 2-3 generations of
downstream proteges. This naturally captures major sub-trees including Urban
Meyer's prolific branch, Barry Alvarez's Wisconsin lineage, and others.

---

## Scope

### Phase 1 — Data Collection
- Research distributed across agents (see RESEARCH_BRIEF.md):
  - Lou Holtz's own career path and upstream mentors
  - Complete staff rosters at all 7 HC stops (1969-2004)
  - Gen-1: Every Holtz protege who became a head coach + their full career
  - Gen-2: Their proteges who became HCs (e.g., Meyer's tree, Alvarez's tree)
  - Gen-3: One more level where data is available (e.g., Ryan Day's assistants)

### Phase 2 — Data Model & Validation
- Define JSON schema for coaches, stints, and relationships
- Ingest research into structured data files
- Cross-reference and validate against multiple sources
- Flag confidence levels and gaps

### Phase 3 — Visualization
- **Interactive network graph** (force-directed or hierarchical tree)
  - Nodes = coaches, sized by # of downstream proteges
  - Edges = mentorship relationships, labeled with school + years
  - Color-coded by coaching "family" / generation
  - Click a node to see full career timeline
- **Timeline view** — horizontal swim-lane showing a coach's career stops
- **Search & filter** — filter by school, conference, era, role type

---

## Design Decisions (Resolved)

| Question | Decision |
|----------|----------|
| **Depth threshold** | Coordinators + position coaches always. GAs/analysts where available, but don't let it block progress. |
| **Time boundary** | Holtz's full career (1960s-2004). Downstream traces as far as current day. |
| **NFL crossover** | Yes — include NFL stints (Holtz's Jets year, Meyer's Jaguars, proteges' NFL careers) |
| **Recursion depth** | 3 generations downstream from Holtz |
| **Visualization** | Start with Python/NetworkX prototype, then D3.js or Cytoscape.js for web |

---

## Data Sources (ranked by utility)

### Tier 1 — Structured / Semi-Structured
| Source | What it has | Access |
|--------|-------------|--------|
| **Wikipedia coach pages** | Career history tables with years, schools, roles | Free |
| **Sports-Reference.com** | Head coach records, school season pages | Free |

### Tier 2 — Rich but Requires Manual Extraction
| Source | What it has | Access |
|--------|-------------|--------|
| **Internet Archive media guides** | Full staff listings by year (gold standard) | Free PDFs |
| **University athletics sites** | Media guide archives, staff bios | Free |
| **Notre Dame Joyce Sports Collection** | 5,000+ physical media guides | Library access |
| **Newspaper archives** | Coaching hire/fire announcements | Varies |

### Tier 3 — Curated / Paid
| Source | What it has | Access |
|--------|-------------|--------|
| **McIllece Sports CFB Coaches Database** | Complete FBS staffs, 2005-2025 | Paid |
| **CBS / ESPN / SI coaching tree articles** | Narrative summaries | Free |

---

## Tech Stack

### Data Layer
- **JSON flat files** (version-controlled, easy to inspect and contribute to)
- **Schema**: `coaches.json` (nodes) + `stints.json` (career stops) + `relationships.json` (edges)
- Graduate to SQLite or Neo4j if the dataset outgrows flat files

### Visualization
- **Phase 1**: Python + NetworkX + pyvis for rapid prototyping
- **Phase 2**: D3.js or Cytoscape.js for interactive web experience

---

## Data Schema (Draft)

```json
// coaches.json
{
  "lou-holtz": {
    "name": "Lou Holtz",
    "born": 1937,
    "birthplace": "Follansbee, WV",
    "current_status": "retired",
    "alma_mater": "Kent State",
    "generation": 0
  },
  "urban-meyer": {
    "name": "Urban Meyer",
    "born": 1964,
    "current_status": "retired",
    "alma_mater": "Cincinnati",
    "generation": 1
  }
}

// stints.json
[
  {
    "coach_id": "urban-meyer",
    "school": "Notre Dame",
    "year_start": 1996,
    "year_end": 1996,
    "roles": ["wide_receivers_coach"],
    "head_coach_id": "lou-holtz",
    "confidence": "medium",
    "notes": "Exact years and role progression need verification"
  }
]

// relationships.json
[
  {
    "mentor_id": "woody-hayes",
    "protege_id": "lou-holtz",
    "context": "Ohio State 1968",
    "relationship_type": "direct_report",
    "generation_gap": -1
  },
  {
    "mentor_id": "lou-holtz",
    "protege_id": "urban-meyer",
    "context": "Notre Dame ~1996",
    "relationship_type": "direct_report",
    "generation_gap": 1
  }
]
```

---

## Task Breakdown

### Phase 1 — Data Collection
- [x] Define project scope and approach
- [x] Create research brief for distributed data collection (RESEARCH_BRIEF.md)
- [ ] Collect Holtz upstream lineage data
- [ ] Collect Holtz staff rosters (all 7 stops)
- [ ] Collect Gen-1 protege career data
- [x] **Bob Davie tree** — ND coordinators 1997-2001, 6 assistants-turned-HCs identified
- [ ] Collect remaining Gen-1 protege career data (Alvarez, Skip Holtz, etc.)
- [ ] Collect Gen-2 protege career data (Meyer tree, Alvarez tree, etc.)
- [ ] Collect Gen-3 protege data (where available)

### Phase 2 — Data Model & Ingestion
- [x] Create JSON data files (`data/coaches.json`, `stints.json`, `relationships.json`)
- [x] Seed with Davie tree research (11 coaches, 30 stints, 10 relationships)
- [ ] Ingest additional research rounds as they complete
- [ ] Validate and cross-reference data

### Phase 3 — Visualization
- [x] Build NetworkX + pyvis prototype (`visualize.py`)
- [x] Interactive HTML output (`coaching_tree.html`) — force-directed, hover tooltips, dark theme
- [x] Static PNG output (`coaching_tree.png`) — matplotlib fallback
- [ ] Build interactive web visualization (D3 or Cytoscape)

---

## File Index

| File | Purpose |
|------|---------|
| `PROJECT_PLAN.md` | This file — project overview and status |
| `RESEARCH_BRIEF.md` | Detailed spec for data collection (hand to research agents) |
| `data/coaches.json` | Coach node data — 11 coaches seeded from Davie tree |
| `data/stints.json` | Career stint data — 30 stints across all seeded coaches |
| `data/relationships.json` | Mentor-protege edges — 10 relationships including dual-mentorship paths |
| `visualize.py` | NetworkX + pyvis prototype — generates HTML (interactive) and PNG (static) |
| `coaching_tree.html` | Generated interactive visualization (open in browser) |
| `coaching_tree.png` | Generated static visualization |
