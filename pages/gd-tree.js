/* The Tree of Life, shared by pages/tree-of-life.html and pages/glossary.html.
   Geometry only (where each sephirah sits); WHICH sephiroth a path joins comes from the
   glossary grammar (tarot/glossary-of-tarot/grammar.json → metadata.tree_paths), and each
   path's letter, trump and attribution from the Golden Dawn deck grammar. Colours are
   theme.css tokens. */
(function () {
  // x: -1 left pillar (Severity, as drawn), 0 middle, 1 right (Mercy). y: classic proportions.
  const SEPH = [
    { id: 'kether', n: 1, name: 'Kether', en: 'Crown', x: 0, y: 0 },
    { id: 'chokmah', n: 2, name: 'Chokmah', en: 'Wisdom', x: 1, y: 0.6 },
    { id: 'binah', n: 3, name: 'Binah', en: 'Understanding', x: -1, y: 0.6 },
    { id: 'chesed', n: 4, name: 'Chesed', en: 'Mercy', x: 1, y: 2.3 },
    { id: 'geburah', n: 5, name: 'Geburah', en: 'Severity', x: -1, y: 2.3 },
    { id: 'tiphareth', n: 6, name: 'Tiphareth', en: 'Beauty', x: 0, y: 2.9 },
    { id: 'netzach', n: 7, name: 'Netzach', en: 'Victory', x: 1, y: 4.6 },
    { id: 'hod', n: 8, name: 'Hod', en: 'Splendour', x: -1, y: 4.6 },
    { id: 'yesod', n: 9, name: 'Yesod', en: 'Foundation', x: 0, y: 5.2 },
    { id: 'malkuth', n: 10, name: 'Malkuth', en: 'Kingdom', x: 0, y: 6.9 },
  ];
  const BY = Object.fromEntries(SEPH.map(s => [s.id, s]));
  // Where a path's badge sits along its line (0..1 from the first sephirah); 0.5 unless crowded.
  const BADGE_T = {};

  const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  // Links written into the grammars are absolute (they travel to recursive.eco); on this
  // site, point them at the local copy so they work from any host (and on localhost).
  function localHref(href, here) {
    const m = String(href).match(/^https:\/\/tarot\.recursive\.eco\/(pages|viewers)\/(.*)$/);
    if (!m) return href;
    if (m[1] === 'pages') {
      if (here && m[2].startsWith(here + '#')) return m[2].slice(here.length);
      return m[2];
    }
    return '../viewers/' + m[2];
  }

  // Small markdown: paragraphs, "- " lists, links, **bold**, *italic*.
  function md(s, here) {
    const inline = t => esc(t)
      .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, text, href) => {
        const h = localHref(href.replace(/&amp;/g, '&'), here);
        const ext = /^https?:/.test(h);
        return `<a href="${esc(h)}"${ext ? ' target="_blank" rel="noopener"' : ''}>${text}</a>`;
      })
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|[^*\w])\*([^*\n]+)\*/g, '$1<em>$2</em>');
    return String(s || '').split(/\n{2,}/).map(block => {
      const lines = block.split('\n');
      if (lines.every(l => /^- /.test(l))) return '<ul>' + lines.map(l => `<li>${inline(l.slice(2))}</li>`).join('') + '</ul>';
      return `<p>${inline(lines.join(' '))}</p>`;
    }).join('');
  }

  /* A small tree for icons. opts: {paths:{"22":[a,b],...}, sephirah, path, w} */
  function mini(opts) {
    const P = opts.paths || {}, w = opts.w || 40, u = 13, r = 4.2;
    const X = x => 20 + x * u, Y = y => 6 + y * u;
    let lines = '', dots = '';
    for (const [p, ab] of Object.entries(P)) {
      const a = BY[ab[0]], b = BY[ab[1]];
      if (!a || !b) continue;
      const on = String(opts.path) === String(p);
      lines += `<line x1="${X(a.x)}" y1="${Y(a.y)}" x2="${X(b.x)}" y2="${Y(b.y)}" stroke="${on ? 'var(--gold)' : 'var(--line)'}" stroke-width="${on ? 3 : 1.2}" stroke-linecap="round"/>`;
    }
    const lit = new Set();
    if (opts.sephirah) lit.add(opts.sephirah);
    if (opts.path && P[opts.path]) P[opts.path].forEach(s => lit.add(s));
    for (const s of SEPH) {
      const on = lit.has(s.id);
      dots += `<circle cx="${X(s.x)}" cy="${Y(s.y)}" r="${on ? r + 1 : r}" fill="${on ? 'var(--gold)' : 'var(--surface)'}" stroke="${on ? 'var(--gold)' : 'var(--mut)'}" stroke-width="1"/>`;
    }
    const h = Math.round(w * 103 / 40);
    return `<svg viewBox="0 0 40 103" width="${w}" height="${h}" aria-hidden="true" focusable="false">${lines}${dots}</svg>`;
  }

  window.GDTree = { SEPH, BY, BADGE_T, esc, md, mini, localHref };
})();
