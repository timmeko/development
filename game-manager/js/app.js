// Soccer Game Day Manager — App
// Depends on: js/data.js, js/recommend.js

(function () {
  'use strict';

  var SGM = window.SGM;

  // ─── Persisted state (roster, games, gameHistory, activeGameId) ─────────
  var state = null;

  // ─── Session state (never persisted) ────────────────────────────────────
  var session = {
    view: 'dashboard',   // dashboard | roster | setup | live | postgame
    modal: null,         // { type, data } or null
    viewingQuarter: null,
    warningsDismissed: false
  };

  // Setup form local state (reset each time setup view opens)
  var setupForm = {
    opponent: '',
    formation: { defense: 3, midfield: 3, forward: 2 },
    attendance: {}
  };

  // ─── State helpers ───────────────────────────────────────────────────────

  function persist() {
    SGM.saveState(state);
  }

  function setSession(patch) {
    Object.assign(session, patch);
    render();
  }

  function activeGame() {
    return SGM.getActiveGame(state);
  }

  function liveQ() {
    var g = activeGame();
    return g ? (session.viewingQuarter || g.currentQuarter) : 1;
  }

  // ─── HTML helpers ────────────────────────────────────────────────────────

  function esc(str) {
    return String(str == null ? '' : str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function bandDot(band) {
    return '<span class="band-dot band-dot--' + band + '"></span>';
  }

  function bandBadge(band) {
    return '<span class="band-badge band-badge--' + band + '">B' + band + '</span>';
  }

  function posChip(type) {
    var lbl = { keeper: 'GK', defense: 'DEF', midfield: 'MID', forward: 'FWD' };
    return '<span class="pos-chip pos-chip--' + type + '">' + (lbl[type] || type) + '</span>';
  }

  function posTypeLabel(type) {
    var lbl = { keeper: 'Goalkeeper', defense: 'Defense', midfield: 'Midfield', forward: 'Forward' };
    return lbl[type] || type;
  }

  // Short display label for a position slot (e.g. def-2 → CD)
  function slotLabel(posId) {
    var map = {
      keeper: 'GK',
      'def-1': 'LD', 'def-2': 'CD', 'def-3': 'RD', 'def-4': 'RD',
      'mid-1': 'LM', 'mid-2': 'CM', 'mid-3': 'RM', 'mid-4': 'RM',
      'fwd-1': 'LF', 'fwd-2': 'RF', 'fwd-3': 'RF'
    };
    return map[posId] || posId.toUpperCase();
  }

  // ─── Render dispatcher ───────────────────────────────────────────────────

  function render() {
    var vc = document.getElementById('view-container');

    // Sync bottom nav active state
    document.querySelectorAll('.nav-tab').forEach(function (tab) {
      tab.classList.toggle('active', tab.dataset.view === session.view);
    });

    var html = '';
    switch (session.view) {
      case 'dashboard': html = renderDashboard(); break;
      case 'roster':    html = renderRoster();    break;
      case 'setup':     html = renderSetup();     break;
      case 'live':      html = renderLive();      break;
      case 'postgame':  html = renderPostgame();  break;
      default:          html = renderDashboard();
    }
    vc.innerHTML = html;

    renderModal();

    // Score inputs need direct listeners (change events)
    if (session.view === 'live') attachScoreListeners();
  }

  // ─── DASHBOARD VIEW ──────────────────────────────────────────────────────

  function renderDashboard() {
    var game = activeGame();
    var roster = state.roster;
    var b1 = roster.filter(function (p) { return p.band === 1; }).length;
    var b2 = roster.filter(function (p) { return p.band === 2; }).length;
    var b3 = roster.filter(function (p) { return p.band === 3; }).length;

    var gameCard = '';
    if (game && game.status !== 'complete') {
      var feas = SGM.computeFeasibility(game, state);
      var feasLabel = { on_track: 'On track', at_risk: 'At risk', not_feasible: 'Not feasible' }[feas];
      gameCard =
        '<div class="active-game-card">' +
          '<div class="game-meta">' +
            '<div>' +
              '<div class="active-game-indicator"><span class="pulse-dot"></span> Live Game</div>' +
              '<div class="opponent">' + esc(game.opponent || 'vs Opponent') + '</div>' +
              '<div class="quarter-badge">Quarter ' + game.currentQuarter + ' of 4</div>' +
            '</div>' +
            '<div class="game-score">' + game.score.home + ' \u2013 ' + game.score.away + '</div>' +
          '</div>' +
          '<div class="feasibility-bar feasibility-bar--' + feas + '">Playing time: ' + feasLabel + '</div>' +
          '<button class="btn btn-primary btn-full" data-action="continue-game">Continue Game \u2192</button>' +
        '</div>';
    } else {
      gameCard =
        '<button class="btn btn-primary btn-full" style="font-size:17px;padding:18px;" data-action="new-game">' +
          'Start New Game' +
        '</button>';
    }

    return (
      '<div class="view dashboard-view">' +
        '<div class="dashboard-logo"><h1>Game Day</h1><p>Youth Soccer Manager</p></div>' +
        gameCard +
        '<div class="card">' +
          '<div style="font-size:14px;font-weight:700;margin-bottom:12px;">Roster</div>' +
          '<div class="roster-summary-grid">' +
            '<div class="roster-stat"><div class="stat-val">' + roster.length + '</div><div class="stat-lbl">Players</div></div>' +
            '<div class="roster-stat"><div class="stat-val" style="color:var(--band1)">' + b1 + '</div><div class="stat-lbl">Band 1</div></div>' +
            '<div class="roster-stat"><div class="stat-val" style="color:var(--band2)">' + b2 + '</div><div class="stat-lbl">Band 2</div></div>' +
            '<div class="roster-stat"><div class="stat-val" style="color:var(--band3)">' + b3 + '</div><div class="stat-lbl">Band 3</div></div>' +
          '</div>' +
          '<button class="btn btn-secondary btn-full" style="margin-top:12px;" data-action="go-roster">Manage Roster</button>' +
        '</div>' +
        '<div style="margin-top:8px;text-align:center;">' +
          '<button class="btn btn-ghost btn-sm" style="color:var(--muted);font-size:12px;" data-action="restart-session">Reset All Data</button>' +
        '</div>' +
      '</div>'
    );
  }

  // ─── LIVE GAME VIEW ──────────────────────────────────────────────────────

  function renderLive() {
    var game = activeGame();
    if (!game) {
      return (
        '<div class="view" style="padding:24px;text-align:center;">' +
          '<p style="color:var(--muted);margin-bottom:16px;">No active game.</p>' +
          '<button class="btn btn-primary" data-action="new-game">Start New Game</button>' +
        '</div>'
      );
    }

    var viewQ      = liveQ();
    var isLiveQ    = (viewQ === game.currentQuarter);   // the active quarter
    var isEditable = (viewQ >= game.currentQuarter);    // current or future = editable
    var warnings   = SGM.computeWarnings(game, state, viewQ);
    var showWarn   = !session.warningsDismissed && warnings.length > 0;

    // Quarter tabs — past quarters read-only, current + future editable
    var tabs = [1, 2, 3, 4].map(function (q) {
      var cls = 'q-tab';
      if (q === viewQ)              cls += ' active';
      else if (q < game.currentQuarter) cls += ' past';
      else                          cls += ' future';
      return '<button class="' + cls + '" data-action="view-quarter" data-q="' + q + '">Q' + q + '</button>';
    }).join('');

    // Warnings banner
    var warnHTML = '';
    if (showWarn) {
      warnHTML =
        '<div class="warnings-banner">' +
          '<div class="warnings-header">' +
            '<span class="warnings-title">Warnings</span>' +
            '<button class="warnings-dismiss" data-action="dismiss-warnings">\u00d7</button>' +
          '</div>' +
          warnings.map(function (w) {
            return '<div class="warning-item">' + esc(w.message) + '</div>';
          }).join('') +
        '</div>';
    }

    // Read-only notice only for past quarters
    var readonlyNotice = (viewQ < game.currentQuarter)
      ? '<div class="readonly-notice">Q' + viewQ + ' already played \u2014 read only</div>'
      : '';

    // Copy Prior Quarter button — available for any editable quarter
    // Q1 → none; Q2 → copy Q1; Q3 → copy Q1 (N-2); Q4 → copy Q2 (N-2)
    var priorQ = viewQ >= 3 ? viewQ - 2 : (viewQ === 2 ? 1 : 0);
    var copyBtn = (isEditable && priorQ > 0)
      ? '<button class="btn btn-secondary" data-action="copy-prior" data-from-q="' + priorQ + '">Copy Q' + priorQ + '</button>'
      : '';

    // Advance / End button — only on the live quarter
    var advBtn = '';
    if (isLiveQ) {
      advBtn = game.currentQuarter < 4
        ? '<button class="btn btn-primary" style="flex:1;" data-action="advance-quarter">End Q' + game.currentQuarter + ' \u2192</button>'
        : '<button class="btn btn-danger"  style="flex:1;" data-action="end-game">End Game</button>';
    }

    // Field size button — only on live quarter
    var f = game.formation;
    var totalPlayers = 1 + f.defense + f.midfield + f.forward;
    var fieldSizeBtn = isLiveQ
      ? '<button class="btn btn-secondary btn-sm" data-action="edit-formation">' + totalPlayers + ' players</button>'
      : '';

    return (
      '<div class="live-view">' +
        '<div class="live-header">' +
          '<div class="live-header-top">' +
            '<div class="live-opponent">' + esc(game.opponent || 'Game') + '</div>' +
            '<div class="live-score">' +
              '<input class="score-input" id="score-home" type="number" min="0" max="99" value="' + game.score.home + '">' +
              '<span class="score-sep">\u2013</span>' +
              '<input class="score-input" id="score-away" type="number" min="0" max="99" value="' + game.score.away + '">' +
            '</div>' +
          '</div>' +
          '<div class="quarter-tabs">' + tabs + '</div>' +
        '</div>' +
        warnHTML +
        readonlyNotice +
        renderField(game, viewQ, isEditable) +
        renderBench(game, viewQ, isEditable) +
        '<div class="live-footer">' + fieldSizeBtn + copyBtn + advBtn + '</div>' +
      '</div>'
    );
  }

  function renderField(game, quarterNum, isEditable) {
    var positions = SGM.getPositionsForGame(game);
    var lineup    = SGM.getQuarterLineup(game, quarterNum);

    var fwd = positions.filter(function (p) { return p.startsWith('fwd'); });
    var mid = positions.filter(function (p) { return p.startsWith('mid'); });
    var def = positions.filter(function (p) { return p.startsWith('def'); });
    var gk  = positions.filter(function (p) { return p === 'keeper'; });

    function row(ids) {
      return '<div class="field-row">' +
        ids.map(function (id) { return renderSlot(id, lineup, game, quarterNum, isEditable); }).join('') +
      '</div>';
    }

    return (
      '<div class="field-section">' +
        (fwd.length ? row(fwd) : '') +
        (mid.length ? row(mid) : '') +
        (def.length ? row(def) : '') +
        (gk.length  ? row(gk)  : '') +
      '</div>'
    );
  }

  function renderSlot(posId, lineup, game, quarterNum, isEditable) {
    var posType  = SGM.getPositionType(posId);
    var pid      = lineup[posId];
    var player   = pid ? SGM.getPlayer(state, pid) : null;
    var doneQ    = quarterNum - 1;

    var cls = 'position-slot position-slot--' + posType + (isEditable ? '' : ' readonly');
    var attrs = isEditable
      ? 'data-action="open-picker" data-pos-id="' + posId + '" data-quarter="' + quarterNum + '"'
      : '';

    var inner = '';
    if (player) {
      var scheduled = SGM.getQuartersScheduled(player.id, game);
      inner =
        '<div class="slot-band-dot band-dot band-dot--' + player.band + '"></div>' +
        '<div class="slot-label">' + slotLabel(posId) + '</div>' +
        '<div class="slot-player">' + esc(player.name) + '</div>' +
        (player.jersey ? '<div class="slot-jersey">#' + esc(player.jersey) + '</div>' : '') +
        '<div class="quarters-badge" style="margin-top:2px;">' + scheduled + 'q</div>';
    } else {
      inner =
        '<div class="slot-label">' + slotLabel(posId) + '</div>' +
        '<div class="slot-empty">Tap to assign</div>';
    }

    return '<div class="' + cls + '" ' + attrs + '>' + inner + '</div>';
  }

  function renderBench(game, quarterNum, isEditable) {
    var bench  = SGM.getBenchPlayers(game, state, quarterNum);
    var sorted = SGM.sortBench(bench, game, state);
    var chips = sorted.map(function (p) {
      var scheduled = SGM.getQuartersScheduled(p.id, game);
      var needsMin  = game.currentQuarter > 1 && scheduled < 2;
      var attrs     = isEditable ? 'data-action="bench-tap" data-player-id="' + p.id + '"' : '';
      return (
        '<div class="bench-chip" ' + attrs + '>' +
          bandDot(p.band) +
          '<span class="bench-name">' + esc(p.name) + '</span>' +
          (p.jersey ? '<span class="bench-jersey">#' + esc(p.jersey) + '</span>' : '') +
          '<span class="quarters-badge">' + scheduled + 'q</span>' +
          (needsMin ? '<span class="needs-min-tag">Needs min</span>' : '') +
        '</div>'
      );
    }).join('');

    // Unavailable players (marked Out)
    var unavail = state.roster.filter(function (p) {
      var s = game.attendance[p.id] || 'expected';
      return s === 'absent';
    });

    var unavailHTML = unavail.length
      ? '<div style="margin-top:10px;padding-top:10px;border-top:1px solid var(--border);">' +
          '<div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px;">Not Available</div>' +
          unavail.map(function (p) {
            var s = game.attendance[p.id] || 'expected';
            return (
              '<div class="absent-chip">' +
                bandDot(p.band) +
                '<span class="absent-name">' + esc(p.name) + '</span>' +
                '<span class="status-pill status-pill--' + s + '">' + SGM.STATUS_LABELS[s] + '</span>' +
              '</div>'
            );
          }).join('') +
        '</div>'
      : '';

    return (
      '<div class="bench-section">' +
        '<div class="bench-header">On Bench (' + sorted.length + ')</div>' +
        '<div class="bench-chips">' + chips + '</div>' +
        unavailHTML +
      '</div>'
    );
  }

  function attachScoreListeners() {
    var homeEl = document.getElementById('score-home');
    var awayEl = document.getElementById('score-away');
    if (!homeEl || !awayEl) return;
    function save() {
      var g = activeGame();
      if (!g) return;
      g.score.home = Math.max(0, Math.min(99, parseInt(homeEl.value) || 0));
      g.score.away = Math.max(0, Math.min(99, parseInt(awayEl.value) || 0));
      persist();
    }
    homeEl.addEventListener('change', save);
    awayEl.addEventListener('change', save);
  }

  // ─── GAME SETUP VIEW ─────────────────────────────────────────────────────

  function renderSetup() {
    var f = setupForm.formation;
    var total = 1 + f.defense + f.midfield + f.forward;

    var rows = state.roster.slice().sort(function (a, b) {
      if (a.band !== b.band) return a.band - b.band;
      return a.name.localeCompare(b.name);
    }).map(function (p) {
      var status = setupForm.attendance[p.id] || 'expected';
      return (
        '<div class="attendance-row" data-action="cycle-attendance" data-player-id="' + p.id + '">' +
          bandDot(p.band) +
          '<div class="attendance-name">' +
            esc(p.name) +
            (p.jersey ? ' <span style="color:var(--muted)">#' + esc(p.jersey) + '</span>' : '') +
          '</div>' +
          bandBadge(p.band) +
          '<span class="status-pill status-pill--' + status + '">' + SGM.STATUS_LABELS[status] + '</span>' +
        '</div>'
      );
    }).join('');

    function stepper(label, type, val, min, max) {
      return (
        '<div class="formation-control">' +
          '<div class="formation-label">' + posChip(type) + ' ' + label + '</div>' +
          '<div class="formation-stepper">' +
            '<button class="stepper-btn" data-action="form-dec" data-ftype="' + type + '" data-min="' + min + '">\u2212</button>' +
            '<div class="stepper-val">' + val + '</div>' +
            '<button class="stepper-btn" data-action="form-inc" data-ftype="' + type + '" data-max="' + max + '">+</button>' +
          '</div>' +
        '</div>'
      );
    }

    return (
      '<div class="view setup-view">' +
        '<div class="view-header">' +
          '<button data-action="go-dashboard" style="font-size:26px;color:var(--muted);padding:2px 8px;">\u2039</button>' +
          '<h1>New Game</h1>' +
        '</div>' +

        '<div class="form-group">' +
          '<label class="form-label">Opponent</label>' +
          '<input class="form-input" id="setup-opponent" type="text" placeholder="Opponent name" value="' + esc(setupForm.opponent) + '">' +
        '</div>' +

        '<div class="card">' +
          '<div style="font-size:14px;font-weight:700;margin-bottom:4px;">' +
            'Formation <span style="color:var(--muted);font-weight:400;font-size:13px;">(' + total + ' on field)</span>' +
          '</div>' +
          stepper('Forwards',    'forward',  f.forward,  1, 3) +
          stepper('Midfielders', 'midfield', f.midfield, 2, 5) +
          stepper('Defenders',   'defense',  f.defense,  2, 5) +
          '<div class="formation-control" style="border-bottom:none;">' +
            '<div class="formation-label">' + posChip('keeper') + ' Goalkeeper</div>' +
            '<div style="font-size:16px;font-weight:700;color:var(--muted)">1</div>' +
          '</div>' +
        '</div>' +

        '<div class="card">' +
          '<div style="font-size:14px;font-weight:700;margin-bottom:8px;">' +
            'Attendance <span style="color:var(--muted);font-weight:400;font-size:12px;">tap to change</span>' +
          '</div>' +
          '<div class="attendance-grid">' + rows + '</div>' +
        '</div>' +

        '<button class="btn btn-primary btn-full" style="font-size:17px;padding:16px;" data-action="start-game">Start Game</button>' +
      '</div>'
    );
  }

  // ─── MODAL RENDERER ──────────────────────────────────────────────────────

  function renderModal() {
    var overlay   = document.getElementById('modal-overlay');
    var container = document.getElementById('modal-container');

    if (!session.modal) {
      overlay.classList.add('hidden');
      overlay.classList.remove('visible');
      container.classList.add('hidden');
      container.classList.remove('visible', 'modal-fullscreen');
      container.innerHTML = '';
      return;
    }

    var html        = '';
    var isFullscreen = false;
    switch (session.modal.type) {
      case 'picker':      html = renderPickerModal(session.modal.data);     break;
      case 'player-form': html = renderPlayerFormModal(session.modal.data); isFullscreen = true; break;
      case 'transition':       html = renderTransitionModal(session.modal.data);    break;
      case 'formation-edit':   html = renderFormationEditModal(session.modal.data); break;
    }

    container.innerHTML = html;
    overlay.classList.remove('hidden');
    container.classList.remove('hidden');
    container.classList.toggle('modal-fullscreen', isFullscreen);

    requestAnimationFrame(function () {
      overlay.classList.add('visible');
      container.classList.add('visible');
    });
  }

  function closeModal(cb) {
    var overlay   = document.getElementById('modal-overlay');
    var container = document.getElementById('modal-container');
    overlay.classList.remove('visible');
    container.classList.remove('visible');
    setTimeout(function () {
      session.modal = null;
      renderModal();
      if (cb) cb();
    }, 250);
  }

  // ─── EVENT HANDLER ───────────────────────────────────────────────────────

  function handleAction(action, el) {
    var game = activeGame();

    switch (action) {

      // Navigation
      case 'continue-game':
        session.viewingQuarter = null;
        session.warningsDismissed = false;
        setSession({ view: 'live' });
        break;

      case 'new-game':
        setupForm.opponent   = '';
        setupForm.formation  = Object.assign({}, SGM.DEFAULT_FORMATION);
        setupForm.attendance = {};
        setSession({ view: 'setup' });
        break;

      case 'go-dashboard': setSession({ view: 'dashboard' }); break;
      case 'go-roster':    setSession({ view: 'roster' });    break;

      // Roster
      case 'add-player':
        setSession({ modal: { type: 'player-form', data: {} } });
        break;

      case 'edit-player':
        setSession({ modal: { type: 'player-form', data: { playerId: el.dataset.playerId } } });
        break;

      case 'save-player': {
        var form = document.getElementById('player-form');
        if (!form) break;
        var nameVal = document.getElementById('pf-name').value.trim();
        if (!nameVal) { alert('Name is required'); break; }

        var prefPos = [], secPos = [];
        form.querySelectorAll('input[data-field="preferredPositions"]:checked').forEach(function (cb) { prefPos.push(cb.dataset.val); });
        form.querySelectorAll('input[data-field="secondaryPositions"]:checked').forEach(function (cb)  { secPos.push(cb.dataset.val); });
        var bandEl = form.querySelector('input[name="pf-band"]:checked');

        var patch = {
          name:               nameVal,
          jersey:             document.getElementById('pf-jersey').value.trim(),
          band:               bandEl ? parseInt(bandEl.value) : 2,
          preferredPositions: prefPos,
          secondaryPositions: secPos,
          keeperWilling:      document.getElementById('pf-keeper').checked,
          notes:              document.getElementById('pf-notes').value.trim()
        };

        if (form.dataset.isNew === 'true') {
          state.roster.push(SGM.createPlayer(patch));
        } else {
          var existing = SGM.getPlayer(state, form.dataset.playerId);
          if (existing) Object.assign(existing, patch);
        }
        persist();
        closeModal(function () { render(); });
        break;
      }

      case 'delete-player':
        if (confirm('Remove this player from the roster?')) {
          state.roster = state.roster.filter(function (p) { return p.id !== el.dataset.playerId; });
          persist();
          closeModal(function () { render(); });
        }
        break;

      // Setup form
      case 'cycle-attendance': {
        var pid  = el.dataset.playerId;
        var cur  = setupForm.attendance[pid] || 'expected';
        var idx  = SGM.STATUS_CYCLE.indexOf(cur);
        setupForm.attendance[pid] = SGM.STATUS_CYCLE[(idx + 1) % SGM.STATUS_CYCLE.length];
        render();
        break;
      }

      case 'form-inc': {
        var ft  = el.dataset.ftype;
        var max = parseInt(el.dataset.max) || 5;
        setupForm.formation[ft] = Math.min(max, (setupForm.formation[ft] || 0) + 1);
        render();
        break;
      }

      case 'form-dec': {
        var ft2 = el.dataset.ftype;
        var min = parseInt(el.dataset.min) || 1;
        setupForm.formation[ft2] = Math.max(min, (setupForm.formation[ft2] || 0) - 1);
        render();
        break;
      }

      case 'start-game': {
        var oppEl = document.getElementById('setup-opponent');
        setupForm.opponent = oppEl ? oppEl.value.trim() : '';
        var newGame = SGM.createGame({
          opponent:   setupForm.opponent,
          formation:  Object.assign({}, setupForm.formation),
          attendance: Object.assign({}, setupForm.attendance)
        });
        state.games.push(newGame);
        state.activeGameId = newGame.id;
        persist();
        session.viewingQuarter    = null;
        session.warningsDismissed = false;
        setSession({ view: 'live' });
        break;
      }

      // Live game
      case 'view-quarter':
        session.viewingQuarter    = parseInt(el.dataset.q);
        session.warningsDismissed = false;
        render();
        break;

      case 'dismiss-warnings':
        session.warningsDismissed = true;
        render();
        break;

      case 'open-picker':
        setSession({ modal: { type: 'picker', data: { posId: el.dataset.posId, quarterNum: parseInt(el.dataset.quarter) } } });
        break;

      case 'bench-tap': {
        // Find the first empty preferred or any empty slot for this player
        if (!game) break;
        var bpid    = el.dataset.playerId;
        var bPlayer = SGM.getPlayer(state, bpid);
        var lineup  = SGM.getQuarterLineup(game, game.currentQuarter);
        var allPos  = SGM.getPositionsForGame(game);
        var target  = null;
        // preferred match first
        for (var i = 0; i < allPos.length; i++) {
          if (!lineup[allPos[i]] && SGM.getPositionMatch(bPlayer, SGM.getPositionType(allPos[i])) === 'preferred') {
            target = allPos[i]; break;
          }
        }
        // any empty slot
        if (!target) {
          for (var j = 0; j < allPos.length; j++) {
            if (!lineup[allPos[j]]) { target = allPos[j]; break; }
          }
        }
        if (target) {
          setSession({ modal: { type: 'picker', data: { posId: target, quarterNum: game.currentQuarter } } });
        }
        break;
      }

      case 'assign-player': {
        if (!game) break;
        var apid    = el.dataset.playerId;
        var posId   = el.dataset.posId;
        var qNum    = parseInt(el.dataset.quarter);
        var lu      = game.quarters[qNum].lineup;
        // Remove this player from any other slot first
        Object.keys(lu).forEach(function (k) { if (lu[k] === apid) lu[k] = null; });
        lu[posId] = apid;
        persist();
        session.warningsDismissed = false;
        closeModal(function () { render(); });
        break;
      }

      case 'clear-slot': {
        if (!game) break;
        game.quarters[parseInt(el.dataset.quarter)].lineup[el.dataset.posId] = null;
        persist();
        closeModal(function () { render(); });
        break;
      }

      case 'copy-prior': {
        if (!game) break;
        var fromQ   = parseInt(el.dataset.fromQ);
        var curQ    = session.viewingQuarter || game.currentQuarter;
        var fromLu  = SGM.getQuarterLineup(game, fromQ);
        game.quarters[curQ].lineup = Object.assign({}, fromLu);
        persist();
        session.warningsDismissed = false;
        render();
        break;
      }

      case 'edit-formation':
        setSession({ modal: { type: 'formation-edit', data: {} } });
        break;

      case 'fe-inc': {
        if (!game) break;
        var feType = el.dataset.type, feMax = parseInt(el.dataset.max) || 4;
        game.formation[feType] = Math.min(feMax, game.formation[feType] + 1);
        // Re-render the stepper val in place without closing modal
        var valEl = document.getElementById('fe-val-' + feType);
        if (valEl) valEl.textContent = game.formation[feType];
        var titleEl = document.querySelector('.modal-title');
        if (titleEl) {
          var f2 = game.formation;
          titleEl.innerHTML = 'Field Size <span style="color:var(--muted);font-size:13px;font-weight:400">(' + (1+f2.defense+f2.midfield+f2.forward) + ' players)</span>';
        }
        break;
      }

      case 'fe-dec': {
        if (!game) break;
        var feType2 = el.dataset.type, feMin = parseInt(el.dataset.min) || 1;
        game.formation[feType2] = Math.max(feMin, game.formation[feType2] - 1);
        var valEl2 = document.getElementById('fe-val-' + feType2);
        if (valEl2) valEl2.textContent = game.formation[feType2];
        var titleEl2 = document.querySelector('.modal-title');
        if (titleEl2) {
          var f3 = game.formation;
          titleEl2.innerHTML = 'Field Size <span style="color:var(--muted);font-size:13px;font-weight:400">(' + (1+f3.defense+f3.midfield+f3.forward) + ' players)</span>';
        }
        break;
      }

      case 'save-formation': {
        if (!game) break;
        // Resize lineups for current and future quarters — preserve existing assignments where slot still exists
        var newPositions = SGM.getPositionsForGame(game);
        for (var q = game.currentQuarter; q <= 4; q++) {
          var oldLineup = game.quarters[q].lineup;
          var newLineup = {};
          newPositions.forEach(function (posId) {
            newLineup[posId] = oldLineup[posId] !== undefined ? oldLineup[posId] : null;
          });
          game.quarters[q].lineup = newLineup;
        }
        persist();
        closeModal();
        setTimeout(render, 260);
        break;
      }

      case 'advance-quarter':
        if (!game) break;
        setSession({ modal: { type: 'transition', data: { fromQ: game.currentQuarter } } });
        break;

      case 'confirm-advance': {
        if (!game) break;
        var toQ      = parseInt(el.dataset.toQ);
        var prefilled = SGM.prefillQuarter(game, state, toQ);
        game.quarters[toQ].lineup = prefilled;
        game.currentQuarter       = toQ;
        persist();
        session.viewingQuarter    = null;
        session.warningsDismissed = false;
        closeModal(function () { render(); });
        break;
      }

      case 'end-game':
        if (!game) break;
        game.status = 'complete';
        persist();
        setSession({ view: 'postgame' });
        break;

      case 'finish-game': {
        if (!game) break;
        state.roster.forEach(function (p) {
          var s = game.attendance[p.id] || 'expected';
          if (s !== 'expected') return;
          var qp = SGM.getQuartersPlayedThisGame(p.id, game, 4);
          state.gameHistory.push({ gameId: game.id, playerId: p.id, quartersPlayed: qp, attended: true });
        });
        state.activeGameId = null;
        persist();
        setSession({ view: 'dashboard' });
        break;
      }

      case 'close-modal':
        closeModal();
        break;

      case 'restart-session':
        if (confirm('Reset all data and start fresh?\n\nThis clears the roster, all games, and game history.')) {
          SGM.clearState();
          window.location.reload();
        }
        break;
    }
  }

  // ─── CSV ROSTER IMPORT ───────────────────────────────────────────────────

  var POS_MAP = {
    mid: 'midfield', midfield: 'midfield',
    def: 'defense',  defense:  'defense',
    fwd: 'forward',  forward:  'forward',
    keeper: 'keeper', gk: 'keeper'
  };

  function parseCSV(text) {
    var lines = text.trim().split(/\r?\n/);
    if (lines.length < 2) return [];
    var headers = lines[0].split(',').map(function (h) { return h.trim().toLowerCase(); });
    return lines.slice(1).map(function (line) {
      var vals = line.split(',').map(function (v) { return v.trim(); });
      var row = {};
      headers.forEach(function (h, i) { row[h] = vals[i] || ''; });
      return row;
    });
  }

  function csvRowToPlayer(row) {
    function parsePos(str) {
      if (!str) return [];
      return str.split(/[;|\/\s]+/).map(function (s) {
        return POS_MAP[s.trim().toLowerCase()] || null;
      }).filter(Boolean);
    }
    return SGM.createPlayer({
      name:               row['name'] || '',
      band:               parseInt(row['band']) || 2,
      preferredPositions: parsePos(row['preferred-pos']),
      secondaryPositions: parsePos(row['secondary-pos']),
      keeperWilling:      (row['keeper_willing'] || '').toLowerCase() === 'yes',
      notes:              row['notes'] || ''
    });
  }

  function loadRosterFromCSV(callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'roster.csv', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        var players = parseCSV(xhr.responseText)
          .map(csvRowToPlayer)
          .filter(function (p) { return p.name; });
        callback(null, players);
      } else {
        callback(new Error('HTTP ' + xhr.status));
      }
    };
    xhr.onerror = function () { callback(new Error('fetch failed')); };
    xhr.send();
  }

  // ─── INIT ────────────────────────────────────────────────────────────────

  function startApp() {
    // Restore to live/postgame if a game was in progress
    var g = SGM.getActiveGame(state);
    if (g && g.status === 'active')   session.view = 'live';
    if (g && g.status === 'complete') session.view = 'postgame';

    // Delegate clicks from view container
    document.getElementById('view-container').addEventListener('click', function (e) {
      var el = e.target.closest('[data-action]');
      if (el) handleAction(el.dataset.action, el);
    });

    // Delegate clicks from modal container
    document.getElementById('modal-container').addEventListener('click', function (e) {
      var el = e.target.closest('[data-action]');
      if (el) handleAction(el.dataset.action, el);
    });

    // Close modal on overlay tap
    document.getElementById('modal-overlay').addEventListener('click', function () {
      closeModal();
    });

    // Bottom nav tabs
    document.getElementById('bottom-nav').addEventListener('click', function (e) {
      var tab = e.target.closest('.nav-tab');
      if (!tab) return;
      var view = tab.dataset.view;
      if (view === 'live' && !SGM.getActiveGame(state)) {
        // No game → go to setup
        setupForm.opponent   = '';
        setupForm.formation  = Object.assign({}, SGM.DEFAULT_FORMATION);
        setupForm.attendance = {};
        setSession({ view: 'setup' });
        return;
      }
      session.viewingQuarter    = null;
      session.warningsDismissed = false;
      setSession({ view: view });
    });

    render();
  }

  function init() {
    var hasSaved = !!SGM.loadState();
    state = SGM.buildInitialState();

    if (!hasSaved) {
      // First run — try to load real roster from roster.csv, fall back to seed data
      loadRosterFromCSV(function (err, players) {
        if (!err && players && players.length) {
          state.roster = players;
          SGM.saveState(state);
        }
        startApp();
      });
    } else {
      startApp();
    }
  }

  document.addEventListener('DOMContentLoaded', init);

  // ─── QUARTER TRANSITION MODAL ────────────────────────────────────────────

  function renderTransitionModal(data) {
    var game  = activeGame();
    if (!game) return '';
    var fromQ = data.fromQ;
    var toQ   = fromQ + 1;

    // Players who still need more minutes
    var present  = SGM.getAvailablePlayers(game, state);
    var belowMin = present.filter(function (p) {
      return SGM.getQuartersPlayedThisGame(p.id, game, fromQ) < 2;
    });

    // Band balance for the quarter just completed
    var fieldIds  = SGM.getPlayersOnField(game, fromQ);
    var bandCnt   = SGM.computeBandBalance(fieldIds, state);
    var feas      = SGM.computeFeasibility(game, state);
    var feasLabel = { on_track: 'On Track', at_risk: 'At Risk', not_feasible: 'Not Feasible' }[feas];
    var feasIcon  = { on_track: '\u2705', at_risk: '\u26a0\ufe0f', not_feasible: '\u274c' }[feas];
    var feasColor = { on_track: 'var(--primary)', at_risk: 'var(--amber)', not_feasible: 'var(--red)' }[feas];

    var belowHTML = belowMin.length
      ? '<div class="transition-summary-item">' +
          '<span class="summary-icon">\u26a0\ufe0f</span>' +
          '<div class="summary-text">' +
            '<div class="summary-label" style="color:var(--amber)">Needs more time</div>' +
            belowMin.map(function (p) {
              var qp = SGM.getQuartersPlayedThisGame(p.id, game, fromQ);
              return esc(p.name) + ' (' + qp + 'q)';
            }).join(', ') +
          '</div>' +
        '</div>'
      : '';

    var bandHTML = fieldIds.length
      ? '<div class="transition-summary-item">' +
          '<span class="summary-icon">\ud83c\udf96\ufe0f</span>' +
          '<div class="summary-text">' +
            '<div class="summary-label">Q' + fromQ + ' Band Balance</div>' +
            '<span style="color:var(--band1)">B1: ' + (bandCnt[1] || 0) + '</span> &middot; ' +
            '<span style="color:var(--band2)">B2: ' + (bandCnt[2] || 0) + '</span> &middot; ' +
            '<span style="color:var(--band3)">B3: ' + (bandCnt[3] || 0) + '</span>' +
          '</div>' +
        '</div>'
      : '';

    var spots = 1 + game.formation.defense + game.formation.midfield + game.formation.forward;
    var feasHTML =
      '<div class="transition-summary-item">' +
        '<span class="summary-icon">' + feasIcon + '</span>' +
        '<div class="summary-text">' +
          '<div class="summary-label" style="color:' + feasColor + '">Playing Time: ' + feasLabel + '</div>' +
          present.length + ' players, ' + spots + ' spots/quarter' +
        '</div>' +
      '</div>';

    return (
      '<div class="modal-handle"></div>' +
      '<div class="modal-header">' +
        '<span class="modal-title">End of Q' + fromQ + '</span>' +
        '<button class="modal-close" data-action="close-modal">\u00d7</button>' +
      '</div>' +
      '<div class="modal-body">' +
        '<div class="transition-modal">' +
          '<div class="transition-title">Q' + fromQ + ' Complete</div>' +
          belowHTML + bandHTML + feasHTML +
        '</div>' +
      '</div>' +
      '<div class="modal-footer">' +
        '<button class="btn btn-primary btn-full" data-action="confirm-advance" data-to-q="' + toQ + '">Continue to Q' + toQ + '</button>' +
        '<button class="btn btn-ghost btn-full" style="margin-top:6px;" data-action="close-modal">Stay in Q' + fromQ + '</button>' +
      '</div>'
    );
  }

  // ─── FORMATION EDIT MODAL ────────────────────────────────────────────────

  function renderFormationEditModal(data) {
    var game = activeGame();
    if (!game) return '';
    var f = game.formation;
    var total = 1 + f.defense + f.midfield + f.forward;

    function stepper(label, type, val, min, max) {
      return '<div class="formation-control">' +
        '<div class="formation-label">' + posChip(type) + ' ' + label + '</div>' +
        '<div class="formation-stepper">' +
          '<button class="stepper-btn" data-action="fe-dec" data-type="' + type + '" data-min="' + min + '">−</button>' +
          '<div class="stepper-val" id="fe-val-' + type + '">' + val + '</div>' +
          '<button class="stepper-btn" data-action="fe-inc" data-type="' + type + '" data-max="' + max + '">+</button>' +
        '</div>' +
      '</div>';
    }

    return '<div class="modal-handle"></div>' +
      '<div class="modal-header">' +
        '<span class="modal-title">Field Size <span style="color:var(--muted);font-size:13px;font-weight:400">(' + total + ' players)</span></span>' +
        '<button class="modal-close" data-action="close-modal">×</button>' +
      '</div>' +
      '<div class="modal-body">' +
        '<div style="padding:8px 16px 0">' +
          stepper('Forwards',    'forward',  f.forward,  1, 3) +
          stepper('Midfielders', 'midfield', f.midfield, 2, 4) +
          stepper('Defenders',   'defense',  f.defense,  2, 4) +
          '<div class="formation-control" style="border-bottom:none">' +
            '<div class="formation-label">' + posChip('keeper') + ' Goalkeeper</div>' +
            '<div style="font-size:14px;font-weight:700;color:var(--muted)">1</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="modal-footer">' +
        '<button class="btn btn-primary btn-full" data-action="save-formation">Apply to Remaining Quarters</button>' +
        '<p style="font-size:12px;color:var(--muted);text-align:center;margin-top:8px">Past quarters are not affected</p>' +
      '</div>';
  }

  // ─── POST-GAME VIEW ───────────────────────────────────────────────────────

  function renderPostgame() {
    var game = activeGame();
    if (!game) { session.view = 'dashboard'; return renderDashboard(); }

    var present = state.roster.filter(function (p) {
      var s = game.attendance[p.id] || 'expected';
      return s !== 'absent';
    }).sort(function (a, b) { return a.name.localeCompare(b.name); });

    var tableRows = present.map(function (p) {
      var cells = [1, 2, 3, 4].map(function (q) {
        var lu    = SGM.getQuarterLineup(game, q);
        var played = Object.values(lu).indexOf(p.id) !== -1;
        return '<td class="' + (played ? 'pt-played' : '') + '">' + (played ? '\u25cf' : '\u00b7') + '</td>';
      }).join('');
      var total = SGM.getQuartersPlayedThisGame(p.id, game, 4);
      return (
        '<tr>' +
          '<td>' + bandDot(p.band) + ' ' + esc(p.name) + (p.jersey ? ' <span style="color:var(--muted)">#' + esc(p.jersey) + '</span>' : '') + '</td>' +
          cells +
          '<td class="pt-total" style="color:var(--primary)">' + total + '</td>' +
        '</tr>'
      );
    }).join('');

    return (
      '<div class="view postgame-view">' +
        '<div class="view-header"><h1>Game Complete</h1></div>' +
        '<div style="padding:16px;">' +
          '<div class="postgame-score">' +
            '<div class="final-label">vs ' + esc(game.opponent || 'Opponent') + '</div>' +
            '<div class="score-display">' + game.score.home + ' \u2013 ' + game.score.away + '</div>' +
          '</div>' +
          '<div class="scroll-x">' +
            '<table class="pt-table">' +
              '<thead><tr>' +
                '<th style="text-align:left;">Player</th>' +
                '<th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th><th>Tot</th>' +
              '</tr></thead>' +
              '<tbody>' + tableRows + '</tbody>' +
            '</table>' +
          '</div>' +
          '<button class="btn btn-primary btn-full" style="margin-top:20px;" data-action="finish-game">Save &amp; Done</button>' +
        '</div>' +
      '</div>'
    );
  }

  // ─── PLAYER FORM MODAL ───────────────────────────────────────────────────

  function renderPlayerFormModal(data) {
    var isNew  = !data.playerId;
    var player = isNew ? SGM.createPlayer({}) : SGM.getPlayer(state, data.playerId);
    if (!player) return '';

    var posTypes   = ['defense', 'midfield', 'forward'];
    var posLabels  = { defense: 'Defense', midfield: 'Midfield', forward: 'Forward' };

    function checkbox(field, type) {
      var checked = (player[field] || []).indexOf(type) !== -1 ? 'checked' : '';
      return (
        '<label class="checkbox-option">' +
          '<input type="checkbox" data-field="' + field + '" data-val="' + type + '" ' + checked + '>' +
          posChip(type) +
          '<span class="option-label">' + posLabels[type] + '</span>' +
        '</label>'
      );
    }

    var bandRadios = [1, 2, 3].map(function (b) {
      var labels = { 1: 'Top tier', 2: 'Mid tier', 3: 'Developing' };
      return (
        '<label class="radio-option">' +
          '<input type="radio" name="pf-band" value="' + b + '" ' + (player.band === b ? 'checked' : '') + '>' +
          bandBadge(b) +
          '<span class="option-label">Band ' + b + ' \u2014 ' + labels[b] + '</span>' +
        '</label>'
      );
    }).join('');

    var prefChecks = posTypes.map(function (t) { return checkbox('preferredPositions', t); }).join('');
    var secChecks  = posTypes.map(function (t) { return checkbox('secondaryPositions',  t); }).join('');

    return (
      '<div class="modal-handle"></div>' +
      '<div class="modal-header">' +
        '<span class="modal-title">' + (isNew ? 'Add Player' : 'Edit Player') + '</span>' +
        '<button class="modal-close" data-action="close-modal">\u00d7</button>' +
      '</div>' +
      '<div class="modal-body">' +
        '<div class="player-form" id="player-form" data-player-id="' + player.id + '" data-is-new="' + isNew + '">' +
          '<div class="form-group">' +
            '<label class="form-label">Name</label>' +
            '<input class="form-input" id="pf-name" type="text" placeholder="Player name" value="' + esc(player.name) + '">' +
          '</div>' +
          '<div class="form-group">' +
            '<label class="form-label">Jersey #</label>' +
            '<input class="form-input" id="pf-jersey" type="text" inputmode="numeric" placeholder="Optional" value="' + esc(player.jersey) + '">' +
          '</div>' +
          '<div class="form-group">' +
            '<label class="form-label">Band (Strength Tier)</label>' +
            '<div class="radio-group">' + bandRadios + '</div>' +
          '</div>' +
          '<div class="form-group">' +
            '<label class="form-label">Preferred Positions</label>' +
            '<div class="checkbox-group">' + prefChecks + '</div>' +
          '</div>' +
          '<div class="form-group">' +
            '<label class="form-label">Secondary Positions</label>' +
            '<div class="checkbox-group">' + secChecks + '</div>' +
          '</div>' +
          '<label class="checkbox-option" style="border:1px solid var(--border);border-radius:var(--radius);padding:12px 14px;">' +
            '<input type="checkbox" id="pf-keeper" ' + (player.keeperWilling ? 'checked' : '') + '>' +
            posChip('keeper') +
            '<span class="option-label">Willing to play Goalkeeper</span>' +
          '</label>' +
          '<div class="form-group">' +
            '<label class="form-label">Notes</label>' +
            '<textarea class="textarea-input" id="pf-notes" placeholder="Optional notes">' + esc(player.notes) + '</textarea>' +
          '</div>' +
          (!isNew
            ? '<button class="btn btn-danger btn-full" data-action="delete-player" data-player-id="' + player.id + '">Remove Player</button>'
            : '') +
        '</div>' +
      '</div>' +
      '<div class="modal-footer">' +
        '<button class="btn btn-primary btn-full" data-action="save-player">Save Player</button>' +
      '</div>'
    );
  }

  // ─── PLAYER PICKER MODAL ─────────────────────────────────────────────────

  function renderPickerModal(data) {
    var posId     = data.posId;
    var quarterNum = data.quarterNum;
    var game      = activeGame();
    if (!game) return '';

    var posType    = SGM.getPositionType(posId);
    var lineup     = SGM.getQuarterLineup(game, quarterNum);
    var curPid     = lineup[posId];
    var curPlayer  = curPid ? SGM.getPlayer(state, curPid) : null;

    // Current occupant bar
    var curHTML = '';
    if (curPlayer) {
      var cq = SGM.getQuartersPlayedThisGame(curPlayer.id, game, quarterNum - 1);
      curHTML =
        '<div class="picker-current">' +
          bandDot(curPlayer.band) +
          '<div style="flex:1;">' +
            '<div class="picker-current-label">Currently assigned</div>' +
            '<div class="picker-current-name">' +
              esc(curPlayer.name) +
              (curPlayer.jersey ? ' <span style="color:var(--muted)">#' + esc(curPlayer.jersey) + '</span>' : '') +
              ' \u00b7 ' + cq + 'q' +
            '</div>' +
          '</div>' +
          '<button class="btn btn-sm btn-danger" data-action="clear-slot" data-pos-id="' + posId + '" data-quarter="' + quarterNum + '">Remove</button>' +
        '</div>';
    }

    var recs = SGM.recommend(posType, quarterNum, game, state, curPid);

    function playerHistory(pid) {
      var cells = '';
      for (var q = 1; q < game.currentQuarter; q++) {
        var qlu = SGM.getQuarterLineup(game, q);
        var posPlayed = null;
        Object.keys(qlu).forEach(function (k) { if (qlu[k] === pid) posPlayed = k; });
        var lbl = posPlayed ? slotLabel(posPlayed) : '\u2014';
        cells += '<span class="ph-cell"><span class="ph-hdr">Q' + q + '</span>' +
                 '<span class="ph-val' + (posPlayed ? '' : ' ph-val--bench') + '">' + lbl + '</span></span>';
      }
      return cells ? '<span class="picker-history">' + cells + '</span>' : '';
    }

    function pickerSection(items, hdrCls, label) {
      if (!items.length) return '';
      var rows = items.map(function (r) {
        var p  = r.player;
        var qp = r.quartersThisGame;
        return (
          '<div class="picker-row" data-action="assign-player"' +
            ' data-player-id="' + p.id + '"' +
            ' data-pos-id="' + posId + '"' +
            ' data-quarter="' + quarterNum + '">' +
            bandDot(p.band) +
            '<span class="picker-name">' + esc(p.name) + '</span>' +
            (p.jersey ? '<span class="picker-jersey">#' + esc(p.jersey) + '</span>' : '') +
            playerHistory(p.id) +
            '<span class="quarters-badge">' + qp + 'q</span>' +
          '</div>'
        );
      }).join('');
      return '<div class="picker-section-header ' + hdrCls + '">' + label + '</div>' + rows;
    }

    return (
      '<div class="modal-handle"></div>' +
      '<div class="modal-header">' +
        '<span class="modal-title">Assign ' + slotLabel(posId) + ' \u00b7 ' + posTypeLabel(posType) + '</span>' +
        '<button class="modal-close" data-action="close-modal">\u00d7</button>' +
      '</div>' +
      '<div class="modal-body">' +
        curHTML +
        pickerSection(recs.best,      'picker-section-header--best', 'Best Fits') +
        pickerSection(recs.good,      'picker-section-header--good', 'Good Options') +
        pickerSection(recs.lessIdeal, 'picker-section-header--less', 'Less Ideal') +
      '</div>'
    );
  }

  // ─── ROSTER VIEW ─────────────────────────────────────────────────────────

  function renderRoster() {
    var sorted = state.roster.slice().sort(function (a, b) {
      if (a.band !== b.band) return a.band - b.band;
      return a.name.localeCompare(b.name);
    });

    var lastBand = null;
    var rows = sorted.map(function (p) {
      var header = '';
      if (p.band !== lastBand) {
        lastBand = p.band;
        var bColor = ['', 'var(--band1)', 'var(--band2)', 'var(--band3)'][p.band];
        header = '<div class="band-group-header" style="color:' + bColor + '">Band ' + p.band + '</div>';
      }
      var prefChips = (p.preferredPositions || []).map(posChip).join('');
      var keepTag = p.keeperWilling ? posChip('keeper') : '';
      return header +
        '<div class="player-row" data-action="edit-player" data-player-id="' + p.id + '">' +
          bandDot(p.band) +
          '<div class="player-info">' +
            '<div class="player-name-row">' +
              '<span class="player-name">' + esc(p.name) + '</span>' +
              (p.jersey ? '<span class="jersey-num">#' + esc(p.jersey) + '</span>' : '') +
              bandBadge(p.band) +
            '</div>' +
            '<div class="player-positions">' + prefChips + keepTag + '</div>' +
          '</div>' +
          '<span style="color:var(--muted);font-size:22px;line-height:1;">\u203a</span>' +
        '</div>';
    }).join('');

    var empty = sorted.length === 0
      ? '<div class="empty-state"><div class="empty-icon">&#128101;</div><div class="empty-text">No players yet. Tap + to add.</div></div>'
      : '';

    return (
      '<div class="view roster-view">' +
        '<div class="view-header"><h1>Roster</h1></div>' +
        '<div class="player-list">' + rows + empty + '</div>' +
        '<button class="fab" data-action="add-player">+</button>' +
      '</div>'
    );
  }



})();
