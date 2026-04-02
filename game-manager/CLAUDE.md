# Youth Soccer Game Day Manager — Claude Context

## What this is
Mobile-first single-page web app for a youth soccer coach to plan and manage live games.
No framework, no build step. Vanilla JS + CSS. Runs on GitHub Pages.

**Live URL:** https://timmeko.github.io/development/game-manager/

**Core principle:** The system suggests. The coach decides. No blocking actions.
**Primary flow:** Tap position → ranked player list → tap player → instant assign.

---

## Repo & Branch
- Repo: `timmeko/development`
- Branch: `game-manager`
- Working dir: `/home/user/development/game-manager/`
- After changes: `git add <files> && git commit && git push -u origin game-manager`
- Do NOT create a pull request

---

## File Structure
```
index.html        — app shell, loads all scripts
style.css         — full dark-theme mobile styles (~1450 lines)
roster.csv        — real player data (14 players, loaded on first run)
js/data.js        — SGM namespace, data model, localStorage, seed data
js/recommend.js   — ranking, prefill, bench sort, warnings
js/app.js         — state, all views, event handling, CSV import
```

---

## Key SGM API (data.js + recommend.js)

```js
// Data
SGM.DEFAULT_FORMATION          // { defense:3, midfield:3, forward:2 }
SGM.STATUS_CYCLE               // ['expected', 'absent']
SGM.STATUS_LABELS              // { expected:'Playing', absent:'Out' }
SGM.createPlayer(data)         // → player object
SGM.createGame(data)           // → game with empty quarters 1-4
SGM.buildInitialState()        // → { roster, games, gameHistory, activeGameId }
SGM.saveState(state)
SGM.getActiveGame(state)
SGM.getPlayer(state, id)
SGM.getPositionsForGame(game)  // ['keeper','def-1',...,'fwd-2']
SGM.getPositionType(posId)     // 'keeper'|'defense'|'midfield'|'forward'
SGM.getQuarterLineup(game, q)  // { posId: playerId|null }
SGM.getPlayersOnField(game, q)
SGM.getBenchPlayers(game, state, q)
SGM.getAvailablePlayers(game, state)  // status === 'expected'
SGM.getQuartersPlayedThisGame(pid, game, upToQ)
SGM.getQuartersScheduled(pid, game)   // total across all 4 quarters
SGM.getFairnessScore(pid, gameHistory)
SGM.computeBandBalance(playerIds, state)  // {1:n, 2:n, 3:n}

// Recommend
SGM.recommend(posType, q, game, state, excludeId) // {best[], good[], lessIdeal[]}
SGM.prefillQuarter(game, state, q)   // → lineup object
SGM.sortBench(players, game, state)  // → sorted array
SGM.computeWarnings(game, state, q)  // → [{type, message}]
SGM.computeFeasibility(game, state)  // 'on_track'|'at_risk'|'not_feasible'
```

---

## App State (app.js)

```js
var state = {   // persisted to localStorage key 'sgm_state'
  roster, games, gameHistory, activeGameId
};
var session = { // NOT persisted
  view: 'dashboard'|'roster'|'setup'|'live'|'postgame',
  modal: null,  // { type: 'picker'|'player-form'|'transition'|'formation-edit', data:{} }
  viewingQuarter: null,
  warningsDismissed: false
};
var setupForm = { opponent, formation, attendance };
```

Key functions: `persist()`, `setSession(patch)`, `render()`, `closeModal()`, `handleAction(action, el)`

---

## Views & Modals
- **Dashboard** — active game card OR start button + roster band summary
- **Roster** — sorted by band, grouped headers, FAB to add
- **Setup** — opponent input, formation steppers, attendance (Playing/Out toggle)
- **Live** — field grid + bench + warnings + footer buttons
- **Postgame** — score + playing time table per player

**Modals:** picker, player-form (fullscreen), transition, formation-edit

---

