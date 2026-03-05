#!/usr/bin/env python3
"""
Coaching Tree Research Automation
Runs all research queries through the OpenAI API and saves results to markdown files.

Usage:
    # Set your API key
    export OPENAI_API_KEY="sk-..."

    # Run all queries
    python run_research.py

    # Run a specific query by number
    python run_research.py --query 1

    # Run a range of queries
    python run_research.py --from 7 --to 20

    # List all queries without running them
    python run_research.py --list

    # Use a different model (default: gpt-4o)
    python run_research.py --model gpt-4o-mini
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

# Output directory
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "research" / "chatgpt"
PROGRESS_FILE = OUTPUT_DIR / "_progress.json"

# System prompt for all queries
SYSTEM_PROMPT = """You are a college football coaching history expert. You are helping build a comprehensive coaching tree database tracing Lou Holtz's coaching lineage.

IMPORTANT RULES:
- Only include connections you are reasonably confident about
- Mark each entry with a confidence level: high, medium, or low
- If you are uncertain about specific years, give your best estimate and mark as medium/low confidence
- Do NOT fabricate connections — if you don't know, say "None found" or mark as low confidence
- Include coaches at ALL levels: NFL, FBS, FCS, D2, D3, NAIA
- "Head coach" includes interim head coaches — mark those as (interim) in the HC stops column

OUTPUT FORMAT:
- Use markdown tables as specified in the prompt
- After the table, add a "## Notes" section for any caveats, uncertain connections, or additional context
- If a coach had no assistants who became HCs, explicitly state "None found"
"""

# All research queries — each is a tuple of (filename, prompt)
QUERIES = [
    # === PHASE 1: Gen 1 Gaps ===
    (
        "01_pete_carroll",
        """I'm building a coaching tree database for college football, specifically tracing Lou Holtz's coaching lineage. Pete Carroll was a graduate assistant under Holtz at Arkansas in 1977 before going on to a legendary coaching career.

I need to identify all assistant coaches who worked under Pete Carroll during his head coaching career and later became head coaches themselves (at any level: NFL, FBS, FCS, D2, NAIA).

Pete Carroll was head coach at:
- New York Jets (1994, 1 season)
- New England Patriots (1997-99)
- USC (2001-09)
- Seattle Seahawks (2010-2023)
- Las Vegas Raiders (2025-)

For each assistant who later became a head coach, provide a markdown table organized by team:

### [Team Name]

| Name | Role Under Carroll | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|

