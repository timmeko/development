# Lou Holtz Coaching Tree Dataset

## Data model and sources

This draft builds a machine-readable dataset for Lou Holtz’s upstream mentors, Holtz’s year-by-year head-coaching staffs, and an initial downstream tree. It follows your role taxonomy where the sources support those labels. Where a staff list only identifies “assistant coach” without a position group, entries use `role: "position_coach"` with `role_detail: null`, plus a note to flag the gap. Staff completeness varies sharply by era and by school, so each stop includes an explicit `coverage_notes`. citeturn46search4turn23view0turn45view0turn36view0

Primary sources used in this draft:

- Holtz’s coaching timeline (years, stops) from Wikipedia’s coaching-career table. citeturn46search4  
- Role and “served under” context for Holtz’s assistant years from a biographical timeline (used only for role labels and mentor names, not for downstream claims). citeturn0search5  
- Notre Dame assistant staff, year-by-year, from the 247Sports/IrisIllustrated staff breakdown, plus an official Notre Dame 1996 season preview note naming Urban Meyer as receivers coach on the 1996 staff. citeturn23view0turn22search11  
- Minnesota staff lists (includes coordinators, position coaches, strength and conditioning, and listed graduate assistants) from the University of Minnesota “All-Time Coaching Staffs” page. citeturn45view0  
- William & Mary assistant-coach year ranges from the William & Mary football record book “All-Time Assistant Coaches” list, plus confirmation of Holtz’s earlier assistant stint under Milt Drewer via a William & Mary news release. citeturn36view0turn34search4  
- Arkansas 1977 coaching staff table from the 1977 season page. Later Arkansas Holtz-era years are thin in the sources reviewed in this run. citeturn46search3turn27view0  
- New York Jets 1976 staff list from the 1976 season page (partial staff listing). citeturn24search7  
- South Carolina Holtz-era coordinator names from season pages, plus an ESPN report naming assistants Holtz dismissed after the 2003 season. citeturn41search0turn43search2turn43search3turn41search6  

## Upstream lineage for Lou Holtz

Key point from source reconciliation: the “Kent State graduate assistant (1960?)” stop from your brief did not appear in the coaching-career table used here. The earliest coaching entry in that table is “Iowa (assistant) 1960.” This draft keeps the Kent State GA node as a flagged, low-confidence placeholder. citeturn46search4

The mentor names for each assistant stop below follow the biographical timeline and the William & Mary university story where applicable. citeturn0search5turn34search4

```json
{
  "upstream": [
    {
      "school": "Kent State",
      "year_start": 1960,
      "year_end": 1960,
      "role": "graduate_assistant",
      "head_coach_served_under": null,
      "other_notable_staff": [],
      "notes": "Flagged: this GA stop appears in the project brief but was not present in the coaching-career table used for this build. Treat as unverified placeholder.",
      "confidence": "low",
      "source_urls": [
        "https://en.wikipedia.org/wiki/Lou_Holtz"
      ]
    },
    {
      "school": "Iowa",
      "year_start": 1960,
      "year_end": 1960,
      "role": "assistant",
      "role_detail": "freshmen coach / linebackers (as described in one biography)",
      "head_coach_served_under": "Forest Evashevski",
      "other_notable_staff": [],
      "notes": "Coaching-career table lists Iowa (assistant) in 1960; role detail and head coach attribution come from the biographical timeline used in this draft.",
      "confidence": "medium",
      "source_urls": [
        "https://en.wikipedia.org/wiki/Lou_Holtz",
        "https://brownsvillehistoricalohio.org/lou-holtz/"
      ]
    },
    {
      "school": "William & Mary",
      "year_start": 1961,
      "year_end": 1963,
      "role": "assistant",
      "role_detail": null,
      "head_coach_served_under": "Milt Drewer",
      "other_notable_staff": [],
      "notes": "William & Mary sources describe this as Holtz's first full-time coaching role and specify head coach Milt Drewer.",
      "confidence": "high",
      "source_urls": [
        "https://en.wikipedia.org/wiki/Lou_Holtz",
        "https://www.wm.edu/news/stories/2009/lou-holtz-to-be-inducted-into-college-football-hall-of-fame123.php"
      ]
    },
    {
      "school": "Connecticut",
      "year_start": 1964,
      "year_end": 1965,
      "role": "assistant",
      "role_detail": null,
      "head_coach_served_under": "Rick Forzano",
      "other_notable_staff": [],
      "notes": "Years from coaching-career table; head coach attribution from the biographical timeline used in this draft.",
      "confidence": "medium",
      "source_urls": [
        "https://en.wikipedia.org/wiki/Lou_Holtz",
        "https://brownsvillehistoricalohio.org/lou-holtz/"
      ]
    },
    {
      "school": "South Carolina",
      "year_start": 1966,
      "year_end": 1967,
      "role": "assistant",
      "role_detail": "defensive backs (as described in one biography)",
      "head_coach_served_under": "Paul Dietzel",
      "other_notable_staff": [],
      "notes": "Years from coaching-career table; role detail and head coach attribution from the biographical timeline used in this draft.",
      "confidence": "medium",
      "source_urls": [
        "https://en.wikipedia.org/wiki/Lou_Holtz",
        "https://brownsvillehistoricalohio.org/lou-holtz/"
      ]
    },
    {
      "school": "Ohio State",
      "year_start": 1968,
      "year_end": 1968,
      "role": "assistant",
      "role_detail": null,
      "head_coach_served_under": "Woody Hayes",
      "other_notable_staff": [],
      "notes": "Years from coaching-career table; head coach attribution from the biographical timeline used in this draft.",
      "confidence": "medium",
      "source_urls": [
        "https://en.wikipedia.org/wiki/Lou_Holtz",
        "https://brownsvillehistoricalohio.org/lou-holtz/"
      ]
    }
  ]
}
```