## Live View Logic
```js
var isEditable = viewQ >= game.currentQuarter;  // current + future quarters
var isLiveQ    = viewQ === game.currentQuarter; // only for advance/end/field-size buttons
```
- Past quarters: read-only notice, no tap actions
- Future quarters: fully editable (pre-game planning)
- Copy Prior Quarter: Q2→copies Q1, Q3→copies Q1, Q4→copies Q2 (N-2 pattern)

---

## Bench Display
- Badge shows `getQuartersScheduled()` — total planned across all 4 quarters
- "Needs min" tag: only shows when `game.currentQuarter > 1 && scheduled < 2`
- Sorted by: needs time first → fewest scheduled → rested last quarter → fairness

---

## Warnings
- `missingKeeper`, `duplicatePlayer`, `invalidCount`, `bandImbalance`
- `belowMinimum` — only fires Q3 and Q4 (`quartersLeft < 2`)
- All warnings are advisory only, never blocking

---

## Formation / Field Size
- Set at game setup (default 1-3-3-2 = 9 players)
- Editable mid-game via "9 players" button in live footer
- Resizes lineups for current + future quarters only; past quarters unchanged
- Position IDs: `keeper`, `def-1/2/3`, `mid-1/2/3`, `fwd-1/2`

---

## roster.csv Format
```
Name,band,preferred-pos,secondary-pos,keeper_willing,notes
```
- Loaded on first run when localStorage is empty
- Position values: `mid`→midfield, `defense`→defense, `forward`→forward, `keeper`→keeper
- `keeper_willing`: `yes` or blank
- Loaded via XHR; falls back to seed data if fetch fails

---

## Attendance Model (simplified)
Two states only:
- `expected` — Playing (green) — default
- `absent` — Out (red)

Tap to toggle. Set during game setup. Available players = `status === 'expected'`.

---

## Design Decisions & Clarifications
1. **No late/left-early states** — planning tool, not real-time tracking
2. **No auto-lineup generator** — suggestions only, coach always decides
3. **No drag-and-drop** — tap only
4. **Goalkeeper is manual** — no automatic keeper suggestions
5. **Band system** — 1=top, 2=mid, 3=developing. Shown as colored dots/badges
6. **Xq badge** = total quarters *scheduled* across all 4 quarters (not just played)
7. **"Needs min" tag** = only meaningful from Q2 onward
8. **Copy Prior Quarter** = N-2 pattern (Q3 mirrors Q1, Q4 mirrors Q2)

---

## CSS Key Classes (style.css)
```
Buttons:     .btn .btn-primary/secondary/danger/ghost/sm/full
Band:        .band-dot .band-dot--1/2/3   .band-badge .band-badge--1/2/3
Position:    .pos-chip .pos-chip--keeper/defense/midfield/forward
Field:       .field-section .field-row .position-slot .position-slot--[type]
             .slot-label .slot-player .slot-empty .slot-band-dot .quarters-badge
Bench:       .bench-section .bench-chip .bench-name .needs-min-tag
Live header: .live-header .live-header-top .live-opponent .live-score .score-input
             .quarter-tabs .q-tab .q-tab.active/.past/.future
Footer:      .live-footer (sticky bottom:0)
Warnings:    .warnings-banner .warning-item .warnings-dismiss
Modal:       .modal-overlay .modal-container .modal-fullscreen
             .modal-handle .modal-header .modal-title .modal-close .modal-body .modal-footer
Picker:      .picker-row .picker-section-header--best/good/less .reason-tag--best/warn/bad
Attendance:  .attendance-row .status-pill .status-pill--expected/absent
Form:        .form-group .form-label .form-input .radio-group .checkbox-group
Misc:        .readonly-notice .feasibility-bar--on_track/at_risk/not_feasible
```

---

## Known Issues / Next Up
- Nothing currently broken
- Potential future work: notes visible during game, mid-game attendance changes