Focus on verifiable connections. Include low-confidence entries rather than omitting them."""
    ),
    (
        "02_jimmy_johnson",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Jimmy Johnson was Holtz's defensive coordinator at Arkansas (1977-78) before becoming one of the most successful coaches in football history.

I need to identify all assistant coaches who worked under Jimmy Johnson during his head coaching career and later became head coaches themselves (NFL, FBS, FCS, D2, or lower).

Jimmy Johnson was head coach at:
- Oklahoma State (1979-83)
- Miami, FL (1984-88)
- Dallas Cowboys (1989-93)
- Miami Dolphins (1996-99)

For each assistant who later became a head coach, provide a markdown table organized by team:

### [Team Name]

| Name | Role Under Johnson | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|

The Miami (FL) and Dallas staffs are especially important — those programs produced many future head coaches."""
    ),
    (
        "03_joe_gibbs",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Joe Gibbs was Holtz's offensive coordinator at Arkansas (1978-79) before becoming a Pro Football Hall of Fame head coach.

I need to identify all assistant coaches who worked under Joe Gibbs during his head coaching career and later became head coaches themselves (NFL, FBS, FCS, or lower).

Joe Gibbs was head coach at:
- Washington Redskins (1981-92, first tenure)
- Washington Redskins (2004-07, second tenure)

For each assistant who later became a head coach, provide a markdown table:

### First Tenure (1981-92)

| Name | Role Under Gibbs | Years | Later HC Stops | Confidence |
|------|-----------------|-------|----------------|------------|

### Second Tenure (2004-07)

| Name | Role Under Gibbs | Years | Later HC Stops | Confidence |
|------|-----------------|-------|----------------|------------|"""
    ),
    (
        "04_ken_hatfield",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Ken Hatfield was an assistant under Holtz at Arkansas (1977-83) before a long head coaching career.

I need to identify all assistant coaches who worked under Ken Hatfield during his head coaching career and later became head coaches themselves (NFL, FBS, FCS, D2, or lower).

Ken Hatfield was head coach at:
- Air Force (1979-83)
- Arkansas (1984-89)
- Clemson (1990-93)
- Rice (1994-2005)

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Hatfield | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|"""
    ),
    (
        "05_batch_gen1_medium",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following head coaches (all former Holtz assistants), I need to know which of THEIR assistants later became head coaches.

For each coach, list any assistants who later became head coaches at any level (NFL, FBS, FCS, D2, NAIA). If none found, say "None found."

1. Skip Holtz (Lou's son) — HC at Connecticut (1994-98), East Carolina (2005-09), South Florida (2010-12), Louisiana Tech (2013-21), Marshall (2023-present)
2. Dave Roberts — HC at Western Kentucky, Northeast Louisiana, Baylor
3. Joker Phillips — HC at Kentucky (2010-12)
4. Rick Stockstill — HC at Middle Tennessee (2006-23)

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),
    (
        "06_batch_gen1_small",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following head coaches (all former Holtz assistants), I need to know which of THEIR assistants later became head coaches.

These are mostly small-program coaches so it's entirely possible some had no proteges who became HCs. If none found, say "None found."

1. Buddy Pough — HC at South Carolina State (2002-23, HBCU/FCS)
2. John Palermo — HC at Austin Peay (FCS, approximate years late 1990s-2000s)
3. Peter Vaas — HC at Holy Cross (1994-98, FCS)
4. Bo Rein — HC at NC State (1976-79, died in plane crash Jan 1980)
5. Ron Cooper — HC at Eastern Michigan (1993-94), Louisville (1995-97), Alabama A&M, Florida International

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),

    # === PHASE 2: Gen 2 → Gen 3 — College Big Trees ===
    (
        "07_brian_kelly",
        """I'm building a coaching tree database. Brian Kelly has been a head coach at multiple schools. I need to identify all assistant coaches who worked under Kelly and later became head coaches themselves.

Brian Kelly was head coach at:
- Grand Valley State (1991-2003, D2)
- Central Michigan (2004-06)
- Cincinnati (2007-09)
- Notre Dame (2010-21)
- LSU (2022-present)

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Kelly | Years | Later HC Stops | Confidence |
|------|-----------------|-------|----------------|------------|

The Notre Dame and LSU staffs are best documented but don't neglect the earlier stops."""
    ),
    (
        "08_mark_dantonio",
        """I'm building a coaching tree database. Mark Dantonio had a long career as a head coach. I need to identify all assistant coaches who worked under him and later became head coaches.

Mark Dantonio was head coach at:
- Cincinnati (2004-06)
- Michigan State (2007-19)

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Dantonio | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|

The Michigan State tenure (13 seasons) is the primary focus as it likely produced the most coaching branches."""
    ),
    (
        "09_bret_bielema",
        """I'm building a coaching tree database. Bret Bielema was a head coach at multiple schools. I need to identify all assistant coaches who worked under him and later became head coaches.

Bret Bielema was head coach at:
- Wisconsin (2006-12)
- Arkansas (2013-17)
- Illinois (2021-24)

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Bielema | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|"""
    ),
    (
        "10_luke_fickell",
        """I'm building a coaching tree database. I already have Marcus Freeman listed as a Luke Fickell protege (DC at Cincinnati, 2017-20 → Notre Dame HC). I need to identify any OTHER assistant coaches who worked under Fickell and later became head coaches.

Luke Fickell was head coach at:
- Ohio State (2011, interim)
- Cincinnati (2017-22)
- Wisconsin (2023-present)

For each assistant (BESIDES Marcus Freeman) who later became a head coach, provide:

| Name | School Under Fickell | Role | Years | Later HC Stops | Confidence |
|------|---------------------|------|-------|----------------|------------|"""
    ),
    (
        "11_ryan_day",
        """I'm building a coaching tree database. I already have Jeff Hafley (co-DC 2019 → Boston College HC) and Brian Hartline (WR coach → South Florida HC) listed as Ryan Day proteges. I need to identify any OTHER assistant coaches who worked under Day and later became head coaches.

Ryan Day has been head coach at:
- Ohio State (2019-present)

For each assistant (BESIDES Hafley and Hartline) who later became a head coach, provide:

| Name | Role Under Day | Years | Later HC Stops | Confidence |
|------|---------------|-------|----------------|------------|"""
    ),
    (
        "12_dan_mullen",
        """I'm building a coaching tree database. I need to identify all assistant coaches who worked under Dan Mullen and later became head coaches.

Dan Mullen was head coach at:
- Mississippi State (2009-17)
- Florida (2018-21)
- UNLV (2024-present)

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Mullen | Years | Later HC Stops | Confidence |
|------|------------------|-------|----------------|------------|"""
    ),
    (
        "13_tom_herman",
        """I'm building a coaching tree database. I need to identify all assistant coaches who worked under Tom Herman and later became head coaches.

Tom Herman was head coach at:
- Houston (2015-16)
- Texas (2017-20)

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Herman | Years | Later HC Stops | Confidence |
|------|------------------|-------|----------------|------------|"""
    ),
    (
        "14_greg_schiano",
        """I'm building a coaching tree database. I need to identify all assistant coaches who worked under Greg Schiano and later became head coaches.

Greg Schiano was head coach at:
- Rutgers (2001-11, first tenure)
- Tampa Bay Buccaneers (2012-13)
- Rutgers (2020-present, second tenure)

For each assistant who later became a head coach, provide a markdown table organized by team/school:

### [Team/School Name]

| Name | Role Under Schiano | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|"""
    ),
    (
        "15_pat_narduzzi",
        """I'm building a coaching tree database. I need to identify all assistant coaches who worked under Pat Narduzzi and later became head coaches.

Pat Narduzzi has been head coach at:
- Pittsburgh (2015-present)

For each assistant who later became a head coach, provide:

| Name | Role Under Narduzzi | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|"""
    ),
    (
        "16_lane_kiffin",
        """I'm building a coaching tree database. I need to identify all assistant coaches who worked under Lane Kiffin and later became head coaches.

Lane Kiffin was head coach at:
- Oakland Raiders (2007-08)
- Tennessee (2009, 1 season)
- USC (2010-13, fired midseason)
- Florida Atlantic (2017-19)
- Ole Miss (2020-present)

For each assistant who later became a head coach, provide a markdown table organized by team/school:

### [Team/School Name]

| Name | Role Under Kiffin | Years | Later HC Stops | Confidence |
|------|------------------|-------|----------------|------------|"""
    ),
    (
        "17_ed_orgeron",
        """I'm building a coaching tree database. I need to identify all assistant coaches who worked under Ed Orgeron and later became head coaches.

Ed Orgeron was head coach at:
- Ole Miss (2005-07)
- USC (2013, interim)
- LSU (2016-21, including 2019 national championship)

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Orgeron | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|

The 2019 LSU championship staff is especially notable."""
    ),
    (
        "18_jim_mora_jr",
        """I'm building a coaching tree database. I need to identify all assistant coaches who worked under Jim Mora Jr. and later became head coaches.

Jim Mora Jr. was head coach at:
- Atlanta Falcons (2004-06)
- Seattle Seahawks (2009, interim)
- UCLA (2012-17)
- UConn (2022-23)

For each assistant who later became a head coach, provide a markdown table organized by team/school:

### [Team/School Name]

| Name | Role Under Mora | Years | Later HC Stops | Confidence |
|------|----------------|-------|----------------|------------|"""
    ),
    (
        "19_ralph_friedgen",
        """I'm building a coaching tree database. I need to identify all assistant coaches who worked under Ralph Friedgen and later became head coaches.

Ralph Friedgen was head coach at:
- Maryland (2001-10)

For each assistant who later became a head coach, provide:

| Name | Role Under Friedgen | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|"""
    ),
    (
        "20_steve_addazio",
        """I'm building a coaching tree database. I need to identify all assistant coaches who worked under Steve Addazio and later became head coaches.

Steve Addazio was head coach at:
- Temple (2011-12)
- Boston College (2013-19)
- Colorado State (2020-21)

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Addazio | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|"""
    ),

    # === PHASE 3: NFL + Small College Batches ===
    (
        "21_batch_nfl_big",
        """I'm building a coaching tree database. For each of the following NFL head coaches, list any assistant coaches who worked under them and later became head coaches themselves (NFL or college, any level). I only need their direct-report assistants who became HCs.

1. Tony Dungy — HC at Tampa Bay Buccaneers (1996-2001), Indianapolis Colts (2002-08)
2. Mike Tomlin — HC at Pittsburgh Steelers (2007-present)
3. John Harbaugh — HC at Baltimore Ravens (2008-2024), New York Giants (2025-present)
4. Lovie Smith — HC at Chicago Bears (2004-12), Tampa Bay Buccaneers (2014-15), Houston Texans (2022)
5. Rex Ryan — HC at New York Jets (2009-14), Buffalo Bills (2015-16)

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If none found for a coach, say "None found." """
    ),
    (
        "22_batch_nfl_small",
        """I'm building a coaching tree database. For each of the following NFL head coaches, list any assistant coaches who worked under them and later became head coaches themselves. I only need direct-report assistants who became HCs.

1. Herm Edwards — HC at New York Jets (2001-05), Kansas City Chiefs (2006-08)
2. Raheem Morris — HC at Tampa Bay Buccaneers (2009-11), Atlanta Falcons (2024-present)
3. Gus Bradley — HC at Jacksonville Jaguars (2013-16)
4. Rod Marinelli — HC at Detroit Lions (2006-08)
5. Brad Childress — HC at Minnesota Vikings (2006-10)
6. Chuck Pagano — HC at Indianapolis Colts (2012-17)
7. Scott Linehan — HC at St. Louis Rams (2006-08)
8. Tom Cable — HC at Oakland Raiders (2008-10)
9. Gunther Cunningham — HC at Kansas City Chiefs (1999-2000)

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If none found, say "None found." """
    ),
    (
        "23_batch_college_small_a",
        """I'm building a coaching tree database. For each of the following college head coaches, list any assistant coaches who worked under them and later became head coaches (any level). If none found, say "None found."

1. Dan McCarney — HC at Iowa State (1995-2006), North Texas (2011-15)
2. Paul Chryst — HC at Pittsburgh (2012-14), Wisconsin (2015-22)
3. Gary Andersen — HC at Utah State (2009-12), Wisconsin (2013-14), Oregon State (2015-17)
4. Dave Doeren — HC at Northern Illinois (2011-12), NC State (2013-present)
5. Don Treadwell — HC at Miami of Ohio (2011, 1 season)
6. Chris Ash — HC at Rutgers (2016-19)
7. Everett Withers — HC at James Madison (2014-15), Texas State (2016-18)

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),
    (
        "24_batch_college_small_b",
        """I'm building a coaching tree database. For each of the following college head coaches, list any assistant coaches who worked under them and later became head coaches (any level). If none found, say "None found."

1. D.J. Durkin — HC at Maryland (2016-18)
2. Tim Beckman — HC at Toledo (2009-11), Illinois (2012-14)
3. Gregg Brandon — HC at Bowling Green (2003-08)
4. Stan Drayton — HC at Temple (2022-23)
5. Tim Beck — HC at Coastal Carolina (2023-present)
6. Jay Norvell — HC at Nevada (2017-21), Colorado State (2022-present)
7. Sterlin Gilbert — HC at McNeese State (2021-present)
8. Mike Sanford Sr. — HC at Indiana State (approximate years 2000s)

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),
    (
        "25_batch_college_small_c",
        """I'm building a coaching tree database. For each of the following college head coaches, list any assistant coaches who worked under them and later became head coaches (any level). If none found, say "None found."

1. Doc Holliday — HC at Marshall (2010-19)
2. Curt Cignetti — HC at IUP (D2), Elon (FCS), James Madison (2019-23), Indiana (2024-present)
3. Manny Diaz — HC at Miami FL (2019-21), Duke (2024-present)
4. Norm Chow — HC at Hawaii (2012-15)
5. Bill Cubit — HC at Western Michigan (2000-04), Illinois (2015, interim)
6. Dan Enos — HC at Central Michigan (2010-14)
7. Kevin Cosgrove — HC at New Mexico (interim)

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),
    (
        "26_batch_college_small_d",
        """I'm building a coaching tree database. For each of the following coaches, list any assistant coaches who worked under them and later became head coaches (any level). If none found, say "None found."

1. Ted Roof — HC at Duke (2003-07)
2. Jeff Horton — HC at UNLV (approximate years early 1990s-2000s)
3. Ted Tollner — HC at San Diego State (approximate years 1994-2001)
4. Mike Smith — HC at Atlanta Falcons (2008-14)
5. Jason Swepson — HC at Elon (approximate years 2010s)
6. Reggie Herring — HC at Houston (interim, approximate 2012)
7. Joe Pate — HC at Tennessee Tech (approximate years 2000s)
8. Bob DeBesse — HC at Southwest Minnesota State (D2)
9. Chip Long — HC at Tulane (2024-present)
10. Greg Colby — HC at Millersville (D2)
11. Dan Henson — HC at Eastern Illinois (approximate years 2000s)
12. Clifford Snow — HC at Connecticut (interim, approximate 1998)

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),

    # === PHASE 4: Gen 2 Remaining ===
    (
        "27_steve_sarkisian",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Steve Sarkisian worked under Pete Carroll at USC (2001-09) as offensive coordinator before becoming a head coach himself. Carroll worked under Lou Holtz at Arkansas (1977).

I need to identify all assistant coaches who worked under Sarkisian during his head coaching career and later became head coaches themselves (any level: NFL, FBS, FCS, D2, NAIA).

Steve Sarkisian was head coach at:
- Washington (2009-13)
- Texas (2021-present)

Note: His Alabama tenure (2016-20) was as offensive coordinator under Nick Saban, not as head coach.

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Sarkisian | Years | Later HC Stops | Confidence |
|------|---------------------|-------|----------------|------------|"""
    ),
    (
        "28_dan_quinn_batch",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. I need to identify assistants who worked under the following Gen 2 head coaches and later became head coaches themselves.

1. Dan Quinn — HC at Atlanta Falcons (2015-20), Dallas Cowboys (2024-present). Quinn worked under Pete Carroll at Seattle as defensive coordinator (2013-14).
2. Jim Colletto — HC at Purdue (1997-2001). Colletto worked under Barry Alvarez at Wisconsin as defensive line coach.

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If no assistants became head coaches, say "None found." """
    ),

    # === PHASE 5: Gen 3 Notable Individuals ===
    (
        "29_bruce_arians",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Bruce Arians worked under Mike Tomlin at Pittsburgh (2004-06) as offensive coordinator. Tomlin worked under Rick Minter (Cincinnati), who worked under Lou Holtz.

I need to identify all assistant coaches who worked under Bruce Arians during his head coaching career and later became head coaches themselves.

Bruce Arians was head coach at:
- Indianapolis Colts (interim, 2012)
- Arizona Cardinals (2013-17)
- Tampa Bay Buccaneers (2019-21)

For each assistant who later became a head coach, provide a markdown table organized by team:

### [Team Name]

| Name | Role Under Arians | Years | Later HC Stops | Confidence |
|------|------------------|-------|----------------|------------|

Notable assistants to check: Todd Bowles (DC → Jets HC, Chiefs HC), Byron Leftwich (OC), Harold Goodwin, others."""
    ),
    (
        "30_ron_rivera",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Ron Rivera worked under Lovie Smith (Chicago Bears, 2004-12) as defensive coordinator. Smith worked under Monte Kiffin, who was a Lou Holtz assistant at Arkansas.

I need to identify all assistant coaches who worked under Ron Rivera during his head coaching career and later became head coaches themselves.

Ron Rivera was head coach at:
- Carolina Panthers (2011-19)
- Washington Commanders (2020-23)

For each assistant who later became a head coach, provide a markdown table organized by team:

### [Team Name]

| Name | Role Under Rivera | Years | Later HC Stops | Confidence |
|------|------------------|-------|----------------|------------|"""
    ),
    (
        "31_james_franklin",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. James Franklin worked under Ralph Friedgen at Maryland (2007-10) as offensive coordinator. Friedgen worked under Bobby Ross, who was a Lou Holtz assistant at William & Mary.

I need to identify all assistant coaches who worked under James Franklin during his head coaching career and later became head coaches themselves (any level).

James Franklin was head coach at:
- Vanderbilt (2011-13)
- Penn State (2014-present)

For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Franklin | Years | Later HC Stops | Confidence |
|------|-------------------|-------|----------------|------------|

Penn State is the primary focus given the 10+ year tenure."""
    ),
    (
        "32_bill_obrien",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Bill O'Brien worked under Ralph Friedgen at Maryland as offensive coordinator (2002-04). Friedgen worked under Bobby Ross, who was a Lou Holtz assistant.

I need to identify all assistant coaches who worked under Bill O'Brien during his head coaching career and later became head coaches themselves.

Bill O'Brien was head coach at:
- Penn State (2012-13)
- Houston Texans (2014-19)
- Alabama (2023-present)

For each assistant who later became a head coach, provide a markdown table organized by team/school:

### [Team/School Name]

| Name | Role Under O'Brien | Years | Later HC Stops | Confidence |
|------|------------------|-------|----------------|------------|"""
    ),

    # === PHASE 6: Gen 3 NFL Batches ===
    (
        "33_gen3_nfl_batch_a",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following NFL head coaches (Generation 3 in the Holtz tree), identify assistants who worked under them and later became head coaches themselves.

1. Gary Kubiak — HC at Houston Texans (2006-13), Denver Broncos (2015-16). Connection: worked under John Harbaugh at Baltimore.
2. Jim Caldwell — HC at Indianapolis Colts (2009-11), Detroit Lions (2014-17). Connection: worked under Tony Dungy at Indianapolis.
3. Leslie Frazier — HC at Minnesota Vikings (2010-13, including interim). Connection: worked under Tony Dungy at Indianapolis and Tampa Bay.
4. Mike Mularkey — HC at Buffalo Bills (2004-05), Jacksonville Jaguars (2011-12), Tennessee Titans (2015-17). Connection: worked under Mike Smith at Atlanta.
5. Todd Haley — HC at Kansas City Chiefs (2009-11). Connection: worked under Herm Edwards at Kansas City.

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If none found, say "None found." """
    ),
    (
        "34_gen3_gibbs_proteges",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Joe Gibbs worked under Lou Holtz at Arkansas (1978-79) as offensive coordinator. The following coaches all worked under Gibbs at Washington and later became head coaches. Now I need to know if THEIR assistants also became head coaches.

1. Joe Bugel — HC at Phoenix/Arizona Cardinals (1990-93), Oakland Raiders (1997). Bugel was Gibbs's offensive line coach.
2. Bill Callahan — HC at Oakland Raiders (2002-03), Nebraska (2004-07). Callahan worked in the Gibbs coaching tree.
3. Gregg Williams — HC at Buffalo Bills (2001-03); interim roles at New Orleans Saints and Cleveland Browns. Williams was Gibbs's defensive coordinator.
4. Richie Petitbon — HC at Washington Redskins (1993, 1 season). Petitbon was Gibbs's defensive coordinator.
5. Al Saunders — Please confirm if and when Saunders was a head coach (he was a long-time OC/WR coach). Connection: worked under Gibbs at Washington.

For each confirmed HC, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If never a head coach (for Saunders — clarify), note that. If no proteges became HCs, say "None found." """
    ),
    (
        "35_gen3_nfl_small",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following coaches (Generation 3, shorter or interim HC tenures), identify any assistants who later became head coaches. Also clarify their HC records where noted.

1. Mike Nolan — HC at San Francisco 49ers (2005-08). Connection: worked under Lovie Smith's defensive staff.
2. David Culley — HC at Houston Texans (2021, 1 season). Connection: worked under John Harbaugh at Baltimore as assistant HC/WR coach.
3. Matt Canada — Confirm if he had any HC role (listed as interim at Maryland, 2015). Connection: worked under Dave Doeren at NC State.
4. Jim Leonhard — HC at Wisconsin (interim, 2022). Connection: worked under Paul Chryst at Wisconsin.
5. Harlon Barnett — HC at Michigan State (interim, 2023). Connection: worked under Mark Dantonio at Michigan State.
6. Mike Tressel — Confirm HC roles (listed as having interim stops). Connection: worked under Mark Dantonio at Michigan State.

For each confirmed HC, provide:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If no assistants became HCs (likely for most of these given brief tenures), say "None found." """
    ),

    # === PHASE 7: Gen 3 College Batches ===
    (
        "36_gen3_active_college_a",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following active college head coaches (Generation 3), identify any assistants who worked under them and later became head coaches (any level).

1. Mario Cristobal — HC at FIU (2013-15), Oregon (2017-21), Miami FL (2022-present). Connection: worked under Greg Schiano at Rutgers.
2. Sam Pittman — HC at Arkansas (2020-present). Connection: worked under Bret Bielema at Arkansas as offensive line coach.
3. Eliah Drinkwitz — HC at Appalachian State (2019), Missouri (2020-present). Connection: worked under Dave Doeren at NC State as offensive coordinator.

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

These are newer HC tenures; it's possible few proteges have moved to HC roles yet. If none found, say "None found." """
    ),
    (
        "37_gen3_active_college_b",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following active college head coaches (Generation 3), identify any assistants who worked under them and later became head coaches (any level).

1. P.J. Fleck — HC at Western Michigan (2013-16), Minnesota (2017-present). Connection: worked under Greg Schiano at Rutgers.
2. Matt Campbell — HC at Toledo (2015), Iowa State (2016-present). Connection: worked under Tim Beckman at Illinois as offensive coordinator.
3. Dave Aranda — HC at Baylor (2020-present). Connection: worked under Ed Orgeron at LSU as defensive coordinator.

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),
    (
        "38_gen3_college_histories",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following college head coaches (Generation 3, longer careers), identify assistants who worked under them and later became head coaches (any level).

1. Hugh Freeze — HC at Arkansas State (2011), Ole Miss (2012-17), Liberty (2019-21), Auburn (2023-present). Connection: worked under Ed Orgeron at Ole Miss.
2. Houston Nutt — HC at Boise State (1997), Arkansas (1998-2007), Ole Miss (2008-11). Connection: worked under Ken Hatfield at Arkansas.
3. Bo Pelini — HC at Nebraska (2008-14), Youngstown State (2015-17, 2019-22). Connection: worked under Ed Orgeron at LSU as defensive coordinator.

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

Houston Nutt had 14 seasons as HC and is the most likely to have produced head coaches. Include any levels."""
    ),
    (
        "39_gen3_college_batch_a",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following college head coaches (Generation 3), identify assistants who worked under them and later became head coaches (any level). If none found, say "None found."

1. Mike Locksley — HC at New Mexico (2009-11), Maryland (2019-present). Connection: worked under Ralph Friedgen at Maryland.
2. Marcus Freeman — HC at Notre Dame (2022-present). Connection: worked under Luke Fickell at Cincinnati as defensive coordinator.
3. Mike Elko — HC at Duke (2022), Texas A&M (2023-present). Connection: worked under Brian Kelly at Notre Dame as defensive coordinator.
4. Butch Jones — HC at Central Michigan (2009-11), Cincinnati (2012), Tennessee (2013-17), Arkansas State (2021). Connection: worked under Brian Kelly at Grand Valley State and Central Michigan.

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),
    (
        "40_gen3_college_batch_b",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following college/pro head coaches (Generation 3), identify assistants who worked under them and later became head coaches (any level). If none found, say "None found."

1. Clay Helton — HC at USC (2015-21). Connection: worked under Lane Kiffin at USC.
2. Dirk Koetter — HC at Arizona State (2007-11), Tampa Bay Buccaneers (2016-18). Connection: worked under Mike Smith at Atlanta.
3. Doug Marrone — HC at Syracuse (2009-12), Jacksonville Jaguars (2017-20). Connection: worked under Gus Bradley.
4. Kevin Wilson — HC at Indiana (2011-16), Tulsa (2024-present). Connection: worked under Ryan Day at Ohio State.
5. Matt Wells — HC at Utah State (2016-18), Texas Tech (2019-21). Connection: worked under Gary Andersen at Utah State.

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),
    (
        "41_gen3_college_medium",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following college head coaches (Generation 3), identify assistants who worked under them and later became head coaches (any level). If none found, say "None found."

1. Geoff Collins — HC at Temple (2018), Georgia Tech (2019-22). Connection: worked under Dan Mullen at Mississippi State.
2. Jeff Hafley — HC at Boston College (2020-22). Connection: worked under Ryan Day at Ohio State as co-defensive coordinator.
3. Jeff Quinn — HC at Buffalo (2010-12). Connection: worked under Brian Kelly at Cincinnati.
4. Chuck Martin — HC at Grand Valley State (D2, interim then HC), Miami (OH) (2013-present). Connection: worked under Brian Kelly at Grand Valley State and Notre Dame.
5. David Bailiff — HC at Texas State (2007-08), Rice (2007-17). Connection: worked under Ken Hatfield at Rice.
6. Tommy West — HC at Memphis (2001-07), Chattanooga (2009-15). Connection: worked under Ken Hatfield at Clemson and Rice.

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|"""
    ),
    (
        "42_gen3_small_misc",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following coaches (Generation 3, shorter or smaller-program tenures), identify any assistants who became head coaches. Most will likely be "None found" given brief tenures, but please check all levels including FCS and D2.

1. Bob Diaco — HC at UConn (2015-17). Connection: worked under Brian Kelly at Notre Dame as defensive coordinator.
2. Charlie Partridge — HC at Florida Atlantic (2014-15). Connection: worked under Bret Bielema at Wisconsin as defensive line coach.
3. Clark Lea — HC at Vanderbilt (2021-present). Connection: worked under Brian Kelly at Notre Dame as linebackers coach/DC.
4. Barry Lunney Jr. — HC at Arkansas (interim, 2019), UTSA (2022-present). Connection: worked under Bret Bielema at Arkansas.
5. Kyle Flood — HC at Rutgers (2012-15). Connection: worked under Greg Schiano at Rutgers.
6. Major Applewhite — HC at Houston (2017-18). Connection: worked under Tom Herman at Houston and Texas.
7. Brian Hartline — HC at South Florida (2024-present). Connection: worked under Ryan Day at Ohio State as wide receivers coach.
8. Brian Polian — HC at Nevada (2013-15). Connection: worked under Brian Kelly at Notre Dame as special teams coordinator.
9. Joe Susan — HC at Colgate (2013-17). Connection: worked under Greg Schiano at Rutgers as defensive coordinator.
10. Matt Canada — HC at Maryland (interim, 2015). Connection: worked under Dave Doeren at NC State.
11. Tony Petersen — HC at East Carolina (interim, 2019). Connection: worked under Doc Holliday at Marshall as offensive coordinator.
12. Tony Hughes — HC at Jackson State (2015-17), Mississippi Valley State (2018-present). Connection: worked under Dan Mullen at Mississippi State.

For each coach, provide a section:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If no assistants became HCs, say "None found." """
    ),

    # === PHASE 5: Uncovered Dead-End Gen 2 Coaches ===
    (
        "43_norv_turner",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Norv Turner was an offensive coordinator under several coaches in the Holtz tree before a long NFL head coaching career.

I need to identify all assistant coaches who worked under Norv Turner during his head coaching career and later became head coaches themselves (NFL, FBS, FCS, D2, or lower).

Norv Turner was head coach at:
- Washington Redskins (1994-2000)
- Oakland Raiders (2004-05)
- San Diego Chargers (2007-12)

His Washington and San Diego tenures were long enough to produce significant coaching branches. For each assistant who later became a head coach, provide a markdown table organized by team:

### [Team Name]

| Name | Role Under Turner | Years | Later HC Stops | Confidence |
|------|------------------|-------|----------------|------------|

Focus on verifiable connections. Include low-confidence entries rather than omitting them."""
    ),
    (
        "44_houston_nutt",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Houston Nutt was a protege of Ken Hatfield (who was a Holtz assistant at Arkansas). Nutt had a long college head coaching career.

I need to identify all assistant coaches who worked under Houston Nutt during his head coaching career and later became head coaches themselves (NFL, FBS, FCS, D2, or lower).

Houston Nutt was head coach at:
- Boise State (1997)
- Arkansas (1998-2007)
- Ole Miss (2008-11)

His decade at Arkansas is the primary focus — those staffs likely produced multiple future head coaches. For each assistant who later became a head coach, provide a markdown table organized by school:

### [School Name]

| Name | Role Under Nutt | Years | Later HC Stops | Confidence |
|------|----------------|-------|----------------|------------|

Focus on verifiable connections. Include low-confidence entries rather than omitting them."""
    ),
    (
        "45_batch_nfl_uncovered",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following NFL head coaches (all Generation 2 in the Holtz tree), list any assistant coaches who worked under them and later became head coaches themselves (NFL or college, any level). I only need their direct-report assistants who became HCs.

1. Bill Callahan — HC at Oakland Raiders (2002-03), Nebraska (2004-07). Also longtime NFL offensive line coach/coordinator. Focus on his HC tenures.
2. Ray Rhodes — HC at Philadelphia Eagles (1995-98), Green Bay Packers (1999). Long NFL defensive coaching career but focus on HC tenures.
3. Joe Bugel — HC at Phoenix Cardinals (1990-93), Oakland Raiders (1997). Legendary offensive line coach but focus on HC tenures.
4. Gregg Williams — HC at Buffalo Bills (2001-03), New Orleans Saints (interim, 2012). Long defensive coordinator career.
5. Al Saunders — HC at San Diego Chargers (1986-88). Later a prominent offensive coordinator in NFL.

For each, format as:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If none found for a coach, say "None found." """
    ),
    (
        "46_batch_college_uncovered",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following college/interim head coaches (all Generation 2 in the Holtz tree), list any assistant coaches who worked under them and later became head coaches (any level: NFL, FBS, FCS, D2, NAIA). If none found, say "None found."

1. Tommy West — HC at Clemson (1993-98, initially as interim), Memphis (2001-09), Chattanooga (2010-12). His long Memphis tenure (9 seasons) is the most likely to have produced branches.
2. Jim Colletto — HC at Cal State Fullerton (1984-86), Purdue (1991-96). Six seasons at Purdue is enough to produce coaching branches.
3. David Bailiff — HC at Texas State (2004-06), Rice (2007-17). Eleven seasons at Rice — check for assistants who became HCs.
4. Darrell Bevell — HC at Detroit Lions (interim, 2020), Jacksonville Jaguars (interim, 2021). Brief interim stints — probably no branches but check.
5. Jerry Rosburg — HC at Denver Broncos (interim, 2023). Single-game interim, unlikely branches.
6. Richie Petitbon — HC at Washington Redskins (1993, interim for 1 season after Gibbs retired). Brief tenure but check.

For each, format as:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If none found, say "None found." """
    ),

    # === PHASE 6: Gap Analysis & Completeness Audit ===
    (
        "47_nfl_uncovered_b",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following NFL head coaches (all Generation 2 in the Holtz tree), list ALL assistant coaches who served on their staffs during their HC tenures and later became head coaches (NFL or college, ANY level including interim). Be thorough — check OC, DC, position coaches, quality control assistants, and special teams coordinators.

IMPORTANT: A previous query returned "None found" for several NFL coaches with multi-year tenures, which seems unlikely. Please be extra thorough and check each coach's full staff rosters season by season.

1. Tom Cable — HC at Oakland Raiders (2008-2010). I believe Hue Jackson was on his staff as offensive coordinator — please verify and check for others.
2. Raheem Morris — HC at Tampa Bay Buccaneers (2009-2011). Three full seasons with a complete NFL staff. Check all coordinators and position coaches.
3. Rod Marinelli — HC at Detroit Lions (2006-2008). Three seasons including the 0-16 year. Check DC, OC, and all position coaches.
4. Scott Linehan — HC at St. Louis Rams (2006-2008). Check all coordinators and position coaches.
5. Gunther Cunningham — HC at Kansas City Chiefs (1999-2000). Short tenure but check all staff.

For each, format as:

## [Coach Name]

| Assistant Name | Role | Years Under HC | Later HC Stops | Confidence |
|---------------|------|----------------|----------------|------------|

If truly none found after thorough search, say "None found — verified." """
    ),
    (
        "48_nfl_recheck",
        """I'm building a coaching tree database tracing Lou Holtz's coaching lineage. A previous research pass returned "None found" for the following NFL head coaches, but I want to double-check with a more thorough search. For each, please check ALL coaching staff members during their HC tenures who later became head coaches at ANY level (NFL, college, any division, including interim).

Check coordinators (OC, DC, ST), position coaches, quality control coaches, and any assistant who later got a head coaching job.

1. Bill Callahan — HC at Oakland Raiders (2002-03), also HC at Nebraska (2004-07). Check BOTH tenures. I know Bo Pelini was his DC at Nebraska — who else from either staff became a HC?
2. Ray Rhodes — HC at Philadelphia Eagles (1995-98), Green Bay Packers (1999). Four seasons at Philadelphia is significant. Who were his coordinators? Did any become HCs?
3. Joe Bugel — HC at Phoenix/Arizona Cardinals (1990-93), Oakland Raiders (1997). Four seasons at Phoenix. Check all staff.
4. Gregg Williams — HC at Buffalo Bills (2001-03). Three seasons. Check all coordinators and position coaches.
5. Al Saunders — HC at San Diego Chargers (1986-88). Three seasons. Check all staff.

For each, format as:

## [Coach Name]

| Assistant Name | Role | Years Under HC | Later HC Stops | Confidence |
|---------------|------|----------------|----------------|------------|

If truly none found, say "None found — verified." """
    ),
    (
        "49_gen2_completeness_big",
        """I'm auditing our coaching tree database for completeness. For each of the following Generation 2 coaches, we already have SOME of their proteges listed. I need you to identify ANY ADDITIONAL assistants who worked under them during their head coaching tenures and later became head coaches (NFL or college, any level, including interim). Do NOT repeat the proteges I already have — only list ones that are MISSING.

1. Dan Quinn — HC at Atlanta Falcons (2015-2020), Dallas Cowboys (2025-).
   Already have: Dan Campbell (Lions HC). MISSING? What about Kyle Shanahan (was he OC at Atlanta under Quinn?), Marquand Manuel, Raheem Morris (was he on Quinn's staff?), others?

2. Jim Mora Jr. — HC at Atlanta Falcons (2004-06), Seattle Seahawks (2009), UCLA (2012-17), UConn (2022-23).
   Already have: Steve Sarkisian (via UCLA). MISSING? Jedd Fisch (now Washington HC — was he at UCLA under Mora?), Adrian Klemm, others?

3. Lovie Smith — HC at Chicago Bears (2004-2012), Tampa Bay Buccaneers (2014-15), Houston Texans (2022).
   Already have: Ron Rivera. MISSING? Rod Marinelli was he on Lovie's Chicago staff? Bob Babich? Any others from a 9-year tenure at Chicago?

4. Ed Orgeron — HC at Ole Miss (2005-07), USC (interim 2013), LSU (2016-2021).
   Already have: Hugh Freeze, Dave Aranda, Bo Pelini, Mickey Joseph, Zach Arnett. MISSING? Any others from LSU's national championship staff (2019)?

5. Greg Schiano — HC at Rutgers (2001-11), Tampa Bay Buccaneers (2012-13), Rutgers (2020-24).
   Already have: Kyle Flood, P.J. Fleck, Joe Susan, Norries Wilson. MISSING? Any from 11 years at Rutgers or 2 years at Tampa Bay?

For each coach, provide ONLY the missing proteges:

## [Coach Name]

**Already tracked:** [list I gave]
**Additional proteges found:**

| Name | Role | Years | Later HC Stops | Confidence |
|------|------|-------|----------------|------------|"""
    ),
    (
        "50_gen2_completeness_mid",
        """I'm auditing our coaching tree database for completeness. For each of the following Generation 2 coaches, we have a small number of proteges. I need to identify ANY ADDITIONAL assistants who became head coaches that we might be missing.

1. Tony Dungy — HC at Tampa Bay Buccaneers (1996-2001), Indianapolis Colts (2002-08).
   Already have: Jim Caldwell, Leslie Frazier. MISSING? Dungy had a famous coaching tree. What about Mike Tomlin (was he under Dungy?), Herm Edwards, Rod Marinelli, Lovie Smith — were any of these on Dungy's staff? Who else from 13 years as NFL HC?

2. John Harbaugh — HC at Baltimore Ravens (2008-present), recently named NY Giants HC.
   Already have: Gary Kubiak, David Culley, Wink Martindale. MISSING? 16+ years as HC. Rex Ryan? Chuck Pagano (was he DC at Baltimore before Colts)? Dean Pees? Others?

3. Herm Edwards — HC at New York Jets (2001-05), Kansas City Chiefs (2006-08), Arizona State (2018-22).
   Already have: Todd Haley, Mike Nolan. MISSING? From 5 years at Jets and 3 years at Chiefs, are there more? Eric Mangini was on his Jets staff?

4. Rex Ryan — HC at New York Jets (2009-14), Buffalo Bills (2015-16).
   Already have: Dennis Thurman (as protege at Buffalo). MISSING? From 6 years at the Jets, any assistants who became HCs? Mike Pettine (DC at Jets, later HC at Cleveland)?

5. Brad Childress — HC at Minnesota Vikings (2006-2010).
   Already have: 2 proteges. MISSING? From 5 years at Minnesota, any additional assistants who became HCs?

6. Lane Kiffin — HC at Oakland Raiders (2007-08), Tennessee (2009-10), USC (2010-13), FAU (2017-19), Ole Miss (2020-).
   Already have: Clay Helton, Jeff Scott. MISSING? From multiple stops, any others? Charlie Weis Jr.? Any coordinators?

For each, provide ONLY the missing proteges:

## [Coach Name]

**Already tracked:** [list I gave]
**Additional proteges found:**

| Name | Role | Years | Later HC Stops | Confidence |
|------|------|-------|----------------|------------|"""
    ),
    (
        "51_gen2_completeness_college",
        """I'm auditing our coaching tree database for completeness. For each of the following college head coaches with multi-year tenures, I have very few or zero Gen 3 proteges. Please check thoroughly for assistants who became head coaches at ANY level.

1. Dan McCarney — HC at Iowa State (1995-2006), North Texas (2011-13). TWELVE seasons at Iowa State. Who from his staff became HCs? Currently have 1 protege only.

2. Steve Addazio — HC at Temple (2011-12), Boston College (2013-2019), Colorado State (2020). Seven seasons at BC. Currently have only Ryan Day (cross-ref). Any others?

3. Steve Sarkisian — HC at Washington (2009-2013), USC (2014-15), Texas (2021-present). Five years at Washington. Currently have 1 protege. Marques Tuiasosopo? Chris Petersen was NOT on his staff. Who else?

4. Paul Chryst — HC at Pittsburgh (2012-14), Wisconsin (2015-2022). Ten years total. Currently have only Jim Leonhard. Any other assistants from Wisconsin or Pitt who became HCs?

5. Bill Cubit — HC at Western Michigan (2005-2012). Eight seasons. Any assistants who became HCs at any level?

6. Gregg Brandon — HC at Bowling Green (2003-2008). Six seasons. Any assistants who became HCs at any level?

7. Ted Roof — HC at Duke (2003-2007). Five seasons. Any assistants who became HCs?

8. Dan Enos — HC at Central Michigan (2010-2014). Five seasons at a MAC school. Any assistants who became HCs?

For each, format as:

## [Coach Name]

| Assistant Name | Role | Years | Later HC Stops | Confidence |
|---------------|------|-------|----------------|------------|

If none found, say "None found — verified." """
    ),
    (
        "52_cross_verification",
        """I'm building a comprehensive coaching tree database centered on Lou Holtz. I need you to help me verify completeness by approaching this from the OTHER direction: instead of looking at mentors and finding proteges, I'm going to list current and recent head coaches and ask you to trace them back to the Holtz tree.

For each of the following current/recent prominent head coaches, tell me:
1. Were they EVER an assistant under any coach in the Lou Holtz tree?
2. If yes, who was the mentor and what was the role/years?

Lou Holtz's tree includes (among others): Pete Carroll, Jimmy Johnson, Joe Gibbs, Barry Alvarez, Urban Meyer, Bob Davie, Brian Kelly, Mark Dantonio, Bret Bielema, Greg Schiano, Dan Quinn, Jim Mora Jr., Lovie Smith, Tony Dungy, John Harbaugh, Herm Edwards, Rex Ryan, Ed Orgeron, Lane Kiffin, Tom Herman, Ryan Day, Luke Fickell, Raheem Morris, Tom Cable, Rod Marinelli, Norv Turner, Houston Nutt, and their proteges.

Check these coaches:
1. Kyle Shanahan (HC San Francisco 49ers)
2. Jedd Fisch (HC Washington Huskies)
3. Hue Jackson (former HC Cleveland Browns, Oakland Raiders)
4. Mike Pettine (former HC Cleveland Browns)
5. Eric Mangini (former HC Cleveland Browns, New York Jets)
6. Todd Bowles (HC Tampa Bay Buccaneers)
7. Kliff Kingsbury (former HC Arizona Cardinals)
8. Sean McDermott (HC Buffalo Bills)
9. Kevin Stefanski (HC Cleveland Browns)
10. Matt LaFleur (HC Green Bay Packers)
11. Sean McVay (HC Los Angeles Rams)
12. Robert Saleh (former HC New York Jets)
13. Dennis Allen (former HC New Orleans Saints, Oakland Raiders)
14. Nathaniel Hackett (former HC Denver Broncos)
15. Frank Reich (former HC Indianapolis Colts, Carolina Panthers)

For each, provide:

| Coach | Connection to Holtz Tree? | Mentor | Role/Years | Confidence |
|-------|--------------------------|--------|------------|------------|

If NO connection found, say "No connection found." """
    ),

    # === PHASE 5: Gen 2 Tree Expansion — Thin Branches ===
    (
        "53_lane_kiffin_deep",
        """I'm building a coaching tree database for college football. Lane Kiffin has been a head coach at five stops:

1. Oakland Raiders (2007-08)
2. Tennessee (2009-10)
3. USC (2010-13, fired mid-season)
4. Florida Atlantic (2017-19)
5. Ole Miss (2020-present)

The previous query only found Clay Helton and Ed Orgeron from his USC staff. I need a MORE THOROUGH search across ALL of his stops.

For each stop, list EVERY assistant who later became a head coach at ANY level (NFL, FBS, FCS, D2, D3, NAIA, high school head coach does NOT count). Also include assistants who became interim head coaches.

Pay special attention to:
- Ole Miss (2020-present): His longest current tenure. Has anyone left to become a HC? Charlie Weis Jr., Chris Partridge, etc.?
- FAU (2017-19): Did any assistants move up?
- Tennessee (2009-10): Short stint but who was on staff? Ed Orgeron was there briefly.

For each assistant who later became a head coach, provide:

| Name | Role Under Kiffin | Years Under Kiffin | School/Team | Later HC Stops | Confidence |
|------|------------------|-------------------|-------------|----------------|------------|

After the tables, list any notable coordinators under Kiffin who are considered "HC candidates" but haven't landed a job yet."""
    ),
    (
        "54_sarkisian_deep",
        """I'm building a coaching tree database for college football. Steve Sarkisian has been a head coach at three stops:

1. Washington (2009-2013)
2. USC (2014-2015, fired mid-season)
3. Texas (2021-present)

The previous query only found Justin Wilcox (Cal HC) from Washington. I need a MUCH more thorough search.

For each stop, list EVERY assistant who later became a head coach at ANY level (NFL, FBS, FCS, D2, D3, NAIA).

Key names to investigate from his staffs:
- Washington: Tosh Lupoi, Nick Holt, Brent Pease, Keith Bhonapha, Eric Schmidt, Peter Sirmon, Johnny Nansen
- USC: Clancy Pendergast, Tyson Helton (later Western Kentucky HC?), Keith Heyward, Tommie Robinson
- Texas: Pete Kwiatkowski, Kyle Flood, Jeff Choate, Jeff Banks, Tashard Choice, Bo Davis, AJ Milwee

For each assistant who later became a head coach, provide:

| Name | Role Under Sarkisian | Years Under Sark | School/Team | Later HC Stops | Confidence |
|------|---------------------|-----------------|-------------|----------------|------------|

Also note any who became NFL position coaches or coordinators but not yet HCs."""
    ),
    (
        "55_lovie_smith_deep",
        """I'm building a coaching tree database for college football/NFL. Lovie Smith has been a head coach at three stops:

1. Chicago Bears (2004-2012)
2. Tampa Bay Buccaneers (2014-2015)
3. Houston Texans (2022)
4. Also: Illinois head coach (2016-2020)

We already have Ron Rivera and Rod Marinelli. I need ALL assistants who later became head coaches.

Key names to investigate:
- Bears: Bob Babich, Greg Blache, Mike Tice, Pep Hamilton, Jeremy Bates, Mike Martz (was he OC under Lovie?), Tim Hightower
- Bears defensive staff produced many NFL coaches
- Buccaneers: Marcus Arroyo, Mike Bajakian, Leslie Frazier (was he under Lovie?)
- Illinois: any assistants who became HCs?

For each, provide:

| Name | Role Under Lovie | Years | Team/School | Later HC Stops | Confidence |
|------|-----------------|-------|-------------|----------------|------------|"""
    ),
    (
        "56_tom_herman_deep",
        """I'm building a coaching tree database for college football. Tom Herman has been a head coach at two stops:

1. Houston (2015-2016)
2. Texas (2017-2020)
3. Also: Florida Atlantic (2023-present)

We only have Major Applewhite (Houston HC). I need ALL assistants across all stops who later became head coaches.

Key names to investigate:
- Houston: Todd Orlando, Kendal Briles, Major Applewhite, Mark D'Onofrio, Jason Washington
- Texas: Todd Orlando, Tim Beck, Derek Warehime, Herb Hand, Craig Naivar, Oscar Giles, Stan Drayton (became Toledo HC?), Corby Meekins, Jeff Banks
- FAU: current staff

Stan Drayton is especially important — he was RB coach under Herman at Texas, then became Toledo HC.

For each, provide:

| Name | Role Under Herman | Years | School/Team | Later HC Stops | Confidence |
|------|------------------|-------|-------------|----------------|------------|"""
    ),
    (
        "57_jim_mora_jr_deep",
        """I'm building a coaching tree database for college football/NFL. Jim Mora Jr. has been a head coach at:

1. Atlanta Falcons (2004-2006)
2. Seattle Seahawks (2009, interim for last game)
3. UCLA (2012-2017)
4. UConn (2022-present)

We only have Jedd Fisch (Arizona/Washington HC). I need ALL assistants who became HCs.

Key names to investigate:
- Falcons: Many NFL assistants — who on his staff became HCs?
- UCLA: Adrian Klemm, Demetrice Martin, Nate Woody, Jeff Ulbrich, Jason Kaufusi, Kennedy Polamalu (interim HC anywhere?)
- UConn: any departures to HC jobs?

For each, provide:

| Name | Role Under Mora | Years | Team/School | Later HC Stops | Confidence |
|------|----------------|-------|-------------|----------------|------------|"""
    ),
    (
        "58_kyle_whittingham_deep",
        """I'm building a coaching tree database for college football. Kyle Whittingham has been head coach at:

1. Utah (2005-2024) — one of the longest tenures in college football
2. Michigan (2025-present)

With nearly 20 years at Utah, he surely produced multiple head coaches from his staff. I need ALL assistants who later became head coaches at ANY level.

Key names to investigate from his Utah staffs over the years:
- Morgan Scalley, Jay Hill (Weber State HC?), Kalani Sitake (BYU HC?), Andy Ludwig, Gary Andersen (Utah State/Wisconsin HC — was he under Whittingham?), Dennis Erickson, Brian Johnson, Aaron Roderick, Sharrieff Shah, Freddie Whittingham

Kalani Sitake (BYU) and Jay Hill (Weber State) are both very likely from his tree.

For each, provide:

| Name | Role Under Whittingham | Years at Utah | Later HC Stops | Confidence |
|------|----------------------|--------------|----------------|------------|"""
    ),
    (
        "59_norv_turner_deep",
        """I'm building a coaching tree database for NFL/college football. Norv Turner has been a head coach at:

1. Washington Redskins (1994-2000)
2. Oakland Raiders (2004)
3. San Diego Chargers (2007-2012)

We have Mike Nolan and Ron Rivera. Need ALL assistants who became HCs.

Key names from his staffs:
- Redskins: Many coaches came through this staff in the late 90s
- Chargers: Rob Ryan, John Pagano, Frank Reich (was he on Chargers staff?), Ken Whisenhunt, Clarence Shelmon
- Any OCs or DCs under Turner who got HC jobs?

For each, provide:

| Name | Role Under Turner | Years | Team | Later HC Stops | Confidence |
|------|------------------|-------|------|----------------|------------|"""
    ),
    (
        "60_paul_chryst_deep",
        """I'm building a coaching tree database for college football. Paul Chryst has been head coach at:

1. Pittsburgh (2012-2014)
2. Wisconsin (2015-2022)

We only have Jim Leonhard (interim at Wisconsin). Need ALL assistants who became HCs.

Key names to investigate:
- Wisconsin: Joe Rudolph, Bob Bostad, Chris Haering, Mickey Turner, Jim Leonhard, Bobby April, Joe Lorig, Matt Canada (was OC before leaving — became Maryland interim HC)
- Pittsburgh: Dave Borbely, Tom Bradley

Matt Canada is key — he was briefly OC at Pitt under Chryst before going to NC State, LSU, Maryland (interim HC), then Steelers OC.

For each, provide:

| Name | Role Under Chryst | Years | School | Later HC Stops | Confidence |
|------|------------------|-------|--------|----------------|------------|"""
    ),
    (
        "61_rex_ryan_deep",
        """I'm building a coaching tree database for NFL. Rex Ryan has been a head coach at:

1. New York Jets (2009-2014)
2. Buffalo Bills (2015-2016)

We have Anthony Lynn (Chargers HC) and Mike Pettine (Browns HC). Need ALL assistants who became HCs.

Key names to investigate:
- Jets: Mike Pettine (DC), Tony Sparano (OL/OC), Brian Schottenheimer (OC), Dennis Thurman, Jeff Weeks, Ben Kotwica, Karl Dunbar
- Bills: Anthony Lynn (interim HC/then Chargers HC), Rob Ryan (DC, twin brother), Greg Roman, Thurman
- Did Brian Schottenheimer ever become HC?

For each, provide:

| Name | Role Under Rex Ryan | Years | Team | Later HC Stops | Confidence |
|------|-------------------|-------|------|----------------|------------|"""
    ),
    (
        "62_houston_nutt_deep",
        """I'm building a coaching tree database for college football. Houston Nutt has been head coach at:

1. Murray State (1993-1996)
2. Boise State (1997)
3. Arkansas (1998-2007)
4. Ole Miss (2008-2011)

I need ALL assistants who later became head coaches at any level.

Key names to investigate:
- Arkansas: Gus Malzahn (was he ever on Nutt's staff?), Bobby Allen, Danny Ford, Mike Markuson, Mike Anderson, Reggie Herring, Louis Campbell
- Ole Miss: Tyrone Nix, Dave Bentley, Werner Roberts
- Murray State / Boise State: any early staff who moved up?

For each, provide:

| Name | Role Under Nutt | Years | School | Later HC Stops | Confidence |
|------|----------------|-------|--------|----------------|------------|"""
    ),
    (
        "63_dan_quinn_deep",
        """I'm building a coaching tree database for NFL. Dan Quinn has been a head coach at:

1. Atlanta Falcons (2015-2020)
2. Washington Commanders (2024-present)

We have Kyle Shanahan (OC, later 49ers HC) and Raheem Morris (later Falcons HC). Need ALL assistants who became HCs.

Key names:
- Falcons: Kyle Shanahan (OC 2015-16), Matt LaFleur (QB coach 2015-16, later Packers HC?), Steve Sarkisian (OC 2017-18), Marquand Manuel, Rahim Morris, Mike McDaniel (was he on this staff?)
- Commanders: current staff — anyone leave for HC?

Matt LaFleur is especially important — he was QB coach under Quinn in 2015-16 before becoming Packers HC. Mike McDaniel (Dolphins HC) may have passed through.

For each, provide:

| Name | Role Under Quinn | Years | Team | Later HC Stops | Confidence |
|------|-----------------|-------|------|----------------|------------|"""
    ),
    (
        "64_gary_andersen_dave_doeren",
        """I'm building a coaching tree database for college football. I need to flesh out two Gen 2 coaches' trees:

## Gary Andersen
Head coach at:
- Utah State (2009-2012)
- Wisconsin (2013-2014)
- Oregon State (2015-2017)

## Dave Doeren
Head coach at:
- Northern Illinois (2011-2012)
- NC State (2013-present)

For each coach at each stop, list EVERY assistant who later became a head coach at any level.

Key names to check:
- Andersen at Utah State: Matt Wells (later Texas Tech HC?), Frank Maile, Todd Orlando
- Doeren at NC State: Dave Huxtable, Tony Gibson, Tim Beck (was he under Doeren before going to Ohio State?), Matt Canada (was OC at NC State under Doeren)

For each, provide:

| Name | Role | Years | School | Later HC Stops | Confidence |
|------|------|-------|--------|----------------|------------|"""
    ),
]


