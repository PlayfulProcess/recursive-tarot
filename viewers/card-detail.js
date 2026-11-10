/* viewers/card-detail.js — the standard card detail: one dialog, picture whole, the card's name,
 * the deck's own text for it, and a link to its page where one exists.
 *   CardDetail.open({ deckSlug, nodeId, name, image, deckLabel, position })
 * The text is the card's own entry in tarot/<deckSlug>/grammar.json, fetched through
 * RefResolve.resolveSourceItem (viewers/reference-resolve.js) when that is loaded, so it is the
 * same resolution the Caster, the card viewer and the tree viewer use. Needs viewers/dialog.js.
 * Paths are resolved from this script's own address, so it works from any folder. */
(function (global) {
  'use strict';
  var ROOT = (function () {
    var s = document.currentScript && document.currentScript.src;
    try { return new URL('../', s).href; } catch (e) { return new URL('./', location.href).href; }
  })();
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  // **bold**, *italic*, [text](url), bare paragraphs. Small on purpose.
  function md(s) {
    var t = esc(s);
    t = t.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
         .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
    return t.split(/\n\s*\n/).map(function (p) { return '<p>' + p.replace(/\n/g, '<br>') + '</p>'; }).join('');
  }
  function localSrc(u) { return String(u || '').replace(/^https:\/\/tarot\.recursive\.eco\//, ROOT); }
  function asciiSlug(s, words) {
    s = String(s).split(/[:;,]/)[0];
    return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').split('-').slice(0, words || 7).filter(Boolean).join('-');
  }
  function exists(url) {
    return fetch(url, { method: 'HEAD' }).then(function (r) { return r.ok; }, function () { return false; });
  }
  // The card's own page, where the site has one (Book T, Rider-Waite-Smith); else its deck's page.
  function pageFor(slug, item) {
    var c = [], name = item && item.name || '';
    if (slug === 'book-t' && item) {
      c.push(ROOT + 'book-t/' + (item.category === 'keys' ? item.id : item.id + '-' + asciiSlug(name)) + '.html');
    } else if (slug === 'rider-waite-smith-pictorial-key' || slug === 'golden-dawn-book-t-tarot') {
      var s = asciiSlug(name); c.push(ROOT + 'card/' + s + '.html'); c.push(ROOT + 'card/' + s.replace(/^the-/, '') + '.html');
    }
    c.push(ROOT + (slug === 'book-t' ? 'book-t/index.html' : 'deck/' + slug + '.html'));
    var i = 0;
    return (function next() {
      if (i >= c.length) return Promise.resolve(null);
      var u = c[i++]; return exists(u).then(function (ok) { return ok ? u : next(); });
    })();
  }
  function load(slug, id) {
    if (global.RefResolve && RefResolve.resolveSourceItem) return RefResolve.resolveSourceItem(slug, id);
    return fetch(ROOT + 'tarot/' + encodeURIComponent(slug) + '/grammar.json').then(function (r) { return r.json(); }).then(function (g) {
      var it = (g.nodes || []).filter(function (n) { return n.id === id; })[0];
      return it ? { status: 'ok', item: it, deckLabel: g.name } : { status: 'error' };
    }, function () { return { status: 'error' }; });
  }
  var FIRST = ['Book T (1912)'];
  function sectionKeys(sections, slug) {
    var keys = global.RefResolve && RefResolve.orderedSectionKeys ? RefResolve.orderedSectionKeys(sections) :
      Object.keys(sections || {}).filter(function (k) { return String(sections[k]).trim(); });
    if (slug === 'book-t') keys = FIRST.filter(function (k) { return keys.indexOf(k) >= 0; }).concat(keys.filter(function (k) { return FIRST.indexOf(k) < 0; }));
    return keys;
  }
  function open(o) {
    o = o || {};
    var d = SiteDialog.open({ title: o.name || '', className: 'sd-wide' });
    var b = d.body;
    var style = 'display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap';
    b.innerHTML = '<div class="cd-top" style="' + style + '"></div><div class="cd-text" style="font-family:var(--serif-body,Georgia,serif);font-size:15.5px;line-height:1.65;color:var(--ink-soft,#4a4439);margin-top:14px"><p style="color:var(--mut,#6b6457)">Loading…</p></div>';
    var top = b.querySelector('.cd-top'), txt = b.querySelector('.cd-text');
    var meta = '<div style="flex:1 1 200px;min-width:0;font-family:var(--sans,system-ui);font-size:13px;color:var(--mut,#6b6457)">' +
      (o.position ? '<div style="font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#8a6414">' + esc(o.position) + '</div>' : '') +
      '<div>' + esc(o.deckLabel || '') + '</div><div class="cd-links" style="margin-top:8px"></div></div>';
    var img = o.image ? '<img src="' + esc(localSrc(o.image)) + '" alt="' + esc(o.name || '') + '" style="flex:0 0 auto;width:min(200px,45%);height:auto;max-height:50vh;object-fit:contain;background:var(--thumb-bg,#faf8f3);border:1px solid var(--line,#d8d2c6);border-radius:8px">' : '';
    top.innerHTML = img + meta;
    var links = b.querySelector('.cd-links');
    load(o.deckSlug, o.nodeId).then(function (r) {
      if (r.status !== 'ok') { txt.innerHTML = '<p>The card’s text would not load.</p>'; return null; }
      var it = r.item, s = it.sections || {}, keys = sectionKeys(s, o.deckSlug), h = '';
      if (it.keywords && it.keywords.length) h += '<p style="font-family:var(--sans,system-ui);font-size:12.5px;color:var(--mut,#6b6457)">' + it.keywords.map(esc).join(' · ') + '</p>';
      keys.forEach(function (k, i) {
        h += '<h3 style="font-family:var(--sans,system-ui);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#8a6414;margin:' + (i ? '18px' : '0') + ' 0 4px">' + esc(String(k).replace(/_/g, ' ')) + '</h3>' + md(s[k]);
      });
      txt.innerHTML = h || '<p>This deck has no text for the card yet.</p>';
      return pageFor(o.deckSlug, it);
    }).then(function (u) {
      if (u) links.innerHTML = '<a href="' + esc(u) + '" style="color:var(--gold,#9a7322);display:inline-block;min-height:44px;line-height:44px">Open its page →</a>';
    });
    return d;
  }
  global.CardDetail = { open: open };
})(window);
