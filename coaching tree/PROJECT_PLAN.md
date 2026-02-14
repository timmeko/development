# College Football Coaching Tree Project

## Goal
Build a comprehensive, interactive network diagram showing mentorship lineages
among college football coaches — starting with Nick Saban's tree and expanding to
all active D1 Power Five head coaches, tracing lineages back ~20+ years to
coaching legends like Woody Hayes, Bo Schembechler, Urban Meyer, Lou Holtz,
Bobby Bowden, Tom Osborne, and others.

---

## Scope

### Phase 1 — Data Model & Saban Pilot
- Define a data schema capturing:
  - **Coach**: name, current role, current school
  - **Staff Stint**: school, year, role (HC / OC / DC / position coach / analyst / GA),
    hired_by (the head coach at that time)
  - **Relationship edge**: mentor → protege, with year range and context
- Manually build the complete Saban dataset:
  - Toledo (1990-94), Michigan State (1995-99), LSU (2000-04),
    Miami Dolphins (2005-06), Alabama (2007-23)
  - For each stop: every coordinator, position coach, analyst, GA — by year
- Validate against multiple sources (see Data Sources below)

### Phase 2 — Expand to All Power Five HCs
- For every current Power Five head coach (~70 coaches), trace backwards:
  - Where did they serve as an assistant? Under whom?
  - Recursively follow the "hired_by" chain back through generations
- This naturally builds out trees for Meyer, Holtz, Bowden, Osborne,
  Schembechler, Hayes, etc. as upstream ancestors are discovered

### Phase 3 — Visualization
- **Interactive network graph** (force-directed or hierarchical tree)
  - Nodes = coaches, sized by # of downstream proteges
  - Edges = mentorship relationships, labeled with school + years
  - Color-coded by coaching "family" / lineage
  - Click a node to see full career timeline
- **Timeline view** — horizontal swim-lane showing a coach's career stops
- **Search & filter** — filter by school, conference, era, role type

---

## Data Sources (ranked by utility)

### Tier 1 — Structured / Semi-Structured (best for scraping/parsing)
| Source | What it has | Access |
|--------|-------------|--------|
| **Wikipedia coach pages** | Career history tables with years, schools, roles | Free, scrapeable |
| **Sports-Reference.com** | Head coach records, school season pages with staff | Free, scrapeable |
| **Wikipedia coaching tree articles** | Explicit tree structures for major coaches | Free |

### Tier 2 — Rich but Requires Manual Extraction
| Source | What it has | Access |
|--------|-------------|--------|
| **Internet Archive media guides** | Full staff listings by year (the gold standard) | Free PDFs |
| **University athletics sites** (e.g., LSU, Alabama, Ohio State) | Media guide archives, staff bios | Free |
| **School library digital collections** (Notre Dame, Maryland) | Digitized historical media guides | Free |

### Tier 3 — Curated / Paid
| Source | What it has | Access |
|--------|-------------|--------|
| **McIllece Sports CFB Coaches Database** | Complete staffs, all FBS teams, 2005-2025 | Paid |
| **CBS / ESPN / SI coaching tree articles** | Narrative summaries of major trees | Free |
| **CollegePressbox.com** | Rosters, coaches, notes | Free |

### Recommended Approach
1. **Start with Wikipedia** — scrape coach biography pages which almost always
   have a structured "Coaching career" table (year, team, role)
2. **Cross-reference Sports-Reference** — for head coaching records and seasons
3. **Fill gaps with media guides** from Internet Archive and school sites
4. **Use journalism** (CBS, ESPN articles) to validate and catch GAs/analysts
   that structured sources miss

---

## Proposed Tech Stack

### Data Layer
- **JSON/CSV flat files** initially (easy to inspect, version-control, contribute to)
- **Schema**: `coaches.json` (nodes) + `stints.json` (edges/career stops)
- Graduate to SQLite or a graph DB (Neo4j) if the dataset grows large

### Scraping / Data Collection
- **Python** with `requests` + `BeautifulSoup` for Wikipedia/Sports-Reference
- **PyPDF2** or **pdfplumber** for media guide PDFs (if needed)
- Manual curation spreadsheet for validation

### Visualization Options (in order of recommendation)
| Tool | Pros | Cons |
|------|------|------|
| **D3.js force-directed graph** | Most flexible, interactive, web-native | Steeper learning curve |
| **Cytoscape.js** | Purpose-built for network graphs, great layouts | Less customizable styling |
| **vis.js Network** | Easy to set up, good interactivity | Can struggle with large graphs |
| **Gephi** (desktop) | Powerful analysis, beautiful exports | Not interactive on web |
| **Python NetworkX + pyvis** | Fast prototyping, exports to HTML | Less polished for production |

**Recommendation**: Start with **Python + NetworkX** for rapid prototyping and data
validation, then build the final interactive viz in **D3.js** or **Cytoscape.js**
for a polished web experience.

---

## Data Schema (Draft)

```json
// coaches.json
{
  "nick-saban": {
    "name": "Nick Saban",
    "born": 1951,
    "current_status": "retired",
    "current_role": "ESPN analyst",
    "alma_mater": "Kent State"
  }
}

// stints.json
[
  {
    "coach_id": "kirby-smart",
    "school": "Alabama",
    "year_start": 2007,
    "year_end": 2015,
    "roles": ["defensive_backs_coach", "associate_head_coach", "defensive_coordinator"],
    "head_coach_id": "nick-saban",
    "notes": "Promoted to DC in 2008"
  }
]

// relationships.json (derived)
[
  {
    "mentor_id": "nick-saban",
    "protege_id": "kirby-smart",
    "context": "Alabama 2007-2015",
    "relationship_type": "direct_report"
  }
]
```

---

## Task Breakdown

- [ ] Create data schema files (JSON templates)
- [ ] Build Saban pilot dataset (all 5 stops, every staffer by year)
- [ ] Write Wikipedia scraper for coach career tables
- [ ] Scrape all current Power Five head coaches
- [ ] Recursively trace mentorship chains back 2-3 generations
- [ ] Validate data against media guide / journalism sources
- [ ] Build NetworkX prototype visualization
- [ ] Build interactive web visualization (D3 or Cytoscape)
- [ ] Add search, filter, and timeline features

---

## Key Questions to Decide
1. **Depth threshold** — How deep do we go? (GAs? Analysts? Or just coordinators+?)
2. **Time boundary** — Hard cutoff at a year (e.g., 2000) or trace as far back as data allows?
3. **NFL crossover** — Include NFL coaching stints? (Saban's Dolphins years are relevant)
4. **"Coaching rehab" relationships** — Flag coaches who joined a staff *after* being fired as HC?
5. **Visualization priority** — Prototype first (Python) or jump straight to web (D3)?
