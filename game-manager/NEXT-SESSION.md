# Next Session Instructions — Game Day Manager

## Goal
Write `js/app.js` — the only missing file. Then commit and push everything to the `game-manager` branch.

---

## Current State

Branch: `game-manager`
Working directory: `/home/user/development/game-manager/`

### Files complete (do NOT modify):
- `index.html` — app shell, loads style.css + js/data.js + js/recommend.js + js/app.js
- `style.css` — full dark-theme mobile-first styles (~1450 lines)
- `js/data.js` — SGM namespace, data model, localStorage, seed data
- `js/recommend.js` — SGM.recommend(), SGM.prefillQuarter(), SGM.sortBench(), SGM.computeWarnings()
- `roster.csv` — real player roster (14 players)

### Missing:
- `js/app.js` — state management, all view renderers, event handling, CSV import

---

## roster.csv format (already in repo)

```
Name,band,preferred-pos,secondary-pos,keeper_willing,notes
```

Position values in CSV use short form: `mid`, `defense`, `forward`, `keeper`
Map these to: `midfield`, `defense`, `forward`, `keeper`

---

## Key SGM API (from data.js and recommend.js)

```js
SGM.DEFAULT_FORMATION          // { defense:3, midfield:3, forward:2 }
SGM.STATUS_CYCLE               // ['expected','present','absent','late','left_early']
SGM.STATUS_LABELS              // { present:'Present', ... }
SGM.createPlayer(data)         // returns player object with id
SGM.createGame(data)           // returns game object with empty quarters 1-4
SGM.buildInitialState()        // loads from localStorage or returns { roster:[], games:[], gameHistory:[], activeGameId:null }
SGM.saveState(state)           // persists to localStorage
SGM.getActiveGame(state)       // returns active game or null
SGM.getPlayer(state, id)
SGM.getPositionsForGame(game)  // ['keeper','def-1',...,'fwd-2']
SGM.getPositionType(posId)     // 'keeper'|'defense'|'midfield'|'forward'
SGM.getQuarterLineup(game, q)  // { posId: playerId|null }
SGM.getPlayersOnField(game, q) // [playerId, ...]
SGM.getBenchPlayers(game, state, q)
SGM.getAvailablePlayers(game, state)
SGM.getQuartersPlayedThisGame(playerId, game, upToQuarter)
SGM.getFairnessScore(playerId, gameHistory)
SGM.getPlayedLastQuarter(playerId, game, currentQuarter)
SGM.computeBandBalance(playerIds, state)  // {1:n, 2:n, 3:n}
SGM.recommend(posType, q, game, state, excludeId)  // {best:[], good:[], lessIdeal:[]}
SGM.prefillQuarter(game, state, q)  // returns lineup object
SGM.sortBench(players, game, state) // sorted array
SGM.computeWarnings(game, state, q) // [{type, message}, ...]
SGM.computeFeasibility(game, state) // 'on_track'|'at_risk'|'not_feasible'
```

---

## CSS Classes to use in HTML strings

### Layout
- `.view`, `.view-header` (sticky top bar with h1)
- `.dashboard-view`, `.roster-view`, `.setup-view`, `.live-view`, `.postgame-view`
- `.card` (surface card with border)
- `.section-label`

### Buttons
- `.btn .btn-primary`, `.btn .btn-secondary`, `.btn .btn-danger`, `.btn .btn-ghost`, `.btn .btn-sm`, `.btn .btn-full`
- `.fab` (fixed bottom-right + button)
- `.back-btn`

### Band indicators
- `.band-dot .band-dot--1/2/3` (10px colored circle)
- `.band-badge .band-badge--1/2/3` (pill: B1/B2/B3)

### Position chips
- `.pos-chip .pos-chip--keeper/defense/midfield/forward`

### Roster view
- `.player-list`, `.player-row`, `.player-info`, `.player-name-row`, `.player-name`, `.player-positions`
- `.band-group-header` (sticky band section header)

### Form / modal
- `.form-group`, `.form-label`, `.form-input`, `.textarea-input`
- `.radio-group`, `.radio-option`, `.checkbox-group`, `.checkbox-option`, `.option-label`
- `.player-form` (id="pf", data-pid, data-new)
- `.modal-handle`, `.modal-header`, `.modal-title`, `.modal-close`, `.modal-body`, `.modal-footer`
- `.modal-fullscreen` (add to modal-container for player form)

### Setup view
- `.attendance-grid`, `.attendance-row`, `.attendance-name`
- `.status-pill .status-pill--expected/present/absent/late/left_early`
- `.formation-control`, `.formation-label`, `.formation-stepper`, `.stepper-btn`, `.stepper-val`

### Live view
- `.live-header`, `.live-header-top`, `.live-opponent`
- `.live-score`, `.score-input` (id="score-home"/"score-away"), `.score-sep`
- `.quarter-tabs`, `.q-tab`, `.q-tab.active`, `.q-tab.past`, `.q-tab.future`
- `.warnings-banner`, `.warnings-header`, `.warnings-title`, `.warnings-dismiss`, `.warning-item`
- `.readonly-notice`
- `.field-section`, `.field-row`, `.field-row--keeper`
- `.position-slot .position-slot--keeper/defense/midfield/forward` (+ `.readonly`)
- `.slot-label`, `.slot-player`, `.slot-empty`, `.slot-band-dot`, `.quarters-badge`
- `.bench-section`, `.bench-header`, `.bench-chips`
- `.bench-chip`, `.bench-name`, `.bench-jersey`, `.needs-min-tag`
- `.absent-chip`, `.absent-name`
- `.live-footer`

