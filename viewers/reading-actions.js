/* viewers/reading-actions.js — the three buttons under a reading, and the picture popup.
 *   ReadingActions.renderActions(container, getState)
 *     getState() -> { deckSlug, deckName, spreadId, spreadName, positions: [label, ...] }
 *   ReadingActions.openPicturePopup({ mode: 'cast' | 'owner', deckName, spreadName, positions, deckSlug })
 * One popup, two wordings: 'cast' for someone casting on screen, 'owner' for someone who holds the
 * printed deck (the QR code in the Book T booklet lands there). Needs viewers/dialog.js and the
 * recursive.eco assistant launcher (assistant.js). Colours: theme.css tokens only. */
(function (global) {
  'use strict';
  var ROOT = (function () {
    var s = document.currentScript && document.currentScript.src;
    try { return new URL('../', s).href; } catch (e) { return new URL('./', location.href).href; }
  })();
  // The app's own spread keys; any other spread is left out and the app uses its default.
  var APP_SPREAD = { spp: 'builtin:cbt-3', ppf: 'builtin:ppf-3', 'celtic-cross': 'builtin:celtic-cross-10' };
  var ecoIds = null;
  function loadIds() {
    if (ecoIds) return Promise.resolve(ecoIds);
    return fetch(ROOT + 'tarot/_eco_ids.json').then(function (r) { return r.json(); }).then(function (j) { return (ecoIds = j.ids || {}); }, function () { return (ecoIds = {}); });
  }
  var CSS = '' +
    '.ra-row{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;align-items:center}' +
    '.ra-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid var(--line,#d8d2c6);background:transparent;color:var(--ink-soft,#4a4439);font:500 14px var(--sans,system-ui);cursor:pointer;text-decoration:none;box-sizing:border-box}' +
    '.ra-btn:hover{border-color:var(--gold,#9a7322);color:var(--ink,#221f1a)}' +
    '.ra-btn:focus-visible{outline:3px solid var(--gold,#9a7322);outline-offset:2px}' +
    '.ra-btn.ra-primary{background:var(--gold,#9a7322);border-color:var(--gold,#9a7322);color:#fff;font-weight:600;font-size:16px;min-height:48px;padding:0 24px}' +
    '.ra-btn.ra-primary:hover{filter:brightness(1.07);color:#fff}' +
    '.ra-p{font-family:var(--serif-body,Georgia,serif);font-size:16px;line-height:1.6;color:var(--ink-soft,#4a4439);margin:0 0 12px}' +
    '.ra-small{font-family:var(--sans,system-ui);font-size:12.5px;line-height:1.5;color:var(--mut,#6b6457);margin:10px 0 0}' +
    '.ra-slot{margin:14px 0 0;padding:10px 12px;border:1px dashed var(--line,#d8d2c6);border-radius:8px;font-family:var(--sans,system-ui);font-size:13px;color:var(--mut,#6b6457)}' +
    '.ra-slot:empty{display:none}';
  function css() {
    if (document.getElementById('ra-css')) return;
    var s = document.createElement('style'); s.id = 'ra-css'; s.textContent = CSS; document.head.appendChild(s);
  }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

  // The launcher loads after this page (assistant.js is deferred): wait for it, up to ~10 s.
  function whenAssistant(cb, tries) {
    var RA = global.RecursiveAssistant;
    if (RA && typeof RA.open === 'function') return cb(RA);
    if ((tries || 0) > 40) return cb(null);
    setTimeout(function () { whenAssistant(cb, (tries || 0) + 1); }, 250);
  }

  function castManually(st, note) {
    loadIds().then(function (ids) {
      var opts = { tab: 'tarot', manual: true };
      if (ids[st.deckSlug]) opts.deckId = ids[st.deckSlug];
      if (APP_SPREAD[st.spreadId]) opts.spread = APP_SPREAD[st.spreadId];
      whenAssistant(function (RA) {
        if (!RA) { if (note) note('The assistant is not ready. Tap the star button at the bottom of the page.'); return; }
        RA.open(opts);
      });
    });
  }

  // Staged ask with the photo button; older launchers fall back to staging the text only.
  function askWithPhoto(text, note) {
    whenAssistant(function (RA) {
      if (!RA) { if (note) note('The assistant is not ready. Tap the star button at the bottom of the page.'); return; }
      if (typeof RA.ask === 'function') { RA.ask(text, { photo: true }); return; }
      RA.open();
      var ifr = document.querySelector('.rec-assistant-shell iframe'), origin;
      try { origin = new URL(ifr.src).origin; } catch (e) { origin = RA.flowBaseUrl && RA.flowBaseUrl(); }
      var msg = { type: 'recursive-eco:ask', id: 'picture-reading', text: text, send: false };
      var send = function () { try { ifr.contentWindow.postMessage(msg, origin); } catch (e) {} };
      send(); setTimeout(send, 1500);
    });
  }

  function openPicturePopup(o) {
    css(); o = o || {};
    var owner = o.mode === 'owner';
    var deck = String(o.deckName || 'tarot').replace(/ \(Golden Dawn\)$/, ''), spread = o.spreadName || 'my spread';
    var pos = (o.positions || []).map(function (p) { return typeof p === 'string' ? p : p.label; });
    var d = SiteDialog.open({ title: 'Read from my picture' });
    var b = d.body;
    if (owner) {
      b.appendChild(el('p', 'ra-p', 'You have the ' + deck + ' deck. Cast your cards on a table, left to right' + (pos.length ? ' (' + pos.join(', ') + ')' : '') + ', and take a photo of them in the assistant. It reads the cards it sees.'));
    } else {
      b.appendChild(el('p', 'ra-p', 'This needs a physical deck. Cast the cards on a table, take a photo in the assistant, and it reads the cards it sees.'));
    }
    // Nov 26 2026 (her ask): the spread on the table may not be the page's. Pick one of the
    // Spread Caster's spreads, or "my own spread": the assistant then asks for its positions and
    // offers to save it as a spread.
    var OWN = '__own__';
    var pick = el('label', 'ra-small', 'The spread on your table');
    pick.style.display = 'block'; pick.style.margin = '0 0 4px';
    var sel = document.createElement('select'); sel.className = 'ra-btn'; sel.style.width = '100%'; sel.style.textAlign = 'left';
    sel.setAttribute('aria-label', 'The spread on your table');
    var cur = document.createElement('option'); cur.value = ''; cur.textContent = spread + (pos.length ? ' (' + pos.length + (pos.length === 1 ? ' card)' : ' cards)') : ''); sel.appendChild(cur);
    var own = document.createElement('option'); own.value = OWN; own.textContent = 'My own spread: I will describe it'; sel.appendChild(own);
    var others = [];
    fetch(ROOT + 'viewers/spreads.json').then(function (r) { return r.json(); }).then(function (j) {
      others = (j.spreads || []).filter(function (s) { return s && s.name && s.name !== spread && Array.isArray(s.positions); });
      others.forEach(function (s, i) {
        var o2 = document.createElement('option'); o2.value = String(i);
        o2.textContent = s.name + ' (' + s.positions.length + (s.positions.length === 1 ? ' card)' : ' cards)');
        sel.insertBefore(o2, own);
      });
    }).catch(function () {});
    var hint = el('p', 'ra-small'); hint.style.margin = '6px 0 14px';
    function showHint() {
      if (sel.value === OWN) { hint.textContent = 'The assistant will ask what each position means, read your cards, and can save your spread for next time.'; return; }
      var s = sel.value === '' ? null : others[+sel.value];
      var p2 = s ? s.positions.map(function (p) { return typeof p === 'string' ? p : p.label; }) : pos;
      hint.textContent = p2.length ? 'Left to right: ' + p2.join(', ') + '.' : '';
    }
    sel.addEventListener('change', showHint);
    b.appendChild(pick); b.appendChild(sel); b.appendChild(hint); showHint();
    var go = el('button', 'ra-btn ra-primary', 'Take a picture in the assistant'); go.type = 'button';
    var note = el('p', 'ra-small'); note.setAttribute('role', 'status');
    go.addEventListener('click', function () {
      var text;
      if (sel.value === OWN) {
        text = 'Here is a photo of the cards I cast from my ' + deck + ' deck, in a spread of my own. Before you read them, ask me what each position means, left to right. Then name the cards you see and read them, and offer to save my spread as a new spread so I can use it again.';
      } else {
        var s = sel.value === '' ? null : others[+sel.value];
        var sName = s ? s.name : spread;
        var sPos = s ? s.positions.map(function (p) { return typeof p === 'string' ? p : p.label; }) : pos;
        text = 'Here is a photo of the cards I cast from my ' + deck + ' deck, in the spread ' + sName +
          (sPos.length ? ' (positions left to right: ' + sPos.join(', ') + ')' : '') + '. Please name the cards you see and read them.';
      }
      askWithPhoto(text, function (m) { note.textContent = m; });
      note.textContent = 'The assistant is open with your words ready. Tap the paperclip if no camera button appears.';
    });
    b.appendChild(go);
    b.appendChild(el('p', 'ra-small', 'Tap the paperclip if no camera button appears.'));
    b.appendChild(note);
    // Reserved: a "Buy this deck" link goes here later (the owner adds buy links; see print-products.json).
    var slot = el('div', 'ra-slot'); slot.id = 'ra-buy-slot'; slot.setAttribute('data-slot', 'buy-this-deck');
    b.appendChild(slot);
    return d;
  }

  function renderActions(container, getState) {
    css();
    container.textContent = '';
    var row = el('div', 'ra-row');
    var adv = el('a', 'ra-btn', 'Advanced spreads'); adv.href = ROOT + 'viewers/caster-studio.html';
    var man = el('button', 'ra-btn', 'Cast manually'); man.type = 'button';
    var pic = el('button', 'ra-btn', 'Read from my picture'); pic.type = 'button';
    // The Caster reads ?spread= (a preset id) and ?src= (a deck's grammar path).
    adv.addEventListener('click', function () {
      var st = getState(), q = [];
      if (st.spreadId) q.push('spread=' + encodeURIComponent(st.spreadId));
      if (st.deckSlug) q.push('src=' + encodeURIComponent('../tarot/' + st.deckSlug + '/grammar.json'));
      adv.href = ROOT + 'viewers/caster-studio.html' + (q.length ? '?' + q.join('&') : '');
    });
    man.addEventListener('click', function () { castManually(getState()); });
    pic.addEventListener('click', function () {
      var st = getState();
      openPicturePopup({ mode: 'cast', deckName: st.deckName, spreadName: st.spreadName, positions: st.positions, deckSlug: st.deckSlug });
    });
    row.appendChild(adv); row.appendChild(man); row.appendChild(pic);
    container.appendChild(row);
  }

  global.ReadingActions = { renderActions: renderActions, openPicturePopup: openPicturePopup };
})(window);
