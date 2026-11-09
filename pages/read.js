/* pages/read.js — the one simple reading: three Book T cards, then talk. Draw and hand-off
   follow viewers/caster-studio.html (uniform shuffle, no reversals for Book T, the
   `recursive:interpret-reading` postMessage contract in docs/ASSISTANT-EMBED-CONTRACT.md). */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var POSITIONS = [
    { label: 'Structures', meaning: 'Underlying structures, patterns, or beliefs shaping the situation' },
    { label: 'Process', meaning: 'The current process: how things are unfolding or being experienced' },
    { label: 'Possibilities', meaning: 'Possibilities, resources, or perspectives to consider' }
  ];
  var DECK_LABEL = 'Book T (Golden Dawn)';
  var pool = null, drawn = [], lastReading = null, drawCount = 0;

  // Uniform integer in [0, n) from crypto, rejection-sampled (no modulo bias).
  function rnd(n) {
    var lim = Math.floor(0x100000000 / n) * n, b = new Uint32Array(1);
    do { crypto.getRandomValues(b); } while (b[0] >= lim);
    return b[0] % n;
  }
  function drawN(n) {
    var p = pool.slice();
    for (var i = p.length - 1; i > 0; i--) { var j = rnd(i + 1), t = p[i]; p[i] = p[j]; p[j] = t; }
    return p.slice(0, n);
  }
  // Book T images are absolute tarot.recursive.eco URLs; load them from this site's own copy.
  function localSrc(u) { return String(u || '').replace(/^https:\/\/tarot\.recursive\.eco\//, '../'); }
  function plain(md) {
    return String(md || '').replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/\*\*([^*]+)\*\*/g, '$1').replace(/\*([^*]+)\*/g, '$1');
  }
  function bookTParagraphs(n) {
    var s = (n.sections || {})['Book T (1912)'] || '';
    return s.split(/\n\s*\n/).map(function (x) { return x.trim(); })
      .filter(function (x, i) { return x && !(i === 0 && /^\*Book T, 1912/.test(x)); }).map(plain);
  }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

  fetch('../viewers/voices.json').then(function (r) { return r.json(); }).then(function (v) {
    $('creed').textContent = (v.shared_intention && v.shared_intention.creed) || '';
  }).catch(function () {});

  function load() {
    if (pool) return Promise.resolve(pool);
    return fetch('../tarot/book-t/grammar.json').then(function (r) { return r.json(); }).then(function (g) {
      pool = (g.nodes || []).filter(function (n) { return !n.parts && n.metadata && n.metadata.arcana; });
      return pool;
    });
  }

  function countDraw() {
    var n;
    try { n = (parseInt(sessionStorage.getItem('readDraws'), 10) || 0) + 1; sessionStorage.setItem('readDraws', String(n)); }
    catch (e) { n = ++drawCount; }
    $('castCount').textContent = n > 1 ? 'Draw ' + n + ' this session' : '';
  }

  function render() {
    var row = $('row'); row.textContent = '';
    drawn.forEach(function (n, i) {
      var pos = POSITIONS[i], slot = el('div', 'slot');
      slot.appendChild(el('p', 'pos', pos.label));
      slot.appendChild(el('p', 'posmean', pos.meaning));
      var b = el('button', 'card-btn'); b.type = 'button'; b.setAttribute('aria-expanded', 'false');
      b.setAttribute('aria-label', pos.label + ': ' + n.name + '. Show its Book T text');
      var img = new Image(); img.alt = n.name; img.src = localSrc(n.image_url); b.appendChild(img);
      slot.appendChild(b);
      slot.appendChild(el('p', 'cname', n.name));
      var m = n.metadata || {};
      if (m.card_name_1912 && m.card_name_1912 !== n.name) slot.appendChild(el('p', 'cprint', m.card_name_1912));
      var t = el('button', 'tap', 'Tap the card for its Book T text'); t.type = 'button';
      slot.appendChild(t);
      var box = el('div', 'text'); box.hidden = true;
      bookTParagraphs(n).forEach(function (p) { box.appendChild(el('p', null, p)); });
      var a = el('a', null, 'Read it on the 1912 page'); a.href = 'book-t.html#' + n.id; box.appendChild(el('p')).appendChild(a);
      slot.appendChild(box);
      var toggle = function () {
        box.hidden = !box.hidden; b.setAttribute('aria-expanded', String(!box.hidden));
        t.textContent = box.hidden ? 'Tap the card for its Book T text' : 'Hide the text';
      };
      b.addEventListener('click', toggle); t.addEventListener('click', toggle);
      row.appendChild(slot);
    });
  }

  function lay() {
    $('lay').disabled = true;
    load().then(function () {
      drawn = drawN(3);
      var q = $('q').value.trim();
      lastReading = {
        v: 1, spread: 'Structures · Process · Possibilities', question: q || null,
        positions: drawn.map(function (n, i) {
          var m = n.metadata || {};
          return { n: i + 1, label: POSITIONS[i].label, meaning: POSITIONS[i].meaning,
            card: { name: n.name, deck: DECK_LABEL, reversed: false, arcana: m.arcana || null,
              number: m.number == null ? null : m.number, image_url: n.image_url || null } };
        }),
        cast_at: new Date().toISOString(),
        source: 'https://tarot.recursive.eco/pages/read.html'
      };
      countDraw(); render();
      $('reading').hidden = false; $('note').textContent = '';
      $('lay').textContent = 'Lay the cards'; 
      $('reading').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }).catch(function () {
      $('note').textContent = 'The deck would not load. Please try again.'; $('reading').hidden = false;
    }).then(function () { $('lay').disabled = false; });
  }

  function summary(r) {
    return r.spread + ' — ' + r.positions.map(function (p) { return p.label + ': ' + p.card.name; }).join('; ') +
      (r.question ? ' — Question: ' + r.question : '');
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
        : 'The chat is not ready. Open it with the star button and describe your three cards.';
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
      // The frame may still be loading the first time it opens: send, and send once more if unacked.
      function send() { try { ifr.contentWindow.postMessage({ type: 'recursive:interpret-reading', reading: lastReading }, origin); return true; } catch (e) { return false; } }
      send();
      setTimeout(function () { if (!acked) send(); }, 1500);
      setTimeout(function () { window.removeEventListener('message', onAck); if (!acked) fallback(); }, 4000);
    });
  }

  $('lay').addEventListener('click', lay);
  $('again').addEventListener('click', lay);
  $('talk').addEventListener('click', talk);
})();
