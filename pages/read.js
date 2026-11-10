/* pages/read.js — the simple reading: pick a spread and a deck (small chips), cast, talk.
   Data sources are the Spread Caster's own: viewers/spreads.json for spreads, the meta grammar's
   _decks and cards (tarot/all-decks-many-lenses) for decks, Book T read from tarot/book-t.
   Draw and hand-off follow viewers/caster-studio.html (uniform shuffle, no reversals for Book T,
   the `recursive:interpret-reading` postMessage contract in docs/ASSISTANT-EMBED-CONTRACT.md).
   The three buttons and the picture popup are viewers/reading-actions.js; the card detail is
   viewers/card-detail.js. The choice lives in the URL: ?spread=<id>&deck=<slug>. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var BOOK_T = 'book-t', OLD_GD = 'golden-dawn-book-t-tarot', BOOK_T_LABEL = 'Book T (Golden Dawn)';
  var META_URL = '../tarot/all-decks-many-lenses/grammar.json';
  var WORDS = { 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten' };
  var q = new URLSearchParams(location.search);
  var spreads = [], spread = null, deckSlug = q.get('deck') || BOOK_T;
  var meta = null, metaP = null, ecoIds = {}, decks = null;      // decks: [{slug,label,date,n}] offered
  var pools = {}, drawn = [], lastReading = null, drawCount = 0;

  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function rnd(n) {            // uniform integer in [0, n), rejection-sampled (no modulo bias)
    var lim = Math.floor(0x100000000 / n) * n, b = new Uint32Array(1);
    do { crypto.getRandomValues(b); } while (b[0] >= lim);
    return b[0] % n;
  }
  function drawN(pool, n) {
    var p = pool.slice();
    for (var i = p.length - 1; i > 0; i--) { var j = rnd(i + 1), t = p[i]; p[i] = p[j]; p[j] = t; }
    return p.slice(0, n);
  }
  // Images that are absolute tarot.recursive.eco URLs load from this site's own copy.
  function localSrc(u) { return String(u || '').replace(/^https:\/\/tarot\.recursive\.eco\//, '../'); }
  function labelOf(slug) {
    if (slug === BOOK_T) return BOOK_T_LABEL;
    var d = (decks || []).filter(function (x) { return x.slug === slug; })[0];
    if (d) return d.label;
    var m = meta && (meta._decks || []).filter(function (x) { return x.slug === slug; })[0];
    return m ? m.label : slug;
  }

  function loadMeta() {
    if (!metaP) metaP = fetch(META_URL).then(function (r) { return r.json(); }).then(function (m) { return (meta = m); });
    return metaP;
  }
  // The pool of cards (with pictures) for a deck.
  function loadPool(slug) {
    if (pools[slug]) return Promise.resolve(pools[slug]);
    if (slug === BOOK_T) {
      return fetch('../tarot/book-t/grammar.json').then(function (r) { return r.json(); }).then(function (g) {
        return (pools[slug] = (g.nodes || []).filter(function (n) { return !n.parts && n.metadata && n.metadata.arcana && n.image_url; }).map(function (n) {
          var m = n.metadata;
          return { deckSlug: BOOK_T, nodeId: n.id, name: n.name, printed: m.card_name_1912 && m.card_name_1912 !== n.name ? m.card_name_1912 : '',
            image: n.image_url, arcana: m.arcana, number: m.number == null ? null : m.number };
        }));
      });
    }
    return loadMeta().then(function (m) {
      var label = labelOf(slug), re = new RegExp('\\s*[\u2014\u2013-]\\s*' + label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*$');
      return (pools[slug] = (m.nodes || []).filter(function (n) {
        var md = n.metadata || {};
        return !n.parts && md.source_deck === slug && md.arcana && n.image_url;
      }).map(function (n) {
        var md = n.metadata;
        return { deckSlug: slug, nodeId: md.source_node_id, name: String(n.name).replace(re, '').replace(/^\d+\s*[\u2014\u2013-]\s*/, ''),
          printed: '', image: n.image_url, arcana: md.arcana, number: md.number == null ? null : md.number };
      }));
    });
  }
  // The decks offered: the Caster's list (meta _decks, Book T in the Golden Dawn's place), only
  // those with pictures for at least the spread's positions and a recursive.eco id.
  function buildDecks() {
    if (decks) return Promise.resolve(decks);
    return loadMeta().then(function (m) {
      var count = {};
      (m.nodes || []).forEach(function (n) {
        var md = n.metadata || {};
        if (!n.parts && md.source_deck && md.arcana && n.image_url) count[md.source_deck] = (count[md.source_deck] || 0) + 1;
      });
      var yr = function (d) { var x = String(d.date || d.era || '').match(/\d{4}/); return x ? +x[0] : 9999; };
      decks = (m._decks || []).slice()
        .sort(function (a, b) { return (a.era_sort == null ? 99 : a.era_sort) - (b.era_sort == null ? 99 : b.era_sort) || yr(a) - yr(b) || String(a.label || '').localeCompare(b.label || ''); })
        .map(function (d) { return d.slug === OLD_GD ? { slug: BOOK_T, label: BOOK_T_LABEL, date: d.date, n: 78 } : { slug: d.slug, label: d.label, date: d.date || d.era || '', n: count[d.slug] || 0 }; })
        .filter(function (d) { return d.n >= 10 && ecoIds[d.slug]; });
      return decks;
    });
  }

  // ── the two chips ──
  function syncUrl() {
    var u = new URL(location.href);
    u.searchParams.set('spread', spread.id); u.searchParams.set('deck', deckSlug); u.searchParams.delete('have');
    try { history.replaceState(null, '', u.pathname + u.search); } catch (e) {}
  }
  function chips() {
    $('chipSpread').textContent = spread.name; $('chipDeck').textContent = labelOf(deckSlug);
    var n = spread.positions.length;
    $('h1').textContent = 'Cast ' + (WORDS[n] || n) + ' card' + (n === 1 ? '' : 's');
    syncUrl();
  }
  function pickList(title, items, current, onPick) {
    var d = SiteDialog.open({ title: title }), list = el('div', 'pick');
    items.forEach(function (it) {
      var b = el('button', 'pick-item' + (it.id === current ? ' on' : '')); b.type = 'button';
      b.appendChild(el('span', 'pick-name', it.name)); if (it.sub) b.appendChild(el('span', 'pick-sub', it.sub));
      b.addEventListener('click', function () { d.close(); onPick(it.id); });
      list.appendChild(b);
    });
    d.body.appendChild(list);
    return d;
  }
  function reset() { drawn = []; lastReading = null; $('reading').hidden = true; $('castCount').textContent = ''; }
  function chooseSpread() {
    pickList('Choose a spread', spreads.map(function (s) { return { id: s.id, name: s.name, sub: s.positions.length + (s.positions.length === 1 ? ' card' : ' cards') + (s.description ? ' \u00b7 ' + s.description : '') }; }),
      spread.id, function (id) {
        spread = spreads.filter(function (s) { return s.id === id; })[0];
        var need = spread.positions.length;
        // Keep the deck if it still has enough pictured cards; else fall back to Book T.
        var ok = function () { chips(); reset(); };
        if (deckSlug === BOOK_T) return ok();
        buildDecks().then(function (ds) {
          var d = ds.filter(function (x) { return x.slug === deckSlug; })[0];
          if (!d || d.n < need) deckSlug = BOOK_T;
          ok();
        });
      });
  }
  function chooseDeck() {
    var need = spread.positions.length;
    var d = SiteDialog.open({ title: 'Choose a deck' });
    d.body.appendChild(el('p', 'ra-small', 'Loading the decks\u2026'));
    buildDecks().then(function (ds) {
      d.body.textContent = '';
      var list = el('div', 'pick');
      ds.filter(function (x) { return x.n >= need; }).forEach(function (x) {
        var b = el('button', 'pick-item' + (x.slug === deckSlug ? ' on' : '')); b.type = 'button';
        b.appendChild(el('span', 'pick-name', x.label)); b.appendChild(el('span', 'pick-sub', (x.date ? x.date + ' \u00b7 ' : '') + x.n + ' cards'));
        b.addEventListener('click', function () { d.close(); deckSlug = x.slug; chips(); reset(); });
        list.appendChild(b);
      });
      d.body.appendChild(list);
    }).catch(function () { d.body.textContent = 'The deck list would not load. Please try again.'; });
  }

  // ── the cards ──
  function countDraw() {
    var n;
    try { n = (parseInt(sessionStorage.getItem('readDraws'), 10) || 0) + 1; sessionStorage.setItem('readDraws', String(n)); }
    catch (e) { n = ++drawCount; }
    $('castCount').textContent = n > 1 ? 'Draw ' + n + ' this session' : '';
  }
  function render() {
    var row = $('row'); row.textContent = '';
    var n = drawn.length; row.className = 'row c' + Math.min(n, 4) + (n > 3 ? ' many' : '');
    drawn.forEach(function (c, i) {
      var pos = spread.positions[i], slot = el('div', 'slot');
      slot.appendChild(el('p', 'pos', pos.label));
      if (pos.meaning) slot.appendChild(el('p', 'posmean', pos.meaning));
      var b = el('button', 'card-btn'); b.type = 'button';
      b.setAttribute('aria-label', pos.label + ': ' + c.name + '. Open the card');
      var img = new Image(); img.alt = c.name; img.src = localSrc(c.image); b.appendChild(img);
      slot.appendChild(b);
      slot.appendChild(el('p', 'cname', c.name));
      if (c.printed) slot.appendChild(el('p', 'cprint', c.printed));
      var t = el('button', 'tap', 'Tap the card for its text'); t.type = 'button';
      slot.appendChild(t);
      var open = function () { CardDetail.open({ deckSlug: c.deckSlug, nodeId: c.nodeId, name: c.name, image: c.image, deckLabel: labelOf(c.deckSlug), position: pos.label }); };
      b.addEventListener('click', open); t.addEventListener('click', open);
      row.appendChild(slot);
    });
  }
  function cast() {
    var btn = $('cast'); btn.disabled = true;
    loadPool(deckSlug).then(function (pool) {
      var need = spread.positions.length;
      if (pool.length < need) throw new Error('few');
      drawn = drawN(pool, need);
      var qn = $('q').value.trim(), dl = labelOf(deckSlug);
      lastReading = {
        v: 1, spread: spread.name, question: qn || null,
        positions: drawn.map(function (c, i) {
          var p = spread.positions[i];
          return { n: i + 1, label: p.label, meaning: p.meaning || '',
            card: { name: c.name, deck: dl, reversed: false, arcana: c.arcana || null, number: c.number, image_url: c.image || null } };
        }),
        cast_at: new Date().toISOString(),
        source: 'https://tarot.recursive.eco/pages/read.html'
      };
      countDraw(); render();
      $('reading').hidden = false; $('note').textContent = '';
      $('reading').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }).catch(function () {
      $('note').textContent = 'The deck would not load. Please try again, or choose another deck.'; $('reading').hidden = false;
    }).then(function () { btn.disabled = false; });
  }

  // ── talk about it (unchanged hand-off) ──
  function summary(r) {
    return r.spread + ' \u2014 ' + r.positions.map(function (p) { return p.label + ': ' + p.card.name; }).join('; ') +
      (r.question ? ' \u2014 Question: ' + r.question : '');
  }
  function iframe() { return document.querySelector('.rec-assistant-shell iframe'); }
  function whenReady(cb, tries) {
    var f = iframe();
    if (f) return cb(f);
    if ((tries || 0) > 40) return cb(null);
    setTimeout(function () { whenReady(cb, (tries || 0) + 1); }, 250);
  }
  function fallback() {
    var s = summary(lastReading), say = function (c) {
      $('note').textContent = c ? 'The chat is not ready. Your reading is copied: paste it into the chat to talk about it.'
        : 'The chat is not ready. Open it with the star button and describe your cards.';
    };
    try { navigator.clipboard.writeText(s).then(function () { say(true); }, function () { say(false); }); } catch (e) { say(false); }
  }
  function talk() {
    if (!lastReading) return;
    whenReady(function (ifr) {
      var RA = window.RecursiveAssistant;
      if (!ifr || !RA || typeof RA.open !== 'function') return fallback();
      RA.open();
      var origin;
      try { origin = new URL(ifr.src).origin; } catch (e) { origin = RA.flowBaseUrl && RA.flowBaseUrl(); }
      var acked = false;
      function onAck(e) { if (e.origin === origin && e.data && e.data.type === 'recursive:interpret-ack') { acked = true; window.removeEventListener('message', onAck); } }
      window.addEventListener('message', onAck);
      function send() { try { ifr.contentWindow.postMessage({ type: 'recursive:interpret-reading', reading: lastReading }, origin); return true; } catch (e) { return false; } }
      send();
      setTimeout(function () { if (!acked) send(); }, 1500);
      setTimeout(function () { window.removeEventListener('message', onAck); if (!acked) fallback(); }, 4000);
    });
  }

  function state() {
    return { deckSlug: deckSlug, deckName: labelOf(deckSlug), spreadId: spread.id, spreadName: spread.name,
      positions: spread.positions.map(function (p) { return p.label; }) };
  }

  function init() {
    fetch('../viewers/voices.json').then(function (r) { return r.json(); }).then(function (v) {
      $('creed').textContent = (v.shared_intention && v.shared_intention.creed) || '';
    }).catch(function () {});
    Promise.all([
      fetch('../viewers/spreads.json').then(function (r) { return r.json(); }),
      fetch('../tarot/_eco_ids.json').then(function (r) { return r.json(); }).catch(function () { return { ids: {} }; })
    ]).then(function (r) {
      spreads = r[0].spreads || []; ecoIds = r[1].ids || {};
      spread = spreads.filter(function (s) { return s.id === q.get('spread'); })[0] || spreads.filter(function (s) { return s.id === 'spp'; })[0] || spreads[0];
      if (deckSlug === OLD_GD) deckSlug = BOOK_T;
      // A deck from a link is checked once the list is known; Book T needs no list.
      var settle = deckSlug === BOOK_T ? Promise.resolve() : buildDecks().then(function (ds) {
        var d = ds.filter(function (x) { return x.slug === deckSlug; })[0];
        if (!d || d.n < spread.positions.length) deckSlug = BOOK_T;
      }).catch(function () { deckSlug = BOOK_T; });
      return settle;
    }).then(function () {
      chips();
      ReadingActions.renderActions($('actions2'), state);
      if (q.get('have') === 'deck') {
        ReadingActions.openPicturePopup({ mode: 'owner', deckName: labelOf(deckSlug), spreadName: spread.name, positions: spread.positions.map(function (p) { return p.label; }), deckSlug: deckSlug });
      }
    }).catch(function () { $('note').textContent = 'The page could not load its spreads. Please reload.'; $('reading').hidden = false; });
  }

  $('chipSpread').addEventListener('click', function () { if (spread) chooseSpread(); });
  $('chipDeck').addEventListener('click', function () { if (spread) chooseDeck(); });
  $('cast').addEventListener('click', function () { if (spread) cast(); });
  $('again').addEventListener('click', function () { if (spread) cast(); });
  $('talk').addEventListener('click', talk);
  init();
})();
