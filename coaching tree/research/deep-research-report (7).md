# Lou Holtz Coaching Tree Staff Gaps, Confidence Scores, and Punch List Updates

## What this update covers

This update fills the highest-impact holes you flagged for staff completeness and downstream recursion, using primary and near-primary sources where possible: postseason programs from the NC State University Libraries athletics media relations collection, South Carolina’s media guide historical staff list, and South Carolina athletics preseason releases for role clarity. citeturn11view0turn14view0turn17view0turn44view0turn36search10

Key scope decisions:

- “Staff completeness” here is a season-level count of identified staffers, not role clarity.
- Baseline expected total staff per season (for scoring): **10** = head coach + 9 assistants/GAs, since multiple primary sources in this set explicitly list 9 named staffers plus the head coach for a given year. citeturn13view2turn15view0turn17view2turn44view0
- Role taxonomy fields are captured when a source spells out assignments. When it does not, the staffer is still counted for completeness, but role granularity is flagged as a follow-up task.

Downloads created from this research:

- [Download holtz_staffs_priority_updates.csv](sandbox:/mnt/data/holtz_staffs_priority_updates.csv)
- [Download holtz_season_completeness_priority.csv](sandbox:/mnt/data/holtz_season_completeness_priority.csv)
- [Download holtz_punch_list_priority.csv](sandbox:/mnt/data/holtz_punch_list_priority.csv)

## Staff completeness confidence scores by season

### NC State under Holtz

NC State is now strong for 1972–1974 because the postseason publications include explicit staff photo captions and staff bios. citeturn13view2turn15view0turn17view2

- **1972: 1.00 (10/10)**. Staff bios and a staff photo caption identify 9 staffers plus the head coach. citeturn13view0turn13view2  
- **1973: 1.00 (10/10)**. Liberty Bowl program lists 9 staffers plus the head coach in a coaching-staff caption and includes role notes for some assistants. citeturn15view0turn16view1  
- **1974: 1.00 (10/10)**. Astro-Bluebonnet Bowl program lists 9 staffers plus the head coach in the coaching-staff caption, and includes notes for at least one defensive assignment. citeturn17view2turn17view3  
- **1975: 0.30 (3/10)**. In this session, only the head coach plus partial assistants are tied down with sources. Full staff still missing. citeturn25search6turn52search46  

What changed versus the earlier weak state: your NC State block stops being a blocker. The only remaining below-threshold year is 1975.

### South Carolina under Holtz

South Carolina season-level staff completeness is now at target for 1999–2004 because a South Carolina media guide PDF includes an “assistant coaching staffs” year-by-year list that covers every Holtz season with 9 assistant names. citeturn44view0

- **1999: 1.00 (10/10)** citeturn44view0  
- **2000: 1.00 (10/10)** citeturn44view0  
- **2001: 1.00 (10/10)** citeturn44view0  
- **2002: 1.00 (10/10)** citeturn44view0  
- **2003: 1.00 (10/10)** citeturn44view0  
- **2004: 1.00 (10/10)** citeturn44view0  

Role clarity is uneven by year, but name completeness is no longer a blocker.

## What got fixed and what is still below threshold

### NC State 1972–1974 is now usable for network graph edges

You requested “at least one defensive coach chain identified.” This is now unlocked with sourced links to head-coaching outcomes.

- **Chuck Amato** appears on the 1972 staff (as a GA in the NC State postseason publication) and later served as head coach at NC State (2000–2006). citeturn13view2turn52search46  
- **Bo Rein** is listed on Holtz’s NC State staff in postseason publications and later served as head coach for the 1979 NC State team. citeturn13view2turn52search47  

This gives you clean edges:
- Holtz → Amato → (future downstream)
- Holtz → Rein → (future downstream)

### NC State 1975 remains below threshold

The season-level completeness score for 1975 is still below 70%. In this session, the only defensible confirmed nodes were:
- **Brian Burke** as “Off Coach” for 1975 (season page source). citeturn25search6  
- **Chuck Amato** still on staff in 1975 per his coaching-career table (DB coach 1973–1975). citeturn52search46  

Everything else for that year stays on the punch list.

### Arkansas 1978–1983 remains the biggest blocker

In this session, the Arkansas seasons were not rebuilt to ≥70%. The public season summaries reliably identify Holtz each year, and some coordinator names appear by season (example: DC Monte Kiffin in 1978–79; DC Bob Cope in 1980; OC Larry Beightol and DC Don Lindsey in 1981). citeturn51search31turn51search34turn51search33turn51search32  

But you still lack the year-by-year position coach grid. That keeps Arkansas well under the target.

## Downstream coaches and tree status against your goals

This section is a quick “what branches are now unlocked” view, using only what is supported by sources gathered in this session.

### Branches now unlocked from South Carolina

