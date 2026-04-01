// Soccer Game Manager - Data Layer
// window.SGM namespace

(function() {
  'use strict';

  window.SGM = window.SGM || {};

  // ─── Constants ────────────────────────────────────────────────────────────

  SGM.POSITIONS_BY_TYPE = {
    keeper:   ['keeper'],
    defense:  ['def-1','def-2','def-3'],
    midfield: ['mid-1','mid-2','mid-3'],
    forward:  ['fwd-1','fwd-2']
  };

  SGM.POSITION_TYPE = {
    'keeper': 'keeper',
    'def-1':  'defense', 'def-2': 'defense', 'def-3': 'defense',
    'mid-1':  'midfield','mid-2': 'midfield','mid-3': 'midfield',
    'fwd-1':  'forward', 'fwd-2': 'forward'
  };

  SGM.POSITION_LABELS = {
    'keeper': 'Keeper',
    'def-1': 'Def', 'def-2': 'Def', 'def-3': 'Def',
    'mid-1': 'Mid', 'mid-2': 'Mid', 'mid-3': 'Mid',
    'fwd-1': 'Fwd', 'fwd-2': 'Fwd'
  };

  SGM.ALL_POSITIONS = ['keeper','def-1','def-2','def-3','mid-1','mid-2','mid-3','fwd-1','fwd-2'];

  SGM.STATUS_COLORS = {
    present:    'var(--primary)',
    absent:     'var(--red)',
    late:       'var(--amber)',
    expected:   'var(--muted)',
    left_early: 'var(--orange)'
  };

  SGM.STATUS_LABELS = {
    present:    'Present',
    absent:     'Absent',
    late:       'Late',
    expected:   'Expected',
    left_early: 'Left Early'
  };

  SGM.STATUS_CYCLE = ['expected','present','absent','late','left_early'];

  SGM.DEFAULT_FORMATION = { defense: 3, midfield: 3, forward: 2 };

  // ─── Utility ──────────────────────────────────────────────────────────────

  SGM.uid = function() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2,7);
  };

  SGM.getPositionsForFormation = function(formation) {
    var positions = ['keeper'];
    for (var i = 1; i <= (formation.defense  || 3); i++) positions.push('def-' + i);
    for (var i = 1; i <= (formation.midfield || 3); i++) positions.push('mid-' + i);
    for (var i = 1; i <= (formation.forward  || 2); i++) positions.push('fwd-' + i);
    return positions;
  };

  SGM.getPositionType = function(posId) {
    if (posId === 'keeper') return 'keeper';
    var prefix = posId.split('-')[0];
    var map = { def: 'defense', mid: 'midfield', fwd: 'forward' };
    return map[prefix] || 'unknown';
  };

  // ─── Factories ────────────────────────────────────────────────────────────

  SGM.createPlayer = function(data) {
    return {
      id:                 data.id || SGM.uid(),
      name:               data.name || '',
      jersey:             data.jersey || '',
      band:               data.band || 2,
      preferredPositions: data.preferredPositions || [],
      secondaryPositions: data.secondaryPositions || [],
      keeperWilling:      data.keeperWilling || false,
      notes:              data.notes || ''
    };
  };

  SGM.createGame = function(data) {
    var formation = data.formation || Object.assign({}, SGM.DEFAULT_FORMATION);
    var positions = SGM.getPositionsForFormation(formation);
    var emptyLineup = {};
    positions.forEach(function(p) { emptyLineup[p] = null; });

    return {
      id:              data.id || SGM.uid(),
      createdAt:       data.createdAt || new Date().toISOString(),
      opponent:        data.opponent || '',
      formation:       formation,
      score:           data.score || { home: 0, away: 0 },
      status:          data.status || 'setup',
      currentQuarter:  data.currentQuarter || 1,
      attendance:      data.attendance || {},
      quarters: {
        1: { lineup: Object.assign({}, emptyLineup) },
        2: { lineup: Object.assign({}, emptyLineup) },
        3: { lineup: Object.assign({}, emptyLineup) },
        4: { lineup: Object.assign({}, emptyLineup) }
      }
    };
  };

  // ─── Storage ──────────────────────────────────────────────────────────────

  SGM.STORAGE_KEY = 'sgm_state';

  SGM.saveState = function(state) {
    try {
      var toSave = {
        roster:        state.roster,
        games:         state.games,
        gameHistory:   state.gameHistory,
        activeGameId:  state.activeGameId
      };
      localStorage.setItem(SGM.STORAGE_KEY, JSON.stringify(toSave));
    } catch(e) {
      console.warn('SGM: save failed', e);
    }
  };

  SGM.loadState = function() {
    try {
      var raw = localStorage.getItem(SGM.STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch(e) {
      console.warn('SGM: load failed', e);
    }
    return null;
  };

  SGM.clearState = function() {
    localStorage.removeItem(SGM.STORAGE_KEY);
  };

  // ─── Query Helpers ────────────────────────────────────────────────────────

  SGM.getPlayer = function(state, id) {
    return state.roster.find(function(p) { return p.id === id; }) || null;
  };

  SGM.getGame = function(state, id) {
    return state.games.find(function(g) { return g.id === id; }) || null;
  };

  SGM.getActiveGame = function(state) {
    return state.activeGameId ? SGM.getGame(state, state.activeGameId) : null;
  };

  SGM.getAvailablePlayers = function(game, state) {
    return state.roster.filter(function(p) {
      var status = game.attendance[p.id] || 'expected';
      return status === 'present' || status === 'late';
    });
  };

  SGM.getPositionsForGame = function(game) {
    return SGM.getPositionsForFormation(game.formation);
  };

  SGM.getQuarterLineup = function(game, quarterNum) {
    var q = game.quarters[quarterNum];
    return q ? q.lineup : {};
  };

  SGM.getPlayersOnField = function(game, quarterNum) {
    var lineup = SGM.getQuarterLineup(game, quarterNum);
    var ids = [];
    Object.values(lineup).forEach(function(id) {
      if (id) ids.push(id);
    });
    return ids;
  };

  SGM.getQuartersPlayedThisGame = function(playerId, game, upToQuarter) {
    var count = 0;
    var max = upToQuarter != null ? upToQuarter : game.currentQuarter;
    for (var q = 1; q <= max; q++) {
      var lineup = SGM.getQuarterLineup(game, q);
      if (Object.values(lineup).indexOf(playerId) !== -1) count++;
    }
    return count;
  };

  SGM.getFairnessScore = function(playerId, gameHistory) {
    var history = gameHistory.filter(function(h) { return h.playerId === playerId && h.attended; });
    if (history.length === 0) return 0;
    var totalQ = history.reduce(function(s, h) { return s + h.quartersPlayed; }, 0);
    return totalQ / history.length;
  };

  SGM.getPlayedLastQuarter = function(playerId, game, currentQuarter) {
    if (currentQuarter <= 1) return false;
    var prevLineup = SGM.getQuarterLineup(game, currentQuarter - 1);
    return Object.values(prevLineup).indexOf(playerId) !== -1;
  };

  SGM.getBenchPlayers = function(game, state, quarterNum) {
    var lineup = SGM.getQuarterLineup(game, quarterNum);
    var onField = new Set(Object.values(lineup).filter(Boolean));
    return SGM.getAvailablePlayers(game, state).filter(function(p) {
      return !onField.has(p.id);
    });
  };

  SGM.getPositionMatch = function(player, positionType) {
    if (player.preferredPositions && player.preferredPositions.indexOf(positionType) !== -1) return 'preferred';
    if (player.secondaryPositions && player.secondaryPositions.indexOf(positionType) !== -1) return 'secondary';
    if (positionType === 'keeper' && player.keeperWilling) return 'secondary';
    return 'none';
  };

  // ─── Band Balance ─────────────────────────────────────────────────────────

  SGM.computeBandBalance = function(playerIds, state) {
    var counts = {1: 0, 2: 0, 3: 0};
    playerIds.forEach(function(id) {
      var p = SGM.getPlayer(state, id);
      if (p) counts[p.band] = (counts[p.band] || 0) + 1;
    });
    return counts;
  };

  SGM.bandBalanceImproved = function(playerId, currentIds, state) {
    var player = SGM.getPlayer(state, playerId);
    if (!player) return false;
    var counts = SGM.computeBandBalance(currentIds, state);
    // Improve means adding this player reduces the skew
    var total = currentIds.length;
    if (total === 0) return true;
    var bandOnField = counts[player.band] || 0;
    // If band is underrepresented → improves balance
    var avgCount = total / 3;
    return bandOnField < avgCount;
  };

  // ─── Seed Data ────────────────────────────────────────────────────────────

  SGM.SEED_ROSTER = [
    // Band 1
    { id: 'p1',  name: 'Alex',   jersey: '7',  band: 1, preferredPositions: ['forward'],  secondaryPositions: ['midfield'],  keeperWilling: false },
    { id: 'p2',  name: 'Jordan', jersey: '10', band: 1, preferredPositions: ['forward'],  secondaryPositions: [],           keeperWilling: false },
    { id: 'p3',  name: 'Sam',    jersey: '3',  band: 1, preferredPositions: ['defense'],  secondaryPositions: ['midfield'],  keeperWilling: false },
    { id: 'p4',  name: 'Casey',  jersey: '1',  band: 1, preferredPositions: ['keeper','defense'], secondaryPositions: [], keeperWilling: true },
    // Band 2
    { id: 'p5',  name: 'Riley',  jersey: '11', band: 2, preferredPositions: ['forward'],  secondaryPositions: ['midfield'],  keeperWilling: false },
    { id: 'p6',  name: 'Morgan', jersey: '5',  band: 2, preferredPositions: ['midfield'], secondaryPositions: ['defense'],   keeperWilling: false },
    { id: 'p7',  name: 'Drew',   jersey: '4',  band: 2, preferredPositions: ['defense'],  secondaryPositions: [],           keeperWilling: false },
    { id: 'p8',  name: 'Quinn',  jersey: '8',  band: 2, preferredPositions: ['midfield'], secondaryPositions: [],           keeperWilling: false },
    // Band 3
    { id: 'p9',  name: 'Parker', jersey: '9',  band: 3, preferredPositions: ['forward'],  secondaryPositions: [],           keeperWilling: false },
    { id: 'p10', name: 'Avery',  jersey: '6',  band: 3, preferredPositions: ['defense'],  secondaryPositions: ['midfield'],  keeperWilling: false },
    { id: 'p11', name: 'Blake',  jersey: '2',  band: 3, preferredPositions: ['defense'],  secondaryPositions: [],           keeperWilling: true  },
    { id: 'p12', name: 'Taylor', jersey: '12', band: 3, preferredPositions: ['midfield'], secondaryPositions: ['forward'],   keeperWilling: false }
  ];

  SGM.buildInitialState = function() {
    var saved = SGM.loadState();
    if (saved && saved.roster && saved.roster.length > 0) {
      // Merge saved state – ensure games have proper structure
      return {
        roster:       saved.roster       || [],
        games:        saved.games        || [],
        gameHistory:  saved.gameHistory  || [],
        activeGameId: saved.activeGameId || null
      };
    }
    return {
      roster:       SGM.SEED_ROSTER.map(function(d) { return SGM.createPlayer(d); }),
      games:        [],
      gameHistory:  [],
      activeGameId: null
    };
  };

})();
