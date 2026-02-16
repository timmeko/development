# Research Brief: Lou Holtz Coaching Tree — Complete Staff Data

## Objective

Build a comprehensive dataset of every coach who worked under Lou Holtz at
every stop in his career, plus one level of upstream (who mentored Holtz) and
two levels of downstream recursion (Holtz's proteges' proteges, and one more
generation beyond that where data exists).

This data will be used to build an interactive network visualization of
coaching lineages in college football.

---

## Deliverables

### Deliverable 1: Lou Holtz Upstream Lineage

Trace Holtz's own career as an assistant and identify his mentors:

- **Kent State** — graduate assistant (1960?)
- **Iowa** — graduate assistant under Forest Evashevski (1960-61?)
- **William & Mary** — assistant coach (1961-63?)
- **Connecticut** — assistant coach (1964-65?)
- **South Carolina** — assistant coach (1966-67?)
- **Ohio State** — assistant coach under Woody Hayes (1968)

For each stop provide:
- Exact years
- His role/title
- The head coach he served under
- Any other notable coaches on staff at the same time

### Deliverable 2: Lou Holtz Head Coaching Staffs (The Core Dataset)

For each of Holtz's seven head coaching stops, provide **every known coaching
staff member by year**. This is the heart of the project.

#### Stops to cover:

| # | School | Years | Priority |
|---|--------|-------|----------|
| 1 | William & Mary | 1969-1971 | Medium (data may be scarce) |
| 2 | NC State | 1972-1975 | Medium |
| 3 | New York Jets (NFL) | 1976 | Medium |
| 4 | Arkansas | 1977-1983 | Medium-High |
| 5 | Minnesota | 1984-1985 | Medium |
| 6 | Notre Dame | 1986-1996 | **HIGHEST** — most proteges came from here |
| 7 | South Carolina | 1999-2004 | High |

#### For each staff member, capture:

| Field | Description | Required? |
|-------|-------------|-----------|
| `name` | Full name | Yes |
| `year_start` | First year on this staff | Yes |
| `year_end` | Last year on this staff | Yes |
| `role` | Title/position (see role taxonomy below) | Yes |
| `role_detail` | Specific position group if applicable (e.g., "wide receivers", "defensive line") | If available |
| `notes` | Any relevant context (e.g., "promoted from GA to full-time in 1990") | If available |
| `later_became_hc` | Did this person later become a head coach? Yes/No | Yes |
| `later_hc_schools` | If yes, where? | If applicable |

#### Role Taxonomy (use these categories):

- `head_coach`
- `offensive_coordinator`
- `defensive_coordinator`
- `special_teams_coordinator`
- `position_coach` (specify group in `role_detail`)
- `graduate_assistant`
- `analyst`
- `director_of_operations`
- `strength_and_conditioning`
- `recruiting_coordinator`
- `assistant_head_coach`
- `administrative_assistant`

#### Special emphasis on Notre Dame (1986-1996):

This is the most important dataset. Known staff members to confirm/expand
(this list is INCOMPLETE — fill in the gaps):

- Urban Meyer — believed to be WR coach or assistant WR coach, ~1996 or earlier
  (PLEASE CONFIRM exact years and exact title — was he a GA first? When
  promoted to position coach?)
- Barry Alvarez — defensive coordinator (1987-1989?)
- Bob Davie — defensive coordinator (1994-1996?)
- Bob Chmiel — secondary coach?
- Joe Moore — offensive line coach
- Skip Holtz — some role on staff
- Pete Cordelli — wide receivers coach?
- Earle Mosley — ?
- George Stewart — ?
- Gary Darnell — ?
- Dave Roberts — ?
- Ron Cooper — ?
- Greg Davis — ?
- Jim Strong — ?
- Vinny Cerrato — recruiting
- Jay Hayes — ?
- Kirk Doll — ?

**Goal: Identify ALL staff members for ALL 11 seasons (1986-1996), not just
the famous ones.**

### Deliverable 3: Downstream Generation 1 (Holtz's Direct Proteges)

For every staff member identified in Deliverable 2 who **later became a head
coach** (at any level — FBS, FCS, D2, D3, NAIA, or NFL), provide their
complete coaching career:

| Field | Description |
|-------|-------------|
| `name` | Full name |
| `career` | List of every coaching job: year_start, year_end, school, role |
| `hc_record` | Win-loss record as HC at each stop |
| `notable_assistants` | List of their assistants who later became HCs (names only — detail in Deliverable 4) |

**Known Gen-1 proteges to trace (incomplete list — add anyone I've missed):**

- Barry Alvarez (Wisconsin)
- Bob Davie (Notre Dame, New Mexico)
- Urban Meyer (Bowling Green, Utah, Florida, Ohio State, Jacksonville Jaguars)
- Skip Holtz (Connecticut, East Carolina, South Florida, Louisiana Tech, Marshall)
- Greg Davis (became OC at Texas, Iowa)
- Pete Cordelli (Kent State?)
- Jim Strong (UNLV?)
- Ron Cooper (Eastern Michigan, Louisville, Alabama A&M)
- Bob Chmiel — did he become a HC?
- Gary Darnell — did he become a HC?
- George Stewart — NFL coaching career?
- Dave Roberts — coaching career?
- Jay Hayes — coaching career?
- Mark Mangino (not sure if Holtz connection — verify)

### Deliverable 4: Downstream Generation 2 (Proteges of Proteges)

For each Gen-1 protege who became a head coach, list their notable assistants
who ALSO became head coaches, with basic career info.

**Known Gen-2 branches to trace:**

**Urban Meyer's tree (highest priority):**
- Dan Mullen (Mississippi State, Florida)
- Luke Fickell (Cincinnati, Wisconsin)
- Tom Herman (Houston, Texas)
- Charlie Strong (Louisville, Texas, South Florida)
- Ryan Day (Ohio State)
- Marcus Freeman (Notre Dame)
- Kerry Coombs
- Mike Vrabel (if applicable)
- Doc Holliday (Marshall)
- Everett Withers (James Madison, Texas State)
- Chris Ash (Rutgers)
- Greg Schiano (Rutgers, Tampa Bay)
- Kyle Whittingham (Utah) — verify if connected to Meyer or independent

**Barry Alvarez's tree:**
- Bret Bielema (Wisconsin, Arkansas, Illinois)
- Gary Andersen (Utah State, Wisconsin, Oregon State)
- Don Treadwell (Miami OH?)
- Dave Doeren (NC State)
- Paul Chryst (Pittsburgh, Wisconsin)

**Bob Davie's tree:**
- Any assistants who became HCs

### Deliverable 5: Downstream Generation 3 (One More Level)

For the most prominent Gen-2 coaches (Meyer's proteges especially), list
their notable assistants who became HCs. Brief info only.

Examples:
- Ryan Day's assistants at Ohio State who have become HCs
- Luke Fickell's assistants at Cincinnati/Wisconsin
- Dan Mullen's assistants at Mississippi State/Florida
- Tom Herman's assistants at Houston/Texas

---

## Desired Output Format

**Please deliver as structured data in one of these formats (in order of
preference):**

### Option A: JSON (preferred)

```json
{
  "upstream": [
    {
      "coach": "Woody Hayes",
      "relationship_to_holtz": "Head coach at Ohio State when Holtz was assistant",
      "years": "1968",
      "school": "Ohio State"
    }
  ],
  "holtz_career": [
    {
      "school": "Notre Dame",
      "years": "1986-1996",
      "role": "head_coach",
      "staff": [
        {
          "name": "Urban Meyer",
          "year_start": 1986,
          "year_end": 1996,
          "role": "position_coach",
          "role_detail": "wide receivers",
          "later_became_hc": true,
          "later_hc_schools": ["Bowling Green", "Utah", "Florida", "Ohio State"],
          "notes": "Started as GA in 1986, promoted to WR coach by 1988 (VERIFY)"
        }
      ]
    }
  ],
  "generation_1": [
    {
      "name": "Urban Meyer",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame 1986-1996",
      "career": [
        {"year_start": 2001, "year_end": 2002, "school": "Bowling Green", "role": "head_coach"}
      ],
      "hc_record_total": "190-32",
      "notable_assistants": ["Dan Mullen", "Luke Fickell", "Tom Herman"]
    }
  ],
  "generation_2": [...],
  "generation_3": [...]
}
```

### Option B: Markdown Tables

If JSON is too cumbersome, deliver as markdown tables with the same fields.
One table per Holtz coaching stop, one table per Gen-1 protege, etc.

### Option C: CSV/Spreadsheet

Three CSVs:
1. `holtz_staffs.csv` — all staff members across all stops
2. `downstream_coaches.csv` — all proteges (Gen 1-3) with career paths
3. `relationships.csv` — mentor/protege edges with context

---

## Research Methodology

### Primary Sources (in priority order):

1. **Wikipedia** — Coach biography pages almost always have a "Coaching career"
   table. Start here for every coach's career path.

2. **Notre Dame media guides** — Notre Dame's library has an extensive
   collection. The university's athletics site and the Hesburgh Library may
   have digitized versions. Search:
   - https://und.com (Notre Dame athletics)
   - Internet Archive: search "Notre Dame football media guide" for years 1986-1996
   - Notre Dame Joyce Sports Research Collection

3. **Sports-Reference.com** — Head coaching records and some school pages:
   - https://www.sports-reference.com/cfb/coaches/lou-holtz-1.html
   - School pages for each year may list coaches

4. **Newspaper archives** — For pre-internet era staffs (1969-1985):
   - Search "Lou Holtz hires" + school name + year
   - AP/UPI wire stories about coaching changes
   - Local papers: South Bend Tribune (Notre Dame), Raleigh News & Observer
     (NC State), Arkansas Democrat-Gazette (Arkansas), Minneapolis Star Tribune
     (Minnesota), The State (South Carolina)

5. **Coaching tree articles** — Search for existing journalism:
   - "Lou Holtz coaching tree"
   - "Notre Dame coaching tree"
   - "coaches who worked under Lou Holtz"

6. **University athletics archives** — Many schools publish historical staff info:
   - Arkansas: https://arkansasrazorbacks.com
   - NC State: https://gopack.com
   - South Carolina: https://gamecocksonline.com
   - Minnesota: https://gophersports.com

7. **Internet Archive media guides** — Search archive.org for:
   - "[school] football media guide [year]" for each school/year combination
   - The collection at https://archive.org/details/college-football-media-guides

### What to do when data is incomplete:

- **Flag it.** If you can only find 6 of an estimated 10 staff members for a
  given year, note that explicitly: "Partial staff — 6 of ~10 identified"
- **Don't fabricate.** If a year or role is uncertain, mark it with a `?` or
  `"confidence": "low"`
- **Distinguish GA vs. position coach.** Urban Meyer at Notre Dame is a key
  example — was he a GA, a WR coach, or both at different times? Get this right.
- **Note role changes within a tenure.** If someone was promoted from DB coach
  to DC during their time on staff, capture both roles with year ranges.

---

## Completeness Expectations

| Dataset | Target Completeness |
|---------|-------------------|
| Holtz upstream (his mentors) | 90%+ — well documented |
| Notre Dame staff 1986-1996 | 80%+ — should be findable |
| South Carolina staff 1999-2004 | 70%+ — internet era |
| Arkansas staff 1977-1983 | 50-60% — pre-internet, harder |
| NC State staff 1972-1975 | 40-50% — quite old |
| William & Mary staff 1969-1971 | 30-40% — may be very thin |
| Minnesota staff 1984-1985 | 40-50% — only 2 years |
| NY Jets staff 1976 | 50%+ — NFL records may help |
| Gen-1 protege careers | 90%+ — Wikipedia covers these well |
| Gen-2 protege careers | 80%+ — most are recent/current coaches |
| Gen-3 protege careers | 60-70% — many are still early career |

---

## Important Notes

- **The name is spelled "Holtz"** (not Holts, Holt, or Holz)
- **Lou Holtz was born in 1937** in Follansbee, West Virginia
- **He played at Kent State**, not as a coach — his first coaching role was as a
  graduate assistant
- **The 1988 Notre Dame team won the national championship** — the staff that
  year is especially interesting
- **There is a 2-year gap (1997-1998)** between Notre Dame and South Carolina
  where Holtz was not coaching — he was doing TV commentary
- **Urban Meyer's connection to Holtz is a centerpiece of this project** — get
  the exact years and roles right. Meyer has said publicly that Holtz was one
  of his primary mentors.
