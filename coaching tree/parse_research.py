"""
Parse ChatGPT research files, cross-reference against existing data, and run gap analysis.
"""
import json
from pathlib import Path

BASE = Path(__file__).parent
coaches_path = BASE / "data/coaches.json"
relationships_path = BASE / "data/relationships.json"

with open(coaches_path) as f:
    coaches = json.load(f)
with open(relationships_path) as f:
    relationships = json.load(f)

existing_rel_ids = {r["id"] for r in relationships}

# ──────────────────────────────────────────────────────────────────────────────
# NEW COACHES (parsed from all 26 research files)
# ──────────────────────────────────────────────────────────────────────────────

NEW_COACHES = {
    # Gen 2 – Pete Carroll proteges
    "steve-sarkisian": {
        "name": "Steve Sarkisian", "born": 1974, "alma_mater": "BYU",
        "current_status": "active", "generation": 2,
        "hc_schools": ["Washington", "USC", "Texas"],
        "mentor": "pete-carroll",
        "mentor_context": "QB Coach at USC, 2001-2003, 2005-2006",
    },
    "dan-quinn": {
        "name": "Dan Quinn", "born": 1970, "alma_mater": "Salisbury",
        "current_status": "active", "generation": 2,
        "hc_schools": ["Atlanta Falcons", "Dallas Cowboys"],
        "mentor": "pete-carroll",
        "mentor_context": "DC at Seattle Seahawks, 2013-2014",
    },
    "darrell-bevell": {
        "name": "Darrell Bevell", "born": 1971, "alma_mater": "Wisconsin",
        "current_status": "active", "generation": 2,
        "hc_schools": ["Detroit Lions (interim)", "Jacksonville Jaguars (interim)"],
        "mentor": "pete-carroll",
        "mentor_context": "OC at Seattle Seahawks, 2011-2017",
    },

    # Gen 3 – Jimmy Johnson proteges
    "butch-davis": {
        "name": "Butch Davis", "born": 1951, "alma_mater": "Arkansas",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Miami (FL)", "Cleveland Browns", "North Carolina", "FIU"],
        "mentor": "jimmy-johnson",
        "mentor_context": "DL Coach at Oklahoma State 1979-83, Miami (FL) 1984-88, Dallas Cowboys 1989-92",
    },
    "dave-wannstedt": {
        "name": "Dave Wannstedt", "born": 1952, "alma_mater": "Pittsburgh",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Chicago Bears", "Miami Dolphins", "Pittsburgh"],
        "mentor": "jimmy-johnson",
        "mentor_context": "DC at Oklahoma State 1979-82, Miami (FL) 1986-88, Dallas Cowboys 1989-92",
    },
    "tommy-tuberville": {
        "name": "Tommy Tuberville", "born": 1954, "alma_mater": "Southern Arkansas",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Ole Miss", "Auburn", "Texas Tech", "Cincinnati"],
        "mentor": "jimmy-johnson",
        "mentor_context": "DL Coach at Miami (FL), 1986-87",
    },
    "norv-turner": {
        "name": "Norv Turner", "born": 1952, "alma_mater": "Oregon",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Washington Redskins", "Oakland Raiders", "San Diego Chargers"],
        "mentor": "jimmy-johnson",
        "mentor_context": "OC at Dallas Cowboys, 1991-93",
    },

    # Gen 3 – Joe Gibbs proteges
    "richie-petitbon": {
        "name": "Richie Petitbon", "born": 1938, "alma_mater": "Tulane",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Washington Redskins (interim)"],
        "mentor": "joe-gibbs",
        "mentor_context": "DC at Washington Redskins, 1981-92",
    },
    "joe-bugel": {
        "name": "Joe Bugel", "born": 1940, "alma_mater": "Western Kentucky",
        "current_status": "deceased", "generation": 3,
        "hc_schools": ["Phoenix Cardinals", "Oakland Raiders"],
        "mentor": "joe-gibbs",
        "mentor_context": "OL Coach at Washington Redskins, 1981-89",
    },
    "al-saunders": {
        "name": "Al Saunders", "born": 1947, "alma_mater": "San Jose State",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["San Diego Chargers"],
        "mentor": "joe-gibbs",
        "mentor_context": "WR Coach at Washington Redskins, 1981-82; Associate HC, 2006-07",
    },
    "gregg-williams": {
        "name": "Gregg Williams", "born": 1958, "alma_mater": "Delta State",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Buffalo Bills", "New Orleans Saints (interim)"],
        "mentor": "joe-gibbs",
        "mentor_context": "AHC/Defense at Washington Redskins, 2004-07",
    },
    "bill-callahan": {
        "name": "Bill Callahan", "born": 1959, "alma_mater": "Illinois-Chicago",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Oakland Raiders", "Nebraska"],
        "mentor": "joe-gibbs",
        "mentor_context": "OL Coach at Washington Redskins, 2005-07",
    },

    # Gen 3 – Ken Hatfield proteges
    "houston-nutt": {
        "name": "Houston Nutt", "born": 1957, "alma_mater": "Oklahoma State",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Boise State", "Arkansas", "Ole Miss"],
        "mentor": "ken-hatfield",
        "mentor_context": "WR Coach at Arkansas, 1989",
    },
    "tommy-west": {
        "name": "Tommy West", "born": None, "alma_mater": None,
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Clemson (interim)", "Memphis", "Chattanooga"],
        "mentor": "ken-hatfield",
        "mentor_context": "DC at Clemson, 1990-92",
    },
    "david-bailiff": {
        "name": "David Bailiff", "born": None, "alma_mater": None,
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Texas State", "Rice"],
        "mentor": "ken-hatfield",
        "mentor_context": "DC at Rice, 2001-03",
    },

    # Gen 3 – Brian Kelly proteges
    "chuck-martin": {
        "name": "Chuck Martin", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Grand Valley State", "Miami (OH)"],
        "mentor": "brian-kelly",
        "mentor_context": "OC at Grand Valley State 2000-03; OC at Notre Dame 2012-13",
    },
    "butch-jones": {
        "name": "Butch Jones", "born": 1968, "alma_mater": "Ferris State",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Central Michigan", "Cincinnati", "Tennessee", "Arkansas State"],
        "mentor": "brian-kelly",
        "mentor_context": "OC at Central Michigan, 2004-06",
    },
    "jeff-quinn": {
        "name": "Jeff Quinn", "born": None, "alma_mater": None,
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Buffalo"],
        "mentor": "brian-kelly",
        "mentor_context": "OC at Cincinnati, 2007-09",
    },
    "bob-diaco": {
        "name": "Bob Diaco", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["UConn"],
        "mentor": "brian-kelly",
        "mentor_context": "DC at Notre Dame, 2010-13",
    },
    "mike-elko": {
        "name": "Mike Elko", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Duke", "Texas A&M"],
        "mentor": "brian-kelly",
        "mentor_context": "DC at Notre Dame, 2017",
    },
    "clark-lea": {
        "name": "Clark Lea", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Vanderbilt"],
        "mentor": "brian-kelly",
        "mentor_context": "DC at Notre Dame, 2018-20",
    },
    "brian-polian": {
        "name": "Brian Polian", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Nevada"],
        "mentor": "brian-kelly",
        "mentor_context": "ST Coordinator at Notre Dame, 2012-16",
    },

    # Gen 3 – Mark Dantonio proteges
    "harlon-barnett": {
        "name": "Harlon Barnett", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Michigan State (interim)"],
        "mentor": "mark-dantonio",
        "mentor_context": "DB Coach/Co-DC at Michigan State, 2007-2017",
    },
    "mike-tressel": {
        "name": "Mike Tressel", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Michigan State (interim)", "Wisconsin (interim)"],
        "mentor": "mark-dantonio",
        "mentor_context": "LB/ST/Co-DC at Michigan State, 2007-2019; DC at Cincinnati under Fickell, 2021-22",
    },

    # Gen 3 – Bret Bielema proteges
    "charlie-partridge": {
        "name": "Charlie Partridge", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Florida Atlantic"],
        "mentor": "bret-bielema",
        "mentor_context": "DL Coach at Wisconsin, 2008-12",
    },
    "sam-pittman": {
        "name": "Sam Pittman", "born": 1961, "alma_mater": "Pittsburg State",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Arkansas"],
        "mentor": "bret-bielema",
        "mentor_context": "OL Coach at Arkansas, 2013-15",
    },
    "barry-lunney-jr": {
        "name": "Barry Lunney Jr.", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Arkansas (interim)", "UTSA"],
        "mentor": "bret-bielema",
        "mentor_context": "TE Coach at Arkansas, 2013-19",
    },

    # Gen 3 – Ryan Day proteges
    "kevin-wilson": {
        "name": "Kevin Wilson", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Tulsa"],
        "mentor": "ryan-day",
        "mentor_context": "OC/TE at Ohio State, 2019-22",
    },

    # Gen 3 – Dan Mullen proteges
    "geoff-collins": {
        "name": "Geoff Collins", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Temple", "Georgia Tech"],
        "mentor": "dan-mullen",
        "mentor_context": "Co-DC/LB Coach at Mississippi State, 2011-14",
    },
    "tony-hughes": {
        "name": "Tony Hughes", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Jackson State", "Mississippi Valley State"],
        "mentor": "dan-mullen",
        "mentor_context": "Safeties Coach at Mississippi State, 2009-15",
    },

    # Gen 3 – Tom Herman proteges
    "major-applewhite": {
        "name": "Major Applewhite", "born": 1979, "alma_mater": "Texas",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Houston"],
        "mentor": "tom-herman",
        "mentor_context": "OC/QB Coach at Houston, 2015-16",
    },

    # Gen 3 – Greg Schiano proteges
    "mario-cristobal": {
        "name": "Mario Cristobal", "born": 1970, "alma_mater": "Miami (FL)",
        "current_status": "active", "generation": 3,
        "hc_schools": ["FIU", "Oregon", "Miami (FL)"],
        "mentor": "greg-schiano",
        "mentor_context": "OL Coach at Rutgers, 2001-03",
    },
    "kyle-flood": {
        "name": "Kyle Flood", "born": None, "alma_mater": None,
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Rutgers"],
        "mentor": "greg-schiano",
        "mentor_context": "OL Coach at Rutgers, 2005-11",
    },
    "joe-susan": {
        "name": "Joe Susan", "born": None, "alma_mater": None,
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Bucknell"],
        "mentor": "greg-schiano",
        "mentor_context": "TE Coach at Rutgers, 2001-09",
    },
    "pj-fleck": {
        "name": "P.J. Fleck", "born": 1980, "alma_mater": "Northern Illinois",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Western Michigan", "Minnesota"],
        "mentor": "greg-schiano",
        "mentor_context": "WR Coach at Tampa Bay Buccaneers, 2012",
    },

    # Gen 3 – Lane Kiffin proteges
    "clay-helton": {
        "name": "Clay Helton", "born": 1973, "alma_mater": "Houston",
        "current_status": "active", "generation": 3,
        "hc_schools": ["USC"],
        "mentor": "lane-kiffin",
        "mentor_context": "QB Coach at USC, 2010-13",
    },

    # Gen 3 – Ed Orgeron proteges
    "hugh-freeze": {
        "name": "Hugh Freeze", "born": 1969, "alma_mater": "Southern Mississippi",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Arkansas State", "Ole Miss", "Liberty", "Auburn"],
        "mentor": "ed-orgeron",
        "mentor_context": "Asst/TE Coach at Ole Miss, 2006-07",
    },
    "dave-aranda": {
        "name": "Dave Aranda", "born": 1977, "alma_mater": "Cal Lutheran",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Baylor"],
        "mentor": "ed-orgeron",
        "mentor_context": "DC at LSU, 2016-19",
    },
    "bo-pelini": {
        "name": "Bo Pelini", "born": 1969, "alma_mater": "Ohio State",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Youngstown State", "Nebraska"],
        "mentor": "ed-orgeron",
        "mentor_context": "DC at LSU, 2020",
        "notes": "Had prior HC career (Nebraska 2008-14) before joining Orgeron",
    },

    # Gen 3 – Ralph Friedgen proteges
    "james-franklin": {
        "name": "James Franklin", "born": 1972, "alma_mater": "East Stroudsburg",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Vanderbilt", "Penn State"],
        "mentor": "ralph-friedgen",
        "mentor_context": "OC at Maryland, 2008-10",
    },
    "mike-locksley": {
        "name": "Mike Locksley", "born": 1969, "alma_mater": "Towson",
        "current_status": "active", "generation": 3,
        "hc_schools": ["New Mexico", "Maryland"],
        "mentor": "ralph-friedgen",
        "mentor_context": "RB Coach at Maryland, 1997-2002",
    },
    "bill-obrien": {
        "name": "Bill O'Brien", "born": 1969, "alma_mater": "Brown",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Penn State", "Houston Texans", "Boston College"],
        "mentor": "ralph-friedgen",
        "mentor_context": "RB Coach at Maryland, 2003-04",
    },

    # Gen 3 – Tony Dungy proteges
    "jim-caldwell": {
        "name": "Jim Caldwell", "born": 1955, "alma_mater": "Iowa",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Indianapolis Colts", "Detroit Lions"],
        "mentor": "tony-dungy",
        "mentor_context": "AHC/QB Coach at Indianapolis Colts, 2002-08",
    },
    "leslie-frazier": {
        "name": "Leslie Frazier", "born": 1959, "alma_mater": "Alcorn State",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Minnesota Vikings"],
        "mentor": "tony-dungy",
        "mentor_context": "DB Coach at Indianapolis Colts, 2005-06",
    },

    # Gen 3 – Mike Tomlin proteges
    "bruce-arians": {
        "name": "Bruce Arians", "born": 1952, "alma_mater": "Virginia Tech",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Arizona Cardinals", "Tampa Bay Buccaneers"],
        "mentor": "mike-tomlin",
        "mentor_context": "OC at Pittsburgh Steelers, 2007-11",
    },

    # Gen 3 – John Harbaugh proteges
    "gary-kubiak": {
        "name": "Gary Kubiak", "born": 1961, "alma_mater": "Texas A&M",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Houston Texans", "Denver Broncos"],
        "mentor": "john-harbaugh",
        "mentor_context": "OC at Baltimore Ravens, 2014",
    },
    "david-culley": {
        "name": "David Culley", "born": 1955, "alma_mater": "Vanderbilt",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Houston Texans"],
        "mentor": "john-harbaugh",
        "mentor_context": "AHC/WR Coach at Baltimore Ravens, 2019-20",
    },

    # Gen 3 – Lovie Smith proteges
    "ron-rivera": {
        "name": "Ron Rivera", "born": 1962, "alma_mater": "California",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Carolina Panthers", "Washington Commanders"],
        "mentor": "lovie-smith",
        "mentor_context": "DC at Chicago Bears, 2004-06",
    },

    # Gen 3 – Herm Edwards proteges
    "todd-haley": {
        "name": "Todd Haley", "born": 1967, "alma_mater": "Miami (OH)",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Kansas City Chiefs"],
        "mentor": "herm-edwards",
        "mentor_context": "WR Coach at New York Jets, 2001-03",
    },
    "mike-nolan": {
        "name": "Mike Nolan", "born": 1959, "alma_mater": "Oregon",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["San Francisco 49ers"],
        "mentor": "herm-edwards",
        "mentor_context": "DC at New York Jets, 2001-04",
    },

    # Gen 3 – Gus Bradley proteges
    "doug-marrone": {
        "name": "Doug Marrone", "born": 1964, "alma_mater": "Syracuse",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Syracuse", "Buffalo Bills", "Jacksonville Jaguars"],
        "mentor": "gus-bradley",
        "mentor_context": "AHC/OL Coach at Jacksonville Jaguars, 2015-16",
    },

    # Gen 3 – Mike Smith (HC) proteges
    "dirk-koetter": {
        "name": "Dirk Koetter", "born": 1959, "alma_mater": "Idaho",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Tampa Bay Buccaneers"],
        "mentor": "mike-smith-hc",
        "mentor_context": "OC at Atlanta Falcons, 2012-14",
    },
    "mike-mularkey": {
        "name": "Mike Mularkey", "born": 1961, "alma_mater": "Florida",
        "current_status": "retired", "generation": 3,
        "hc_schools": ["Jacksonville Jaguars", "Tennessee Titans"],
        "mentor": "mike-smith-hc",
        "mentor_context": "OC at Atlanta Falcons, 2008-11",
    },

    # Gen 3 – Gary Andersen proteges
    "matt-wells": {
        "name": "Matt Wells", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Utah State", "Texas Tech"],
        "mentor": "gary-andersen",
        "mentor_context": "OC at Utah State, 2011-12",
    },

    # Gen 3 – Dave Doeren proteges
    "eliah-drinkwitz": {
        "name": "Eliah Drinkwitz", "born": 1983, "alma_mater": "Northwest Missouri State",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Appalachian State", "Missouri"],
        "mentor": "dave-doeren",
        "mentor_context": "OC at NC State, 2015",
    },
    "matt-canada": {
        "name": "Matt Canada", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["Maryland (interim)"],
        "mentor": "dave-doeren",
        "mentor_context": "OC at NC State, 2013-15",
    },

    # Gen 3 – Paul Chryst proteges
    "jim-leonhard": {
        "name": "Jim Leonhard", "born": 1982, "alma_mater": "Wisconsin",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Wisconsin (interim)"],
        "mentor": "paul-chryst",
        "mentor_context": "DC at Wisconsin, 2017-22",
    },

    # Gen 3 – Tim Beckman proteges
    "matt-campbell": {
        "name": "Matt Campbell", "born": 1980, "alma_mater": "Mount Union",
        "current_status": "active", "generation": 3,
        "hc_schools": ["Toledo", "Iowa State"],
        "mentor": "tim-beckman",
        "mentor_context": "OC at Toledo, 2009-11",
    },

    # Gen 3 – Doc Holliday proteges
    "tony-petersen": {
        "name": "Tony Petersen", "born": None, "alma_mater": None,
        "current_status": "active", "generation": 3,
        "hc_schools": ["East Carolina (interim)"],
        "mentor": "doc-holliday",
        "mentor_context": "OC at Marshall, 2010-12",
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# NEW RELATIONSHIPS
# ──────────────────────────────────────────────────────────────────────────────

NEW_RELATIONSHIPS = [
    # Pete Carroll primary proteges
    {"id": "carroll-to-sarkisian", "mentor_id": "pete-carroll", "protege_id": "steve-sarkisian",
     "school": "USC", "year_start": 2001, "year_end": 2006, "relationship_type": "direct_report",
     "protege_role": "QB Coach", "generation_gap": 1, "confidence": "high",
     "notes": "QB coach at USC under Carroll 2001-03, 2005-06; later HC at Washington, USC, Texas"},
    {"id": "carroll-to-quinn", "mentor_id": "pete-carroll", "protege_id": "dan-quinn",
     "school": "Seattle Seahawks", "year_start": 2013, "year_end": 2014, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Seattle under Carroll 2013-14; later HC at Atlanta Falcons, Dallas Cowboys"},
    {"id": "carroll-to-bevell", "mentor_id": "pete-carroll", "protege_id": "darrell-bevell",
     "school": "Seattle Seahawks", "year_start": 2011, "year_end": 2017, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Seattle under Carroll 2011-17; later interim HC at Detroit and Jacksonville"},

    # Pete Carroll cross-references (coaches already in DB)
    {"id": "carroll-to-lane-kiffin-usc", "mentor_id": "pete-carroll", "protege_id": "lane-kiffin",
     "school": "USC", "year_start": 2005, "year_end": 2006, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "Lane Kiffin was OC at USC under Carroll 2005-06 before his first HC job at Oakland Raiders"},
    {"id": "carroll-to-orgeron-usc", "mentor_id": "pete-carroll", "protege_id": "ed-orgeron",
     "school": "USC", "year_start": 2001, "year_end": 2004, "relationship_type": "direct_report",
     "protege_role": "defensive_line_coach", "generation_gap": 1, "confidence": "high",
     "notes": "Orgeron was DL coach under Carroll at USC 2001-04, preceding his Ole Miss HC stint"},
    {"id": "carroll-to-chow-usc", "mentor_id": "pete-carroll", "protege_id": "norm-chow",
     "school": "USC", "year_start": 2001, "year_end": 2004, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "Norm Chow was OC at USC under Carroll 2001-04 before Hawaii HC job"},
    {"id": "carroll-to-gus-bradley-sea", "mentor_id": "pete-carroll", "protege_id": "gus-bradley",
     "school": "Seattle Seahawks", "year_start": 2010, "year_end": 2012, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "Gus Bradley was DC at Seattle under Carroll 2010-12 before Jacksonville HC job"},

    # Jimmy Johnson proteges
    {"id": "johnson-to-butch-davis", "mentor_id": "jimmy-johnson", "protege_id": "butch-davis",
     "school": "multiple", "year_start": 1979, "year_end": 1992, "relationship_type": "direct_report",
     "protege_role": "defensive_line_coach", "generation_gap": 1, "confidence": "high",
     "notes": "DL coach under Johnson at Oklahoma State 1979-83, Miami 1984-88, Dallas 1989-92"},
    {"id": "johnson-to-wannstedt", "mentor_id": "jimmy-johnson", "protege_id": "dave-wannstedt",
     "school": "multiple", "year_start": 1979, "year_end": 1992, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC under Johnson at Oklahoma State 1979-82, Miami 1986-88, Dallas 1989-92"},
    {"id": "johnson-to-tuberville", "mentor_id": "jimmy-johnson", "protege_id": "tommy-tuberville",
     "school": "Miami (FL)", "year_start": 1986, "year_end": 1987, "relationship_type": "direct_report",
     "protege_role": "defensive_line_coach", "generation_gap": 1, "confidence": "high",
     "notes": "DL coach at Miami (FL) under Johnson 1986-87; later HC at Ole Miss, Auburn, Texas Tech, Cincinnati"},
    {"id": "johnson-to-norv-turner", "mentor_id": "jimmy-johnson", "protege_id": "norv-turner",
     "school": "Dallas Cowboys", "year_start": 1991, "year_end": 1993, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Dallas under Johnson 1991-93; later HC at Washington, Oakland Raiders, San Diego Chargers"},

    # Joe Gibbs proteges
    {"id": "gibbs-to-petitbon", "mentor_id": "joe-gibbs", "protege_id": "richie-petitbon",
     "school": "Washington Redskins", "year_start": 1981, "year_end": 1992, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Washington under Gibbs 1981-92; succeeded him as interim HC in 1993"},
    {"id": "gibbs-to-bugel", "mentor_id": "joe-gibbs", "protege_id": "joe-bugel",
     "school": "Washington Redskins", "year_start": 1981, "year_end": 1989, "relationship_type": "direct_report",
     "protege_role": "offensive_line_coach", "generation_gap": 1, "confidence": "high",
     "notes": "OL coach at Washington under Gibbs 1981-89; later HC at Phoenix Cardinals, Oakland Raiders"},
    {"id": "gibbs-to-al-saunders", "mentor_id": "joe-gibbs", "protege_id": "al-saunders",
     "school": "Washington Redskins", "year_start": 1981, "year_end": 1982, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "high",
     "notes": "WR coach at Washington 1981-82; also Associate HC 2006-07; HC at San Diego Chargers 1986-88"},
    {"id": "gibbs-to-gregg-williams", "mentor_id": "joe-gibbs", "protege_id": "gregg-williams",
     "school": "Washington Redskins", "year_start": 2004, "year_end": 2007, "relationship_type": "direct_report",
     "protege_role": "assistant_head_coach", "generation_gap": 1, "confidence": "high",
     "notes": "AHC/Defense at Washington under Gibbs 2004-07; earlier HC at Buffalo Bills"},
    {"id": "gibbs-to-callahan", "mentor_id": "joe-gibbs", "protege_id": "bill-callahan",
     "school": "Washington Redskins", "year_start": 2005, "year_end": 2007, "relationship_type": "direct_report",
     "protege_role": "offensive_line_coach", "generation_gap": 1, "confidence": "high",
     "notes": "OL coach at Washington under Gibbs 2005-07; earlier HC at Oakland Raiders, Nebraska"},
    # Gibbs cross-reference: Dan Henning was OC under Gibbs before Holtz connection (Gen 1)
    {"id": "gibbs-to-henning", "mentor_id": "joe-gibbs", "protege_id": "dan-henning",
     "school": "Washington Redskins", "year_start": 1981, "year_end": 1982, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "Dan Henning was OC at Washington under Gibbs 1981-82; cross-reference (also in Holtz tree)"},

    # Ken Hatfield proteges
    {"id": "hatfield-to-houston-nutt", "mentor_id": "ken-hatfield", "protege_id": "houston-nutt",
     "school": "Arkansas", "year_start": 1989, "year_end": 1989, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "high",
     "notes": "WR coach at Arkansas under Hatfield 1989; later HC at Boise State, Arkansas, Ole Miss"},
    {"id": "hatfield-to-tommy-west", "mentor_id": "ken-hatfield", "protege_id": "tommy-west",
     "school": "Clemson", "year_start": 1990, "year_end": 1992, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Clemson under Hatfield 1990-92; later HC at Clemson (interim), Memphis, Chattanooga"},
    {"id": "hatfield-to-bailiff", "mentor_id": "ken-hatfield", "protege_id": "david-bailiff",
     "school": "Rice", "year_start": 2001, "year_end": 2003, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Rice under Hatfield 2001-03; later HC at Texas State, Rice"},

    # Brian Kelly proteges
    {"id": "kelly-to-chuck-martin", "mentor_id": "brian-kelly", "protege_id": "chuck-martin",
     "school": "Grand Valley State", "year_start": 2000, "year_end": 2003, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Grand Valley State 2000-03; also OC at Notre Dame 2012-13 under Kelly; HC at Miami (OH)"},
    {"id": "kelly-to-butch-jones", "mentor_id": "brian-kelly", "protege_id": "butch-jones",
     "school": "Central Michigan", "year_start": 2004, "year_end": 2006, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Central Michigan under Kelly 2004-06; later HC at CMU, Cincinnati, Tennessee, Arkansas State"},
    {"id": "kelly-to-jeff-quinn", "mentor_id": "brian-kelly", "protege_id": "jeff-quinn",
     "school": "Cincinnati", "year_start": 2007, "year_end": 2009, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Cincinnati under Kelly 2007-09; later HC at Buffalo"},
    {"id": "kelly-to-bob-diaco", "mentor_id": "brian-kelly", "protege_id": "bob-diaco",
     "school": "Notre Dame", "year_start": 2010, "year_end": 2013, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Notre Dame under Kelly 2010-13; later HC at UConn"},
    {"id": "kelly-to-mike-elko", "mentor_id": "brian-kelly", "protege_id": "mike-elko",
     "school": "Notre Dame", "year_start": 2017, "year_end": 2017, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Notre Dame under Kelly 2017; later HC at Duke, Texas A&M"},
    {"id": "kelly-to-clark-lea", "mentor_id": "brian-kelly", "protege_id": "clark-lea",
     "school": "Notre Dame", "year_start": 2018, "year_end": 2020, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Notre Dame under Kelly 2018-20; later HC at Vanderbilt"},
    {"id": "kelly-to-brian-polian", "mentor_id": "brian-kelly", "protege_id": "brian-polian",
     "school": "Notre Dame", "year_start": 2012, "year_end": 2016, "relationship_type": "direct_report",
     "protege_role": "special_teams_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "ST coordinator at Notre Dame under Kelly 2012-16; later HC at Nevada"},

    # Mark Dantonio proteges
    {"id": "dantonio-to-harlon-barnett", "mentor_id": "mark-dantonio", "protege_id": "harlon-barnett",
     "school": "Michigan State", "year_start": 2007, "year_end": 2017, "relationship_type": "direct_report",
     "protege_role": "defensive_backs_coach", "generation_gap": 1, "confidence": "high",
     "notes": "DB/Co-DC at Michigan State under Dantonio 2007-17; interim HC at MSU 2023"},
    {"id": "dantonio-to-mike-tressel", "mentor_id": "mark-dantonio", "protege_id": "mike-tressel",
     "school": "Michigan State", "year_start": 2007, "year_end": 2019, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "high",
     "notes": "LB/ST/Co-DC at MSU under Dantonio 2007-19; interim HC at MSU 2019; interim HC at Wisconsin 2023"},
    # Dantonio cross-references
    {"id": "dantonio-to-narduzzi-msu", "mentor_id": "mark-dantonio", "protege_id": "pat-narduzzi",
     "school": "Michigan State", "year_start": 2007, "year_end": 2014, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at MSU under Dantonio 2007-14; cross-reference (primary mentor: rick-minter at Cincinnati)"},
    {"id": "dantonio-to-treadwell-msu", "mentor_id": "mark-dantonio", "protege_id": "don-treadwell",
     "school": "Michigan State", "year_start": 2007, "year_end": 2010, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at MSU under Dantonio 2007-10; cross-reference (primary mentor: barry-alvarez)"},

    # Bret Bielema proteges
    {"id": "bielema-to-partridge", "mentor_id": "bret-bielema", "protege_id": "charlie-partridge",
     "school": "Wisconsin", "year_start": 2008, "year_end": 2012, "relationship_type": "direct_report",
     "protege_role": "defensive_line_coach", "generation_gap": 1, "confidence": "high",
     "notes": "DL coach at Wisconsin under Bielema 2008-12; later HC at Florida Atlantic"},
    {"id": "bielema-to-pittman", "mentor_id": "bret-bielema", "protege_id": "sam-pittman",
     "school": "Arkansas", "year_start": 2013, "year_end": 2015, "relationship_type": "direct_report",
     "protege_role": "offensive_line_coach", "generation_gap": 1, "confidence": "high",
     "notes": "OL coach at Arkansas under Bielema 2013-15; later HC at Arkansas"},
    {"id": "bielema-to-lunney", "mentor_id": "bret-bielema", "protege_id": "barry-lunney-jr",
     "school": "Arkansas", "year_start": 2013, "year_end": 2019, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "medium",
     "notes": "TE coach at Arkansas under Bielema 2013-19; interim HC at Arkansas, later HC at UTSA"},
    # Bielema cross-references
    {"id": "bielema-to-chryst", "mentor_id": "bret-bielema", "protege_id": "paul-chryst",
     "school": "Wisconsin", "year_start": 2006, "year_end": 2011, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Wisconsin under Bielema 2006-11; cross-reference (primary mentor: barry-alvarez)"},
    {"id": "bielema-to-doeren", "mentor_id": "bret-bielema", "protege_id": "dave-doeren",
     "school": "Wisconsin", "year_start": 2006, "year_end": 2010, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Wisconsin under Bielema 2006-10; cross-reference (primary mentor: barry-alvarez)"},
    {"id": "bielema-to-ash", "mentor_id": "bret-bielema", "protege_id": "chris-ash",
     "school": "Wisconsin", "year_start": 2010, "year_end": 2012, "relationship_type": "direct_report",
     "protege_role": "defensive_backs_coach", "generation_gap": 1, "confidence": "high",
     "notes": "DB coach at Wisconsin under Bielema 2010-12; cross-reference (primary mentor: urban-meyer)"},

    # Ryan Day proteges
    {"id": "day-to-kevin-wilson", "mentor_id": "ryan-day", "protege_id": "kevin-wilson",
     "school": "Ohio State", "year_start": 2019, "year_end": 2022, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC/TE at Ohio State under Day 2019-22; later HC at Tulsa"},
    # Day cross-reference
    {"id": "addazio-to-ryan-day", "mentor_id": "steve-addazio", "protege_id": "ryan-day",
     "school": "Boston College", "year_start": 2013, "year_end": 2014, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "Ryan Day was OC/QB at Boston College under Addazio 2013-14; cross-reference (primary mentor: urban-meyer)"},

    # Dan Mullen proteges
    {"id": "mullen-to-geoff-collins", "mentor_id": "dan-mullen", "protege_id": "geoff-collins",
     "school": "Mississippi State", "year_start": 2011, "year_end": 2014, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "Co-DC/LB coach at MSU under Mullen 2011-14; later HC at Temple, Georgia Tech"},
    {"id": "mullen-to-tony-hughes", "mentor_id": "dan-mullen", "protege_id": "tony-hughes",
     "school": "Mississippi State", "year_start": 2009, "year_end": 2015, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "high",
     "notes": "Safeties coach at MSU under Mullen 2009-15; later HC at Jackson State, Mississippi Valley State"},
    # Mullen cross-reference
    {"id": "mullen-to-manny-diaz", "mentor_id": "dan-mullen", "protege_id": "manny-diaz",
     "school": "Mississippi State", "year_start": 2010, "year_end": 2015, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at MSU under Mullen 2010 and 2015; cross-reference (primary mentor: chuck-amato)"},

    # Tom Herman proteges
    {"id": "herman-to-applewhite", "mentor_id": "tom-herman", "protege_id": "major-applewhite",
     "school": "Houston", "year_start": 2015, "year_end": 2016, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Houston under Herman 2015-16; succeeded Herman as HC at Houston"},

    # Greg Schiano proteges
    {"id": "schiano-to-cristobal", "mentor_id": "greg-schiano", "protege_id": "mario-cristobal",
     "school": "Rutgers", "year_start": 2001, "year_end": 2003, "relationship_type": "direct_report",
     "protege_role": "offensive_line_coach", "generation_gap": 1, "confidence": "high",
     "notes": "OL coach at Rutgers under Schiano 2001-03; later HC at FIU, Oregon, Miami (FL)"},
    {"id": "schiano-to-kyle-flood", "mentor_id": "greg-schiano", "protege_id": "kyle-flood",
     "school": "Rutgers", "year_start": 2005, "year_end": 2011, "relationship_type": "direct_report",
     "protege_role": "offensive_line_coach", "generation_gap": 1, "confidence": "high",
     "notes": "OL coach at Rutgers under Schiano 2005-11; succeeded him as HC at Rutgers"},
    {"id": "schiano-to-joe-susan", "mentor_id": "greg-schiano", "protege_id": "joe-susan",
     "school": "Rutgers", "year_start": 2001, "year_end": 2009, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "high",
     "notes": "TE coach at Rutgers under Schiano 2001-09; later HC at Bucknell"},
    {"id": "schiano-to-pj-fleck", "mentor_id": "greg-schiano", "protege_id": "pj-fleck",
     "school": "Tampa Bay Buccaneers", "year_start": 2012, "year_end": 2012, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "high",
     "notes": "WR coach at Tampa Bay under Schiano 2012; later HC at Western Michigan, Minnesota"},

    # Lane Kiffin proteges
    {"id": "lane-kiffin-to-helton", "mentor_id": "lane-kiffin", "protege_id": "clay-helton",
     "school": "USC", "year_start": 2010, "year_end": 2013, "relationship_type": "direct_report",
     "protege_role": "QB Coach", "generation_gap": 1, "confidence": "high",
     "notes": "QB coach at USC under Lane Kiffin 2010-13; later interim then HC at USC"},

    # Ed Orgeron proteges
    {"id": "orgeron-to-hugh-freeze", "mentor_id": "ed-orgeron", "protege_id": "hugh-freeze",
     "school": "Ole Miss", "year_start": 2006, "year_end": 2007, "relationship_type": "direct_report",
     "protege_role": "assistant_coach", "generation_gap": 1, "confidence": "high",
     "notes": "Asst/TE coach at Ole Miss under Orgeron 2006-07; later HC at Arkansas State, Ole Miss, Liberty, Auburn"},
    {"id": "orgeron-to-dave-aranda", "mentor_id": "ed-orgeron", "protege_id": "dave-aranda",
     "school": "LSU", "year_start": 2016, "year_end": 2019, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at LSU under Orgeron 2016-19; later HC at Baylor"},
    {"id": "orgeron-to-bo-pelini", "mentor_id": "ed-orgeron", "protege_id": "bo-pelini",
     "school": "LSU", "year_start": 2020, "year_end": 2020, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "medium",
     "notes": "DC at LSU under Orgeron 2020; had prior HC career at Nebraska 2008-14"},
    {"id": "orgeron-to-helton-usc", "mentor_id": "ed-orgeron", "protege_id": "clay-helton",
     "school": "USC", "year_start": 2013, "year_end": 2013, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at USC under Orgeron (interim) 2013; cross-reference (primary mentor: lane-kiffin)"},
    # Ed Orgeron cross-reference with Gary Andersen
    {"id": "andersen-to-dave-aranda", "mentor_id": "gary-andersen", "protege_id": "dave-aranda",
     "school": "Wisconsin", "year_start": 2013, "year_end": 2014, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Wisconsin under Andersen 2013-14; cross-reference (primary mentor: ed-orgeron at LSU)"},

    # Ralph Friedgen proteges
    {"id": "friedgen-to-james-franklin", "mentor_id": "ralph-friedgen", "protege_id": "james-franklin",
     "school": "Maryland", "year_start": 2008, "year_end": 2010, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Maryland under Friedgen 2008-10; later HC at Vanderbilt, Penn State"},
    {"id": "friedgen-to-mike-locksley", "mentor_id": "ralph-friedgen", "protege_id": "mike-locksley",
     "school": "Maryland", "year_start": 1997, "year_end": 2002, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "high",
     "notes": "RB coach at Maryland under Friedgen 1997-2002; later HC at New Mexico, Maryland"},
    {"id": "friedgen-to-bill-obrien", "mentor_id": "ralph-friedgen", "protege_id": "bill-obrien",
     "school": "Maryland", "year_start": 2003, "year_end": 2004, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "high",
     "notes": "RB coach at Maryland under Friedgen 2003-04; later HC at Penn State, Houston Texans"},

    # Tony Dungy proteges
    {"id": "dungy-to-jim-caldwell", "mentor_id": "tony-dungy", "protege_id": "jim-caldwell",
     "school": "Indianapolis Colts", "year_start": 2002, "year_end": 2008, "relationship_type": "direct_report",
     "protege_role": "assistant_head_coach", "generation_gap": 1, "confidence": "high",
     "notes": "AHC/QB coach at Indianapolis under Dungy 2002-08; succeeded him as HC, won Super Bowl XLV"},
    {"id": "dungy-to-leslie-frazier", "mentor_id": "tony-dungy", "protege_id": "leslie-frazier",
     "school": "Indianapolis Colts", "year_start": 2005, "year_end": 2006, "relationship_type": "direct_report",
     "protege_role": "defensive_backs_coach", "generation_gap": 1, "confidence": "high",
     "notes": "DB coach at Indianapolis under Dungy 2005-06; later HC at Minnesota Vikings 2010-13"},
    # Dungy cross-references
    {"id": "dungy-to-lovie-smith", "mentor_id": "tony-dungy", "protege_id": "lovie-smith",
     "school": "Tampa Bay Buccaneers", "year_start": 1996, "year_end": 2000, "relationship_type": "direct_report",
     "protege_role": "linebackers_coach", "generation_gap": 1, "confidence": "high",
     "notes": "LB coach at Tampa Bay under Dungy 1996-2000; cross-reference (primary mentor: monte-kiffin)"},
    {"id": "dungy-to-herm-edwards", "mentor_id": "tony-dungy", "protege_id": "herm-edwards",
     "school": "Tampa Bay Buccaneers", "year_start": 1996, "year_end": 2000, "relationship_type": "direct_report",
     "protege_role": "defensive_backs_coach", "generation_gap": 1, "confidence": "high",
     "notes": "DB coach at Tampa Bay under Dungy 1996-2000; cross-reference (primary mentor: monte-kiffin)"},

    # Mike Tomlin proteges
    {"id": "tomlin-to-bruce-arians", "mentor_id": "mike-tomlin", "protege_id": "bruce-arians",
     "school": "Pittsburgh Steelers", "year_start": 2007, "year_end": 2011, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Pittsburgh under Tomlin 2007-11; later HC at Arizona Cardinals, Tampa Bay Buccaneers"},

    # John Harbaugh proteges
    {"id": "harbaugh-to-gary-kubiak", "mentor_id": "john-harbaugh", "protege_id": "gary-kubiak",
     "school": "Baltimore Ravens", "year_start": 2014, "year_end": 2014, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Baltimore under Harbaugh 2014; also HC at Houston Texans (2006-13), Denver Broncos (2015-16)"},
    {"id": "harbaugh-to-david-culley", "mentor_id": "john-harbaugh", "protege_id": "david-culley",
     "school": "Baltimore Ravens", "year_start": 2019, "year_end": 2020, "relationship_type": "direct_report",
     "protege_role": "assistant_head_coach", "generation_gap": 1, "confidence": "high",
     "notes": "AHC/WR coach at Baltimore under Harbaugh 2019-20; later HC at Houston Texans"},
    # Harbaugh cross-reference: Chuck Pagano
    {"id": "harbaugh-to-pagano", "mentor_id": "john-harbaugh", "protege_id": "chuck-pagano",
     "school": "Baltimore Ravens", "year_start": 2008, "year_end": 2011, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Baltimore under Harbaugh 2008-11; cross-reference (primary mentor: jim-strong)"},

    # Lovie Smith proteges
    {"id": "lovie-to-ron-rivera", "mentor_id": "lovie-smith", "protege_id": "ron-rivera",
     "school": "Chicago Bears", "year_start": 2004, "year_end": 2006, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Chicago under Lovie Smith 2004-06; later HC at Carolina Panthers, Washington Commanders"},
    # Lovie cross-reference: Leslie Frazier
    {"id": "childress-to-leslie-frazier", "mentor_id": "brad-childress", "protege_id": "leslie-frazier",
     "school": "Minnesota Vikings", "year_start": 2007, "year_end": 2010, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Minnesota under Childress 2007-10; succeeded him as HC 2010-13; cross-reference (primary mentor: tony-dungy)"},

    # Herm Edwards proteges
    {"id": "edwards-to-todd-haley", "mentor_id": "herm-edwards", "protege_id": "todd-haley",
     "school": "New York Jets", "year_start": 2001, "year_end": 2003, "relationship_type": "direct_report",
     "protege_role": "position_coach", "generation_gap": 1, "confidence": "high",
     "notes": "WR coach at NY Jets under Edwards 2001-03; later HC at Kansas City Chiefs 2009-11"},
    {"id": "edwards-to-mike-nolan", "mentor_id": "herm-edwards", "protege_id": "mike-nolan",
     "school": "New York Jets", "year_start": 2001, "year_end": 2004, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at NY Jets under Edwards 2001-04; later HC at San Francisco 49ers 2005-08"},

    # Gus Bradley proteges
    {"id": "bradley-to-doug-marrone", "mentor_id": "gus-bradley", "protege_id": "doug-marrone",
     "school": "Jacksonville Jaguars", "year_start": 2015, "year_end": 2016, "relationship_type": "direct_report",
     "protege_role": "assistant_head_coach", "generation_gap": 1, "confidence": "high",
     "notes": "AHC/OL at Jacksonville under Bradley 2015-16; succeeded him as HC at Jacksonville"},

    # Mike Smith (HC) proteges
    {"id": "mikesmith-to-dirk-koetter", "mentor_id": "mike-smith-hc", "protege_id": "dirk-koetter",
     "school": "Atlanta Falcons", "year_start": 2012, "year_end": 2014, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Atlanta under Mike Smith 2012-14; later HC at Tampa Bay Buccaneers"},
    {"id": "mikesmith-to-mike-mularkey", "mentor_id": "mike-smith-hc", "protege_id": "mike-mularkey",
     "school": "Atlanta Falcons", "year_start": 2008, "year_end": 2011, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Atlanta under Mike Smith 2008-11; later HC at Jacksonville Jaguars, Tennessee Titans"},

    # Gary Andersen proteges
    {"id": "andersen-to-matt-wells", "mentor_id": "gary-andersen", "protege_id": "matt-wells",
     "school": "Utah State", "year_start": 2011, "year_end": 2012, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Utah State under Andersen 2011-12; succeeded him as HC at Utah State; later HC at Texas Tech"},

    # Dave Doeren proteges
    {"id": "doeren-to-eliah-drinkwitz", "mentor_id": "dave-doeren", "protege_id": "eliah-drinkwitz",
     "school": "NC State", "year_start": 2015, "year_end": 2015, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at NC State under Doeren 2015; later HC at Appalachian State, Missouri"},
    {"id": "doeren-to-matt-canada", "mentor_id": "dave-doeren", "protege_id": "matt-canada",
     "school": "NC State", "year_start": 2013, "year_end": 2015, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at NC State under Doeren 2013-15; interim HC at Maryland 2018"},
    # Narduzzi cross-reference for Matt Canada
    {"id": "narduzzi-to-matt-canada", "mentor_id": "pat-narduzzi", "protege_id": "matt-canada",
     "school": "Pittsburgh", "year_start": 2016, "year_end": 2016, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Pittsburgh under Narduzzi 2016; cross-reference (primary mentor: dave-doeren)"},

    # Paul Chryst proteges
    {"id": "chryst-to-jim-leonhard", "mentor_id": "paul-chryst", "protege_id": "jim-leonhard",
     "school": "Wisconsin", "year_start": 2017, "year_end": 2022, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Wisconsin under Chryst 2017-22; interim HC at Wisconsin 2022"},

    # Tim Beckman proteges
    {"id": "beckman-to-matt-campbell", "mentor_id": "tim-beckman", "protege_id": "matt-campbell",
     "school": "Toledo", "year_start": 2009, "year_end": 2011, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "OC at Toledo under Beckman 2009-11; succeeded him as HC at Toledo; later HC at Iowa State"},

    # Fickell cross-reference: Mike Tressel at Cincinnati
    {"id": "fickell-to-mike-tressel", "mentor_id": "luke-fickell", "protege_id": "mike-tressel",
     "school": "Cincinnati", "year_start": 2021, "year_end": 2022, "relationship_type": "direct_report",
     "protege_role": "defensive_coordinator", "generation_gap": 1, "confidence": "high",
     "notes": "DC at Cincinnati under Fickell 2021-22; served as interim HC at Wisconsin when Fickell was hired"},

    # Doc Holliday proteges
    {"id": "holliday-to-tony-petersen", "mentor_id": "doc-holliday", "protege_id": "tony-petersen",
     "school": "Marshall", "year_start": 2010, "year_end": 2012, "relationship_type": "direct_report",
     "protege_role": "offensive_coordinator", "generation_gap": 1, "confidence": "medium",
     "notes": "OC at Marshall under Holliday 2010-12; later interim HC at East Carolina 2022"},
]

# ──────────────────────────────────────────────────────────────────────────────
# APPLY CHANGES
# ──────────────────────────────────────────────────────────────────────────────

already_in_db = [k for k in NEW_COACHES if k in coaches]
truly_new = {k: v for k, v in NEW_COACHES.items() if k not in coaches}

coaches.update(truly_new)

new_rels_added = []
rels_skipped = []
for rel in NEW_RELATIONSHIPS:
    if rel["id"] in existing_rel_ids:
        rels_skipped.append(rel["id"])
    else:
        relationships.append(rel)
        new_rels_added.append(rel["id"])

with open(coaches_path, "w") as f:
    json.dump(coaches, f, indent=2)

with open(relationships_path, "w") as f:
    json.dump(relationships, f, indent=2)

# ──────────────────────────────────────────────────────────────────────────────
# CROSS-REFERENCE REPORT
# ──────────────────────────────────────────────────────────────────────────────

print("=" * 70)
print("PARSE & CROSS-REFERENCE REPORT")
print("=" * 70)

print(f"\n✓ New coaches added:    {len(truly_new)}")
for k, v in truly_new.items():
    gen = v["generation"]
    mentor = v.get("mentor", "—")
    print(f"   Gen {gen}  {v['name']:30s}  (mentor: {mentor})")

print(f"\n⚠  Already in DB (no duplicate): {len(already_in_db)}")
for k in already_in_db:
    print(f"   {k}")

print(f"\n✓ New relationships added: {len(new_rels_added)}")
print(f"⚠  Relationships skipped (already exist): {len(rels_skipped)}")

# ──────────────────────────────────────────────────────────────────────────────
# GAP ANALYSIS
# ──────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("GAP ANALYSIS")
print("=" * 70)

# Coaches by generation
from collections import defaultdict
gen_counts = defaultdict(list)
for k, v in coaches.items():
    gen_counts[v["generation"]].append(v["name"])

print("\nCoaches by generation:")
for g in sorted(gen_counts.keys()):
    print(f"  Gen {g:2d}: {len(gen_counts[g])} coaches")

# Coaches with no outgoing relationships (leaf nodes = no proteges who became HCs)
all_mentors = {r["mentor_id"] for r in relationships}
all_proteges = {r["protege_id"] for r in relationships}

leaf_coaches = []
for k, v in coaches.items():
    gen = v["generation"]
    if gen <= 2 and k not in all_mentors:
        leaf_coaches.append((gen, v["name"], k))

leaf_coaches.sort()
print(f"\nGen 0-2 coaches with NO documented proteges ({len(leaf_coaches)}):")
for gen, name, key in leaf_coaches:
    print(f"  Gen {gen}  {name}")

# Coaches with missing birth year or alma mater
missing_bio = [(v["name"], k) for k, v in coaches.items()
               if v.get("born") is None or v.get("alma_mater") is None]
print(f"\nCoaches with incomplete bio data (born/alma_mater): {len(missing_bio)}")

# Gen 3 coaches who have NO proteges at all (expected, but note for future research)
gen3_no_proteges = [(v["name"], k) for k, v in coaches.items()
                    if v["generation"] == 3 and k not in all_mentors]
print(f"\nGen-3 coaches not yet researched for their own trees: {len(gen3_no_proteges)}")
for name, key in sorted(gen3_no_proteges):
    print(f"   {name}")

# Summary stats
total_coaches = len(coaches)
total_rels = len(relationships)
print(f"\n{'─'*70}")
print(f"TOTALS: {total_coaches} coaches | {total_rels} relationships")
print(f"{'─'*70}")