From the South Carolina assistant-staff year lists (1999–2004), you have validated membership on the Holtz staff for several future or former head coaches. citeturn44view0

- **Skip Holtz** is a confirmed South Carolina assistant under Holtz, and his coaching-career table confirms later head-coaching stops (Connecticut, East Carolina, South Florida, Louisiana Tech, and the Birmingham Stallions in spring football). citeturn54search48turn54news50  
  Tree status: **Gen-1 node is solid**. Gen-2 and Gen-3 staffs under Skip are not built in this session.

- **Ron Cooper** is a confirmed 2004 assistant under Holtz, and his coaching-career table confirms multiple head-coaching stops (Eastern Michigan, Louisville, Alabama A&M, interim at FIU, and later LIU). citeturn44view0turn53search32  
  Tree status: **Gen-1 node is solid**. Staffs under him as HC are still missing, so Gen-2 remains blocked.

- **Dave Roberts** is a confirmed South Carolina assistant under Holtz and his biography confirms head coaching roles at Western Kentucky, Northeast Louisiana, and Baylor. citeturn44view0turn47search0  
  Tree status: **Gen-1 node is solid**. Staffs under him as HC are still missing, so Gen-2 remains blocked.

- **Oliver “Buddy” Pough** is confirmed as a South Carolina assistant in early Holtz years, and South Carolina State confirms his long head-coaching tenure there. citeturn44view0turn54search0  
  Tree status: **Gen-1 node is solid**. Gen-2 remains blocked.

- **Joker Phillips** is confirmed as a 2002 South Carolina assistant and later served as head coach at Kentucky. citeturn44view0turn54search49  
  Tree status: **Gen-1 node is solid**. Gen-2 remains blocked.

### Branches unlocked from NC State 1972–1974

- **Chuck Amato** and **Bo Rein** are now confirmed on Holtz’s NC State staff and both later became head coaches at NC State (Rein in 1979, Amato in 2000–06). citeturn13view2turn52search47turn52search46  
  Tree status: **Gen-1 for those two is solid**. Their downstream staffs still need work.

### Below-threshold branches

Against your stated goal for recursion, these remain below threshold because assistant staffs under the Gen-1 head coaches are not populated:

- Ron Cooper branch. citeturn53search32  
- Dave Roberts branch. citeturn47search0  
- Skip Holtz branch (Gen-2 and Gen-3). citeturn54search48  

They are explicitly called out in the punch list file.

## Upstream cleanup result

Your Kent State graduate assistant node should be removed.

Multiple biographical sources agree that Holtz’s coaching career begins as a graduate assistant at Iowa in 1960. His standard coaching-career summaries list Iowa (1960) as the start, then William & Mary (assistant), Connecticut (assistant), South Carolina (assistant), and Ohio State (assistant). citeturn50search35turn50search3turn50search5

This resolves your “no half measures” requirement: the Kent State GA node is not supported by these sources, so it is deleted in the updated punch list.

## Punch list to reach your ≥70% target and unlock recursion

This is the action list that falls out of the updated completeness scoring and tree blockers. The same list is in `holtz_punch_list_priority.csv`.

### High priority items

NC State 1975 staff
- Gap: Only partial names are pinned down right now for 1975. citeturn25search6turn52search46  
- What you need: full on-field assistant list for that season plus roles.
- Best sources to hit next: 1975 NC State media guide staff pages, 1975 game programs with staff page, and preseason newspaper “staff roundup” items.

Arkansas 1978–1983 staff by year
- Gap: assistant coaching staffs by season are not filled. Coordinator-only data is not enough for ≥70%.
- What you need: one table per season that includes OC, DC, and position coaches, plus role continuity year to year.
- Best sources to hit next: Arkansas football media guides for 1978–1983 and offseason hire-change coverage. Wikipedia season infoboxes alone will not meet your threshold. citeturn51search31turn51search32turn51search33turn51search34  

### Medium priority items

South Carolina 2001–2003 role transitions
- Gap: staffer names are complete, but several role shifts still need exact year ranges.
  - Paul Lounsberry OL to TE/ST shift year.
  - Dave Roberts TE or Spurs to RB shift year.
  - Charlie Williams 2003 role. citeturn44view0turn36search10turn43search2  

Dave Roberts branch recursion
- Gap: assistants under Roberts as head coach at Western Kentucky, Northeast Louisiana, and Baylor are missing. citeturn47search0  
- What you need: assistants under Roberts who later became head coaches, plus their own downstream.

Ron Cooper branch recursion
- Gap: assistants under Cooper at Eastern Michigan, Louisville, Alabama A&M, and FIU interim are missing. citeturn53search32turn53search2  

### Low priority item

Kent State GA node
- Status: resolved by deletion (see upstream section). citeturn50search35turn50search3