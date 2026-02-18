# Coaching Tree Research — ChatGPT Prompt Playbook

## How to Use This Document

### Option A: Automated (Recommended)
Run `run_research.py` to execute all queries via the OpenAI API automatically:
```bash
pip install openai
export OPENAI_API_KEY="sk-your-key-here"
python "coaching tree/run_research.py"
```
Results are saved to `research/chatgpt/01_pete_carroll.md`, `02_jimmy_johnson.md`, etc.
See the script's `--help` for options (run specific queries, use different models, etc.)

### Option B: Manual Copy-Paste
1. Work through prompts in order (Phase 1 → 2 → 3 → 4)
2. Copy-paste each prompt into ChatGPT (regular mode, not deep research)
3. Save each response to `research/chatgpt/` using the filename shown for each query
4. Mark each prompt as DONE in the progress tracker at the bottom
5. Bring all results back to this project for JSON entry

**Scoping Rules:**
- Gen 1 (Holtz proteges): Find all assistants who became HCs → these become Gen 2
- Gen 2 (college coaches): Find their assistants who became HCs → these become Gen 3
- Gen 2 (NFL-only coaches): Find direct-report assistants who became HCs → STOP (no Gen 4)
- Pete Carroll, Jimmy Johnson, Joe Gibbs: Find their assistants who became HCs → STOP (don't recurse their sub-trees)
- Cap at Gen 3 maximum depth from Holtz

---

## Phase 1: Complete Gen 1 Gaps (6 queries)

### Query 1: Pete Carroll
```
I'm building a coaching tree database for college football, specifically tracing Lou Holtz's coaching lineage. Pete Carroll was a graduate assistant under Holtz at Arkansas in 1977 before going on to a legendary coaching career.

I need to identify all assistant coaches who worked under Pete Carroll during his head coaching career and later became head coaches themselves (at any level: NFL, FBS, FCS, D2, NAIA).

Pete Carroll was head coach at:
- New York Jets (1994, 1 season)
- New England Patriots (1997-99)
- USC (2001-09)
- Seattle Seahawks (2010-2023)
- Las Vegas Raiders (2025-)

For each assistant who later became a head coach, provide:
1. Full name
2. Which team they worked under Carroll at
3. Their role (position coach, coordinator, GA, etc.)
4. Approximate years they overlapped with Carroll
5. Where they later became head coach (all HC stops)
6. Confidence level (high/medium/low) — mark low if you're uncertain

Organize by the team where they served under Carroll. Format as a table:
Name | Team Under Carroll | Role | Years | Later HC Stops | Confidence

Focus on verifiable connections. Include low-confidence entries rather than omitting them.
```

### Query 2: Jimmy Johnson
```
I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Jimmy Johnson was Holtz's defensive coordinator at Arkansas (1977-78) before becoming one of the most successful coaches in football history.

I need to identify all assistant coaches who worked under Jimmy Johnson during his head coaching career and later became head coaches themselves (NFL, FBS, FCS, D2, or lower).

Jimmy Johnson was head coach at:
- Oklahoma State (1979-83)
- Miami, FL (1984-88)
- Dallas Cowboys (1989-93)
- Miami Dolphins (1996-99)

For each assistant who later became a head coach, provide:
1. Full name
2. Which team they worked under Johnson at
3. Their role (position coach, coordinator, GA, etc.)
4. Approximate years they overlapped with Johnson
5. Where they later became head coach (all HC stops)
6. Confidence level (high/medium/low)

Organize by the team where they served under Johnson. Format as a table:
Name | Team Under Johnson | Role | Years | Later HC Stops | Confidence

Focus on verifiable connections. The Miami (FL) and Dallas staffs are especially important — those programs produced many future head coaches.
```

### Query 3: Joe Gibbs
```
I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Joe Gibbs was Holtz's offensive coordinator at Arkansas (1978-79) before becoming a Pro Football Hall of Fame head coach.

I need to identify all assistant coaches who worked under Joe Gibbs during his head coaching career and later became head coaches themselves (NFL, FBS, FCS, or lower).

Joe Gibbs was head coach at:
- Washington Redskins (1981-92, first tenure)
- Washington Redskins (2004-07, second tenure)

For each assistant who later became a head coach, provide:
1. Full name
2. Their role under Gibbs
3. Approximate years they overlapped with Gibbs
4. Which tenure (1st or 2nd)
5. Where they later became head coach (all HC stops)
6. Confidence level (high/medium/low)

Format as a table:
Name | Role Under Gibbs | Years | Tenure | Later HC Stops | Confidence

The 1981-92 tenure is especially important as it was a dynasty period that likely produced many coaching branches.
```

### Query 4: Ken Hatfield
```
I'm building a coaching tree database tracing Lou Holtz's coaching lineage. Ken Hatfield was an assistant under Holtz at Arkansas (1977-83) before a long head coaching career.

I need to identify all assistant coaches who worked under Ken Hatfield during his head coaching career and later became head coaches themselves (NFL, FBS, FCS, D2, or lower).

Ken Hatfield was head coach at:
- Air Force (1979-83)
- Arkansas (1984-89)
- Clemson (1990-93)
- Rice (1994-2005)

For each assistant who later became a head coach, provide:
1. Full name
2. Which school they worked under Hatfield at
3. Their role
4. Approximate years they overlapped
5. Where they later became head coach (all HC stops)
6. Confidence level (high/medium/low)

Organize by school. Format as a table:
Name | School Under Hatfield | Role | Years | Later HC Stops | Confidence
```

### Query 5: Batch — Medium Gen 1 Coaches
```
I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following head coaches (all former Holtz assistants), I need to know which of THEIR assistants later became head coaches.

For each coach, list any assistants who later became head coaches at any level (NFL, FBS, FCS, D2, NAIA). If none found, say "None found."

1. Skip Holtz (Lou's son) — HC at:
   - Connecticut (1994-98)
   - East Carolina (2005-09)
   - South Florida (2010-12)
   - Louisiana Tech (2013-21)
   - Marshall (2023-present)

2. Dave Roberts — HC at:
   - Western Kentucky (year unknown)
   - Northeast Louisiana (year unknown)
   - Baylor (year unknown)

3. Joker Phillips — HC at:
   - Kentucky (2010-12)

4. Rick Stockstill — HC at:
   - Middle Tennessee (2006-23)

Format for each coach found:
Coach Name > Assistant Name | Role | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 6: Batch — Small Gen 1 Coaches
```
I'm building a coaching tree database tracing Lou Holtz's coaching lineage. For each of the following head coaches (all former Holtz assistants), I need to know which of THEIR assistants later became head coaches.

For each coach, list any assistants who later became head coaches at any level (NFL, FBS, FCS, D2, NAIA). If none found, say "None found." These are mostly small-program coaches so it's entirely possible some had no proteges who became HCs.

1. Buddy Pough — HC at South Carolina State (2002-23, HBCU/FCS)
2. John Palermo — HC at Austin Peay (FCS, approximate years late 1990s-2000s)
3. Peter Vaas — HC at Holy Cross (1994-98, FCS)
4. Bo Rein — HC at NC State (1976-79, died in plane crash Jan 1980)
5. Ron Cooper — HC at:
   - Eastern Michigan (1993-94)
   - Louisville (1995-97)
   - Alabama A&M
   - Florida International

Format for each:
Coach Name > Assistant Name | Role | Years | Later HC Stops | Confidence (high/med/low)
```

---

## Phase 2: Gen 2 → Gen 3 — College Big Trees (14 queries)

### Query 7: Brian Kelly
```
I'm building a coaching tree database. Brian Kelly has been a head coach at multiple schools. I need to identify all assistant coaches who worked under Kelly and later became head coaches themselves.

Brian Kelly was head coach at:
- Grand Valley State (1991-2003, D2)
- Central Michigan (2004-06)
- Cincinnati (2007-09)
- Notre Dame (2010-21)
- LSU (2022-present)

For each assistant who later became a head coach, provide:
Name | School Under Kelly | Role | Years | Later HC Stops | Confidence (high/med/low)

Organize by school. The Notre Dame and LSU staffs are best documented but don't neglect the earlier stops.
```

### Query 8: Mark Dantonio
```
I'm building a coaching tree database. Mark Dantonio had a long career as a head coach. I need to identify all assistant coaches who worked under him and later became head coaches.

Mark Dantonio was head coach at:
- Central Michigan (2004-06)
- Cincinnati (2004-06) [correction: he went from CMU to Cincinnati]
  - Actually: Cincinnati (2004-06)
- Michigan State (2007-19)

For each assistant who later became a head coach, provide:
Name | School Under Dantonio | Role | Years | Later HC Stops | Confidence (high/med/low)

The Michigan State tenure (13 seasons) is the primary focus as it likely produced the most coaching branches.
```

### Query 9: Bret Bielema
```
I'm building a coaching tree database. Bret Bielema was a head coach at multiple schools. I need to identify all assistant coaches who worked under him and later became head coaches.

Bret Bielema was head coach at:
- Wisconsin (2006-12)
- Arkansas (2013-17)
- Illinois (2021-24)

For each assistant who later became a head coach, provide:
Name | School Under Bielema | Role | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 10: Luke Fickell (expand)
```
I'm building a coaching tree database. I already have Marcus Freeman listed as a Luke Fickell protege (DC at Cincinnati, 2017-20 → Notre Dame HC). I need to identify any OTHER assistant coaches who worked under Fickell and later became head coaches.

Luke Fickell was head coach at:
- Ohio State (2011, interim)
- Cincinnati (2017-22)
- Wisconsin (2023-present)

For each assistant (BESIDES Marcus Freeman) who later became a head coach, provide:
Name | School Under Fickell | Role | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 11: Ryan Day (expand)
```
I'm building a coaching tree database. I already have Jeff Hafley (co-DC 2019 → Boston College HC) and Brian Hartline (WR coach → South Florida HC) listed as Ryan Day proteges. I need to identify any OTHER assistant coaches who worked under Day and later became head coaches.

Ryan Day has been head coach at:
- Ohio State (2019-present)

For each assistant (BESIDES Hafley and Hartline) who later became a head coach, provide:
Name | School Under Day | Role | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 12: Dan Mullen
```
I'm building a coaching tree database. I need to identify all assistant coaches who worked under Dan Mullen and later became head coaches.

Dan Mullen was head coach at:
- Mississippi State (2009-17)
- Florida (2018-21)
- UNLV (2024-present)

For each assistant who later became a head coach, provide:
Name | School Under Mullen | Role | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 13: Tom Herman
```
I'm building a coaching tree database. I need to identify all assistant coaches who worked under Tom Herman and later became head coaches.

Tom Herman was head coach at:
- Houston (2015-16)
- Texas (2017-20)

For each assistant who later became a head coach, provide:
Name | School Under Herman | Role | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 14: Greg Schiano
```
I'm building a coaching tree database. I need to identify all assistant coaches who worked under Greg Schiano and later became head coaches.

Greg Schiano was head coach at:
- Rutgers (2001-11, first tenure)
- Tampa Bay Buccaneers (2012-13)
- Rutgers (2020-present, second tenure)

For each assistant who later became a head coach, provide:
Name | Team/School Under Schiano | Role | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 15: Pat Narduzzi
```
I'm building a coaching tree database. I need to identify all assistant coaches who worked under Pat Narduzzi and later became head coaches.

Pat Narduzzi has been head coach at:
- Pittsburgh (2015-present)

For each assistant who later became a head coach, provide:
Name | Role Under Narduzzi | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 16: Lane Kiffin
```
I'm building a coaching tree database. I need to identify all assistant coaches who worked under Lane Kiffin and later became head coaches.

Lane Kiffin was head coach at:
- Oakland Raiders (2007-08)
- Tennessee (2009-09, 1 season)
- USC (2010-13, fired midseason)
- Florida Atlantic (2017-19)
- Ole Miss (2020-present)

For each assistant who later became a head coach, provide:
Name | Team/School Under Kiffin | Role | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 17: Ed Orgeron
```
I'm building a coaching tree database. I need to identify all assistant coaches who worked under Ed Orgeron and later became head coaches.

Ed Orgeron was head coach at:
- Ole Miss (2005-07)
- USC (2013, interim)
- LSU (2016-21, including 2019 national championship)

For each assistant who later became a head coach, provide:
Name | School Under Orgeron | Role | Years | Later HC Stops | Confidence (high/med/low)

The 2019 LSU championship staff is especially notable.
```

### Query 18: Jim Mora Jr.
```
I'm building a coaching tree database. I need to identify all assistant coaches who worked under Jim Mora Jr. and later became head coaches.

Jim Mora Jr. was head coach at:
- Atlanta Falcons (2004-06)
- Seattle Seahawks (2009, interim)
- UCLA (2012-17)
- UConn (2022-23)

For each assistant who later became a head coach, provide:
Name | Team/School Under Mora | Role | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 19: Ralph Friedgen
```
I'm building a coaching tree database. I need to identify all assistant coaches who worked under Ralph Friedgen and later became head coaches.

Ralph Friedgen was head coach at:
- Maryland (2001-10)

For each assistant who later became a head coach, provide:
Name | Role Under Friedgen | Years | Later HC Stops | Confidence (high/med/low)
```

### Query 20: Steve Addazio
```
I'm building a coaching tree database. I need to identify all assistant coaches who worked under Steve Addazio and later became head coaches.

Steve Addazio was head coach at:
- Temple (2011-12)
- Boston College (2013-19)
- Colorado State (2020-21)

For each assistant who later became a head coach, provide:
Name | School Under Addazio | Role | Years | Later HC Stops | Confidence (high/med/low)
```

---

## Phase 3: Gen 2 NFL + Small College Batches (6 queries)

### Query 21: Batch — NFL Big Names
```
I'm building a coaching tree database. For each of the following NFL head coaches, list any assistant coaches who worked under them and later became head coaches themselves (NFL or college, any level). I only need their direct-report assistants who became HCs — no need to trace further.

1. Tony Dungy — HC at Tampa Bay Buccaneers (1996-2001), Indianapolis Colts (2002-08)
2. Mike Tomlin — HC at Pittsburgh Steelers (2007-present)
3. John Harbaugh — HC at Baltimore Ravens (2008-2024), New York Giants (2025-present)
4. Lovie Smith — HC at Chicago Bears (2004-12), Tampa Bay Buccaneers (2014-15), Houston Texans (2022)
5. Rex Ryan — HC at New York Jets (2009-14), Buffalo Bills (2015-16)

For each, format as:
Coach Name > Assistant Name | Role | Years | Later HC Stops | Confidence (high/med/low)

If none found for a coach, say "None found."
```

### Query 22: Batch — NFL Smaller Names
```
I'm building a coaching tree database. For each of the following NFL head coaches, list any assistant coaches who worked under them and later became head coaches themselves. I only need direct-report assistants who became HCs.

1. Herm Edwards — HC at New York Jets (2001-05), Kansas City Chiefs (2006-08)
2. Raheem Morris — HC at Tampa Bay Buccaneers (2009-11), Atlanta Falcons (2024-present)
3. Gus Bradley — HC at Jacksonville Jaguars (2013-16)
4. Rod Marinelli — HC at Detroit Lions (2006-08)
5. Brad Childress — HC at Minnesota Vikings (2006-10)
6. Chuck Pagano — HC at Indianapolis Colts (2012-17)
7. Scott Linehan — HC at St. Louis Rams (2006-08)
8. Tom Cable — HC at Oakland Raiders (2008-10)
9. Gunther Cunningham — HC at Kansas City Chiefs (1999-2000)

For each, format as:
Coach Name > Assistant Name | Role | Years | Later HC Stops | Confidence (high/med/low)

If none found, say "None found."
```

### Query 23: Batch — College Small Trees A
```
I'm building a coaching tree database. For each of the following college head coaches, list any assistant coaches who worked under them and later became head coaches (any level). If none found, say "None found."

1. Dan McCarney — HC at Iowa State (1995-2006), North Texas (2011-15)
2. Paul Chryst — HC at Pittsburgh (2012-14), Wisconsin (2015-22)
3. Gary Andersen — HC at Utah State (2009-12), Wisconsin (2013-14), Oregon State (2015-17)
4. Dave Doeren — HC at Northern Illinois (2011-12), NC State (2013-present)
5. Don Treadwell — HC at Miami of Ohio (2011, 1 season)
6. Chris Ash — HC at Rutgers (2016-19)
7. Everett Withers — HC at James Madison (2014-15), Texas State (2016-18)

Format: Coach Name > Assistant Name | Role | Years | Later HC Stops | Confidence
```

### Query 24: Batch — College Small Trees B
```
I'm building a coaching tree database. For each of the following college head coaches, list any assistant coaches who worked under them and later became head coaches (any level). If none found, say "None found."

1. D.J. Durkin — HC at Maryland (2016-18)
2. Tim Beckman — HC at Toledo (2009-11), Illinois (2012-14)
3. Gregg Brandon — HC at Bowling Green (2003-08)
4. Stan Drayton — HC at Temple (2022-23)
5. Tim Beck — HC at Coastal Carolina (2023-present)
6. Jay Norvell — HC at Nevada (2017-21), Colorado State (2022-present)
7. Sterlin Gilbert — HC at McNeese State (2021-present)
8. Mike Sanford Sr. — HC at Indiana State

Format: Coach Name > Assistant Name | Role | Years | Later HC Stops | Confidence
```

### Query 25: Batch — College Small Trees C
```
I'm building a coaching tree database. For each of the following college head coaches, list any assistant coaches who worked under them and later became head coaches (any level). If none found, say "None found."

1. Doc Holliday — HC at Marshall (2010-19)
2. Curt Cignetti — HC at IUP, Elon, James Madison (2019-23), Indiana (2024-present)
3. Manny Diaz — HC at Miami FL (2019-21), Duke (2024-present)
4. Norm Chow — HC at Hawaii (2012-15)
5. Bill Cubit — HC at Western Michigan (2000-04), Illinois (2015, interim)
6. Dan Enos — HC at Central Michigan (2010-14)
7. Kevin Cosgrove — HC at New Mexico (interim)

Format: Coach Name > Assistant Name | Role | Years | Later HC Stops | Confidence
```

### Query 26: Batch — College Small Trees D (Final)
```
I'm building a coaching tree database. For each of the following college head coaches, list any assistant coaches who worked under them and later became head coaches (any level). If none found, say "None found."

1. Ted Roof — HC at Duke (2003-07)
2. Jason Swepson — HC at Elon (approximate years 2010s)
3. Reggie Herring — HC at Houston (interim, approximate year 2012)
4. Joe Pate — HC at Tennessee Tech (approximate years 2000s)
5. Bob DeBesse — HC at Southwest Minnesota State
6. Chip Long — HC at Tulane (2024-present)
7. Jeff Horton — HC at Nevada (approximate), UNLV (approximate)
8. Ted Tollner — HC at San Diego State (approximate 1994-2001)
9. Ralph Friedgen — HC at Maryland (2001-10) [if not already covered in Query 19]
10. Greg Colby — HC at Millersville (D2)
11. Dan Henson — HC at Eastern Illinois
12. Clifford Snow — HC at Connecticut (interim, approximate 1998)
13. Mike Smith — HC at Atlanta Falcons (2008-14)

Format: Coach Name > Assistant Name | Role | Years | Later HC Stops | Confidence
```

---

## Phase 4: Verification (3-5 queries)

After completing Phases 1-3, compile all medium/low confidence entries and run verification batches:

### Verification Template
```
I need to verify the following coaching staff connections. For each, tell me if this is ACCURATE, INACCURATE, or UNCERTAIN. If inaccurate, provide the correction.

1. [Name] was [role] at [school] under [head coach] from approximately [years] — ACCURATE / INACCURATE / UNCERTAIN?
2. [Name] later became head coach at [school(s)] — ACCURATE / INACCURATE / UNCERTAIN?
[repeat for 15-20 entries per batch]

If you can provide a source or reason for your answer, please do.
```

---

## After All Queries Are Done

Bring the collected data back to this project. We will:
1. Parse all ChatGPT responses into the JSON schema
2. Add new coaches to `coaches.json`
3. Add relationships to `relationships.json`
4. Add career stints to `stints.json`
5. Re-run `visualize.py` to regenerate the coaching tree visualization
6. Review for gaps and duplicates

---

## Progress Tracker

| # | Query | Status | New Coaches Found |
|---|-------|--------|-------------------|
| 1 | Pete Carroll tree | TODO | |
| 2 | Jimmy Johnson tree | TODO | |
| 3 | Joe Gibbs tree | TODO | |
| 4 | Ken Hatfield tree | TODO | |
| 5 | Batch: Skip Holtz, Roberts, Phillips, Stockstill | TODO | |
| 6 | Batch: Pough, Palermo, Vaas, Bo Rein, Ron Cooper | TODO | |
| 7 | Brian Kelly tree | TODO | |
| 8 | Mark Dantonio tree | TODO | |
| 9 | Bret Bielema tree | TODO | |
| 10 | Luke Fickell (expand) | TODO | |
| 11 | Ryan Day (expand) | TODO | |
| 12 | Dan Mullen tree | TODO | |
| 13 | Tom Herman tree | TODO | |
| 14 | Greg Schiano tree | TODO | |
| 15 | Pat Narduzzi tree | TODO | |
| 16 | Lane Kiffin tree | TODO | |
| 17 | Ed Orgeron tree | TODO | |
| 18 | Jim Mora Jr. tree | TODO | |
| 19 | Ralph Friedgen tree | TODO | |
| 20 | Steve Addazio tree | TODO | |
| 21 | Batch NFL: Dungy, Tomlin, Harbaugh, Lovie, Rex Ryan | TODO | |
| 22 | Batch NFL: Edwards, Morris, Bradley, etc. | TODO | |
| 23 | Batch College small A | TODO | |
| 24 | Batch College small B | TODO | |
| 25 | Batch College small C | TODO | |
| 26 | Batch College small D | TODO | |
| 27-31 | Verification batches | TODO | |