citeturn46search4turn0search5turn34search4

## Holtz head coaching staffs by stop

This section is the core export. Notre Dame (1986–1996) and Minnesota (1984–1985) have the strongest staff coverage in the sources reviewed here. William & Mary has partial coverage from an “all-time assistants” index, without positions. Arkansas is strong for 1977 only in this run. Jets 1976 is partial. South Carolina in this run is coordinator-level plus a small number of assistant names from a 2003 staffing-change report. citeturn23view0turn45view0turn36view0turn24search7turn46search3turn41search0turn41search6

```json
{
  "holtz_career": [
    {
      "school": "William & Mary",
      "years": "1969-1971",
      "role": "head_coach",
      "staff": [
        {
          "name": "Lou Holtz",
          "year_start": 1969,
          "year_end": 1971,
          "role": "head_coach",
          "role_detail": null,
          "notes": null,
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Bobby Ross",
          "year_start": 1970,
          "year_end": 1970,
          "role": "defensive_coordinator",
          "role_detail": null,
          "notes": "Listed as defensive coordinator on the 1970 season page.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Chuck Clausen",
          "year_start": 1969,
          "year_end": 1970,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Ed Helies",
          "year_start": 1969,
          "year_end": 1971,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Kevin Hennessee",
          "year_start": 1969,
          "year_end": 1971,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Bob Herb",
          "year_start": 1968,
          "year_end": 1970,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach per record book assistant index (year range overlaps Holtz head-coaching years).",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Carrington Herbert",
          "year_start": 1969,
          "year_end": 1969,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "John Hibbs",
          "year_start": 1969,
          "year_end": 1970,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Phil Mosser",
          "year_start": 1970,
          "year_end": 1971,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Tommy Johnson",
          "year_start": 1969,
          "year_end": 1971,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Bob Kemp",
          "year_start": 1969,
          "year_end": 1971,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Duff Rearick",
          "year_start": 1969,
          "year_end": 1971,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Steve Regan",
          "year_start": 1969,
          "year_end": 1971,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach; position not specified in the record book assistant index.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Larry Beightol",
          "year_start": 1968,
          "year_end": 1971,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach per record book assistant index (year range overlaps Holtz head-coaching years).",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        },
        {
          "name": "Brian Burke",
          "year_start": 1971,
          "year_end": 1971,
          "role": "position_coach",
          "role_detail": null,
          "notes": "Assistant coach per record book assistant index (single-year listing in 1971).",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "low"
        }
      ],
      "coverage_notes": "Partial staff. The record book provides assistant names and year ranges, not position responsibilities. 1970 defensive coordinator is identified on the season page.",
      "source_urls": [
        "https://static.tribeathletics.com/custompages/files/fb/2022/2022_record_book.pdf",
        "https://en.wikipedia.org/wiki/1970_William_%26_Mary_Indians_football_team"
      ]
    },
    {
      "school": "NC State",
      "years": "1972-1975",
      "role": "head_coach",
      "staff": [
        {
          "name": "Lou Holtz",
          "year_start": 1972,
          "year_end": 1975,
          "role": "head_coach",
          "role_detail": null,
          "notes": null,
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Brian Burke",
          "year_start": 1972,
          "year_end": 1975,
          "role": "offensive_coordinator",
          "role_detail": null,
          "notes": "Listed as offensive coordinator ('Off Coach') across multiple Holtz-era NC State season pages reviewed in this run.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "medium"
        }
      ],
      "coverage_notes": "Low coverage in this run. Season pages reviewed list head coach and offensive coordinator only.",
      "source_urls": [
        "https://en.wikipedia.org/wiki/1972_NC_State_Wolfpack_football_team",
        "https://en.wikipedia.org/wiki/1973_NC_State_Wolfpack_football_team",
        "https://en.wikipedia.org/wiki/1974_NC_State_Wolfpack_football_team",
        "https://en.wikipedia.org/wiki/1975_NC_State_Wolfpack_football_team"
      ]
    },
    {
      "school": "New York Jets",
      "years": "1976",
      "role": "head_coach",
      "staff": [
        {
          "name": "Lou Holtz",
          "year_start": 1976,
          "year_end": 1976,
          "role": "head_coach",
          "role_detail": "head coach for first 13 games",
          "notes": "Interim head coach handled final game.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Mike Holovak",
          "year_start": 1976,
          "year_end": 1976,
          "role": "head_coach",
          "role_detail": "interim head coach (final game)",
          "notes": "Listed as interim head coach for final game in staff section.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Dan Henning",
          "year_start": 1976,
          "year_end": 1976,
          "role": "position_coach",
          "role_detail": "wide receivers",
          "notes": "Listed under offensive coaches.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Joe Gardi",
          "year_start": 1976,
          "year_end": 1976,
          "role": "special_teams_coordinator",
          "role_detail": "tight ends / special teams",
          "notes": "Listed as TE/special teams under offensive coaches.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Bob Fry",
          "year_start": 1976,
          "year_end": 1976,
          "role": "position_coach",
          "role_detail": "offensive line",
          "notes": "Listed under offensive coaches.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        }
      ],
      "coverage_notes": "Partial staff. The season page lists front office, head coaches, and a subset of offensive coaches in the excerpted staff section.",
      "source_urls": [
        "https://en.wikipedia.org/wiki/1976_New_York_Jets_season"
      ]
    },
    {
      "school": "Arkansas",
      "years": "1977-1983",
      "role": "head_coach",
      "staff": [
        {
          "name": "Lou Holtz",
          "year_start": 1977,
          "year_end": 1983,
          "role": "head_coach",
          "role_detail": null,
          "notes": "Full year-by-year assistant coverage not established in this run. 1977 staff table is fully enumerated on the 1977 season page.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Don Breaux",
          "year_start": 1977,
          "year_end": 1977,
          "role": "position_coach",
          "role_detail": "quarterbacks",
          "notes": "From 1977 coaching staff table.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Jesse Branch",
          "year_start": 1977,
          "year_end": 1977,
          "role": "position_coach",
          "role_detail": "wide receivers",
          "notes": "From 1977 coaching staff table.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Larry Beightol",
          "year_start": 1977,
          "year_end": 1977,
          "role": "position_coach",
          "role_detail": "offensive line",
          "notes": "From 1977 coaching staff table.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Monte Kiffin",
          "year_start": 1977,
          "year_end": 1977,
          "role": "defensive_coordinator",
          "role_detail": null,
          "notes": "From 1977 coaching staff table.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "John Mitchell",
          "year_start": 1977,
          "year_end": 1977,
          "role": "position_coach",
          "role_detail": "defensive ends",
          "notes": "From 1977 coaching staff table.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Bob Cope",
          "year_start": 1977,
          "year_end": 1977,
          "role": "position_coach",
          "role_detail": "defensive backs",
          "notes": "From 1977 coaching staff table.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Pete Carroll",
          "year_start": 1977,
          "year_end": 1977,
          "role": "graduate_assistant",
          "role_detail": null,
          "notes": "Listed as graduate assistant on the 1977 coaching staff table.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Dave Wommack",
          "year_start": 1981,
          "year_end": 1981,
          "role": "position_coach",
          "role_detail": "wide receivers",
          "notes": "Listed under Coordinators/assistant coaches on the 1981 season page (partial listing).",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "low"
        }
      ],
      "coverage_notes": "Medium-low coverage beyond 1977 in this run. 1977 staff is fully enumerated on the season page. 1981 page lists only a single assistant under 'Coordinators/assistant coaches' in the excerpted section.",
      "source_urls": [
        "https://en.wikipedia.org/wiki/1977_Arkansas_Razorbacks_football_team",
        "https://en.wikipedia.org/wiki/1981_Arkansas_Razorbacks_football_team"
      ]
    },
    {
      "school": "Minnesota",
      "years": "1984-1985",
      "role": "head_coach",
      "staff": [
        {
          "name": "Lou Holtz",
          "year_start": 1984,
          "year_end": 1985,
          "role": "head_coach",
          "role_detail": null,
          "notes": null,
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Larry Beckish",
          "year_start": 1984,
          "year_end": 1985,
          "role": "offensive_coordinator",
          "role_detail": null,
          "notes": "Listed as offensive coordinator for both 1984 and 1985.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "John Gutekunst",
          "year_start": 1984,
          "year_end": 1985,
          "role": "defensive_coordinator",
          "role_detail": null,
          "notes": "Listed as defensive coordinator for both 1984 and 1985.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Pete Cordelli",
          "year_start": 1984,
          "year_end": 1985,
          "role": "position_coach",
          "role_detail": "wide receivers",
          "notes": "Listed as wide receivers coach for both 1984 and 1985.",
          "later_became_hc": true,
          "later_hc_schools": [
            "Kent State"
          ],
          "confidence": "high"
        },
        {
          "name": "Jim Hueber",
          "year_start": 1984,
          "year_end": 1985,
          "role": "position_coach",
          "role_detail": "offensive line",
          "notes": "Listed as offensive line coach for both 1984 and 1985.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "John Palermo",
          "year_start": 1984,
          "year_end": 1985,
          "role": "position_coach",
          "role_detail": "defensive line",
          "notes": "Listed as defensive line coach for both 1984 and 1985.",
          "later_became_hc": true,
          "later_hc_schools": [
            "Austin Peay"
          ],
          "confidence": "medium"
        },
        {
          "name": "George Stewart",
          "year_start": 1984,
          "year_end": 1985,
          "role": "position_coach",
          "role_detail": "offensive line",
          "notes": "Listed as offensive line coach for both 1984 and 1985. Note: Minnesota page lists Stewart as offensive line coach; Notre Dame article lists him as TE coach when he arrived at Notre Dame.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Jim Strong",
          "year_start": 1984,
          "year_end": 1985,
          "role": "position_coach",
          "role_detail": "running backs",
          "notes": "Listed as running backs coach for both 1984 and 1985.",
          "later_became_hc": true,
          "later_hc_schools": [
            "UNLV"
          ],
          "confidence": "high"
        },
        {
          "name": "George Wemeier",
          "year_start": 1984,
          "year_end": 1985,
          "role": "position_coach",
          "role_detail": "linebackers (1984) / outside linebackers (1985)",
          "notes": "Listed as linebackers (1984) and outside linebackers (1985).",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Phil Elmassian",
          "year_start": 1984,
          "year_end": 1984,
          "role": "position_coach",
          "role_detail": "defensive backs",
          "notes": "Listed as defensive backs coach in 1984 staff list.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Dick Biddle",
          "year_start": 1985,
          "year_end": 1985,
          "role": "position_coach",
          "role_detail": "inside linebackers",
          "notes": "Listed as inside linebackers coach in 1985 staff list.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Butch Nash",
          "year_start": 1984,
          "year_end": 1985,
          "role": "administrative_assistant",
          "role_detail": "junior varsity coach (1984); volunteer coach (1985)",
          "notes": "Minnesota page lists 'Junior Varsity Coach' for 1984 and 'Volunteer Coach' for 1985.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Bob Rohde",
          "year_start": 1984,
          "year_end": 1985,
          "role": "strength_and_conditioning",
          "role_detail": null,
          "notes": "Listed as strength and conditioning coach (explicitly in 1985; listed in all-time staffs list context).",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Vinny Cerrato",
          "year_start": 1984,
          "year_end": 1985,
          "role": "graduate_assistant",
          "role_detail": null,
          "notes": "Listed as graduate assistant in 1984 and 1985 staff lists.",
          "later_became_hc": false,
          "later_hc_schools": [],
          "confidence": "high"
        },
        {
          "name": "Greg McMahon",
          "year_start": 1984,
          "year_end": 1984,
          "role": "graduate_assistant",
          "role_detail": null,
          "notes": "Listed as graduate assistant in 1984 staff list.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Ron Cooper",
          "year_start": 1985,
          "year_end": 1985,
          "role": "graduate_assistant",
          "role_detail": null,
          "notes": "Listed as graduate assistant in 1985 staff list.",
          "later_became_hc": true,
          "later_hc_schools": [
            "Eastern Michigan",
            "Louisville",
            "Alabama A&M",
            "Florida International"
          ],
          "confidence": "high"
        },
        {
          "name": "Jeff Horton",
          "year_start": 1985,
          "year_end": 1985,
          "role": "graduate_assistant",
          "role_detail": null,
          "notes": "Listed as graduate assistant in 1985 staff list.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        }
      ],
      "coverage_notes": "High coverage for 1984-1985 because staff lists are enumerated in the University of Minnesota all-time staffs page, including listed graduate assistants and strength and conditioning.",
      "source_urls": [
        "https://gophersports.com/news/2006/5/16/All_Time_Coaching_Staffs"
      ]
    },
    {
      "school": "Notre Dame",
      "years": "1986-1996",
      "role": "head_coach",
      "staff": [
        {
          "name": "Lou Holtz",
          "year_start": 1986,
          "year_end": 1996,
          "role": "head_coach",
          "role_detail": null,
          "notes": null,
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },

        { "name": "Mike Stock", "year_start": 1986, "year_end": 1986, "role": "offensive_coordinator", "role_detail": "offensive coordinator / running backs", "notes": "Listed as OC/RB in 1986 staff breakdown.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Jim Strong", "year_start": 1987, "year_end": 1989, "role": "offensive_coordinator", "role_detail": "offensive coordinator / running backs", "notes": "Listed as OC/RB (1987-1989).", "later_became_hc": true, "later_hc_schools": ["UNLV"], "confidence": "high" },
        { "name": "Skip Holtz", "year_start": 1992, "year_end": 1993, "role": "offensive_coordinator", "role_detail": "offensive coordinator / wide receivers", "notes": "Listed as OC/WR in 1992-1993; listed as WR coach in 1991.", "later_became_hc": true, "later_hc_schools": ["Connecticut", "East Carolina", "South Florida", "Louisiana Tech"], "confidence": "high" },
        { "name": "Dave Roberts", "year_start": 1994, "year_end": 1996, "role": "offensive_coordinator", "role_detail": "wide receivers (1994); quarterbacks (1995-1996)", "notes": "Listed as OC/WR in 1994 and OC/QB in 1995-1996.", "later_became_hc": true, "later_hc_schools": ["Western Kentucky", "Northeast Louisiana", "Baylor"], "confidence": "high" },

        { "name": "Foge Fazio", "year_start": 1986, "year_end": 1987, "role": "defensive_coordinator", "role_detail": "defensive coordinator / inside linebackers", "notes": "Listed as DC/ILB in 1986-1987.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Barry Alvarez", "year_start": 1987, "year_end": 1989, "role": "defensive_coordinator", "role_detail": "outside linebackers (1987); defensive coordinator/LB (1988); assistant head coach/defensive coordinator/LB (1989)", "notes": "Role progression in the year-by-year staff breakdown.", "later_became_hc": true, "later_hc_schools": ["Wisconsin"], "confidence": "high" },
        { "name": "Gary Darnell", "year_start": 1990, "year_end": 1991, "role": "defensive_coordinator", "role_detail": "defensive coordinator / linebackers", "notes": "Listed as DC/LB (1990) and DC/ILB (1991).", "later_became_hc": true, "later_hc_schools": ["Tennessee Tech", "Western Michigan"], "confidence": "high" },
        { "name": "Rick Minter", "year_start": 1992, "year_end": 1993, "role": "defensive_coordinator", "role_detail": "defensive coordinator / defensive backs (1992); defensive coordinator / linebackers (1993)", "notes": "Listed as DC/B (1992) and DC/LB (1993).", "later_became_hc": true, "later_hc_schools": ["Cincinnati"], "confidence": "high" },
        { "name": "Bob Davie", "year_start": 1994, "year_end": 1996, "role": "defensive_coordinator", "role_detail": "defensive coordinator (1994); defensive coordinator/inside linebackers (1995-1996)", "notes": "Listed as DC (1994) and DC/ILB (1995-1996).", "later_became_hc": true, "later_hc_schools": ["Notre Dame", "New Mexico"], "confidence": "high" },

        { "name": "Tony Yelovich", "year_start": 1986, "year_end": 1988, "role": "position_coach", "role_detail": "offensive line (1986-1987); guards/centers (1988)", "notes": "Listed as OL or G/C through 1988.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Tony Yelovich", "year_start": 1989, "year_end": 1990, "role": "position_coach", "role_detail": "wide receivers (1989); wide receivers/tight ends (1990)", "notes": "Listed as WR (1989) and WR/TE (1990). Duplicate name entry reflects role change.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Tony Yelovich", "year_start": 1991, "year_end": 1993, "role": "special_teams_coordinator", "role_detail": "special teams / recruiting coordinator", "notes": "Listed as ST/RC (1991-1993). Duplicate name entry reflects coordinator role.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Vinny Cerrato", "year_start": 1986, "year_end": 1990, "role": "recruiting_coordinator", "role_detail": null, "notes": "Listed as recruiting coordinator in yearly breakdown through 1990.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Vinny Cerrato", "year_start": 1991, "year_end": 1991, "role": "recruiting_coordinator", "role_detail": null, "notes": "Still listed as RC in 1991; later years show ST/RC handled by Yelovich and no RC line item in 1994-1996.", "later_became_hc": false, "later_hc_schools": [], "confidence": "medium" },

        { "name": "Pete Cordelli", "year_start": 1986, "year_end": 1988, "role": "position_coach", "role_detail": "wide receivers", "notes": "Listed as WR coach 1986-1988.", "later_became_hc": true, "later_hc_schools": ["Kent State"], "confidence": "high" },
        { "name": "Pete Cordelli", "year_start": 1989, "year_end": 1990, "role": "position_coach", "role_detail": "quarterbacks", "notes": "Listed as QB coach 1989-1990.", "later_became_hc": true, "later_hc_schools": ["Kent State"], "confidence": "high" },

        { "name": "George Stewart", "year_start": 1986, "year_end": 1988, "role": "position_coach", "role_detail": "tight ends", "notes": "Listed as TE coach 1986-1988.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Joe Moore", "year_start": 1988, "year_end": 1988, "role": "position_coach", "role_detail": "offensive tackles / tight ends", "notes": "Listed as OT/TE in 1988.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Joe Moore", "year_start": 1989, "year_end": 1996, "role": "position_coach", "role_detail": "offensive line", "notes": "Listed as OL coach 1989-1996.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Joe Yonto", "year_start": 1986, "year_end": 1987, "role": "position_coach", "role_detail": "defensive line", "notes": "Listed as DL coach 1986-1987.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Kurt Schottenheimer", "year_start": 1986, "year_end": 1986, "role": "position_coach", "role_detail": "outside linebackers", "notes": "Listed as OLB coach in 1986.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Terry Forbes", "year_start": 1986, "year_end": 1987, "role": "position_coach", "role_detail": "defensive backs", "notes": "Listed as DB coach 1986-1987.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "John Palermo", "year_start": 1988, "year_end": 1989, "role": "position_coach", "role_detail": "defensive line (1988); defensive tackles (1989)", "notes": "Listed as DL (1988) and DT (1989).", "later_became_hc": true, "later_hc_schools": ["Austin Peay"], "confidence": "high" },
        { "name": "Chuck Heater", "year_start": 1988, "year_end": 1990, "role": "position_coach", "role_detail": "defensive backs", "notes": "Listed as DB coach 1988-1990.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Jay Hayes", "year_start": 1989, "year_end": 1991, "role": "position_coach", "role_detail": "defensive ends (1989); outside linebackers (1990-1991)", "notes": "Listed as DE coach (1989) and OLB coach (1990-1991).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Peter Vaas", "year_start": 1990, "year_end": 1990, "role": "position_coach", "role_detail": "running backs", "notes": "Listed as RB coach (1990).", "later_became_hc": true, "later_hc_schools": ["Holy Cross"], "confidence": "high" },
        { "name": "Peter Vaas", "year_start": 1991, "year_end": 1991, "role": "position_coach", "role_detail": "quarterbacks", "notes": "Listed as QB coach (1991).", "later_became_hc": true, "later_hc_schools": ["Holy Cross"], "confidence": "high" },
        { "name": "Dick Bumpas", "year_start": 1990, "year_end": 1991, "role": "position_coach", "role_detail": "defensive line", "notes": "Listed as DL coach (1990-1991).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Tom Beck", "year_start": 1991, "year_end": 1991, "role": "position_coach", "role_detail": "running backs", "notes": "Listed as RB coach (1991).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Ron Cooper", "year_start": 1991, "year_end": 1991, "role": "position_coach", "role_detail": "defensive backs", "notes": "Listed as DB coach (1991).", "later_became_hc": true, "later_hc_schools": ["Eastern Michigan", "Louisville", "Alabama A&M", "Florida International"], "confidence": "high" },
        { "name": "Ron Cooper", "year_start": 1992, "year_end": 1992, "role": "assistant_head_coach", "role_detail": "assistant head coach / defensive backs", "notes": "Listed as Asst. HC/DB (1992).", "later_became_hc": true, "later_hc_schools": ["Eastern Michigan", "Louisville", "Alabama A&M", "Florida International"], "confidence": "high" },

        { "name": "Tom Clements", "year_start": 1992, "year_end": 1994, "role": "position_coach", "role_detail": "quarterbacks", "notes": "Listed as QB coach (1992-1994).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Tom Clements", "year_start": 1995, "year_end": 1995, "role": "assistant_head_coach", "role_detail": "assistant head coach / wide receivers", "notes": "Listed as Asst. HC/WR (1995).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Earle Mosley", "year_start": 1992, "year_end": 1996, "role": "position_coach", "role_detail": "running backs", "notes": "Listed as RB coach (1992-1996).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Mike Trgovac", "year_start": 1992, "year_end": 1992, "role": "position_coach", "role_detail": "defensive line", "notes": "Listed as DL coach (1992).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Mike Trgovac", "year_start": 1993, "year_end": 1994, "role": "assistant_head_coach", "role_detail": "assistant head coach / defensive line", "notes": "Listed as Asst. HC/DL (1993-1994).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Joe Wessel", "year_start": 1992, "year_end": 1992, "role": "position_coach", "role_detail": "defensive ends", "notes": "Listed as DE coach (1992).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Joe Wessel", "year_start": 1993, "year_end": 1993, "role": "position_coach", "role_detail": "defensive backs", "notes": "Listed as DB coach (1993).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Keith Armstrong", "year_start": 1993, "year_end": 1993, "role": "special_teams_coordinator", "role_detail": "defensive ends / special teams", "notes": "Listed as DE/ST (1993).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Bob Chmiel", "year_start": 1994, "year_end": 1996, "role": "recruiting_coordinator", "role_detail": "tight ends / recruiting coordinator", "notes": "Listed as TE/RC (1994-1996).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Kirk Doll", "year_start": 1994, "year_end": 1995, "role": "special_teams_coordinator", "role_detail": "linebackers / special teams", "notes": "Listed as LB/ST (1994-1995).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Kirk Doll", "year_start": 1996, "year_end": 1996, "role": "special_teams_coordinator", "role_detail": "defensive ends / special teams", "notes": "Listed as DE/ST (1996). Duplicate name entry reflects role change.", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Dean Pees", "year_start": 1994, "year_end": 1994, "role": "position_coach", "role_detail": "defensive backs", "notes": "Listed as DB coach (1994).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },
        { "name": "Charlie Strong", "year_start": 1995, "year_end": 1996, "role": "position_coach", "role_detail": "defensive line", "notes": "Listed as DL coach (1995-1996).", "later_became_hc": true, "later_hc_schools": ["Louisville", "Texas", "South Florida"], "confidence": "high" },
        { "name": "Tom McMahon", "year_start": 1995, "year_end": 1996, "role": "position_coach", "role_detail": "defensive backs", "notes": "Listed as DB coach (1995-1996).", "later_became_hc": false, "later_hc_schools": [], "confidence": "high" },

        { "name": "Urban Meyer", "year_start": 1996, "year_end": 1996, "role": "position_coach", "role_detail": "wide receivers", "notes": "Listed as WR coach in 1996 and separately identified as 'receiver coach' in a Notre Dame 1996 season preview note.", "later_became_hc": true, "later_hc_schools": ["Bowling Green", "Utah", "Florida", "Ohio State"], "confidence": "high" }
      ],
      "coverage_notes": "High coverage for the 9-on-field assistant era because the source provides a year-by-year assistant breakdown. This does not enumerate the full ecosystem of GAs/analysts/support roles for each season.",
      "source_urls": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/",
        "https://fightingirish.com/sports-m-footbl-archive-96season-nd-game04-nd-m-fb-ev-gm04-prev-html/"
      ]
    },
    {
      "school": "South Carolina",
      "years": "1999-2004",
      "role": "head_coach",
      "staff": [
        {
          "name": "Lou Holtz",
          "year_start": 1999,
          "year_end": 2004,
          "role": "head_coach",
          "role_detail": null,
          "notes": null,
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Skip Holtz",
          "year_start": 1999,
          "year_end": 2004,
          "role": "offensive_coordinator",
          "role_detail": null,
          "notes": "Listed as offensive coach on multiple season pages in this run (example: 1999 as OC year 1; 2004 as OC year 6).",
          "later_became_hc": true,
          "later_hc_schools": ["Connecticut", "East Carolina", "South Florida", "Louisiana Tech"],
          "confidence": "high"
        },
        {
          "name": "Charlie Strong",
          "year_start": 1999,
          "year_end": 2002,
          "role": "defensive_coordinator",
          "role_detail": null,
          "notes": "Listed as defensive coach on 1999-2002 season pages in this run. End year requires confirmation because 2003 page was not sourced in this run.",
          "later_became_hc": true,
          "later_hc_schools": ["Louisville", "Texas", "South Florida"],
          "confidence": "medium"
        },
        {
          "name": "Rick Minter",
          "year_start": 2004,
          "year_end": 2004,
          "role": "defensive_coordinator",
          "role_detail": null,
          "notes": "Listed as defensive coach on the 2004 season page (DC year 1).",
          "later_became_hc": true,
          "later_hc_schools": ["Cincinnati"],
          "confidence": "high"
        },
        {
          "name": "Chris Cosh",
          "year_start": 2003,
          "year_end": 2003,
          "role": "defensive_coordinator",
          "role_detail": "linebackers",
          "notes": "Named as defensive coordinator/linebackers coach who did not return after staff changes reported in late 2003.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Dave DeGuglielmo",
          "year_start": 2003,
          "year_end": 2003,
          "role": "position_coach",
          "role_detail": "offensive line",
          "notes": "Named as offensive line coach who did not return after staff changes reported in late 2003.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "Todd Fitch",
          "year_start": 2003,
          "year_end": 2003,
          "role": "position_coach",
          "role_detail": "quarterbacks",
          "notes": "Named as quarterbacks coach who did not return after staff changes reported in late 2003.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        },
        {
          "name": "John Gutekunst",
          "year_start": 2003,
          "year_end": 2003,
          "role": "position_coach",
          "role_detail": "defense (unspecified)",
          "notes": "Named as a defensive coach who did not return after staff changes reported in late 2003.",
          "later_became_hc": null,
          "later_hc_schools": null,
          "confidence": "high"
        }
      ],
      "coverage_notes": "Medium-low coverage in this run. Season pages establish OC/DC for multiple years, and a 2003 report identifies four assistant roles. Full year-by-year staff enumeration needs South Carolina media guides or a program record book section not retrieved in this run.",
      "source_urls": [
        "https://en.wikipedia.org/wiki/1999_South_Carolina_Gamecocks_football_team",
        "https://en.wikipedia.org/wiki/2002_South_Carolina_Gamecocks_football_team",
        "https://en.wikipedia.org/wiki/2004_South_Carolina_Gamecocks_football_team",
        "https://www.espn.com/college-football/news/story?id=1670882"
      ]
    }
  ]
}
```