def load_progress():
    """Load progress tracker."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {}


def save_progress(progress):
    """Save progress tracker."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def run_query(client, model, query_num, filename, prompt):
    """Run a single query and save results."""
    output_path = OUTPUT_DIR / f"{filename}.md"

    print(f"\n{'='*60}")
    print(f"Query {query_num}/{len(QUERIES)}: {filename}")
    print(f"{'='*60}")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,  # Lower temperature for factual recall
            max_tokens=4096,
        )

        content = response.choices[0].message.content

        # Write response with metadata header
        with open(output_path, "w") as f:
            f.write(f"# Query {query_num}: {filename}\n\n")
            f.write(f"**Model:** {model}  \n")
            f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Tokens:** {response.usage.total_tokens} "
                    f"(prompt: {response.usage.prompt_tokens}, "
                    f"completion: {response.usage.completion_tokens})  \n\n")
            f.write("---\n\n")
            f.write(content)
            f.write("\n")

        print(f"  Saved to: {output_path}")
        print(f"  Tokens used: {response.usage.total_tokens}")
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run coaching tree research queries via OpenAI API")
    parser.add_argument("--query", type=int, help="Run a specific query number (1-indexed)")
    parser.add_argument("--from", dest="from_q", type=int, help="Start from this query number")
    parser.add_argument("--to", dest="to_q", type=int, help="End at this query number (inclusive)")
    parser.add_argument("--list", action="store_true", help="List all queries without running them")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model to use (default: gpt-4o)")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds to wait between queries (default: 2)")
    parser.add_argument("--skip-completed", action="store_true", default=True,
                        help="Skip queries that already have output files (default: true)")
    parser.add_argument("--force", action="store_true", help="Re-run even if output file exists")
    args = parser.parse_args()

    # List mode
    if args.list:
        print(f"\n{'#':>3}  {'Filename':<35}  {'Status'}")
        print(f"{'─'*3}  {'─'*35}  {'─'*10}")
        for i, (filename, _) in enumerate(QUERIES, 1):
            output_path = OUTPUT_DIR / f"{filename}.md"
            status = "DONE" if output_path.exists() else "TODO"
            print(f"{i:>3}  {filename:<35}  {status}")
        total = len(QUERIES)
        done = sum(1 for fn, _ in QUERIES if (OUTPUT_DIR / f"{fn}.md").exists())
        print(f"\n{done}/{total} complete")
        return

    # Validate API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Set it with: export OPENAI_API_KEY='sk-...'")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Determine which queries to run
    if args.query:
        indices = [args.query - 1]
    elif args.from_q or args.to_q:
        start = (args.from_q or 1) - 1
        end = args.to_q or len(QUERIES)
        indices = list(range(start, end))
    else:
        indices = list(range(len(QUERIES)))

    # Filter completed if not forcing
    if not args.force:
        filtered = []
        for i in indices:
            filename = QUERIES[i][0]
            output_path = OUTPUT_DIR / f"{filename}.md"
            if output_path.exists():
                print(f"Skipping query {i+1} ({filename}) — already complete. Use --force to re-run.")
            else:
                filtered.append(i)
        indices = filtered

    if not indices:
        print("\nNo queries to run. All selected queries are complete.")
        print("Use --force to re-run completed queries, or --list to see status.")
        return

    print(f"\nRunning {len(indices)} queries using model: {args.model}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Delay between queries: {args.delay}s")

    # Estimate cost
    est_cost = len(indices) * 0.08  # rough estimate for gpt-4o
    print(f"Estimated cost: ~${est_cost:.2f} (rough estimate)")

    # Confirm
    response = input(f"\nProceed with {len(indices)} queries? [y/N] ")
    if response.lower() != "y":
        print("Aborted.")
        return

    # Run queries
    progress = load_progress()
    successes = 0
    failures = 0

    for idx, i in enumerate(indices):
        filename, prompt = QUERIES[i]
        query_num = i + 1

        success = run_query(client, args.model, query_num, filename, prompt)

        if success:
            successes += 1
            progress[filename] = {
                "status": "complete",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "model": args.model,
            }
            save_progress(progress)
        else:
            failures += 1
            progress[filename] = {
                "status": "failed",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            save_progress(progress)

        # Delay between queries (but not after the last one)
        if idx < len(indices) - 1:
            print(f"  Waiting {args.delay}s before next query...")
            time.sleep(args.delay)

    print(f"\n{'='*60}")
    print(f"COMPLETE: {successes} succeeded, {failures} failed")
    print(f"Results saved to: {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