### Player picker modal
- `.picker-section-header .picker-section-header--best/good/less`
- `.picker-current`, `.picker-current-label`, `.picker-current-name`
- `.picker-row`, `.picker-name`, `.picker-jersey`
- `.reason-tag`, `.reason-tag--best`, `.reason-tag--warn`, `.reason-tag--bad`

### Quarter transition modal
- `.transition-modal`, `.transition-title`
- `.transition-summary-item`, `.summary-icon`, `.summary-text`, `.summary-label`

### Post game
- `.postgame-score`, `.final-label`, `.score-display`, `.vs-text`
- `.pt-table`, `.pt-played`, `.pt-total`

### Misc
- `.feasibility-bar .feasibility-bar--on_track/at_risk/not_feasible`
- `.empty-state`, `.empty-icon`, `.empty-text`

---

## app.js Architecture

Single IIFE: `(function() { 'use strict'; var SGM = window.SGM; ... })()`

### State
```js
var state = null;  // persisted: roster, games, gameHistory, activeGameId
var session = {    // NOT persisted
  view: 'dashboard',  // 'dashboard'|'roster'|'setup'|'live'|'postgame'
  modal: null,        // { type: 'picker'|'player-form'|'transition', data: {} }
  viewingQuarter: null,
  warningsDismissed: false
};
var setupData = {   // temp state for game setup screen
  opponent: '',
  formation: { defense:3, midfield:3, forward:2 },
  attendance: {}
};
```

### Core functions
```js
function setState(patch)    // Object.assign(state,patch) + SGM.saveState + render()
function setSession(patch)  // Object.assign(session,patch) + render()
function render()           // routes to correct view, updates nav active, calls renderModal()
function closeModal()       // animate out, then session.modal=null + render()
function attachScoreListeners()  // called after live view renders
```

### Utility functions
```js
function esc(str)           // HTML escape
function bandDot(band)      // returns HTML string
function bandBadge(band)    // returns HTML string
function posChip(type)      // returns HTML string
function posTypeLabel(type) // 'Goalkeeper' etc
function slotLabel(posId)   // 'GK','LD','CD','RD','LM','CM','RM','LF','RF'
function activeGame()       // SGM.getActiveGame(state)
function viewQ()            // session.viewingQuarter || game.currentQuarter
function isCurrentQ()       // viewQ() === game.currentQuarter
```

### CSV Import
```js
var POS_MAP = { mid:'midfield', midfield:'midfield', def:'defense', defense:'defense',
                fwd:'forward', forward:'forward', keeper:'keeper', gk:'keeper' }
function parseCSV(text)          // returns array of row objects
function csvRowToPlayer(row)     // maps CSV row to SGM.createPlayer() call
function loadRosterFromCSV(cb)   // XHR GET 'roster.csv', calls cb(err, players)
```
Called in `init()` only when `state.roster.length === 0`.

### View renderers (all return HTML strings)
- `renderDashboard()` — active game card OR start button + roster summary grid
- `renderRoster()` — sorted by band, band group headers, player rows, FAB
- `renderSetup()` — opponent input, formation steppers, attendance grid
- `renderLive()` — calls renderField() + renderBench(), warnings banner, footer buttons
- `renderField(game, q, isCur)` — 4 rows: fwd/mid/def/keeper
- `slot(posId, lineup, game, q, isCur)` — single position slot
- `renderBench(game, q, isCur)` — sorted bench chips + not-available section
- `renderPickerModal(data)` — 3 sections: best/good/lessIdeal
- `renderPlayerFormModal(data)` — name, band radios, position checkboxes, keeper checkbox, notes
- `renderTransitionModal(data)` — below-min players, band balance, feasibility
- `renderPostgame()` — score card + playing time table

### Event handling
Single `act(action, el)` function handles all data-action attributes.
Event delegation on: `#view-container`, `#modal-container`, `#bottom-nav`.
Overlay click → closeModal().

### Actions list
```
continue-game, new-game, go-dashboard, go-roster
add-player, edit-player, save-player, delete-player
cycle-att, form-inc, form-dec, start-game
view-q, dismiss-warn, open-picker, bench-tap
assign, clear-pos, copy-prior, advance-q, confirm-advance
end-game, finish-game, close-modal
```

---

## Copy Prior Quarter Logic
- Q1: no button
- Q2: "Copy Q1" (priorQ = 1)
- Q3: "Copy Q1" (priorQ = 3-2 = 1)  ← Q3 mirrors Q1
- Q4: "Copy Q2" (priorQ = 4-2 = 2)  ← Q4 mirrors Q2

```js
var priorQ = q >= 3 ? q - 2 : (q === 2 ? 1 : 0);
// show button only when isCur && priorQ > 0
// data-action="copy-prior" data-from="priorQ"
```

---

## Init sequence
```js
function init() {
  state = SGM.buildInitialState();
  if (state.roster.length === 0) {
    loadRosterFromCSV(function(err, players) {
      if (!err && players.length) { state.roster = players; SGM.saveState(state); }
      startApp();
    });
  } else {
    startApp();
  }
}
function startApp() {
  // set initial view based on active game status
  // attach all event listeners
  // call render()
}
document.addEventListener('DOMContentLoaded', init);
```

---

## After writing app.js — commit and push

```bash
git -C /home/user/development add game-manager/js/app.js
git -C /home/user/development commit -m "Add app.js — complete Game Day Manager MVP"
git -C /home/user/development push -u origin game-manager
```

Do NOT create a pull request.