citeturn36view0turn39view0turn29search0turn29search2turn29search3turn24search7turn46search3turn26view0turn45view0turn23view0turn22search11turn41search0turn43search3turn41search6

## Downstream tree extraction

This run supports a clean, source-based extraction of a Generation 1 list for the Notre Dame branch because the Notre Dame staff breakdown explicitly identifies which Holtz assistants later became head coaches, and it names their head-coaching destinations at a high level. citeturn23view0

For South Carolina, Arkansas, and NC State, Generation 1 extraction is incomplete in this run because the staff lists were incomplete. For Minnesota, several names overlap with the Notre Dame list and are captured there, plus Ron Cooper appears as a Minnesota graduate assistant in 1985. citeturn45view0turn23view0turn46search3

```json
{
  "generation_1": [
    {
      "name": "Barry Alvarez",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame assistant staff (1987-1989) with DC duties in 1988-1989 per staff breakdown",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Flag: full career and HC records not assembled in this run. Use Wikipedia 'Coaching career' tables as the primary fill source in a follow-on pass.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    },
    {
      "name": "Pete Cordelli",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame assistant staff (1986-1990)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at Kent State.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    },
    {
      "name": "John Palermo",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame assistant staff (1988-1989)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at Austin Peay.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    },
    {
      "name": "Peter Vaas",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame assistant staff (1990-1991)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at Holy Cross.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    },
    {
      "name": "Ron Cooper",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame assistant staff (1991-1992); also listed as Minnesota GA in 1985",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at Eastern Michigan, Louisville, Alabama A&M, and Florida International.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/",
        "https://gophersports.com/news/2006/5/16/All_Time_Coaching_Staffs"
      ]
    },
    {
      "name": "Rick Minter",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame defensive coordinator (1992-1993)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at Cincinnati.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    },
    {
      "name": "Bob Davie",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame defensive coordinator (1994-1996)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at Notre Dame and New Mexico.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    },
    {
      "name": "Dave Roberts",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame offensive coordinator (1994-1996)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at Western Kentucky, Northeast Louisiana, and Baylor.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    },
    {
      "name": "Jim Strong",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame offensive coordinator (1987-1989)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at UNLV.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    },
    {
      "name": "Gary Darnell",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame defensive coordinator (1990-1991)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at Tennessee Tech and Western Michigan.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    },
    {
      "name": "Urban Meyer",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame wide receivers coach (1996)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Role as 1996 receivers coach is corroborated by a Notre Dame season preview note. Head-coaching destinations listed in the staff breakdown.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/",
        "https://fightingirish.com/sports-m-footbl-archive-96season-nd-game04-nd-m-fb-ev-gm04-prev-html/"
      ]
    },
    {
      "name": "Charlie Strong",
      "mentor": "Lou Holtz",
      "mentor_context": "Notre Dame defensive line coach (1995-1996)",
      "career": null,
      "hc_record": null,
      "notable_assistants": null,
      "notes": "Identified by the staff breakdown as a later head coach at Louisville, Texas, and South Florida.",
      "sources": [
        "https://247sports.com/article/nd-assistants-holtz-to-kelly-part-1-74905323/"
      ]
    }
  ],
  "generation_2": [],
  "generation_3": [],
  "generation_notes": "Generation 2 and 3 branches require a full assistant-coach dataset for each Gen-1 coach's head-coaching stops. This run did not retrieve those media guides or equivalent structured staff pages."
}
```

citeturn23view0turn22search11turn45view0

## Coverage gaps and what still blocks full completeness

Notre Dame is close to your “80%+” target for on-field assistants (the nine-assistant era) because the staff breakdown enumerates each year and position grouping. It does not enumerate analysts, directors of operations, or a complete GA list for every season. citeturn23view0turn22search11

Minnesota is strong for 1984–1985 because the staff list includes coordinators, position coaches, strength and conditioning, and listed graduate assistants. citeturn45view0

William & Mary sits in the “names and years exist, roles sparse” bucket in this run. The record book provides assistant names and year ranges, but not assignments like “QB” or “OL.” citeturn36view0turn39view0

NC State, Arkansas (post-1977), Jets, and South Carolina remain under target completeness in this run due to missing single-source year-by-year staff enumerations. South Carolina has coordinator continuity by season pages and a small assistant set from a staff-change report, but not full yearly staff lists. citeturn29search0turn46search3turn24search7turn41search0turn41search6