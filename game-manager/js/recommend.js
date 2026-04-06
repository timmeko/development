// Soccer Game Manager - Recommendation Engine
// Depends on: js/data.js (window.SGM)

(function() {
  'use strict';

  var SGM = window.SGM;

  // ─── Core Recommendation ─────────────────────────────────────────────────

  /**
   * recommend(positionType, quarterNum, game, state, excludeId)
   * Returns { best: [], good: [], lessIdeal: [] }
   * Each entry: { player, score, category, reasons, quartersThisGame, positionMatch }
   */
  SGM.recommend = function(positionType, quarterNum, game, state, excludeId) {
    var available = SGM.getAvailablePlayers(game, state);

    // Remove players already on field in this quarter (except the one being swapped out)
    var lineup = SGM.getQuarterLineup(game, quarterNum);
    var onField = new Set(Object.values(lineup).filter(Boolean));
    if (excludeId) onField.delete(excludeId);

    var candidates = available.filter(function(p) {
      return !onField.has(p.id);
    });

    var currentFieldIds = Object.values(lineup).filter(function(id) {
      return id && id !== excludeId;
    });

    var results = candidates.map(function(player) {
      return SGM._scorePlayer(player, positionType, quarterNum, game, state, currentFieldIds);
    });

    results.sort(function(a, b) { return a.score - b.score; });

    var best = [], good = [], lessIdeal = [];
    results.forEach(function(r) {
      if (r.category === 'best')       best.push(r);
      else if (r.category === 'less_ideal') lessIdeal.push(r);
      else                             good.push(r);
    });

    return { best: best, good: good, lessIdeal: lessIdeal };
  };

  SGM._scorePlayer = function(player, positionType, quarterNum, game, state, currentFieldIds) {
    var score = 0;
    var reasons = [];

    // quartersThisGame: count Q1..currentQuarter-1 (already-completed quarters)
    var completedUpTo = quarterNum - 1;
    var quartersThisGame = SGM.getQuartersPlayedThisGame(player.id, game, completedUpTo);

    var playedLastQuarter = SGM.getPlayedLastQuarter(player.id, game, quarterNum);
    var fairnessScore = SGM.getFairnessScore(player.id, state.gameHistory);
    var positionMatch = SGM.getPositionMatch(player, positionType);
    var improvesBand = SGM.bandBalanceImproved(player.id, currentFieldIds, state);

    // 1. quartersThisGame < 2 → subtract 1000
    if (quartersThisGame < 2) {
      score -= 1000;
    }

    // 2. sort by quartersThisGame ascending → add 200 per quarter
    score += quartersThisGame * 200;

    // 3. !playedLastQuarter → subtract 500
    if (!playedLastQuarter) {
      score -= 500;
    }

    // 4. fairnessScore ascending → subtract 100 * (1/(fairnessScore+1))
    score -= 100 * (1 / (fairnessScore + 1));

    // 5. positionMatch
    if (positionMatch === 'preferred') {
      score -= 200;
    } else if (positionMatch === 'secondary') {
      score -= 100;
    }

    // 6. band balance
    if (improvesBand) {
      score -= 50;
    }

    // ── Reason labels ──────────────────────────────────────────────────────
    if (quartersThisGame < 2)             reasons.push('Needs minutes');
    if (!playedLastQuarter && quarterNum > 1) reasons.push('Rested last quarter');
    if (positionMatch === 'preferred')    reasons.push('Good position fit');
    if (improvesBand)                     reasons.push('Balances lineup');
    if (quartersThisGame >= 3)            reasons.push('Already played 3 quarters');
    if (playedLastQuarter && quarterNum > 1) reasons.push('Played last quarter');
    if (positionMatch === 'none')         reasons.push('Out of position');

    // ── Category ──────────────────────────────────────────────────────────
    var category;
    if (positionMatch === 'preferred' && (quartersThisGame < 2 || !playedLastQuarter)) {
      category = 'best';
    } else if (positionMatch === 'none' || quartersThisGame >= 3) {
      category = 'less_ideal';
    } else {
      category = 'good';
    }

    return {
      player:           player,
      score:            score,
      category:         category,
      reasons:          reasons,
      quartersThisGame: quartersThisGame,
      positionMatch:    positionMatch
    };
  };

  // ─── Prefill Quarter ──────────────────────────────────────────────────────

  /**
   * prefillQuarter(game, state, quarterNum) → lineup object { positionId: playerId|null }
   */
  SGM.prefillQuarter = function(game, state, quarterNum) {
    var positions = SGM.getPositionsForGame(game);
    var lineup = {};
    positions.forEach(function(p) { lineup[p] = null; });

    if (quarterNum <= 1) {
      // Q1: no prior quarter info, sort by band balance then fairness
      var available0 = SGM.getAvailablePlayers(game, state);
      var sorted0 = available0.slice().sort(function(a, b) {
        return SGM.getFairnessScore(a.id, state.gameHistory) - SGM.getFairnessScore(b.id, state.gameHistory);
      });
      var selected0 = sorted0.slice(0, positions.length);
      var filled0 = new Set();
      // preferred pass
      positions.forEach(function(posId) {
        var posType = SGM.getPositionType(posId);
        for (var i = 0; i < selected0.length; i++) {
          if (filled0.has(selected0[i].id)) continue;
          if (SGM.getPositionMatch(selected0[i], posType) === 'preferred') {
            lineup[posId] = selected0[i].id; filled0.add(selected0[i].id); break;
          }
        }
      });
      // secondary pass
      positions.forEach(function(posId) {
        if (lineup[posId]) return;
        var posType = SGM.getPositionType(posId);
        for (var i = 0; i < selected0.length; i++) {
          if (filled0.has(selected0[i].id)) continue;
          if (SGM.getPositionMatch(selected0[i], posType) !== 'none') {
            lineup[posId] = selected0[i].id; filled0.add(selected0[i].id); break;
          }
        }
      });
      // fill remainder
      positions.forEach(function(posId) {
        if (lineup[posId]) return;
        for (var i = 0; i < selected0.length; i++) {
          if (!filled0.has(selected0[i].id)) {
            lineup[posId] = selected0[i].id; filled0.add(selected0[i].id); break;
          }
        }
      });
      return lineup;
    }

    var available = SGM.getAvailablePlayers(game, state);

    // Sort: didn't play last quarter first, then fairness score ascending
    var sorted = available.slice().sort(function(a, b) {
      var aLast = SGM.getPlayedLastQuarter(a.id, game, quarterNum) ? 1 : 0;
      var bLast = SGM.getPlayedLastQuarter(b.id, game, quarterNum) ? 1 : 0;
      if (aLast !== bLast) return aLast - bLast;
      var aF = SGM.getFairnessScore(a.id, state.gameHistory);
      var bF = SGM.getFairnessScore(b.id, state.gameHistory);
      return aF - bF;
    });

    // Take top N
    var selectedPlayers = sorted.slice(0, positions.length);
    var unassigned = selectedPlayers.slice();

    // Assign positions: preferred first, then secondary, then any
    var filled = new Set();

    // Pass 1: preferred
    positions.forEach(function(posId) {
      var posType = SGM.getPositionType(posId);
      for (var i = 0; i < unassigned.length; i++) {
        if (filled.has(unassigned[i].id)) continue;
        if (SGM.getPositionMatch(unassigned[i], posType) === 'preferred') {
          lineup[posId] = unassigned[i].id;
          filled.add(unassigned[i].id);
          break;
        }
      }
    });

    // Pass 2: secondary
    positions.forEach(function(posId) {
      if (lineup[posId]) return;
      var posType = SGM.getPositionType(posId);
      for (var i = 0; i < unassigned.length; i++) {
        if (filled.has(unassigned[i].id)) continue;
        var match = SGM.getPositionMatch(unassigned[i], posType);
        if (match === 'secondary') {
          lineup[posId] = unassigned[i].id;
          filled.add(unassigned[i].id);
          break;
        }
      }
    });

    // Pass 3: any remaining
    positions.forEach(function(posId) {
      if (lineup[posId]) return;
      for (var i = 0; i < unassigned.length; i++) {
        if (filled.has(unassigned[i].id)) continue;
        lineup[posId] = unassigned[i].id;
        filled.add(unassigned[i].id);
        break;
      }
    });

    return lineup;
  };

  // ─── Bench Sorting ────────────────────────────────────────────────────────

  /**
   * sortBench(players, game, state) → sorted array
   */
  SGM.sortBench = function(players, game, state) {
    var quarterNum = game.currentQuarter;
    return players.slice().sort(function(a, b) {
      var aQ = SGM.getQuartersPlayedThisGame(a.id, game, quarterNum - 1);
      var bQ = SGM.getQuartersPlayedThisGame(b.id, game, quarterNum - 1);

      // 1. quartersThisGame < 2 first
      var aNeedsMin = aQ < 2 ? 0 : 1;
      var bNeedsMin = bQ < 2 ? 0 : 1;
      if (aNeedsMin !== bNeedsMin) return aNeedsMin - bNeedsMin;

      // 2. lowest quartersThisGame
      if (aQ !== bQ) return aQ - bQ;

      // 3. !playedLastQuarter first
      var aLast = SGM.getPlayedLastQuarter(a.id, game, quarterNum) ? 1 : 0;
      var bLast = SGM.getPlayedLastQuarter(b.id, game, quarterNum) ? 1 : 0;
      if (aLast !== bLast) return aLast - bLast;

      // 4. lowest fairnessScore
      var aF = SGM.getFairnessScore(a.id, state.gameHistory);
      var bF = SGM.getFairnessScore(b.id, state.gameHistory);
      return aF - bF;
    });
  };

  // ─── Warnings ─────────────────────────────────────────────────────────────

  /**
   * computeWarnings(game, state, quarterNum) → array of warning objects
   */
  SGM.computeWarnings = function(game, state, quarterNum) {
    var warnings = [];
    var lineup = SGM.getQuarterLineup(game, quarterNum);
    var positions = SGM.getPositionsForGame(game);
    var fieldIds = Object.values(lineup).filter(Boolean);

    // missingKeeper
    if (!lineup['keeper']) {
      warnings.push({ type: 'missingKeeper', message: 'No keeper assigned' });
    }

    // duplicatePlayer
    var seen = {};
    var hasDupe = false;
    fieldIds.forEach(function(id) {
      if (seen[id]) hasDupe = true;
      seen[id] = true;
    });
    if (hasDupe) {
      warnings.push({ type: 'duplicatePlayer', message: 'Same player assigned multiple times' });
    }

    // invalidCount
    var filledCount = fieldIds.length;
    var posCount = positions.length;
    if (filledCount > 0 && filledCount < posCount) {
      warnings.push({ type: 'invalidCount', message: filledCount + ' of ' + posCount + ' positions filled' });
    }

    // bandImbalance
    if (fieldIds.length > 0) {
      var bandCounts = SGM.computeBandBalance(fieldIds, state);
      var allBand1 = bandCounts[1] === fieldIds.length;
      var allBand3 = bandCounts[3] === fieldIds.length;
      var noBand1WithMany = bandCounts[1] === 0 && fieldIds.length > 5;
      if (allBand1 || allBand3 || noBand1WithMany) {
        warnings.push({ type: 'bandImbalance', message: 'Band distribution is unbalanced' });
      }
    }

    // consecutiveQuarters: warn if any player in this lineup played more than 2 consecutive previous quarters
    if (quarterNum > 3) {
      var overplayed = fieldIds.filter(function(pid) {
        var streak = 0;
        for (var q = quarterNum - 1; q >= 1; q--) {
          var qLineup = SGM.getQuarterLineup(game, q);
          var qIds = Object.values(qLineup).filter(Boolean);
          if (qIds.indexOf(pid) !== -1) {
            streak++;
          } else {
            break;
          }
        }
        return streak > 2;
      });
      if (overplayed.length > 0) {
        var names = overplayed.map(function(pid) {
          var p = SGM.getPlayer(state, pid);
          return p ? p.name : pid;
        }).join(', ');
        warnings.push({
          type: 'consecutiveQuarters',
          message: 'Played every quarter so far: ' + names
        });
      }
    }

    return warnings;
  };

  // ─── Playing Time Feasibility ─────────────────────────────────────────────

  SGM.computeFeasibility = function(game, state) {
    var present = SGM.getAvailablePlayers(game, state);
    var presentCount = present.length;
    var positions = SGM.getPositionsForGame(game);
    var posCount = positions.length;
    var slotsTotal = posCount * 4;
    var minTarget = presentCount * 2;

    if (minTarget <= slotsTotal) return 'on_track';
    if (minTarget <= slotsTotal * 1.2) return 'at_risk';
    return 'not_feasible';
  };

})();
